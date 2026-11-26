from math import isqrt

M = 304365552096227318875363816654357253586027286308708901211
K = 1_172_027_091
Q = (3, 7, 11, 19, 23, 31, 43, 47, 59, 67, 71, 103, 107,
     127, 131, 167, 199, 227, 239, 347, 463, 487, 499, 631,
     1123, 4759, 11863)

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

def valuation(n, p):
    assert n > 0
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e

def surviving_columns(x, r, cap, side):
    shift = 0 if side == "parent" else r
    scale = 5 if side == "parent" else 1
    y = x if side == "parent" else 5*x + r
    cap = min(y, (cap + shift) // scale)
    columns = set()
    d, b = 0, 1
    while b + 1 <= cap:
        a = 1
        while b + a <= cap:
            v = y - b - a
            if v == 0 or all(valuation(v, p) % 2 == 0 for p in Q):
                columns.add(d)
                break
            a *= 3
        d, b = d+1, b*5
    return columns

def edges(cap):
    p = surviving_columns(M, 1, cap, "parent")
    c = surviving_columns(M, 1, cap, "child")
    return {(d, e) for d in p for e in (d, d+1) if e in c}

assert len(set(Q)) == 27 and all(p % 4 == 3 and prime(p) for p in Q)
assert edges(K - 1) == set()
assert (9, 10) in edges(K)
p = M - 5**9 - 1
q = 5*M + 1 - 5**10 - 3**19
assert all(p % t and q % t for t in Q)
assert prime(3251) and prime(458063)
assert valuation(p, 3251) == valuation(q, 458063) == 1
assert 5**10 + 3**19 - 1 == K
h = 234_405_419
assert (5*(h-1)-K, 5*h-K) == (-1, 4)
# Strict window versus active-at-zero control for a different digit.
r, m = 2, h-1
assert 5*m+r-5**10-3**19 == 0
assert m-5**9-1 == 9486**2+11936**2
print("PASS: 27-prime predecessor, unit-vs-norm contrast, and zero boundary")
