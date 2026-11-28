# Modulo 11 closes the fixed-anchor cubic models at slopes ±3

Use the four offsets and anchors from [#88](https://github.com/Samsen879/a303656/pull/88): \(s_i=a_iS^4+b_iR^4\), with \((a_i,b_i)=(1,9),(5,81),(25,1),(125,729)\), and \(A_i(S,R)=\ell_iS^2+m_iR^2\) with the vectors in the replay below. Write \(N(x,y)=x^2+y^2\). For each \(\lambda\in\{3,-3\}\), suppose \(P_i\in\mathbb Q[S,R,t]^2\) are homogeneous cubics satisfying \(P_i(S,R,0)=(S+\lambda R)A_i\), and all four \(N(P_i)/(S+\lambda R)^2+s_i\) coincide as rational functions. Then \(P_i=(S+\lambda R)A_i\) for every \(i\). This excludes every nonconstant deformation in this fixed model, including those with denominator cancellation, and does not rule out new integer specializations, higher-degree numerators, or other slopes and anchors.

The formal \(7\)-adic branches in [#108](https://github.com/Samsen879/a303656/pull/108) remain valid. They are local formal identities, and are compatible with this polynomial obstruction at another prime.

## Exact coefficient elimination


It suffices to treat \(S+3R\). The substitution \(S\mapsto-S\), followed by negating each numerator, exchanges the slopes and preserves the anchors and labels. Set \(R=1,\ X=S+3\), let \(A_i=\ell_i(X-3)^2+m_i\), and write
\[
P_i=XA_i+tB_i+t^2C_i+t^3E_i,
\qquad \deg_X(B_i,C_i,E_i)\le(2,1,0).
\]
The constant coefficient of \(N(P_i)+X^2s_i\) is already shared. The remaining coefficients must each be independent of \(i\).

| Power | Coefficient |
|---|---|
| \(t\) | \(2X A_i\cdot B_i\) |
| \(t^2\) | \(N(B_i)+2X A_i\cdot C_i\) |
| \(t^3\) | \(2(B_i\cdot C_i+X A_i\cdot E_i)\) |
| \(t^4\) | \(N(C_i)+2B_i\cdot E_i\) |
| \(t^5\) | \(2C_i\cdot E_i\) |
| \(t^6\) | \(N(E_i)\) |

The reduction uses three exact linear solves.

1. **Recover \(B_i\).** Its value at \(X=0\), together with the shared quartic \(F=A_i\cdot B_i\), determines \(B_i\). After removing the prescribed value, divide by \(X\) and solve for a linear vector. The map \(C\mapsto A_i\cdot C\) from linear vectors to cubics is invertible because \(\ell_i,m_i\) are independent.
2. **Solve \(t^3\) before constructing \(E_i\).** The shared \(t^2\) polynomial \(G\) has \(G(0)=N(B_i(0))\). For fixed \(B_i\), its other four coefficients determine \(C_i\) via \(2A_i\cdot C_i=(G-N(B_i))/X\). Put \(U_i=B_i\cdot C_i\). Since \(XA_i\cdot E_i\) lies in \(\operatorname{span}\{X,X(X-3)^2\}\), the exact \(t^3\) compatibility conditions are that
   \[
   (U_{i,0},\ U_{i,2}+6U_{i,3})
   \]
   be shared. These give six linear equations on the four remaining coefficients of \(G\).
3. **Solve \(t^4\) in two variables.** Let \(h_1,h_3\) be the \(X,X^3\) coefficients of the shared half-\(t^3\) polynomial. Recover \(E_i\) from
   \[
   A_i(0)\cdot E_i=h_1-U_{i,1},\qquad
   \ell_i\cdot E_i=h_3-U_{i,3}.
   \]
   The \(t^4\) equations are then linear in \((h_1,h_3)\). Check \(t^5,t^6\) on the resulting solutions.

Modulo 11, all four anchor matrices are invertible. Normalizing the first nonzero coefficient of \(F\) to 1 by rescaling \(t\), the enumeration gives:

| Stage | Survivors |
|---|---:|
| Normalized \(B\) tuples | 704,233 |
| \(B\) tuples compatible with \(t^3\) | 7,162 |
| Compatible \((B,C)\) tuples | 36,322 |
| \((B,C)\) tuples compatible with \(t^4\) | 1, namely \(B=C=0\) |
| Full \((B,C,E)\) tuples | 1, the zero deformation |

To pass from \(\mathbb Q\) to this check, suppose a nonzero rational deformation exists and take \(\pi^6=11\). For each nonzero scalar coefficient \(c\) in the \(t^j\) part, form \(6v_{11}(c)/j\). Their minimum \(e\) is an integer since \(j\in\{1,2,3\}\). Replacing \(t\) by \(\pi^{-e}t\) makes all coefficients integral at \(\pi\), with at least one positive-\(t\) coefficient a unit. Reduction modulo \(\pi\) gives a nonzero deformation over \(\mathbb F_{11}\), a contradiction. This argument keeps the anchor fixed.

## Executable replay

The synthetic control adds a common cubic numerator increment whose other coordinate makes every extra norm coefficient shared. It tests a genuine nonzero deformation over the integers; its anchors are intentionally different from the actual labels tested above. Run the following with Python 3 and assertions enabled.

```python
from itertools import product
p = 11

def solutions(A,n):
    A = [list(row) for row in A]
    piv = []
    for j in range(n):
        i = len(piv)
        k = next((k for k in range(i,len(A)) if A[k][j]),None)
        if k is None:
            continue
        A[i],A[k] = A[k],A[i]
        z = pow(A[i][j],-1,p)
        A[i] = [a*z%p for a in A[i]]
        for k,row in enumerate(A):
            if k != i and row[j]:
                A[k] = [(a-row[j]*b)%p for a,b in zip(row,A[i])]
        piv.append(j)
    if any(row[n] for row in A[len(piv):]):
        return
    free = [j for j in range(n) if j not in piv]
    for v in product(range(p),repeat=len(free)):
        x = [0]*n
        for j,t in zip(free,v):
            x[j] = t
        for i,j in enumerate(piv):
            x[j] = (A[i][n]-sum(A[i][k]*x[k] for k in free))%p
        yield x

def inverse(A):
    n = len(A)
    return list(zip(*(next(solutions(
        [list(r)+[i==j] for i,r in enumerate(A)],n)) for j in range(n))))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))%p

def mv(A,v):
    return [dot(row,v) for row in A]

def pairs(v):
    return list(zip(v[::2],v[1::2]))

def conv(A,B):
    c = [0]*(len(A)+len(B)-1)
    for i,a in enumerate(A):
        for j,b in enumerate(B):
            c[i+j] += dot(a,b)
    return [x%p for x in c]

def diff(u,v):
    return [(a-b)%p for a,b in zip(u,v)]

def setup(ell,mm):
    A = [(((9*e[0]+m[0])%p,(9*e[1]+m[1])%p),
          tuple(-6*x%p for x in e),tuple(x%p for x in e))
         for e,m in zip(ell,mm)]
    K = [inverse([list(a[k] if k<3 else (0,0))
                  +list(a[k-1] if k else (0,0)) for k in range(4)]) for a in A]
    W = [inverse([a[0],a[2]]) for a in A]
    return A,K,W

def test(B,K,W,actual=False):
    Ns = [conv(b,b)[1:] for b in B]
    R = []
    for (u,v,w),k,n in zip(B,K,Ns):
        d = [(a+6*b)%p for a,b in zip(v,w)]
        L = [[dot(a,c) for c in zip(*k)] for a in ([*u,0,0],[*w,*d])]
        R.append([a+[dot(a,n)] for a in L])
    for g in solutions([diff(r[j],R[0][j]) for r in R[1:]
                        for j in range(2)],4):
        C = [pairs(mv(k,[(x-y)*6%p for x,y in zip(g,n)]))
             for k,n in zip(K,Ns)]  # 6 = 1/2 mod 11
        U = [conv(b,c) for b,c in zip(B,C)]
        rows = []
        for b,c,w,u in zip(B,C,W,U):
            e = mv(w,[(-u[1])%p,(-u[3])%p])
            h,j = zip(*w)
            rows.append([[2*dot(x,h)%p,2*dot(x,j)%p,(-v-2*dot(x,e))%p]
                         for x,v in zip(b,conv(c,c))])
        for h in solutions([diff(r[j],rows[0][j]) for r in rows[1:]
                            for j in range(3)],2):
            if actual:
                assert all(not any(z) for row in B+C for z in row)
            E = [mv(w,diff(h,[u[1],u[3]])) for w,u in zip(W,U)]
            if (len({tuple(conv(c,[e])) for c,e in zip(C,E)})==1
                and len({dot(e,e) for e in E})==1):
                yield C,E

A,K,W = setup(((20,7),(21,2),(19,8),(17,6)),
              ((0,87),(21,84),(59,-64),(57,-60)))
V = list(product(range(p),repeat=2))
fs = list(product(range(p),repeat=4))
counts = [0,0]
for L,G in product((0,1),range(p)):
    opts = [[v for v in V if dot(a[0],v)==L and dot(v,v)==G] for a in A]
    if not all(opts):
        continue
    assert L or G==0
    for v in product(*opts):
        base = [conv(a,[u])[1:]+[0,0] for a,u in zip(A,v)]
        for f in fs:
            if L==0 and next((j for j in f if j),1)!=1:
                continue
            B = [[u]+pairs(mv(k,diff(f,b))) for u,k,b in zip(v,K,base)]
            counts[0] += 1
            for C,E in test(B,K,W,actual=True):
                counts[1] += 1
                assert all(not any(e) for e in E)
assert counts == [704233,1]

_,K,W = setup(tuple((1,u) for u in (1,2,4,5)),
              tuple((1,u) for u in (20,10,5,4)))
assert any(C==[[(1,0),(0,0)]]*4 and E==[[1,0]]*4
           for C,E in test([[(1,0),(0,0),(0,0)]]*4,K,W))
print("PASS",counts)
```
