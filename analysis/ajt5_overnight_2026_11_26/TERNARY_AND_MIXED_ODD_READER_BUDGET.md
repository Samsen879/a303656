# Ternary reader obstruction and an optimal exponential base for mixed odd stripes

**Ternary orders beat the \(7^{h/6}\) obstruction.** With \(h=2k+r\) higher readers, \(r\in\{0,1\}\), actual \(3,5\) quarter-height charts can lose exactly the first
\[
F(h)=(r+1)3^k-1
\]
columns while retaining a periodic survivor. Each higher reader has its own exact valuation-one stripe. The new exponential base per higher reader is \(\sqrt3\), compared with \(7^{1/6}\). The construction uses three fixed native rows.

There is also a mixed-order upper bound. If each higher reader deletes one congruence class of odd modulus on the repaired chart and some phase survives, every fully deleted interval has length \(O(3^{h/2})\), with an absolute constant. Thus mixing odd moduli cannot improve the exponential base in this model.

## Actual ternary stripes

Write
\[
R(u,v)=n-3^{3+Au}-5^{Bv}.
\]
Use native primes \(3,23,59\). Take \(n\equiv10\bmod27\), \(B\) even, and \(3\nmid B\). Since the first exponent is at least three and \(5^B\) has order three modulo nine,
\[
v\not\equiv0\pmod3\quad\Longrightarrow\quad \nu_3(R)=1.
\]
This genuine norm test supplies the vertical lock. At \(v=0\) it gives \(\nu_3(R)=2\). On the old \(7,59\) native line, all three \(v\bmod3\) phases can instead be lifted to exact native valuation two. A single reader of vertical order three can collide in only one of those phases at fixed \(u\), so it cannot erase a whole column containing all three lifts.

Assign two higher primes at each depth \(1\le j\le k\) to the stripes
\[
u\equiv 3^{j-1}-1,\quad 2\cdot3^{j-1}-1\pmod{3^j}.
\]
If \(r=1\), assign one more prime to \(u\equiv3^k-1\bmod3^{k+1}\). These classes are disjoint, cover \(0,\ldots,F(h)-1\), and leave \(F(h)\). The bound is exact for arbitrary ternary stripes with a survivor. Relative to a surviving phase, an interval of \((r+1)3^k\) integers meets both sibling classes at each of the first \(k\) depths. It also meets \(r+1\) distinct next digits on the surviving branch. Those disjoint requirements cost \(2k+r+1\) readers.

