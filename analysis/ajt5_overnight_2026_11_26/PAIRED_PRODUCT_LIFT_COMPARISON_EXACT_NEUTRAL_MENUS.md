# Paired-product residue comparison without individual short-order witnesses

Let \(S_T(a)\) be the saturated support in \(R\) supplied by \(\prod_{1\le m\le T,\ 7\nmid m}(a^m-1)\). A prime \(p\mid R\) belongs to the support exactly when \(\operatorname{ord}_p(a)\) is prime to 7 and at most \(T\). This follows by taking the first available multiple of the order, which is its order itself. Work in the fixed neutral chart, with its root \(x\) of order 343 at every prime, \(L\) prime to 7, and \(H\) a power of 7 large enough to kill the 7-part of every pertinent unit order.

For each word \(W=3^u5^v\) and proposed lift \((E,k)\), compare \(S_T(W^{LH})\) with \(S_T(W^Lx^{-LE(u+vk)})\). The arguments have the same prime-to-7 order at each prime, since raising to \(H\) permutes the prime-to-7 component and the twist changes only the 7-component. Consequently the second support is exactly the subset of the first where the 7-primary phase equality holds. This gives the inputs to [the per-prime gcd/lcm rejection](https://github.com/Samsen879/a303656/commit/802470b8e420403ca6fd9d75c72968f74d8d7a7a) without needing the individual short orders. This scoring comparison does not remove the size cutoff.

## Independently regenerated neutral rows

The replay covers two pinned norms and independently regenerates both native roots and all 14 lifts across their fixed tag menus. All Euclidean divisions modulo the composite have verified unit pivots; the linear gcd therefore resolves the root modulo every prime of the coefficient ring. The frozen three-band chart enumerator then gives exactly the seven \((E,66)\) with \(E=15\bmod49\) for the first row and the seven \((E,59)\) with \(E=30\bmod49\) for the second. Modular power checks reject every permitted lift, including on the unfactored first-row composite part. These two exact row certificates are within the specified chart and do not assert broader cohort totals.

## Exact cutoff and filter control

On the prime complement \(C=83464673905159\), the projected base 3 and 5 have order \(m=42193\cdot73939\). In the two prime-order projections the second-axis logs are 9067 and 49366; the smallest centered residues of \(-v\) times the respective logs for \(1\le v\le120\) are 270 and 220. Thus any nonzero word with \(\max(|u|,|v|)\le120\) has full residual order \(m\), whereas the actual word \((-89,121)\) has residual order 73939. This is a boundary for this word box, not an all-word obstruction.

The same complement gives a direct negative control for omitting the restriction \(7\nmid m\) in the product: the single-axis 7-primary exponent is 190. The false shift 239 is congruent to it modulo 49, but its twisted order is \(7m\). An unfiltered product with \(T=7m\) would accept this wrong fine lift. The filtered support rejects it. This last control isolates one axis and does not assert that 190 or 239 is a permitted joint chart lift.

```python
from functools import cache
from math import gcd, lcm, prod

R = 7320452716949759354345164426511787518233
D = 87707198440240691069086687
C = R // D
R0 = 8703205831390420819770510177452311233617

def free7(n):
    while n % 7 == 0:
        n //= 7
    return n

L = free7(lcm(*range(1, 20001)))
cases = [(R,12,51,[(D,L*35882695707051169),(C,free7(C-1))]),
         (R0,93,47,[(R0,L*1939502147593)])]

def root(n,a,b):
    f = [int(i%49 == 0) for i in range(295)]
    g = [0]*(max(a,b)+1)
    g[0] = g[a] = 1
    g[1] = g[b] = -1
    while g:
        while g and g[-1]%n == 0:
            g.pop()
        if not g:
            break
        inv = pow(g[-1],-1,n)
        g = [z*inv%n for z in g]
        d = len(g)-1
        for j in range(len(f)-1,d-1,-1):
            for i in range(d):
                f[j-d+i] = (f[j-d+i]-f[j]*g[i])%n
        f,g = g,f[:d]
    assert len(f) == 2 and f[1] == 1
    return -f[0]%n

@cache
def canonical(a,b):
    P,Q = (0,a),(1,b)
    return min(((p[1-i]-p[i])*s%343,(q[1-j]-p[i])*s%343,d)
               for p,q in ((P,Q),(Q,P))
               for i in (0,1) for j in (0,1)
               if (d := (q[j]-p[i])%343)%7
               for s in (pow(d,-1,343),))

menus = {(a,b):set() for _,a,b,_ in cases}
bands = [(17,{33,12,47},{39,11,46}), (24,{40,5,26},{46,4,25}),
         (38,{5,40,33},{11,39,32})]
for a in range(36,343,49):
    h = a+343*((-a)%6)
    g,f = pow(3,h,2401),pow(5,h,2401)
    inv = {pow(f,v,2401):v for v in range(343)}
    for start,left,right in bands:
        for u in range(start,343,49):
            delta = pow(g,u,2401)-pow(g,u+1,2401)
            for v in range((1-u)%7,343,7):
                if v%49 in left:
                    continue
                w = inv[(pow(f,v,2401)+delta)%2401]
                if w%49 in right:
                    continue
                for k in range(1,343):
                    if k%7:
                        b,c,d = canonical((k*v-u)%343,(k*w-u)%343)
                        if (b,c) in menus:
                            menus[b,c].add((pow(a*d,-1,343),k))

assert menus[12,51] == {(E,66) for E in range(15,343,49)}
assert menus[93,47] == {(E,59) for E in range(30,343,49)}
for n,a,b,parts in cases:
    x,H = root(n,a,b),7**n.bit_length()
    assert pow(x,343,n) == 1 and gcd(n,pow(x,49,n)-1) == 1
    assert prod(d for d,M in parts) == n
    for d,M in parts:
        U,V = (pow(w,M,d) for w in (3,5))
        assert M%7 and pow(U,H,d) == pow(V,H,d) == 1
        for E,k in menus[a,b]:
            assert gcd(d,U-pow(x,M*E%343,d),V-pow(x,M*k*E%343,d)) == 1

# Sharp short-word boundary and the wrong fine-lift control on C.
from math import isqrt
def prime(n):
    return n>1 and n%2 and all(n%d for d in range(3,isqrt(n)+1,2))
assert all(map(prime,(C,42193,73939)))
H=1
while 7*H<=R//4_000_000_000:
    H*=7
x=root(R,12,51)
m=42193*73939
A,B=(pow(w,L*H,C) for w in (3,5))
assert pow(A,m,C)==pow(B,m,C)==1
for p,e,j,lo in [(42193,73939,9067,270),(73939,42193,49366,220)]:
    a,b=pow(A,e,C),pow(B,e,C)
    assert a!=1 and pow(a,p,C)==1 and pow(a,j,C)==b
    assert min(min(v*j%p,-v*j%p) for v in range(1,121))==lo
    assert ((-89+121*j)%p==0)==(p==42193)
assert pow(3,L*m,C)==pow(x,L*m*190%343,C)
B=pow(3,L,C)*pow(x,(-L*239)%343,C)%C
assert pow(B,7*m,C)==1
assert all(pow(B,7*m//p,C)!=1 for p in (7,42193,73939))
```
