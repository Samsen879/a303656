# A true thin-axis rectangle and a translation-invariant forbidden menu

Two independent exact arithmetic observations. They distinguish removal of a local restriction from producing a complete rectangle of positive integer norms.

## Local release and a genuine finite rectangle

For each \(k\), let \(D_k=\{0,2,\ldots,2k-2\}\) and let \(C_k\) be the first \(k\) nonnegative even integers not congruent to 4 mod 6. Then \(3^{C_k}\subseteq\{1,2\}\) mod 7 and \(5^{D_k}\subseteq\{1,2,4\}\) mod 7. The sumset avoids 1. For every \(k\), every \(n\equiv1\bmod7\) above the activation threshold therefore has all remainders positive and units at 7. This leaves all other norm conditions to prove.

At \(n=24396\) the axes \(C=\{0,2,6,8\}\), \(D=\{0,2,4,6\}\) give a genuine \(4\times4\) sum-of-two-squares rectangle. Each cell below verifies the actual equality on the same \(n\). The old label \((4,2)\) at this very \(n\) has remainder \(24290\equiv35\bmod49\), exact odd valuation 1. This is an exact release of the old 7-adic issue, not a proof that both axes can grow unboundedly in a true rectangle.

## An absolute translated forbidden pattern

For all nonnegative shifts \(c_0,d_0\), the menu containing the whole product of
\[
c_0+\{0,2,\ldots,20\}\quad\text{and}\quad
d_0+\{0,4,5,6,10,11,12,16,17,18\}
\]
cannot give a complete Gaussian norm rectangle at any integer \(n\). Write \(A=3^{c_0},B=5^{d_0}\), \(X_i=9^i,Y_j=5^{e_j}\). For each of the \(22\cdot23\) pairs \((\lambda,u)=(A/B,n/B)\bmod23\), the exact replay finds three cells on \(\lambda X_i+Y_j=u\) whose differences form a determinant divisible by 23 but not by \(23^2\). If the three actual remainders were norms, each would be divisible by \(23^2\) (also true for literal zero). Subtracting the rows would give a matrix \(M\) with \(M(A,B)^\top=0\bmod23^2\). Multiplying by its adjugate implies \(23\mid A,B\), impossible. The same certificate applies to \(x^2+2y^2\), since \(-2\) is also a nonsquare mod 23. No search over heights is needed.

## Minimal exact replay

~~~python
from itertools import combinations

def check(ok):
    if not ok:
        raise ValueError("certificate failed")

C, D = (0,2,6,8), (0,2,4,6)
W = [[(75,137),(31,153),(19,153),(11,93)],
     [(19,155),(71,139),(31,151),(29,89)],
     [(95,121),(29,151),(29,149),(11,89)],
     [(47,125),(11,133),(7,131),(1,47)]]
n = 24396
for i,c in enumerate(C):
    for j,d in enumerate(D):
        x,y = W[i][j]
        check(3**c+5**d+x*x+y*y == n)
check(n % 7 == 1 and (n-3**4-5**2) % 49 == 35)

p, pp = 23, 529
X = [pow(9,i,pp) for i in range(11)]
Y = [pow(5,j,pp) for j in (0,4,5,6,10,11,12,16,17,18)]
for l in range(1,p):
    for u in range(p):
        F = [(x,y) for x in X for y in Y if (l*x+y-u) % p == 0]
        check(len(F) >= 3)
        a,b = F[0]
        V = [(x-a)*(w-b)-(z-a)*(y-b) for (x,y),(z,w) in combinations(F[1:],2)]
        check(any(v % p == 0 and v % pp != 0 for v in V))
check(pow(-2,11,23) == 22)
~~~

All 16 finite norm coordinates, the exact odd-valuation control, and all 506 directions were independently replayed in exact integer arithmetic. This note does not rely on the larger offline bundle or adopt its stronger local-height claims.
