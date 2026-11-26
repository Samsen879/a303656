# Five preselected heads for four inert targets

**Five preselected mod \(3960\) heads suffice for four terminals.** The fifth can be added without changing any of the previous four heads or varying \(d\). The unused digit is \(c\bmod3\) in the order \(30\) at \(31\). Use distinct \(c\bmod15\) at that row and distinct \(c\bmod11\) at the other four pinned rows.

For any finite panel with at most four designated inert terminals above \(23\), if every other required inert row above \(23\) is ordinary, some phase in this menu gives units at all designated terminals and passes all the ordinary rows. This applies in particular to a panel with at most four genuine common Wieferich rows. The menu depends only on the small-head readings. [Previous preselected-menu theorem](https://github.com/Samsen879/a303656/blob/b530c59c587786059765e396db035e386bcca1f0/analysis/ajt5_overnight_2026_11_26/PRESELECTED_MENU_UP_TO_THREE_TERMINALS.md)

### Selecting the fifth head

Keep the common \(d\) and \(c\bmod8\). At \(7\), at least two of the three choices in steps of \(8\) pass, and they have distinct \(c\bmod3\). Extend each through \(19\) using steps of \(24\), which preserve \(c\bmod3\). At \(11\), each branch offers at least four legal \(c\bmod5\) values via steps of \(72\), again preserving \(c\bmod3\). Together these branches offer **at least eight distinct \(c\bmod15\) values**, even when the same mod-\(5\) value is forbidden on every branch.

Choose the first legal \(c\bmod15\) unused by the four old heads. At \(23\), steps of \(360\) preserve it and give at least ten legal \(c\bmod11\) values. Choose the first unused one. The original four heads already have distinct residues modulo \(15\) because they were distinct modulo \(5\).

The pinned primes are \(31,67,199,331,991\). Their orders of \(3\) are \(30,22,198,330,330\), respectively. Thus \(15\) divides the first order and \(11\) divides each of the other four. With \(d\) common, the five shifts are distinct at every pinned row. At most four pinned rows can veto at most four heads.

### Restoring four terminals

Use the previous largest-free-source descent. Remove all active targets reading the chosen prime \(s\), and insert \(s\) as a single auxiliary unit target if it is inert and above \(23\). The target count never increases. On restoration a reader with \(D\) free values along its stronger axis excludes at most \(1/D\) of the grid. Ordinary repairs above \(s\) use their own digits and preserve the active terminal shifts.

For \(s\ge5\), the total exclusion is at most \(4/s<1\). At \(s=3\), a shallow reader has depth exactly \(3\), so both its orders divide \(2970\). The exact gcd identity below leaves only \(271\) and \(2971\) as shallow inert readers. This bound applies **even when deeper readers are present**. A deeper reader has at least nine free values because the lock fixes only the first two \(3\)-digits. If \(a\le2\) of the readers are shallow, the total exclusion is at most
\[
\frac a3+\frac{4-a}{9}\le\frac89.
\]

### Reproducible pinned control

At \(n=118776407814393\) with \(d=275\), the row at \(11\) forbids \(c\equiv2\bmod5\) on every branch. Each of the four old heads is vetoed at a distinct pinned row. The deterministic fifth head is \(c=291\). It shares \(c\bmod5=1\) with \(c=11\), but differs modulo \(3\).

```python
from math import gcd, isqrt, prod

C = 3960
P = (2,7,11,19,23,31,61,67,181,199,331,661,991)
extra = (109,271,541,2971)

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p)) % p

def prime(p):
    return p > 1 and all(p % j for j in range(2,isqrt(p)+1))

assert all(map(prime,P+extra))
G = gcd(3**990-1,5**990-1)
assert G == 44*prod(P)
assert gcd(3**2970-1,5**2970-1) == G*prod(extra)
assert [p for p in extra if p%4==3] == [271,2971]

L = [p for p in P if p>23 and p%4==3]
assert L == [31,67,199,331,991]
assert [next(j for j in range(1,p) if pow(3,j,p)==1) for p in L] == [
    30,22,198,330,330]
assert all(pow(b,p-1,p*p)!=1 for p in L for b in (3,5))

rows = ((7,8,3),(19,24,3),(11,72,5),(23,360,11))
for i,(p,h,k) in enumerate(rows):
    assert h%8==0 and len({pow(3,h*j,p) for j in range(k)})==k
    assert all(pow(3,h,t)==1 for t,_,_ in rows[:i])
    assert all(pow(b,C,p)==1 for b in (3,5))
assert 8%3 and 24%3==0 and 72%3==0 and 72%5 and 360%15==0 and 360%11

def append_head(n,c8,d,old):
    for i in range(3):
        a = c8+8*i
        if (n-S(a,d,7))%7==0:
            continue
        a = next(a+24*j for j in range(3) if (n-S(a+24*j,d,19))%19)
        for j in range(5):
            x = a+72*j
            if (n-S(x,d,11))%11==0 or any((x-y)%15==0 for y in old):
                continue
            for k in range(11):
                c = x+360*k
                if (n-S(c,d,23))%23 and all((c-y)%11 for y in old):
                    return c%C
    raise AssertionError("no unused head")

n,d,old = 118776407814393,275,(339,11,3,435)
assert {j for j in range(5) if S(j,d,11)==n%11} == {2}
c = append_head(n,3,d,old)
assert c==291 and c%5==11%5 and c%3!=11%3
assert all((n-S(a,d,32))%32==1 and (n-pow(5,d,3))%3
           and all((n-S(a,d,p))%p for p,_,_ in rows) for a in old+(c,))
assert all(len({S(a,d,p) for a in old+(c,)})==5 for p in L)
assert all((n-S(a,d,p))%p==0 for a,p in zip(old,L))
assert [(n-S(c,d,p))%p for p in L[:4]] == [14,24,125,35]
print("OK")
```

Five is minimal for the **uniform pinned-unit test**. For any terminal-blind menu of at most four heads, assign each head a different pinned prime and set that prime’s observation equal to the head’s shift. CRT preserves the small-head readings. Those pinned primes are ordinary, so this lower bound concerns unit avoidance. It gives no norm blocker or lower bound for menus tested only against genuine common Wieferich terminals. The result is finite-local, with no new density-one or pointwise conclusion.

The unrestricted ten-target count remains stronger when there is no preselection requirement.
