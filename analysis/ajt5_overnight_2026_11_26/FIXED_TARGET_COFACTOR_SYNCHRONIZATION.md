# Fixed-target synchronization by auxiliary cofactor movement

**Yes, on the fixed target from the previous replay.** Moving \(c_{653}\) alone makes both genuine exceptional guards forbid \(d_{31}=6\), but they still require different complementary \(c_{31}\) labels. Moving both axes at \(653\) makes the same actual pair \((c,d)\) have exact valuation \(1\) at both guards. The target stays unchanged. For this pair of primes, \(653\) is a globally chosen coordinate read by one guard; **no second primary coordinate is read by both guards**. [Full-component baseline](https://github.com/Samsen879/a303656/blob/d5227b2f92a3a1d942bb8145c6b4ff035d537248/analysis/ajt5_overnight_2026_11_26/FULL_COMPONENT_GUARD_OVERLAP.md)

### Transferable test

After the other cofactor digits are locked, write the two powers at guard \(p\) as
\[
3^c=A_p U_p^a g_p^{\tau_p i},\qquad
5^d=B_p V_p^b g_p^j\pmod p.
\]
Here \(i=c_r,\ j=d_r\), \(g_p\) has order \(r\), \(\tau_p\) is the actual base-\(3\)-to-base-\(5\) log slope, and \(a,b\) are the movable auxiliary coordinates on the two axes. Use \(U_p=1\) or \(V_p=1\) when that axis does not read the auxiliary coordinate.

For fixed \(j,b\), set \(T_p=(N-B_pV_p^b g_p^j)/A_p\bmod p\). If \(T_p=0\), it cannot be a \(3\)-power. Otherwise the test has two steps:

1. Solve \(T_p^r=(U_p^r)^a\) at each guard. These are congruences for the **same** \(a\), modulo the actual orders of \(U_p\). They must be compatible with each other and with the prelocks. This certifies a shared forbidden \(d_r\) label.
2. The complementary \(c_r\) label is \(\tau_p^{-1}\log_{g_p}(T_p/U_p^a)\). These labels must also agree to obtain one common pair \((c,d)\).

For a nonzero target, staying in the diagonal branch \(N/2\in A_pH_p=B_pH_p\) pins every auxiliary digit read in that quotient: the coset containing \(N/2\) is unique. The successful move below leaves that branch. At a **zero target modulo \(p\)**, fixed cosets give all labels forbidden if they are opposite, and none otherwise. The nonzero-target singleton argument does not apply.

### Fixed-target control

Keep the original disjoint target throughout:
\[
N=10+9752781853725239220214221361^2+
11075246640031221347570696376^2.
\]
The guards are \(p=20771,\ q=40487\), with actual \((o_3,o_5)\) equal to \((335\cdot31,335\cdot31)\) and \((653\cdot31,1306\cdot31)\). Their slopes are \(6,7\). The original locks are \(c\equiv0\bmod14437830\), \(d\equiv0\bmod1312530\), with forbidden sets \(\{6\}\), \(\{7\}\). In the moves below, **only the indicated residues modulo \(653\) change**. The other prime-power locks stay fixed.

| Move | Full forbidden \(d_{31}\) sets | Complementary \(c_{31}\) at \(d_{31}=6\) |
|---|---|---|
| \(c_{653}=172,\ d_{653}=0\) | \(\{6\},\{6\}\) | \(1,7\) |
| \(c_{653}=35,\ d_{653}=407\) | \(\{6\},\{6\}\) | \(1,1\) |

For the first move, at \(q\) the complement is \(T=27952\), the normalized \(c_{653}\) generator is \(U=16648\), and \(T^{31}=(U^{31})^{172}=4041\bmod q\). Since \(U^{31}\) has order \(653\), **172 is the unique move of this kind**. After division by \(U^{172}\), the complement is \(6073=(3\text{-primary generator})^7\bmod q\). Thus changing only \(c_{653}\) can align the forbidden label, but cannot align the complementary label there.

After moving both axes, the common hard pair is
\[
(c,d)=(167439030,\ 17207610).
\]
Both guards satisfy \(5^{p-1}\equiv1\bmod p^2\). The two residues are \(17629\cdot20771\bmod20771^2\) and \(7330\cdot40487\bmod40487^2\), so both valuations are exactly \(1\). This is a simultaneous hard pair on a target fixed before the moves. It is separate from the **ordinary** lift at \(31\): at a safe \(d_{31}=1\), the same cofactor locks leave \(c_{31}\) available, and the replay checks a lift from valuation \(1\) to \(2\). The actual short square representation of \(N\) remains \(c=2,d=0\).

```python
from math import gcd, isqrt
N=10+9752781853725239220214221361**2+11075246640031221347570696376**2
r,s,p,q=31,653,20771,40487
Mc,Md=14437830,1312530
def phase(M,a,i):
    L=M//s
    v=L*(a*pow(L,-1,s)%s)
    return v+M*((i-v)*pow(M,-1,r)%r)
for z,oa,ob in ((p,335*r,335*r),(q,s*r,2*s*r)):
    assert all(z%j for j in range(2,isqrt(z)+1))
    for b,o in ((3,oa),(5,ob)):
        assert pow(b,o,z)==1 and all(pow(b,o//l,z)!=1 for l in (2,5,31,67,653) if o%l==0)
    assert pow(5,z-1,z*z)==1 and pow(3,z-1,z*z)!=1
def rem(c,d,m): return (N-pow(3,c,m)-pow(5,d,m))%m
for a,b,W in ((0,0,[[(1,6)],[(1,7)]]),(172,0,[[(1,6)],[(7,6)]]),(35,407,[[(1,6)],[(1,6)]])):
    assert [[(i,j) for i in range(r) for j in range(r)
             if not rem(phase(Mc,a,i),phase(Md,b,j),z)] for z in (p,q)]==W
T=(N-pow(5,phase(Md,0,6),q))%q
U=pow(3,phase(Mc,1,0),q)
assert (T,U)==(27952,16648) and [a for a in range(s) if pow(T,r,q)==pow(U,r*a,q)]==[172]
c,d=167439030,17207610
assert c%(Mc//s)==d%(Md//s)==0 and (c%s,d%s,c%r,d%r)==(35,407,1,6)
assert rem(c,d,p*p)==17629*p and rem(c,d,q*q)==7330*q
d=phase(Md,407,1)
c0=phase(Mc,35,0)
assert rem(c0,d,r*r) in range(r,r*r,r)
c=c0+Mc*next(i for i in range(r*r) if rem(c0+Mc*i,d,r**3)==r*r)
assert all(rem(c,d,z) for z in (p,q))
print("OK")
```

The auxiliary prime is distinct from the shared primary prime. This supplies a fixed-target mechanism only when the stated cofactor moves remain available; it does not show an all-exponent blocker or a uniform overlap saving.
