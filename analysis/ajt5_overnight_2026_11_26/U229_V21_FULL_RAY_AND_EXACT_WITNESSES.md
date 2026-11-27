# A new exact double-half ray at (229,21)

Both actual odd halves H=(5^229−3^21)/2 and J=(5^229+3^21)/8 have full integer Eisenstein norm coordinates. The replay checks scalar modular roots and uses Euclidean descent, with exact coordinate equality as the final test. This gives a genuinely new checked base ray at phase 458/9 in the previously tracked gap.

Write A=5^229, S=3^21. Multiplying the two half-norm coordinates, scaling coordinates by 8, and multiplying by the Eisenstein unit (1+sqrt(−3))/2 gives x²+3W²=4(A²−S²). Exact integer checks give |W|>A/100, 3 not dividing W, and A>1000 S. From a layer (A,S) to its cube, multiply the element by A² + S²(1+sqrt(−3))/2 of norm A^4+A²S²+S^4. This transports the identity exactly; the coefficients remain divisible by 4 because the original element is 8 times a full Eisenstein integer and that ring has only half-integer coordinates in the 1,sqrt(−3) basis. Modulo 3 the W coefficient stays a unit through the lift. The total angular displacement is at most ∑_(j≥0)(S/A)^(2·3^j)<2(S/A)². Since the initial normalized absolute imaginary component exceeds sqrt(3)/200, every later layer has |W|>A_layer/200>3 S_layer.

For each actual layer put Q=A_layer², s=S_layer and take W positive. For L=1 or 3 define
```
n=Q+(4−L)s²+x²+(W+s)²
 =5Q−2W(W−s)+(1−L)s².
```
The first form is a true representation of the requested shape with exponents (2*21*3^k+1,2*229*3^k) for L=1 and (2*21*3^k,2*229*3^k) for L=3. The two forms give Q<n<5Q. Since W is divisible by 4 and not by 3, the respective classes are 21 and 3 modulo 24. The exact replay verifies both first-layer exponents (127,1374),(126,1374), and also the next layer. This is an explicit growth ray, not arbitrary n. This note makes no assertion about the global indexed catalogue size, the updated coverage exponent, or improved natural density.

```python
from math import gcd, isqrt, lcm

A, S = 5**229, 3**21
H, J = (A-S)//2, (A+S)//8
p = 3692254399036927
assert 2*H == A-S > 0 and 8*J == A+S
assert H%p == J%199 == 0 and gcd(p,H//p) == 1

coords=[]
for N, b, E in [(H,13,lcm(p-1,H//p-1)), (J,12,lcm(198,J//199-1))]:
    while E%3 == 0:
        E //= 3
    z = pow(b,E,N)
    assert (z*z+z+1)%N == 0
    r = (2*z+1)%N
    a,x = N,min(r,N-r)
    while x*x > N:
        a,x = x,a%x
    y = isqrt((N-x*x)//3)
    assert x*x+3*y*y == N
    coords.append((x,y))

def mul(z,w):
    a,b=z
    c,d=w
    return a*c-3*b*d,a*d+b*c
def half(z):
    assert not any(v%2 for v in z)
    return tuple(v//2 for v in z)

z=tuple(8*v for v in mul(*coords))
z=half(mul(z,(1,1)))
assert 100*abs(z[1])>A and z[1]%3 and A>1000*S
for k in range(1,3):
    z=half(mul(z,(2*A*A+S*S,S*S)))
    A,S=A**3,S**3
    Q=A*A
    x,W=z[0],abs(z[1])
    assert W%4==0 and W%3 and W>3*S and x*x+3*W*W==4*(Q-S*S)
    for L,remainder in ((1,21),(3,3)):
        U,V=229*3**k,21*3**k
        c,d=2*V+(L==1),2*U
        n=Q+(4-L)*S*S+x*x+(W+S)**2
        assert n == 3**c+5**d+x*x+(W+S)**2 and Q<n<5*Q and n%24==remainder
print("PASS")
```
