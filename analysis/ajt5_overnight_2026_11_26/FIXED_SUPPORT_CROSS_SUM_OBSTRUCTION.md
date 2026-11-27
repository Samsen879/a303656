# Fixed-support rough-product obstruction below the cross sum

Let \(a,b\ge0,\ u,v\ge1\). Put \(A=3^a,\ B=5^b,\ X=3^{a+u},\ Z=5^{b+v}\). On the two labels \((a,b+v),(a+u,b)\) the residuals are \(R_1=n-A-Z\) and \(R_2=n-X-B\). Assume both are positive and \(n<X+Z\). For a fixed finite set of primes \(S\supset\{3,5\}\), write \(\rho_S(r)\) for the positive result of stripping all \(S\)-factors from \(r\). Then, for each \(0<\epsilon<1\),
\[
  \rho_S(R_1)\rho_S(R_2)\gg_{S,\epsilon} n^{1-\epsilon}.
\]
The constant is ineffective. This requires neither equal residual scales nor divisibility of \(X+Z-n\) by \(AB\).

Indeed the signed list \(X,B,R_2,-Z,-A,-R_1\) sums to zero. Choose an inclusion-minimal zero subsum containing \(X\); it cannot contain a proper nonempty zero subsum, by taking the complement inside it if necessary. Since \(X>A+R_1\), that block must contain \(-Z\); as \(X,Z>1\) are coprime, it also contains a third term. Drop any term except \(X,-Z\). The resulting list \(x_1,\ldots,x_t\) has at least two terms, none of its nonempty subsums vanishes, and their sum is the negative of the dropped term. Apply [Bugeaud–Evertse, Proposition 2.1](https://arxiv.org/pdf/1611.00485#page=5) over \(\mathbb Q\) with \(U=T=S\cup\{\infty\}\). The maximum norm at each finite place in \(T\) is 1 because \(X,Z\) are coprime integers, so \(H_T=\max_i |x_i|\ge\max(X,Z)>n/2\). The product formula turns the left side of the cited inequality into the product of the stripped parts of all terms in the minimal block, including the dropped term. Each pure power term contributes 1 and the remaining terms contribute at most \(\rho_S(R_1)\rho_S(R_2)\).

If both stripping steps use only primes from the fixed \(S\), a strong two-label product test with first four inert primes above \(Y\) has threshold \(O(Y^4)\) by the prime number theorem in fixed progressions. Thus any unbounded successful family of this form needs \(Y\ge n^{1/4-o(1)}\). More generally, at \(Y=n^{o(1)}\) in an unbounded successful family, the product of stripped factors supported **outside any fixed \(S\)** has logarithmic lower exponent at least 1. This leaves open growing supports and does not rule out a different true-norm method.

## Exact negative-offset controls with a third smooth base

In these controls \(n=X+Z-jAB\), \(j>0\). The reduced residuals satisfy
\[
R_1/A=3^u-1-jB,\qquad R_2/B=5^v-1-jA.
\]
Strip primes at most \(Y\) from the actual residuals. The following two independent controls reverse which side survives; adding the base 2 to the usual \(3,5\) factors is effective in both.

| \(Y\) | \(n\) | labels | \(j\) | \(R_1,R_2\) | rough parts |
|:---:|---:|---|---:|---|---|
| 11 | 31708 | \((2,6),(9,1)\) | 80 | \(16074,12020\) | \(893,601\) |
| 7 | 72694 | \((2,6),(10,1)\) | 44 | \(57060,13640\) | \(317,341\) |

In each row both rough parts are \(1\bmod4\), coprime, at least the one-label threshold and below the strict two-label threshold in product. The stripped inert valuations are even. In row one \(893=19\cdot47\) fails, while \(12020=28^2+106^2\) passes. In row two \(341=11\cdot31\) fails, while \(57060=48^2+234^2\) passes. There is no label giving a zero residual at either target.

```python
from math import gcd,isqrt,prod
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
def rough(r,Y):
    for p in range(2,Y+1):
        if not prime(p):
            continue
        e=0
        while r%p==0:
            r//=p
            e+=1
        assert p%4!=3 or e%2==0
    return r
for Y,n,u,j,values,expected in [
    (11,31708,7,80,(16074,12020),(893,601)),
    (7,72694,8,44,(57060,13640),(317,341)),
]:
    X,Z=3**(2+u),5**6
    assert n==X+Z-j*9*5
    r=(n-9-Z,n-X-5)
    assert r==values
    w=tuple(rough(x,Y) for x in r)
    assert w==expected and gcd(*w)==1 and all(x%4==1 for x in w)
    q=[p for p in range(Y+1,50) if p%4==3 and prime(p)][:4]
    assert min(w)>=q[0]*q[1] and prod(w)<prod(q)
    assert all(3**c+5**d!=n for c in range(1+n.bit_length())
               for d in range(1+n.bit_length()))
assert 12020==28**2+106**2 and 57060==48**2+234**2
assert 16074==18*19*47 and 13640==40*11*31
```
