# Optimal dyadic sector selection for zero-observation rigid sources

**The rigid-source bound survives the extra dyadic parity sectors.** The key is that a dyadic lift of \(d\) preserves every odd inert-prime test once its parity is fixed. This gives a uniform one-third mute at \(n\equiv0\pmod{24}\), where even-even is unavailable. Other target classes can miss an entire Legendre sign type, so a positive fraction then requires information about the actual sign counts. [Pinned sign argument](https://github.com/Samsen879/a303656/commit/01da98288734948b95f4d0f307aa83b88d77bedf) · [Seventeen-source theorem](RANK_SEVEN_SIXTEEN_SOURCE_ESCAPE.md)

### Which sectors preserve the theorem

Write \(ab=(c\bmod2,d\bmod2)\). For a modulus containing 8, the dyadic sector is available exactly when \(n-3^a-5^b\bmod8\) lies in \(\{0,1,2,4,5\}\).

| \(n\bmod8\) | Dyadic sectors |
|---|---|
| 0 | \(01,10,11\) |
| 1 or 5 | \(10,11\) |
| 2 | \(00,01,11\) |
| 3 or 7 | \(00,01\) |
| 4 | \(00,10,11\) |
| 6 | \(00,01,10\) |

For a factor 4 alone, exclude only residual class \(3\bmod4\). A factor 2 imposes no restriction.

For fixed \(c\) and \(d\)-parity, \(5^d\bmod32\) runs through all lifts of its residue modulo 8. Thus residual classes 0 and 4 can be made \(8\bmod32\) and \(4\bmod16\), respectively. Every inert odd prime power has \(5\)-order with 2-part at most 2. CRT therefore lets us impose the dyadic choice of \(d\) on **every odd-order phase** in the fixed-parity slice. The proof does not need to discard any of its ternary or higher odd-prime coordinates.

When \(9\mid M\), keep row 3 inactive by additionally requiring \(n\bmod3\ne(-1)^b\bmod3\). This keeps both \(d\)-parities at \(n\equiv0\bmod3\), only odd \(d\) at \(n\equiv1\bmod3\), and only even \(d\) at \(n\equiv2\bmod3\). If \(9\nmid M\), row 3 contributes no rejection. A sector with matching signs at 3 can pass locally after a lift, but that lift forces a particular \(d\bmod3\). The replay shows why this restriction is visible to the odd-prime graph.

On any remaining sector, the four helper mutes and singly exceptional base-3 corrections apply with the selected parities. The dyadic choice can be made afterward. Thus the current seventeen-source threshold still applies. [Parity-preserving helper reservation](https://github.com/Samsen879/a303656/commit/c3cee9b) · [Exact modulus bridge](https://github.com/Samsen879/a303656/commit/1c648df)

### Exact count from the sign pairs

Let \(U\) count the relevant common Wieferich primes with \(q\nmid n\), and let \(Z_{\sigma\tau}\) count those dividing \(n\), grouped by \(((3/q),(5/q))\). Count only primes whose squares divide the witness modulus.

| Sign pair | Actual inert classes mod 60 | Muted outside \(00\) in |
|---|---|---|
| \(++\) | 11, 59 | every sector |
| \(+-\) | 23, 47 | \(10\) |
| \(-+\) | 19, 31 | \(01\) |
| \(--\) | 7, 43 | \(11\) |

Sector \(00\) mutes all four types. Let \(m_*\) be the largest number muted among the available sectors. The necessary condition for a finite obstruction is
\[
U+\sum_{\sigma,\tau}Z_{\sigma\tau}-m_*\ge17.
\]
This is a count of potential rigid sources. A row that misses the sign test can still be inactive for another arithmetic reason.

At \(n\equiv0\pmod{24}\), all three non-even-even sectors are available, so
\[
m_* = Z_{++}+\max(Z_{+-},Z_{-+},Z_{--}).
\]
This mutes at least a third of the zero rows. If \(U=0\), an obstruction in this target class would require at least **26 zero-observation common Wieferich primes of non-\(++\) type**. In contrast, at \(n\equiv9\pmod{24}\) the only sectors are \(10,11\), and neither mutes type \(-+\). Counts concentrated on that type give zero guaranteed saving. This is a sharp limit of sign selection alone. It assumes no distribution of genuine common Wieferich primes.

### Runnable finite control

The same four actual primes realize all four sign types. The first target mutes exactly one of \(7,19,23\) in each of its three sectors. The second target leaves \(19\) at exact valuation one in both available sectors. These primes are all ordinary to base 5, so the replay tests the sign and unit rules without supplying common-exception examples.

```python
from math import prod

P = (7,11,19,23)
assert all(pow(5,q-1,q*q) != 1 for q in P)
assert [tuple(pow(b,(q-1)//2,q) == 1 for b in (3,5)) for q in P] == [
    (False,False),(True,True),(False,True),(True,False)]
C = prod(q*((q-1)//2) for q in P)

def target(a,m):
    pairs = [(a,m)] + [(q,q*q) for q in P]
    M = prod(q for _,q in pairs)
    return sum(v*(M//q)*pow(M//q,-1,q) for v,q in pairs)%M

def res(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def good2(x):
    return x%4==1 or x%8==2 or x%16==4 or x==8

expected = {"01":{11,19}, "10":{11,23}, "11":{7,11}}
for a,want in ((0,["01","10","11"]),(9,["10","11"])):
    n = target(a,96)
    sectors = [f"{e}{b}" for e in (0,1) for b in (0,1)
               if (n-3**e-5**b)%8 in (0,1,2,4,5) and n%3!=5**b%3]
    assert sectors == want
    for sector in sectors:
        e,b = map(int,sector)
        c,d0 = (2-e)*C,(2-b)*C
        ds = [d0+2*C*j for j in range(4)]
        d = next(t for t in ds if good2(res(n,c,t,32)))
        assert res(n,c,d,3)
        muted = {q for q in P if res(n,c,d,q)}
        assert muted == expected[sector]
        assert len(muted-{11})==1 if a==0 else 19 not in muted
        for q in P:
            v = res(n,c,d,q*q)
            assert all(res(n,c,t,q*q)==v for t in ds)
            if q not in muted:
                assert v==q

# A ternary restriction changes the actual row at 7.
n = target(1,9)
assert [res(n,C,d,9) for d in (0,2,4)] == [0,3,6]
assert [res(n,C,d,7) for d in (0,2,4)] == [0,4,6]
S=((0,1),(1,0),(1,1))
for n in range(24):
    opts=[(a,b) for a in (0,1) for b in (0,1) if
          (n-3**a-5**b)%8 in (0,1,2,4,5) and n%3!=5**b%3]
    assert opts
assert next(t for t in range(100) if t-(t+2)//3>=17)==26
print("OK")
```

The theorem concerns an exact finite obstruction. The replay checks finite residues and gives no all-prime square-sum conclusion.

For the 26 count, discard the ++ rows, which are sign-protected in every sector. If M counts the remaining three types and U=0, at least ceil(M/3) are muted in the best sector at n=0 mod 24. Thus at most floor(2M/3) can supply rigid sources; the verified seventeen-source condition forces M≥26. This statement is conditional on a hypothetical finite obstruction and does not assume these common exceptional primes exist.
