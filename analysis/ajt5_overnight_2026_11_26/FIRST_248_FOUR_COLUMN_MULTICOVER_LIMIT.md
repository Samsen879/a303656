# A genuine four-column norm cover with only finitely many integral parameters

Start at [the four-column first-248 seed](FIRST_248_FOUR_COLUMN_SEED_AND_OLD_LIMIT.md), using the base columns \(d=4,16\). Set \(U_*=(36836,678599)\), \(G=(199569,-60944)\), \(g=\|G\|^2=43541956897\), \(q=G\cdot U_*=-34005213772\), and \(s_*=G^\perp\cdot U_*=137672257015\). Then \(q+g=(5^{16}-5^4)/16\). Just as for the previous pair construction, along the integer line \(G\cdot U=q\), \(m=5^{16}+1+4\|U\|^2\), the two base columns are always norms. The seed's prior obstructions can be preserved by restricting to \(U=U_*+4M'nG^\perp\), using the product \(M'\) of the seed's blocker squares.

On this line the three additional targets, first root 248 and columns \(d=8,12\), are \(f_i(s)=s^2+h_i\) times the respective Gaussian norm scalars \(20/g,4/g,4/g\), where \(s=G^\perp\cdot U\) and
\[
 h_0=q^2+g(5^{17}-239)/20,\qquad
 h_d=q^2+g(5^{16}-5^d)/4\quad(d=8,12).
\]
Take \(F_i=f_i(s_*)\), \(\lambda_i=1/F_i\), \(b=1/s_*\), \(u_i=s_*\lambda_i-b/2\) and \(a_i=\lambda_i-u_i^2\). The \(\lambda_i\) are norms by the genuine seed. For \(\xi=s-s_*\) the degree-eight cover defined by
\[
 Y_i^2=\xi(b+a_i\xi)\quad (i=0,8,12)
\]
simultaneously gives the three identities \(\lambda_i f_i(s)=(1+u_i\xi)^2+Y_i^2\). All \(a_i\) are positive and distinct, verified below. This is a genuine family of formal simultaneous norm identities; the exact seed remains a simultaneous arithmetic point.

## Integrality imposes finiteness for the separate-root model

More generally, consider a fixed cover with \(k\) independent radical polynomials \((s-s_*)a_j(s-\sigma_j)\) for distinct \(\sigma_j\ne s_*\), \(a_j\in\mathbb Q^\times\). Their square classes are independent even over the algebraic closure of the constant field, by the distinct simple second roots. The normalization has degree \(2^k\) over the s-line, simply ramifies at the \(k+1\) distinct points (all ramifications of index two) and does not ramify at infinity. At the shared first root the ratios of the radicands are units and hence are local squares over algebraically closed constants, so even there the index is only two. Riemann–Hurwitz gives \(2g_{\rm curve}-2=2^{k-1}(k-3)\); the parameter s has \(2^k\) distinct geometric poles. For \(k=2\) this is genus zero with four poles, and for \(k=3\) genus one with eight poles.

Every rational point on a fixed such cover with integral s has all rational \(Y_j\) integral outside the fixed primes of coefficient denominators (square valuations show this directly). The affine cover and its normalization away from infinity can use the same integral-point model after enlarging that finite set, because normalization is finite; the excluded singular fibers supply only finitely many s values. [Siegel's theorem for integral points on curves](https://annals.math.princeton.edu/wp-content/uploads/annals-v160-n2-p09.pdf) therefore gives only finitely many such points when \(k=2,3\). In particular the explicit three-square-root cover above cannot generate an unbounded integer four-column family despite its unbounded real branches. This is a statement about fixed covers of this shape, not about all arithmetic four-column points.

## A necessary locus for a shared quadratic cover

If instead all radicands share one second root \(\sigma\), a common cover has \(Y^2=a(s-s_*)(s-\sigma)\). At each target root \(\theta_i^2=-h_i\), the cover must give residue fields containing i above that point to permit a norm identity with a simple target zero. The field \(\mathbb Q(\theta_i)\) does not already contain i: each \(h_i\) is positive and nonsquare (for \(h_0\) the 2-adic valuation is odd; the other two have exact 2-adic valuation 3 and residue 12 modulo 16, respectively). When the cover does not ramify there, the residue extension thus must be the one adjoining i, or equivalently \(a(\theta_i-s_*)(\theta_i-\sigma)\) is a negative square in \(\mathbb Q(\theta_i)\). Taking its norm implies
\[
   w_i^2=(\sigma^2+h_i)/F_i\quad(i=0,8,12).
\]
As all \(\theta_i\) are nonreal, rational \(s_*,\sigma\) cannot ramify at them. The three distinct positive h give six distinct simple geometric branch points. This multiquadratic necessary locus has degree eight and genus five by Riemann–Hurwitz. Its rational solutions need not satisfy the full square-class tests or give an integral trajectory. Thus the common-cover route has an explicit remaining rational-point problem, rather than an automatic extension of the three-column Pell proof.

~~~python
from fractions import Fraction as F
a,b=199569,-60944
u,v=36836,678599
g,q,s=a*a+b*b,a*u+b*v,-b*u+a*v
assert (g,q,s)==(43541956897,-34005213772,137672257015)
assert q+g==(5**16-5**4)//16
assert 5**16+1+4*(u*u+v*v)==2000001865414
hs=[q*q+F(g*(5**17-239),20)]
hs+=[q*q+F(g*(5**16-5**d),4) for d in (8,12)]
assert len(set(hs))==3 and min(hs)>0
assert hs[0].denominator%2==0 and hs[0].numerator%2==1
assert all(h.denominator==1 for h in hs[1:])
assert hs[1]%16==8 and hs[2]%16==12
coefs=[]
for h in hs:
    lam=1/(s*s+h)
    u=s*lam-F(1,2*s)
    coefs.append(lam-u*u)
assert min(coefs)>0 and len(set(coefs))==3
~~~
