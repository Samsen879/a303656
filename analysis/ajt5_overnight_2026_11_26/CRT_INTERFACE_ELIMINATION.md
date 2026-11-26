# Exact CRT membership-cell elimination with bounded joint interfaces

**Yes, with a bound on the joint CRT interface.** Each prime-power axis can first be compressed to the prefix tests the panel actually reads. Exact elimination then keeps a table on the coordinates shared with the remaining rows. This works through any number of nonlinear pivots. The width bound depends on the actual order scopes and the elimination order. [Starting guard-set invariant](https://github.com/Samsen879/a303656/commit/32befe4d52fd90c4ff12c2fcfc03ab9d10a9b8d0)

### Exact compression

Fix \(n,c\) and the parity of \(d\). On an axis modulo \(p^D\), collect every prefix \(d\equiv a\bmod p^e\) read by an order guard, and every center prefix needed to decide that row’s valuation shells. For an odd-prime dynamic row, the order guard fixes the logarithm modulo the prime-to-\(p\) order. The remaining shell tests are differences of nested prefixes on the \(p\)-axis.

If there are \(m_p\) distinct prefix tests, there are at most \(m_p+1\) nonempty **membership cells**. The prefixes are laminar. The cells are each prefix minus its maximal tested subprefixes, with the whole axis included as a root. Their sizes are exact differences of powers of \(p\). Reversing the base-\(p\) digits turns the prefixes into intervals, so the cells and a representative of each can be found from interval endpoints. Every original row is constant on products of these cells.

Work with **safe** constraints. When eliminating \(p\), collect the current constraints \(\mathcal B_p\) that read it. Write \(I_p\) for the other coordinates they read. The exact replacement is
\[
M_p(a_{I_p})=\bigvee_{a_p}\ \bigwedge_{f\in\mathcal B_p} f(a_p,a_{I_p}).
\]
The same cell \(a_p\) must satisfy the whole bucket. Constraints outside it pass through. The replacement has \(\prod_{i\in I_p}(m_i+1)\) entries at most, and each entry tries at most \(m_p+1\) cells. This is the complement of universal forbidden-fibre projection, so the identity applies at successive actual nonlinear ranks as well. To measure the lower phases with an escape, finish the Boolean eliminations first, then sum the sizes of the accepted lower cells. Multiple lifts of one lower phase count once.

If eliminating all hidden axes first produces a large interface, a second exact representation is a layered graph. Process the coordinates in an interleaved order and keep assignments only to previously read cells still mentioned by an unfinished constraint. Label retained-coordinate edges by their cells and hidden-coordinate edges by \(\epsilon\). A lower word survives exactly when it labels an accepting path. A **synthetic** chain with hidden state \(h_i=h_{i-1}\lor[x_i=2]\), \(h_0=0,h_k=1\), has a two-state projected graph. Its forbidden set is all words in \(\{0,1\}^k\), with \(2^k\) feasible minimal witnesses over the original single-value guards. The graph compresses that family. Distinct-word counting still needs to account for any ambiguity in the graph.

### Arithmetic control and a sharp failure

- **Actual 7/11/463 controls.** At the fixed hit and miss targets, the \(3,5,7,11,463\) axes compress to \(2,2,2,2,2\) cells and \(2,2,2,3,2\) cells, respectively. Charging the whole actual 463 order guard reproduces **14 of 15** lower phases surviving in the hit case and **15 of 15** in the miss case. With the genuine square-precision row at 463, its safe center gives **15 of 15** in both cases. These are actual arithmetic checks through two eliminations. The hit overcover uses centered relays. The two-essential-pivot check below uses synthetic supports.
- **Synthetic joint-interface failure.** After eliminating 11, require \(z=x\oplus y\), where \(x,y\in\{0,1\}\) are retained and \(z\) is the remaining 7 digit. Keep a separate constraint \(z=0\). The interface relation and its opposite parity have identical pairwise shadows, even with multiplicities. Eliminating 7 gives the diagonal for one and the antidiagonal for the other. Joining the pairwise shadows instead reports all four lower pairs as safe, falsely admitting two in either case. Both stages can be realized as nonlinear full-fibre tests using synthetic single-prefix vetoes for the forbidden tuples.

The replay compares the whole-guard overcover against the exact square-modulus row at its actual center and validates the synthetic interface contrast.

```python
from itertools import combinations, product
from math import prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

def table(D, scope, f):
    return scope, {r for r in product(*(D[p] for p in scope)) if f(*r)}

def accepts(F, env):
    return all(tuple(env[p] for p in scope) in T for scope,T in F)

def elim(D, F, p):
    bucket = [(s,T) for s,T in F if p in s]
    keep = [(s,T) for s,T in F if p not in s]
    I = tuple(sorted({q for s,_ in bucket for q in s} - {p}))
    return keep + [table(D,I,lambda *r: any(
        accepts(bucket,dict(zip(I,r)) | {p:a}) for a in D[p]))]

q = 463
assert pow(5,462,q) == 1 and pow(5,462,q*q) == 17595
assert all(pow(5,462//p,q) != 1 for p in (2,3,7,11))
M = 8*3*49*31*71*5167*19531
for a,b,k in ((2,168,0),(1,30,1)):
    u = crt([(3,M),(2,121),(a,q)])
    v = crt([(8,M),(2,121),(b,q)])
    n = 4+u*u+v*v
    X,Y = {0:2,2:1}, {0:4,4:1}
    D = {3:X,5:Y,7:(0,2),11:((0,1) if k==0 else (0,1,2))}

    def residue(p,K,*digits):
        d = crt([(0,2),*digits])
        return (n-3-pow(5,d,p**K)) % p**K

    def good(p,*digits):
        r = residue(p,2,*digits)
        return r==0 or r%p!=0

    F = [table(D,(3,7),lambda x,z:good(7,(x,3),(z,7))),
         table(D,(5,11),lambda y,t:good(11,(y,5),(t,11))),
         table(D,(3,7,11),lambda x,z,t:residue(q,1,(x,3),(z,7),(t,11))!=0)]
    G = elim(D,elim(D,F,11),7)
    d_anchor=crt([(0,2),(2,3),(2,7),(k,11)])
    centers=[j for j in range(q) if (n-3-pow(5,d_anchor+462*j,q*q))%(q*q)==0]
    assert len(centers)==1
    center=d_anchor+462*centers[0]
    D[q]=(center%q,(center+1)%q)
    def exact_q(x,z,t,h):
        v=residue(q,2,(x,3),(z,7),(t,11),(h,q))
        return v==0 or v%q!=0
    FF=F[:-1]+[table(D,(3,7,11,q),exact_q)]
    GG=elim(D,elim(D,elim(D,FF,q),11),7)
    assert sum(X[x]*Y[y] for x,y in product(X,Y)
               if accepts(GG,{3:x,5:y}))==15
    assert sum(X[x]*Y[y] for x,y in product(X,Y)
               if accepts(G,{3:x,5:y})) == 14+k

# Synthetic parity interfaces. Equal shadows, different exact outcomes.
D = {3:range(2),5:range(2),7:range(7),11:range(11)}
def parity(k):
    return elim(D,[table(D,(3,5,11),lambda x,y,t:t==(k^x^y)),
                   table(D,(7,11),lambda z,t:z==t),
                   table(D,(7,),lambda z:z==0)],11)

even, odd = parity(0), parity(1)
for i,j in combinations(range(3),2):
    assert {(r[i],r[j]) for r in even[-1][1]} == {
        (r[i],r[j]) for r in odd[-1][1]} == set(product(range(2),repeat=2))
assert elim(D,even,7) == [((3,5),{(0,0),(1,1)})]
assert elim(D,odd,7) == [((3,5),{(0,1),(1,0)})]
print("PASS")
```

The width bound is stated for a fixed elimination ordering and actual table scopes; it is not a uniform small-width theorem for every order graph. Local constraints are joined before projecting a common variable. Retaining only marginal shadows, or counting distinct witness paths instead of distinct lower words, is not generally a valid replacement. The final weighted count sums lower membership-cell sizes rather than numbers of higher lifts.
