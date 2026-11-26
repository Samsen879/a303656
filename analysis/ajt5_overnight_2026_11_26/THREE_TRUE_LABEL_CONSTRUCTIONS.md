# Two mechanisms for three genuine labels at the same target

All representations below use the actual bases 3 and 5 and positive integer residuals. These are explicit families of targets, not an arbitrary-target claim.

## Balanced-label transfer followed by a 3–4–5 rotation

Take \(a\equiv3\bmod8,\ b\equiv2\bmod8\) with \(0.9<B/A<1.1\), where \(A=3^a,B=5^b\). For each odd \(1\le j<b\), set \(C=5^{b-j}\) and
\[
 x=(5A-3B)/4,\quad z=(5B-3A)/4,\quad
 t=(5C-3z)/4,\quad w=(5z-3C)/4 .
\]
For integrality use \(A\equiv27,B\equiv25\bmod32\), so \(x\equiv7,z\equiv3\bmod8\), and \(C\equiv5\bmod8\). In particular \(t\) is even. The two identities
\[
 z^2-x^2=B^2-A^2,\qquad (4z-3t,3z+4t)=(5w,5C)
\]
give the following three true residuals for \(n=1+B^2+x^2+t^2\):
\[
 n-1-B^2=x^2+t^2,\quad
 n-1-A^2=z^2+t^2,\quad
 n-A^2-C^2=w^2+1 .
\]
On the balance range, \(x,z,w>0.3A,\ |t|<15A/32\), and \(x^2+t^2<9A^2/16\) (use \(x<23A/40\)). Consequently the odd target lies strictly between \(\max(A^2,B^2)+1\) and \(A^2+B^2\), at distance \(>A^2/3\) below the latter, and all residuals are \(>9A^2/100\). The allowed ratio recurs for infinitely many \(a,b\) in their prescribed progressions by irrational rotation, since \(\log3/\log5\) is irrational. As odd \(j\) increases, \(t<0\) and \(|t|\) strictly increases, giving \(b/2\) distinct targets at each balanced pair. This extends [the two-label construction](BALANCED_LABEL_TRUE_TRANSFER.md). The initial two labels alone do not imply the third: the previous \(n=915\) has the first two norms but gives 161 at the third label for \(a=3,b=2,j=1\), with odd valuations at 7 and 23.

## Shared Gaussian factor, without assuming a pure-power center

Take \(C\equiv1\bmod4,\ C\ge9\), odd \(D\ge3\), positive \(t\equiv5\bmod30\), and \(n=3^C+5^D+2t^2\). The source at \((C,D)\) is \(t(1+i)\). The two downward jumps to \(C-1,C-5\) have increments \(2s^2\) with \(s=3^{(C-1)/2},11\cdot3^{(C-5)/2}\); this uses \(3^5-1=2\cdot11^2\). Thus both new Gaussian certificates are \((1+i)(t+is)\) with the appropriate \(s\). The target is \(2\bmod8,3\bmod5\), ruling out a sum of the two powers with both square terms zero. Taking the largest exponents in their progressions with each power at most \(X/4\), and \(X/8\le2t^2\le X/4\), yields \(\gg\sqrt X\) distinct targets up to \(X\) with both exponents of order \(\log X\).

A cross-axis variant takes even \(c\ge4\), odd \(d\ge3\), \(t>0\) coprime to 30, and \(n=3^{c+4}+5^{d+1}+5t^2\). The two increments from \((c+4,d+1)\) down the two axes are \(5(4\cdot3^{c/2})^2\) and \(5(2\cdot5^{(d-1)/2})^2\); use the shared Gaussian factor \(2+i\). These targets are odd, so also cannot equal just \(3^u+5^v\).

```python
def rotate(a,b,j):
    A,B,C=3**a,5**b,5**(b-j)
    assert 9*A<10*B<11*A
    numer=(5*A-3*B,5*B-3*A)
    assert all(q%4==0 for q in numer)
    x,z=(q//4 for q in numer)
    assert (5*C-3*z)%4==(5*z-3*C)%4==0
    t,w=(5*C-3*z)//4,(5*z-3*C)//4
    n=1+B*B+x*x+t*t
    assert n==1+A*A+z*z+t*t==A*A+C*C+w*w+1
    assert n%2==1 and 3*(A*A+B*B-n)>A*A
    return n

assert rotate(3,2,1)==855
assert len({rotate(331,226,j) for j in range(1,226,2)})==113
assert 915-3**6-5**2==7*23

def shared(C,D,t,x,y,targets):
    g=x*x+y*y
    n=3**C+5**D+g*t*t
    for c,d,s in targets:
        assert (x*t-y*s)**2+(y*t+x*s)**2==n-3**c-5**d>0
    return n

assert shared(9,3,5,1,1,[(8,3,81),(4,3,99)])==19858
assert shared(8,4,1,2,1,[(4,4,36),(8,3,10)])==7191
```
