# Twenty-five finite-phase centers for the entire even deficient stratum

This closes the even stratum left by the [old-head classification](https://github.com/Samsen879/a303656/commit/15e5ad9178ba84a4efe74abfd1eb5408c9eed2a0): \(n\equiv6\bmod8,\ n\equiv1\bmod3,\ 7\cdot23\mid n\). The theorem includes all residues at 11, 19 and 31 and both branches at 67. It is not a positive-height theorem.

Use the same 25 labels \(I\), now with exponents \(D+8j\). Let \(D_*=135004545787\), \(P=1629320\). The anchors are \(C=66+(3t+w)P,\ D=D_*+(5w+3s)P\), with \(t,w=0,1,2\) and \(s=0,1\), followed by the earlier order-seven, order-eleven and order-five shifts. The seed change \(+50\) and doubled gaps preserve the discarded class at 7 and the unique retained hit \(j=15\) at 23. The \(3P\) vertical fallback multiplies the repeated vertical set at 271 by 106, giving a disjoint set. The old \(12P\) fallback would multiply by 178 and has nonempty intersection. Prefer the unshifted type if any legal horizontal digit passes 271; otherwise use the fallback.

The exact replay gives 458 normalized \(11\cdot31\cdot271\) profiles, 53 minimal ones, and 2014 inclusion-minimal eligibility sets over the two 67 branches. For each such set a single chart or a pair cannot be covered by masks from actual prime residues shared across the charts. The order-eleven forbidden budgets remain 2, 3, 2 at 67, 199, 4159 in the nonzero branch; zero at 67 forces digit zero. Rows 211 and 631 together forbid at most four vertical order-five choices. The previous tie-row restoration applies: the doubled vertical values preserve repetition cardinalities by injectivity of squaring on their odd-order group, and the sensitive restoration maxima are again 2, 2 and 6 at 163, 487 and 47. Their replay is included. Doubling does not enlarge the odd parts of exponent gaps; the same factor certificate limits every common-Wieferich reader to one hit across the retained set.

After the ordinary odd-prime repairs for any prescribed finite panel, take \(K\) as the lcm of \(V/4,\ 23^2\), and \(q^2(q-1)\) for the relevant inert odd panel primes \(q>3\). Then \(v_2(K)=1\). The step preserves the odd readings and every first tie reading, since their base-5 orders divide \(V/4\). The retained exponents agree modulo 8, making all remainders constant modulo 32, and the remainder is 0 modulo 8. The four available \(D+bK\) shifts give all four residues modulo 32 above 0 modulo 8. Select the one giving residue 8, whose valuation at 2 is exactly three and odd part is 1 modulo 4. Therefore all 25 centers pass the ordinary rows of the prescribed finite panel; up to 24 common-Wieferich rows cannot kill all of them.

The displayed controls verify the new fallback at \(382253601814\) where the old doubled fallback failed, and show that at \(1196230\) a paired shift preserving all first tie readings changes \(8\bmod32\) to the failing \(24\bmod32\). The passing controls are both replayed through 271.

~~~python
from collections import Counter
from functools import cache
from itertools import combinations, product
from math import isqrt, lcm

I = [j for j in list(range(0,33,2)) + list(range(-3,36,2))
     if j % 3 != 1 and j != 26]
Q = {43,67,71,127,199,211,271,379,631,4159}
P,E,J,G = 1629320,6284520,3999240,8798328
D,L,V = 135004545787,1569603835800,36100888223400
A = [(66+(3*t+w)*P,D+(5*w+3*s)*P)
     for s,w,t in product(range(2),range(3),range(3))]
FULL = (1<<49)-1

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+8*j,q)) % q for j in I}

def repeated(q):
    return {b for b,k in Counter(pow(5,8*j,q) for j in I).items() if k>1}

B = {q:repeated(q) for q in Q}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*b) % q for b in B[q]}

