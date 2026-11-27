# Two genuine residual sources require different full-depth directions

At an actual prime with covered 343-primary axes, a fixed (e,k) tag matching modulo 49 but not 343 can be rejected by a single primitive direction w only if w·(1,k)=0 mod 7. Indeed a projected high-digit condition is w·δ=j w·(1,k), where the actual pair is e(1,k)+49δ. A nonzero right coefficient always allows some j. If the right coefficient is zero then the nonmatching full pair forces the left coefficient nonzero for the primitive perpendicular direction.

The true (32,305) remainder has a collision at 8756387804994449437096567 with tag (25,27), forcing u−v=0 mod 7. The true (70,180) remainder has a collision at 105252402993769124507 with tag (43,324), forcing u+2v=0 mod 7. The chart menus in the replay were independently reconstructed. Distinct direction lines prove that no single primitive direction works jointly on these two actual remainders. A height-one pair, (1,1) and (1,−1), succeeds: its determinant is −2, so inversion modulo 2401 reconstructs both axes on their certified common support. Within (70,180) alone the winning tailored direction (−2,1) has height two and no height-one direction can work alone. This is a result about two distinct sources, not a same-source necessity theorem.

For the still-unfactored true (17,188) source R, every prime factor is 1 mod 343 because the native root has exact order 343 at each prime. Since R is 3 mod 4, for a factor pair ab=R we have (a−1)(b−1) divisible by 8·7^6, so a+b≡R+1 mod that modulus. The first possible sum above sqrt(4R) has nonsquare discriminant, giving the stated exact gap lower bound. This neither supplies an annihilator nor closes this source.

```python
from math import gcd, isqrt, prod

F=1943082217354490828347054251619066486713606725263955277084
H=2401
assert F%7
iv=pow(2,-1,H)

cases=[
    (1226529180174843075531420358020848179,
     329367279535621018558882955258773074,
     8756387804994449437096567,25,27,
     ((25,27),(31,97),(31,146),(31,244)),(1,1)),
    (11051476612278046737802105046809349,
     9245853789192210049832386241957137,
     105252402993769124507,43,324,
     ((15,58),(43,324)),(-2,1)),
]
for Q,x,p,e,k,T,(u,v) in cases:
    assert Q%p==0 and p%1372==687
    assert pow(x,343,Q)==1 and gcd(Q,pow(x,49,Q)-1)==1
    Z=pow(x,F,Q)
    X=pow(15,F,Q)
    Y=pow(3*pow(5,-1,Q)%Q,F,Q)
    assert pow(X,H,Q)==pow(Y,H,Q)==1
    A=pow(X*Y%Q,iv,Q)
    B=pow(X*pow(Y,-1,Q)%Q,iv,Q)

    # Genuine mod-49 collision with full-depth mismatch.
    assert gcd(Q,pow(A,7,Q)-pow(Z,7*e,Q),
                 pow(B,7,Q)-pow(A,7*k,Q))==p
    assert gcd(p,B-pow(A,k,Q))==1

    # The two height-one mixed readings close the whole residual.
    assert all(gcd(Q,pow(A,7,Q)-pow(Z,7*i,Q),B-pow(A,j,Q))==1
               for i,j in T)

    # The tailored one-word reading also closes this residual.
    assert all((u+j*v)%7==0 for i,j in T)
    W=pow(pow(3,u,Q)*pow(5,v,Q)%Q,F,Q)
    assert pow(W,H,Q)==1
    assert gcd(Q,prod(W-pow(Z,i*(u+j*v),Q) for i,j in T))==1

assert 27%7!=324%7
assert all((u+2*v)%7 for u in (-1,0,1) for v in (-1,0,1)
           if (u,v)!=(0,0))

R=626751537547263614426465772417729978972491
x=252568635021313874012910903862214825457075
assert R%4==3 and pow(x,343,R)==1 and gcd(R,pow(x,49,R)-1)==1
m=8*7**6
s=1+isqrt(4*R)
s+=(R+1-s)%m
d=s*s-4*R
assert s==1583352819238041815588 and isqrt(d)**2!=d
d=(s+m)**2-4*R
lo=isqrt(d)
assert lo*lo<d and lo+1==60360012342528
```
