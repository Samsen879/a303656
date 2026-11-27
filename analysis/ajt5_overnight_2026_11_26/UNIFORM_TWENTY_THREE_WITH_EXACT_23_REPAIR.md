# Twenty-three uniform centers with exact repair at the 23 row

**The same 37 offsets give twenty-three centers uniformly if the small-head test at \(23\) accepts exact valuation two.** The construction keeps one seed and the existing separate-axis locks. The strict unit-at-\(23\) version also reaches twenty-three whenever \(23\nmid n\) or \(n\not\equiv1\bmod3\). The remaining strict-unit case is unresolved here.

### Keep one more index at the head

Start with the previous 25 candidates. Use the same joint steering at \(23,67,199\), giving priority to clearing \(23\) whenever some \(C\)-choice does so.

In the generic head, send the forbidden class at \(23,67\) to \(5\) or \(9\bmod11\). Delete **only index \(27\)** for class \(5\), or **only index \(9\)** for class \(9\). This leaves at most one hit at each of \(23,67\), retains 24 candidates, and still breaks the endpoint pair needed for the \(271,379,4159\) step. The \(199\) test cannot veto both choices: their forbidden head classes differ by \(4\bmod11\), whereas the repeated representatives at \(199\) lie in \(0,\ldots,3\). This argument works even when testing \(199\) on all 25 candidates.

