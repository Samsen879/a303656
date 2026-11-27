# Even-D 25-center finite-phase menu: both non-1 target residues modulo 3

This is a finite-panel continuation of [the mixed-axis catalogue and conditional restorations](https://github.com/Samsen879/a303656/commit/28240deae8c34b7ef71da45ee4c95d1f15bd0fbf). The gap catalogue, common-Wieferich non-reuse and generic tie/ordinary lifting lemmas are inherited from those results. The new finite mask enumeration was independently rerun with different bit-mask code: all six profile triples, 2,976 minimal eligibility tests, the 84 anchors and the maximum exclusion of ten were reproduced. An independent modular replay also checked both same-target controls through the complete stated panel. No positive norm in the ordinary height box, natural-density upgrade, or solution of Sun's conjecture is claimed.

**Every target \(n>1\) with \(n\bmod3\in\{0,2\}\) now has 25-center finite-phase coverage.** In particular, this covers all 176 requested classes mod \(552\) with \(n\equiv2\bmod3\) and \(23\nmid n\), including all eight residues mod \(8\). The proof also covers \(23\mid n\). There is no restriction on \(n\bmod7,11,19,31\).

### Two even-\(D\) menus

Keep the 25 retained labels \(I\) and offsets \(D+8j\). Write
\[
P=1629320,\quad E=6284520,\quad J=3999240,\quad G=8798328,
\quad H=5498955.
\]
Use the anchors
\[
(C,D)=\bigl(66+\epsilon H+(3t+w)P,\ 
135010044742+(5w+3s+\delta_w)P\bigr),
\]
where \(t,w\in\{0,1,2\}\), \(s\in\{0,1\}\), and \(\epsilon\) is the chosen parity of \(C\). The digits add \(xE+uG+zJ\) to \(C\) and \(yE+vG+hJ\) to \(D\). The order-eleven digits \(z,h\) are independent.

- For **odd \(C\)**, use \(\delta=(0,0,0)\), except at \((n_7,n_{19})=(1,0),(3,0)\). At either exception use \(\delta=(0,2,1)\) and keep \(w=1,2\). In the unshifted menu, \(7\) blocks \(w=0\) and \(19\) blocks every anchor of \(w=1,2\). The targeted shift clears both rows on the two retained types.
- For **even \(C\)**, use the following \(\delta\)-table. It makes \(7\) a unit on every retained center, before the chart selection.

| \(n\bmod7\) | \(\delta\) |
|---|---|
| \(0,1,2,4\) | \((0,0,0)\) |
| \(3\) | \((2,1,0)\) |
| \(5\) | \((1,0,2)\) |
| \(6\) | \((0,2,1)\) |

The \(11,31\) head is tested against the actual target residues. Within each \(w,u\), the two \(s\)-choices have disjoint repeated-value sets at \(271\). After this selection, the exact certificate checks **2,976 inclusion-minimal eligibility sets** across the six menu cases. Each has one or two eligible charts that cannot be jointly covered by actual residues at \(43,71,127,379\). The last vertical digit clears \(211,631\) at a combined cost of at most four of the five choices.

For the order-eleven step, fix an anchor and its order-seven horizontal digit. For each horizontal \(z\), combine the forbidden vertical masks from \(67,199\). Mark \(z\) only if their union covers all eleven vertical choices. Add the horizontal masks at \(23,4159\). The exact maximum of this union is **ten**, over all actual residues and all \(84\cdot7\) anchor and horizontal-digit inputs. A legal pair \((z,h)\) therefore remains. At \(23\), both powers are squares because \(D\) is even and \(3\) has order eleven. When \(n\equiv0\bmod23\), this row contributes the empty mask since \(-1\) is a nonsquare.

### Restoration and the exact \(2\)-adic lift

The gap catalogue and generic tie restoration are unchanged. The doubled repeated-value sets at \(163,487\) forbid at most two order-three digits for **every** nonzero horizontal-to-vertical ratio, so the restoration works with either parity of \(C\). With \(23\) a unit at all centers, the horizontal line at \(47,31051\) still costs at most \(5+7\) of its 23 digits. Ordinary repair then applies to any prescribed finite panel.

Choose \(C\) odd at \(n\bmod8\in\{0,1,4,5,6\}\), and even at \(n\bmod8\in\{2,3,7\}\). After the odd-prime repairs, the vertical period of \(2\)-adic valuation one gives these exact common remainders:

| \(n\bmod8\) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| \(R_j\bmod32\) | 4 | 5 | 8 | 1 | 8 | 1 | 2 | 5 |

All have odd part \(1\bmod4\). The anchors start positive and every lift is nonnegative. In particular the unit test at \(3\) uses \(C>0\) directly. When \(n\equiv2\bmod3\) and \(D\) is even, \(C=0\) instead gives a multiple of \(3\), so it cannot be substituted into this guard.

### Exact controls

- **\(3901745\)** is in the forced odd-\(C\) case and has \((n_7,n_{19})=(1,0)\). Every unshifted odd-\(C\) anchor fails at \(7\) or \(19\). The targeted shift gives \((C,D)=(19925909,415295264013762)\). All 25 remainders are \(5\bmod32\) and units at \(23\). The ordinary panel through \(271\) passes, with the last repair at \(j=9\) giving \(149\cdot271^2\bmod271^3\).
- **\(218018\)** is in the forced even-\(C\) case for this menu. Every odd-\(C\), even-\(D\) seed has remainder \(6\bmod8\). The even-\(C\) choice \((13775226,207715126872452)\) gives all 25 remainders \(8\bmod32\) and units at \(23\). The ordinary panel through \(271\) passes after repairs at \(43,47,59\).

The common-Wieferich non-reuse bound is unchanged because the exponent gaps are unchanged. These are finite-phase certificates.

### Replay

This checks the six menu cases, the exact local mask bound, the restoration capacities, and both ordinary panels. It uses the unchanged tie-prime catalogue.

```python
from collections import Counter
from functools import cache
from itertools import combinations, product
from math import isqrt, lcm

I = [j for j in list(range(0,33,2))+list(range(-3,36,2))
     if j%3 != 1 and j != 26]
P,E,J,G,H = 1629320,6284520,3999240,8798328,5498955
D,V = 135010044742,36100888223400
Q = {43,67,71,127,199,211,271,379,631,4159}
FULL = (1<<49)-1

def small(c,d,q):
    return {(pow(3,c,q)+pow(5,d+8*j,q))%q for j in I}

B = {q:{a for a,k in Counter(pow(5,8*j,q) for j in I).items() if k>1}
     for q in Q|{47,163,487,31051}}

def bad(q,c,d):
    return {(pow(3,c,q)+pow(5,d,q)*a)%q for a in B[q]}

assert len(I)==25 and {j%5 for j in I}==set(range(5))
assert {j%11 for j in I}==set(range(11))
assert all(k%(q-1)==0 for q in (7,11,19,31) for k in (E,J))
assert all(G%(q-1)==0 for q in (7,19))
assert all(3*P%(q-1)==0 for q in (7,11,31))
assert all(pow(b,G,q)==1 for q in Q-{71,211,271,631} for b in (3,5))
assert all(pow(b,J,q)==1 for q in Q-{67,199,4159} for b in (3,5))
assert all(pow(b,E,q)==1 for q in (67,199,271) for b in (3,5))
assert pow(5,G,31)==pow(5,E,71)==pow(5,E,4159)==pow(5,J,4159)==1
assert pow(5,5*G,71)==pow(3,5*G,71)==pow(5,G,271)==1
assert pow(3,J,23)!=1 and pow(3,11*J,23)==pow(5,11*J,23)==1
assert B[71]=={pow(5,k,71) for k in range(5)}
assert not B[271]&{b*pow(5,3*P,271)%271 for b in B[271]}
for q in (211,631):
    assert len(B[q])==2 and pow(5,G,q)!=1 and pow(5,5*G,q)==1

def anchor(e,delta,i):
    w = i//3%3
    return 66+e*H+(3*(i%3)+w)*P, D+(5*w+3*(i//9)+delta[w])*P

def norm(us):
    return min(tuple(tuple(sorted((u+k)%5 for u in s)) for s in us)
               for k in range(5))

def cert(e,delta,heads,only,want):
    A = [anchor(e,delta,i) for i in range(18)]
    B271 = [[bad(271,A[3*w][0]+u*G,A[3*w][1]) for u in range(5)]
            for w in range(6)]
    for i,(c,d) in enumerate(A):
        assert B271[i//3]==[bad(271,c+u*G,d) for u in range(5)]

    @cache
    def head(a,b):
        return tuple(tuple(u for u in range(5)
                           if a not in small(c+u*G,d,11)
                           and b not in small(c+u*G,d,31))
                     if w%3 in only else ()
                     for w,(c,d) in enumerate(A[::3]))

    def profile(a,b,r):
        us = [tuple(u for u in s if r not in B271[w][u])
              for w,s in enumerate(head(a,b))]
        return tuple(s if w<3 or not us[w-3] else () for w,s in enumerate(us))

    profiles = {norm(profile(a,b,r))
                for a,b,r in product(range(11),range(31),range(271))}
    minimal = []
    for us in sorted(profiles,key=lambda p:(sum(map(len,p)),p)):
        if not any(all(set(a)>=set(b) for a,b in zip(us,v)) for v in minimal):
            minimal.append(us)
    fixed = {q:[small(c,d,q) for c,d in A] for q in (7,19)}

    @cache
    def mask(i,q,us):
        c,d = A[i]
        out = {}
        for x,y in product(range(7),repeat=2):
            h = (set.intersection(*(bad(71,c+x*E+u*G,d) for u in us))
                 if q==71 else bad(q,c+x*E,d+y*E))
            for a in h:
                out[a] = out.get(a,0)|(1<<(7*x+y))
        return out

    @cache
    def cover(ss,us):
        rows = []
        for q in (43,71,127,379):
            ms = [mask(i,q,u if q==71 else ()) for i,u in zip(ss,us)]
            rows.append({tuple(m.get(a,0) for m in ms) for a in range(q)})
        rows.sort(key=lambda h:-max(sum(m.bit_count() for m in z) for z in h))
        lim = [[0]*len(ss) for _ in range(5)]
        for k in reversed(range(4)):
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
    for us in minimal:
        states = {frozenset(i for i in range(18) if us[i//3]
                            and a not in fixed[7][i] and b not in fixed[19][i])
                  for a,b in heads}
        for s in states:
            if any(r<s for r in states):
                continue
            assert any(not cover(z,tuple(us[i//3] for i in z))
                       for k in (1,2) for z in combinations(sorted(s),k))
            total += 1
    assert (len(profiles),len(minimal),total)==want
    return [a for i,a in enumerate(A) if i//3%3 in only]

exc = {(1,0),(3,0)}
heads = set(product(range(7),range(19)))
anchors = set(cert(1,(0,0,0),heads-exc,{0,1,2},(403,50,950)))
anchors.update(cert(1,(0,2,1),exc,{1,2},(124,9,9)))
for delta,a7,want in [
    ((0,0,0),(0,1,2,4),(458,53,636)),
    ((0,2,1),(6,),(441,41,357)),
    ((1,0,2),(5,),(459,40,340)),
    ((2,1,0),(3,),(434,40,684)),
]:
    anchors.update(cert(0,delta,list(product(a7,range(19))),{0,1,2},want))
assert len(anchors)==84

H23 = {pow(3,j,23) for j in range(11)}
def reads(q,c,d):
    rows = [[0]*11 for _ in range(q)]
    for z,h in product(range(11),repeat=2):
        for a in bad(q,c+z*J,d+h*J):
            rows[a][z] |= 1<<h
    return rows

for c,d in anchors:
    p,q = reads(67,c,d),reads(199,c,d)
    dead = {sum(1<<z for z in range(11) if a[z]|b[z]==2047)
            for a in p for b in q}
    h23 = {sum(1<<z for z in range(11) if (a-pow(3,c+z*J,23))%23 in H23)
           for a in range(23)}
    for x in range(7):
        h4159 = Counter()
        for z in range(11):
            for a in bad(4159,c+x*E+z*J,d):
                h4159[a] |= 1<<z
        assert max((a|b|h).bit_count()
                   for a in dead for b in h23 for h in set(h4159.values())|{0})<=10

for q,p in [(163,43991640),(487,131974920)]:
    Z = {pow(3,p*x,q) for x in range(3)}
    assert len(Z)==3
    assert max(max(Counter((a*z+b)%q for z in Z for b in B[q]).values())
               for a in range(1,q))==2
for q,k in ((47,5),(31051,7)):
    assert len(B[q])==k and len({pow(3,3742200*x,q) for x in range(23)})==23
assert 3742200%22==0

def R(n,c,d,j,q):
    return (n-pow(3,c,q)-pow(5,d+8*j,q))%q

n = 3901745
assert (n%8,n%3,n%7,n%19,n%23,n%67)==(1,2,1,0,2,0)
assert all(n%7 in small(*anchor(1,(0,0,0),i),7)
           or n%19 in small(*anchor(1,(0,0,0),i),19) for i in range(18))
K = lcm(V//4,529)
assert K%4==2
c,d = anchor(1,(0,2,1),3)
assert (c+G+J,d+7*J+2*K)==(19925909,415295264013762)
c,d = anchor(0,(2,1,0),2)
assert (c+J,d+E+K)==(13775226,207715126872452)
assert all(R(218018,19925909,415295264013762,j,8)==6 for j in I)

tie = (31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
       4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
       595123,3981071,5096867,9384251,12207031,16018507,190771747,
       28086211607,386478495679,6090817323763,42272797713043,
       625552508473588471)
assert all(pow(5,K,q)==1 for q in set(tie)|{7,11,19,23,31})
panel = [q for q in range(27,272,4) if all(q%k for k in range(2,isqrt(q)+1))]
for n,c,d,r,last in [
    (3901745,19925909,415295264013762,5,(271,9,208,149)),
    (218018,13775226,207715126872452,8,(59,-3,46,32)),
]:
    assert all(R(n,c,d,j,32)==r and all(R(n,c,d,j,p) for p in (3,7,11,19,23,31))
               for j in I)
    assert all(sum(R(n,c,d,j,q)==0 for j in I)<=1 for q in tie)
    lock,trace = 529,[]
    for q in panel:
        hits = [j for j in I if not R(n,c,d,j,q)]
        if hits:
            j, = hits
            e = lcm(V,lock,q-1)
            assert e%q and pow(5,e,q*q)!=1
            x = next(x for x in range(2*q)
                     if R(n,c,d+x*e,j,q*q)==0<R(n,c,d+x*e,j,q**3))
            d += x*e
            trace.append((q,j,x,R(n,c,d,j,q**3)//q**2))
        lock = lcm(lock,q*q*(q-1))
    assert trace[-1]==last
    assert all(R(n,c,d,j,32)==r and R(n,c,d,j,23) for j in I)
    assert all(R(n,c,d,j,q) or R(n,c,d,j,q*q)==0<R(n,c,d,j,q**3)
               for j in I for q in panel)
    print(n,trace)
```
