# Nonhomothetic labels in the phase gap can be obstructed at every depth

On the already certified ray (U,V)=(133n,23n), n=3^j, consider the real positive odd exponent labels (U',V')=(230n−1,299n+2). Positivity of 5^U'−3^V' follows from 5^229>3^301 and n≥1. Their normalized phase (460−2/n)/9 stays strictly inside (50,470/9). But modulo 23²,
```
5^230 = 3^299 = 170,
5^(-1)+9 = 115.
```
Thus 5^U'+3^V' has exact 23-adic valuation one at every depth, blocking the odd Eisenstein half. This rules out an actual growing trajectory inside the gap, not the entire gap. A second swapped-label trajectory (230n−1,133n) is vetoed by exact 53-adic valuation one for j divisible by 156; the replay checks the necessary exponent period and first residue modulo 53².

## Factor reuse under fixed shifts

Set A=5^U,S=3^V and let D be any odd divisor of A²−S². Replacing A,S by fA,gS with fixed rational power shifts f=5^a,g=3^b, write f=P/C,g=Q/C with C supported only on 3 and 5. In any label where the shifted actual exponents are nonnegative, the gcd of D with the shifted square difference is gcd(D,P²−Q²): modulo D we have A²=S², and both C and S are units. Thus arbitrary mixed conjugate factor reuse is bounded by a fixed integer for every nonzero fixed shift.

There is also no generic four-independent-coordinate rational norm identity of this type for unequal positive f,g. The prior halves M=N(z), P_0=N(w) give A=M+4P_0,S=4P_0−M. The shifted halves are nontrivial rational linear combinations of both M and P_0 with nonzero coefficients. As polynomials in four independent coordinates they are rank-four quadratic forms explicitly fixed by conjugation and irreducible over Q(sqrt(−3)); an irreducible of this rank cannot be a product of two linear forms. A rational-function norm has even valuation at such a fixed irreducible, whereas each shifted half has valuation one at itself. This does not rule out a special integer label having its own certificate.

## Exact finite phase strip

Across u=227,229,231,233 and all legal v, the gcd of 25^u−9^v with the full odd kernel of the 266/9 seed is always 1 or 7. The newly checked u=231 row leaves only v=13,31,131,149,295 undecided; when 3|v its norm obstruction descends to the u=77 row, because the cubic quotients are primitive odd Eisenstein norms, adding no inert odd prime factors. Remaining finite vetoes are exact valuations or odd unit-divisor certificates. This run certifies no new phase.

```python
from math import gcd, isqrt

def N(a,b):
    return a*a+3*b*b

A,S=5**133,3**23
m=(20545392562693284644384637886087735400246635261,
   3514935999169995489797558912862627624253200474)
p=(996465818327706923877110216328632044839102412,
   6159042838796558433682659260361950264266519400)
assert 2*N(*m)==A-S and 8*N(*p)==A+S and A>S

D=(A*A-S*S)//256
assert 256*D==A*A-S*S and D%2
assert 3**341<5**233<3**342
for u in (227,229,231,233):
    assert 450<2*u<470
    assert {gcd(D,pow(25,u,D)-pow(9,v,D))
            for v in range(342) if 3**v<5**u}=={1,7}

# Uniform inert obstruction across the affine growth family.
z=23**2
assert 5**229>3**301 and 450<458<460<470
assert pow(5,230,z)==pow(3,299,z)==170
assert (pow(5,-1,z)+9)%z==115
assert gcd(170,23)==1 and 115%23==0 and 115%z!=0
assert (5**229+3**301)%z==506

# Swapped exponent slots, on depths j divisible by 156.
assert pow(3,156,53*52)==1 and 5**229>3**133
assert (pow(5,229,53**2)+pow(3,133,53**2))%53**2==583==11*53

def oddval(n,p):
    e=0
    while n%p==0:
        n//=p
        e+=1
    return e%2

P=[p for p in range(2,20001,3)
   if all(p%d for d in range(2,isqrt(p)+1))]
v77={13:120983462693,23:381047,39:3861059,47:807729579959,
     71:75680634679733,87:3724439,111:20507}
v231={5:64938823274483,71:81527,79:5546711,109:50123,151:24593,
      197:244637,223:95063,247:362027,271:157907,335:23135543}

def tail(U,end,skip):
    assert 3**end<5**U<3**(end+1)
    return {v for v in range(end+1) if not skip(v)
            and not any(oddval(25**U-9**v,p) for p in P)}

assert tail(77,112,lambda v: False)==v77.keys()
assert tail(231,338,lambda v: v%3==0)-v231.keys()=={13,31,131,149,295}
for U,row in ((77,v77),(231,v231)):
    for v,d in row.items():
        H=25**U-9**v
        assert d%2==1 and d%3==2 and H%d==0 and gcd(d,H//d)==1
print("PASS")
```
