# Close-gap collision bound in the fixed Gaussian critical band

Take genuine labels \(A=9^r,B=25^s\) with \(n^{1/32}\le A\le B\le n^{1/16}\); write \(D=A+2B\), \(S=n-3A-5B>0\), and \(k=\lfloor\log_2S\rfloor\). This note concerns the band \(64k^2q\le S\le64k(k+1)q\) in the Gaussian seed language, with odd numerical norm \(q\) and \(2qS=(D-q)^2+4w^2\), \(w\ge0\). It is a distinct, wider critical band than [the density-zero logarithmic band](https://github.com/Samsen879/a303656/commit/39c8ba81abc7b518070aa6d42687c9533bd970fb). The small-gap count is independently checked below. The full second moment is not bounded here.

For the real quadratic step, both real embeddings of the algebraic integer are polynomially bounded because all coordinates are. As their product is a nonzero integer, both are also bounded away from zero by a reciprocal polynomial. The ideal choices are at most the divisor count of the absolute norm, and generators of any one principal ideal in that height box differ by only \(O(\log X)\) units, uniformly. This supplies the subpower bound without any uniform class-number estimate.

### Close-\(q\) second moment

Let \(X=2^K\), and count unordered pairs of distinct certificates at the same \(n\in[X,2X)\) with \(|q'-q|\le U\), where \(U\ge1\). Each certificate is counted once as a triple \((r,s,q)\). The nonnegative \(w\) is determined by that triple.

For every \(\epsilon>0\), the count is
\[
\ll_\epsilon X^\epsilon
     \left(U^2+\frac{X^{1/16}U}{K^2}\right).
\tag{1}
\]
For pairs at the **same** label, the second term can be dropped. In particular, \(U=X^{49/100}\) gives a power saving over \(X\).

Here is where the critical band enters. Put \(L=2A+3B\), so \(S+D=n-L\), and write
\[
h=q'-q>0,\qquad j=w'-w,\qquad E=L'-L,\qquad F=D'^2-D^2.
\]
The band gives \(q=n(1+O(1/K))/(64K^2)\) and \(w=n(1+O(1/K))/(8\sqrt2 K)\), even when the two values of \(k\) straddle a power of two. Subtracting the certificates then puts \(j\) in the strip
\[
j=2\sqrt2 K h-\frac{\sqrt2 E}{32K}
  +O\!\left(h+\frac{X^{1/16}}{K^2}\right).
\tag{2}
\]
For a fixed label, the error is \(O(h)\). The width in (2) uses the relative \(O(1/K)\) thickness of the band. Using only \(q\asymp X/K^2\) would leave a width of order \(Kh\).

For fixed labels and \(h,j\), eliminate \(n\) from the two certificates. With \(C=h^2+2hE+4j^2\) and \(Y=2hw-2jq\), the exact equation is
\[
Y^2=Cq^2+h(C+F)q-h^2D^2.
\tag{3}
\]
In a genuine collision \(C>0\). Indeed, \(C\le0\) implies \(E<0\). On the allowed labels \(D\) and \(L\) are strictly ordered the same way: a change in \(B\) is by a factor of at least 25, and at fixed \(B\) both increase with \(A\). Thus \(F<0\), and the right side of (3) would be negative.

Completing the square in (3) gives a norm equation with nonzero right side:
\[
\bigl(2Cq+h(C+F)\bigr)^2-C(2Y)^2
=h^2\bigl((C+F)^2+4CD^2\bigr).
\]
For square \(C\), factor the left side. Otherwise pass to the real quadratic field of the squarefree part of \(C\). The number of ideals of the indicated norm is at most the divisor count of that norm. Within each principal ideal the solutions differ by units. All coordinates and the norm are polynomially bounded in \(X\), and a real quadratic unit of absolute value greater than one is at least the golden ratio. Hence there are \(X^{o(1)}\) solutions per fixed pair of labels and \(h,j\), uniformly. Each solution determines \(n\). Summing the strip widths in (2) over \(h\le U\) proves (1), including the polylogarithmic number of label pairs.

### No cross-label collision with equal \(q\)

If \(h=0\) at distinct labels, subtraction gives \(8jw+4j^2=-2qE-F\). The case \(j=0\) is impossible because \(E,F\) are nonzero with the same sign. Otherwise \(q\mid 4w^2+D^2\) implies
\[
q\mid (F+4j^2)^2+16D^2j^2 .
\tag{4}
\]
The integer on the right is positive and too small. In detail, set \(T=n^{1/16}\) and \(K_n=\lfloor\log_2 n\rfloor\). Every legal target has \(n\ge25^{16}\), and the band gives \(q\ge n/[128K_n(K_n+1)]>313T^4\). Also \(D,D'\le3T\), \(|E|\le5T\), \(|F|\le9T^2\), and \(w+w'\ge\sqrt{qn/2}\). The difference equation thus gives \(|j|<T\), bounding the right side of (4) by \(313T^4\). This exclusion holds throughout the legal range.

### Genuine close pairs and exact controls

There are infinitely many within-label collisions with \(q'-q\asymp\sqrt n/\log n\). Take \(r=s\), \(k=100r\), \(m=\lfloor\sqrt{32}\,k\rfloor+2\), and \(M=1+4m^2\). For odd \(c\), set
\[
\alpha=c^2-2D-4,\qquad N=(M\alpha+4mc+1)/2,\qquad b=2m\alpha+c .
\]
The Gaussian integers \(N\pm2i\) and \(N-\alpha+ib\) have norms \(S=N^2+4\) and \(R=S+2D\), respectively. Each half squared distance gives an odd numerical norm \(q\). Half the absolute determinant gives its \(w\). Their numerical gap is \(4b\).

Choose \(c\) with \(Mc^2/2\) between \(1.1\cdot2^{k/2}\) and \(1.25\cdot2^{k/2}\). For all sufficiently large \(r\), this gives the required ordinary height, the actual \(k=\lfloor\log_2 S\rfloor\), and \(S/q=M/2+o(1)\) for both certificates, strictly inside the critical band. Thus the band does not force a pointwise gap of order \(\sqrt n\).

The replay below verifies a native within-label pair at \(n=1267798385586337782800993357740\) with gap \(7943313125220<n^{49/100}\). It also checks a different native target where the same numerical \(q\) meets both labels’ height and band tests, but the second label fails exact squarehood.

```python
from math import isqrt

def row(n, r, s, q):
    A, B = 9**r, 25**s
    D, S = A+2*B, n-3*A-5*B
    k = S.bit_length()-1
    assert n <= A**32 and A <= B and B**16 <= n
    assert S > 0 and q > 0 and q % 2
    assert 64*k*k*q <= S <= 64*k*(k+1)*q
    z, rem = divmod(2*q*S-(D-q)**2, 4)
    assert rem == 0 and z >= 0
    return z

def within(r, c=None):
    k = 100*r
    m = isqrt(32*k*k)+2
    M = 1+4*m*m
    A, B = 9**r, 25**r
    D = A+2*B
    if c is None:
        c = isqrt((5*(1<<(k//2-1)))//M)
        c += (c+1)%2
    alpha = c*c-2*D-4
    N = (M*alpha+4*m*c+1)//2
    a, b = N-alpha, 2*m*alpha+c
    S = N*N+4
    assert S.bit_length()-1 == k and a*a+b*b == S+2*D
    n = S+3*A+5*B
    qs = []
    for y in (2,-2):
        f, j = N-a, y-b
        assert f%2 and j%2 and (N*b-y*a)%2==0
        q = ((f+j)//2)**2 + ((f-j)//2)**2
        w = abs(N*b-y*a)//2
        assert row(n,r,r,q) == w*w
        qs.append(q)
    assert qs[1]-qs[0] == 4*b > 0
    return n, 4*b

n, h = within(1,41847)
assert (n,h) == (1267798385586337782800993357740,7943313125220)
assert h**100 < n**49
for r in (1,2,3,5,10,20):
    within(r)

# The same q passes the real band at both labels, then fails squarehood.
k = 240
A, B = 9**3, 25**3
D = A+2*B
m = isqrt(32*k*k)+2
z = isqrt((1<<(k+1))//(4*m*m+1))
z += z%2+2
q = D*D+z*z
w = z//2+m*q
S, rem = divmod((D-q)**2+4*w*w,2*q)
assert rem==0 and S.bit_length()-1==k
n = S+3*A+5*B
assert row(n,3,3,q)==w*w
bad = row(n,4,3,q)
assert isqrt(bad)**2!=bad
```

The critical band still allows gaps of order \(X/K^3\), far beyond the power-saving range of (1). The larger-gap contribution is the remaining second-moment problem. These results give no positive-density conclusion.
