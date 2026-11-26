# Cubic pullbacks: exact tests, a splitting restriction, and genus bounds

Use \(k=\mathbb Q(i)\), \(E=\mathbb Q(i,\sqrt B)\), \(u=2-im+i\sqrt B\), \(\alpha^2=u\) and \(L=E(\alpha)\) at the fixed actual label of [the rank-zero certificate](QUADRATIC_VERTEX_RANK_ZERO_CERTIFICATE.md). In particular \([L:\mathbb Q]=8\): the four conjugates \(2\pm i(m\pm\sqrt B)\) of u are distinct and u is nonsquare in E.

For \(h(T)=a(T^3+PT+Q)\) after rational input translation, \(f(h)\) is reducible over k iff \(h(T)-\alpha\) has a root in L, by Capelli and the cubic degree. A root \(\beta=x+y\alpha\) must satisfy
\[
 x(x^2+3uy^2+P)+Q=0,\qquad ay(3x^2+uy^2+P)=1.
\]
For \(Q\ne0\) necessarily \(x\ne0\). Eliminating y gives the following exact condition: for some \(x\in E^\times\), write \(D_x=8x^3+2Px-Q\) and require
\[
 D_x\ne0,\qquad a^2(x^3+Px+Q)D_x^2=-27x^3u.
\]
Indeed then \(y=3x/(aD_x)\) satisfies the two original equations. This also proves \(\mathbb Q(x)=E\), since the displayed equation recovers u from x. Finding such a root alone does not give an integral orbit; its input must additionally attain a genuine integer anchor.

## Odd cubic coordinates

If \(h=aT^3+cT\), the involution \(\tau\) of \(L/E\) maps roots of \(h(T)-\alpha\) to roots of \(h(T)+\alpha\). Thus \(\beta\mapsto-\tau\beta\) is an involution on the roots in L. If it exchanges two roots, the sum-zero relation gives a third root fixed under this involution. Hence reducibility is equivalent to a root \(y\alpha\); writing \(w=1/y\) gives \(w^3-cw^2=au\). The split prime 17 in E has one component of u of valuation one and the other three of valuation zero, as verified below. No rational scaling a makes all four divisible by three, so \(c=0\) never works in this model.

For \(c\ne0\), set \(z=w/c,\ t=a/c^3\). The exact condition becomes \(z^2(z-1)=tu\) in E with \(t\in\mathbb Q^\times\). Necessarily \(v_{17}(t)\ge0\): a negative valuation at a unit component would have to be divisible by 3 (because the left side at negative valuation has valuation \(3v(z)\)); in the exceptional component it then differs by one and stays negative, a contradiction.

A reducible odd cubic has exactly one root in L. For the normalized monic cubic its discriminant is \(\Delta=(-4-27tu)/t^3\). It is not a square in E: any square of the form \(r+i\gamma(m-\sqrt B)\) with rational \(r,\gamma\ne0\) would give the same rank-zero contradiction after the elliptic reduction in the linked note, scaled by \(\gamma\) (the two squared differences become \(B\gamma^2,m^2\gamma^2\)). Nor is \(\Delta/u\) a square in E: set \(e=v_{17}(t)\ge0\). If e is even, at the exceptional component it has odd valuation \(-3e-1\); if e is odd, at a unit component it has odd valuation \(-3e\). These are the only two ways for \(\Delta\in E\) to become square in \(L=E(\sqrt u)\). Thus the cubic cannot split completely in L; if reducible there, its factors have degrees 1 and 2. The corresponding \(f(h)\) has factors of degrees 4 and 8 over k.

## Finite number of normalized parameters at a fixed center

Over algebraically closed constants the restriction-of-scalars equation for the odd case gives the fiber product of the four cubics \(z_j^2(z_j-1)=t u_j\), where \(u_j\) are the conjugates of u. Each map has transposition inertia at 0 and at \(-4/(27u_j)\), and a 3-cycle at infinity. Each of the four nonzero finite branch values is distinct, giving a single-factor transposition in the joint monodromy. The projections are each all of \(S_3\); conjugating each single-factor transposition in the joint group generates the entire corresponding \(S_3\). Thus the joint action is the full product, and the cover is geometrically connected of degree \(3^4\). For r factors the degree is \(N=3^r\), and the respective inertia defects are \((N-1)/2\) at zero, \(N/3\) at each of r separate finite places, and \(2N/3\) at infinity. [Riemann–Hurwitz](https://stacks.math.columbia.edu/tag/0C1B) gives genus 21 at \(r=4\). By [Faltings's finiteness theorem](https://geodesic.mathdoc.fr/item/IM_1983__73_143051/), only finitely many nonzero rational t can be reducible, after normalization by input scale. This does not compute them.

For a fixed nonzero rational center value b in \(aT^3+cT+b\) and \(c\ne0\), the analogous exact equation is \(z^2(z-1)=t(\alpha-b)^2\) in L, with \(z=(\alpha-b)/(c\beta)\). Now all eight constants \((\alpha_j-b)^2\) are distinct. A collision would give two distinct roots \(\alpha_j+\alpha_\ell=2b\), requiring opposite imaginary parts and equal real-part magnitudes (since \(\Re(\alpha_j^2)=2\)). Since \(b\ne0\), both real parts would be b. This makes \(\Im(\alpha_j)^2=b^2-2\) rational, whereas \((2b\Im(\alpha_j))^2=(\pm m\pm\sqrt B)^2\) is irrational. Therefore the same branch calculation at \(r=8\) gives genus 6015 and finite normalized parameters for this fixed b. For \(c=0\), two admissible leading coefficients would have ratio a rational number which is a cube in the degree-eight field L, and hence a rational cube by the degree of an irreducible pure cubic. This only bounds each fixed center separately. No reducible anchored cubic or degree-12 integer trajectory is constructed here.

~~~javascript
const m=4816930n,B=9633851n,p=17n;
const mod=(x,p)=>(x%p+p)%p;
const bits=[];
for(let i=0n;i<p;i++)for(let r=0n;r<p;r++)
  if(mod(i*i+1n,p)===0n&&mod(r*r-B,p)===0n)
    bits.push([i,r,mod(2n-i*m+i*r,p)].join(","));
if(bits.join(";")!=="4,6,4;4,11,7;13,6,0;13,11,14")
  throw Error("split prime data");
const norm=(4n-m*m+B)**2n+16n*m*m;
if(norm%(p*p)!==51n)throw Error("valuation data");
for(const [r,g] of [[4,21],[8,6015]]){
  const N=3**r,d=(N-1)/2+r*N/3+2*N/3;
  if(1+(-2*N+d)/2!==g)throw Error("genus data");
}
~~~
