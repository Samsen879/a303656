# Exact terminal-state recursion with ordinary-axis pruning

Fix an inert terminal \(q>23\) and condition on the small-head chosen class \(c,d\bmod3960\) used in the [effective first-blocking bound](SINGLE_WITNESS_COVER_TREE_DENSITY_BOUND.md). The following finite-state calculation is exact for first blocking **of that phase class**. An unrestricted blocker must also block the chosen class eventually, but the two first terminal primes need not agree.

Retain both exponent order residues at \(q\). Descend through older inert primes \(p>23\). Let \(\ell_b(p)\) be the \(p\)-primary depth of exponent axis \(b\) required by the retained later tests or by the initial class, and \(e_b(p)=v_p(b^{p-1}-1)\). If \(k_p=\min_b(e_b(p)+\ell_b(p))=1\), drop this old test: one ordinary axis has its own digits unconsumed. Otherwise retain the row as a test at depth \(k_p\) and retain its earlier unit-order digits. A passing residue has even valuation below \(k_p\), or lies in the zero ball. The fastest available unconsumed axis fills that ball. Therefore the retained tests are necessary and sufficient for existence of an extension at each fixed terminal-order pair: once a projected point passes, restore the omitted tests and zero-ball own digits in increasing prime order, without changing the retained digits. Ordinary retained tests can only occur where all their ordinary axes are read later. If \(p\mid\operatorname{ord}_s(b)\) for a later inert \(s\), then \(s\ge2p+1\); ordinary tests above \(q/2\) need not be retained.

Let \(\mathcal U\) be the **whole** finite retained phase space. For each retained \(p\), \(A_p(t)\subseteq\mathcal U\) is the exact pass set at \(n_p=t\bmod p^{k_p}\). Group observations with the same pass set, writing \(c_p(A)\) for their count. Traverse the retained rows with state \(F\subseteq\mathcal U\), initially \(\mathcal U\). Intersect with \(A\) at transition probability \(c_p(A)/p^{k_p}\); empty states can be discarded since they already fail the old prefix. Haar readings at distinct rows remain independent given the chosen initial small-head class. At the end multiply each nonempty \(F\) by
\[
 q^{-e_q}\#\{t\bmod q^{e_q}:A_q(t)\cap F=\varnothing\},\qquad
 e_q=\min_b e_b(q).
\]
Summing gives the exact conditional probability. The terminal depth only uses \(e_q\) because no \(q\)-primary digits are read earlier. If \(F\) has at least two distinct first terminal shifts the multiplier is zero. If \(e_q=2\) and all terminal shifts have one first digit and \(m\) distinct second-digit lifts, it is \((q-m)/q^2\). In either row or terminal counting the observation tree can aggregate a subtree once it has separated from all shift centers: parity of the separation depth fixes each status. It is not safe to merge states using only their axis marginals, or discard an entire head because a selected reset trajectory is empty.

## A convergent rigorous tail for a finite cutoff

Exact calculations through \(X\ge9\cdot10^{14}\) can be combined with a uniform upper bound for the rest. Retain the original [explicit high/low order envelopes](SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md). Set \(K=\max(27,\lfloor(3/4)\log X\rfloor)\) and \(L=\log K+1/2\). The low-order dyadic contribution beyond \(X\) is bounded by
\(\log(3) X^{-21/125}/[\log X(1-2^{-21/125})]\).
The remaining source powers satisfy \(D>K\), with reciprocal envelope \(R_D\le S_D\le(3/2)(\log D+1/2)/D\), depth charge at most \(D^{-1/2}\), and reader charge at most \(3S_D^2\) from the one-digit tree. Bounding the prime powers by all integers \(D>K\) and integrating both decreasing functions gives the additional tail
\[
 \frac{3(\log K+5/2)}{\sqrt K}
 +\frac{81}{8K^2}\left(\frac{L^3}{2}+\frac{3L^2}{4}
                           +\frac{3L}{4}+\frac38\right).
\]
This tends to zero but is not an improvement to the existing \(0.0876\%\) all-tail certificate without further arithmetic. The ten-target theorem for unlocked phases is not asserted to apply inside the preloaded class.

In the replay a single ordinary source (31) can be removed at one ordinary terminal but not another, depending on the separate axis reads. The 31-state counts really are nonuniform (a line or the full grid). Separately a fully covered nine-phase trajectory and a distinct surviving phase coexist at the same old observations. None of the sample terminals is a true rare first blocker.

~~~python
from collections import Counter
from math import lcm

C = 3960
def order(b, p):
    return next(j for j in range(1, p) if pow(b,j,p)==1)
def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

assert [order(b,5023) for b in (3,5)] == [5022,162]
assert [order(b,683) for b in (3,5)] == [31,682]
assert all(pow(b,30,31**2)!=1 for b in (3,5))
n = 2272216023
assert (n-S(C,C,31**2)) % 31**2 == 31
assert (n-S(C,360360,31**3)) % 31**3 == 23*31**2
assert (360360-C) % lcm(C,162) == 0
assert pow(5,C,683) != pow(5,360360,683)

centers = [S(C*(i+1),C*(j+1),31**2)
           for i in range(31) for j in range(31)]
sizes = Counter(sum((t-s)%31 != 0 or (t-s)%31**2 == 0
                    for s in centers)
                for t in range(31**2))
assert sizes == {961:930, 31:31}

n = 418327968725963073627290346158715
ps = (379,1567,163,487,811)
step = 706910912918687058120
hits = [{j for j in range(9)
         if (n-S(C+step*j,C,p*p))%(p*p) in range(p,p*p,p)}
        for p in ps]
assert hits == [{0,3,6},{1,4,7},{2},{5},{8}]
assert len({S(C+step*j,C,3727) for j in range(9)}) == 9
c = 185596159320
assert c%C == 0
for p in ps:
    u = (n-S(c,C,p**3)) % p**3
    assert u%p or u in range(p*p,p**3,p*p)

~~~
