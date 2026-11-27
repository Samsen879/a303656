# Fixed-axis finite kernel and a three-exception exclusion

**A finite all-exponent blocker must retain an additional hard base-5 exceptional prime on every viable fixed-\(c\) channel.** The three archived primes \(20771,40487,1645333507\), even with arbitrarily many ordinary rows, cannot block any fixed \(c=C\) for which \(N-3^C\not\equiv0\pmod4\). The additional prime may vary with \(C\). This follows from an exact reduction that preserves ordinary repairs. [Prior private-source result](https://github.com/Samsen879/a303656/blob/6e89d414219cb58645eb670780e27bc039fb5155/analysis/ajt5_overnight_2026_11_26/PRIVATE_SOURCE_FIXED_AXIS_DISJOINTNESS.md)

### The finite kernel

Fix \(N,C\), and let \(S\) be the odd inert primes in a finite panel. Write \(A=N-3^C\), \(o_p=\operatorname{ord}_p(5)\), and \(w_p=v_p(5^{o_p}-1)\). Call a row *hard* if its unique collision class \(d\equiv e_p\pmod{o_p}\) has odd residual valuation below \(w_p\). The class exists only if \(A\bmod p\) lies in \(\langle5\rangle\). A row with no hard class can be repaired on its own \(p\)-primary coordinate whenever that coordinate is unread.

Retain all hard rows. Then whenever a retained row \(p\) has \(r\mid o_p\) with \(r\in S\), retain row \(r\) as well. Repeat to closure. **The retained panel, together with the \(2\)-adic condition, is feasible exactly when the original panel is feasible.** Starting with a solution for the retained rows, repair discarded rows in increasing prime order. Changing the \(r\)-primary coordinate preserves every retained row, by closure, and every smaller row, because its foreign order factors are smaller than its own prime. A collision at a discarded row either already has a certified even valuation or can be lifted to one.

The retained problem itself is finite. With \(L=\operatorname{lcm}(2,o_p:p\text{ retained})\), test \(d\bmod L\) at row \(p\) to depth \(w_p+v_p(L)\). A zero at that depth can be lifted to an exact even valuation using the unread tail. At \(2\), only parity is read by the inert orders. Both parities extend when \(A\equiv1,2\pmod4\), one extends when \(A\equiv3\pmod4\), and neither extends when \(A\equiv0\pmod4\). In particular, every \(N\) has a channel among \(C=0,1\) with both parities available.

### What has to remain after peeling

Suppose \(q\) is the first row that blocks a viable fixed-\(C\) channel when the panel is added in prime order. Every survivor before \(q\) must have the same \(d\bmod o_q\), namely its hard anchor. If \(o_q\) reads an odd \(r\)-digit at depth \(h\) and that digit has no retained owner row, **at least \(r-1\) distinct earlier retained rows must read \(r^h\)**. Vary that one digit from an earlier survivor, holding all others fixed. Each foreign reader can reject at most one choice, since it can reject only in its unique collision class.

This gives an unconditional exclusion for \(q=40487\) as a first fixed-axis blocker. Its order reads the split prime \(653\). There are at most **15** earlier inert integers even eligible to read that digit, since they must be \(1\bmod653\) and \(3\bmod4\). The forcing bound requires **652** earlier readers.

### Applying the kernel to the three actual primes

Their exact downward closure retains only the following ordinary owners in addition to the three possible hard rows.

| Possible hard row | Actual base-5 order | Ordinary owners reached |
|---|---:|---|
| \(20771\) | \(5\cdot31\cdot67\) | \(31,3,67,11\) |
| \(40487\) | \(2\cdot31\cdot653\) | \(31,3\) |
| \(1645333507\) | \(2\cdot3^3\cdot30469139\) | \(3,30469139,1523\) |


Here is an explicit order of repairs, so a later move cannot spoil an already protected row:

1. Choose an allowed parity and satisfy the 2-adic norm condition by adjusting higher binary digits. Then repair the ordinary rows \(3,31,67,1523\) in increasing order on their own primary coordinates, leaving the \(11\)-primary coordinate fixed. In particular \(o_5(67)=22\) reads the fixed \(11\)-primary digit and parity, and \(o_5(1523)=2\cdot761\).
2. Choose \(d_5\) to make \(11\) and \(20771\) units. Each forbids at most one of its five choices; neither move affects any of the repaired rows in step 1. This choice keeps the \(11\)-primary digit fixed.
3. Choose \(d_{653}\) to make \(40487\) a unit. Choose \(d_{1429}\) to make \(30469139\) a unit, then choose \(d_{30469139}\) to make \(1645333507\) a unit. These choices preserve all previously serviced rows. The two source primes 653 and 1429 are split, so they require no odd local norm condition of their own.
4. Apply the closure argument to repair remaining nonhard rows. If additional rows are in the larger finite panel and none of them is hard on this channel, the same argument applies.

This proves the claimed necessity for each viable fixed channel. It does not expand it to a genuine finite blocker or an integer representation for a prescribed target.

```python
from math import isqrt
def prime(p):return p>1 and all(p%j for j in range(2,isqrt(p)+1))
def fac(n):
    out=[]
    j=2
    while j*j<=n:
        if n%j==0:
            out.append(j)
            while n%j==0:n//=j
        j+=1
    return out+([n] if n>1 else [])
def order(b,p):
    e=p-1
    for l in fac(e):
        while e%l==0 and pow(b,e//l,p)==1:e//=l
    return e
S=(3,11,31,67,1523,30469139,20771,40487,1645333507)
assert all(prime(p) and p%4==3 for p in S)
O={p:order(5,p) for p in S}
print(O)
assert all(pow(5,O[p],p*p)!=1 for p in S[:6])
assert all(pow(5,O[p],p*p)==1 for p in S[6:])
for q,W in ((20771,{31,3,67,11}),(40487,{31,3}),(1645333507,{3,30469139,1523})):
    T={q}
    while True:
        Q=T|{r for p in T for r in fac(O[p]) if r%4==3}
        if T==Q:break
        T=Q
    assert T-{q}==W
assert len([653*k+1 for k in range(2,62,4)])==15
def good2(u):
    f=u & -u
    return bool(f and f<=8 and (u//f)%4==1)
for A in range(32):
    allowed=[e for e in range(2) if any(good2((A-pow(5,d,32))%32)
                                          for d in range(e,8,2))]
    assert len(allowed)=={0:0,1:2,2:2,3:1}[A%4]
print("OK")
```
