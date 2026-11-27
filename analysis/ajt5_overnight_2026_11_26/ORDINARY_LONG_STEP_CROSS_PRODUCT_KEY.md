# Cross-product residue charging for ordinary long-step triples

For a fixed target integer \(n\) and fixed primes \(r,s\asymp R\), consider the ordinary long-step triples whose two displacements are \((ah,bk),(ch,dk)\), with positive \(a,b,c,d\ll\sqrt R\), nonzero signed \(h,k\), displacements \(O(R)\), and \(r\mid ad-bc\ne0\). Retain the short-grid phase injectivity and physical prime order hypotheses of the ordinary-orbit count. The normalized crossed product
\[
I=ad\bmod r=bc\bmod r
\]
is a key for **charging**, not for identifying an orbit. For a common subset \(\mathcal I\subset\mathbb F_r\), across all physical primes, the genuine triple weight obeys
\[
W_n(\mathcal I)\ll_\epsilon |\mathcal I| R^{2+\epsilon}.
\]
The ordinary orbit closure of the selected triples has the same bound in the double-nonresidue stratum with the existing bound of 36 unordered triples per orbit. This gives a power saving over the \(R^{55/24}\) threshold only when the common key set is \(O(R^{7/24-\delta})\); the hypotheses give no such unconditional support bound. The estimate is for fixed \(r,s\), not a joint sum over choices of them.

## Proof of the restricted bound

Each of \(ad,bc\) is a positive integer \(O(R)\) in a prescribed residue class modulo \(r\asymp R\), hence has \(O(1)\) choices. Divisor bounds give \(O_\epsilon(R^\epsilon)\) quadruples for one key. Since \(|ad-bc|\ge r\), at least one product is \(\gg R\). One factor on each axis is therefore \(\gg\sqrt R\), so the displacement bound gives \(|h|,|k|\ll\sqrt R\).

Put \(X=3^{720h},Y=5^{720k}\), and let
\[
\Delta=(X^a-1)(Y^d-1)-(X^c-1)(Y^b-1).
\]
Every contributing physical prime divides the numerator of \(\Delta\), by eliminating the two actual starting powers. This numerator is nonzero in the long-step regime \(720|h|>\log_3(\max(a,b,c,d))\). Indeed \(a=c\) or \(b=d\) in an equality forces both. Otherwise equality yields \((X^a-1)/(X^c-1)=(Y^b-1)/(Y^d-1)\). For \(h>0\), subtract 1 on both sides: the left 3-adic valuation is \(720h\min(a,c)\), while the right is \(v_3(b-d)-v_3(d)\), by lifting the exponent (also for negative integral \(k\), using 3-adic units). For \(h<0\), use the ratios without subtracting 1: the left valuation is \(720h(a-c)\), the right \(v_3(b)-v_3(d)\). Each contradicts the long-step inequality. Clearing the denominators costs \(O(R)\) in log-height, since all four products of a coefficient and a step have size \(O(R)\).

For each physical prime, fixed target, and tuple of displacements, the starting powers are determined by their sum and the first displacement equation. If the equations are dependent then the two phase multipliers agree; at a hit their common value must be 1 since the target is nonzero modulo the prime. The actual orders and nonzero short steps exclude this. Phase injectivity then gives at most one starting address. The square-free prime weight per tuple of displacements is at most the \(O(R)\) log-height; summing \(O(R)\) step pairs per coefficient tuple proves the bound. With all triples counted over each physical prime, closing under the bounded ordinary orbit costs at most 36.

Candidate geometry alone allows \(R^{1-o(1)}\) different keys: put \(L=\lfloor \sqrt r\rfloor\), pick coprime \(a\in[L,9L/8],c\in[7L/8,L)\), choose \(b\in[a,2a)\) with \(bc\equiv-r\bmod a\), and put \(d=(r+bc)/a\). There are \(\gg L^2\) coprime pairs (standard mean density of coprime pairs in fixed-proportion rectangles); \(a>c,d>b\) and all coefficients are comparable to \(L\). Here \(ad-bc=r\). The divisor argument still allows only \(R^{o(1)}\) templates per key, proving the stated candidate lower bound. These templates need not be genuine hits.

## Independent exact control at the same target

Use \(p=1259,r=17,C=466643,E=155665\). For a fully specified common integer target put \(M=146651884329720,\ Q=8807^2,\ L=1859996\) and
\[
x(a,b)=2^L+\bigl[a+M((b-a)M^{-1}\bmod Q)-2^L\bigr]_{MQ}.
\]
Here \([\,]_{m}\) is the least nonnegative residue. With \(U=x(61827877807697,0)\), \(V=x(135417323161960,39021647)\), take \(n=3^C+5^E+85(U^2+V^2)\). Then \(U,V\bmod p^2=(676086,49)\), \(n\bmod p^2=1223507\). The two true triples are \(((148,16),(160,1),(232,13))\) and \(((1,268),(75,33),(111,153))\), with fourth points \((171,9)\) and \((47,143)\) respectively. These are genuine **local obstruction hits** (valuation exactly 1 at \(p\)), not two-square representations. Both keys are 1: their \((ad,bc)\) are \((1,35)\) and \((851,2585)\). The step pairs are \((12,-3)\) and \((2,-5)\). The triples have distinct ordinary orbit labels, and shifting the first \(k\) to \(-4\) keeps this key but changes the determinant from 0 to 189 modulo \(p\).

Short replay, using the exact target residue above:

~~~python
p, r, C, E = 1259, 17, 466643, 155665
P, n = p*p, 1223507
rows = [
    ([(148,16),(160,1),(232,13)], (171,9), (1,35)),
    ([(1,268),(75,33),(111,153)], (47,143), (851,2585)),
]
def hit(i,j):
    a,b=pow(3,C+720*i,P),pow(5,E+720*j,P)
    z=a*pow(n,-1,p)%p
    assert (n-a-b)%P in range(p,P,p)
    assert all(pow(t,(p-1)//2,p)==p-1 for t in [z,1-z])
    return z
def images(z):
    a,b=pow(z,-1,p),pow(1-z,-1,p)
    return [z,1-z,a,1-a,b,1-b]
orbits=[]
for pts,f,products in rows:
    assert all(x%r==1 for x in products)
    hit(*f)
    orbit={tuple(sorted(x%p for x in col)) for col in zip(*(images(hit(*z)) for z in pts))}
    assert all(sum(col)%p!=1 for col in orbit)
    orbits.append(orbit)
assert orbits[0].isdisjoint(orbits[1])
X=pow(3,720*12,p)
def delta(k):
    Y=pow(5,720*k,p)
    return ((X-1)*(Y-1)-(pow(X,7,p)-1)*(pow(Y,5,p)-1))%p
assert (delta(-3),delta(-4))==(0,189)
~~~
