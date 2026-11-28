# Exact primitive displacement menus for adjacent 3/5 labels

For two adjacent labels, orient the pair as \(L,U\) so that the signed difference \(D=U-L\equiv6\bmod8\); also \(3\nmid D\). The notation \(L,U\) here does not imply an order on the integers. For \(Q=27\cdot2^k\), \(k\ge5\), put \(\ell=\lceil k/2\rceil\). The minimum size of a primitive displacement menu covering all locally feasible common target classes is
\[
4(\ell-1).
\]
It has a realization with maximum displacement \(O_\varepsilon(Q^{3/8+\varepsilon})\). This sharpens [#96](https://github.com/Samsen879/a303656/pull/96), which gives elementary \(\Theta(k)\) size and \(O(\sqrt Q)\) maximum length. This is not a sharp displacement-length exponent or a pointwise result.

## The exact addresses

Put \(B=N-L\), \(A=u^2+v^2\), and \(H=(D+A)/2\). A displacement covers a class when the integer line \(u x+v y=H\) contains a point of norm \(B\bmod Q\). The two local primes can be studied separately. The \(2\)-adic determinant equation for the scaled norm \(B/2^{2j}\) uses the same criterion and lifting as #96.

At the dyadic prime, use precisely these \(\ell-1\) groups:
\[
v_2(H)=s\quad(2\le s<\ell),\qquad 2^\ell\mid H.
\]
The nonzero even valuations \(v_2(B)=2s\ge4\) force the corresponding group, and the zero class forces the last, by taking out the largest common power of 2 from the low coordinates. These are all necessary to cover every class. The prescriptions for \(A\) are \(2^{s+1}-D\bmod2^{s+2}\), and \(-D\bmod2^{\ell+1}\) for the last. Every prescription has \(A\equiv2\bmod8\).

Here is why these same groups suffice. For \(v_2(B)=1\), writing \(\rho=B/2\), local feasibility forces \(\rho\equiv-D/2\bmod8\). For any group, \((H-D/2)\rho-(H/2)^2=1\bmod8\): when \(H=4\bmod8\), the added and subtracted 4 cancel. For \(v_2(B)=2j+1\ge3\), let \(r=k-2j-1\) be the precision of the odd part \(\rho\). A squared determinant after removing the factors of 2 is
\[
C=(H-D/2)\rho-(H/2^{j+1})^2.
\]
For \(r\ge4\) use \(v_2(H)=j+2\) or \(2^{j+3}\mid H\), which are available: these make \(C\) respectively \(a\rho-4\) or \(a\rho\) modulo 8, with \(a=H-D/2\equiv-D/2\bmod8\) and \(a\rho\equiv1\bmod4\). One is 1 modulo 8. For \(r=3\), take \(v_2(H)=j+1\); \(C\) is 0 or 4 modulo 8. Fix a matching square \(w^2\bmod8\) and complete the odd part by taking \(\rho=(w^2+(H/2^{j+1})^2)/a\) in \(\mathbb Z_2\). For \(r=2\), the same choice works with \(w=0\) since only \(1\bmod4\) is prescribed. For \(r=1\), the last group suffices: choose \(w=0\) if \(H/2^{j+1}\) is odd, or \(w=1\) if it is even, then the same formula gives an odd representative. Even nonzero valuations and zero were handled in #96.

Modulo 27, the low singular residuals are \(B\equiv0,9,18\). These can only be covered by \(A\equiv-D\bmod3\), since \(AB-H^2\) must be a square. At most two of the three are covered by any one \(A\), since only 0 and 9 are squares among multiples of 9 modulo 27. The choices \(A\equiv-D,-D+3\bmod9\) cover all three: if \(A\equiv-D\bmod9\) then \(H^2\equiv0\bmod27\), and otherwise \(H^2\equiv9\bmod27\); the missing one in the first choice is included by the second. Swapping endpoints, the other singular side requires the disjoint addresses \(A\equiv D,D+3\bmod9\). The nine double-unit classes have determinant square \(1\bmod3\) for all four addresses and lift. A displacement with \(3\mid A\) has both coordinates divisible by 3, so its dot product cannot equal \(H\). Thus four addresses per dyadic group are necessary and sufficient. In particular the exact count is not inferred from the finite replay.

## Turning an address into a short primitive vector

All the addresses are of the form \(A\equiv a\bmod M\), \(M=9\cdot2^m=O(\sqrt Q)\), \(a\equiv2\bmod8\), \(3\nmid a\). The number \(C^*(Y;M,a)\) of primitive signed lattice points in this address, with norm at most \(Y\), satisfies
\[
C^*(Y;M,a)=\frac{24}{\pi}\frac{Y}{M}
 +O_\varepsilon(\sqrt Y\,M^{-1/4+\varepsilon})
 \quad (M^{3/2}\le Y\le M^2/4).
\]
Here is the analytic input and the primitivity check. The unfiltered count comes from [Tolev, equations (2) and (10)](https://arxiv.org/pdf/1106.3474v2). There are \(2^{m+1}\) solutions modulo \(2^m\), because every odd first coordinate has four possible second coordinates, and twelve solutions modulo 9, giving \(\eta_a(M)=8M/3\). Common divisors \(d\) are coprime to 6. Use Möbius inversion with \(B_0=\sqrt Y\), \(D_0=B_0M^{-3/4}\), \(E_0=B_0/\sqrt M\).
- For \(d\le D_0\), Tolev at \(Y/d^2\) gives an error sum \(O_\varepsilon(M^\varepsilon(D_0\sqrt M+Y^{1/3}D_0^{1/3}))\). Extending the main term adds \(O(Y/(M D_0))\) and gives the Euler factor \(\prod_{p\ge5}(1-p^{-2})=9/\pi^2\).
- For \(D_0<d\le E_0\), count integer reduced norms in a progression, weighted by the divisor bound for representations. The sum is \(O_\varepsilon(M^\varepsilon(Y/(MD_0)+E_0))\).
- For \(d>E_0\), on each dyadic block \(W<d\le2W\) the number of reduced-norm/divisor pairs is \(O(\min(W,Y/W^2))\). In one direction each \(d\) has at most one reduced norm; in the other direction a reduced norm gives at most eight classes for \(d\) modulo \(M/2\) after dividing by 2, and each class occurs at most once since \(d\le M/2\). The dyadic sum is \(O(Y^{1/3})\), which is at most \(B_0M^{-1/4}\) in the stated range. Include the divisor bound for multiplicity as before.
These errors yield the displayed estimate. Choosing \(Y=M^{3/2+2\varepsilon}\) with sufficiently small \(\varepsilon>0\) gives positive count for large \(M\) and length \(O_\varepsilon(M^{3/4+\varepsilon})\). A bounded set of small moduli is covered by the elementary odd-coordinate CRT construction from #96. The count is uniform in the address.

## Scale and real witnesses

Every chosen vector is primitive and each coordinate is odd. Modulo 27 at least one coordinate is a unit; swap axes if needed. Retain the scale \(2^j\) in the integral dot-product line as in #96, so an address with \(m=j+O(1)\) gives physical step \(O_\varepsilon(Q 2^{-j(1/4-\varepsilon)})\) for nonzero classes. For the zero class the step is \(O_\varepsilon(Q^{7/8+\varepsilon})\). In the ordinary-height window of #96 the latter gives sublinear forward gaps for \(Q\le X^{4/7-\eta}\) at the zero class, for any fixed \(\eta>0\) and sufficiently small \(\varepsilon\); all classes keep the #96 \(Q=o(\sqrt X)\) regime. None of these statements prescribes the actual target integer.

The replay checks dyadic boundaries, the native \(k=13\) positive witness, and a vector which satisfies the dyadic address but cannot satisfy the three-adic condition.

```python
from math import gcd

L, U = 3**4+5**6, 3**5+5**7
D, X = U-L, 10**12

def norms(m):
    s = {x*x % m for x in range(m)}
    return {(x+y) % m for x in s for y in s}

for k in range(5, 11):
    m, ell = 1<<k, (k+1)//2
    got = set()
    for j in range(2, ell+1):
        h, h0 = j+(j<ell), (1<<j if j<ell else 0)
        v = next(v for v in range(2<<h)
                 if (v*v-2*h0+D+1) % (2<<h) == 0)
        H = (D+1+v*v)//2
        got |= {((H-v*y)**2+y*y) % m for y in range(m)}
    s = norms(m)
    assert got == {b for b in s if (b-D) % m in s}

def shortest(r):
    return min((u*u+v*v,u,v)
               for u in range(1,64,2) for v in range(1,u+1,2)
               if gcd(u,v)==1 and (u*u+v*v+D)%256==0
               and (u*u+v*v+D-r)%9==0)

assert shortest(0)==(1850,41,13) and shortest(3)==(314,17,5)
n, x, y = 1131810708826, -320832, 1014336
assert n==L+x*x+y*y==U+(x-41)**2+(y-13)**2
assert X<n<2*X and (n-L)%(27*2**13)==0
assert (-((D+314)//2)**2)%27==18
assert 18 not in {x*x%27 for x in range(27)}
print("OK")

```
