# Complete prime-local cover for the second four-square pattern

Let \(A=3^a,B=5^b\), \(a,b\ge2\) even, and \(S_i=9^iA+5^{P_i}B\) for \(P=(2,4,3,0)\). Call an exponent pair locally admissible if for every prime \(p\) there is a \(K_p\in\mathbb Z_p\) making all four \(K_p-S_i\) squares in \(\mathbb Z_p\). This allows \(K_p\) to depend on \(p\). The only prime exclusions are at \(7,11,13,17,19,61\). On writing \(a=2u,b=2v\), exactly 7,224 of the 129,600 classes \((u,v)\bmod360\) are locally admissible. This does not decide the existence of a single integer \(K\).

For \(p\ge7\), divide the four shifts by the unit square \(B\) and put \(t=A/B\bmod p\). The six lists of nonzero square ratios with no simultaneous translated square are
\[
 7:\{1\},\quad 11:\{3,4,5,9\},\quad 13:\{4,9\},\quad
 17:\{16\},\quad 19:\{9,16\},\quad 61:\{16\}.
\]
At all \(7\le p\le169\), a surviving ratio permits a point with at most one zero residual (exhaustive test below). For that optional zero residual choose \(K\equiv S_i+p^2\bmod p^3\); it is then a square of valuation two and all other residuals are unit squares. For \(2,3,5\) use respectively \(K\equiv S_2+16B\bmod128,\ K\equiv125B+9\bmod27,\ K\equiv5\bmod25\). These choices give even valuations and square units for all four rows; check the exponents in their periods, and use \(a,b\ge2\) where a base is not a unit.

For \(p>169\) merge equal shifts and let \(r\le4\) be the number of different translates. The smooth projective model of the joint square cover is geometrically connected (the distinct linear factors are independent square classes over the geometric function field). It has degree \(2^r\) over the \(K\)-line. The inertia index is two at the \(r\) finite roots and at infinity, and there are no other branch points. Riemann–Hurwitz thus gives genus at most five, with at most \(5\cdot8=40\) geometric points above the branch points. The Hasse–Weil lower bound \(p+1-10\sqrt p>40\) guarantees a point off those fibers. It gives four nonzero square residues, hence four simultaneous \(p\)-adic squares by unit lifting. This shows why adding larger primes cannot improve this local test.

~~~python
from math import isqrt
P=(2,4,3,0)
def rows(A,B):
    return [9**i*A+5**d*B for i,d in enumerate(P)]
bad={}
for p in range(7,170):
    if any(p%i==0 for i in range(2,isqrt(p)+1)): continue
    Q={i*i%p for i in range(p)}
    for t in Q-{0}:
        S=rows(t,1)
        keys=[z for z in range(p) if all((z-s)%p in Q for s in S)]
        if not keys: bad.setdefault(p,set()).add(t)
        else: assert min(sum((z-s)%p==0 for s in S) for z in keys)<=1
assert bad=={7:{1},11:{3,4,5,9},13:{4,9},17:{16},19:{9,16},61:{16}}
live=[(u,v) for u in range(360) for v in range(360)]
counts=[]
for p,F in sorted(bad.items()):
    assert pow(9,360,p)==pow(25,360,p)==1
    live=[(u,v) for u,v in live if pow(9,u,p)*pow(25,-v,p)%p not in F]
    counts.append(len(live))
assert counts==[86400,17280,11520,10080,7560,7224]
assert (167,114) in live
~~~

In particular \((a,b)\equiv(334,228)\bmod720\) survives every prime separately. These classes contain arbitrarily large real balanced exponent pairs by irrationality of \(\log3/\log5\). More generally each of the finite exponent classes is equidistributed in that fixed-ratio strip by irrational rotation, so the fraction surviving this local test within the even-exponent balanced strip is \(7224/129600=301/5400\). A finite CRT combination is still weaker than an exact integer square condition for a common \(K\).
