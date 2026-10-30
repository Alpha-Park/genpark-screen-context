# -*- coding: utf-8 -*-
"""
GenPark Screen Context FastMCP Server
"""

import json
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from client import GenParkScreenContext

mcp = FastMCP("genpark-screen-context")
ctx = GenParkScreenContext()

@mcp.tool()
def resolve_axtree_bounding_boxes(
    ax_nodes_json: str,
    viewport_width: float = 1920.0,
    viewport_height: float = 1080.0
) -> str:
    """
    Normalizes Accessibility Tree (AXTree) element bounding boxes to [0.0, 1.0] viewport space.
    """
    nodes = json.loads(ax_nodes_json)
    res = ctx.resolve_axtree_bounding_boxes(nodes, viewport_width, viewport_height)
    return json.dumps(res, indent=2)

@mcp.tool()
def calculate_viewport_occlusion_and_clipping(
    candidate_elements_json: str,
    viewport_rect_json: Optional[str] = None
) -> str:
    """
    Calculates clipping polygon intersection and visibility ratio against viewport boundaries.
    """
    elements = json.loads(candidate_elements_json)
    vp = json.loads(viewport_rect_json) if viewport_rect_json else None
    res = ctx.calculate_viewport_occlusion_and_clipping(elements, vp)
    return json.dumps(res, indent=2)

@mcp.tool()
def match_omnichannel_intent_trigger(
    dom_text_tokens_json: str,
    intent_patterns_json: Optional[str] = None
) -> str:
    """
    Matches real-time screen tokens against e-commerce and SaaS behavioral intent triggers.
    """
    tokens = json.loads(dom_text_tokens_json)
    patterns = json.loads(intent_patterns_json) if intent_patterns_json else None
    res = ctx.match_omnichannel_intent_trigger(tokens, patterns)
    return json.dumps(res, indent=2)

def main():
    print("Testing Screen Context:")
    print(match_omnichannel_intent_trigger(json.dumps(["checkout", "order", "total"])))

if __name__ == "__main__":
    main()
