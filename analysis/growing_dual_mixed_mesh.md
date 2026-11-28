# Frozen final theorem: two growing primitive mixed-edge meshes at one positive-gap anchor

This note is self-contained. The final anchor is H0=A+125B; formulas and numerical obstruction controls from earlier anchors must not be mixed with it.

## Theorem and exact quantifiers

For every integer J>=128 define

m=floor(J/16), O=lcm(1,3,...,2J+1), L=4O,
s=20L, K=90s, A=9^s, B=25^s,
F=lcm(1,2,...,4m+1).

There is a deterministic finite construction of an integer n with

B^16<n<A^32, n=6 mod8,

one Gaussian integer P and two families of Gaussian integers R_(1,j), R_(2,j), 0<=j<m, such that

N(P)=n-H0, H0=A+125B=3^(2s)+5^(2s+3),
N(R_(1,j))=n-H1, H1=3A+25B=3^(2s+1)+5^(2s+2),
N(R_(2,j))=n-H2, H2=27A+B=3^(2s+3)+5^(2s).

All three norms are positive. Both labels change on each of the two edges from P. Put

D=50B-A>0, E=62B-13A>0, S=N(P).

Every chord R_(i,j)-P has two odd, coprime coordinates. With q_(i,j)=N(R_(i,j)-P)/2 and w_(i,j)=det(R_(i,j)-P,P)/2,

2q_(i,j)S=(D_i-q_(i,j))^2+4w_(i,j)^2,
2^K<=S<2^(K+1),
64K^2q_(i,j)<S<64K(K+1)q_(i,j),

where D_1=D and D_2=E. In particular q is a positive odd integer and w is integral.

Define

a=1/[64K(K+1)], Delta=1/[64K^2(K+1)], xi=(q/S-a)/Delta.

The first family's m xi values occupy, one each, the m equal bins of [1/4,3/8]. The second family occupies the m equal bins of [5/8,3/4]. The xi values are distinct within and across families. Including the endpoints, each normalized maximum gap is at most1/(4m), with endpoint gaps at most1/(8m). The generating positive Gaussian rotation angles form meshes on the corresponding critical arcs, with maximum angle gap at most1/(16mK^2), or at most3/m times the length of that arc. Thus their normalized mesh size tends to zero.

This is an existence and explicit-construction theorem on the displayed sparse sequence of exponent layers. The chosen n is common to all points at one layer; it is not an arbitrary externally prescribed n. The theorem has three labels; the mesh size, rather than the number of labels, grows. No claim gcd(q,D_i)=gcd(S,D_i)=1 is made.

## 1. Exact quadratic norm identity

Let rho=(2+i)^(2s), so N(rho)=B. Define

U(t)=A[(3-i)t-38+12i]
    +B[(-15+5i)t^2+(-147+49i)t+138-16i].

Set

P=U(t)/(2bar(rho)),
v1=1+3i, v2=(t+1)+i(3t+1),
Q1=P+rho v1, Q2=P+rho v2,
n=H0+N(P).

Then identically in rational t,

N(Q1)-N(P)=2D,
N(Q2)-N(P)=2E.

A compact verification uses
V=5Bt^2+(D-B)t+D-E-4B,
U=2D-10B-3V+iV.
The scalar product of U/(2B) with(1,3) equalsD/B-5. Substitution into the second chord verifies its half gapE/B. Multiplication by rho multiplies all norms by B.

## 2. Integrality and parity

Write rho=r0+i r1. Its coordinates are coprime, and r1 is invertible modulo B. Let

I5=r0*r1^(-1) modB,
t=(38-12I5)*(3-I5)^(-1) modB,
t=0 mod2.

Here I5^2=-1 modB and I5=2 mod5; the denominator is1 mod5 and t=4 mod5. Substitution i=I5 shows bar(rho) divides U/2. Hence P is integral.

For t=2k, the coordinates of U/2 are

3Ak-19A-30Bk^2-147Bk+69B,
-Ak+6A+10Bk^2+49Bk-8B.