assert len(I)==25 and V==23*L
assert all(s%(22*23**2)==0 for s in (P,E,G))
assert pow(3,P,7)==pow(5,5*P,7)
assert pow(3,J,23**3)==pow(5,5*J,23**3)
assert pow(5,L,529)==24 and pow(5,V,23**3)==530
assert all(pow(5,L,q)==1 for q in Q|{7,11,19,31})
assert all(s%(q-1)==0 for s in (E,J) for q in (7,11,19,31))
assert all(G%(q-1)==0 for q in (7,19))
assert all(3*P%(q-1)==0 for q in (7,11,31))
assert all(pow(b,G,q)==1 for b in (3,5) for q in Q-{71,211,271,631})
assert all(pow(3,J,q)==pow(5,5*J,q)==1 for q in Q-{67,199,4159})
assert all(pow(b,E,q)==1 for b in (3,5) for q in (67,199,271))
assert all(pow(b,P,67)==1 for b in (3,5))
assert pow(5,E,4159)==pow(5,J,4159)==1
assert pow(5,E,71)==pow(5,5*G,71)==pow(3,5*G,71)==1
assert pow(5,G,271)==pow(5,G,31)==1
assert B[71]=={pow(5,k,71) for k in range(5)}
assert {j%5 for j in I}==set(range(5))
for q in (211,631):
    assert len(B[q])==2 and pow(5,G,q)!=1 and pow(5,5*G,q)==1

assert not B[271] & {106*b%271 for b in B[271]}
assert B[271] & {178*b%271 for b in B[271]} == {1,125,259}
assert (pow(5,3*P,271),pow(5,12*P,271))==(106,178)
B271 = [[bad(271,A[3*w][0]+u*G,A[3*w][1]) for u in range(5)]
        for w in range(6)]
