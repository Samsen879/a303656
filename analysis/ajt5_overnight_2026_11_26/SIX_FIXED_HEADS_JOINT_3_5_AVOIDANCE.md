# Six fixed heads with joint release at 3 and 5

**Six heads preselected modulo \(3960\) suffice for six terminals.** They can be chosen using only the small-head readings, and the previous five can be retained. The proof releases the remaining \(3\)- and \(5\)-coordinates together, then fixes one digit of \(d\) if there are shallow \(3\)-readers.

Precisely, take any finite panel with at most six designated inert terminals above \(23\). If every other required inert row above \(23\) is ordinary, some phase in the menu gives units at all designated terminals and passes all the ordinary rows. This applies to panels with up to six genuine common Wieferich rows, if such rows exist. The head selection uses no terminal orders or observations. [Published preselected-menu baseline](https://github.com/Samsen879/a303656/blob/b530c59c587786059765e396db035e386bcca1f0/analysis/ajt5_overnight_2026_11_26/PRESELECTED_MENU_UP_TO_THREE_TERMINALS.md)

### The head menu

Keep \(d\) and \(c\bmod8\) fixed. The previous construction offers at least eight legal \(c\bmod15\) values before the final adjustment at \(23\). There are at least two legal \(c\bmod3\) branches at \(7\), and each extends through \(19\) to at least four legal \(c\bmod5\) values at \(11\). At \(23\), steps of \(360\) preserve \(c\bmod15\) and offer at least ten legal \(c\bmod11\) values. Choose the first unused residue at each stage. This adds a sixth head to the previous five.

The five pinned primes are \(31,67,199,331,991\). The order of \(3\) at \(31\) is divisible by \(15\), and its order at each of the other four is divisible by \(11\). Thus each pinned row vetoes at most one head. A six-head menu leaves a survivor even if all five pinned rows are live.

### The joint \(3,5\) bound

Peel sources \(s\ge7\) as before. Withdraw the targets reading \(s\), and use \(s\) as a single auxiliary unit target if it is inert and above \(23\). The active count never increases. On restoration the exclusion cost is at most \(6/s<1\). Once the only free sources are \(3\) and \(5\), both can be released together while preserving the small head. Ordinary rows above \(23\) can afterward be repaired on their own primary coordinates, which the remaining targets do not read.

At a remaining target \(p\), write \(x,y\) for the free orders of \(3,5\), respectively. Each is its full order divided by its gcd with \(3960\). The row excludes at most \(1/\max(x,y)\) of the grid. Fixing the first free \(3\)-digit of \(d\), equivalently fixing \(d\bmod27\), changes this denominator to
\[
\widetilde D_p=\max\!\left(x,\frac{y}{\gcd(y,3)}\right).
\]
This gives a finite arithmetic certificate for every row with \(\widetilde D_p<9\). Indeed, \(x,y/\gcd(y,3)\in\{1,3,5\}\), so both full orders divide \(44550=990\cdot45\). The exact gcd factorization in the replay yields the following complete list apart from pinned rows.

| Target | \((x,y)\) | \(\widetilde D_p\) |
|---:|---:|---:|
| 151 | \((5,5)\) | 5 |
| 271 | \((1,3)\) | 1 |
| 1783 | \((3,9)\) | 3 |
| 2971 | \((1,3)\) | 1 |
| 4951 | \((1,5)\) | 5 |

There are two cases.

- **Neither shallow row \(271,2971\) is live.** Keep the whole grid. At most two rows have free denominator \(5\), and every other unpinned row has denominator at least \(9\). The cost is at most \(2/5+4/9=38/45\).
- **At least one shallow row is live.** Each shallow row vetoes at most one of the three choices for \(d\bmod27\). Fix a choice avoiding both and remove their tests from the count. At most five unpinned rows remain. The restricted grid has at most two denominators \(5\), at most one denominator \(3\), and all others at least \(9\). The cost is at most \(2/5+1/3+2/9=43/45\).

The transferable criterion is to clear the shallow rows on a common coordinate first, then sum reciprocal **restricted** orders on the surviving grid. This uses the shared coordinate directly. It requires no independence assumption or scan over larger primes.

### Standalone arithmetic replay

The ordinary control below has the two shallow rows veto different digits. Exactly one digit survives, and \(160\) of the \(225\) points in the resulting grid give units at all five ordinary readers. The same small-head readings append \(c=1163\) to the previous five heads, with \(d=275\).

```python
from itertools import product
from math import gcd, isqrt, prod

C = 3960
P = (2,7,11,19,23,31,61,67,181,199,331,661,991)
Q = (109,151,163,271,541,811,1621,1783,2971,3301,4051,
     4951,8101,9901,14851,89101)

def prime(p):
    return p > 1 and all(p%j for j in range(2,isqrt(p)+1))

def order(b,p):
    return next(j for j in range(1,p) if pow(b,j,p)==1)

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

assert len(set(P+Q))==len(P+Q) and all(map(prime,P+Q))
G = gcd(3**990-1,5**990-1)
assert G==44*prod(P)
assert gcd(3**44550-1,5**44550-1)==G*prod(Q)

pinned = [p for p in P if p>23 and p%4==3]
assert pinned==[31,67,199,331,991]
assert [order(3,p) for p in pinned]==[30,22,198,330,330]
small = {}
for p in Q:
    if p%4==3:
        a,b = order(3,p),order(5,p)
        x,y = a//gcd(a,C), b//gcd(b,C)
        D = max(x,y//gcd(y,3))
        if D<9:
            small[p]=(x,y,D)
assert small=={151:(5,5,5),271:(1,3,1),1783:(3,9,3),
               2971:(1,3,1),4951:(1,5,5)}
assert all(pow(b,p-1,p*p)!=1 for p in small for b in (3,5))

n,d = 1490980374686314747641,275
assert tuple(n%p for p in (32,3,7,19,11,23))==(25,0,0,1,10,1)
old = (339,11,3,435,291)

def append_head(n,d,old):
    for i in range(3):
        a = 3+8*i
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

c6 = append_head(n,d,old)
assert c6==1163
menu = old+(c6,)
assert all((n-S(c,d,32))%32==1 and (n-pow(5,d,3))%3
           and all((n-S(c,d,p))%p for p in (7,19,11,23)) for c in menu)
assert all(len({S(c,d,p) for c in menu})==6 for p in pinned)

c = 291
assert [[j for j in range(3) if (n-S(c,d+C*j,p))%p==0]
        for p in (271,2971)]==[[0],[1]]
assert sum(all((n-S(c+C*i,d+C*(2+3*j),p))%p for p in small)
           for i,j in product(range(15),repeat=2))==160
print("OK",menu)
```

Six is minimal for the uniform test against all five pinned **unit** rows, by assigning a different row to veto each of at most five heads and realizing the readings by CRT. This is a result about a fixed, terminal-blind menu, separate from the unrestricted ten-target count. The replay uses ordinary primes and establishes no norm blocker. The theorem gives no new density-one or pointwise conclusion.
