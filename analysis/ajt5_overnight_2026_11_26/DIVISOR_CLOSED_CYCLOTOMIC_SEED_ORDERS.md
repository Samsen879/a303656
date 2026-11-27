# Cyclotomic shells and divisor-closed norm seed multipliers

**An active inert prime cannot be repaired by putting it into the multiplier.** Splitting the gap into cyclotomic factors forces a new, larger inert prime. This applies to arbitrary multipliers, without a multiplicative-closure assumption. In particular, valid multipliers are closed under taking divisors, and every moving seed \(5^m-3^e=a^2+3b^2>0\) has \(m\equiv e\equiv2\pmod4\).

### The cyclotomic obstruction

Fix \(A=5^m>B=3^e\) with \(m,e\) even. For an odd inert prime \(q\ne5\), put \(o_q=\operatorname{ord}_q(A/B)\) and \(b_q=v_q(A^{o_q}-B^{o_q})\). LTE and cyclotomic factorization give
\[
v_q(\Phi_d(A,B))=
\begin{cases}
b_q,&d=o_q,\\
1,&d=o_q q^j,\ j\ge1,\\
0,&\text{otherwise}.
\end{cases}
\]
Indeed, summing the right side over \(d\mid k\) gives the LTE valuation of \(A^k-B^k\).

Now take \(d=o_q q^j\), \(j\ge1\). The cyclotomic value is odd and is \(1\bmod3\). Dividing out its single factor \(q\) leaves a number \(2\bmod3\), so another odd inert prime \(p\) occurs to odd valuation. It must have **exact order \(d\)**. A nonprimitive odd prime divisor of \(\Phi_d(A,B)\) must be the largest prime factor of \(d\), by the displayed formula and \(o_p\mid p-1\). Here that largest prime is \(q\). In particular \(p>q\).

Suppose a valid multiplier \(k\) contains any inert prime \(q\) with \(o_q\mid k\). Choose the largest such \(q\). The layer \(d=o_q q\mid k\) forces the prime \(p>q\) above. If \(p\mid k\), it contradicts maximality. Otherwise its odd valuation persists in \(A^k-B^k\). Either way the norm fails.

The dyadic layers give an unconditional exclusion as well. For \(d=2^j,\ j\ge1\),
\[
\Phi_d(A,B)=A^{2^{j-1}}+B^{2^{j-1}}
\]
has valuation one at \(2\). Its odd half is \(2\bmod3\), so it has an odd inert divisor to odd valuation and exact order \(2^j\). **Every even multiplier fails.** For arbitrary moving seeds, reduction modulo \(3\) and \(8\) first forces \(m,e\) even. If exactly one is divisible by \(4\), the gap has valuation three at \(2\). If both are divisible by \(4\), the gap is an even-multiplier extension of their halved exponents and fails by the dyadic argument.

### The remaining density question

For a fixed valid seed, let
\[
\mathcal O=\{o_q:q\text{ odd inert},\ b_q\text{ odd}\}.
\]
The exact all-prime criterion is now **\(k\) is valid iff no \(d\in\mathcal O\) divides \(k\)**. In particular \(2\in\mathcal O\). The shell argument puts every \(o_q q^j\), for odd inert \(q\ne5\) and \(j\ge1\), in \(\mathcal O\), so avoiding \(\mathcal O\) also prevents any active inert prime from dividing the multiplier. LTE then leaves only the even valuations of the primitive factors.

The forced shell indices have summable reciprocals: \(o_q\ge \log q/\log A\), and
\[
\sum_q\sum_{j\ge1}\frac1{o_q q^j}
=\sum_q\frac1{o_q(q-1)}<\infty.
\]
Hence these systematic exclusions alone leave positive density. More generally, **summability of the reciprocal minimal forbidden orders of \(\mathcal O\)** would give positive natural density of true seeds. For finite sets, the events \(d\nmid k\) are positively associated by CRT on prime valuations, giving a lower bound \(\prod_d(1-1/d)\). The omitted orders cost at most their reciprocal tail sum. Positive natural density would give consecutive multiplier ratios tending to one, and the sphere construction would then give uniform \(X^{1/2-\epsilon}\) coverage in both odd classes. I have not proved that summability. The unconditional uniform exponent remains \(13/34\), distinct from the per-height exponent \(1/2\).

### Exact control

For \(25,9\), the multiplier \(11\) fails at \(23\). Multiplying by \(23\) makes its valuation even and passes the small panel below, but the layer of order \(253\) has a new exact veto at \(1013\).

```python
from math import isqrt

def gap(k, mod):
    return (pow(25,k,mod)-pow(9,k,mod)) % mod

assert gap(11,23**2) == 20*23
assert gap(253,23**3) == 20*23**2
assert [gap(253,p) for p in (5,11,17)] == [1,2,1]
assert gap(253,32) == 16

p = 1013
assert p%3 == 2 and all(p%d for d in range(2,isqrt(p)+1))
assert gap(253,p) == 0 and gap(11,p) and gap(23,p)
assert gap(253,p*p) == 1006*p

# Same moving powers, both odd classes, actual positive representations.
Q,Z,t,v,r = 5**6,3**6,136,64,163
assert v*v+3*t*t == 4*(Q-Z)
for lam,x,y in ((1,109,136),(3,163,82)):
    S,P,A = x*x+y*y,lam*Z,(4-lam)*Z
    n = 5*Q+P-S
    assert Q<n<5*Q and n%4 == lam and (n-5*Q)%3
    assert 2*P-S == r*r-3*t*t and n == Q+A+v*v+r*r
```

Independent BigInt replay verifies the order 253 of the new inert prime 1013, its exact valuation-one obstruction, preservation of the small panel, and the two positive witness controls.
