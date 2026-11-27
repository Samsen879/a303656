# A twenty-first sphere phase and a positive cubic-order norm certificate

**Phase \(50\) is certified by \((m,e)=(150,22)\).** It lies inside \(142/3<50<470/9\). The scale-\(1\) strip has no admissible pair, and this is the unique admissible pair at scale \(3\). The twenty-one-ray construction now has maximum adjacent phase ratio \(89/81\), improving the uniform generated-population exponent to **\(81/178\)** in both odd classes.

### Exact seed and a positive order criterion

Put \(A=5^{75}\) and \(B=3^{11}\). The two odd halves have these certificates for \(x^2+3y^2\).

| Half | \(x\) | \(y\) |
|---|---:|---:|
| \((A+B)/8\) | 40036541520532131108623704 | 23845319549734265133358541 |
| \((A-B)/2\) | 99912911189343717632820767 | 32925673764398290824422180 |

The half-exponents \(75,11\) are coprime. In particular, the seed at scale \(3\) survives even though its height phase has no seed at scale \(1\).

The finite strip proof uses **coprime divisors**. If \(D\mid N=5^m-3^e\), \(\gcd(D,N/D)=1\), and \(D\equiv2\bmod3\), then \(N\) fails the Eisenstein norm criterion. Indeed, if every inert prime had even valuation in \(N\), the same would hold in \(D\), forcing \(D\equiv1\bmod3\). Thus the replay needs no primality assertions for its divisor witnesses. It checks all 18 pairs at \(m=50\) and all 164 pairs at \(m=146,150,154\).

There is also a transferable **positive** test. For an odd half \(H>1\) coprime to \(3\), supply a unit \(T\bmod H\) and an exponent \(E=3^a t\) with \(3\nmid t\). If
\[
T^E\equiv1\pmod H,\qquad \gcd(H,T^t-1)=1,
\]
then every prime dividing \(H\) splits in the Eisenstein field. More concretely, \(D_j=\gcd(H,T^{3^jt}-1)\) contains a whole prime power of \(H\) exactly when its order has \(3\)-adic depth at most \(j\). On \(D_j/D_{j-1}\), the element \(T^{3^{j-1}t}\) is a root of \(X^2+X+1\). CRT joins these roots, and the Eisenstein gcd of \(H\) and \(\omega-r\) for the joined root \(r\) gives a generator of norm \(H\). This certifies a norm and constructs its coordinates given an order exponent. Finding that exponent is a separate arithmetic task.

For the new seed, **\(T=5\) works on both halves**. The plus half has three nonempty depth classes and the minus half has two. A single power of \(5\) cannot be a nontrivial cube root on every class, since the required valuation of its exponent differs by class. The actual half \((5^{13}-3^5)/2=7727^2+3\cdot13548^2\) shows the limit of fixing \(T=5\): it is divisible by \(67\), where \(5^{22}\equiv1\), so this base cannot certify the half.

### Growing labels and same-height controls

At depth \(k\), let \(Q=5^{150\cdot3^k}\), \(Z=3^{22\cdot3^k}\), and \(s=\sqrt Z\). Multiplying the two half-norms starts \(V^2+3W^2=4(Q-Z)\) with coordinates divisible by \(8\). Each cubing multiplies the norm element by \((Q-Z)/2+(Q+Z)\sqrt{-3}/2\). The three Eisenstein unit rotations give all three ratios \(W/V\bmod3\). Of the two rotations with \(3\nmid W\), one has \(3W^2\ge Q-Z\). Its coordinates are divisible by \(4\), and \(Q>10Z\) ensures \(W^2>3Z\).

Use \(S_1(t)=(t-s)^2+t^2\) and \(S_3(t)=(t+s)^2+(t-2s)^2\). At \(t=|W|\),
\[
n_\lambda=5Q+\lambda Z-S_\lambda(t)
          =Q+(4-\lambda)Z+V^2+(t+s)^2,\qquad Q<n_\lambda<5Q.
\]
The classes are \(21\bmod24\) and \(3\bmod24\), with true positive exponent pairs \((22\cdot3^k+1,150\cdot3^k)\) and \((22\cdot3^k,150\cdot3^k)\), respectively.

At the same heights and in both classes, \(t=s+13\) at depth \(0\) gives a signed witness whose selected positive residual is \(35\bmod49\). At depth \(1\), \(t=s+5\) gives \(18507=93\cdot199\bmod199^2\). Both are exact valuation-one failures at Gaussian inert primes. They exclude the selected exponent pairs.

### Population and replay

