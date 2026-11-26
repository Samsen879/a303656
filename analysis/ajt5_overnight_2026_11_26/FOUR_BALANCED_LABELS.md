# Four actual labels in the balanced rotation family

For the balanced-power construction in [THREE_TRUE_LABEL_CONSTRUCTIONS.md](THREE_TRUE_LABEL_CONSTRUCTIONS.md), we have the exact identity
\[
 n=1+B^2+x^2+t^2=1+A^2+C^2+w^2,\qquad
 A=3^a,\ B=5^b,\ C=5^{b-j}.
\]
It immediately gives a fourth true label: interchanging the roles of the square \(A^2\) and the base-3 power 1 in the right expression gives \((0,2(b-j))\) with residual \(w^2+A^2\). All four labels are distinct for \(0<j<b\). For \(n=855\) the four residuals are \(229,125,101,829\).

There is a fixed integer-coordinate rotation on an infinite subfamily. Take
\[
 a\equiv27,\ b\equiv162\pmod {216},\qquad j=45,\qquad 0.9<B/A<1.1.
\]
With the prior coordinates \(z=(5B-3A)/4,\ w=(5z-3C)/4\), these congruences give \(A=B=1,\ C=63,\ z=55,\ w=76\bmod109\). Therefore for both \(y=1\) and \(y=A\),
\[
 ((60w-91y)/109,\ (91w+60y)/109)
\]
is integral and has norm \(w^2+y^2\), since \(60^2+91^2=109^2\). Since \(0.3A<w<25A/32\), both coordinates in each of these two representations have absolute value of order \(A\) as \(A\) grows. This changes the certificates, not the underlying residuals or their density.

Irrational rotation gives balanced choices with bounded gaps in the allowed \(a\)-progression: the backwards iterates of the nonempty open balance interval cover the circle, and compactness gives a finite subcover. Thus for each sufficiently large \(X\) there is a member of this constructed family with \(n\le X\) and \(n\asymp X\), since \(A^2<n<(221/100)A^2\). In particular all nonzero power labels in these four representations have their respective \(\log_3 X\) or \(\log_5 X\) exponent scale with bounded additive error when \(j\) is fixed. This does not claim a representation for any prescribed \(n\).

```python
def div(x,d):
    q,r=divmod(x,d)
    assert r==0
    return q

def check(a,b,j,rotate):
    A,B,C=3**a,5**b,5**(b-j)
    assert 9*A<10*B<11*A
    x,z=div(5*A-3*B,4),div(5*B-3*A,4)
    t,w=div(5*C-3*z,4),div(5*z-3*C,4)
    n=1+B*B+x*x+t*t
    def pair(y):
        return (div(60*w-91*y,109),div(91*w+60*y,109)) if rotate else (w,y)
    rows=[(0,2*b,x,t),(2*a,0,z,t),
          (2*a,2*(b-j),*pair(1)),(0,2*(b-j),*pair(A))]
    assert len({(e,d) for e,d,_,_ in rows})==4
    assert all(n-3**e-5**d==u*u+v*v for e,d,u,v in rows)
    return n

assert check(3,2,1,False)==855
assert check(45171,30834,45,True).bit_length()==143190
```
