# Exact two-row parity masks for one shared exponent

Fix an integer n≡2 mod 63 and nonnegative shared t for residuals n−9−25^t and n−81−25^t. This interface first determines local parity, without imposing upper activation height. The output is a set of two-bit masks, each attained at **one** exponent; it is not the OR of all masks. In particular {0,1,2} has separate marginal survivors without a joint survivor. Only {0} means both rows are covered for every admissible index.

For a finite inert panel p≥7 and a fixed exponent congruence t≡a0 mod W, let e_p=ord_p(25), s_p=v_p(25^e_p−1), H=lcm(W,{e_p}). Use variables x_r=t mod r^v_r(H). For each row p has at most one mod-e_p contact class. If it contacts but it is nonzero modulo p^s_p, the valuation is fixed. Otherwise in a fixed mod-e_p contact class choose the unique residue u modulo p^k, k=v_p(H), at which the p-adic zero is reached modulo p^(s_p+k). This follows since 25^e_p maps successive p-adic digits bijectively onto the corresponding principal-unit digits; e_p is a p-adic unit, so one may equally describe the root by t mod p^k. If x_p differs from u, the exact finite valuation is s_p+v_p(x_p−u); if it matches, the remaining deeper digits can fix either finite parity. Only one row at any p can require these digits because their difference 72 is a p-adic unit. After all x_r are fixed, later digits can be chosen simultaneously at the different primes using CRT in t+Hz. Every attainable parity pattern has a stable residue cylinder and therefore nonnegative exponent representatives.

A frontier enumerator keeps one representative for every true/false pattern of the nested or disjoint coordinate congruence balls, the pending factor states for each row, and the surviving mask. With m_r tests a coordinate has at most m_r+1 patterns: a new laminar ball can split at most one existing atom. For example, the tests for the shell at u are its successive prefix balls. Pending factors update the mask by intersection, branching only when a deep parity choice is still possible. Do not merge masks by disjunction. This description assumes exact order and contact data; it does not claim tractable cost to compute discrete logs for arbitrary panels.

Exact comparison by literal enumeration of only the 31 coarse representatives in a frozen actual phase:

```python
q,p,L = 20771,40487,5*67*653
T = 3*L

def fixture(r):
    a,M = 0,1
    for d,z in [(63,2), (31**3,9+pow(25,T,31**3)+31**2),
                (q*q,10+q), (p*p,r)]:
        a += M*((z-a)*pow(M,-1,d) % d)
        M *= d
    return a + M*25**(T+1)

def masks(n):
    out = set()
    for j in range(31):
        t = T*j
        states = {3}
        for s in (31,q,p):
            for bit,h in ((1,9),(2,81)):
                r = (n-h-pow(25,t,s*s)) % (s*s)
                if r%s == 0:
                    off = {v & ~bit for v in states}
                    states = off if r else states | off
        out |= states
    return out

assert masks(fixture(10+p)) == {2,3}
n = fixture(81+pow(25,T,p*p)+p)
assert masks(n) == {0,1,2}
assert 4*max(81,25**T) < n
assert (n-9-pow(25,T,31**3)) % 31**3 == 31**2
assert (n-81-pow(25,T,p*p)) % (p*p) == p
```

The assertions check local feasibility of this selected strip, not all labels of a given integer, and not density or the original conjecture.
