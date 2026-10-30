# -*- coding: utf-8 -*-
import json
from client import GenParkScreenContext

sc = GenParkScreenContext()

# 1. AXTree Coordinate Normalization
nodes = [
    {"id": "btn_buy", "role": "button", "label": "Proceed to Checkout", "box": {"x": 800, "y": 450, "w": 320, "h": 60}},
    {"id": "link_terms", "role": "link", "label": "Terms of Service", "box": {"x": 900, "y": 950, "w": 120, "h": 20}},
    {"id": "hidden_div", "role": "generic", "box": {"x": 0, "y": 0, "w": 0, "h": 0}}
]
norm = sc.resolve_axtree_bounding_boxes(nodes, 1920.0, 1080.0)
print(f"AXTree Normalized: {norm['total_nodes_parsed']} nodes ({norm['interactive_targets_count']} interactive)")
for n in norm["normalized_elements"]:
    print(f"  {n['node_id']} ({n['role']}): Pos=({n['center_normalized']['cx']}, {n['center_normalized']['cy']})")

# 2. Viewport Occlusion & Clipping
elements = [
    {"id": "hero_banner", "label": "Hero Banner", "box": {"x": 0, "y": 0, "w": 1920, "h": 500}},
    {"id": "partially_offscreen", "label": "Footer Banner", "box": {"x": 0, "y": 1000, "w": 1920, "h": 200}}, # 80px visible
    {"id": "completely_offscreen", "label": "Offscreen Section", "box": {"x": 0, "y": 1500, "w": 1920, "h": 400}}
]
clipping = sc.calculate_viewport_occlusion_and_clipping(elements)
print()
print(f"Viewport Clipping Audit: FullyVisible={clipping['fully_visible_count']} | Clipped={clipping['clipped_count']} | Offscreen={clipping['offscreen_count']}")
for e in clipping["elements"]:
    print(f"  {e['id']}: Visibility={e['visibility_ratio']*100}% | Prominence={e['prominence_score']}/100")

# 3. Omnichannel Intent Matching
tokens = ["cart", "proceed", "checkout", "shipping", "subtotal", "$49.99"]
intent = sc.match_omnichannel_intent_trigger(tokens)
print()
print(f"Screen Intent Match: Primary='{intent['primary_intent']}' (HighConfidence={intent['has_high_intent_trigger']})")
print(f"  Details: {intent['detected_intents']}")
