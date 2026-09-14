# Three mechanisms and their failed gates

## 1. Norm-preserving 5-neighbor descent

State: (n,c,q∈H), N(q)=n-3^c>0. Maps: every legal alpha q beta/5 and the
explicit finite symmetry group G. Norm and n are preserved; integrality is
fully classified.

Two genuinely different arithmetic heights were tested, with all favorable
symmetries already allowed. For a G orbit O, let

    H_bad(O)=min bad5(x_i²+x_j²),
    H_Omega(O)=min Omega(bad5(x_i²+x_j²)),

where the minima range over integral members, unordered coordinate pairs,
and positive pair norms. Here bad5(s)=s/5^v5(s), and Omega counts prime factors
with multiplicity. H_bad=1 and H_Omega=0 are exactly the target condition.
A logarithm of H_bad is the same ordering, not a third mechanism.

These heights do not provide descent. M-D1 excludes *any* universal
well-founded target-terminating height on all states in this move family.
M=81 gives a primitive, target-accessible local minimum for H_Omega.
M=1175 gives a primitive, target-accessible state whose H_bad must rise from
2 to at least 13 on every target path, even if plateaus are allowed.
The exact statements and finite certificates are in COUNTEREXAMPLES.md.

A graph-distance-to-target function decreases along a shortest path only once
a target's existence and accessibility are already known. It is not an
independent arithmetic descent or a proof that all relevant shells hit the
target. The computed BFS distances are diagnostic data only.

D1–D4 and the intended terminal interpretation are explicit; the required
universal D5 strict decrease fails. There is no Level B theorem here.

## 2. Factor transfer / Gaussian Euclidean operations

The universal statement 'if ell≠5 divides N(w), transfer one ell-adic defect
to z at fixed norm' is false without further hypotheses. At q=(1,1,1,1),
N(q)=4 and N(w)=2. Every integral representation of 4 has every positive pair
norm even, so no output can lower v2(N(w)) from 1 to 0. Taking w'=0 does not
satisfy a pure-power terminal condition. The same target obstruction occurs
on every shell 4·25^k.

Quaternion Euclidean division supplies a smaller **remainder norm**. It does
not preserve the shell N(q)=M, and its factorization consequences do not imply
a monotone defect of a selected coordinate pair. Refactorizations using only
the norm-5-generated action still preserve kappa_5. No general statement
about arbitrary prime denominators is proved.

The universal SL2(Z[i]) left/right preserving subgroup is finite by M-D2 in
MATRIX_MODEL.md. Thus ordinary Gaussian row/column reduction cannot be
imported as a universal shape-preserving fixed-norm descent. State-specific
maps outside that subgroup were not proved impossible; no terminating one
was found in this task.

## 3. Minimal-counterexample lift coupled to 3-power choice

The displayed coordinate shift in MINIMAL_COUNTEREXAMPLE.md preserves n under
an exact representation-dependent hypothesis. That hypothesis fails on a
complete small shell, and no strict target height accompanies it. M-D3 rules
out every fixed finite displacement list with bounded exponent jumps as a
universal remedy, including after arbitrary fixed-norm preprocessing.

No valid lift from the known representations of all smaller n has been
established for a hypothetical least counterexample. Accordingly this
mechanism fails the promotion gate too.

## Stop decision

All three tested mechanisms have met a concrete failure gate. The decision is
PAUSE, not another density heuristic, original-n scan, or automatic Phase M2.
The retained result is a Level D pruning package, with no claimed universal
impossibility of representation-dependent quaternion methods.
