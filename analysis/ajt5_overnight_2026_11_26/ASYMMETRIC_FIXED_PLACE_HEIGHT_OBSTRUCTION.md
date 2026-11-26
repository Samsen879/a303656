# Fixed-place bounds constrain the shallow side of an asymmetric certificate

Use labels \((0,v),(u,0)\), high powers \(X=3^u,Z=5^v\) with \(X/Z\) bounded above and below, and odd \(n\) with \(\max(X,Z)+1<n<X+Z\). Let \(R_1=n-1-Z,\ R_2=n-1-X\). Suppose a growing panel \(Y=n^{o(1)}\) strips only primes from a fixed \(S\supset\{2,3,5\}\) and at most one additional prime \(p\le Y\). The remaining positive rough parts satisfy the strong product bound, so \(w_1w_2=O(Y^4)\). Assume \(R_s\ge n^\eta\) for a fixed \(\eta>0\) on the shallower side, its \(p\)-depth \(t\) has \(t\log p=o(\log n)\), and the deep side has \(p\)-depth \(E>t\). Put \(L=\log(2p)\log(2Y)(1+\log\log n)\).

If \(S=\{2,3,5\}\), such an unbounded family needs \(L\gg_\eta\log n\). In particular a panel with \(\log Y=o(\sqrt{\log n/(1+\log\log n)})\) is excluded under these hypotheses. More generally, if \(L=o(\log n)\), at least one fixed extra prime must carry a macroscopic power on the shallow side. Indeed, writing \(F=S\setminus\{2,3,5\}\) and \(d_q=v_q(Z-X)\), the necessary budget is
\[
 \sum_{\substack{q\in F,\ q\le Y\\q\equiv1(4)\ \text{or}\ d_q\text{ even}}}
     v_q(R_s)\log q\ \ge\ \eta\log n-o(\log n).
\]
Here all stripped inert valuations on both sides are assumed even, as in the strong product test. In particular the same exclusion holds if all extra fixed primes are inert with odd \(d_q\). This does not exclude any remaining model with a shallow residual smaller than the specified power, unrestricted extra fixed primes, or sufficient panel height.

## Proof

Use [the fixed-support rough-product bound](FIXED_SUPPORT_CROSS_SUM_OBSTRUCTION.md) with the same fixed \(S\). It gives \(p^{t+E}w_1w_2\gg_{S,\epsilon} n^{1-\epsilon}\) for all fixed \(\epsilon>0\); thus \(E\log p=(1-o(1))\log n\) in any such unbounded family. If the first residual is shallow, \(Z-R_2=X-R_1\), so \(v_3(R_1)=v_3(Z-R_2)\), since \(0<R_1<X=3^u\). If positive, \(R_2/Z\) is a \(3\)-adic unit and is not \(1\). At \(5\),
\(\min(v_5(R_1),v)\le v_5(X+R_2)\), because \(X+R_2=Z+R_1\). A positive right-side valuation makes \(R_2/X\) a \(5\)-adic unit congruent to \(-1\); the valuation equals that of \((R_2/X)^2-1\), which is nonzero as a rational difference. Expand the deep residual into its fixed \(S\)-factors, \(p^E\) and \(w_2\). The unit tests allow the varying bottom at the active \(3\)- or \(5\)-place to be dropped if its exponent is zero; in fact no factor at that place divides the deep residual when the corresponding valuation estimate is needed. All nonzero exponents are \(O(\log n)\). The standard fixed-place consequence of [Yu's bound as stated by Bugeaud–Evertse, Theorem 3.2](https://arxiv.org/pdf/1611.00485#page=8) bounds these two valuations by \(O_S(L)\). In that form take the \(\delta\) in the displayed theorem proportional to \(B_n/B\), so \(\log T=O_S(1+\log\log n)\) in the present height range and the product of varying base heights is \(O(\log(2p)\log(2Y))\). By symmetry interchange 3 and 5 for a shallow second residual.

When \(L=o(\log n)\), the truncated \(5\)-adic comparison gives the actual shallow valuation bound since \(v\asymp\log n\). Oddness removes the factor at 2. At a fixed extra \(q\), Yu applied directly to \(5^v/3^u-1\) gives \(d_q=O_S(1+\log\log n)\). Unequal valuations of the two residuals would have minimum \(d_q\). If \(d_q\) is odd and both actual valuations must be even, they therefore coincide below \(d_q\). Summing the logarithmic factors of \(R_s\) now proves the budget. Some eligible \(q\) has \(v_q(R_s)\gg_{S,\eta}\log n\), while the deep residual has valuation exactly \(d_q\). The exact additional congruence when the first residual is shallow is \(R_d/q^{d_q}\equiv(Z-X)/q^{d_q}\bmod q^{v_q(R_s)-d_q}\); the sign reverses in the other orientation.

## Finite true-label controls

At \(u=33,v=22\), the two examples both show the same asymmetric moving depths \(v_{23}(R_1),v_{23}(R_2)=(2,4)\). An extra \(10979\) of odd label-gap depth cannot enter a valid inert panel; an extra \(11\) at even depth zero is not ruled out by this necessary condition. Neither point passes the full strong product test. The first deep residual is \(29039455^2\) and the second is \(28316841^2\). Both shallow residuals fail globally at the displayed odd inert factor.

```python
def v(a,p):
    a=abs(a); k=0
    while a%p==0:
        a//=p; k+=1
    return k
X,Z=3**33,5**22
for n,b,q,depth,pair in [(6402350513252549,29039455,10979,1,(1,2)),
                         (6360904050774805,28316841,11,0,(2,0))]:
    r,t=n-1-Z,n-1-X
    assert max(X,Z)+1<n<X+Z and t==b*b
    assert (v(r,23),v(t,23))==(2,4)
    assert v(Z-X,q)==depth and (v(r,q),v(t,q))==pair
assert v(6360904050774805-1-Z,103)==1
```
