# Shared index protection by descending order dependencies

Fix n≡2 mod 63 and a finite panel of inert primes. The two residuals are n−9−25^t and n−81−25^t. Let e_p=ord_p(25). Call p≥7 nonregular if v_p(25^e_p−1)>1. If the panel has at most three nonregular primes, there is one common t for which all panel valuations on both rows are even. This is local and does not guarantee the index lies in the active box for the given n.

For p≥7 let B_p be the at-most-two classes of t modulo e_p giving either residual divisible by p. Starting at each nonregular p with B_p nonempty, choose a prime power r^j dividing e_p and forbid the projection of B_p at that coordinate. If r is itself in the panel and B_r is nonempty, continue from r. Each path descends because e_p divides (p−1)/2. When forbiddances arrive at one coordinate, extend them to its highest assigned precision. If no coordinate is entirely forbidden, choose allowed digits there in advance, then finish the other digits by increasing prime. At any active contact of an unassigned panel prime p, the smaller coordinates determine t mod e_p. It is an ordinary prime by construction, and only one row can contact it since their difference is 72. The two digits mod p² of t can enforce valuation exactly 2, using ord_{p³}(25)=e_p p². The p-adic digit choices are compatible by CRT. The seeded 3 and 7 do not cause any contact: 3 is immediate, and at 7 the two differences n−9 and n−81 are 0 and 5 mod 7, outside the nonzero squares.

With at most three descending paths, each coordinate receives at most three projected constraints, each of size at most two. Prefer r≥7, otherwise mod 9 or mod 25 whenever possible. The only remaining orders are 3, 5, 15 (order 1 would require p|24). Among inert primes, order 3 occurs only at 7 and 31, and the two possible contact sets for n mod 31 are {3,10,14} and {13,20,24}, disjoint. Thus the shallow mod-3 prohibition is confined to one residue. Order 5 occurs only at 11 and 71, so there are at most two distinct shallow mod-5 sources. Order 15 has none: Phi_15(25)=61*181*1741*7621, all split. The maximum forbidden fractions at these coordinate types are 6/7, 1/3+4/9, and 4/5+2/25, respectively. They are all strictly below one, proving the sufficient condition without treating shared orders independently.

The control below uses the real shared order 10385=5*31*67 and tests the old failing choices and one common repair. The constructed witness is in the actual box for this example.

```python
def v(x,p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k

q = 20771
e = 5*31*67
assert pow(25,e,q*q) == 1 and pow(25,e,q**3) != 1
assert all(pow(25,e//r,q) != 1 for r in (5,31,67))

n = 1105521367401923640459948281 + 1982239917016703405946139521*25**322
P = (3,7,19,31,43,67,q)
assert n%63 == 2 and 4*max(81,25**321) < n
assert v(n-9-25**6,q) == v(n-81-25**321,q) == 1
assert v(n-9-25**6,31) == 2 and v(n-10,31) == 1
assert v(n-34,43) == v(n-106,19) == 2
assert all(v(n-h-25,p)%2 == 0 for h in (9,81) for p in P)
```

This does not rule out larger nonregular panels, establish asymptotic density, or address all unselected primes. No novelty claim is made.
