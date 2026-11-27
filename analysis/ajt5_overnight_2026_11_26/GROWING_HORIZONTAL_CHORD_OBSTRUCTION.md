# A growing family excludes shared horizontal-unit chords, not arbitrary seeds

For labels (4+T,3+T),(3+T,4+T), write H_i=U_i+D_i and a,b for odd slopes. The common-target equations for horizontal unit chords are exactly f_i(u)=(a_i u+D_i−(a_i²+1)/2)^2+u²+H_i. Gaussian conjugate-factor rotation preserves this target equation. On the stated fixed congruence progression in T and a, put K=96T and a near sqrt(128K²−1) with gap in [1/4,1/2]. Irrational rotation supplies infinitely many such choices. By the [narrow Gaussian sector theorem](https://arxiv.org/pdf/2008.11325), the same first-label construction can choose a factor with norm about K^8 and angular displacement in [0.045,0.055]/K²; its one linear congruence fits the actual u interval, and the first chord rotates strictly into the band while preserving n.

If the second horizontal chord with odd slope b could pass after angular change ≤11/(200K²), its original q is ≈X/K². The actual chord yields |b|=O(K), and S=(b²+1)q/2+Db(2v−b)+D(D−1) controls its relative angle as 2 arctan(1/|b|)+o(K^−2). Comparing both band ends and the allowed shifts leaves exactly the possible even differences |b|−a in {−2,0,2,4,6,8}. Five nonzero differences are excluded by actual mod-p² value-set incompatibilities at 19, 7, 5, 17 and 29. For difference zero the completed-square equation yields L₁²−L₂²=(D₂−D₁)(D₂+D₁)+(a²+1)((H₂−D₂)−(H₁−D₁)); its positive size O(X^(1/8)+K²X^(1/16)) is too small between the actual squares with |L_i| comparable to K√X. This covers all possible slopes of this restricted type only, including the bounded single rotation of the second chord.

For consecutive odd slopes (a,a+2), the general common-target identity becomes a genuine conditioned Pell equation with discriminant e₁e₂=((ab+1)/2)^2+1 and literal coordinate residues. A first short-prime factor π imposes n≡H₁ mod Nπ; this creates an additional square gate on the second completed coordinate. Even when it passes, some integral orbit must hit both height and residue. The explicit norm-one unit ((ab+1)/2+√(e₁e₂))^4 preserves the coordinate residues and grows as K^8, so a positive orbit has at most one hit per ordinary dyadic height interval. This is an obstruction to assuming free synchronization of local conditions; it does not count all orbits or exclude other chord directions.

Exact K396 control: at the same actual n the first short rotation and a second genuine seed with general coordinates work, while all relevant unrotated horizontal-unit options fail and the b=4481 option has another inert depth obstruction even after passing the selected short-prime gate. The finite verifier checks the five residue-table entries and original matched data.

~~~python
from math import gcd, isqrt

def data(T):
    A,B = 9**(T+3),25**(T+3)
    return 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B

def C(a,D): return D-(a*a+1)//2
def image(a,H,D,m):
    return {((a*u+C(a,D))**2+u*u+H)%m for u in range(m)}

L,M,a0 = 23604840,214964688050,72170223301
H,D,J,E = data(0)
for h,p,a,r,s,t in [
    (-2,19,25,8,331,293),(2,7,1,5,19,40),(4,5,1,3,8,18),
    (6,17,17,9,94,213),(8,29,49,26,519,780)
]:
    m = p*p
    assert a0%2 and (a0-a)%m==M%m==0
    assert pow(9,L,m)==1 and (p==5 or pow(25,L,m)==1)
    assert image(a,H,D,p)&image(a+h,J,E,p)=={r}
    assert {x for x in image(a,H,D,m) if x%p==r}=={s}
    assert {x for x in image(a+h,J,E,m) if x%p==r}=={t} and s!=t

def N(z): return z[0]**2+z[1]**2
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]
def smallprime(p): return p>1 and all(p%d for d in range(2,isqrt(p)+1))
def seed(P,Q,D):
    x,y = P[0]-Q[0],P[1]-Q[1]
    assert x%2 and y%2 and N(Q)==N(P)+2*D
    q = ((x+y)//2)**2+((x-y)//2)**2
    h = P[0]*Q[1]-P[1]*Q[0]
    assert q%2 and h%2==0 and 2*q*N(P)==(D-q)**2+h*h
    return q

K,a,m = 396,4479,6272660
H,D,J,E = data(1)
u = 107631485316749505966915001550914801154368133026062392450
P = (a*u+C(a,D),u)
Q = (P[0]+1,a-u)
n = N(P)+H
p,F = m*m+1,(19*971)**2
assert F*F>p and (p-1)%F==0 and pow(3,p-1,p)==1
assert all(smallprime(l) and gcd(pow(3,(p-1)//l,p)-1,p)==1 for l in (19,971))
z = mul(P,(m,-1))
assert all(x%p==0 for x in z)
P1 = mul(tuple(x//p for x in z),(m,-1))
assert 400*K*K*m>9*p and 400*K*K<11*m
assert 64*K*K*seed(P,Q,D)>N(P)

V = (39291590784097337611247250162511840943599363386177292437728,
    -480477554754808827738402215681093878519857497990500323681558)
W = (39077203952492360055572050915095205482030172452458985200149,
    -480495038331053522082116298363812621569685932789593250143863)
S = N(V)
assert N(P1)==N(P) and S+J==n and 25**80<=n<=9**128
for X,Y,d in [(P1,Q,D),(V,W,E)]:
    q = seed(X,Y,d)
    assert 2**K<=N(X)<2**(K+1) and 64*K*K*q<N(X)<64*K*(K+1)*q

assert 128*E*(2*isqrt(S)+3*E+4)*K*(K+1)<S
bs = [b for b in range(1,isqrt(128*K*(K+1))+1,2)
      if 128*K*K<b*b+1<128*K*(K+1)]
assert bs==[4481,4483,4485]
res = [((b*b+1)*S-C(b,E)**2)%31 for b in bs]
assert res==[24,21,26] and not set(res)&{x*x%31 for x in range(31)}

b,r = 4481,13399
assert pow((-C(b,E)**2-(b*b+1)*(J-H))%p,(p-1)//2,p)==1
e1,e2 = (a*a+1)//2,(b*b+1)//2
disc = e1*e2
rhs = e2*(disc*((J-H)//2)+e1*(C(b,E)//2)**2-e2*(C(a,D)//2)**2)
assert smallprime(r) and rhs%r==0 and rhs%(r*r)!=0
assert pow(disc%r,(r-1)//2,r)==r-1
~~~
