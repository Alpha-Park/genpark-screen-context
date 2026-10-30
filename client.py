# -*- coding: utf-8 -*-
"""
GenPark Screen Context Client
Zero-dependency Accessibility Tree (AXTree) coordinate normalizer,
viewport occlusion clipping polygon solver, and omnichannel intent trigger matcher.
"""

import math
from typing import Dict, List, Any, Optional

class GenParkScreenContext:
    """
    Parses Accessibility Tree (AXTree) coordinates, computes viewport occlusion clipping,
    and matches real-time user intent triggers from DOM tokens.
    """

    DEFAULT_INTENTS = {
        "checkout_intent": ["cart", "checkout", "buy", "pay", "total", "shipping", "order", "place order"],
        "price_comparison": ["compare", "versus", "vs", "competitor", "alternative", "pricing", "plans"],
        "cancellation_risk": ["cancel", "unsubscribe", "refund", "downgrade", "billing error", "terminate"],
        "support_inquiry": ["help", "contact", "support", "ticket", "faq", "chat", "live agent", "issue"]
    }

    def resolve_axtree_bounding_boxes(
        self,
        ax_nodes: List[Dict[str, Any]],
        viewport_width: float = 1920.0,
        viewport_height: float = 1080.0
    ) -> Dict[str, Any]:
        """
        Normalizes Accessibility Tree (AXTree) element bounding boxes to [0.0, 1.0] viewport space.
        """
        if viewport_width <= 0 or viewport_height <= 0:
            raise ValueError("Viewport dimensions must be strictly positive.")

        normalized_nodes = []
        interactive_count = 0

        for node in ax_nodes:
            box = node.get("box", {})
            x = box.get("x", 0.0)
            y = box.get("y", 0.0)
            w = box.get("w", 0.0)
            h = box.get("h", 0.0)

            # Skip zero-sized elements
            if w <= 0 or h <= 0:
                continue

            # Normalized coordinates
            nx = round(x / viewport_width, 4)
            ny = round(y / viewport_height, 4)
            nw = round(w / viewport_width, 4)
            nh = round(h / viewport_height, 4)
            cx = round(nx + nw / 2.0, 4)
            cy = round(ny + nh / 2.0, 4)

            role = node.get("role", "generic")
            is_clickable = role in ["button", "link", "checkbox", "radio", "menuitem", "tab", "combobox"]
            if is_clickable:
                interactive_count += 1

            normalized_nodes.append({
                "node_id": node.get("id", "ax_node"),
                "role": role,
                "label": node.get("label", ""),
                "is_interactive": is_clickable,
                "bounding_box_normalized": {"x": nx, "y": ny, "w": nw, "h": nh},
                "center_normalized": {"cx": cx, "cy": cy}
            })

        return {
            "viewport": {"width": viewport_width, "height": viewport_height},
            "total_nodes_parsed": len(normalized_nodes),
            "interactive_targets_count": interactive_count,
            "normalized_elements": normalized_nodes
        }

    def calculate_viewport_occlusion_and_clipping(
        self,
        candidate_elements: List[Dict[str, Any]],
        viewport_rect: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculates clipping polygon intersection and visibility ratio against viewport boundaries.
        """
        vp = viewport_rect or {"x": 0.0, "y": 0.0, "w": 1920.0, "h": 1080.0}
        vx1, vy1 = vp["x"], vp["y"]
        vx2, vy2 = vx1 + vp["w"], vy1 + vp["h"]

        audited_elements = []

        for elem in candidate_elements:
            box = elem.get("box", {})
            ex1 = box.get("x", 0.0)
            ey1 = box.get("y", 0.0)
            ew = box.get("w", 100.0)
            eh = box.get("h", 100.0)
            ex2 = ex1 + ew
            ey2 = ey1 + eh
            total_area = max(1e-9, ew * eh)

            # Intersection rect
            ix1 = max(vx1, ex1)
            iy1 = max(vy1, ey1)
            ix2 = min(vx2, ex2)
            iy2 = min(vy2, ey2)

            iw = max(0.0, ix2 - ix1)
            ih = max(0.0, iy2 - iy1)
            visible_area = iw * ih
            visibility_ratio = round(visible_area / total_area, 3)

            # Center distance to viewport center
            vp_cx, vp_cy = (vx1 + vx2) / 2.0, (vy1 + vy2) / 2.0
            elem_cx, elem_cy = (ex1 + ex2) / 2.0, (ey1 + ey2) / 2.0
            dist_to_center = math.hypot(elem_cx - vp_cx, elem_cy - vp_cy)

            # Visual prominence score (0 to 100): Visibility * (1 - normalized center distance)
            max_dist = math.hypot(vp["w"], vp["h"]) / 2.0
            norm_dist = min(1.0, dist_to_center / max(1e-9, max_dist))
            prominence = round(visibility_ratio * (1.0 - 0.5 * norm_dist) * 100.0, 1)

            audited_elements.append({
                "id": elem.get("id", "elem"),
                "label": elem.get("label", ""),
                "visibility_ratio": visibility_ratio,
                "is_fully_visible": visibility_ratio >= 0.99,
                "is_clipped": 0.0 < visibility_ratio < 0.99,
                "is_offscreen": visibility_ratio == 0.0,
                "prominence_score": prominence
            })

        # Sort by prominence
        audited_elements.sort(key=lambda x: x["prominence_score"], reverse=True)

        return {
            "viewport_bounds": vp,
            "elements_evaluated": len(audited_elements),
            "fully_visible_count": sum(1 for e in audited_elements if e["is_fully_visible"]),
            "clipped_count": sum(1 for e in audited_elements if e["is_clipped"]),
            "offscreen_count": sum(1 for e in audited_elements if e["is_offscreen"]),
            "elements": audited_elements
        }

    def match_omnichannel_intent_trigger(
        self,
        dom_text_tokens: List[str],
        intent_patterns: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Matches real-time screen tokens against e-commerce and SaaS behavioral intent triggers.
        """
        patterns = intent_patterns or self.DEFAULT_INTENTS
        token_set = set(t.strip().lower() for t in dom_text_tokens)

        matched_intents = {}

        for intent_name, keywords in patterns.items():
            matches = [k for k in keywords if k in token_set or any(k in t for t in token_set)]
            if matches:
                # Confidence based on match count
                conf = round(min(1.0, len(matches) / math.sqrt(len(keywords))), 3)
                matched_intents[intent_name] = {
                    "matched_keywords": matches,
                    "trigger_confidence": conf
                }

        # Identify primary intent
        primary_intent = max(matched_intents, key=lambda k: matched_intents[k]["trigger_confidence"]) if matched_intents else None

        return {
            "tokens_scanned": len(dom_text_tokens),
            "primary_intent": primary_intent,
            "has_high_intent_trigger": any(i["trigger_confidence"] >= 0.60 for i in matched_intents.values()),
            "detected_intents": matched_intents
        }
