# A low-complexity obstruction for the true common-target quadratic progression

In the actual second progression n=J+2(t²+c²), write the first endpoints as S=2(t²+U), R=2(t²+V), where c=(E−1)/2, U=c²+60B−12A and V=U+D. Direct bounds using the actual 3,5 powers give (c+1)²<U<V<(c+2)². Thus t²+U and t²+V are distinct irreducibles in Q(i)[t] fixed by conjugation. Each has odd valuation in SR=4(t²+U)(t²+V) but any norm Z conjugate(Z) has even valuation there. There is no rational Gaussian norm formula in the original t. A rational substitution of odd degree cannot fix this: applying the relative field norm would make SR to an odd power a norm, which can be divided by the norm of the corresponding real half-power to make SR itself a norm.

For fixed maximal degree, a candidate Gaussian rational F(t)/G(t) has at least one of the coefficient scales h(F), B² h(G) comparable to B^4 if it matches at an actual |t|≥B^8. Indeed the difference F conjugate(F)−SR G conjugate(G) is a nonzero integral polynomial of coefficient height O(h(F)²+B^4 h(G)²); the root bound applied to such an actual t implies the claimed scale. The finite K671 procedure was allowed to use large coefficients and recovered factors after choosing the target, so the obstruction does not contradict that genuine witness.

## Quadratic substitution and its exact cost

After a quadratic polynomial substitution, the two relatively prime endpoint polynomials must separately be Gaussian norms if their product is. Rational unit rotations normalize the leading real parts to t−k1,t−k2 after dividing out the common norm 2; the imaginary terms are linear. The cubic coefficient first forces the real offsets to be constant. Comparing the two imaginary squares then gives the same axis of symmetry and a rational slope ratio λ, with
```
k2=λ² k1,   V−λ² U=λ²(λ²−1) k1².
```
We can take λ positive by reversing one imaginary sign. Since V>U, the identity forces 1<λ²<V/U, so the reduced denominator of λ exceeds 2U/D, of order B. Conversely a rational Y with Y²=(λ²−1)(V−Uλ²) gives k1=Y/[λ(λ²−1)] and t=(z²+k1²−U)/(2k1). This constructs the polynomial norms but does not guarantee integer endpoints, CRT constraints, or actual angles.

If the two normalized leading directions lie in a fixed finite set, an actual critical chord at ordinary scale also requires |k_i| of order at least |t|/K² for one endpoint. In each endpoint the unit direction is within O(sqrt(|k_i/t|+B²/t²)) of its leading direction. Equal leading directions need this discrepancy to create a gap of order 1/K; unequal fixed directions require it to shrink their fixed positive separation. Combining with k2=λ²k1 and the previous identity forces denominator ≫ t²/(D K^4), hence ≫B^15/K^4 on the stated ordinary scale. This excludes a bounded-denominator use of this specific degree-two scheme, not all integer constructions.

The replay retains the previously verified true K671 common target and its sibling all-direction inert negative. No new growth of true double targets is claimed from this obstruction.

```python
from math import gcd, lcm

K = 671
A,B = 9**7,25**7
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
U,V = c*c+60*B-12*A,c*c+62*B-3*A
assert (c+1)**2 < U < V < (c+2)**2
assert 2*U//D == 3801411590945

t = 79186934766042045095929803573073104476777060604159795000641641588139114268924441178860030070538531575
P = (44431203582073559282494574809832918293984662102542474582518318621124282161821021916287391661118156350,
    -102795960151803292317648126601409819709413677981069550595950114807445277622604722731580554168269201516)
Q = (44404131936308723490377453276856351802501036674815895158077617651899081800748832297785227943339691253,
    -102807657021574440378638433005380974661597798592021324296397639839177576805982968758041358322577020383)
ms = (7592,7594,7596)

def norm(P):
    return sum(x*x for x in P)

def check(n,P,Q,H,D):
    S = n-H
    assert 25**128 <= n <= 9**224 and 2**K <= S < 2**(K+1)
    assert norm(P)==S and norm(Q)==S+2*D
    x,y = Q[0]-P[0],Q[1]-P[1]
    q,h = (x*x+y*y)//2,x*P[1]-y*P[0]
    assert x%2 and y%2 and gcd(x,y)==1 and h%2==0
    assert 2*q*S==(D-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
    return q

def second(t):
    n = 2*(t*t+c*c)+J
    qs = set()
    for m in ms:
        v,rem = divmod(t+m*(c+1),m*m+1)
        assert rem==0
        f,g = (m*m-1)*v-m*(c+1),2*m*v-c-1
        qs.add(check(n,(t-c,t+c),(f-g,f+g),J,E))
    assert len(qs)==3
    return n

n = second(t)
S = n-H
q = check(n,P,Q,H,D)
assert gcd(S,D)==gcd(q,D)==1
Z = (P[0]*Q[0]+P[1]*Q[1],P[0]*Q[1]-P[1]*Q[0])
assert norm(Z)==4*(t*t+U)*(t*t+V) and q==S+D-Z[0]
assert min(abs(Q[j]-P[j]) for j in (0,1)).bit_length()==323
bad = second(t+4*lcm(*(m*m+1 for m in ms)))
assert (bad-H)%49==21
```
