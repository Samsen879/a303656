# Exact parity and the reader budget for a complete native vertical fibre

**Seven higher readers are necessary and sufficient to erase a complete native vertical fibre in the \(7\)-primary model.** At the minimum, six must have vertical order \(49\). The seventh can have order \(49\) or \(343\). The order-\(343\) option is real: the replay below erases the entire column \(u=2\) and preserves \((3,54)\) at the **same target**, with both inside the quarter-height box.

The difference from the earlier six-reader count is exact parity. Six readers can erase all lifts of native valuation two at \(7\), but the remaining branch contains lifts of valuation four and higher even valuations.

## Exact order budget

Keep the native \(3,7\) chart from the previous result, with \(R=n-3^{C+Au}-5^{Bv}\), \(v_3(B)=2\), and \(49\mid R\) on \(v\equiv1-u\bmod7\). Work at a column where the fixed \(3571\) row is a unit, and count additional readers of vertical order \(7^d\) with \(d\ge2\).

Write the native line as \(v=s+7x\), \(0\le s<7\). Since \(5^{7B}-1\) has valuation two at \(7\), there is a unique \(7\)-adic root \(r\) with
\[
\nu_7(R(u,s+7x))=2+\nu_7(x-r)
\]
away from zero. This follows by lifting one digit at a time using the unit coefficient of \((5^{7B}-1)/49\). The exact valuation-four test at \(3\) can be enforced independently by \(v\equiv0\bmod9\). Thus every even shell around \(r\) contains native survivors.

An order-\(7^d\) reader can collide on at most one class of \(x\bmod7^{d-1}\). Six first digits away from \(r\) each contain a full even shell. With seven readers total, each of these digits needs one order-\(49\) reader. Inside the seventh digit, the six children away from \(r\bmod49\) have odd native valuation. One order-\(343\) reader on \(r\bmod49\) therefore suffices. A single reader of still higher order cannot cover the class \(r\bmod49\), since each of its seven next digits contains even-shell points.

More generally, if every reader has order at least \(7^{\ell+1}\), the exact minimum is
\[
N_\ell=1+6\!\!\sum_{\substack{0\le j<\ell\\ j\ {\rm even}}}7^{\ell-j-1}.
\]
This counts the classes modulo \(7^\ell\) meeting an even shell, including the class containing the root. Each reader can serve only one of them. Assigning one reader of order \(7^{\ell+1}\) to each attains the bound. The first three minima are \(7,43,301\).

There is also an exact test for a mixed order budget. At depth \(j\), let \(b_j\) be the number of available order-\(7^{j+1}\) readers. Start at depth one with six full branches and one branch containing the root. If \(a\) full branches and a root indicator \(\epsilon\in\{0,1\}\) remain, choose whether to spend \(z\in\{0,\epsilon\}\), \(z\le b_j\), on the root branch. Spend \(x=\min(a,b_j-z)\) on full branches. The next state is
\[
\left(7(a-x)+6(\epsilon-z)\mathbf1_{j\ {\rm even}},\ \epsilon-z\right).
\]
At the last depth, require both \(a-x=0\) and \(\epsilon-z=0\). This is exact because a full branch has seven required children, and the root branch has six additional required children precisely when the shell at that depth is even.

These are full-fibre statements. For a bounded box, if a required class remains uncovered and the deepest reader has order \(7^{L+1}\), a native survivor that is a unit at every higher reader can be chosen at \(v<9\cdot7^{L+3}\). In the root class, choose the first differing digit to give valuation \(L\) or \(L+1\) in \(x-r\), whichever is even. Then impose \(v\equiv0\bmod9\) by CRT. This gives an explicit height at which an uncovered periodic phase becomes an active escape.

## Realizing the budget with \(3,5\)