Both are even, since A and B are odd. Since rho has odd norm, P is an even coordinate pair. The two Q_i are odd coordinate pairs. Their raw chords are primitive: gcd(t+1,3t+1)=1 for even t; multiplication by rho can only create a common factor5, and the conjugate5 component of v2 is2t+3=1 mod5. For v1, use1+3i=(1+i)(2+i).

The identities also give S=0 mod8: Q1 has odd coordinates, so N(Q1)=2 mod8; D=1 mod4, hence2D=2 mod8. Since H0=6 mod8, n=6 mod8.

## 3. Primitive Gaussian factor families from the actual bases

Put r=(3/5)^20. For e=2^v h, h odd, define

gamma_e=[5^(20e)+chi4(h)i3^(20e)]/(1+i),
chi4(h)=(-1)^((h-1)/2).

Each gamma_e is integral and primitive, and
N(gamma_e)=[5^(40e)+3^(40e)]/2
is odd and coprime to3 and5.

Use e_(1,j)=2j+1 and e_(2,j)=2(2j+1), 0<=j<=J. Within either family arbitrary products of positive powers remain primitive. The norm moduli of the two families are coprime.

For the first assertion, let X=5^20/3^20 modulo an odd common norm prime. If a factor at index2j+1 and a conjugate factor at2k+1 shared the same Gaussian prime, then at its i=I branch
X^(2j+1)=-(-1)^j I,
X^(2k+1)=(+1)(-1)^k I.
Raising to the other odd exponent gives contradictory signs for the same nonzero power. The second family uses X^2. For cross-family coprimality, a common prime would give X^(2e)=-1 and X^(4f)=-1 for odd e,f; raising these to2f ande gives1=-1.

For every selected e, 2e dividesL. Thus A=B moduloN(gamma_e), by raising the identity(5/3)^(40e)=-1 to an even power.

Let d1=ceil(r^-2), d2=ceil(r^-4), and force

G_i=product_j gamma_(e_i,j)^(4F d_i), M_i=N(G_i).

The products remain primitive, and M1,M2 are coprime.

## 4. Simple quadratic roots lift without a global discriminant square

For G=u+iv primitive, M=N(G), take I=-u*v^(-1) modM. The divisibility condition G|z is equivalent to Re(z)+I Im(z)=0 modM.

The endpoint polynomials C_i=2Q_i bar(rho)=U+2Bv_i have scalar coefficients

a=B(-15+5I),
b1=A(3-I)+B(-147+49I), c1=A(-38+12I)+B(140-10I),
b2=A(3-I)+B(-145+55I), c2=A(-38+12I)+B(140-14I).

When A=B at an initial factor modulus, both polynomials have root t0=(3+I)/5. Their derivatives there are

C1'(t0)=B(-164+48I), with Gaussian norm29200 B^2=2^4*5^2*73 B^2,
C2'(t0)=B(-162+54I), with Gaussian norm29160 B^2=2^3*3^6*5 B^2.

The only extra possible bad forcing prime is73, and it never occurs. Indeed, a norm divisible by73 would imply(5/3)^(40e)=-1 mod73. Taking the ninth power contradicts Fermat, since360e=72*(5e). Thus both derivatives are units on every forcing modulus.

Lift only C1 on M1 and only C2 on M2. Within a family the initial norms can share primes, so A=B is asserted only modulo their lcmR_i, not their product. One has
R_i|M_i and M_i|R_i^[4F d_i(J+1)].
The same-side orientation makes the initial roots compatible. Newton iteration on the full M_i,