The inserted phase splits the old gap into ratios \(75/71\) and \(47/45\). The new maximum \(89/81\) occurs between \(18\) and \(178/9\). The effective sphere count transfers to the new ray in both classes. The two sphere values are \(2,6\bmod8\) and both are \(3\bmod9\). Their squarefree parts have the same bounded multiplicity argument, since writing either as \(3Df^2\) gives \(W^2-Df^2=-2\cdot3^{22\cdot3^k-1}\) or \(-2\cdot3^{22\cdot3^k}\). Unit rotations preserve the distinct shell ideals, and \(Z=Q^\gamma\) for fixed \(\gamma<1\) preserves the height-trimming saving. Thus in each class
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{81/178}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}}.
\]
The largest gap and the per-height upper bound make \(81/178\) sharp as a lower limiting exponent for these generated sphere populations. [Effective sphere argument](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md) · [De la Bretèche–Tenenbaum mean-value theorem](https://arxiv.org/abs/2403.19320)

The replay checks the full finite strip, the cubic CRT roots and the norm witnesses. An independent BigInt implementation reproduced all of these checks.

```python
from fractions import Fraction as F
from math import gcd, isqrt

def veto(N, d):
    f = 1
    while N % d == 0:
        N, f = N//d, f*d
    return f % 3 == 2 and gcd(f, N) == 1

panel = [2,17,11,53,23,59,113,1091,107,137,173,227,233,653,2477,19973,
         22973,47,71,293,311,359,557,719,839,857,911,983,1217,1553,1733,
         9851,13907,14153,20507,135017,333287,381047,1153337,3413507,3724439,
         3861059,25122173,30194453,120983462693,807729579959,75680634679733,
         169661285168723,68118579093818071361633]
assert [[m for m in range(2,53*t,4) if 426*t < 9*m < 470*t]
        for t in (1,3)] == [[50],[146,150,154]]
left = []
for m,E in [(50,70),(146,210),(150,218),(154,222)]:
    assert E%4 == 2 and 3**E < 5**m < 3**(E+4)
    left.extend((m,e) for e in range(2,E+1,4)
                if not any(veto(5**m-3**e,d) for d in panel))
assert left == [(150,22)] and gcd(75,11) == 1

def normroot(H, E):
    t = E
    while t%3 == 0:
        t //= 3
    assert pow(5,E,H) == 1 and gcd(H,pow(5,t,H)-1) == 1
    old,r,depths = 1,0,0
    while t < E:
        x = pow(5,t,H)
        t *= 3
        new = gcd(H,pow(5,t,H)-1)
        assert new%old == 0
        q,old = new//old,new
        if q > 1:
            assert gcd(x-1,q) == 1 and (x*x+x+1)%q == 0
            r += x*(H//q)*pow(H//q,-1,q)
            depths += 1
    assert old == H and (r*r+r+1)%H == 0
    return depths

A,B = 5**75,3**11
a,b = 40036541520532131108623704,23845319549734265133358541
c,d = 99912911189343717632820767,32925673764398290824422180
assert 8*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B
assert normroot((A+B)//8,17018271044650369696274180111843227401271404840) == 3
assert normroot((A-B)//2,45016631975674751244347068142871485339929539249246) == 2
H = (5**13-3**5)//2
assert H == 7727**2+3*13548**2 and H%67 == 0 and pow(5,22,67) == 1

Q,Z = A*A,B*B
v,w = 8*(a*c-3*b*d),8*(a*d+b*c)
for j,p,rem in [(13,7,35),(5,199,18507)]:
    s = isqrt(Z)
    W,V = max((abs(y),abs(x)) for x,y in
              [(v,w),((v-3*w)//2,(v+w)//2),
               ((-v-3*w)//2,(v-w)//2)] if y%3)
    assert s*s == Z and V*V+3*W*W == 4*(Q-Z) and 3*W*W >= Q-Z > 9*Z
    assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
    assert 0 < rem < p*p and rem%p == 0
    for L in (1,3):
        for t in (W,s+j):
            x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
            S = x*x+y*y
            n = 5*Q+L*Z-S
            R = n-Q-(4-L)*Z
            assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
            if t == W:
                assert R == V*V+(W+s)**2
            else:
                assert R > 0 and R%(p*p) == rem
    x,y = (Q-Z)//2,(Q+Z)//2
    v,w,Q,Z = x*v-3*y*w,x*w+y*v,Q**3,Z**3

g = list(map(F, ("18 178/9 182/9 22 70/3 74/3 26 82/3 30 290/9 34 110/3 "
                 "38 118/3 122/3 42 46 142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(89,81)
print("PASS")
```
