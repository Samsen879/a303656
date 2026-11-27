# Real three-shift norm controls near the square-modulus edge

Use \(S_i=3^{c_i}+5^{e_i}\), \(\delta=S_0-S_1,\ \gamma=S_0-S_2,\ F=\gamma-2\delta\), with the [square-modulus common divisor gate](SQUARE_MODULUS_COMMON_DIVISOR.md). Exact square-sum admissibility of \(F/2\) and success of the original center divisor gate are separate.

## A positive norm and a negative divisor check at the same prime

Take \((c_i,e_i)=(39,1),(51,7),(50,13)\) and \(X=3^{154}\). Then \(v_3(\delta)=v_3(\gamma)=2,\ v_3(F)=4\), the highest 3-power is \(3^{-1/3}X^{1/3}\), and
\[
 F/2=1146647866680^2+692778184407^2.
\]
For \(p=27720440095211,\ m=p^2\) choose \((d_0,A_0,B_0,r,s,V)=(41,23,1425982,-17391296576160,52100918326863,61217)\), with \(h=(A_0m+r)/d_0,\ k=(B_0m+s)/d_0\). The scaled residual equation \(2(r^2+s^2)=d_0^2F\), integer primitive chord values, and square-modulus test \(m\mid2(h^2+k^2)-F\) all hold. But the original divisor test fails: writing \(d=k-hV,\ j_{\rm edge}=2h-m\) and
\[
 Z=-\big((h^2+k^2)j_{\rm edge}(j_{\rm edge}-h)
                 +hj_{\rm edge}\delta-h^2\gamma\big)/(2m),
\]
one gets \(d=337187672636797182580564299534\) and \(Z\bmod d=247160988029273722436046358557\). No integer center is asserted.

## Finite panels can be passed cofinally

Fix a finite set of odd primes other than \(3,5\). Let \(L\) be the lcm of the parts of their \(p-1\)'s prime to 3, with \(L=1\) for an empty set. For \(j=3^t,\ N=10Lj\) use
\[
(c_0,c_1,c_2)=(2N,2N+3,2N+1),\quad
(e_0,e_1,e_2)=(j,j+2Lj,j+4Lj),\quad X=3^{6N+9}.
\]
Both axes grow; the highest 3-power is \(X^{1/3}\), and all 5-powers are below \(X^{1/3}\). In this family
\[
 F/2=25\cdot3^{2N}-5^j(5^{2Lj}-1)^2/2 .
\]
Lifting the exponent gives \(v_3(5^{2Lj}-1)=t+1\), hence \(v_3(\delta)=v_3(\gamma)=t+1,\ v_3(F)=2t+2\). At the fixed panel primes, for sufficiently large \(t\), \(p-1\mid 2Lj\) and \(F/2\) is a nonzero square modulo \(p\). At 2 it is \(1\bmod8\); at 3 it is of even valuation; at 5 the norm is split. Thus it passes the finite norm panel, with no assertion about untested prime factors. For \(L=1,t=1\), \(F/2\) passes \(2,3,5,7\) but has odd valuation at the inert prime 11119.

A necessary arithmetic-spacing condition explains the use of equally spaced 5-exponents. In a growing label family with the three required 3-valuations, suppose the 3-exponents all exceed \(2t+2\), write \(e_1-e_0=2ju,\ e_2-e_0=2jv\) using the first two valuations, with \(3\nmid uv\). Expansion of \(2(5^{2j})^u-1-(5^{2j})^v\) modulo \(3^{2t+2}\) then gives \(3^{t+1}\mid 2u-v\). Either the 5-exponents form an arithmetic progression or \(|2e_1-e_0-e_2|\ge 6j^2\). If the window has \(\log X\asymp j\), eventually only exact equality fits. This is a valuation restriction, not a sufficiency criterion.

~~~python
from math import gcd, isqrt, prod
def val(x,p):
    assert x
    v=0
    while x%p==0: x//=p; v+=1
    return v
S=[3**c+5**e for c,e in [(39,1),(51,7),(50,13)]]
delta,gamma=S[0]-S[1],S[0]-S[2]
F=gamma-2*delta
assert [val(x,3) for x in (delta,gamma,F)]==[2,2,4]
assert F==2*(1146647866680**2+692778184407**2)
p=27720440095211
qs=(2,5,49853,55604357)
assert prod(qs)==p-1 and all(all(q%d for d in range(2,isqrt(q)+1)) for q in qs)
assert pow(2,p-1,p)==1 and all(gcd(pow(2,(p-1)//q,p)-1,p)==1 for q in qs)
m=p*p
d0,A0,B0,r,s,V=(41,23,1425982,-17391296576160,52100918326863,61217)
assert 2*(r*r+s*s)==d0*d0*F
h,hr=divmod(A0*m+r,d0);k,kr=divmod(B0*m+s,d0)
assert hr==kr==0 and h%2==k%2==V%2==1 and gcd(h,k)==1 and (h*k)%p
P=h*h+k*k; d=k-h*V; j_edge=2*h-m
assert (2*P-F)%m==0
Z,zr=divmod(-(P*j_edge*(j_edge-h)+h*j_edge*delta-h*h*gamma),2*m)
assert zr==0 and d==337187672636797182580564299534
assert Z%d==247160988029273722436046358557
m0=25*3**60-5**3*(5**6-1)**2//2
assert m0%8==1 and val(m0,3)==4 and m0%7!=0
assert 11119%4==3 and all(11119%d for d in range(2,isqrt(11119)+1))
assert val(m0,11119)%2==1
~~~
