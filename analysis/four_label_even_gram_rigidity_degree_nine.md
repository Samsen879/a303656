# Fixed-anchor even-quartic Gram rigidity through degree nine

**Degree eight is excluded for the fixed-anchor even-quartic Gram model.** The rigidity bound therefore extends from degree seven to **degree nine**, since odd degrees are already excluded by positivity. The next possible degree is ten, with a rank-one highest coefficient. The result allows arbitrary rational denominators in the original square coordinates, as in the descent in [#117](https://github.com/Samsen879/a303656/pull/117). [Pinned #88 input](https://github.com/Samsen879/a303656/blob/5277b098af15dbef95cf5a90c91a58c418598439/analysis/four_distinct_noncollinear_labels.md)

## Degree-eight reduction

Write \(M=\left(\begin{smallmatrix}A&C\\ C&B\end{smallmatrix}\right)\), \(K=AB-C^2\), and \(D_i=\operatorname{diag}(a_i,b_i)\). By the previous polynomial descent, each \(\det(M-D_i)\) has a polynomial square root \(y_i\). We have
\[
y_i^2=K-b_iA-a_iB+a_ib_i,\qquad
r\cdot(y^2-y(0)^2)=0,\quad r=(705,-571,-189,55).
\]

A rank-two highest coefficient is excluded by the previous common-leading-term argument. For rank one, the first three \(M-D_i\) are strictly positive definite on the real line because each exceeds \(M-D_3\) by a positive diagonal matrix. Their determinant roots have even degree, at most six.

If one root had degree six, all four would have degree six and, after choosing the same leading sign, would share every coefficient above degree two. This follows from
\[
(y_i-y_j)(y_i+y_j)=\det(M-D_i)-\det(M-D_j),
\]
whose right side has degree at most eight. Write \(y_i=f+e_i\), where \(f\) has degree six and zero constant term, and \(\deg e_i\le2\). The cofactor identity gives \(2f(r\cdot e)+r\cdot e^2=\text{constant}\). Since the second term has degree at most four, \(r\cdot e=0\). At zero this contradicts \(r\cdot(\pm1740,\pm1722,\pm1688,\pm1362)\ne0\) for every sign choice. Thus **all four roots have degree at most four**. We can now choose each constant sign independently to be positive.

## Finite obstruction at \(11^3\)

Modulo 11, the cofactor identity on the first three roots is \(y_0^2+y_1^2-2y_2^2=1\). Set
\[
u=y_0+y_1-2y_2,\qquad v=y_0+y_1+2y_2,\qquad w=y_0-y_1.
\]
Then \(uv=2-w^2\), with constants \((u,v,w)(0)=(9,7,7)\). Enumerate \(w\) up to \(t\)-rescaling, enumerate the degree-at-most-four divisors \(u\) with constant 9, and recover \(v\) by division. For each triple, test all fourth roots of degree at most four and constant 9. The pointwise square filter is followed by the full polynomial square test for \(AB-K\).

| Stage | Survivors |
|---|---:|
| Normalized first-three tuples | 1,599 |
| Four-root tuples passing the pointwise mod-11 filter | 5,022 |
| Nonconstant tuples passing the polynomial square test mod 11 | 4 |
| Normalized lifts mod \(11^2\) | 11, from one class |
| Lifts mod \(11^3\) | **0** |

The four mod-11 leading triples \((A_8,B_8,C_8)\) are \((1,4,2)\) twice, \((3,9,7)\), and \((0,2,0)\). Only the last lifts to \(11^2\). An exact positive control at that depth is the following list of coefficients of \(t,t^2,t^3,t^4\) in the four roots:
\[
(21,54,71,3),\quad(20,105,16,65),\quad
(47,88,114,4),\quad(108,117,0,5).
\]
It has no lift to \(11^3\).

**The lift obstruction applies to arbitrary rational coefficients.** Initially normalize the nonconstant root coefficients by weighted \(t\)-rescaling in the extension \(\pi^{12}=11\). Weights \(1,2,3,4\) divide 12, so the reduction is integral and nonconstant with residue field \(\mathbb F_{11}\). Recovery of \(A,B,K\) uses a matrix invertible modulo 11, and integrality of \(C^2=AB-K\) implies integrality of \(C\) by the Gauss valuation. Every nonconstant surviving class has a unit linear coefficient in \(w\). Thus the minimum weighted valuation was attained at weight one, so the initial rescaling is actually a power of **11**. The normalized rational candidate is unramified, and the checks modulo \(11^2,11^3\) apply. A further unit rescaling sets \(w'(0)=1\) exactly.

This closes degree eight within the specified polynomial Gram model. It gives no exclusion for conic covers, other anchors, or arbitrary prescribed integers.

### Executable replay

Python with SymPy for finite-field factorization. The lift checks use integer arithmetic.

```python
from itertools import product
from sympy import Poly, symbols, factor_list

p = 11
a,b = (1,5,25,125),(9,81,1,729)
r,k = (705,-571,-189,55),(1740,1722,1688,1362)
J = ((100,-120,20),(-728,648,80),(-18100,-6480,2020))
M = [(-b[i],-a[i],1) for i in (1,2,3)]

def dot(u,v):
    return sum(x*y for x,y in zip(u,v))

assert [[dot(row,col) for col in zip(*M)] for row in J] == [
    [-22560,0,0],[0,-22560,0],[0,0,-22560]]
assert all(dot(r,v)==0 for v in ((1,)*4,a,b))
assert all(dot(r,[x*s for x,s in zip(k,e)])
           for e in product((-1,1),repeat=4))
assert all(k[i]**2==(450-a[i])*(7578-b[i])-609**2 for i in range(4))

def conv(u,v):
    z = [0]*(len(u)+len(v)-1)
    for i,x in enumerate(u):
        for j,y in enumerate(v):
            z[i+j] += x*y
    return z

def gram(q,m):
    z = pow(-22560,-1,m)
    return [dot(row,q)*z%m for row in J]

def residual(y,m):
    yy = [conv(v,v) for v in y]
    f = [dot(r,col)%m for col in list(zip(*yy))[1:]]
    for i in (1,2,3):
        yy[i][0] -= a[i]*b[i]
    A,B,K = zip(*(gram(col,m) for col in zip(*yy[1:])))
    H = conv(A,B)
    for i,x in enumerate(K):
        H[i] -= x
    C = [609%m]
    assert (H[0]-C[0]**2)%m == 0
    for j in range(1,9):
        s = sum(C[i]*C[j-i] for i in range(1,j))
        C.append((H[j]-s)*pow(1218,-1,m)%m)
    cc = conv(C,C)
    return f+[(H[j]-cc[j])%m for j in range(9,17)],(A[8],B[8],C[8])

X = symbols('X')
def first_three():
    for tail in product(range(p),repeat=4):
        w = (7,)+tail
        j = next((j for j in range(1,5) if w[j]),0)
        if j and w[j] not in ((1,2) if j%2==0 else (1,)):
            continue
        Z = Poly.from_list(w[::-1],X,modulus=p)
        F = Poly(2,X,modulus=p)-Z**2
        _,fs = factor_list(F)
        for es in product(*(range(e+1) for _,e in fs)):
            d = sum(e*f.degree() for e,(f,_) in zip(es,fs))
            if d>4 or F.degree()-d>4:
                continue
            U = Poly(1,X,modulus=p)
            for e,(f,_) in zip(es,fs):
                U *= f**e
            U *= 9*pow(int(U.eval(0))%p,-1,p)
            V = F.exquo(U)
            u = [int(U.nth(i)) for i in range(5)]
            v = [int(V.nth(i)) for i in range(5)]
            yield [[(3*(x+y)+6*z)%p for x,y,z in zip(u,v,w)],
                   [(3*(x+y)-6*z)%p for x,y,z in zip(u,v,w)],
                   [3*(y-x)%p for x,y in zip(u,v)]]

sq = {i*i%p for i in range(p)}
T = [[pow(t,j,p) for j in range(5)] for t in range(1,p)]
four = [(9,)+c for c in product(range(p),repeat=4)]
mask = [{s:0 for s in sq} for _ in T]
for j,f in enumerate(four):
    for row,t in zip(mask,T):
        row[dot(t,f)**2%p] |= 1<<j

found,counts = [],[0,0]
for y in first_three():
    counts[0] += 1
    live = (1<<len(four))-1
    for row,t in zip(mask,T):
        keep = 0
        for s in sq:
            A,B,K = gram([dot(t,y[1])**2-a[1]*b[1],
                          dot(t,y[2])**2-a[2]*b[2],s-a[3]*b[3]],p)
            if (A*B-K)%p in sq:
                keep |= row[s]
        live &= keep
        if not live:
            break
    while live:
        z = live & -live
        live -= z
        yy = y+[four[z.bit_length()-1]]
        counts[1] += 1
        if not any(residual(yy,p)[0]):
            found.append(yy)

assert counts == [1599,5022] and len(found)==5
zero = next(y for y in found if not any(x for v in y for x in v[1:]))
assert [v[0] for v in zero] == [d%p for d in k]
found.remove(zero)
assert all((y[0][1]-y[1][1])%p==1 for y in found)

def lifts(y,q):
    m = q*p
    f,_ = residual(y,m)
    assert all(v%q==0 for v in f)
    ij = list(product(range(4),range(1,5)))
    cols = []
    for i,j in ij:
        z = [v[:] for v in y]
        z[i][j] += q
        g,_ = residual(z,m)
        assert all((a-b)%q==0 for a,b in zip(g,f))
        cols.append([((a-b)//q)%p for a,b in zip(g,f)]
                    +[int((i,j)==(0,1))-int((i,j)==(1,1))])
    E = [list(row)+[rhs%p]
         for row,rhs in zip(zip(*cols),[-v//q for v in f]+[0])]
    piv = []
    for j in range(16):
        i = len(piv)
        h = next((h for h in range(i,len(E)) if E[h][j]%p),None)
        if h is None:
            continue
        E[h],E[i] = E[i],E[h]
        E[i] = [v*pow(E[i][j]%p,-1,p)%p for v in E[i]]
        for h in range(len(E)):
            if h != i:
                E[h] = [(v-E[h][j]*w)%p for v,w in zip(E[h],E[i])]
        piv.append(j)
    if any(row[-1] for row in E[len(piv):]):
        return []
    free = [j for j in range(16) if j not in piv]
    out = []
    for t in product(range(p),repeat=len(free)):
        x = [0]*16
        for j,v in zip(free,t):
            x[j] = v
        for i,j in enumerate(piv):
            x[j] = (E[i][-1]-sum(E[i][h]*x[h] for h in free))%p
        z = [v[:] for v in y]
        for (i,j),v in zip(ij,x):
            z[i][j] += q*v
        assert (z[0][1]-z[1][1])%m == 1 and not any(residual(z,m)[0])
        out.append(z)
    return out

profile = []
for yy in found:
    y = [[d,*row[1:]] for d,row in zip(k,yy)]
    q = lifts(y,11)
    profile.append((residual(y,p)[1],len(q)))
    assert not any(lifts(z,121) for z in q)
assert sorted(profile) == [
    ((0,2,0),11),((1,4,2),0),((1,4,2),0),((3,9,7),0)]
print("PASS",counts,sorted(profile))
control=[[d,*u] for d,u in zip(k,((21,54,71,3),(20,105,16,65),(47,88,114,4),(108,117,0,5)))]; assert residual(control,121)[0]==[0]*16 and not lifts(control,121)
```
