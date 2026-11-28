# A rank-19 true minimum behind the original panel through 883

**Rank 19 is feasible through cutoff 883.** The constructed target \(n\) matches all **44,460 exact valuations** of the original \(N\) on the 570-row phase and satisfies \(N<n<N(1+10^{-91})\). Its rank-19 residual at \((23,209)\) is a primitive sum of two squares. Among the earlier rows, only ranks 7 and 14 survive the old panel. They have valuation one at **887** and **907**, respectively. These are the two smallest inert primes above 883, so the construction attains #123’s lower bound \(887\cdot907=804509\) on the extra coarse CRT product. The result certifies one constructed target with minimum rank 19. The quartet through 883 and the earlier ranks of the original \(N\) remain open. [#123 and its joint-prime obstruction](https://github.com/Samsen879/a303656/pull/123/files)

### CRT and height

For each old prime \(p\), let \(e_p=\max_i v_p(N-S_i)\). The congruence \(n\equiv N\bmod p^{e_p}\) preserves all valuations below \(e_p\). Each row at valuation \(e_p\) forbids one next digit. I fixed the original next digit for the ten primes with the largest fraction of forbidden digits, then sieved the remaining digits in a single scalar progression. The new rows use coarse congruences at 887 and 907 and forbid valuation two or higher.

Finding a square root for the chosen rank-19 residual was a bounded search. The verification is exact. A root modulo the residual divided by 101 combines with \(10^2\equiv-1\pmod{101}\). The resulting lattice \(x\equiv ty\pmod m\) has determinant \(m\), and every squared length is divisible by \(m\). Two-dimensional Gauss reduction gives a nonzero squared length at most \(2m/\sqrt3\), hence exactly \(m\). The replay also checks coprimality directly.

### Portable certificate

```python
from math import gcd, isqrt

N = 3**540 + 5**270 + 7986363
S = sorted(3**(5+18*u) + 5**(200+9*v)
           for u in range(30) for v in range(19))
top = min(3**545 + 5**200, 3**5 + 5**371)
assert len(S) == len(set(S)) == 570
assert [S[i] for i in (6, 13, 18)] == [
    3**113 + 5**200, 3**239 + 5**200, 3**23 + 5**209]

def val(r, p):
    e = 0
    while r % p == 0:
        r //= p
        e += 1
    return e

P = [p for p in range(3, 908, 4)
     if all(p % q for q in range(2, isqrt(p)+1))]
assert P[-2:] == [887, 907]
P = P[:-2]

def table(n):
    return [[val(n-s, p) for s in S] for p in P]

T = table(N)
assert len(T) == 78
assert [i+1 for i in range(19)
        if all(row[i] % 2 == 0 for row in T)] == [7, 14, 19]

fixed = {331, 443, 463, 503, 523, 563, 571, 587, 599, 607}
congruences = [(N, p**(max(row) + (p in fixed)))
               for p, row in zip(P, T)]
congruences += [(S[6], 887), (S[13], 907)]

c, D = N % 8, 8
for residue, modulus in congruences:
    if modulus > 1:
        c += D * ((residue-c) * pow(D, -1, modulus) % modulus)
        D *= modulus

n = N + (c-N) % D + 12_682_426*D
assert len(str(D)) == 159
assert S[-1] < N < n < top and 10**91*(n-N) < N
assert table(n) == T
assert [[val(n-S[i], p) for p in (887, 907)] for i in (6, 13, 18)] == [
    [1, 0], [0, 1], [0, 0]]

m = n-S[18]
r, rem = divmod(m, 101)
assert rem == 0 and gcd(r, 101) == 1 and r % 4 == 1
t = pow(7, (r-1)//4, r)
assert (t*t+1) % r == 0
t += r * ((10-t) * pow(r, -1, 101) % 101)
assert (t*t+1) % m == 0

def dot(x, y):
    return x[0]*y[0] + x[1]*y[1]

u, w = (m, 0), (t, 1)
while True:
    if dot(u, u) > dot(w, w):
        u, w = w, u
    a, d = dot(u, u), dot(u, w)
    if abs(2*d) <= a:
        break
    k = (2*d+a)//(2*a)
    w = w[0]-k*u[0], w[1]-k*u[1]

assert dot(u, u) + S[18] == n and gcd(*u) == 1
print(n, abs(u[0]), abs(u[1]))
```
