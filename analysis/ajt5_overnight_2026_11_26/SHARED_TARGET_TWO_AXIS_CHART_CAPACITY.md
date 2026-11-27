# The shared target improves the two-axis chart capacity bound

Use the selected chart c=C+16i,d=D+144k, whose two widths are both comparable to a bit-height parameter H. At an inert prime p≥7 write a=ord_p(3^16), b=ord_p(5^144), g=gcd(a,b), ℓ=lcm(a,b). Let ν_p(n) count cells in an exact a×b period whose two powers sum to n mod p. Exact-one markers modulo p² can count no more than these congruence cells.

If p divides n, the two power cosets must meet after negating the second. This happens exactly when (−5^D·3^(−C))^ℓ=1, in which case the intersection has exactly g points. Their periodic density is 1/ℓ; otherwise it is zero. At C=3,D=1, primes 23 and 67 both have order pair (11,11), but the zero target hits respectively 11 and 0 cells.

If p does not divide n, scaling gives cosets on x+y=1. When (ab)²<p³ and ab≥27, the one-coset case of [Mit’kin's Lemma 10 as stated in Shkredov, Solodkova and Vyugin](https://arxiv.org/pdf/1302.3839v3) gives O((ab)^(1/3)). If p³≤(ab)², multiplicative character expansion gives ab/p+O(√p); the product of the two normalizing indices cancels the number of Jacobi sums. This is also O(ab/p+(ab)^(1/3)). Bounded ab follows from ν_p≤min(a,b). Thus the periodic density is O(p^(−1)+(ab)^(−2/3)).

Write T=H/log H. A sublinear bit cost uses o(T) distinct primes. As in the [order-diversity obstruction](https://github.com/Samsen879/a303656/commit/9f031aef172346b8d1408d255c1a2b719abf746a), those with max(a,b)≥T have total marked fraction o(1) by the one-axis bound. For the remainder, periodic density carries over to the actual chart with additive O(1/H) per prime, because ν_p≤min(a,b). It follows that nonzero reads with p≥T and ab≥T^(3/2), and zero reads with ℓ≥T, each aggregate to o(1) coverage. In particular comparable orders with small enough gcd can be excluded already on the T^(3/4) scale under these hypotheses.

All primes with exact order pair (a,b) divide gcd(3^(16a)−1,5^(144b)−1) and are ≥2ℓ+1, since both base powers are quadratic residues and p is inert. If K≤a,b≤2K and g≤K^(2/3), each prime has periodic density O(K^(−4/3)) and there are O(K/log K) possibilities per fixed pair. So even o(K^(1/3)log K) pairs in this range (a growing number) cannot cover a positive fraction when K grows and total bit cost is o(H). The actual finite-rectangle errors are charged separately by o(T)/H. This leaves other short/high-gcd sectors open and does not address exponents outside the chosen chart.

## Exact replay

In addition to the 16-marker matched control, the last fixture has a 1,200-bit target for which each allowed single-axis move from (131,289) fails within the chosen j=1 lane: p=7 on its column and p=11 on its row. A simultaneous move to (51,145) has an explicit two-square certificate.

~~~python
from itertools import product
from math import isqrt, prod

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

def crt(rows):
    M = prod(rows)
    return sum(v*(M//m)*pow(M//m,-1,m) for m,v in rows.items()) % M, M

def lift_mark(p, shifts):
    s = shifts[0] % p
    assert all(v % p == s for v in shifts)
    return next(s+j*p for j in range(p)
                if all((s+j*p-v) % p**2 for v in shifts))

grid = list(product(range(51,301,16), (145,289)))
S = [3**c+5**d for c,d in grid]
marks = {139:(12,15),151:(27,),163:(14,21),199:(25,28),
         263:(7,24),271:(0,30),283:(6,11),331:(5,8),
         367:(9,20),547:(3,17,31),643:(2,19),827:(1,18),
         1399:(16,23),3851:(4,26),4003:(22,29),4079:(10,13)}
P = [p for p in range(7,138,4) if prime(p)]
M = 1728*17
W = M*prod(p**3 for p in P if p <= 75)
u,q0 = 2**1195+1109,2**1193
q = q0+(u*pow(5,-1,W)-q0)%W+413*W
good = S[0]+85*q
assert q%8 == 1 and pow(3,(q-1)//2,q) == q-1
assert good%8 == 5 and good%3 != 2 and good%17 == S[0]%17
assert all((good-S[0])%p for p in P)
Q = 25*M*prod(p**3 for p in P)

rows = {p**2:lift_mark(p,[S[i] for i in cells]) for p,cells in marks.items()}
bad,B = crt({Q:good%Q,**rows})
bad = good+(bad-good)%B
assert bad>good and (bad-good)%Q == 0
assert good.bit_length() == bad.bit_length() == 1200 and B.bit_length() == 577
assert sorted(i for cells in marks.values() for i in cells) == list(range(32))
for p,cells in marks.items():
    assert prime(p) and p%4 == 3 and any(pow(a,p-1,p*p)!=1 for a in (3,5))
    assert all(bad>S[i] and (bad-S[i])%p==0 and (bad-S[i])%p**2 for i in cells)

for p,want in ((23,11),(67,0)):
    assert all(pow(a,11,p)==1 and a!=1 for a in (pow(3,16,p),pow(5,144,p)))
    assert sum((pow(3,3+16*i,p)+pow(5,1+144*k,p))%p==0
               for i,k in product(range(11),repeat=2)) == want

lines = {7:[3**131+5**d for d in (145,289)],
         11:[3**c+5**289 for c in range(51,301,80)]}
xs,ys = {120:1},{120:40}
for p,line in lines.items():
    m = p*p
    target = (lift_mark(p,line)-S[0])*pow(85,-1,m)%m
    assert target%p
    x,y = next((x,y) for x,y in product(range(m),repeat=2)
               if (x*x+y*y-target)%m==0)
    xs[m],ys[m] = x,y
x,L = crt(xs)
y,_ = crt(ys)
u = 2**596
x,y = u+(x-u)%L,u+(y-u)%L
n = S[0]+85*(x*x+y*y)
assert n.bit_length()==1200 and n%8==5 and n%3!=2 and n%17==S[0]%17
assert (n-S[0])%25==10 and n-S[0]==(7*x-6*y)**2+(6*x+7*y)**2
assert [c for c in range(51,301,16)
        if (n-3**c-pow(5,145,25))%25==10] == list(range(51,301,80))
for p,line in lines.items():
    assert all(n>s and (n-s)%p==0 and (n-s)%p**2 for s in line)
~~~
