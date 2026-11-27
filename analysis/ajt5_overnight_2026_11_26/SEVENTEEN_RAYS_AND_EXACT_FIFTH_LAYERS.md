# Seventeen sphere rays and exact fifth-power norm layers

**Phase \(470/9\) closes the \(142/3\)–\(158/3\) gap**, using the exact seed \((m,e)=(470,582)\). The seventeen rays now have maximum consecutive ratio \(99/89\), giving the effective generated-population bound
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{89/198}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3.
\]
The exponent \(89/198\) is sharp in the liminf for these rays.

**The large-ratio hypothesis can be dropped entirely for fifth-power lifts.** Every plus layer is an Eisenstein norm. Both signs always acquire fresh odd-valuation primes, and the minus layer has an exact criterion for admissibility.

### Fifth-power layers

Let \(A=5^u>B=3^v\), with \(u,v\) odd. At layer \(j\ge1\), set \(C=A^{5^{j-1}}\), \(D=B^{5^{j-1}}\), and define
\[
M_j=\frac{C^5-D^5}{C-D},\qquad P_j=\frac{C^5+D^5}{C+D}.
\]
Since \(5CD=3T^2\) for an integer \(T\), the two exact identities are
\[
\begin{aligned}
M_j&=(C^2+3CD+D^2)^2-3[T(C+D)]^2,\\
P_j&=(C^2-3CD+D^2)^2+3[T(C-D)]^2 .
\end{aligned}
\]
Thus \(P_j\) is always an Eisenstein norm. Every prime divisor of \(M_j\) has exact order \(5^j\) for \(A/B\). The first identity also forces \(3\) to be a quadratic residue at that prime: a common zero of the two norm coordinates at a layer prime (which cannot divide \(T\), since it is different from 3 and 5) would require \(C+D=0\), where the first coordinate is \(-D^2\ne0\). So every prime divisor of \(M_j\) is \(1\) or \(11\bmod60\). The layer is an Eisenstein norm exactly when all its \(11\bmod60\) prime valuations are even. Equivalently, \(M_j\) must be a Gaussian norm. The layer supports are disjoint by exact order, and their primes are distinct from \(5\), so this is a layer-by-layer test for a \(5^h\)-lift of an admissible base. [Cyclotomic valuation framework](https://raw.githubusercontent.com/Samsen879/a303656/945ab5dbf0455c900e60a465f67c818cb6c7b85ff3b9e/analysis/ajt5_overnight_2026_11_26/DIVISOR_CLOSED_CYCLOTOMIC_SEED_ORDERS.md)

The nonsquare tests are uniform in \(A/B\). Modulo \(7\), \(C/D\in\{1,2,4\}\), because \(5\) and \(3\) are both quadratic nonresidues and their exponents are odd. The values of \(\Phi_5(C/D)\) are \(5,3,5\), all nonsquares. Also \(P_j\equiv5\bmod8\). Thus both layers have an odd-valuation prime. On an admissible lift, the fresh kernel primes are at least
\[
12\cdot5^j+1\quad\text{on the minus side},\qquad
6\cdot5^j+1\quad\text{on the plus side}.
\]
They survive subsequent cubing. This gives a linear smoothness obstruction on these lift families without a size condition on the two powers.

Two actual primes impose further restrictions. Since \(5^5\equiv1+9\cdot11\) and \(3^5\equiv1\bmod11^2\), **a first fifth-power lift requires \(11\mid u\)**. At \(251\), the analogous residues at power \(125\) force \(3u\equiv2v\bmod251\) by the third fifth-power layer. The certified base \((m,e)=(22,6)\) accepts the first lift \((110,30)\), but its second lift fails at \(7451\), with exact order \(25\) and valuation one. The new seed \((470,582)\) uses the freedom to choose the \(3\)-exponent: its half-exponents \(235,291\) are coprime. Any fifth-power lift at that same lower exponent would have reduced \(u=47\), which the \(11\)-test excludes.

### Phase gain and exact replay

The new adjacent ratios are \(235/213\) and \(237/235\). The maximum moves to \(178/9\)–\(22\). At \(X=5^{22\cdot3^j}\) the preceding lower power is \(5^{(178/9)3^j}\), giving the matching liminf ceiling. Although the new seed has \(e>m\), \(3^{582}<5^{413}\) supplies a uniform height margin under cubing. The positive labels are \((582\cdot3^k+\mathbf1_{\lambda=1},\,470\cdot3^k)\), giving classes \(21\bmod24\) and \(3\bmod24\) for \(\lambda=1,3\). [Effective fixed-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The replay checks both classes at depths zero and one, including signed witnesses whose prescribed positive residual has exact \(47\)-valuation one.

```python
from fractions import Fraction as F

def N(a,b):
    return a*a+3*b*b

def orient(a,b,c,d):
    z = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((p for p in z if p[1]%3), key=lambda p:p[1])

a = 2156252835559625891393929480436341116439775451027247765640316978273041577896890001
b = 5351241740549826086382832614266976317835620083486640234620834204516895219323086536
c = 7871718028956553545006223120319388949360429389002082151506181520288726312683639148
d = 3087223459187207120096661931091958800942005949731595563429603005148262544448792538
q,s = 5**235,3**291
assert 2*N(a,b) == q-s and 2*N(c,d) == q+s
Q,Z = q*q,s*s
assert Z < 5**413
v,w = (4*z for z in orient(a,b,c,d))
for k,(j,h) in enumerate(((13,1222),(1,1081))):
    assert Q == 5**(470*3**k) and Z == 3**(582*3**k) == s*s
    assert N(v,w) == 4*(Q-Z) and w>s and w%3
    for good,t in ((True,w),(False,s+j)):
        for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
            S,r = x*x+y*y,t+s
            n = 5*Q+lam*Z-S
            assert Q<n<5*Q and S>lam*Z and n%24==(21 if lam==1 else 3)
            assert 2*lam*Z-S == r*r-3*t*t
            R = n-Q-(4-lam)*Z
            assert R==v*v+r*r if good else R%47**2==h and h%47==0
    v,w = orient(v,w,(Q-Z)//2,(Q+Z)//2)
    Q,Z,s = Q**3,Z**3,s**3

assert (5**5-3**5)//2 == 11*131 and (5**5+3**5)//8 == N(11,10)
assert (pow(5,5,121),pow(3,5,121)) == (100,1)
assert (pow(5,125,251**2),pow(3,125,251**2)) == (52711,35141)
p = 7451
assert (pow(5,55,p)-pow(3,15,p))%p == 1047
assert (pow(5,275,p*p)-pow(3,75,p*p))%(p*p) == 6992*p

ph = [F(18),F(178,9),F(22),F(70,3),F(74,3),F(26),F(82,3),F(30),
      F(290,9),F(34),F(110,3),F(38),F(42),F(46),F(142,3),
      F(470,9),F(158,3),F(54)]
assert max(b/a for a,b in zip(ph,ph[1:])) == F(99,89)
```

The population bound counts generated targets. The failure tests concern their specified positive exponent pairs.
