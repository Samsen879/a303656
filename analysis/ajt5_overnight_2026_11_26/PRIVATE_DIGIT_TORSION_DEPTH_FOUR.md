# A higher reader can block the private-digit repair at depth four

Let q>3 be inert and doubly ordinary, and suppose an admissible family of torsion choices T yields powers U T,V T modulo q^E, with n and S=U+V divisible by q. The pairs share their q-primary exponent coordinates at full period precision, and rows not reading those coordinates pass throughout. Open the private exponent digits while preserving all prime-to-q coordinates and predecessors. The exact repair line for the first digits is A x+B y=(n/q)T^(-1)−S/q modulo q, with A,B nonzero. This follows by expanding the two powers and dividing by T. Every lift on the line passes at precision two or three; at higher precision at least 1−1/q of the next lifts have exact valuation two.

If v_q(n)=1, different torsion choices yield different parallel repair lines. A single deeper reader can veto at most 1/q of the lifts above a first point. A single shallow reader covering a whole repair line must have zero target modulo its own prime and matching nontrivial characters. Its required q-primary line is fixed by the shared primary coordinates: when both axes are read, the primary components must agree independently of the other torsion factors, and the other torsion factors can only prevent activation. Thus it can cover at most one distinct repair line. Two torsion choices suffice against one such reader. A unique frozen hole among at least three choices at E=2 or 3 forces the valuation-one case, since unequal valuations give constant behavior, and equal even valuation permits at most one rejection.

At E=4, both frozen terms can have valuation three, and all torsion choices then have the same first repair line. In the replay at n=487145982612429033 and M=7²*43^4*98299², the order-seven torsion family has frozen residual 43³(1−T), with one hole. Opening the 43-primary digits preserves the predecessor at 7². All parent passes require v=41u modulo 43, where reader 98299 gives exact valuation one and is blind to the later 43-primary digits. Removing that reader permits independent exact lifts to zero at 43^4, which are also replayed.

The unrestricted panel passes at (1,0). Thus the result concerns a genuine restricted higher-reader obstruction, not an all-exponent cover. A generic minimal obstruction is not known to supply the assumed torsion family or shared primary coordinates. No global change follows.

```python
from math import gcd, lcm

p,q,R = 7,43,98299
n,d = 487145982612429033,33697459974838
Q = q**4
H = (R-1)*R
P,L = lcm(6*q**3,H),lcm(42,H//q)
assert gcd(P,p)==gcd(L,q)==1 and L%42==0

def r(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

T = pow(3,P,Q)
assert T==pow(5,2*P,Q) and T%q!=1 and pow(T,p,Q)==1
assert pow(3,P,R*R)==pow(5,P,R*R)==1
X,Y = pow(3,L,R*R),pow(5,L,R*R)
assert X==pow(Y,41,R*R) and Y%R!=1 and pow(Y,q,R*R)==1
assert [r(1,d,m) for m in (49,Q,R*R)]==[0,0,R]
assert [pow(a,L,q*q) for a in (3,5)]==[1334,259]
for x in range(p):
    c,e=1+P*x,d+2*P*x
    assert r(c,e,49)==0 and r(c,e,Q)==q**3*(1-pow(T,x,q))%Q
    for u in range(q):
        for v in range(q):
            z=r(c+L*u,e+L*v,q*q)
            assert z%q==0 and (z==0)==(v==41*u%q)
            if z==0:
                assert r(c+L*u,e+L*v,R*R)==R
assert all(r(1,0,t**e)%t for t,e in ((p,2),(q,4),(R,2)))
print("PASS")

# Check explicitly that higher parent repair steps are invisible to the reader.
for a in (3,5):
    assert pow(a,L*q,R*R)==1 and pow(a,L,49)==1
# Removing the reader permits a full zero repair in each torsion phase.
for x in range(p):
    c,e=1+P*x,d+2*P*x
    for k in range(1,4):
        assert r(c,e,q**k)==0
        e=next(e+L*q**(k-1)*i for i in range(q)
               if r(c,e+L*q**(k-1)*i,q**(k+1))==0)
    assert r(c,e,Q)==r(c,e,49)==0
print("Independent full parent lifts and reader invisibility checked")
```
