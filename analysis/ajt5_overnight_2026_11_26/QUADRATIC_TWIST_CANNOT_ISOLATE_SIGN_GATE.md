# A whole quadratic twist does not isolate an inert sign side

In the neutral chart let K=Q(ζ_343), L=K(i), and let I be the native ideal of x over the unfactored source. The order-7 logarithm on the full extended ideal obeys λ_(I O_L)(γ)=λ_I(N_(L/K)γ) for any unit at the support. At a split prime the two local symbol logs add and correspond to the product. At an inert prime the identity γ^((p²−1)/7)=(γ^(p+1))^((p−1)/7) yields exactly the same norm formula. Multiplicities follow by additivity. Thus a base-field value D doubles its original whole log on full extension, and a norm-one twist gives zero; this cannot isolate the sign-gate side. In particular the verified (17,188) whole-source discrepancy 6 only becomes 5 mod 7, not an identified inert contradiction.

If one could instead retain one lift of each split prime while retaining the inert quadratic lift, subtracting the original log would give the desired inert-side sum on base-field inputs. But the ideal norm divided by the original norm would then already equal the product of the inert prime powers. When both sides occur this selects a nontrivial integer factor, not a free consequence of a whole quadratic twist.

The exact native (31,295) control has a split factor whose norm-one twist reads 2 and 5 on its two lifts, summing to zero, while its sign-gate factor reads zero. The two sign-gate factors of (40,86) have nonzero original discrepancies, yet their norm-one twists both read zero. This note does not assert a universal impossibility for all factor-sensitive functions, or close (17,188).

```python
from math import gcd, isqrt, prod

def gp(z, n, p):
    def mul(u, v):
        a,b = u
        c,d = v
        return ((a*c-b*d)%p,(a*d+b*c)%p)
    w = (1,0)
    while n:
        if n%2:
            w = mul(w,z)
        z = mul(z,z)
        n //= 2
    assert w[1] == 0
    return w[0]

for x,u,v,d,rows in [
    (68693850624006015651041237082,31,295,1,[
        (421761845597,[23646661],1,3,(3,3),(2,5)),
        (402997726421332771,[5987,16232033],687,0,(0,),(0,))]),
    (13129993496012691450693331,40,86,5,[
        (45574318763,[66434867],687,6,(5,),(0,)),
        (337621934255663,[55529759],687,3,(6,),(0,))])]:
    Q = prod(row[0] for row in rows)
    assert pow(x,343,Q)==1 and gcd(pow(x,49,Q)-1,Q)==1
    assert (1-x+pow(x,u,Q)-pow(x,v,Q))%Q==0
    for p,fs,gate,A,base,twist in rows:
        F = prod(fs)
        assert p%1372==gate and F*F>p and (p-1)%F==0 and pow(2,p-1,p)==1
        for f in fs:
            assert all(f%j for j in range(2,isqrt(f)+1))
            assert gcd(pow(2,(p-1)//f,p)-1,p)==1
        y,h = pow(x,49,p),(p-1)//7
        D = 3*pow(5,-1,p)*pow(x,-d,p)%p
        assert pow(D,h,p)==pow(y,A,p)
        def lift(a,b):
            if gate==687:
                return (gp((a%p,b%p),(p*p-1)//7,p),)
            i = pow(2,(p-1)//4,p)
            assert i*i%p==p-1
            return tuple(pow((a+t*i*b)%p,h,p) for t in (1,-1))
        n = pow(D*D+1,-1,p)
        assert lift(D,0)==tuple(pow(y,k,p) for k in base)
        assert lift((D*D-1)*n,2*D*n)==tuple(pow(y,k,p) for k in twist)
```
