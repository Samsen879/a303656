# One actual coupled reader, two stripes, and a true nearby norm

**One actual reader can erase two coupled columns.** With native primes \(3,7\), the fixed inert prime \(3571\) supplies two exact valuation-one stripes modulo \(7\). Together with \(2k\) ternary single-stripe readers, it gives a sharp gap of \(3^{k+1}-1\) columns. The single-stripe maximum with the same \(2k+1\) higher readers is \(2\cdot3^k-1\). This is a strict gain in width, with the same exponential base \(\sqrt3\).

## Exact bound for the coupled model

Suppose \(2k\) readers each delete one class modulo a power of \(3\). The other readers together delete \(b\) classes modulo a common \(T\) prime to \(3\), where \(b<T\). If the periodic chart has a surviving column, the maximum fully deleted interval has length at most \((b+1)3^k-1\).

To prove this, take a surviving phase \(w\) and an interval of length \((b+1)3^k\). Each of the two siblings of \(w\) at every ternary depth \(j\le k\) contains at least \(b+1\) consecutive points of its progression in the interval. Those points have distinct residues modulo \(T\), so at least one needs a ternary reader. A ternary class avoiding \(w\) can serve only one sibling. This spends all \(2k\) readers. The progression \(w\bmod3^k\) also has \(b+1\) points in the interval with distinct residues modulo \(T\). At least one of those needs another reader. This proves the bound, including for arbitrary placements of the ternary stripes.

There is a more general reduction for mixed odd single stripes. If the coupled deletions all have periods dividing \(T\), freeze the residue modulo \(T\) of a surviving column. On that progression each remaining single stripe is either empty or one congruence class. The mixed-odd bound then gives \(O(T\,3^{h_{\rm single}/2})\) in the original index. Thus a bounded common period cannot change the exponential rate.

## Realizing the sharp gap

Put \(L=3^k,\ w=L-1,\ F=3L-1\). Use the usual two ternary sibling stripes at each depth through \(k\), leaving \(u\equiv w\bmod L\). The coupled reader will erase \(w\) and \(w+L\) on that progression, while \(F=w+2L\) survives.

