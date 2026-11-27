# Shared-parity constraints on two fixed exponent channels

**A shared parity gives a quantitative separation between the \(c=0\) and \(c=1\) channels for even \(n\).** At any candidate inert prime \(p\), at most \((p-3)/4\) residues of \(n\bmod p\) permit a hard row on both channels at that parity. If the two anchors must also agree on a cofactor that leaves a subgroup of order \(k\), this drops to at most \((k-1)/2\) residues. Two genuine base-5 exceptional primes can still be common on the same represented integer.

### The shared repair schedule

For even \(n\), the channels share an allowed \(d\)-parity. It is odd for \(n\equiv0,2\pmod8\) and even for \(n\equiv4,6\pmod8\). One channel fixes that parity at \(2\). Its norm condition is then settled modulo \(8\), and higher binary digits can repair the other channel.

At any odd ordinary owner, the two residuals for the **same** \(d\) differ by \(2\). At most one can collide modulo the owner prime, so its ordinary lift leaves the other a unit. This permits the published repairs at \(3,31,67,1523\) before reserving the later coordinates. In particular, \(d_5\) can make both \(11\) and \(20771\) units on both channels, since there are at most four exclusions among five digits. The later choices at \(653,1429,30469139\) each have at most two exclusions. Thus the three archived exceptional rows can be escaped on both channels with one \(d\). [Published repair schedule](https://github.com/Samsen879/a303656/blob/a94e44465f9309b2fa1e982379731fd8a8a502ea/analysis/ajt5_overnight_2026_11_26/FIXED_AXIS_HARD_ORDER_KERNEL.md)

### What the same target forces at a common row

Let \(o=\operatorname{ord}_p(5)\), and let \(e_0,e_1\) be the two collision anchors. At the shared parity, \(x=n-1\) and \(x-2=n-3\) must have the same prescribed quadratic character. Suppose the anchors also agree modulo \(m\mid o\). Then
\[
u=\frac{x-2}{x}\in K=\left\langle 5^{\operatorname{lcm}(m,\gcd(2,o))}\right\rangle,
\qquad x=\frac2{1-u}.
\]
The order \(k=|K|\) is odd because \(p\equiv3\pmod4\). For each inverse pair \(u,u^{-1}\ne1\), the two resulting \(x\)'s are related by \(x\mapsto-ux\), which reverses their quadratic character. At most one fits the shared parity. This proves the \((k-1)/2\) bound. Parity alone gives \(k\le(p-1)/2\).

There are two ways to use the bound.

- **At the same fixed \(n\)**, if the remaining ratio orders all divide a fixed odd \(K_0\), every common prime divides
  \[
  F_{K_0}(n)=\frac{(n-1)^{K_0}-(n-3)^{K_0}}2.
  \]
  In particular \(F_3=3(n-2)^2+1\), \(F_5=5(n-2)^4+10(n-2)^2+1\), and \(K_0=1\) excludes sharing altogether. The product of distinct common primes divides this explicit integer.
- **Across a fixed CRT family**, with the parity and cofactor coset locked independently of \(n\bmod p\), fewer than half of the local target classes already hard on one channel can be hard on both. Each first-channel anchor admits the same number of lifts, and at most \((k-1)/2\) of its \(k\) anchors can be shared. Without conditioning on first-channel hardness, the bound is less than \(1/4\) per candidate prime. Independence here is over CRT residues for a fixed prime family.

If a separate count requires \(k_0,k_1\) new hard rows on the two restricted channels and the cofactor test leaves at most \(u\) eligible common primes, the union requires at least \(k_0+k_1-u\) distinct new primes. For example, two per-channel requirements of seven and at most three eligible common primes would give eleven. The pinned note proves the three-prime exclusion. I could not verify from it that the prior seven-row bound applies separately to these restricted channels, so I have not promoted eleven to an unconditional bound.


### Independently constructed same-integer control

The following replay builds a represented integer by CRT, starting from \(N=26+X^2+Y^2\) and \(N=30\bmod32\). At each of the three actual exceptional primes, it first verifies both anchors have the same target modulo \(p\), then excludes at most two lifts in order to make both valuations exactly one. The first two pairs share the even parity and the stated cofactor; the third does not share the parity. No claim is made here about simultaneously satisfying a larger set of ordinary rows at those anchors.

```python
from math import isqrt
def crt(z,m,w,p):
    return z+m*((w-z)*pow(m,-1,p)%p)
def norms(z,p):
    for x in range(200):
        y=pow((z-x*x)%p,(p+1)//4,p)
        if y and (x*x+y*y-z)%p==0:
            y+=p*((z-x*x-y*y)//p*pow(2*y,-1,p)%p)
            assert (x*x+y*y-z)%(p*p)==0
            return x,y
    raise AssertionError('no witness')
data=((20771,13910,18064,31*67,5),(1645333507,426290984,974735486,2*9*30469139,3),
      (40487,0,20243,1,None))
x,y,m=2,0,32
for p,c0,c1,lock,small in data:
    assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
    assert pow(5,p-1,p*p)==1
    a,b=(1+pow(5,c0,p*p))%(p*p),(3+pow(5,c1,p*p))%(p*p)
    assert a%p==b%p
    z=next(a%p+k*p for k in range(3) if a%p+k*p not in (a,b))
    u,v=norms(z-26,p)
    x,y,m=crt(x,m,u,p*p),crt(y,m,v,p*p),m*p*p
    if small:
        assert c0%2==c1%2==0 and (c0-c1)%lock==0
        ratio=pow(5,(c1-c0)%(p-1),p)
        assert ratio!=1 and pow(ratio,small,p)==1
    else: assert c0%2==0 and c1%2==1
N=26+x*x+y*y
assert N%32==30
for p,c0,c1,_,_ in data:
    for a,d in ((0,c0),(1,c1)):
        r=(N-3**a-pow(5,d,p*p))%(p*p)
        assert r and r%p==0
print('OK')
```