t <- t-C_i(t)*(C_i'(t))^(-1) modM_i,

doubles all initial prime valuations each step and terminates in at mostceil(log2(4F d_i(J+1))) steps. This uses gcd and modular inversion, not prime factorization. The two resulting t roots combine by CRT because M1,M2 are coprime.

## 5. Complete integral rotation meshes and exact bin selection

Every switch
Z_i=product_j gamma_(e_i,j)^(4F b_j), 0<=b_j<=d_i,
produces an integral point R_i=(Q_i/Z_i)bar(Z_i) of the required norm.

The rotation angle is
phi=-8F sum_j chi4(oddpart(e_i,j)) b_j atan(r^e_i,j) mod2pi.

Reversing negative digits converts this to a translate of a positive digit box. Adjacent step ratios are at most r^-2 orr^-4, while the digit caps are at least these ratios. The first digit range exceeds a full circle. Greedy subtraction gives full-circle maximum gaps

delta1<=8F r^(2J+1), delta2<=8F r^(4J+2).

No uniqueness of digit expansions is assumed. The gap bound itself supplies distinct points in disjoint intervals.

Let a andDelta be as in the theorem. Divide [1/4,3/8] and[5/8,3/4] into m equal bins. For each bin preselect a full-mesh angle whose ideal coordinate(eta-a)/Delta lies in the bin's central half, whereeta=1-cos(phi). This yields exactly2m desired rotations, chosen before t.

This selection is exactly decidable: if Z=z+iw, theneta=2w^2/N(Z) andsin(phi)=-2zw/N(Z). The bin tests use integer cross-products, and sin(phi)>0 selects the positive small arc. No floating-point angle claim is required.

## 6. Simultaneous primitivity at one t

First gcd(M1M2,DE)=1. At every forcing prime A=B, soD=E=49B. Its only possible overlap prime is7, but a primitive Gaussian norm has no3 mod4 prime divisor.

Any odd common coordinate divisor of a chord divides the corresponding half gapD orE. Both gaps are odd and coprime to3 and5, so onlyp>=7 need consideration.

At p|DE withp<=4m, every rotation multiplier is1 modulo p. A norm-one unit has order dividingp-1 in the split ring andp+1 in the inert field. Both divideF=lcm(1,...,4m+1). The raw chord never vanishes as a pair modulo suchp: the first has norm10B, and for the second t+1=3t+1=0 would imply2=0.

Atp|DE withp>4m, each desired rotation forbids at most two t classes. If its multiplierlambda is1, there is no bad class. Otherwiselambda-1 is a unit: in the split ring a norm-one pair is(x,x^-1), and a component equal to1 forces both to be1; the inert ring is a field. The quadratic leading coefficient of P isrho(-15+5i)/2, whose norm is(125/2)B and hence a unit atp>=7. Thus the rotated chord has at most two simultaneous coordinate roots.

There are2m preselected chords, so at most4m forbidden classes. Sincep>4m, a legal common class exists. All preselected mesh points therefore survive at the same t; no unjustified maximum-gap conclusion is drawn from a mere count of survivors.

## 7. A deterministic factorization-free avoidance algorithm

Let N=|DE|. For each selected Z on edge i define
W_(i,Z)(t)=C_i(t)bar(Z)-U(t)Z.
The denominator2bar(rho)Z is a unit at every prime ofN, so a chord vanishes modulo such a prime exactly when both coordinates ofW do.

Maintain a remaining modulusR, initiallyN. For k=0,...,4m set

h=gcd(R, product_selected gcd(R,Re W(k),Im W(k))),
bad=gcd(R,h^bit_length(R)), good=R/bad.

Modular exponentiation suffices. The bad part contains each supported prime to its full valuation inR, so good andbad are coprime. Assignt=k modgood, incorporate that block by CRT, and replaceR bybad. Every prime is assigned by the end: small primes accept all k; a large prime sees4m+1 distinct candidate classes but at most4m forbidden ones.

The final period after including integrality and both forcing roots is
h_total=2B M1M2 |DE|<6200 B^3 M1M2<2^13 B^3 M1M2.
No factorization ofDE or unbounded search for t is needed.

## 8. Explicit gate J>=128 and ordinary height

Elementary LCM estimates give
4^(J+1)/(2J+1)^2<=L<=4^(2J+2),
s>20*2^(2J)/(J+1)^2,
s<2^(4J+9), K<2^(4J+16).

The lower LCM bound follows becausebinom(2J,J) divideslcm(1,...,2J), and removal of its maximal power of2 costs at most2J+1. For the upper boundlcm(1,...,n)<=4^n, induct on n: the ratios from n to floor/ceiling(n/2) divide the relevant central binomial coefficient. For odd n=2h+1, usebinom(2h+1,h)<=2^(2h).

One has2^-15<r<2^-14, d1<=2^30,d2<=2^60 andlog2N(gamma_e)<93e. Hence
log2(M1M2)<F*2^71(J+1)^2.
Also log2F<=8m+2<=J/2+2. ForJ>=128,log2(J+1)<=J/16, giving

log2(log2(M1M2))<5J/8+73,
log2s>15J/8+4.

Thuslog2(M1M2)<s andlog2h_total<13+16s.

PutT=(2^K/B)^(1/4) and choose t in[3T/8,2T/5]. SinceB<2^(5s), the window widthT/40 haslog2 greater than21.25s-6, so it contains a representative of every legal CRT class.

For the present anchor, d=D/B=50-A/B lies in(49,50), and e=E/B=62-13A/B lies in(49,62). WriteP/rho=vt^2+wt+c withv=(-15/2,5/2). Direct coefficient bounds give|w|<78,|c|<70, whence

|P/rho-vt^2|<150t,
|S/B-(125/2)t^4|<2^15 t^3.

For t>=2^16 the relative error is<1/16. Therefore throughout the window
(9/8)2^K<S<(7/4)2^K.
SinceH0<=126B,
B^16<2^(80s)<S<n<2^(90s+2)<2^(96s)<A^32.

For t>=256,|P|>=7sqrt(B)t^2. The raw chord lengths are at most4sqrt(B) and5sqrt(B)t, and both gaps are at most62B. The exact formula

q_i/S=1-cos(phi)+D_i/S-Re(exp(i phi)(Q_i-P)bar(P))/S

therefore has error<1/t. The chosen window gives t>2^24K^4: useK<128s ands^4<=2^s for s>=16. Since m<K, this implieserror<Delta/(64m). It is smaller than the selected core's margin to its bin boundary. Hence every actual xi lies strictly in the required bin.

Finallydelta1<2^(-27.5J-9), while every central half-bin has angular width at least1/(512mK^2)>2^(-9J-41). Thus each core contains a full-mesh point. On the relevant arcs,1/(16K)<sin(phi)<1/(4K), andsin_max/sin_min<=2. The selected angle gaps are consequently at most1/(16mK^2), or3/m times the arc length. This completes all simultaneous integrality, height, norm, primitivity, and mesh requirements.

## 9. Exact native obstructions inside the same final model

The global discriminant-square route fails on every main layer. The second endpoint has

Disc_t C2=(3-i)^2 R,
R=(D-5B)^2+20EB=A^2-350AB+3265B^2
 =2916B^2+(B-A)(349B-A)>0.

At the fixed prime193, x=9/25=93 satisfiesx^48=-1,x^96=1. Every main layer has s=80O=48 mod96 becauseO is an odd multiple of3. ThusA/B=-1 mod193 and
R/B^2=3616=142 mod193,
142^96=-1 mod193.
So R is never a rational square, and since it is positive it is not a square inQ(i). The quadratic C2 is irreducible overQ(i) throughout the entire main family. The positive construction uses separate local simple-root lifts, not a false global-square premise.

There is also an exact common-lift criterion. Forp not dividing30 andI^2=-1 modp^k,
C2-C1=2B[(1+3I)t-2I].
A common root must equal t0=(3+I)/5; substitution gives
C_i(t0)=12(-3+I)(A-B).
All these coefficients are units, so a common root exists if and only if A=B modp^k.

In this FINAL anchor model, the actual values s=2,A=81,B=625,p=17,k=2,I=38 give common initial root15 modulo17, but separate simple lifts49 and100 modulo289 and no common root. At s=34, the common root66 modulo289 returns. These are the correct countercontrol numbers for H0=A+125B.


## 10. Count distinct targets, not parameter aliases

In the interval for \(t\), one legal parameter class modulo the displayed total period contributes at least \(\lfloor 2^{21s/4-19}\rfloor\ge2^{5s}\) integers. Each keeps the same preselected bins, divisibility, and primitivity conditions. Write \(P/\rho=vt^2+wt+c\), with \(|v|^2=125/2\), \(|w|<78\) and \(|wt+c|<150t\). For \(t\ge256\),
\[
(P/\rho)\cdot(P/\rho)' \ge125t^3-3024t^2-11700t>0.
\]
Thus these parameters generate distinct \(n\). The elementary bounds on the odd LCM give \(\log K\asymp J\), so each of both edges has \(\Theta(\log K)\) occupied bins. The count does not yield pointwise coverage or any density conclusion.

## Exact replay at a smaller native layer

The script constructs the eight verified endpoints (four per edge) at \(s=42,K=4029\), with actual labels, and checks bin membership, ordinary height, primitivity and a same-target countercontrol. It is a finite native control, not a materialization of the enormous all-\(J\) construction. The all-\(J\) quantifier is proved above.

```python
from math import comb,gcd,isqrt,prod
s,K=42,4029
A,B=9**s,25**s
H=(A+125*B,3*A+25*B,27*A+B)
D,E=(H[0]-H[1])//2,(H[0]-H[2])//2
# edge, bin, a,b for divisor a-i*b, verified modular root
pack=(
    (1, 0, 4786648, 105, 4166402983095),
    (1, 1, 2233760, 49, 4203548683733),
    (1, 2, 3191071, 70, 268576829947),
    (1, 3, 5424800, 119, 15962826517306),
    (2, 0, 2871850, 63, 2913516008210),
    (2, 1, 2233654, 49, 1937840990991),
    (2, 2, 4786382, 105, 21199354421098),
    (2, 3, 4467275, 98, 12010672491224),
)
r=sum(comb(2*s,j)*2**(2*s-j)*(-1)**(j//2) for j in range(0,2*s+1,2))
v=sum(comb(2*s,j)*2**(2*s-j)*(-1)**((j-1)//2) for j in range(1,2*s,2))
assert r*r+v*v==B
I=r*pow(v,-1,B)%B
mods=[(0,2),(0,abs(D*E)),((38-12*I)*pow(3-I,-1,B)%B,B)]
mods += [(root,a*a+b*b) for _,_,a,b,root in pack]
M=prod(d for _,d in mods)
R=0
for a,d in mods:
    h=M//d
    assert gcd(h,d)==1
    R+=a*h*pow(h,-1,d)
T=isqrt(isqrt((1<<K)//B));lo=(3*T+7)//8;hi=2*T//5
t=lo+(R-lo)%M
assert lo<=t<hi
fx=A*(3*t-38)+B*(-15*t*t-147*t+138)
fy=A*(-t+12)+B*(5*t*t+49*t-16)
assert (r*fx-v*fy)%(2*B)==(v*fx+r*fy)%(2*B)==0
x,y=(r*fx-v*fy)//(2*B),(v*fx+r*fy)//(2*B)
S=x*x+y*y;n=S+H[0]
assert 1<<K<S<1<<(K+1) and B**16<n<A**32 and n%8==6
qs=[]
for edge,j,a,b,root in pack:
    p,q=(1,3) if edge==1 else (t+1,3*t+1)
    ux,uy=r*p-v*q,v*p+r*q
    X,Y=x+ux,y+uy;N=a*a+b*b;c,h=a*a-b*b,2*a*b
    assert gcd(a,b)==1 and (c*X-h*Y)%N==(h*X+c*Y)%N==0
    xx,yy=(c*X-h*Y)//N,(h*X+c*Y)//N
    assert X*X+Y*Y==xx*xx+yy*yy==n-H[edge]>0
    dx,dy=xx-x,yy-y;seed=(dx*dx+dy*dy)//2
    gap=(D,E)[edge-1];det=x*dy-y*dx
    assert dx%2==dy%2==1 and gcd(dx,dy)==1 and det%2==0
    origin=S if gap>0 else S+2*gap
    assert 1<<K<origin<1<<(K+1)
    assert 2*seed*origin==(abs(gap)-seed)**2+det*det
    k=(8 if edge==1 else 20)+j
    assert k*origin<32*(64*K*K*(K+1)*seed-K*origin)<(k+1)*origin
    assert 64*K*(K+1)*((ux*ux+uy*uy)//2)<S # same-n negative control
    qs.append(seed)
assert qs==sorted(set(qs))
print('PASS',n.bit_length(),M.bit_length(),len(qs),[n%1000000007,*[q%1000000007 for q in qs]])
```