For each assigned class choose a distinct inert \(q\) of the required order \(m=7^d\), using the previous Chebotarev prescription for equal normalized \(3,5\) steps of exact order \(m\). Choose the common strides \(A=\lambda B\), with \(\lambda\equiv1\) modulo every order, \(v_3(B)=2\), \(7\nmid B\), and \(q\mid B\) for each reader. Take \(C\) divisible by every \(q(q-1)\). Thus both steps equal \(g\) of order \(m\) modulo \(q^2\). Prescribing \(n\equiv g^2+g^b+q\bmod q^2\) gives exact valuation one on the assigned residue \(v\equiv b\bmod m\) in column \(2\). [Tschebotareff’s density theorem](https://link.springer.com/article/10.1007/BF01206606)

Center the native root at \(v=27\) to the required depth by prescribing \(R(2,27)\) to have a sufficiently large **even** valuation at \(7\). Keep \(n\equiv82\bmod243\) and the \(3571\) pair \(0,1\bmod7\). To preserve column \(3\), exclude the finite prime divisors of the cyclotomic norms of
\[
z^2+z^b-z^3-z^{v'},\qquad v'\in\{54,117\},
\]
for each assigned row, where \(z\) has order \(m\). These differences are nonzero. Two pairs on the unit circle with the same nonzero sum are the same unordered pair, and the second pair here contains no \(z^2\). At least one of \(54,117\) has native valuations \(4,2\) at \(u=3\), and the exclusions make it a unit at every higher reader.

For any finite such assignment, \(\lambda\) can supply the required vertical height. Taking two adjacent CRT targets on either side of \(4\cdot3^{C+3A}\) gives horizontal maxima \(2,3\). The first box is fully blocked. The second keeps column \(2\) fully blocked and has an active survivor in column \(3\).

## Same-target replay

The seven-row control uses six order-\(49\) readers and one order-\(343\) reader. The latter is essential at \((2,27)\), where the native valuations are \(4,4\). On the previous fine diagonal \(u+v\equiv22\bmod49\), \((2,216)\) fails and \((3,117)\) escapes. Off that diagonal, \((3,54)\) also escapes. The erasure of column \(2\) covers all native lifts, including those off the diagonal.

```python
from math import isqrt, lcm, prod

Q = 3571
rows = [(6763,49,6), (119659,49,13), (190807,49,20),
        (430907,49,34), (434827,49,41), (472067,49,48),
        (9145067,343,27)]
panel = [(Q,7,0), *rows]
C = lcm(*(q*(q-1) for q,m,b in panel))
B = lcm(18, *(q*((q-1)//m) for q,m,b in panel))
A = 4117*B

def S(u,v,m):
    return (pow(3,C+A*u,m) + pow(5,B*v,m)) % m

for q,m,b in panel:
    assert q%4 == 3 and all(q%d for d in range(2,isqrt(q)+1))
    g = pow(3,A,q*q)
    assert g == pow(5,B,q*q) and pow(3,C,q*q) == 1
    assert pow(g,m,q*q) == 1 != pow(g,m//7,q)
assert pow(5,B,27) == 1 != pow(5,B,81)
assert pow(5,9*B,243) == 1
assert pow(3,A,49) == pow(5,B,49) != 1

eq = [(4,3), (243,82), (7**5,S(2,27,7**5)+7**4),
      (Q*Q,S(0,1,Q*Q)+Q)]
eq += [(q*q,S(2,b,q*q)+q) for q,m,b in rows]
M = prod(m for m,_ in eq)
a = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M

def val(u,v,p):
    return next(k for k in range(6)
                if (a-S(u,v,p**(k+1)))%p**(k+1))

owner = {b:q for q,m,b in rows}
for v in range(27,406,63):
    assert val(2,v,3) == 4 and val(2,v,Q) == 0
    assert val(2,v,7) == (4 if v == 27 else 2)
    assert [q for q,m,b in rows if val(2,v,q)] == [owner[v%49]]
    assert val(2,v,owner[v%49]) == 1
assert val(2,468,7) == 3
for v in (54,117):
    assert (val(3,v,3),val(3,v,7)) == (4,2)
    assert all(val(3,v,q) == 0 for q,m,b in panel)
assert [u for u in range(7) if val(u,(1-u)%7,Q)] == [0,1]
assert all(val(u,(1-u)%7,Q) == 1 for u in (0,1))

E = C+3*A
delta = 1+(4*pow(3,E,M)-1-a)%M
assert E > M.bit_length() and 3**(3*4117) > 5**405
# Failed box at n_minus = 4*3**E-delta.
# Same-target failed column and escape at n_plus = n_minus+M.
print(E, M, delta)
```

For the full-fibre check, the six order-\(49\) rows cover every \(v\equiv6\bmod7\) except \(v\equiv27\bmod49\). Inside that last class, \(v\not\equiv27\bmod343\) gives native valuation three at \(7\). The order-\(343\) reader covers \(v\equiv27\bmod343\) at exact valuation one. The height inequalities make all displayed points active and their remainders positive.

The escape is a periodic local survivor in the neighboring column. Its full two-square status is outside this certificate.