Let \(Q=3571,\ C=Q(Q-1)\), and use
\[
R(u,v)=n-3^{C+Au}-5^{Bv},\qquad A=4096D,\quad B=D.
\]
For each ternary stripe of depth \(j\), choose a distinct inert \(q\equiv2\bmod7\) with \(v_3(q-1)=j+2\). Require that for \(m=3^{j+2}\), the powers \(3^{(q-1)/m},5^{(q-1)/m}\) have orders \(m,27\), respectively. These conditions follow from Chebotarev by prescribing the cyclotomic action and the Kummer multipliers \(\zeta_m,\zeta_m^{m/27}\). The radical classes are independent over the cyclotomic field. A positive odd radical of \(3^a5^b\) in that abelian field would generate a normal real subfield, hence would be rational because its defining odd-power polynomial has only one real root. Rationality forces \(m\mid a,b\). [Tschebotareff’s original density theorem](https://link.springer.com/article/10.1007/BF01206606) · [Stevenhagen and Lenstra’s exposition](https://websites.math.leidenuniv.nl/algebra/chebotarev.pdf)

Take
\[
D=\operatorname{lcm}\bigl(18,\ C/7,\ \{q(q-1)/3^{j_q+2}\}\bigr).
\]
Then \(v_3(D)=2\) and \(7\nmid D\). The native CRT constraints are
\[
n\equiv3\bmod4,\qquad n\equiv82\bmod243,\qquad
R(F,27)\equiv49\bmod343.
\]

- At \(3\), \(\nu_3(5^B-1)=3\). Every \(v\not\equiv0\bmod3\) gives \(\nu_3(R)=3\). Every \(v\equiv0\bmod9\) gives \(\nu_3(R)=4\).
- At \(7\), \(3^6\equiv5^6\equiv43\bmod49\) and \(4096\equiv1\bmod7\). Consequently \(49\mid R\) exactly on \(v\equiv F+6-u\bmod7\). Off that line the valuation is one. Each column has a native lift \(v\le125\) with valuations \(4,2\). Choose \(v_0<63\) with \(v_0\equiv0\bmod9\) on the line, then try \(v_0,v_0+63\). At most one lifts past valuation two at \(7\).

At a ternary reader the actual step orders are \(3^j,3\), including modulo \(q^2\). Thus \(v\equiv0\bmod3\) makes the \(5\)-term constant, and prescribing \(R(b,0)\equiv q\bmod q^2\) gives exactly the intended stripe \(u\equiv b\bmod3^j\).

At \(Q\), the baseline equality \(3^{4096C/7}\equiv5^{C/7}\pmod{Q^2}\) is checked below. Raising to the common power \(7D/C\), a unit modulo 7, shows that the actual steps coincide in an element \(g\) of order seven modulo \(Q^2\), and \(3^C\equiv1\bmod Q^2\). On the native line the offset is \(g^u+g^{t-u}\), where \(t\equiv F+6\equiv2w+L\bmod7\). Prescribe \(n\equiv g^w+g^{w+L}+Q\bmod Q^2\). The two values at \(w,w+L\) agree modulo \(Q^2\), so both valuations are exactly one. Over \(\mathbb F_Q\), multiplying the collision equation by \(g^u\) gives a quadratic with those two distinct roots. Every other column is a \(Q\)-unit on the line.

Let \(M\) be the combined target modulus and \(X=3^{C+AF}\). We have \(M\le4\cdot243\cdot343D^2<X\). The last target \(n_-<4X\) and next target \(n_+=n_-+M\) in the CRT class have quarter-height horizontal maxima \(F-1,F\). Both admit \(v\le125\). The entire active box at \(n_-\) fails at a specified odd valuation. At \(n_+\), \((F,27)\) passes every specified test. The same phase repeats at \(n_-\) above its active height, so the failed box still has a periodic survivor.

## Exact replay

For \(k=1\), the maximum index pairs are \((7,22367)\) and \((8,22367)\). The replay checks exact native lifts and shows that each higher reader is essential at the same failed target. It also verifies a separate **true two-square positive** in the same CRT class and at the same quarter height.

```python
from math import isqrt, lcm, prod

Q, F, w, V = 3571, 8, 2, 22367
rows = [(25867,3,0), (46279,3,1)]
C = Q*(Q-1)
D = lcm(18, C//7, *(q*((q-1)//(9*m)) for q,m,b in rows))
A, B = 4096*D, D

def S(u,v,m):
    return (pow(3,C+A*u,m)+pow(5,B*v,m)) % m

for q in (Q,25867,46279):
    assert q%4 == 3 and all(q%d for d in range(2,isqrt(q)+1))
assert pow(5,B,27) == 1 != pow(5,B,81)
assert pow(5,9*B,243) == 1
assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(3,A,7) == pow(5,B,7) == pow(3,C,7) == 1
g0 = pow(3,4096*(C//7),Q*Q)
assert g0 == pow(5,C//7,Q*Q) and g0%Q != 1 and pow(g0,7,Q*Q) == 1
g = pow(3,A,Q*Q)
assert g == pow(5,B,Q*Q) and g%Q != 1 and pow(g,7,Q*Q) == 1
assert pow(3,C,Q*Q) == 1
for q,m,b in rows:
    for base,step,t in ((3,A,m),(5,B,3)):
        assert pow(base,step*t,q*q) == 1 != pow(base,step*(t//3),q)

eq = [(4,3),(243,82),(343,S(F,27,343)+49),(Q*Q,S(w,5,Q*Q)+Q)]
eq += [(q*q,S(b,0,q*q)+q) for q,m,b in rows]
M = prod(m for m,t in eq)
a = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M
E = C+A*F
delta = 1+(4*pow(3,E,M)-1-a)%M
# n_- = 4*3**E-delta; n_+ = n_-+M
assert E//2 > (100*M).bit_length()
assert 3**(4096*F) > 5**V and D >= 2*C+4
assert 3**(2*4096*F+1) < 5**(2*(V+1))

def exact(u,v,p,k):
    return (a-S(u,v,p**(k+1)))%p**(k+1) in range(p**k,p**(k+1),p**k)

assert [u for u in range(7) if (a-S(u,(F+6-u)%7,Q))%Q == 0] == [2,5]
for u,v in enumerate((0,27,54,81,45,72,36,0,27)):
    assert exact(u,v,3,4) and exact(u,v,7,2)
    bad = [q for q in (25867,46279,Q) if exact(u,v,q,1)]
    assert bad == ([] if u == F else [(25867,46279,Q)[u%3]])

x0,y0 = 3897420313633017059177787853845, 846622110305849907072221799264
assert 0 <= x0 < M and 0 <= y0 < M and 4*5**27 < 3**(4096*F)
assert (x0*x0+y0*y0+S(F,27,M)-a)%M == 0
delta_x = (x0-15*pow(3,E//2,8*M)//8)%M
print((7,V), (8,V), E, M, delta, delta_x)
```

For the true positive, set \(Y=3^{E/2}\), \(x=\lfloor15Y/8\rfloor+\texttt{delta\_x}\), and \(n^\star=X+5^{27B}+x^2+y_0^2\). The modular calculation puts \(n^\star\) in the same target class. The bounds \(Y>100M\) and \(5^{27B}<X/4\) give \(4X<n^\star<5X\), so the two-square witness is active at \((8,27)\).

The sharp bound leaves open coupled deletions whose common period grows substantially with the reader count. The failed box is an obstruction for the specified anchored chart. The true positive certifies its constructed target. Neither conclusion settles the original conjecture.
