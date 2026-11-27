# Directional gcd recovery and singleton limit

**Two directional gcds recover the full primitive norm \(4625\) at the pinned target \(n=5277\). At that same target, even the full pairwise gcd menu misses the prime norm \(5273\).** The distinction is whether each prime appears at another numerical offset. A large divisor can be reconstructed from several probes even when the whole divisor occurs at only one cell. [Verified directional energy baseline](https://github.com/Samsen879/a303656/commit/899394a45387a98e261b4f40926cfb1146a7ca16)

### Inverting the directions

Write \(F_i=3^{c_i}+5^{d_i}\) and \(R_i=n-F_i\), using distinct numerical offsets. At a chosen starting cell \(i\), a probe at \(j\) returns
\[
\gcd(R_i,F_j-F_i)=\gcd(R_i,R_j).
\]
The lcm of these outputs is the exact divisor recovered by the anchored menu: its valuation at \(p\) is
\[
\min\!\left(v_p(R_i),\ \max_{j\ne i}v_p(R_j)\right).
\]
After saturation by \(\gcd(R_i,C_i^{\operatorname{bitlength}(R_i)})\), where \(C_i\) is that lcm, it contains the full powers of precisely the primes shared with a probe. If the retained factors have roots of \(-1\), this gives a primitive Gaussian norm divisor. This is a useful selection rule when different probes expose different split factors.

The determinant inversion has exactly the same information away from singular primes. For remainders \(r,s\) at the endpoints of a forward direction, put \(X=3^u,\ Y=5^v\) and \(H=\gcd(s-Yr,Xr-s)\). Then
\[
\gcd(H,r)=\gcd(r,s),\qquad
\gcd(r,s)\mid H\mid |X-Y|\gcd(r,s).
\]
The first identity follows by reducing the two entries modulo \(r\). The second follows by taking linear combinations that give \((X-Y)r\) and \((X-Y)s\). Thus any extra prime in the determinant output comes from the singular factor \(X-Y\) and needs a remainder check.

### Exact controls

At \(5277\), anchor at \((3,4)\). Probes \((3,3)\) and \((2,3)\) give gcds \(125\) and \(37\), respectively. Their lcm is the entire remainder \(4625=64^2+23^2\), with coprime coordinates.

At \((1,0)\) the remainder is \(5273=28^2+67^2\), a split prime. The full \(n/4\) box has offset span \(1352\), so this prime cannot be shared by distinct offsets. At \(5349\), the same box has zero hits modulo \(5273\), versus one at \(5277\). Every pair gcd has the same trivial \(5273\)-part in both cases. Even every nonzero signed direction in the box is nonsingular modulo \(5273\), so the determinant menu misses it too.

```python
from itertools import combinations, product
from math import gcd, isqrt, lcm

def F(c,d):
    return 3**c+5**d

n = 5277
R = n-F(3,4)
G = [gcd(R,F(3,4)-F(*z)) for z in ((3,3),(2,3))]
assert G == [125,37] and lcm(*G)==R==64**2+23**2
assert gcd(64,23)==1

p = 5273
assert p%4==1 and all(p%j for j in range(2,isqrt(p)+1))
assert n-F(1,0)==p==28**2+67**2 and gcd(28,67)==1
box = list(product(range(7),range(5)))
offsets = {F(c,d) for c,d in box}
assert max(offsets)-min(offsets)==1352
for N,count in ((5277,1),(5349,0)):
    assert 4*3**6<=N<4*3**7 and 4*5**4<=N<4*5**5
    assert sum((N-F(c,d))%p==0 for c,d in box)==count
    assert all(gcd(N-a,N-b)%p for a,b in combinations(offsets,2))
assert all(pow(3,u,p)!=pow(5,v,p) for u,v in
           product(range(-6,7),range(-4,5)) if (u,v)!=(0,0))

# A singular determinant can introduce a split prime with zero true hits.
N = 8177**6
A,B,X,Y = 3,25,3**2,5**10
r,s = N-A-B,N-A*X-B*Y
H = gcd(s-Y*r,X*r-s)
assert 4*max(A*X,B*Y)<N
assert H==1224 and H%17==0 and r%17 and s%17
assert gcd(H,r)==gcd(r,s)==9
print("Two-gcd norm recovery, singleton blind spot, and singular false seed")
```

The inversion is useful for repeated **prime support**, even with a unique hit for the combined modulus. Recovering an isolated prime requires information from an individual remainder beyond the pairwise directions.

The displayed valuation identity follows from the prime valuations of gcd and lcm. In the ascending directions considered here, (X\ne Y) for a nonzero direction by unique prime factorization. For the primitive-norm assertion, the root condition is a root of −1 modulo the **full retained prime power**, including at 2: an even primitive norm has valuation exactly one at 2. This note gives no pointwise coverage theorem.
