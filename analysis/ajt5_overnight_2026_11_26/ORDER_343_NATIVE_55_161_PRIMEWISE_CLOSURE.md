# A strict factor extraction closes the native (55,161) source

The previous [order-343 aggregate](https://github.com/Samsen879/a303656/commit/56de060c946b019063e56638162e44721a489c35) proved that at least one prime of this native evaluation norm failed; it did not locate any prime. A separate, simple factor discovery now gives a strict block. Starting solely from the exact non-7 norm N and base 3, compute gcd(3^lcm(1,…,B)−1,N). The result is 1 at B=2^15,2^16,2^17,2^18 and 878168614051 at B=2^19. Those are verified separate probes, not a proof about every intermediate bound; B=2^19 was fixed retrospectively.

| Prime factor of N | p mod 1372 | Actual Euler log pair mod 343 | Individual rejection |
|---:|---:|---|---|
| 878168614051 | 687 | (45,4) | (p−1)/343≡20 mod 343, and menu E≡27 mod 49 requires first-axis log 1 mod 49, not 45 |
| 47794969965658312997552418718599515765101 | 1 | (298,241) | Sign gate requires 687 mod 1372 |

Full Lucas certificate chains below certify both primes and their product N. Their actual logs sum to (0,245) modulo 343. Why order 49 was aggregate-blind: relative to the same native allowed menu, the two deviations reduce to (44,33) and (5,16), which add to zero modulo 49. The new outcome is a genuinely primewise closure of this one native chart source. The aggregate alone did not provide the factor or imply full closure. No wider cohort claim follows.

## Standalone factor and primewise replay

The norm/root/menu are independently verified in the previous note; this replay takes N and the native root, not unknown factors or prime-group orders, as inputs to discovery.

~~~python
from math import gcd, isqrt, prod
N = 41972042533351331790887366901335366135158470044034151
x = 30015482896187807087217920276249313249092836022188472
# 从 N 和底数 3 提取严格支持。
bound = 2**19
S = bytearray(b'\1')*(bound+1)
S[:2] = b'\0\0'
for i in range(2,isqrt(bound)+1):
    if S[i]:
        S[i*i::i] = b'\0'*((bound-i*i)//i+1)
a = 3
for i in range(2,bound+1):
    if S[i]:
        z = i
        while z*i<=bound:
            z *= i
        a = pow(a,z,N)
p = gcd(a-1,N)
q = N//p
assert a==26483856054303227615035846006135852711782359055485269
assert (p,q)==(878168614051,47794969965658312997552418718599515765101)
assert p*q==N

C = {
    p:(3,[2,3,3,5,5,7,7,7,13,437651]),
    437651:(2,[2,5,5,8753]),
    q:(2,[2,2,3,5,5,7,7,7,27196151,107536499635769,158819373520201]),
    27196151:(11,[2,5,5,73,7451]),
    107536499635769:(3,[2,2,2,7,2777,691499689]),
    691499689:(14,[2,2,2,3,11,719,3643]),
    158819373520201:(34,[2,2,2,3,3,5,5,19,49481,93851]),
    49481:(3,[2,2,2,5,1237]),
    93851:(2,[2,5,5,1877]),
}
def prime(v):
    if v<10000:
        assert v>1 and all(v%i for i in range(2,isqrt(v)+1))
        return
    a,F = C[v]
    assert prod(F)==v-1 and pow(a,v-1,v)==1
    for f in set(F):
        prime(f)
        assert gcd(pow(a,(v-1)//f,v)-1,v)==1

for v,y,J in ((p,447693287590,(45,4)),
              (q,42431982734739276385644460573777094182747,(298,241))):
    prime(v)
    assert x%v==y and v%343==1
    assert all(pow(u,(v-1)//343,v)==pow(y,j,v) for u,j in zip((3,5),J))
assert (p%1372,q%1372)==(687,1)
assert ((p-1)//343)%343==20 and 45%49!=20*27%49
assert ((45+298)%343,(4+241)%343)==(0,245)
print("aggregate", (0,245), "primewise rejection", p, q)
~~~
