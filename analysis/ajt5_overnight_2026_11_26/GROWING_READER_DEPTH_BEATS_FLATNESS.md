# Growing actual reader depth defeats any fixed flatness threshold

**The obstruction can grow unconditionally.** For each \(k\ge1\), one can use \(6k\) actual inert prime readers to delete the entire anchored quarter-box, while the shortest dual width tends to infinity. A surviving column remains outside the box. At the next target in the same CRT class, that column enters the box and supplies a positive remainder passing the local panel.

### Cover the columns one digit at a time

Put \(T=7^k\). For each depth \(j=1,\ldots,k\), choose six distinct higher inert primes \(q>59\) with
\[
7^j\parallel q-1,\qquad q\equiv2\bmod59,
\]
such that \(3^{(q-1)/7^j}\) has order \(7^j\) and \(5^{(q-1)/7^j}=1\bmod q\).

These are actual arithmetic orders. For \(m=7^j\), use the cyclotomic field containing \(\zeta_{4\cdot59\cdot7m}\) and adjoin \(3^{1/m},5^{1/m}\). The radical multipliers are independent. A nontrivial Kummer relation would place a nontrivial positive real odd radical of \(3^a5^b\) in an abelian field. After canceling the largest common power of 7, the polynomial of this radical is irreducible by the 3-adic or 5-adic valuation, since at least one exponent is coprime to the remaining power of 7. Its minimal polynomial has only one real root, so a nontrivial such subfield could not be Galois over \(\mathbb Q\). Prescribe cyclotomic Frobenius by \(q\equiv3\bmod4,\ q\equiv2\bmod59,\ q\equiv1+m\bmod7m\), and prescribe the two radical multipliers to be \(\zeta_m,1\). Reduction gives the required power conditions, and Chebotarev supplies infinitely many choices at each depth. [Stevenhagen–Lenstra, *Chebotarëv and his density theorem*](https://link.springer.com/article/10.1007/BF03027290)

Let \(D\) be the lcm of \(522\) and all \(q(q-1)/7^j\) from the selected rows. Use
\[
c=99+Au,\qquad d=Bv,\qquad A=827D,\quad B=414D.
\]
Neither stride is divisible by \(7\) or \(59\). Their multipliers agree modulo \(413=7\cdot59\), so the actual \(7,59\) native coefficients retain the repair-lattice slope \(v\equiv-27u\bmod413\).

At a depth-\(j\) reader, \(3^A\) has exact order \(7^j\) modulo \(q^2\), while \(5^B=1\bmod q^2\). Use its six target readings to impose exact valuation one on the six columns
\[
u\equiv (a+1)7^{j-1}-1\pmod{7^j},\qquad 0\le a<6.
\]
For the column \(u\equiv b\), take \(n\equiv3^{99+Ab}+1+q\bmod q^2\). Each reading erases that column for **every** \(v\), and gives a unit off it. Across depths these are the disjoint classes where the first digit differing from the all-sixes string occurs. They cover precisely \(u\not\equiv T-1\bmod T\). In the one-column-per-reader model, \(6k\) is minimal for this cover: each of the six sibling classes at each depth needs a reader inside it.

### Height and width

Set the native target residues modulo \(7^3,59^3\) to give exact valuation two at \((u,v)=(T-1,0)\). This fixes the first repair coset to \(27u+v\equiv27(T-1)\bmod413\). Include \(n\equiv1\bmod4,\ n\equiv0\bmod3\). Write \(r\bmod M\) for the resulting CRT class and \(X=3^{99+A(T-1)}\).

Take \(n_-\) and \(n_+\) as the adjacent representatives of this class immediately below and at or above \(4X\). Here \(M<X\). For the selected panel, this follows from \(M\le12\cdot413^3D^2\) and the size of \(X\).

- At \(n_-\), the quarter-box has \(0\le u\le T-2\) and a \(v\)-bound at least \(T-2\). Every column is deleted.
- At \(n_+\), \((T-1,0)\) enters the quarter-box and passes all selected rows. Its remainder is positive.
- Before the column deletions, the exact native repair class of \((T-1,0)\) repeats modulo \(413^2\) on both axes. The number of exact-native candidates inside the negative box therefore grows without bound.

The homogeneous lattice stays fixed. Every nonzero dual functional has the form \((h,k')/413\) with integral numerator, so the negative box has shortest dual width at least \((T-2)/413\). This tends to infinity. The height assertions use \(M<X\), hence \(n_->3X\), and the fact that \(3^{827}>5^{414}\). Planar flatness controls the convex box before the arithmetic deletions. The family shows that no fixed width threshold alone can certify survival after these readers. [Averkov–Wagner, Theorem 2.2](https://arxiv.org/html/1003.4365v2)

The construction can also include the entire prime prefix through the largest selected \(q\). For each additional inert prime, choose the target residue to make the positive witness a unit. This leaves the negative deletion intact. If the largest selected prime is \(Q\), the enlarged modulus is at most \(12\cdot413^3Q^{2Q}\), while \(A(T-1)\ge827Q(Q-1)(T-1)/T\), so the height lift still fits.

### Exact two-depth replay

The negative control has index box \([0,47]\times[0,65]\), shortest width \(1334/413\), and eight exact-native cells before the column deletions. At the adjacent positive target, \((48,0)\) enters and passes the selected panel.

```python
from math import gcd, isqrt, lcm, prod

G = ((71,1303,2311,2591,4159,4943),
     (71443,157291,233143,249607,367207,420323))
P, T = 413, 49
rows = [(q,7**j,(a+1)*7**(j-1)-1)
        for j,group in enumerate(G,1) for a,q in enumerate(group)]
assert len({q for q,_,_ in rows}) == 12
assert all(q>59 and q%4==3 and (q-1)%m==0 and gcd((q-1)//m,P)==1
           and all(q%d for d in range(2,isqrt(q)+1)) for q,m,_ in rows)

D = lcm(522,*(q*((q-1)//m) for q,m,_ in rows))
A,B = 827*D,414*D
assert gcd(A*B,P)==1
def off(m,u,v):
    return (pow(3,99+A*u,m)+pow(5,B*v,m)) % m

t = {4:1,3:0}
for q,m,a in rows:
    assert pow(3,A*m,q*q)==pow(5,B,q*q)==1
    assert pow(3,A*(m//7),q)!=1
    t[q*q]=(off(q*q,a,0)+q)%(q*q)
    assert (t[q*q]-off(q*q,T-1,0))%q
for p in (7,59):
    assert pow(3,A,p)==pow(5,B,p)==1
    a=(pow(3,A,p*p)-1)//p*pow(3,99,p)%p
    b=(pow(5,B,p*p)-1)//p%p
    assert b and a==27*b%p
    t[p**3]=(off(p**3,T-1,0)+p*p)%p**3
assert all(sum(u%m==a for _,m,a in rows)==(u!=T-1) for u in range(T))

M=prod(t)
r=sum(a*(M//m)*pow(M//m,-1,m) for m,a in t.items())%M
# X = 3**e. Only its residue and an exact size bound are needed.
e=99+A*48
x=pow(3,e,M)
assert e>M.bit_length()                         # X > M
assert (r-4*x)%M + 1 + (4*x-1-r)%M == M          # n_+ - n_-
assert 3**(827*48)>5**(414*65)
assert 3**(99+827*48)<5**(414*66)                 # exact v-bound at n_-

U,V=47,65
w=27*U+V
assert min([P*U]+[U*abs((27*k+P//2)%P-P//2)+V*k
                   for k in range(1,w//V+1)])==1334
S=[(u,v) for u in range(U+1) if (v:=(27*(48-u))%P)<=V]
assert len(S)==10
assert sum(all((z:=(r-off(p**3,u,v))%p**3) and z%p**2==0
               for p in (7,59)) for u,v in S)==8
```

The growing feature is the reader depth. With a fixed \(7,59\) modulus and a fixed upper bound on the digits read, the local conditions are periodic in both indices. Once the box contains a full period, any periodic survivor enters. Here the increasing \(7\)-power orders move that boundary, and the strides grow with the actual reader periods. The result concerns constructed targets and anchored exponent charts. It establishes no fixed-stride obstruction, no complete obstruction across all exponent phases, and no two-square representation.
