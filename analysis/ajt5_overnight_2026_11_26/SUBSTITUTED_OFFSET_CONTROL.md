# One offset substitution: a 25-center control but the same uniform obstruction

Replace index 36 by 39 in the single \(D+8i\) menu. The resulting \(J=\{0,\ldots,35,39\}\) still cannot provide 25 uniformly, even allowing an arbitrary shared \(C\), initial \(D\), and choice of retained subset. On a different explicit CRT class it gives 25 and fixes a specific tie at 199.

### Same hard class for all seeds

For \(n\equiv372715\bmod658812\), apply the parity and unit tests of the [original menu obstruction](https://github.com/Samsen879/a303656/commit/2f6837d5552626a9973825edd41179943cc432a6). If \(D\) is odd, the union of the two discarded classes modulo 3 and 11 still has at least 14 indices, checked directly on \(J\). Exactly the same order-506 bound at \(23^2\) permits at most one reinstatement since \(|i-j|\le39<253\). This caps the count at 24 with the even-valuation repair at 23 and 23 with units there. In the only remaining branch, \(C=0,\ D\) even, the union of the classes modulo 3 and 5 still has at least 16 entries; the bound is 22 even allowing the possible reinstatement at 31.

### A 25-center finite-phase control on another target class

At seed \(C=D=2\), keep \(i\not\equiv1\bmod3\). The old menu hits indices 3 and 36 at 199 with first readings \(1,43\), so a common base-5 first digit cannot repair both. The substituted menu has only the hit at 3. A single base-5 repair leaves \(182\cdot199^2\bmod199^3\), with units at all other tested inert odd primes through 211 and at the protected tie primes. This comparison holds at the same target and at the same frozen starting seed; it does not exclude other seed choices for the old menu.

For non-reuse, if an inert \(q>23\) ties two offsets, its base-5 order divides \(2m\), where \(m\) is the odd part of their difference. The factorization replay certifies the exact tie universe and the fact that each such \(q\) occurs only to exponent one in the appropriate \(5^{2m}-1\). Consequently a base-5 Wieferich prime cannot tie two centers, since otherwise its square would divide that same integer. This includes any genuine common-Wieferich reader. Neither the targeted count nor this non-reuse argument supplies an ordinary height bound.

~~~python
from collections import Counter
from math import gcd, isqrt, lcm, prod

# Multiplying the rows indexed by divisors of m gives 5**(2*m)-1.
F = {
 1:(2,2,2,3), 3:(3,7,31), 5:(11,71,521), 7:(29,449,19531),
 9:(3,19,829,5167), 11:(23,67,5281,12207031),
 13:(5227,38923,305175781), 15:(61,181,1741,7621),
 17:(409,3061,41540861,466344409), 19:(191,761,6271,19609,3981071,213029),
 21:(7,43,127,379,7603,519499), 23:(47,8971,42272797713043,332207361361),
 25:(101,251,401,1901,9384251,50150933101),
 27:(3,109,163,271,487,4159,31051,16018507),
 29:(59,35671,5096867,22125996444329,6090817323763),
 31:(1303,1861,21207101,28086211607,625552508473588471),
 33:(199,595123,190771747,386478495679), 35:(211,631,4201,15216601,85280581,4698932281),
 37:(149,9103,29010221,13971969971,8737481256739,45920153384867),
 39:(79,3121,22735632934561,608459012088799)
}
W = {42272797713043:(13967,4523),332207361361:(9781,293),
     50150933101:(201167,277),22125996444329:(13624382047,),
     6090817323763:(2061161,37),28086211607:(453003413,),
     625552508473588471:(391337,25654001),386478495679:(5855734783,),
     13971969971:(5394583,),8737481256739:(28294769,),
     45920153384867:(620542613309,),22735632934561:(3271,701,227),
     608459012088799:(95393,82021)}

def prime(n):
    if n not in W:
        return n>1 and all(n%d for d in range(2,isqrt(n)+1))
    u=prod(W[n])
    return (u*u>n and (n-1)%u==0 and pow(2,n-1,n)==1
            and all(prime(p) and gcd(pow(2,(n-1)//p,n)-1,n)==1 for p in W[n]))

T=set()
for m in F:
    f=Counter(q for d,fs in F.items() if m%d==0 for q in fs)
    assert all(map(prime,f)) and prod(q**j for q,j in f.items())==5**(2*m)-1
    assert all(j==1 for q,j in f.items() if q>23)
    T.update(q for q in f if q>23 and q%4==3)
assert len(T)==46
V=lcm(3960,*(2*m for m in F))
assert all(pow(5,V,q)==1 for q in T)

def fq(b,p):
    return (pow(b,p-1,p*p)-1)//p
assert [p for p in range(27,40,4) if prime(p) and V%p==0]==[31]

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p
def crt(R):
    M=prod(R)
    return sum(r*(M//p)*pow(M//p,-1,p) for p,r in R.items())%M

P=tuple(p for p in range(27,212,4) if prime(p))
assert all(fq(5,p) for p in P)
def repair(n,c,d,I):
    L=23**2
    steps=[]
    for p in P:
        H=[i for i in I if (n-S(c,d+8*i,p))%p==0]
        if H:
            i,=H
            B=lcm(V,L,p-1)
            assert B%p
            r=(n-S(c,d+8*i,p*p))%(p*p)//p
            j=r*pow(pow(5,d+8*i,p)*((pow(5,B,p*p)-1)//p),-1,p)%p
            d+=B*j
            if (n-S(c,d+8*i,p**3))%p**3==0: d+=B*p
            steps.append((p,i,j,(n-S(c,d+8*i,p**3))%p**3//p**2))
        L=lcm(L,p*p*(p-1))
    for i in I:
        for p in P+(23,):
            r=(n-S(c,d+8*i,p**3))%p**3
            assert r%p or (r and r%(p*p)==0)
    return d,steps

J=tuple(range(36))+(39,)
assert min(sum(i%3==a or i%11==b for i in J)
           for a in range(3) for b in range(11))==14
assert min(sum(i%3==a or i%5==b for i in J)
           for a in range(3) for b in range(5))==16
assert pow(5,3,31)==1 and pow(5,22,23)==1
assert fq(5,23)==14 and fq(5,31)==9

# Second target. Replacement saves one center at the same frozen seed.
I=[i for i in J if i%3!=1]
old=[i for i in range(37) if i%3!=1]
p=199
R={q:0 for q in T|set(P)|{3,7,11,19,23}}
del R[p]
R[32]=3
R[p**3]=(S(2,26,p**3)+p)%p**3
n=crt(R)
assert len(I)==25 and R[p**3]==2834946
assert [i for i in old if (n-S(2,2+8*i,p))%p==0]==[3,36]
assert [(n-S(2,2+8*i,p*p))%(p*p) for i in (3,36)]==[p,43*p]
assert [i for i in I if (n-S(2,2+8*i,p))%p==0]==[3]
D,steps=repair(n,2,2,I)
assert steps==[(199,3,15,182)]
assert (n-S(2,D,32))%32==1
assert all((n-S(2,D+8*i,q))%q for i in I for q in (3,7,11,19,23,31,67))
~~~
