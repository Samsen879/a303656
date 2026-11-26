# Shared-modulus separators can remove high overlap from exact phase counting

Use the [boundary-aware finite pre-lift test](BOUNDARY_CRT_ELIMINATION.md). Suppose each row \(p_i\) has free mod-\(p_i\) order \(m\ell_i\) on both axes, with \(m\) fixed and the \(\ell_i\) distinct primes not dividing \(m\). Thus the free period is \(T=m\prod_i\ell_i\) on each axis. Assume \(p_i\nmid T\) and \(p_i\) divides both boundary strides \(B_3,B_5\). Consequently the cutoff is \(t_i=\min_b(v_{p_i}(b^{o_{b,p_i}}-1)+v_{p_i}(B_b))\ge2\), with \(o_{b,p_i}\) the original order at \(p_i\). At this cutoff the entire row reads just the two coordinates modulo \(m\ell_i\): the LTE order of \(b^{B_b}\) has no extra \(p_i\)-power at that depth.

Condition on the two shared mod-\(m\) coordinates \(u,v\). Let \(b_i(u,v)\) count the row's bad cells among the private \(\ell_i^2\) pairs. The count of passing pairs is exactly
\[
\sum_{u,v\bmod m}\,\prod_i\bigl(\ell_i^2-b_i(u,v)\bigr).
\]
CRT is the only independence needed: private coordinates now vary freely and independently across rows, even if all unconditioned row events overlap. Fixing one private coordinate, the other axis contributes \(\ell_i\) distinct powers modulo \(p_i\), so at most one of them can create a root. Thus \(b_i\le\ell_i\) and every shared boundary extends, even with all residuals units modulo their respective row primes. With a modular lookup table only \(\ell_i\) local collision candidates need exact-depth testing per row and shared cell. This is an exact finite separator statement; it does not by itself bound least ordinary-height witnesses or prove that general full prefixes have bounded separators.

## Two real rows

For the original bases \(3,5\), take \(m=7,\ p_1=463,\ p_2=911,\ \ell_1=11,\ell_2=13\), and
\[
 c=4+12653790x,\qquad d=37961370y,\qquad T=1001.
\]
For \(n\equiv896668227339\bmod4269824036376\) each depth is two. The individual \(77^2\) and \(91^2\) grids have 14 and 8 bad cells; both reject \(x=y=0\). The shared slice tables have overlap count 2 in the full \(1001^2\) grid. The separator formula gives 998669 passing cells. The residue class admits the true square-sum construction
\[
 n=3^{12653794}+1+
  (177909334849+4269824036376H)^2+1303306550260^2,
\]
and by making \(H\) large one can activate all displayed exponent representatives. This is a finite two-row control and puts no condition on outside primes.

```python
from math import gcd
ps=(463,911); ls=(11,13); B3,B5=12653790,37961370
n,M=896668227339,4269824036376
def order(b,p):
    return next(k for k in range(1,p) if pow(b,k,p)==1)
C=[]
for p,l,o in zip(ps,ls,(462,455)):
    assert M%(p*p)==0
    for b,B in ((3,B3),(5,B5)):
        assert order(b,p)==o and pow(b,o,p*p)!=1
        assert o//gcd(o,B)==7*l and B%p==0 and B%(p*p)!=0
    tab=[0]*49
    for x in range(7*l):
        for y in range(7*l):
            r=(n-pow(3,4+B3*x,p*p)-pow(5,B5*y,p*p))%(p*p)
            if r and r%p==0:
                tab[(x%7)*7+y%7]+=1
    C.append(tab)
    assert (n-82)%(p*p) in range(p,p*p,p)
a,b=C
assert (sum(a),sum(b),sum(x*y for x,y in zip(a,b)))==(14,8,2)
assert sum((121-x)*(169-y) for x,y in zip(a,b))==998669
assert (pow(3,12653794,M)+1+177909334849**2+1303306550260**2)%M==n
```
