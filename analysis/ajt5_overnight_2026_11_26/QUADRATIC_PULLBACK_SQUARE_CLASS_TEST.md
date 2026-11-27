# Global square-class test for a quadratic double-moving pullback

Use \(B=9633851\), \(H=9633860\), \(m=H/2\), and \(H F(s)=(s^2-2+im)^2+B\) at the [fixed actual label](MOVING_PARENT_QUARTIC.md). This F is irreducible over \(k=\mathbb Q(i)\) by the [root-field calculation](BOTH_ENDPOINTS_MOVING_DEG28.md). Write \(E=k(\sqrt B)\), \(u=2-im+i\sqrt B\), \(\alpha^2=u\) and \(L=E(\alpha)=k(\alpha)\).

For real rational \(a\ne0,\ b,\eta\), consider \(h(T)=a(T-\eta)^2+b\). By [Capelli's composition criterion](https://www.m-hikari.com/imf-password2009/37-40-2009/aliIMF37-40-2009.pdf), \(F(h)\) is reducible over k iff \((\alpha-b)/a\) is a square in L. Equivalently,
\[
  \exists q\in E:\quad q^2=b^2-u,\qquad (q-b)/(2a)\in E^{\times2}.
\]
In fact write a potential square root \(x+y\alpha\). Comparison gives \(2xy=1/a\), \(a(x^2+uy^2)=-b\), and putting \(q=a(x^2-uy^2)\) gives the displayed test. Conversely take \(x\) with square \((q-b)/(2a)\) and \(y=1/(2ax)\); the two coefficient identities follow. Neither x nor \(q-b\) can vanish. This is a test for reducibility, independent of finding an integer anchor where both rotated norm coordinates are integral. The known anchor is \(s_0=8404257\).

## Global obstruction and finite local compatibility

The first test forces \(N_{E/\mathbb Q}(b^2-u)=N_{\mathbb Q(i)/\mathbb Q}(H F(b))\) to be a rational square. If \(b\in\mathbb Z_3\), then the latter norm is 2 modulo 3 for every b; hence any globally viable b has a 3-adic pole. For the explicit anchored choice \(b=1/12,\ a=s_0-b,\ \eta=0\), the cleared norm is 6 modulo 17, a nonsquare, so \(F(h)\) is irreducible although \(h(1)=s_0\).

A finite list of local square tests cannot replace the global condition, even with that anchor imposed. For every finite set S of rational primes choose \(b\in\mathbb Q\) with sufficiently deep poles at those primes and put \(a=s_0-b\), \(\eta=0\). In every corresponding completion of L,
\[
       (\alpha-b)/(s_0-b)=1+(\alpha-s_0)/(s_0-b)
\]
is a square: the correction can be made arbitrarily small, so Hensel's lemma applies near 1 (for instance \(v(\text{correction})>2v(2)\)). The same h preserves the old anchor. If \(17\notin S\), b can in addition be chosen with \(b\equiv1/12\bmod17\), by choosing the numerator of a fraction with sufficiently large prime powers in its denominator via CRT. This gives a genuine finite-panel countercontrol with the same global obstruction at 17. Neither the criterion nor this example supplies a genuine reducible real quadratic pullback or a degree-eight integral two-moving trajectory.

~~~python
B,m=9633851,4816930
def norm(b,p):
    y=(b*b-2)%p
    return ((y*y+B-m*m)**2+(2*m*y)**2)%p
assert [norm(j,3) for j in range(3)]==[2,2,2]
p=17
b=pow(12,-1,p)
v=pow(12,8,p)*norm(b,p)%p
assert v==6 and all((t*t-v)%p for t in range(p))
~~~