for i,(c,d) in enumerate(A):
    assert 0 not in small(c,d,7)
    assert [j for j in I if (pow(3,c,23)+pow(5,d+8*j,23))%23==0]==[15]
    assert B271[i//3]==[bad(271,c+u*G,d) for u in range(5)]
    for q,cap in [(67,2),(199,3),(4159,2)]:
        for x in range(7 if q==4159 else 1):
            sets = [bad(q,c+x*E+z*J,d+5*z*J) for z in range(11)]
            h = Counter(a for s in sets for a in s)
            assert max(k for a,k in h.items() if a or q!=67)<=cap
            if q==67:
                assert [z for z,s in enumerate(sets) if 0 not in s]==[0]

@cache
def head(a,b):
    out = []
    for w in range(6):
        c,d = A[3*w]
        out.append(tuple(u for u in range(5)
                         if a not in small(c+u*G,d,11)
                         and b not in small(c+u*G,d,31)))
    assert all(out)
    return out

def profile(a,b,r):
    out = [tuple(u for u in s if r not in B271[w][u])
           for w,s in enumerate(head(a,b))]
    return tuple(s if w<3 or not out[w-3] else () for w,s in enumerate(out))

def norm(us):
    return min(tuple(tuple(sorted((u+k)%5 for u in s)) for s in us)
               for k in range(5))

profiles = {norm(profile(a,b,r))
            for a,b,r in product(range(11),range(31),range(271))}
minimal = []
for us in sorted(profiles,key=lambda s:(sum(map(len,s)),s)):
    if not any(all(set(a)>=set(b) for a,b in zip(us,v)) for v in minimal):
        minimal.append(us)
assert (len(profiles),len(minimal))==(458,53)

fixed = {q:[small(c,d,q) if q==19 else bad(q,c,d) for c,d in A]
         for q in (19,199)}

@cache
def mask(i,q,us):
    c,d = A[i]
    out = {}
    for x,y in product(range(7),repeat=2):
        s = (set.intersection(*(bad(71,c+x*E+u*G,d) for u in us))
             if q==71 else bad(q,c+x*E,d+y*E))
        for a in s:
            out[a] = out.get(a,0) | (1<<(7*x+y))
    return out

@cache
def cover(ss,us,zero):
    live = {43,71,127,379} | ({4159} if zero else set())
    rows = []
    for q in live:
        ms = [mask(i,q,u if q==71 else ()) for i,u in zip(ss,us)]
        rows.append(set(tuple(m.get(a,0) for m in ms) for a in range(q)))
    rows.sort(key=lambda h:-max(sum(m.bit_count() for m in z) for z in h))
    lim = [[0]*len(ss) for _ in range(len(rows)+1)]
    for k in reversed(range(len(rows))):
        lim[k] = [lim[k+1][i]+max(z[i].bit_count() for z in rows[k])
                  for i in range(len(ss))]

    @cache
    def visit(k,seen):
        if all(m==FULL for m in seen):
            return True
        if any(m.bit_count()+r<49 for m,r in zip(seen,lim[k])):
            return False
        for z in rows[k]:
            new = tuple(a|b for a,b in zip(seen,z))
            if all(m.bit_count()+r>=49 for m,r in zip(new,lim[k+1])):
                if visit(k+1,new):
                    return True
        return False

    ans = visit(0,(0,)*len(ss))
    visit.cache_clear()
    return ans

total = 0
for zero in (False,True):
    for us in minimal:
        states = {frozenset(i for i in range(18) if us[i//3]
                            and a not in fixed[19][i]
                            and (not zero or b not in fixed[199][i]))
                  for a in range(19) for b in range(199 if zero else 1)}
        least = [s for s in states if not any(r<s for r in states)]
        assert len(least)==(26 if zero else 12)
        for s in least:
            assert any(not cover(z,tuple(us[i//3] for i in z),zero)
                       for k in (1,2) for z in combinations(sorted(s),k))
        total += len(least)
assert total==2014

for q,p in [(163,43991640),(487,131974920)]:
    Z = {pow(3,p*x,q) for x in range(3)}
    Bq = repeated(q)
    assert len(Z)==3 and pow(5,(q-1)//2,q)==q-1
    assert max(max(Counter((a*z+b)%q for z in Z for b in Bq).values())
               for a in range(1,q) if pow(a,(q-1)//2,q)==q-1)==2
q,e = 47,3742200
Z,Bq = {pow(3,e*x,q) for x in range(23)},repeated(q)
assert len(Z)==23 and pow(5,16*e,q)==pow(3,10*e,q)
assert max(max(Counter(v for z in Z for v in
                       {(a*z+b*pow(z,10,q))%q for b in Bq}).values())
           for a in range(1,q))==6
assert len(repeated(31051))==7

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+8*j,q)) % q

K0 = lcm(V//4,529)
assert K0==207580107284550 and K0%4==2 and K0%(22*529)==0
n = 382253601814
assert (n%8,n%3,n%7,n%23,n%11,n%31,n%271,n%19,n%67)==(6,1,0,0,7,26,269,15,1)
for s,i,u in product((0,12),range(9),range(5)):
    c,d = A[i]
    c,d = c+u*G,d+s*P
    assert (7 in small(c,d,11) or 26 in small(c,d,31)
            or 269 in bad(271,c,d) or 15 in small(c,d,19))
c,d = A[10]
assert (c+4*G,d+E+17*L+12*V+K0)==(40081338,667609046892217)

tie = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
       4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
       595123,3981071,5096867,9384251,12207031,16018507,190771747,
       28086211607,386478495679,6090817323763,42272797713043,
       625552508473588471)
assert all(pow(5,K0,q)==1 for q in tie)
assert all(R(1196230,4888026,1100034892482637-2*K0,j,32)==24 for j in I)
panel = [q for q in range(27,272,4) if all(q%k for k in range(2,isqrt(q)+1))]
for n,c,d,last in [(382253601814,40081338,667609046892217,(271,17,108,53)),
                   (1196230,4888026,1100034892482637,(239,32,40,120))]:
    assert all(R(n,c,d,j,32)==8 and
               all(R(n,c,d,j,q) for q in (3,7,11,19,31)) for j in I)
    assert all(sum(R(n,c,d,j,q)==0 for j in I)<=1 for q in tie)
    lock,trace = 529,[]
    for q in panel:
        hits = [j for j in I if R(n,c,d,j,q)==0]
        if hits:
            j, = hits
            e = lcm(V,lock,q-1)
            assert e%q and pow(5,e,q*q)!=1
            k = next(k for k in range(2*q)
                     if R(n,c,d+k*e,j,q*q)==0<R(n,c,d+k*e,j,q**3))
            d += k*e
            trace.append((q,j,k,R(n,c,d,j,q**3)//q**2))
        lock = lcm(lock,q*q*(q-1))
    assert trace[-1]==last and R(n,c,d,15,23**3)==529
    assert all(R(n,c,d,j,32)==8 for j in I)
    assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q)==0<R(n,c,d,j,q**3)
               for j in I for q in panel+[23])
print("Verified", total, "minimal eligibility sets and both finite controls.")
~~~
