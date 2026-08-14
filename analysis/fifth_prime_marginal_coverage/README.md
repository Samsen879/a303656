# Exact fifth-prime marginal-coverage landscape

This module performs exact modular combinatorial analysis only. It never evaluates a new integer, calls a `T` backend, calls a direct two-square oracle, or runs a P5 CRT integer search.

The authenticated prime authority is read directly from the tracked Stage-0 ZIP and checked against both the archive SHA256 and its embedded member SHA256. The bound remains exactly `B=5000`. The fixed 407-pair domain and all 13 frozen P4 masks are checked against prior certified authorities.

For each candidate `q`, the complete `q^2` landscape is represented by an exact partition. For a fixed residue `r mod q`, all pairs with `shift == r mod q` are covered on every one of the `q` lifts except that a pair is excluded on its unique `shift mod q^2` lift. Residues `r` with no pair contribute `q` empty lifts. These multiplicities sum exactly to `q^2`.

`enumerator_a.py` accumulates direct mod-`q^2` exclusion events. `enumerator_b.py` independently constructs mod-`q` buckets and mod-`q^2` exclusions, with separate score aggregation. The literal oracle loops over every residue for predeclared small primes and computes valuations by repeated exact division.

The resulting `G5` and residual counts are guaranteed P4/P5 prime-square-persistent coverage only. They are not `T`, counterexample proximity, or authorization for integer search. The global A303656 problem remains **UNRESOLVED**.
