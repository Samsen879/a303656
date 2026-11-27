# Cube allowance audit: retained versus unrestricted prefixes

For q=2p^3+1 inert, no older inert prime r has p-order depth three. In the published cube allowance the older reads are thus all retained. Fix their observations, the old head, and (for each considered chart) the prime-to-p coordinates. Older tests see at most two p-digits on each axis. Varying the third p-digit or repairing the fourth source digit preserves those tests, provided all necessary non-p periods are held fixed. The free digits from an experiment in which some older tests were dropped cannot simply be reused here.

For fixed retained observations let V be the shifts modulo p^3 from phases passing the retained tests with the source test omitted. A reading t with a shift differing at valuation zero or two has a robust phase. On the residual branch, a first-blocker candidate must lie in V; outside V there is no allowed phase when all available differences have valuation one. Thus the exceptional readings are the t in V whose differences from every other v in V have valuation one. There can be at most p of these, since they share a residue modulo p and differ modulo p². This is the exceptional gate from ORDINARY_INERT_CUBE_DENSITY_BOUND.md.

For such a t, only retained-compatible prefixes realizing t are usable. Each has at most one next source digit that collapses its terminal line, under the ordinary-source, equal-depth cube hypotheses. If two usable prefixes have different collapse digits (or one cannot collapse), no common collapse can occur. This is a deletion test on the correct conditioning event. It does not assert a quantitative improvement or an equality for first-blocker probabilities.

## Same-target fixed-anchor obstruction

At p=59, q=410759 and reader r=2243, take the established target n=1772213347634616708129 and either non-p anchor (23,8817) or (8839,8817). At source reading 105837 mod p³ the unrestricted chart gives two distinct lower prefixes each with 59 terminal shifts. Once the reader is retained at these fixed anchors, every source-compatible first-digit pair has exact valuation one at r, preserved by all later p-digit changes. Therefore none of these unrestricted pairs are in the retained set for this anchor. Changing the reader's own primary coordinate separately repairs r on the very same target while preserving the source valuation and terminal shift. This scope matters: the mask is empty in the displayed anchors, not necessarily in the union over all non-p completions. The replay uses an ordinary terminal; it finds no common Wieferich terminal or unconditional saving.

```python
from math import isqrt, lcm

p, r, q = 59, 2243, 410759
n, d, H = 1772213347634616708129, 8817, 3960
L = lcm(H, 58, 38, 30, 42, 46, r)
assert q == 2*p**3+1 and r == 38*p+1
for t in (p, r, q):
    assert t%4 == 3 and all(t%i for i in range(2, isqrt(t)+1))
    assert all(pow(b, t-1, t*t) != 1 for b in (3, 5))
assert all(pow(b, (q-1)//p, q) != 1 for b in (3, 5))
assert all(pow(b, 38, r) != 1 for b in (3, 5))
assert (n%p**2, n%p**3, n%r**2) == (1407, 105837, r)
assert pow(3, 2*p*p, q) == pow(5, 47*2*p*p, q) != 1

def S(z, m):
    a, b = z
    return (pow(3, a, m) + pow(5, b, m)) % m

def exact(z, t, k):
    m = t**(k+1)
    return (n-S(z, m))%m in range(t**k, m, t**k)

def head(z):
    return ((n-S(z, 32))%32 == 17 and (n-S(z, 3))%3
            and all((n-S(z, t))%t for t in (7,11,19,23,31,43,47)))

def phase(c, x, h):
    P = p**h
    a, b = c+L*((x-c)*pow(L, -1, P)%P), d
    for i in range(h):
        U, M = L*p**i, p**(i+2)
        b += U*next(k for k in range(p) if n%M == S((a,b+U*k), M))
    if h == 3 and n%p**5 == S((a,b), p**5):
        b += L*P
    assert (a-c)%H == (b-d)%H == 0
    return a,b

f,g = [(pow(b, p-1, p*p)-1)//p for b in (3,5)]
for c in (23,8839):
    assert head((c,d))
    assert -pow(3,c,p)*f*pow(pow(5,d,p)*g, -1, p)%p == 44
    low = [phase(c,x,1) for x in range(p)]
    assert all(S(z,p*p) == n%(p*p) and exact(z,r,1) for z in low)
    assert all(pow(b,L*p,r*r) == 1 for b in (3,5))
    for x in (0,1):
        pts = [phase(c,x+p*p*j,3) for j in range(p)]
        assert len({S(z,q) for z in pts}) == p
        assert all(head(z) and exact(z,p,4) and exact(z,r,1) for z in pts)

a,b = phase(23,0,3)
U = lcm(H,q-1,p**4*(p-1),r-1,30,42,46)
assert U%r
b += U*next(k for k in range(r) if n%r**2 == S((a,b+U*k),r*r))
if n%r**3 == S((a,b),r**3):
    b += r*U
assert exact((a,b),r,2) and exact((a,b),p,4)
assert head((a,b)) and S((a,b),q) == S(phase(23,0,3),q)
print("Empty retained mask, split unrestricted lines, and reader repair verified")
```
