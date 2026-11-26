# Higher-order relations give an escape bound without one short ratio

Scope: the [pinned nonzero moving readers](TRANSLATED_WINDOW_MULTI_READER_ESCAPE.md), not arbitrary read graphs. Let labels range over \(\mathbb Z/h\), with \(h\) prime, and let \(f(j)=Cw^j\bmod p\) be the forced digit, where \(w\) has order \(h\) modulo \(p\). At a reader a hit satisfies \(A\chi(j)G^{f(j)}+B\psi(j)=N\), where \(A,B,N\ne0\), \(G\) has order \(p\), and \(\psi\) has order \(h\). The characters and constants are in the reader field, and those at different readers need not agree.

## All subsets of offsets

For \(2\le s\le h\), take distinct offsets \(t_i\). Put \(M=\lfloor p^{1/(s-1)}\rfloor\). Two of the \((M+1)^{s-1}>p\) vectors with coordinates in \([0,M]\) have the same weighted sum modulo \(p\) against \(w^{t_i}-w^{t_1}\), for \(i\ge2\). Subtract them and choose \(e_1=-\sum_{i\ge2}e_i\). This gives a nonzero vector satisfying \(\sum e_i=0\) and \(\sum e_iw^{t_i}=0\bmod p\), with positive mass at most \(D_s=(s-1)M\). For the last bound, the positive mass is the larger of the positive and negative masses among the \(s-1\) free entries.

If every \(j+t_i\) hits one reader, put \(Z=B\psi(j)\), \(v_i=\psi(t_i)\), and \(u_i=\chi(t_i)\). Multiplying the hit equations on the positive and negative sides gives
\[
  \prod_{e_i>0}(N-v_iZ)^{e_i}
  =\left(\prod_i u_i^{e_i}\right)\prod_{e_i<0}(N-v_iZ)^{-e_i}.
\]
The common factor cancels by the zero sum, and the powers of \(G\) cancel by the congruence. At \(Z=N/v_i\) for any positive entry \(e_i\), only the left side vanishes, because \(N\ne0\) and the \(v_i\) are distinct. Thus this is a nonzero polynomial of degree at most \(D_s\). There are at most \(D_s\) starting labels, by injectivity of \(\psi\).

For one reader's hit set \(T\), summing the count over all \(s\)-subsets of offsets gives \(h\binom{|T|}{s}\le D_s\binom hs\): each \(s\)-subset of \(T\) is counted once for each choice of starting label. Hence for the union of \(m\) readers,
\[
 \frac{|\bigcup T|}{h}\le m\left(\frac{s-1}{h}+(D_s/h)^{1/s}\right).
\]
The bound is useful when a retained set has more elements than the right-hand side times \(h\). With \(s=1+\lceil2\log p/\log h\rceil\), \(D_s\le(s-1)\sqrt h\); if \(\log p=o((\log h)^2)\), then \(s=o(\log h)\) and the fraction is \(o(1)\) for fixed \(m\). More generally the same holds if \(\log m=o((\log h)^2/\log p)\). This is a conditional asymptotic about a family of actual relays in the stated regime; it does not supply such a family.

## Five-label control on the same target

Five integers \(X=(1185,1229,1251,1284,1515)\) lie in one order-653 coset modulo 40487. Choose their offsets by \(w^{t_i}=X_i/X_1\). For a triple \(x<y<z\), use coefficients \((z-y,-(z-x),y-x)\) divided by \(\gcd(z-y,y-x)\). This gives polynomial degree \((z-x)/\gcd(z-y,y-x)\); the ten degrees sum to 97.

Assign each hit one reader colour. For each colour in a translated window the number of labels is at most two plus the number of monochromatic triples. Sum over windows, using the polynomial bounds for each triple: on the full 653 labels the union has at most \(\lfloor(4\cdot653+2\cdot97)/5\rfloor=561\) hits, giving at least 91 escapes on the 652 retained labels. The exact replay shows that the twenty corresponding polynomials have no roots on their actual slow-character cosets. Then the union has at most \(\lfloor4\cdot653/5\rfloor\) hits, giving at least 130 escapes by this certificate. The earlier direct enumeration found 650; the improvement here is to the structural certificate, not the actual hit count. Neither estimate controls inert primes outside the pinned panel.

```python
from itertools import combinations
from math import gcd,lcm
h,p=653,40487
R=(10250810005031,83354871477263)
q=83354871555623
n=5876287000060657202950467015460482075793645557875570177493028174478665292305806831
H=lcm(p*p*(p-1),*(r*(r-1) for r in R),q*(q-1))
J=(H//h)*pow(H//h,-1,h)
D=(p-1)//2*p*R[0]*R[1]*q
w=pow(3,-J,p)
logs={pow(w,i,p):i for i in range(h)}
assert len(logs)==h
X=(1185,1229,1251,1284,1515)
assert {pow(x,h,p) for x in X}=={8000}
assert sum((z-x)//gcd(z-y,y-x) for x,y,z in combinations(X,3))==97
assert 652-(2*2*h+2*97)//5==91
for r in R:
    N,b,g,B=n%r,pow(5,401*J,r),pow(3,J,r),pow(5,D,r)
    for x,y,z in combinations(X,3):
        t=[logs[v*pow(X[0],-1,p)%p] for v in (x,y,z)]
        d=gcd(z-y,y-x)
        i,k,j=(z-y)//d,(z-x)//d,(y-x)//d
        u=pow(g,i*t[0]-k*t[1]+j*t[2],r)
        v=[pow(b,ti,r) for ti in t]
        for a in range(h):
            Z=B*pow(b,a,r)%r
            Q=[(N-vv*Z)%r for vv in v]
            assert (pow(Q[0],i,r)*pow(Q[2],j,r)-u*pow(Q[1],k,r))%r
assert 652-4*h//5==130
print("OK")
```
