# Computation notes and scope clarification

The original specification and its pre-run addendum are retained unchanged.
The regular skeleton {3,7,31}, K=2, E={1}, r=2, has actual coarse U=6.
During proof audit, the prescribed period 1302 in the addendum was also
identified as the ACTUAL FULL period L=lcm(6,42,93)=1302 of those three rows.
Thus its 1300 covered / 2 common-safe full-period cells are an actual
shared-residue arithmetic result, not a surrogate model.

What remains conditional is promotion of 1302 to a COARSE support period and
closure of the two surviving cells by an actual nonregular terminal prime.
No such prime is supplied by this package. The implementation checks both
period equalities. The addendum's warning against claiming an induced coarse
U=1302 remains essential and correct.

The selected mixed nonregular-row checks use q=20771, K=4, E={1,3}, one
shared residue, and six exponent offsets at each anchor. The complete period
w_q*q^2 is NOT enumerated. The global row classification follows from the
symbolic principal-subgroup/LTE proof, not from those twelve sample points.
