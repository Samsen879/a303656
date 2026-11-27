# Short-jump order spectra and a two-axis exponential height obstruction

**The height bound is polynomial when the actual order spectra have bounded short-jump chains. Without an order restriction, an exponential loss is necessary.** The lower bound holds even when every higher reader has a nonzero target residue and reads both bases.

### A sharper bound from the actual orders

In the fixed-budget theorem, let \(h\) be the number of native and higher rows, and put \(L=2h^2+h+1\). For each basis direction \(i\) and prime \(\ell\), sort
\[
\{0\}\cup\{v_\ell(d_{q,i}):q\text{ a tested row}\},
\]
where \(d_{q,i}\) is the actual directional period used by the theorem. Use the ratio period for a zero reading, the joint order for a nonzero reading, and period \(p\) for a native exact-two test.

Starting at zero, stop at the first gap larger than \(J_\ell=\lfloor\log_\ell(L-1)\rfloor\). Call the last reachable exponent \(e_{\ell,i}\). The scale factors in the preceding absorption argument satisfy
\[
M_i\le\prod_\ell\ell^{e_{\ell,i}}.
\]
Indeed, a scale change replaces \(M_i\) by \(\operatorname{lcm}(M_i,d_{q,i})\) only when the residual period is less than \(L\). Each prime exponent therefore jumps to a listed level by at most \(J_\ell\), and cannot cross the first larger gap.

If the total number of reachable positive levels, summed over primes in each direction, is at most \(K\), then \(M_i\le(L-1)^K\). The previous grid argument gives a sufficient index-height factor \(L(L-1)^K\) times the basis coordinate widths, provided a compatible local residue exists. Bounded \(K\) gives a polynomial bound. \(K=O(\log h)\) gives a quasipolynomial bound. Orders beyond the first gaps can be arbitrarily deep.

### An exponential obstruction with both axes read

Put \(T=7^k\). At each depth \(j=1,\dots,k\), choose six inert primes \(q\) with \(7^j\parallel q-1\), \(q\equiv11\bmod12\), and \(q\equiv2\bmod59\). Require the \(7\)-primary projections of \(3,5\) to have respective orders \(7^j,7\), and require the projections to agree at depth one.

Chebotarev realizes these conditions. Over the cyclotomic field for the displayed congruences, adjoin the \(7^j\)-th roots of \(3,5\) and prescribe their Frobenius multipliers as \(\zeta_{7^j},\zeta_{7^j}^{7^{j-1}}\). The multipliers are independent by the positive-real-radical argument in an abelian field. These prescriptions concern orders modulo \(q\). [Stevenhagen–Lenstra, *Chebotarëv and his density theorem*](https://link.springer.com/article/10.1007/BF03027290)

As before, let \(D\) be the lcm of \(522\) and the factors \(q(q-1)/7^j\), and use
\[
c=99+827Du,\qquad d=414Dv.
\]
The native \(7,59\) coefficients give the first repair line \(27u+v\equiv27(T-1)\bmod413\) when the native target is chosen at \((T-1,0)\). In particular \(v\equiv u+1\bmod7\).

At depth \(j\), assign the six readers the six columns
\[
u\equiv b=(a+1)7^{j-1}-1\pmod{7^j},\qquad 0\le a<6.
\]
On such a column, \(v\bmod7\) is fixed by the native line. Both terms are therefore fixed modulo \(q^2\), and CRT sets the remainder to \(q\bmod q^2\). The target reading modulo \(q\) is nonzero: \(3\) has odd order at \(q\equiv11\bmod12\), and the \(5\)-step has order seven. Both terms are squares in an inert field, where \(-1\) is not a square, so they cannot cancel.

The outside phase \((T-1,0)\) is a unit at every reader. At depth one the two steps agree, so on the native line the offset is a nonzero constant times a seventh root indexed by \(u\). At deeper levels the stripe and the outside phase agree in \(v\bmod7\) and differ in \(u\bmod7^j\). The six columns at each level thus erase every \(u<T-1\), and the outside phase can have exact valuation two at \(7,59\).

Let \(X=3^{99+827D(T-1)}\). Choose adjacent representatives \(n_-<4X\le n_+\) of the same target CRT class. Its modulus is at most \(12\cdot413^3D^2<X\). At \(n_-\), both quarter-box index bounds are at least \(T-2\), and the \(u\)-bound is exactly \(T-2\). The box fails. At \(n_+\), \((T-1,0)\) enters and passes. With \(h=6k+2\) rows, this forces a uniform sufficient index-height threshold of at least \(7^{(h-2)/6}-1\) in this model. The contiguous \(7\)-power order spectrum is the feature the upper hypothesis excludes.

### Two-depth replay

The failed control has box \([0,47]\times[0,65]\), with nine exact-native candidates, all deleted. The adjacent positive control passes at \((48,0)\). The targets are exact CRT integers specified symbolically by their height boundary.

```python
from math import gcd, isqrt, lcm, prod

G = ((911,2423,3011,3767,6203,6791),
     (9311,29303,36947,51647,59879,115151))
T,P = 49,413
Q = [(q,7**j,(a+1)*7**(j-1)-1)
     for j,group in enumerate(G,1) for a,q in enumerate(group)]
assert len({q for q,_,_ in Q}) == 12
assert all(q%12==11 and (q-1)%m==0 and gcd((q-1)//m,P)==1
           and all(q%d for d in range(2,isqrt(q)+1)) for q,m,_ in Q)
D = lcm(522,*(q*((q-1)//m) for q,m,_ in Q))
A,B = 827*D,414*D
def off(s,u,v):
    return (pow(3,99+A*u,s)+pow(5,B*v,s)) % s

t = {4:1,3:0}
for q,m,b in Q:
    g,h = pow(3,A,q),pow(5,B,q)
    assert pow(g,m,q)==1 and pow(g,m//7,q)!=1
    assert pow(h,7,q)==1 and h!=1 and (m!=7 or g==h)
    assert pow(3,A*m,q*q)==pow(5,B*7,q*q)==1
    t[q*q] = (off(q*q,b,(b+1)%7)+q)%(q*q)
    assert t[q*q]%q and (t[q*q]-off(q,48,0))%q
for p in (7,59):
    assert pow(3,A,p)==pow(5,B,p)==1
    a=(pow(3,A,p*p)-1)//p*pow(3,99,p)%p
    b=(pow(5,B,p*p)-1)//p%p
    assert b and a==27*b%p
    t[p**3]=(off(p**3,48,0)+p*p)%p**3

M=prod(t)
r=sum(a*(M//m)*pow(M//m,-1,m) for m,a in t.items())%M
e=99+A*48
x=pow(3,e,M)                    # X modulo M
assert e>M.bit_length()          # X > M
assert (r-4*x)%M + 1+(4*x-1-r)%M == M
assert 3**(827*48)>5**(414*65)
assert 3**(99+827*48)<5**(414*66)
assert (r-off(4,48,0))%4==1 and (r-off(3,48,0))%3

C=[(u,v) for u in range(48) if (v:=(27*(48-u))%P)<=65]
assert sum(all((z:=(r-off(p**3,u,v))%p**3) and z%p**2==0
               for p in (7,59)) for u,v in C)==9
for u,v in C:
    q,_,_=next(row for row in Q if u%row[1]==row[2])
    assert (r-off(q*q,u,v))%q**2==q
```

These are bounds on actual local repairs in an anchored exponent chart. The strides and targets are constructed together. The positive control has a positive remainder and passes the specified panel, with the other inert divisors still unchecked.
