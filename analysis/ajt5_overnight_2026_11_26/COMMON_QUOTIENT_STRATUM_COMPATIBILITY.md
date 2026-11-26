# Common-quotient compatibility can rule out pairs of rough-depth strata

Fix the actual labels and the smooth parts away from 109 in [the one-sided test](ONE_SIDED_FIXED_DEPTH_PRIME_INTERVAL.md). Two strata with \(f<f'\) have shallow scales \(S,HS\), \(H=109^{f'-f}\), and deep scales \(D,D'\). Their necessary equations at the same actual gap \(\Delta\) (though possibly different targets) are \(Dw-Su=\Delta=D'w'-HSu'\) with all four rough parts in \([L,U)\).

Let \(G=\gcd(D,D')\), \(g=\gcd(G,S)\), \(A=D/G\), \(B=D'/G\), \(C=G/g\), \(V=S/g\). Because \(Hu'-u>0\) in the stated narrow window, subtracting the two equations gives one common positive integer \(\ell\) satisfying
\[
 Hu'-u=C\ell,\qquad Bw'-Aw=V\ell.
\]
This yields a necessary pairwise compatibility test even before checking the fixed value of \(\Delta\): for each feasible \(\ell\), intersect each side's coordinate range and permitted rough integers with the indicated linear relation. The least allowed \(u'\) minimizes both \(u,u'\), and the least allowed \(w'\) minimizes both \(w,w'\), by positivity of the coefficients. If these minima already violate either strict product inequality, no pair at that \(\ell\) can pass. Giving the minima the benefit of the doubt about pairwise gcd and fixed gap keeps the rejection sound. For a finite family of strata, draw an edge whenever a pair is not excluded. Any set of genuinely passing strata forms a clique, but an edge or clique is not a certificate for the actual gap.

When the moving prime is the same and \(E\ne E'\), \(C\) contains its full minimum-depth power; since the rough factors are units, the second equation also gives \(p\nmid\ell\) when \(p\nmid S,D_0\). For distinct additional primes the common gcd has no moving prime factor, and in the second equation both moving primes must be absent from \(\ell\) under the same unit assumptions. None of these pairwise tests licenses replacing the prescribed case-specific \(\Delta\).

## Exact product-sensitive compatibility example

At original labels \(X=3^{20}, Z=5^{14}\), use \(S=109,\ H=109,\ D=D'=1125\cdot11^2\). At \(\ell=16\) the two relations admit two loose pairs in the ordinary positive-height windows with rough parts that are panel units, \(1\bmod4\), and mutually coprime on each side. Both violate the strict product window. Their two free common gaps also differ from the actual \(Z-X=2616731224\), so neither can replace the original check. The example isolates the stronger product test rather than giving a new true representation.

```python
from math import gcd,isqrt
L,U=127*131,139*151
S,D=109,1125*121
X,Z=3**20,5**14
def prime(p):
    return all(p%d for d in range(2,isqrt(p)+1))
ps=[p for p in range(2,110) if prime(p)]
def ok(w):
    return L<=w<U and w%4==1 and all(w%p for p in ps)
ans=[]
for up in range(L,U):
    u=109*up-D*16
    if not (ok(u) and ok(up)):
        continue
    for w in range(L,U):
        wp=w+109*16
        n1,n2=X+1+D*w,X+1+D*wp
        if (ok(w) and ok(wp) and max(X,Z)+1<min(n1,n2)
            and max(n1,n2)<X+Z and gcd(u,w)==gcd(up,wp)==1):
            gap=D*w-S*u
            assert gap==D*wp-109*S*up and gap!=Z-X
            assert u*w>=L*U or up*wp>=L*U
            ans.append((u,w,up,wp,gap))
assert ans==[(19549,19237,20161,20981,2616505784),
             (20857,19237,20173,20981,2616363212)]
```
