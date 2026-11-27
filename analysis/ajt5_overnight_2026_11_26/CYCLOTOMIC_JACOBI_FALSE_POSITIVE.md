# A Jacobi-symbol false positive for the extra cyclotomic factor

Keep the plus-sign chart of CYCLOTOMIC_EXTRA_FACTOR_OBSTRUCTIONS.md. For $U=5^{73^k}$, $A=5U-131770$, $x=365U^q$, and $r=x$ or $A/x$, write
$$
 F_q=x^2-4x+A=5(U-1)G_q(U),\quad
 G_q(U)=26645\frac{U^{2q}-1}{U-1}-292\frac{U^q-1}{U-1}+1.
$$
At the actual parameters $k=2$, $d=5330$, $q=197$, let $D=G_q(U)/3$. All three Jacobi symbols $(-1/D),(-A/D),(A/D)$ equal $+1$. Nevertheless $p=9199$ is an inert prime with $v_p(F_q)=1$ and $(-A/p)=-1$.

In particular both slopes are units at $p$, and $H=F_q/x$ vanishes modulo $p$. A parameter giving an integral $w$ must be $p$-adically integral, since otherwise its $r^2t^4$ term gives a pole in the numerator. Reducing that numerator modulo $p$ gives $(rt^2+r)(rt^2+A/r)$, so $t^2=-1$ or $t^2=-A/r^2$ would be necessary. Neither has a solution. The whole-product character data have therefore missed a real obstruction in the added factor. This is a counterexample to that proposed certificate, not an obstruction to all $q$ or all other denominator graphs.

```python
from math import isqrt
def jacobi(a,n):
    assert n>0 and n%2
    a %= n
    s=1
    while a:
        while a%2==0:
            a//=2
            if n%8 in (3,5):
                s=-s
        if a%4==n%4==3:
            s=-s
        a,n=n%a,a
    return s if n==1 else 0
U=5**5329
A=5*U-131770
q,p=197,9199
assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
G=26645*((U**(2*q)-1)//(U-1))-292*((U**q-1)//(U-1))+1
assert G%3==0 and (G//3)%2==1
D=G//3
assert [jacobi(c,D) for c in (-1,-A,A)]==[1,1,1]
x=365*pow(U,q,p*p)
assert U%p not in (0,1) and A%p!=0 and x%p!=0
assert (x*x-4*x+A)%(p*p)==4609*p
assert pow(-A,(p-1)//2,p)==p-1
```