For each stripe of depth \(j\), put \(m=3^j\). Choose a distinct inert prime \(q\equiv7\bmod12\), with \(q\equiv1+m\bmod3m\) and \(q\equiv2\bmod p\) for \(p=23,59\), for which
\[
\operatorname{ord}_q\bigl(3^{(q-1)/m}\bigr)=m,\qquad
\operatorname{ord}_q\bigl(5^{(q-1)/m}\bigr)=3.
\]
Chebotarev gives these primes by prescribing the cyclotomic action and the two Kummer multipliers \(\zeta_m,\zeta_m^{m/3}\). The Kummer classes are independent over the cyclotomic field. If \(3^a5^b\) had an \(m\)th root there, its positive real root would also lie there and generate a normal real field over \(\mathbb Q\). Its odd-power polynomial has just one real root, so the root would be rational, implying \(m\mid a,b\). The chosen orders are invariant under Frobenius conjugation. [Tschebotareff’s original density theorem](https://link.springer.com/article/10.1007/BF01206606) · [Stevenhagen and Lenstra’s exposition](https://websites.math.leidenuniv.nl/algebra/chebotarev.pdf)

Set
\[
D=\operatorname{lcm}\bigl(638,\{q(q-1)/3^{j_q}\}\bigr),\qquad A=4096D,\quad B=D.
\]
Then \(D\) is prime to \(3,23,59\). The step orders at each \(q\) are \(3^{j_q},3\) and stay the same modulo \(q^2\) because both strides are divisible by \(q\). For the stripe \(u=b\bmod3^{j_q}\), prescribe
\[
n\equiv 3^{3+Ab}+1+q\pmod{q^2}.
\]
On every native-pass column fibre, \(v\equiv0\bmod3\). There the \(5\)-term is constant modulo \(q^2\), and the \(3\)-term is injective modulo \(q\) in its period. Hence the assigned stripe has valuation exactly one and every other column is a \(q\)-unit.

Complete the single target class by requiring \(n\equiv1\bmod4\) and \(R(F,0)\equiv p^2\bmod p^3\) at \(p=3,23,59\). At \(23,59\), the strides preserve both powers modulo \(p\) and have nonzero first lifting coefficients. At any fixed \(u\), the two tests \(p^2\mid R\), together with \(v\equiv0\bmod3\), prescribe one class modulo \(3\cdot23\cdot59\). Among five consecutive representatives, the \(3\)-test spoils at most two and each of \(23,59\) spoils at most one. Thus every column has an exact native lift with \(v\le20354\). In particular, every column would have a native lift within this vertical bound before its higher-reader test. The point \((F,0)\) passes all rows and repeats in a joint period.

Let \(M\) be the target modulus and \(X=3^{3+AF}\). We have \(M\le108(23\cdot59)^3D^2<X\). Take the last target \(n_-<4X\) in this class and the next target \(n_+=n_-+M\). Their quarter-height horizontal maxima are \(F-1\) and \(F\), respectively, and both vertical maxima are at least \(F\). At \(n_-\) every active cell has a specified odd valuation. At \(n_+\), \((F,0)\) is active and passes all the specified tests. Both boxes have positive remainders throughout.

## Why mixed odd stripes cannot improve the exponential base

Start with any surviving integer \(w\). For each forbidden class modulo an odd \(m\), choose a prime-power factor of \(m\) on which the class differs from \(w\). Enlarge that class to the sibling at its first differing digit. The enlarged system still leaves \(w\) and has at most \(h\) classes.

At prime \(p\), let \(t_p\) be the number of consecutive initial levels at which all \(p-1\) siblings are forbidden. Those full levels spend \(H=\sum_p(p-1)t_p\) readers and leave the progression \(w\bmod M_0\), where
\[
M_0=\prod_p p^{t_p}\le3^{H/2}.
\]
After fixing the whole shared progression, the first nonfull level at \(p\) has at most \(p-2\) forbidden siblings. If deeper exclusions remain, enlarge them to the one continuing digit. In the progression coordinate this leaves \(k_p<p\) forbidden residues modulo each \(p\), with \(\sum k_p\le s=h-H\).

The remaining gap cost is \(\exp(o(s))\), uniformly in the primes. To see this, fix one allowed digit for every \(p\le\sqrt{s}\) and every \(p\) with \(k_p>p/2\). Their product is \(\exp(O(\sqrt{s}\log(s+2)))\), since there are at most \(2\sqrt{s}\) large heavy primes and each is at most \(2s\). On the resulting progression put \(\lambda=\sum k_p/p\le\sqrt{s}\) for the remaining primes. Their CRT density is at least \(e^{-2\lambda}\). Odd Bonferroni truncation at the least odd \(t\ge8(\sqrt{s}+1)\) loses at most \(\lambda^{t+1}/(t+1)!<\tfrac12e^{-2\lambda}\). For an interval of length \(L\), the total CRT counting error is at most \((s+1)^t\), since an intersection contributes at most \(\prod k_p\) residue classes. Taking \(L>2e^{2\lambda}(s+1)^t\) guarantees a survivor. The case \(s=0\) needs only the progression modulo \(M_0\).

The total interval bound is therefore \(3^{(h-s)/2}\exp(O(\sqrt{s}\log(s+2)))=O(3^{h/2})\). This uses exact CRT counts in the interval. It applies to actual readers once each deletion is a single projected class and a surviving column can be lifted within the vertical budget.

## Replay

The four-reader example has quarter-height maxima \((7,22367)\) and \((8,22367)\). Each higher reader is essential at the **same** failed target \(n_-\). The fourth entry in each row below is a vertical index that passes every other test.

```python
from math import isqrt, lcm, prod

rows = [(31,3,0,4221), (283,3,1,1149), (199,9,2,6219), (739,9,5,5145)]
native = (3,23,59)
F, V = 8, 22367
D = lcm(638, *(q*((q-1)//m) for q,m,b,v in rows))
A, B = 4096*D, D

def S(u,v,m):
    return (pow(3,3+A*u,m) + pow(5,B*v,m)) % m

for p in native[1:]:
    for base,step in ((3,A),(5,B)):
        assert pow(base,step,p) == 1 != pow(base,step,p*p)
assert A%2 == B%2 == 0
assert pow(5,B,3) == 1 != pow(5,B,9)
assert pow(5,9*B,27) == 1 != pow(5,3*B,27)
for q,m,b,v in rows:
    assert q%4 == 3 and all(q%d for d in range(2,isqrt(q)+1))
    for base,step,t in ((3,A,m),(5,B,3)):
        assert pow(base,step*t,q*q) == 1 != pow(base,step*(t//3),q)

eqs = [(4,1)] + [(p**3,S(F,0,p**3)+p*p) for p in native]
eqs += [(q*q,S(b,0,q*q)+q) for q,m,b,v in rows]
M = prod(m for m,_ in eqs)
a = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eqs) % M
e = 3+A*F
delta = 1+(4*pow(3,e,M)-1-a)%M
# Exact targets: 4*3**e-delta and 4*3**e-delta+M.
assert 1 <= delta <= M and e > M.bit_length()
assert D >= 10 and 3**(4096*F) > 5**V
assert 3**(2*4096*F+1) < 5**(2*(V+1))

def exact(u,v,p,k):
    return ((a-S(u,v,p**k))%p**k == 0
            and (a-S(u,v,p**(k+1)))%p**(k+1) != 0)

assert [sum(u%m == b for q,m,b,v in rows) for u in range(F+1)] == [1]*F+[0]
for q,m,b,v in rows:
    assert 0 <= v <= V and exact(b,v,q,1)
    assert all(exact(b,v,p,2) for p in native)
    assert all((a-S(b,v,t))%t for t,_,_,_ in rows if t != q)
assert all(exact(F,0,p,2) for p in native)
assert all((a-S(F,0,q))%q for q,_,_,_ in rows)
print((F-1,V), (F,V), e, M, delta)
```

The construction lets the strides grow with the reader budget. The upper bound covers single projected stripes, including mixed odd orders. Readers with several coupled deletion classes and the two-square status of the positive remainder lie outside these conclusions.
