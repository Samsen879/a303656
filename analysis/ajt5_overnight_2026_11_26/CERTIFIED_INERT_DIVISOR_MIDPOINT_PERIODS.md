# A certified inert divisor excludes many midpoint periods

**One certified odd-valuation inert divisor can rule out exponentially many midpoint periods at once.** For the genuine first-kernel case \((\ell,d)=(23,139)\), it rules out the first **267 full periods**. A midpoint in the second period passes the earlier congruences, including the mod‑17 test, but is ruled out by this bound.

### The exact divisor bound

Let \(\ell>5\) be prime, \(H=(5^\ell+3^\ell)/8\), and \(d=6\ell+1\). Consider a putative factorization
\[
H=d s^2q_1q_2
\]
with \(d\) squarefree and \(q_1,q_2\) distinct inert primes. Put \(C=H/d\) and \(N=s(q_1+q_2)/2\).

Every prime divisor of \(H\) has exact order \(\ell\) for \(-5/3\), so it is \(1\bmod2\ell\). In particular, \(d\) must be prime if it occurs as this kernel, since \(d<(2\ell+1)^2\). It is split modulo \(3\). Now certify an inert prime \(p\) with \(v_p(H)\) odd. **One of \(q_1,q_2\) must equal \(p\)**. The factor \(d\) cannot supply that inert prime, and \(s^2\) contributes an even valuation.

Write \(q\) for the other witness. If exact congruences or divisibility give \(|q-p|\ge D\), then
\[
\frac{N^2}{C}
 = \frac{(p+q)^2}{4pq}
 = 1+\frac{(q-p)^2}{4pq}
 \ \ge\ 1+\frac{D^2}{4p(p+D)}.
\]
The last bound holds on both sides of \(p\). For \(q=p+t\), \(t^2/[p(p+t)]\) increases with \(t>0\). For \(q=p-t\) it is larger still.

The default \(D=6\ell\) follows from the shared inert residue class modulo \(6\ell\). When \(p=O(\ell)\), the bound puts \(N\) a fixed positive fraction of \(\sqrt C\) above \(\sqrt C\). Since \(C\asymp5^\ell/\ell\), it excludes \(\gg 5^{\ell/2}/\ell^{5/2}\) full periods of length \(72\ell^2\) for each qualifying exponent. The bound holds for every \(s\).

### Two exact half controls

**At \(\ell=23\)**, \(p=47\) and \(d=139\) both have valuation one in \(H\). Here \(p\) is the least possible prime divisor, so write \(q=p+6\ell j\) with \(j>0\). Because \(dH\equiv5\bmod8\) and \(dH\equiv pq\bmod8\), we get \(j\equiv2\bmod4\). Also \(-5/3\) is a square modulo each inert witness, so quadratic reciprocity gives \(q\equiv\pm2\bmod5\). With \(p=47\), this gives \(j\equiv0,2\bmod5\). Together these leave \(j\equiv2,10\bmod20\).

The first candidate \(q=323\) is composite. The second, \(1427\), gives \(H\bmod1427=1273\). Thus \(j\ge22\), and the bound gives \(N\ge13{,}461{,}177\). Starting at \(\lfloor\sqrt C\rfloor+1=3{,}274{,}194\), this skips 267 full periods. The genuine pair is \(47,228092436443\). The earlier local tests all admit \(N=3{,}339{,}187\), which lies below the new cutoff.

**At \(\ell=853\)**, the same half has \(v_{3413}(H)=v_{5119}(H)=1\), with \(p=3413\) inert and \(d=5119=6\ell+1\). The default \(D=6\ell\) excludes more than \(10^{287}\) periods. This is an exact exclusion for that half and kernel. Existence of a full witness pair at \(\ell=853\) was not established.

The method requires an odd-valuation inert divisor small enough to give a useful cutoff. The first-kernel condition alone supplies a split divisor. It gives no uniform bound on the size of the smallest odd-valuation inert divisor.

```python
from math import isqrt

def prime(n):
    return n > 1 and all(n % a for a in range(2, isqrt(n)+1))

def cutoff(ell, p, d, a, b, D):
    assert all(map(prime, (ell,p,d))) and p % 3 == 2 and d == 6*ell+1
    H = (5**ell+3**ell)//8
    assert 25**ell-9**ell == 8*(5**ell-3**ell)*H
    assert H % (p*p) == a*p and 0 < a < p
    assert H % (d*d) == b*d and 0 < b < d
    C, q0 = H//d, p+D
    L = isqrt((C*(p+q0)**2-1)//(4*p*q0))+1
    return H, C, L, (L-isqrt(C)-1)//(72*ell*ell)

ell,p,d,q = 23,47,139,228092436443
H,C,L,K = cutoff(ell,p,d,36,108,6*ell*22)
assert p+6*ell*2 == 17*19 and H % (p+6*ell*10) == 1273
assert H == d*p*q and prime(q) and q % 3 == 2
assert (p+q)//2 >= L and (L,K) == (13461177,267)

N = 3339187
t2 = N*N-C
assert (N-1)%ell == t2%(9*ell*ell) == 0
assert N%2 == 1 and t2%16 == 4 and pow(t2,8,17) == 1
assert N < L

assert cutoff(853,3413,5119,566,619,6*853)[3] > 10**287
```

Independent BigInt verified exact odd valuations at both exponents, the first 267 excluded periods at 23, the earlier mod-17 false positive, and the 288-digit period count at 853. There is a genuine witness pair at 23. The argument at 853 excludes these periods for any such pair but does not establish that a pair with the specified kernel exists.
