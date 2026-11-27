# Odd-order muting beyond dyadic sign protection

**Odd orders give a conditional mute on the \(n\equiv9\pmod{24}\) slice without lowering the seventeen-source threshold.** The mute works when the order of \(-3\) has a suitable factor outside the order of \(5\). There is an exact limit at \(19\): every odd \(c\) has a collision in both \(d\)-parities, and the actual reader at \(271\) can prevent avoiding that collision by an invisible change of \(d\). [Pinned sector selection](https://github.com/Samsen879/a303656/commit/3a462d5c1cd3953a8077672b6bfbb2f79519c78a) · [Seventeen-source theorem](https://github.com/Samsen879/a303656/blob/3a462d5c1cd3953a8077672b6bfbb2f79519c78a/analysis/ajt5_overnight_2026_11_26/RANK_SEVEN_SIXTEEN_SOURCE_ESCAPE.md)

### A mute that preserves the full \(d\)-slice

Let \(q\mid n\) be inert with Legendre type \((-,+)\). Set
\[
a_q=\operatorname{ord}_q(-3),\qquad b_q=\operatorname{ord}_q(5),\qquad
D_q=\frac{a_q}{\gcd(a_q,b_q)}.
\]
Both orders are odd. For odd \(c\), a zero collision requires \((-3)^c=5^d\bmod q\). In the cyclic group this has a solution exactly when \(D_q\mid c\). Whenever it has one, the solutions form a single class modulo \(b_q\), which meets **both** \(d\)-parities. Thus \(D_q\nmid c\) mutes the entire row, while \(D_q=1\) defeats every fixed odd-\(c\) choice.

The helper reservation can be strengthened to \(\gcd(c,800730)=1\). At row 31, the eight unit classes modulo 30 give eight distinct values of \(3^c\), with at most three forbidden. At the subsequent fresh digits \(41,7,31\), excluding zero leaves \(40,6,30\) choices against at most \(9,5,7\) forbidden values. The reservation still allows the singly exceptional base-3 corrections. [Actual helper orders and reservation](https://github.com/Samsen879/a303656/commit/c3cee9b)

More generally, for each row to mute, choose a prime factor of \(D_q\) that is **outside the set of primes requiring a singly exceptional base-3 correction**. For a chosen factor outside the old reservation, impose \(c\equiv1\) modulo that factor. CRT joins these requirements, and the later corrections preserve them. This gives simultaneous unit rows while leaving every odd \(d\)-coordinate available.

In particular, let \(Z_{\rm ord}\) count the zero-observation \((-,+)\) common-exception rows that meet this protecting-factor condition. With the other counts as in the pinned result, a finite obstruction at \(n\equiv9\pmod{24}\) must satisfy
\[
U+Z_{-+}-Z_{\rm ord}+\min(Z_{+-},Z_{--})\ge17 .
\]
This is conditional on the orders in the hypothetical modulus. It makes no count of genuine common exceptional primes.

### The exact limit and actual controls

A further mute is possible when a \(d\)-coordinate is invisible to the other rows. Let \(L_{\rm rest}\) be their joint \(d\)-period, including parity. If \(b_q\nmid L_{\rm rest}\), every fixed other-row phase has more than one lift modulo \(b_q\), and one can avoid the single collision class. If \(b_q\mid L_{\rm rest}\), a phase in that collision class forces the collision in every lift preserving it.

At \(19\), \(a_q=b_q=9\) and \(-3=5^7\bmod19\), so the collision is \(d\equiv7c\bmod9\). At \(271\), the order of \(5\) is 27. Preserving its actual phase fixes \(d\bmod9\). The control below has exact valuation-one hits at \(19\) in both permitted sectors and an active nonzero observation at \(271\) on the shared phase. When \(271\) is instead given a zero observation, its own \(D_q=5\) makes it a unit throughout the \(c=19\) slice.

For a hypothetical **common** Wieferich row with \(v_q(n)=1\) and \(D_q=1\), the collision would already be rigid modulo \(q^2\). Both powers are prime-to-\(q\) roots of unity at that depth, so cancellation modulo \(q\) lifts to cancellation modulo \(q^2\). The actual controls below are ordinary to base 5.

```python
from math import gcd, prod

p,q,r = 19,31,271
c,d0,d1 = 19,19*16,19*7
assert gcd(c,800730)==1

def order(a,m,k,factors):
    assert pow(a,k,m)==1
    assert all(pow(a,k//l,m)!=1 for l in factors)

order(-3,p,9,(3,))
order(5,p,9,(3,))
assert pow(5,7,p)==(-3)%p
order(-3,q,15,(3,5))
order(5,q,3,(3,))
order(-3,r,15,(3,5))
order(5,r,27,(3,))
assert all(pow(5,z-1,z*z)!=1 for z in (p,q,r))

helpers = (71,5167,19531)
pairs = [(9,24),(p,p*p),(q,q*q),
         ((pow(3,c,r*r)+pow(5,d1,r*r)+r)%(r*r),r*r)]
pairs += [(pow(3,c,z),z) for z in helpers]
M = prod(m for _,m in pairs)
n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M

def res(d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert n%24==9 and all(n%z==pow(3,c,z) for z in helpers)
assert all(d%9==7*c%9 for d in (d0,d1))
assert (d0%2,d1%2)==(0,1)
assert all(res(d,4)==1 and res(d,3)!=0 for d in (d0,d1))
assert all(res(d,p*p)==p for d in (d0,d1))
assert pow(-3,3*c,q)!=1  # 31 is a unit for every d
assert n%r!=0 and res(d1,r*r)==r
assert res(d1+54,p)==0  # preserving the 271 phase keeps the 19 hit
assert res(d1+2,p)!=0 and res(d1+2,r)!=0

period = M//(r*r)
z = n+period*((r-n)*pow(period,-1,r*r)%(r*r))
assert z%(r*r)==r and (z-n)%period==0
assert pow(-3,27*c,r)!=1  # at this new zero reading, 271 is a unit
assert len({pow(3,j,31) for j in range(30) if gcd(j,30)==1})==8
for p,order3,order25 in ((5167,738,9),(71,35,5),(19531,6510,7)):
    assert next(j for j in range(1,order3+1) if pow(3,j,p)==1)==order3
    assert next(j for j in range(1,order25+1) if pow(25,j,p)==1)==order25
print("OK")
```

These are finite-sector results. They leave the seventeen-source threshold intact and distinguish an order-based mute from a restriction that changes the lower phase space.

The 19/271 example is a genuine obstruction to avoiding a *collision* while keeping the other row's higher order phase, not an obstruction to changing the odd valuation at the ordinary prime 19. For several invisible-digit mutes, the one-row period criterion must be applied with the period of all rows whose conditions are already to be kept; simultaneous independent removals need not commute. The stronger c-reservation uses a single CRT construction, so all its protected rows remain units as c is corrected.
