# An infinite genuine joint-label Pell orbit with a fixed split factor

The [fixed quadratic track](FIXED_SPLIT_FACTOR_SECOND_LABEL_THINNESS.md) has a true simultaneous point for \(K=10940,10928\) but density zero for the second target within that parameter. A different track gives infinitude unconditionally, with no prime-value input.

The target offsets differ by \(12=4^2-2^2\). At any positive integral solution of \(x^2-5p^2=10924\) one has
\[
 5p^2+10940=x^2+4^2,\qquad 5p^2+10928=x^2+2^2 .
\]
These are both child residuals at the same \(m=p^2+2188\), for \(x_{\rm child}=5m+2\) and the actual shifts \((e,f)=(0,0),(1,2)\) respectively. The parent residual at the original edge is \(p^2\). An exact seed is \((x,p)=(3577,1599)\) with \(p=41\cdot39\).

Put \(\epsilon=9+4\sqrt5\) and
\[
 x_n+p_n\sqrt5=(3577+1599\sqrt5)\epsilon^{387860n}.
\]
The unit has norm one and positive coefficients, and \(p_n\) strictly increases. Repeated squaring verifies \(\epsilon^{387860}\equiv1\bmod 4\cdot41^2\cdot43^2\) in both coefficients. Therefore every \(p_n\equiv3\bmod4\) has exactly one factor 41. For \(q_n=p_n/41\) we have \(q_n\equiv39\bmod43^2\); stripping the factor makes \(5q_n^2+10928\equiv43\bmod43^2\) fail at the inert prime 43, although the unstripped second label always succeeds.

The simultaneous orbit follows from a general sufficient recipe: if offsets \(K_i\) admit a common C with \(K_i-C\) all integer squares, then any positive integer anchor of \(x^2-5p^2=C\) gives a Pell orbit with every \(5p^2+K_i\) a genuine norm. Since a norm-one unit is invertible modulo any fixed modulus, some power is the identity there, so the orbit can preserve all anchor congruences. This requires an actual anchor; local norm survival alone does not furnish one. The present construction does not imply that q is prime or almost prime infinitely often, that the original quadratic track has infinitely many joint points, or that all integers admit a representation.

~~~python
x,p = 3577,1599
assert x*x-5*p*p == 10924 and p == 41*39 and p % 4 == 3
m = p*p+2188
assert m == 2558989
assert 5*m+2-(5**0+3**0) == x*x+4**2
assert 5*m+2-(5**1+3**2) == x*x+2**2
assert 9*9-5*4*4 == 1
assert (5*39*39+10928) % 43**2 == 43
M = 4*41**2*43**2
def mul(a,b):
    x,y = a
    u,v = b
    return ((x*u+5*y*v)%M, (x*v+y*u)%M)
a,b,N = (1,0),(9,4),387860
while N:
    if N & 1:
        a = mul(a,b)
    b = mul(b,b)
    N >>= 1
assert a == (1,0)
~~~
