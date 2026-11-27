# Boundary-aware LTE elimination and a two-row marginal collision

Consider the finite pre-lift test from [the fixed-panel construction](FIXED_PANEL_EVEN_VALUATION_CONSTRUCTION.md), with possibly prescribed boundary congruences \(c=c_0\bmod B_3\) and \(d=d_0\bmod B_5\) incorporating the seed. For each panel row \(p>3\) and \(b\in\{3,5\}\), put
\[
 o_{b,p}=\operatorname{ord}_p b,\quad
 r_{b,p}=o_{b,p}/\gcd(o_{b,p},B_b),\quad
 T_b=\operatorname{lcm}_{p}r_{b,p},\quad
 h_{b,p}=v_p(b^{o_{b,p}}-1)+v_p(B_b).
\]
The free exponent parameters \(x_b\), where the exponent is \(c_0+B_3x_3\) or \(d_0+B_5x_5\), are reduced modulo \(T_b\). The residual's truncated depth is \(t_p=\min_b(h_{b,p}+v_p(T_b))\). The exact test rejects a nonzero residue of odd valuation mod \(p^{t_p}\). A passing cell extends to full even valuations in the finite panel by increasing the free parameters by multiples of \(T_b\) and applying LTE plus the prime-by-prime CRT. Representatives must still meet the ordinary height bound for strict activity.

## Preserve the chosen boundary

Call \(p\) a root if neither base \(b\) has both \(v_p(b^{o_{b,p}}-1)=1\) and \(p\nmid B_b\). Keep the roots and their order-factor ancestors: keep \(p\) if a kept \(q\) has \(p\mid o_{3,q}o_{5,q}\), and repeat to closure. Remove the other rows and restore them in ascending order. To restore a removed \(p\), choose a base with the two stated properties. Adjust that free parameter by multiples of the prime-to-\(p\) part of \(T_b\). No accepted smaller row or kept larger row reads this \(p\)-coordinate. LTE adjusts the residual, when necessary, to zero modulo \(p^{t_p}\) without changing any previously satisfied row or the actual boundary. In particular an ordinary row need not be removable once an external boundary fixes its relevant low digits.

## Exact cylinder calculus and an inexpensive sufficient test

Fix the other base's residue to examine one axis at row \(p\). Collision modulo \(p\) uses at most one residue \(x_b\equiv x_0\bmod r_{b,p}\). In this cylinder write \(x_b=x_0+r_{b,p}k\). If \(t_p\le h_{b,p}\) or the residual does not vanish modulo \(p^{h_{b,p}}\), the rejection predicate on the cylinder is constant. Otherwise the principal-unit orbit gives a unique \(k_*\bmod p^{t_p-h_{b,p}}\) and the truncated valuation is
\[
 \min(t_p,h_{b,p}+v_p(k-k_*)).
\]
Treating the congruent case as truncated depth \(t_p\), this yields rejection as a disjoint union of differences of nested congruence cylinders. When both axes are free, one may enumerate the smaller local axis period and apply this decomposition to the other axis. Intersections of cylinders on a common axis are empty if residues disagree modulo the gcd, and otherwise are one cylinder by CRT. Expanding the product of per-row acceptance indicators counts exact extensions without having to materialize the whole joint period table, though the expansion can itself be large.

For a cheaper sufficient certificate, let \(E_i\) be row rejection events on the uniform free parameters in a block with fixed boundary. For any forest \(F\) of row intersections,
\[
 \Pr(\bigcup E_i)\le\sum_i\Pr(E_i)-\sum_{ij\in F}\Pr(E_i\cap E_j).
\]
At a point belonging to \(k>0\) bad sets, the induced forest has at most \(k-1\) edges, giving the pointwise proof. All terms can be counted by the cylinder calculus. A bound strictly below 1 gives an extension; an upper bound of 1 alone gives none. No row independence is assumed.

## A genuine fixed-boundary collision

Let \(a=35875+543606\cdot5^{5418}\), \(n=3^{903}+5^{1032}+a^2\), and take panel \(\{7,43\}\). Use the boundary \(c\equiv129\bmod258,\ d\equiv258\bmod774\). The coarse cell representatives are \(c=129+258u,\ d=258+774v\) for \(u,v\in\mathbb F_7\). Both pre-lift depths equal 2: the mod-43 orders of both bases are 42, both boundary moduli contain 43, and the free-period quotient for each axis is 7. Both bases have initial lifting depth one at 7 and 43.

Direct modular powering gives 7 acceptance iff \(v=5u\), and 43 rejection iff \(v=3u\). At each fixed \(v\), 7 accepts one cell and 43 accepts six. For \(v=0\) there is no simultaneous pass, while for \(v=1\) there is exactly one, at \(u=3\), with the independent true square \(a^2\). The two bad sets are disjoint along \(v=0\) and intersect in one cell along \(v=1\). Thus the per-row marginals do not determine the extension count, including when all rows are ordinary. Freeing both parameters gives six simultaneous passes. This is a finite interface control, not a full-prefix or original-conjecture claim.

```python
def target(m):
    a = (35875 + 543606*pow(5,5418,m)) % m
    return (pow(3,903,m)+pow(5,1032,m)+a*a) % m

def accepts(p,c,d):
    m=p*p
    z=(target(m)-pow(3,c,m)-pow(5,d,m))%m
    return z==0 or z%p!=0

for b in (3,5):
    for p,o in ((7,6),(43,42)):
        assert next(i for i in range(1,p) if pow(b,i,p)==1)==o
        assert pow(b,o,p*p)!=1
counts=[]
for v in range(7):
    rows=[(accepts(7,129+258*u,258+774*v),
           accepts(43,129+258*u,258+774*v)) for u in range(7)]
    assert rows==[(v==5*u%7,v!=3*u%7) for u in range(7)]
    counts.append((sum(a for a,b in rows),sum(b for a,b in rows),
                   sum(a and b for a,b in rows)))
assert counts==[(1,6,0)]+[(1,6,1)]*6
assert (129+258*3,258+774)==(903,1032)
```
