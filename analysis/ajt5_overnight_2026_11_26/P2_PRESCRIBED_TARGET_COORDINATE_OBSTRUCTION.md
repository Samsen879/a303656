# Prescribed targets can forbid shared coordinates at two genuine labels

Use A=3^a, B=5^b, labels S0=A+25B, S1=9A+625B, S2=81A+125B, S3=729A+B; set d=(S1−S0)/4, e=(S2−S0)/4. Work in the balanced strip 39/40<B/A<122/125 with ordinary heights S3<K<=729A+625B. In the actual phase a=2 mod 10, b=64 mod 110, we have S0=36 mod 121, d=4 mod 11 and e=9 mod 11. A target n=36 mod 121 and a shared coordinate would require n−S0=L²+t², so L,t vanish modulo 11. Both L²−4d and L²−4e are then nonsquares modulo 11. Thus neither of the adjacent labels can share a square coordinate with S0. Without prescribing n, the two edge conditions are locally compatible: set L²=4e+121, which has a unit square root over the 11-adics and gives 11-adic squares on both edges.

The target exclusion is not vacuous. For W=sqrt(A) and r=1 mod 11 with 1.49 W<=r<=1.5 W, put F=(e+r²+1)/11, x=nearest integer to F/r, y=F−rx, and X=11x,Y=11y. With n=S0+X²+Y², the exact identity gives n−S2=(X−2r)²+(Y−2)². For W>=1100 the strip and rounding bounds give 31W<X<32W and |Y|<9W; the corresponding two individual heights are within the ordinary window. Varying r gives on the order of W distinct coordinate pairs, since r+(e+1)/r decreases by more than one rounding step as r increases by 11. A target is repeated at most 4 tau(n−S0)=A^o(1) times, so there are A^(1/2−o(1)) distinct targets in this explicit family. Infinitely many balanced even exponent pairs satisfying the displayed residue classes exist by irrationality of log 3/log 5. The replay checks a genuine large balanced member.

These targets are represented for A303656; the obstruction concerns synchronizing the particular labels at a prescribed target. It does not change the global density or finite-certificate bounds.

```python
a, b = 574422, 392104
W, B = 3**(a//2), 5**b
A = W*W
assert a%10 == 2 and b%110 == 64
assert 39*A < 40*B and 125*B < 122*A

S0, S1, S2, S3 = A+25*B, 9*A+625*B, 81*A+125*B, 729*A+B
d, e = 2*(A+75*B), 20*A+25*B
assert (S0%121, d%11, e%11) == (36,4,9)
squares = {j*j%11 for j in range(11)}
assert (-4*d)%11 not in squares and (-4*e)%11 not in squares
assert (4*e)%11 == 3 and (4*(e-d))%11 == 9

r = 1 + 11*((3*W-2)//22)
assert 149*W <= 100*r <= 150*W and (e+r*r+1)%11 == 0
F = (e+r*r+1)//11
x = (2*F+r)//(2*r)
X, Y = 11*x, 11*(F-r*x)
n = S0 + X*X + Y*Y
assert n%121 == 36
assert n-S2 == (X-2*r)**2 + (Y-2)**2
K0, K2 = n-Y**2, n-(Y-2)**2
assert S3 < min(K0,K2) < max(K0,K2) <= 729*A+625*B

# Verify a solution of the edge conditions with no prescribed target.
assert pow(3,10,121)==pow(5,110,121)==1
lifts=[u for u in range(121) if (u*u-4*e)%121==0]
assert lifts and all((h*h-4*d)%11 in squares-{0} for h in lifts)
assert (X%11,Y%11)==(0,0) and ((X-2*r)%11,(Y-2)%11)==(9,9)
print("Prescribed-target exclusion and true unequal-coordinate witnesses verified")
```
