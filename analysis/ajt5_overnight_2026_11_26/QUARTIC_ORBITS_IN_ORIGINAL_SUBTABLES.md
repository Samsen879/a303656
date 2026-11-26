# Quartic trajectories inside the original two subtables

The earlier quartic control was outside the restricted subtables. The two fixed edges (11,4;11,5) and (10,4;11,5) are inside G0 and G1 respectively. Write w=5j+1821, A=5^d+3^c−131779 and B=(5^e+3^f−658897)/5. Both examples have v5(B−A)=−1. They give integral quartic w with j≡3 and j≡1 mod 6 respectively and true square-sum residuals.

For the construction choose nonzero rational r,m,s with A=−m²−m(r+B/r)−s²(r−B/r)²/4. Set lambda=−r/s, K=−m/s−s(r+B/r)/2, Z=lambda*t²+K and Q=(Z²+m²+A)/(2m). Then Q²−A=(Q−m)²+Z². Over the reals put U=lambda*t²−m/s+i*r*t and J=s+i*t. Expansion gives |U±sqrt(B)J|²=2m(Q∓sqrt(B)), so Q²−B=|(U²−BJ²)/(2m)|² with rational polynomial coordinates. Choose an affine rational substitution for t and w=−Q as checked below. The integer polynomial coefficient check proves both admissible progressions. The norm coordinates can initially be rational: a nonnegative integer which is a rational sum of two squares is an integer sum of two squares by the inert valuation criterion. Here both residuals are positive for all sufficiently large parameters, which suffices for the orbit counts.

The integer and identity checks are self-contained. Each cleared polynomial identity has degree at most eight, so nine distinct parameter values suffice.

```python
from fractions import Fraction as F

cases = (
    ((11,4,11,5), F(1,5), F(-462943102,25), F(4841429,4976185),
     6211563454986637499818904815176588633,
     48366013477558304653639750966327911000, 4976185),
    ((10,4,11,5), F(3,5), F(-1206998652,145), F(3489913905,3492286517),
     41726766710934165065916783375122593963690636517,
     206080402213224193702392521865816506927025210000, 3492286517),
)

for (d,c,e,f), r,m,s,N,L,D in cases:
    A = 5**d + 3**c - 131779
    V = 5**e + 3**f - 658897
    B = F(V,5)
    assert (V-5*A) % 5 == 1
    assert A == -m*m-m*(r+B/r)-(s*(r-B/r)/2)**2

    lam, K = -r/s, -m/s-s*(r+B/r)/2
    a, b = F(N,D), F(L,D)
    z = (lam*a*a+K, 2*lam*a*b, lam*b*b)
    terms = [m*m+A, F(0), F(0), F(0), F(0)]
    for i, zi in enumerate(z):
        for j, zj in enumerate(z):
            terms[i+j] += zi*zj
    w = [-v/(2*m) for v in terms]
    assert w[4] > 0 and all(v.denominator == 1 for v in w)
    assert [v % 30 for v in w] == [(6,26)[e-d],0,0,0,0]

    # 两个多项式恒等式的次数至多八，九点即够。
    for u in range(9):
        t = a+b*u
        W = sum(v*u**i for i,v in enumerate(w))
        x, y = lam*t*t-m/s, r*t
        R = (x*x-y*y-B*(s*s-t*t))/(2*m)
        I = (2*x*y-2*B*s*t)/(2*m)
        assert W*W-A == (-W-m)**2 + (lam*t*t+K)**2
        assert 5*W*W-V == (R-2*I)**2 + (2*R+I)**2

print("G0 and G1 quartics verified")
```

These two individual orbits each have order X^(1/4) distinct j up to height X, with no density or growing-menu claim. They disprove the proposed prohibition based solely on the 5-adic gap. No novelty claim is made.
