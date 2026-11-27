# Factor-free signed-index selection and an explicit high-order barrier

This follows [signed full-modulus masks](https://github.com/Samsen879/a303656/commit/e93c06499943722a1bc6dbf7b20f8844d7edcba2). Start from the public chart modulus and native root/menu. For each prime \(20{,}000<\ell\le343^2\) coprime to \(R\), calculate \(h_\ell=\operatorname{ord}_\ell(R)\) by factoring only the **small** integer \(\ell-1\). The first signed return is \(R^{h_\ell/2}+1\) when \(h_\ell\) is even and \(R^{h_\ell}-1\) otherwise. Retain the index if it is at most 16,384 and put the retained auxiliary primes into a squarefree exponent envelope \(E\).

The saturated gcd of the two powers minus one with \(R\) captures the common prime support of the normalized axes \(3^{LH},5^{LH}\) where both orders divide \(E\). This is an order condition modulo each prime, not necessarily an equality at its full prime-power depth. Phase checks use the actual same menu lift at each prime. For the block deletion on the captured support in the replay, evaluate powers modulo its squarefree part if necessary (saturated gcd equality rather than full equality to 1 handles multiplicities); on the old row the captured support is independently prime. A block is deletable exactly when its factors are absent from every required order on that support. Balanced recursion on a squarefree envelope uses at most \(1+2s\lceil \log_2 N\rceil\) tests for \(s\) surviving primes among \(N\) candidates. In the old row, actual factor-free selection yields 3,772 candidates, 45 deletion checks, and exactly the two signed masks with indices 7,032 and 12,323. The existing [full phase replay](https://github.com/Samsen879/a303656/commit/26575f9c2ca06e032a2947555db77561d5840438) closes the old support using the complement. There is no additional row closure.

For the second actual row, \(R=5983388811034150170813207181151374478873\) and \(x=55710389148389160288578247553687525224\). The frozen chart source is \((13,67)\) and its independently regenerated menu has \((E\bmod49,k)=(25,171)\). The same three-band enumerator in the earlier replay gives this menu by requesting \((13,67)\). The native \(q=9881419104602277971980597987\) has phase logs 327,340 relative to \(x\), or tag \((33,236)\), so it is incompatible. The two normalized axes have prime order \(\ell=71663686702074742700351\); the two finite power sets for exponent magnitudes at most 120 meet only at 1. Every nonzero word in that box therefore has order \(\ell\). The actual \(R\bmod\ell\) has odd order \(h=35831843351037371350175\). No plus mask touches \(\ell\), and a minus mask does so only at multiples of \(h\). Finite products or lcms at smaller indices cannot break this local obstruction. The bounded envelope captures no support on this actual row.


```python
from math import gcd, isqrt, lcm, prod

r0=7320452716949759354345164426511787518233
r1=5983388811034150170813207181151374478873
x=55710389148389160288578247553687525224
def factors(n):
    ps, d=set(),2
    while d*d<=n:
        while n%d==0:
            ps.add(d); n//=d
        d+=1
    if n>1: ps.add(n)
    return ps
def ordsmall(r,p):
    h=p-1
    for q in factors(h):
        while h%q==0 and pow(r,h//q,p)==1: h//=q
    return h
def envelope(R):
    lim=343**2
    ok=bytearray([1])*(lim+1)
    ok[:2]=b'\0\0'
    for p in range(2,isqrt(lim)+1):
        if ok[p]: ok[p*p::p]=b'\0'*((lim-p*p)//p+1)
    a=[]
    for p in range(20001,lim+1):
        if ok[p] and R%p:
            h=ordsmall(R,p)
            m,sg=(h,-1) if h%2 else (h//2,1)
            if m<=16384: a.append((p,m,sg))
    return a
L=lcm(*range(1,20001))
while L%7==0: L//=7
def axes(R):
    return [pow(b,L*7**R.bit_length(),R) for b in (3,5)]
def capture(R,A,B,E):
    c=gcd(R,pow(A,E,R)-1,pow(B,E,R)-1)
    while gcd(R,c*c)!=c: c=gcd(R,c*c)
    return c
M=envelope(r0)
A,B=axes(r0)
E=prod(q for q,_,_ in M)
C=capture(r0,A,B,E)
assert len(M)==3772 and C==83464673905159
assert all(C%d for d in range(2,isqrt(C)+1))
def prune(A,B,C,L,E):
    p=prod(q for q,_,_ in L)
    if pow(A,E//p,C)==pow(B,E//p,C)==1: return E//p,1
    if len(L)==1: return E,1
    m=len(L)//2
    E,l=prune(A,B,C,L[:m],E)
    E,r=prune(A,B,C,L[m:],E)
    return E,1+l+r
E,t=prune(A,B,C,M,E)
assert t==45 and [z for z in M if E%z[0]==0]==[(42193,7032,1),(73939,12323,-1)]

q=9881419104602277971980597987
ell=71663686702074742700351
r=1433273734041494854007
f,g=3981683,179983405766041
for p in (f,g):
    assert p%2 and all(p%d for d in range(3,isqrt(p)+1,2))
def pock(p,a,F):
    f=prod(F)
    assert (p-1)%f==0 and f*f>p and pow(a,p-1,p)==1
    assert all(gcd(pow(a,(p-1)//d,p)-1,p)==1 for d in set(F))
pock(r,5,[2,f,g])
pock(ell,11,[2,5,5,r])
pock(q,2,[ell])
assert r1==605519181779*q and q%1372==687
assert pow(x,343,r1)==1 and gcd(r1,pow(x,49,r1)-1)==1
assert (1+pow(x,13,r1)-x-pow(x,67,r1))%r1==0
A,B=axes(r1)
assert capture(r1,A,B,prod(v for v,_,_ in envelope(r1)))==1
assert A%q!=1 and B%q!=1 and pow(A,ell,q)==pow(B,ell,q)==1
assert ({pow(A,j%ell,q) for j in range(-120,121)} &
        {pow(B,j%ell,q) for j in range(-120,121)})=={1}
h=(ell-1)//2
assert h==25*r and pow(r1,h,ell)==1
assert pow(r1,h//5,ell)!=1 and pow(r1,h//r,ell)!=1
F=(q-1)//343
assert [pow(b,F,q) for b in (3,5)]==[pow(x,F*j%343,q) for j in (327,340)]
assert 327%49==33 and 340*pow(327,-1,343)%343==236
```
