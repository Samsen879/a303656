# Independently checked selected outcomes of three native research turns

Only the results below were independently replayed here. The much larger native packages and prospective density claims are not included.

## A. A finite-window completeness lemma for an existing true double row

For actual A=9^r≤B=25^s with B^16≤n≤A^32 and n>1, set S=n−3A−5B, D=A+2B, R=S+2D, k=floor(log_2 S). A permitted number q is a positive odd Gaussian norm with 2qS=(D−q)²+4w². Window j requires 32768k³ q≤j³ S≤32768k²(k+1)q.

The relation proves both S and R are norms: replacing D−q by D+q gives 2qR, and the inert-prime valuations of 2q are all even. Conversely if S,R are norms, their residues mod 8 force n=2 or 4 mod 8, so their even halves are also Gaussian norms; choose z,z' with those half-norms. Write z' conjugate(z)=a+bi, m=S+D odd. Then a²+b²=(m²−D²)/4, and |a|,|b|≤(m−1)/2, so each component has magnitude >D/2 because S>(D−1)² under the height restriction. A Gaussian unit makes the dot product min(|a|,|b|). It yields q=norm(z'−z)=m−2 min(|a|,|b|), odd and positive, satisfying (1−1/sqrt(2))S≤q<S and the seed equation. The j=20k,…,32k ranges for S/q are contiguous and contain [1,2+sqrt(2)]: adjacent endpoints overlap since ((j+1)/j)^3≤1+1/k in that range. Therefore j≤32k captures every already true double row, not necessarily any row for a designated n.

The exact example n=37778932400068593789036 has only label A=9,B=25 and k=75. Let z=137438954449. The two individually true half-norms are z²+29² and z²+30². Pocklington verifies the split primes (z²+841)/2 and z²+900. Their product times 8 equals RS, whose 16 ordered signed coordinates are the sign/unit permutations of (2(z²+870),2z) and (2(z²−870),118z). The eight candidates q=S+D−x consequently give no window up to 2399 and one at 2400=32k. This is a finite exact sharpness control, not asymptotic optimality after exceptions.

```python
from math import gcd
n=37778932400068593789036
z=137438954449
S,D=n-27-125,59
R=S+2*D
k=S.bit_length()-1
assert k==75 and S==2*(z*z+841) and R==2*(z*z+900)
p0,p1,p,q0,q=(2863311551,22487459761945591541,9444733100017148447221,
              778188815077,18889466200034296894501)
from math import isqrt,prod
for v,a,fs in [(p0,7,[65899]),(p1,2,[2,2,5,p0]),(p,2,[p1]),(q0,5,[2,2,3,413233]),(q,2,[q0])]:
    F=prod(fs)
    assert (v-1)%F==0 and F*F>v and pow(a,v-1,v)==1
    for t in set(fs):
        if t<414000: assert all(t%d for d in range(2,isqrt(t)+1))
        assert gcd(pow(a,(v-1)//t,v)-1,v)==1
assert p==(z*z+841)//2 and q==z*z+900 and p%4==q%4==1 and R*S==8*p*q
a,b,c,d=2*(z*z+870),2*z,2*(z*z-870),118*z
assert a*a+b*b==c*c+d*d==R*S
xs={a,-a,b,-b,c,-c,d,-d}
assert len(xs)==8
def win(q,j):
    return 32768*k**3*q<=j**3*S<=32768*k*k*(k+1)*q
assert not any(win(S+D-x,j) for x in xs for j in range(1,2400))
q=37778932383850797163961
w=18889466200034296892731
assert win(q,2400) and q==137438954420**2+137438954419**2
assert 2*q*S==(D-q)**2+4*w*w
assert 25**16<=n<=9**32 and 81**16>n and 625**16>n
```

## B. A common-row norm requires information beyond true products

If positive integers QA_i are all two-square norms, let G=gcd_i A_i. Then Q is a two-square norm iff G is: for every inert prime, the A_i valuations have the same parity as Q, and taking the minimum preserves that parity. In particular this does not license recovering a common single row just from the existence of product coordinates and an integer Gaussian quotient. At actual n=34 the rows 30,24,6 give three pairwise true products while 24 has v_3=1.

Factor refinement of positive actual rows by replacing two overlapping factors with their gcd and exact cofactors yields a pairwise-coprime base. It terminates by decreasing the product of distinct factors. Multiplication, gcd and exact division are then exponent addition, minimum and nonnegative subtraction, so the base describes their entire generated multiplicative language. The replay verifies a hidden nonnorm row n−2 in two complete actual positive domains: it shares no prime with any other positive row and is 1 mod 8, yet has two inert prime factors.

```python
"""Run with python3; standard library only, checks also survive -O."""
from math import gcd

def ok(b):
    if not b: raise ArithmeticError("certificate failed")

def powers(b, n):
    a, x = [], 1
    while x < n:
        a.append(x); x *= b
    return a

for n, p, q, x, y, count in (
    (21355, 163, 131, 81, 86, 67),
    (106531, 307, 347, 27, 230, 87),
):
    r = n-2
    rows = {(c,d): n-a-b for c,a in enumerate(powers(3,n))
            for d,b in enumerate(powers(5,n)) if a+b <= n}
    ok(r == p*q == x*x+2*y*y and gcd(p,q) == 1)
    ok(p % 72 == 19 and q % 72 == 59 and r % 8 == 1)
    ok(len(rows) == count and min(rows.values()) > 0)
    ok(all(gcd(r,v) == 1 for k,v in rows.items() if k != (0,0)))
    ok(all(v % 9 in (3,6) for (c,d),v in rows.items() if d == 0 and c > 0))
    print(n, "complete positive rows", count, "PASS")

n, r = 21355, 21353
a, b = n-1-5, n-9-5
ok(a == 145**2+18**2 and b == 146**2+5**2)
ok(a*b == 21080**2+3353**2)
ok((r*a)*(r*b) == (r*21080)**2+(r*3353)**2)
ok(gcd(r,145**2-18**2) == 163 and gcd(r,146**2-5**2) == 1)
# True local products do not imply the common SINGLE row is a norm.
n, A, Q, B = 34, 30, 24, 6
ok((A,Q,B) == (n-3-1,n-9-1,n-27-1))
ok(A*Q == 24**2+12**2 and B*Q == 12**2 and A*B == 12**2+6**2)
ok(144 % Q == 0 and Q % 9 == 6 and gcd(A,B) == 6)
ok(n-1-1 == 4**2+4**2 and Q == 4**2+2*2**2)
print("same-n true products / negative common row / N2 / projection controls: PASS")
```

## C. Fixed-size bilinear coordinate charts cannot grow full positive-root rectangles

With fixed positive opposite-axis root input, a bilinear common-denominator chart takes the form ((at+b)/(et+f),(ct+d)/(et+f)). For target norm H−t² and nonzero e, four supported distinct positive roots would make the cross-multiplied polynomial e² times their four linear factors. Its cubic coefficient puts the denominator pole at half the sum of the roots. Positivity of the numerator norm at that pole forces the largest root to be less than the sum of the other three (equality gives zero denominator). Four same-parity exponent root inputs have consecutive ratios ≥2, impossible. For nonsquare base, mixed parity gives three rational and one quadratic irrational input (up to a common scaling), or two of each. The former has irrational cross ratio; in the latter the cross ratio can be ordered as (P−Q√D)/(P−R√D), with P>0 and Q−R a nonzero product of differences, hence irrational. A nonconstant coordinate function is Möbius and preserves cross ratio, so it cannot output four rational coordinates from these inputs. Constant denominator already gives degree at most two. The proof also works with any positive-definite binary quadratic form in the numerator. Thus each chart supports at most three positive-root entries per line and K such charts need max(side lengths)≤3K. This constrains the indicated formula interface, not the existence of larger true rectangles.

The exact controls replay the real 4×4, a true 2×3 using one chart, and an actual growing square menu with all positive active residues but one permanently inert-bad cell, even though six other cells have exact coordinates. No unrestricted growing full 3,5 rectangle is claimed.

```python
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt

def need(ok):
    if not ok:
        raise ValueError("failed exact evidence")

def true(n, c, d, x, y, Q=1):
    need(n - 3**c - 5**d == x*x + Q*y*y > 0)

# 原同一n真4×4。
n = 24396
C, D = [0,2,6,8], [0,2,4,6]
xy = [
    (75,137),(31,153),(19,153),(11,93),
    (19,155),(71,139),(31,151),(29,89),
    (95,121),(29,151),(29,149),(11,89),
    (47,125),(11,133),(7,131),(1,47)
]
for (c,d),(x,y) in zip(product(C,D), xy):
    true(n,c,d,x,y)
need(gcd(*(n-3**c-5**d for c,d in product(C,D))) == 2)

# 新匹配边为真，缺少的交叉格却有精确v3=1。
true(n,1,5,62,132)
need((n-1-5**5) % 9 == 3)

# 单张根双一次图的实际真2×3。
for c,d in product([0,2], [0,4,6]):
    U,V = 3**(c//2), 5**(d//2)
    T = 145-V
    x,y = F((4-U)*T,T), F(22775-167*V,T)
    need(x.denominator == y.denominator == 1)
    true(24660,c,d,x,y)
need(F(22775-167*139,145-139) == -73)
need(5**6 < 139**2 < 5**7)

# 两方向真条带不保证交叉闭包。
W = [(3,32),(3,30),(3,20),(1,32),(1,30),(1,20),
     (13,28),(10,27)]
cells = list(product([0,2,4],[0,3,4]))
for (c,d),(x,y) in zip(cells[:8],W):
    true(1035,c,d,x,y)
need(1035-3**4-5**4 == 329 and 329 % 49 == 35)

# 两轴增长、全部严格活跃、六真格与一个确定假格。
for L in (4,7,10):
    n = 3**(6*L)+3**(8*L)+24650*5**(2*L)
    C = list(range(6*L,8*L+1,2))
    D = list(range(2*L,4*L+1,2))
    need(len(C) == len(D) == L+1)
    need(isqrt(n) < 3**min(C)+5**min(D))
    need(n > 3**max(C)+5**max(D))
    for c,x in [(6*L,3**(4*L)),(8*L,3**(3*L))]:
        for d,y in zip([2*L,2*L+4,2*L+6],[157,155,95]):
            true(n,c,d,x,y*5**L)
    need((n-3**(6*L+4)-5**(2*L)) % 49 == 35)
    need(all((n-3**c-5**d)%8 == 2
             and (n-3**c-5**d)%3 == 1
             for c,d in product(C,D)))

# 有限面板完整可过，但实际11奇赋值。
n = 2385696297800403
E = [18,20,22]
true(n,18,18,48804505,38792)
need(all((n-3**c-5**d)%8 == 1
         and all((n-3**c-5**d)%p for p in (3,7))
         for c,d in product(E,E)))
need((n-3**20-5**18) % 121 == 11)

# 另一正定范数的同点正/反控。
for (c,d),(x,y) in zip(product([2,4],[2,4]),
                       [(9,20),(9,10),(3,20),(3,10)]):
    true(915,c,d,x,y,2)
need(915-3**4-5**4 == 209 and 209 % 121 == 88)

print("PASS")
```