In the exceptional head, omit \(9\) before trimming to 25, as before. Choose an admissible head class containing at most two candidates and retain one of them. The seven-phase bound of one deletion applies unchanged, and the ternary step still clears all three rows. The later steering bounds use at most 12 repeated classes per row for 24 candidates. At the nineteen-phase step this changes the zero-row survivor lower bound to \(19(19-12)=133\), still larger than \(6\cdot12=72\) nonzero companion exclusions. If both readings are nonzero their caps remove at most \((6+2)12<19^2\); if both are zero their slopes are independent. The seven-phase bounds depend only on the available residue representatives, not on rounding the number of candidates down to 23. For each remaining group from the [twenty-center constructor](https://github.com/Samsen879/a303656/blob/a00176489cff6c1882530aaac183d3ec12a0f720/analysis/ajt5_overnight_2026_11_26/UNIFORM_TWENTY_CENTER_CERTIFICATE.md), recompute its budget with \(\min(12,h,37-h)\); each directional order still exceeds the group budget, including after augmenting the period by \(23^2\) at the 47/31051 stage. In particular, the \(47,31051\) group has at most \(12+10=22\) exclusions and 23 choices when \(23\) is already a unit.

### Repair \(23\) while protecting \(47\) and \(31051\)

A retained hit at \(23\) occurs only when \(n\equiv0\bmod23\) and \(D\) is odd. For a nonzero observation, the translate of the \(3\)-coset cannot equal the \(5\)-coset, since both cosets sum to zero. Thus some \(C\)-choice clears \(23\) outright. At zero with \(D\) even, both powers are squares and their sum is a unit.

At the \(47,31051\) stage the existing period is
\[
K=19286363250,\qquad 22\mid K,\quad 23\nmid K.
\]
Both increments \(Kx,Ky\) preserve every reading already fixed. For the singleton hit at \(23\), the first-digit equation is
\[
y=16x+t\pmod{23}.
\]
Indeed, the Fermat quotients of \(3,5\) at \(23\) are \(17,14\), their ratio is \(16\), and the two powers at the hit are negatives of each other modulo \(23\).

At \(47\), \(3^K=(5^K)^{20}\). Along the repair line, the two moving factors therefore have the form \(X,X^{10}\) over the order-23 subgroup. The replay checks that at most **six** \(x\)-choices create a repeated hit at \(47\), for any target and any initial scales. At \(31051\), the \(D\)-move is invisible and at most ten repeated classes can veto an \(x\). Thus at least seven of the 23 first-digit choices clear both rows.

If necessary, add \(23K\) to \(D\) to make the valuation exactly two. This preserves both newly protected readings. Include \(23^2K\) in the subsequent \(C\)-period and \(23^2\) in both ordinary repair locks. The singleton at \(67\) can then be repaired on base \(5\) in the usual way.

This gives \(24-1=23\) centers. **Non-reuse still holds within that one selected menu.** A genuine common-Wieferich reader hitting two offsets would have its square divide \(5^{2m}-1\) for some odd \(m\le35\), which the unchanged squarefree certificate excludes.

### Same-target control

Take \(C=22,D=631\) and retain the indices \(i\not\equiv1\bmod3\) other than \(27\). The CRT target below has a singleton at index \(5\) at both \(23\) and \(67\).

- **Failed repair:** \((x,y)=(0,2)\) gives exact valuation two at \(23\), but ties indices \(0,23\) at \(47\). Their first readings are \(22,45\bmod47\), so a common repair cannot save both.
- **Coupled repair:** \((x,y)=(1,18)\) gives remainder \(20\cdot23^2\bmod23^3\) and makes \(47\) a unit at every retained index. The later repair gives \(21\cdot67^2\bmod67^3\) and preserves the \(23^3\) reading.

The result is finite-phase. The control can be lifted to positive remainders, but there is no ordinary exponent-height bound for the input target.

```python
from math import isqrt, lcm, prod

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p)) % p

def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

K=lcm(187110*19,6510,434,519498,125)
assert K==19286363250 and K%22==0 and K%23
locked=(7,11,19,23,31,67,199,71,43,127,211,631,
        271,379,4159,163,487,191,6271,19531,1303,519499,251)
assert all(pow(b,K,p)==1 for b in (3,5) for p in locked)
f=[(pow(b,22,23**2)-1)//23 for b in (3,5)]
assert f==[17,14] and f[0]*pow(f[1],-1,23)%23==16
assert pow(3,2,47)==pow(5,40,47) and 20*10%23==16
assert pow(5,K,31051)==1 and pow(3,K,31051)!=1
assert pow(3,23*K,31051)==1 and pow(5,23*K,47)==1

rare={i for i in range(37) if all(S(89,89+8*i,p)!=r
      for p,r in ((7,2),(19,0),(11,8),(31,27)))}
def pairs(I,m):
    return {i for i in range(37-m) if i in I and i+m in I}

head={i for i in range(37) if i%3!=1}
R0={0,3,6,9,12}
R1=pairs(rare,23)
assert R1=={2,4,7,9,11,12}
assert all(pairs(head-{e},23)<=R0 for e in (9,27))
H={pow(x,2,47) for x in range(1,47)}
def cap(R):
    W={pow(5,8*i,47) for i in R}
    return max(sum((n-x)*pow(b*pow(x,10,47),-1,47)%47 in W
                   for x in H) for b in range(1,47) for n in range(47))
assert cap(R0)==cap(R1)==6

c,d=22,631
I=sorted(head-{27})
assert len(I)==24
assert all([i for i in I if S(c,d+8*i,p)==0]==[5] for p in (23,67))
n23=(S(c,d+40,23**3)+23)%23**3
beta=(pow(5,K,23**2)-1)//23
t=pow(pow(5,d+40,23)*beta,-1,23)
badD=d+K*t
n47=S(c,badD,47)
assert (n23,t,n47)==(7521,2,10)
assert [i for i in I if S(c,badD+8*i,47)==n47]==[0,23]
assert (n23-S(c,badD+40,23**3))%23**3==17*23**2

C,D=c+K,d+18*K
assert (16+t)%23==18
assert (n23-S(C,D+40,23**3))%23**3==20*23**2
assert all(S(C,D+8*i,47)!=n47 for i in I)

T={31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,4159,
   5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,595123,3981071,
   5096867,9384251,12207031,16018507,190771747,28086211607,386478495679,
   6090817323763,42272797713043,625552508473588471}
P=tuple(q for q in range(27,68,4) if prime(q))
V=lcm(3960,*range(2,71,4))
assert all(pow(5,V,q)==1 for q in T)
R=[(32,(S(C,D,32)+1)%32),(3,1),(23**3,n23),(47,n47),(67**3,15678)]
for q in (T|{7,11,19}|set(P))-{47,67}:
    forbidden={S(C,D+8*i,q) for i in I}
    R.append((q,next(r for r in range(q) if r not in forbidden)))
M=prod(q for q,r in R)
n=sum(r*(M//q)*pow(M//q,-1,q) for q,r in R)%M

B=lcm(23**2,V,66,*(q*q*(q-1) for q in P if q<67))
D+=B
assert (n-S(C,D+40,67**3))%67**3==21*67**2
assert (n-S(C,D+40,23**3))%23**3==20*23**2
assert (n-S(C,D,32))%32==1
assert [(n-S(c,badD+8*i,47**2))%(47**2)
        for i in (0,23)]==[22*47,45*47]
for i in I:
    assert all((n-S(C,D+8*i,q))%q for q in (3,7,11,19,31))
    for q in P+(23,):
        r=(n-S(C,D+8*i,q**3))%q**3
        assert r%q or (r and r%(q*q)==0)
```

This remains a **finite-phase** bound. It gives no ordinary exponent-height bound for the input \(n\).
