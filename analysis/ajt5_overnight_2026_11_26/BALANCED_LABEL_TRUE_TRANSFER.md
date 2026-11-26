# Balanced powers give actual same-target transfers at ordinary height

For each odd \(a\ge3\), choose \(b\ge1\) with \(5^{2b-1}<3^{2a}<5^{2b+1}\). Let \(A=3^a,B=5^b,M=\min(A,B)\). Because \(A+B\equiv0\bmod4\), both
\[
 x=(5A-3B)/4,\qquad z=(5B-3A)/4
\]
are integral, and \(z^2-x^2=B^2-A^2\). For every integer \(t\in[M/4,M/2]\) the single target \(n=1+B^2+x^2+t^2\) therefore has the two exact representations
\[
 n-1-B^2=x^2+t^2,\qquad n-1-A^2=z^2+t^2.
\]
These are actual exponent labels \((0,2b)\) and \((2a,0)\).

Since the ratio of larger to smaller power is below \(\sqrt5<7/3\), the coordinate corresponding to the smaller power in \(A^2-x^2=B^2-z^2\) has magnitude at most \(M/2\). Thus this common quantity is at least \(3M^2/4\). Both residuals are at least \(M^2/16\), and the target satisfies
\[
 \max(A^2,B^2)+1<n\le A^2+B^2+1-M^2/2<A^2+B^2<6M^2.
\]
Choosing \(t\) of opposite parity to \(x\) makes \(n\) odd and gives at least \(M/8-1\) distinct \(n\) for each choice of labels. This is a true ordinary-height family, not an arbitrary-\(n\) conclusion.

More generally, when the positive difference of residuals is divisible by four, a change of one square coordinate that preserves the other is characterized by factor pairs of that difference divided by four. If the original and new magnitudes are \(v<v'\), they have the same parity, and the positive integers \((k,m)=((v'-v)/2,(v'+v)/2)\) satisfy \(k\le m\) and \(4km=v'^2-v^2\); the converse uses \(v=m-k,v'=m+k\). A generic source representation need not have an eligible coordinate.

```python
A,B,t=27,25,8
x,z=(5*A-3*B)//4,(5*B-3*A)//4
n=1+B*B+x*x+t*t
assert (x,z,n)==(15,11,915)
assert n-1-B*B==15**2+8**2 and n-1-A*A==11**2+8**2
assert 799-1-B*B==13**2+2**2
assert 799-1-A*A==3*23  # Not a sum of two squares.
```
