# Pell normalization for a negative determinant and fixed-label controls

Let $S$ be an integral symmetric matrix with determinant $-D<0$, where $D$ is a positive nonsquare integer. A nontrivial Pell solution $t^2-Du^2=1$ gives a determinant-one integral automorphism $P=tI+uJS$, with $J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)$. In fact $(JS)^2=DI$, $(JS)^tS+S(JS)=0$, and therefore $P^tSP=S$.

A useful consequence for a fixed orbit is the following balancing statement. If the entries of $A^t\gamma^tS\gamma A$ are $O(X)$ for $\gamma\in\mathrm{SL}_2(\mathbb Z)$ and $A\in\mathrm{SL}_2(\mathbb R)$, there is a representative $P^j\gamma$ in the same orbit with $\|P^j\gamma A\|=O_S(\sqrt X)$. To see this, diagonalize $P$ over $\mathbb R$ along the two $S$-null directions, with eigenvalues $\lambda,\lambda^{-1}$ and $\lambda>1$ (choose a positive Pell solution). In this basis the form is an off-diagonal matrix with nonzero off-diagonal coefficient. Let $v,w$ be the two row vectors of $\gamma A$ in this basis. The square of the Frobenius norm of $v^tw+w^tv$ is $2\|v\|^2\|w\|^2+2(v\cdot w)^2$, so the matrix-entry bound implies $\|v\|\|w\|=O_S(X)$. Multiplication by $P^j$ scales the rows inversely. Choose $j$ so their norm ratio is bounded above and below by constants depending only on $\lambda$. This proves the claimed size bound.

For the actual label $K=10937-3^{10}=-48112$, the prime $p=103$ gives the positive norm $5p^2+K=33^2+62^2$. At $p=139$ the value instead factors as $71\cdot683$, two distinct inert primes. This produces the integral matrix $S$ below, of determinant $5K=-240560$, and the replay checks a concrete Pell automorphism. A second fixed label checks that selecting even valuation at $3$ still allows failure at other primes.

This note verifies an algebraic component and finite controls for a possible analytic counting argument. It does not assert the prime lower bound, an unconditional positive density, or a result for the entire growing family.

```python
from math import isqrt

def prime(v):
    return v > 1 and all(v % d for d in range(2, isqrt(v)+1))

def mul(X,Y):
    return [[sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def tr(X):
    return list(map(list,zip(*X)))
def det(X):
    return X[0][0]*X[1][1]-X[0][1]*X[1][0]

K=10937-3**10
assert K==-48112
p,q,r=139,71,683
assert all(prime(v) and v%4==3 for v in (p,q,r))
assert 5*p*p+K==q*r==48493
assert 5*103**2+K==33**2+62**2
S=[[q,5*p],[5*p,5*r]]
J=[[0,-1],[1,0]]
D=240560
t,u=3198920319,6522164
assert det(S)==-D and isqrt(D)**2!=D and t*t-D*u*u==1
JS=mul(J,S)
P=[[u*JS[i][j]+(t if i==j else 0) for j in range(2)] for i in range(2)]
assert det(P)==1 and mul(mul(tr(P),S),P)==S
for p,v in [(67,2),(7,1),(12919,2)]:
    assert prime(p)
    F=5*p*p+10936
    assert F%3**v==0 and F%3**(v+1)!=0
assert 5*67**2+10936==90**2+159**2
assert 5*12919**2+10936==9*2399*38651
assert all(prime(v) and v%4==3 for v in (2399,38651))
```
