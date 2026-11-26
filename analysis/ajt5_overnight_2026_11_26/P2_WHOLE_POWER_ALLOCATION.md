# A P2 square class fixes whole collision-prime powers

Use the [P2 notation and cyclotomic blocks](P2_CYCLOTOMIC_SELMER_BLOCKS.md). Write \(R,Y,H,J\) for the positive rational half-roots of \(K-S_0,K-S_1,K-S_2,K-S_3\), respectively. In the integer half-root branch \(R,Y,H,J\in\mathbb Z\), put \(e_4=(S_3-S_0)/4=182A-6B\). In the balanced strip these shifts are strictly ordered relative to \(S_0\), so \(R>Y\) and \(d=(R+Y)(R-Y)>0\). This note gives a necessary allocation test, not a proof that the entire construction is impossible.

At an odd block prime \(p\mid C_j\), \(A=-75B\bmod p\), so \(-e=25\cdot59B\bmod p\), and \(-e_4=4\cdot3414B\bmod p\). Define
\[
 t_2=[(R+H)(Y+H)],\quad t_3=[(R+J)(Y+J)]
\]
as rational square classes. For the elliptic quotient with third root \(e\), the first expression is the Kummer coordinate for that root at a half-point with horizontal coordinate \(R^2+RY+RH+YH\): subtract \(e=R^2-H^2\). The algebra for \(e_4\) is identical. Here only the residues of these products are needed.

If \((59/p)=-1\), \(p\) cannot divide both \(R,Y\), since \(H^2=R^2-e\) would be nonsquare modulo \(p\). Hence it divides precisely one of \(R+Y,R-Y\) and the whole of \(p^{v_p(d)}\) goes to that factor. When \(p\mid R+Y\), \((R+H)(Y+H)=H^2-R^2=-e\bmod p\) has character \(-1\). When \(p\mid R-Y\), it is a nonzero square modulo \(p\), as \(p\nmid e\). The character of \(t_2\) therefore fixes the whole assignment, even at even collision depth; the value of \(v_p(d)\bmod 2\) alone could not do this. The same implication holds with \(3414,t_3\) when \((3414/p)=-1\). At a prime split for both characters, these tests alone need not determine the allocation.

For a factorization-free count at fixed \(t_2\) and fixed allocations outside \(C_j\), recall \(U/V\) has order \(2\cdot11^j\) at \(p\mid C_j\), and \((\frac{U/V}{p})=(\frac3p)\) since the 3 exponent is odd and the 5 exponent even. Its order has 2-part exactly two, so its character is \((\frac{-1}{p})\). By quadratic reciprocity this forces \(p=1\bmod3\) as well as \(p=1\bmod 2\cdot11^j\). Put
\[
 L_j=\left\lfloor\log_{1+6\cdot11^j} C_j\right\rfloor.
\]
The sum of the factor multiplicities is at most \(L_j\). The block character \((\frac{59}{C_j})=-1\) ensures at least one nonsplit factor, leaving at most \(L_j-1\) total multiplicity for the split factors. A split factor of multiplicity \(m\) can give at most \(m+1\le2^m\) choices of its exponent in \(R+Y\); hence at most \(2^{L_j-1}\) allocations overall. If the parity of the exponent assigned at every split prime is also fixed, the factor \(m+1\) improves to \(\lfloor m/2\rfloor+1\le2^{\lfloor m/2\rfloor}\), giving at most \(2^{\lfloor(L_j-1)/2\rfloor}\) allocations. Any actual allocation determines \(R=(R+Y+R-Y)/2\), hence at most one \(K\). The bound does not fix the square classes or allocations outside the block and is not a rank estimate.

## Independent finite controls

The exponent example below is locally admissible at all primes by the [complete separate local cover](FOURTH_SQUARE_COMPLETE_LOCAL_COVER.md). A first block contains two different split behaviors and a depth-two nonsplit prime. The final computation exhibits a different collision at 83; for the formal Kummer triple \((75241,75241,1)\), the single-root coordinate there is a nonsquare unit while the collision valuations are both even, violating the isolated odd-depth necessary condition. No global point is assumed in the example.

~~~python
from fractions import Fraction as F
a,b=149374607874053559604530046712138071254976,101964032633743994567082439504174842605532
assert (a%720,b%720)==(16,12)
assert (a-1)%319==(b+2)%319==0
for p,bad in [(7,{1}),(11,{3,4,5,9}),(13,{4,9}),(17,{16}),(19,{9,16}),(61,{16})]:
    assert pow(3,a,p)*pow(5,-b,p)%p not in bad
def ln(k):
    t=F(k-1,k+1); n=300
    lo=2*sum(t**(2*j+1)/(2*j+1) for j in range(n))
    return lo,lo+2*t**(2*n+1)/((2*n+1)*(1-t*t))
l3,u3=ln(3); l5,u5=ln(5)
assert -F(1,25)<b*l5-a*u3<=b*u5-a*l3<F(1,25)
def dep(x,p):
    v=0
    while x%p==0:
       x//=p; v+=1
    return v
for p,want in [(67,(1,1,1)),(1123,(1,1,1122)),(199,(2,198,1))]:
    mod=p**4
    u,v=pow(3,(a-1)//11,mod),pow(5,(b+2)//11,mod)
    fj=sum((-1)**j*u**(10-j)*v**j for j in range(11))%mod
    assert fj!=0
    assert (dep(fj,p),pow(59,(p-1)//2,p),pow(3414,(p-1)//2,p))==want
p=83; mod=p**4
A,B=pow(3,a,mod),pow(5,b,mod)
assert dep(5*(4*A+5*B),p)==1 and dep(2*(A+75*B),p)==0
assert pow(75241,41,p)==p-1
~~~
