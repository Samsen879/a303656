# Candidate design comparison

All candidates are T-blind preregistration candidates only; none is authorized for evaluation.

| Design | Integers | Per-band projections | Per-band masks | raw G | Main limitation |
|---|---:|---|---|---|---|
| A | 384 | 2/2/2 | 4/4/4 | 227/227/227 | strict 384-point blueprint |
| B | 288 | 3/3/3 | 3/3/3 | 227/227/227 | more raw-G-matched projection diversity; 288 points |
| C | 480 | 5/5/5 | 5/5/5 | 222,223,225,228/226,227/226,227,228 | all five H8=201 projections; residual raw-G/projection confounding |

Design A follows the proposed 3×2×2×4×8 hierarchy exactly. Design B uses three projections per band, one mask per projection, four classes per mask, and eight integers per class. Design C uses five projections per band to include all five accepted H8=201 projections; it therefore cannot retain exact raw-G matching.
