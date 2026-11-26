# Three actual columns in two directions, with one remaining quartic norm

Use the period $P$ and modulus $M$ from FIRST_248_PRIMITIVE_SIEVE_SEED.md, and take $d=4,e=4+2P,E=4+4P$. The common odd-direction obstruction in FIRST_248_THREE_COLUMN_DIRECTION_LIMIT.md can be bypassed for the three parent norms and their three associated child norms. The construction below does **not** make the first root 248 genuine; its value is a separate quartic condition.

Put $J_1=(5^E-5^d)/16$, $J_2=(5^E-5^e)/16$, $K=4M$. Let $A=(a,b)$ and choose $B$ with determinant $\det(A,B)=1$, using the explicit recipe in the replay. For $B_t=B+KtA$, solve the two integral equations
$$
 A\cdot U_t=J_1-\|A\|^2,\qquad B_t\cdot U_t=J_2-\|B_t\|^2.
$$
The solution is integral for all $t$ because the determinant stays one. Let $m=5^E+1+4\|U_t\|^2$. The three positive parent norms, for sufficiently large parameters, are represented by $2U_t$, $2(U_t+2A)$, $2(U_t+2B_t)$ at exponents $E,d,e$ respectively. For example $\|U_t+2A\|^2-\|U_t\|^2=4J_1$, so multiplication by four gives the required difference $5^E-5^d$. Multiplication by 5 gives all three true child norms at $x=5m+4$. The modular checks below ensure $m\equiv5150158917\bmod M$ and $m\equiv6\bmod16$, which preserve the old negative certificates before 248.

The remaining quantity is the quartic $F(t)=x-248=20\|U_t\|^2+5^{E+1}-239$. The first linear equation stays fixed, and in the second subtracting off $KtA$ shows $U_t-U_0$ is a quadratic polynomial times $(-b,a)$. Hence $F$ is a quartic. On $t\equiv142\bmod529$, its residue is 23, giving an unbounded genuine family where the three specified columns exist but the candidate 248 fails. Also modulo 61 its polynomial is $-11t^4-24t^3+12t^2-18t-9$. The remainder of $t^{61^2}-t$ is $-2t+10$, and the quartic is nonzero at 5. Thus it has no factor of degree 1 or 2 over that field, and is irreducible there. As 61 splits in the Gaussian integers and the leading coefficient is a unit there, $F$ is irreducible over $\mathbb Q(i)$; it cannot be an identically rational-function square sum, since a conjugation-fixed irreducible factor of such a norm has even exponent. This does not rule out true square sums at individual integer parameters.

```python
M=9347826066398882709188429669140410838620697995580440275819854118709839842706586206254981282837544384679264569603
P=6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
a,b=5784055134056927907247635382153734482167865971255565960965180622193242759438167057594857860878893616437210675069,15024202558212281670089175723106771482915330797258891372556723885206861634066331881237934140021751558873102167448
c,h=9633617704578251581428466164919189062461147474120517796315181795640269266366476622446875122795056478309929118304,10518065210484555673235118299279298517604524197909937395058128453101112196058770338435270230330259748922227002541
K=4*M
r=pow(a,-1,b)
s=(1-a*r)//b
z=(r*(c+s)+s*(h-r))%K
B=(-s+z*a,r+z*b)
assert a*B[1]-b*B[0]==1
assert (B[0]%K,B[1]%K)==(c,h)
d,e,E=4,4+2*P,4+4*P
def J(i,q):
    return ((pow(5,E,16*q)-pow(5,i,16*q))%(16*q))//16
def U(t,q):
    C,D=((B[0]+K*t*a)%q,(B[1]+K*t*b)%q)
    j1,j2=J(d,q)-a*a-b*b,J(e,q)-C*C-D*D
    return ((D*j1-b*j2)%q,(a*j2-C*j1)%q)
def F(t,q):
    u,v=U(t,q)
    return (20*(u*u+v*v)+pow(5,E+1,q)-239)%q
u,v=U(0,M)
assert (4*(u*u+v*v)+626-5150158917)%M==0
assert U(0,4)==(1,2)
assert U(142,529)==(360,24) and F(142,529)==23
assert all(F(t,61)==(-11*t**4-24*t**3+12*t*t-18*t-9)%61 for t in range(5))
```
