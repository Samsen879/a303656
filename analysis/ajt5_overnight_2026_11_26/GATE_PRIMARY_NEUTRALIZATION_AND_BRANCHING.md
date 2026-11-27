# Gate-primary neutralization and a necessary branching condition

**A doubly ordinary gate \(q\) with \(v_q(n)=1\) can be opened against fewer than \(\lceil q/B_q\rceil\) responsive higher rows**, where
\[
B_q=\left\lfloor\frac{1+\sqrt{4q-3}}2\right\rfloor.
\]
The key is that a matching zero-target reader cannot even collide at a first repair point. This gives a necessary branching condition in a divisor-minimal tail modulus without assuming it supplies a full inherited torsion family.

### Preserving the receiving chart

For each base \(a\), let \(d_a\) be the greatest \(q\)-read depth among rows whose powers must be preserved, including the receiving row. Pure \(q\)-primary shifts preserving those powers have indices divisible by \(q^{d_a}\). At a gate of precision \(E\), LTE makes the reachable residuals exactly the lifts of the starting residue modulo
\[
q^\kappa,\qquad \kappa=\min(E,s_3(q)+d_3,s_5(q)+d_5),
\]
where \(s_a(q)=v_q(a^{\operatorname{ord}_q(a)}-1)\). The gate can be repaired with those powers held fixed exactly when the truncated residual passes. Zero lifts to zero, and an odd valuation below \(\kappa\) persists. Any responsive rows still need their own checks. In particular, protecting both first digits locks a doubly ordinary valuation-one gate. [Exact precision closure](https://github.com/Samsen879/a303656/commit/fac27d29f366a0aed19e2ce917577d8084e9166e)

### Why a matching reader is silent on the repair line

Put \(\delta_a=(a^{q-1}-1)/q\bmod q\). Whenever \(3^c+5^d\equiv0\bmod q\), expanding the \((q-1)\)-st powers gives
\[
(3^c+5^d)/q\equiv-3^c(\delta_3c-\delta_5d)\pmod q.
\]
With \(v_q(n)=1\), a first repair \(3^c+5^d\equiv n\bmod q^2\) therefore requires **a nonzero value** of \(\delta_3c-\delta_5d\).

A shallow two-axis reader \(\ell\) with \(n\equiv0\bmod\ell\) can collide only when the \(q\)-primary component of \(-3^c/5^d\bmod\ell\) is trivial. This is a **homogeneous** equation in \(c,d\bmod q\). When the reader’s characters match along the repair slope, its equation is proportional to \(\delta_3c-\delta_5d=0\). Hence it has no collision on the repair line, irrespective of its frozen phase.

The remaining shallow rows hit at most \(B_q\) first points each, using the ordered-difference bound for two nonmatching characters and the one-point bound for the other cases. A first point missed by shallow readers needs at least \(q\) deep readers. Each can veto at most \(1/q\) of its lifts, while the gate’s exact passing fraction exceeds \(1-1/q\) because the even-valuation lifts and zero pass. Thus fewer than \(\lceil q/B_q\rceil\) responsive rows leave an exact repair. [Branching charge](https://github.com/Samsen879/a303656/commit/66b0b68c6f3fa63601d890dbb43442b6be45885e)

This applies directly in a **divisor-minimal tail modulus**. Lower an essential \(q^E\) by one to obtain a witness passing every other row, with residual valuation \(E-1\) at \(q\). Open both \(q\)-primary axes from that witness. Nonreaders stay passing, so the bound forces at least \(\lceil q/B_q\rceil\) distinct active higher primes on this opening. For \(q=379\), that is **20**. A receiving row whose powers are released is one of those readers, counted once. The bound uses \(v_q(n)=1\), and moving \(c\) at small exponents still requires a separate ternary check.

### Exact controls

- **Protected receiver, silent readback.** Extend the real \(7\to7603\) chart by row \(5628151\). At one fixed target all seven inherited phases initially veto at both 379 and \(5628151\). Opening 379 preserves the receiving powers at \(7603^2\), repairs all seven at \(379^2\), and makes \(5628151\) a unit on each repair. Then 7603 can be opened independently.
- **Locked receiver, live readback.** In the real \(7,43,458123\) panel, preserving the two powers at \(7^2\) and \(458123^2\) fixes the full orders at \(43^2\). All seven gate vetoes are locked. Releasing 458123 allows all seven gate repairs. At the same target it still vetoes one selected mixed repair, with exact residual \(458123\bmod458123^2\).

```python
from math import gcd, lcm

def r(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def crt(a,m,b,n):
    g=gcd(m,n)
    assert (b-a)%g==0
    return a+m*((b-a)//g*pow(m//g,-1,n//g)%(n//g))

def step(n,c,d,L,q):
    z=r(n,c,d,q*q)
    A=pow(5,d,q)*((pow(5,L,q*q)-1)//q)%q
    assert z%q==0 and A
    return L*(z//q*pow(A,-1,q)%q)

q,R,H=379,7603,5628151
F=(H-1)*H
n=crt(162032070120662,49*q*q*R*R,H,H*H)
c=crt(295723497699,lcm(42,378*q,(R-1)*R),F//2,F)
P=lcm(6,54*q,1086*R,F)
L=lcm(42,378,(R-1)*R,F//q)
J=lcm(42,378*q,R-1,F)
assert pow(3,L,H)==pow(5,342*L,H)!=1
assert all(pow(a,L,R*R)==1 for a in (3,5))
for t in range(7):
    C,D=c+P*t,P*t
    assert [r(n,C,D,m) for m in (49,q*q,R*R,H*H)]==[0,q,R,H]
    D+=step(n,C,D,L,q)
    assert r(n,C,D,q*q)==0 and r(n,C,D,H)!=0
    D+=step(n,C,D,J,R)
    assert all(r(n,C,D,m)==0 for m in (49,q*q,R*R))
    assert r(n,C,D,H)!=0

q,R=43,458123
n,c,d=6524646325572475,4,203637600769
L=lcm(42,(R-1)*R//q)
assert all(lcm(42,w*R)%(42*q)==0 for w in ((R-1)//2,R-1))
assert [r(n,c,d,m) for m in (49,q*q,R*R)]==[0,q,R]
D=d+step(n,c,d,L,q)
assert r(n,c,D,49)==r(n,c,D,q*q)==0 and r(n,c,D,R)!=0
assert r(n,c+40*L,d+8*L,q*q)==0
assert r(n,c+40*L,d+8*L,R*R)==R
print("PASS")
```

In the homogeneous collision argument, project the quotient of the two nonzero base powers onto the order-\(q\) subgroup at a shallow reader; the sign has trivial projection since \(q\) is odd. This tests the actual exponents modulo \(q\), not coordinates translated relative to an arbitrary origin. The parent condition has a nonzero intercept because \(n/q\) is nonzero modulo \(q\) and \(3^c\bmod q\) is fixed and nonzero. In the divisor-minimal application, lower rows and higher rows with no \(q\)-primary read stay passing at the witness. The count is for higher primes which can veto on the opened repair set, and makes no assertion that any such modulus exists.
