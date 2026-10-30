# genpark-screen-context

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-zero-success)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

GenPark Screen Context is a zero-dependency autonomous UI agent perception engine implementing Accessibility Tree (AXTree) coordinate bounding box normalization, viewport occlusion and clipping polygon analysis, and real-time omnichannel e-commerce intent trigger detection.

```mermaid
flowchart TD
    A[Raw Accessibility Tree Nodes] --> B[AXTree Normalizer]
    B --> C[Normalized Center & Interactive Bounding Boxes]
    D[Candidate Elements & Viewport Bounds] --> E[Occlusion & Clipping Polygon Solver]
    E --> F[Visibility Ratio & Visual Prominence Score]
    G[DOM Screen Text Tokens] --> H[Omnichannel Intent Pattern Engine]
    H --> I[Checkout, Price Comparison & Cancellation Alerts]
```

## Features
- **AXTree Coordinate Normalizer**: Maps arbitrary screen resolutions to unit $[0, 1]$ bounding box vectors and interactive element classifications.
- **Viewport Occlusion Solver**: Computes geometric intersection, offscreen detection, and center-weighted visual prominence scores.
- **Omnichannel Intent Matcher**: Detects purchase, price comparison, and churn risk triggers from DOM token streams.

## Quickstart

```python
from client import GenParkScreenContext

sc = GenParkScreenContext()
res = sc.match_omnichannel_intent_trigger(["checkout", "order", "total"])
print("Intent:", res["primary_intent"])
```

## License
MIT
