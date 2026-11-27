# Intermediate split-prime marks: conditional lower bound and an unconditional switching gap

For the switched anchor \(u=dp\), I obtained a **conditional signed lower bound of order \(BK/\log B\)** in the intermediate range \(B^{\theta_1}\ll p\ll B^{\theta_2}\), for fixed \(2/3<\theta_1<\theta_2<3/4\). It holds on the 42 blocked phases under the prime-count form of Elliott–Halberstam. Unconditionally, the forward and reverse switches expose a specific distribution gap in this range. The previous top-cutoff transfer remains separate, and the full-grid sign remains open.

### Conditional signed comparison

Use the same ordinary window, \(n=S_0+45u\), and \(k=(S_0-S_i)/45\). Restrict the labels to the 42 phases where \(u+k\) has exact \(7\)-depth one in \(r_-\). Restrict the anchor marks to
\[
u=dp,\qquad B^{1-\theta_2}\le d\le B^{1-\theta_1},
\]
with every prime factor of \(d\) congruent to \(1\bmod4\) and \(p\equiv1\bmod4\) prime. The count in \(r_-\) is zero by the depth-one obstruction.

In \(r_0\), fixing \(d\) gives a reduced progression for \(p\bmod196\) and an interval of length and location \(\asymp X=B/d\). Both \(u\) and \(u+k\) are units at \(7\). The second number is odd and \(1\bmod4\). Sift it at every inert prime through \(z=\sqrt{CB}+1\), with \(C\) a fixed upper bound for \((u+k)/B\). A surviving value has no inert prime factors: size permits at most one above \(z\), and the residue modulo \(4\) requires an even number.

At an inert \(q\nmid7k\), the sieve removes one reduced prime class, with density \(1/(q-1)\). Primes dividing \(k\) would require \(p=q\), which is outside the range \(q\le z<p\). The density has the uniform half-dimensional upper product bound. A prime distribution level \(X^\rho\) with \(\rho\theta_1>1/2\) gives a fixed positive margin in \(\log D/\log z>1\), where the half-dimensional lower sieve is positive. Ordinary prime-count Elliott–Halberstam supplies this level, with slack to include the base modulus 196. The resulting lower bound is \(\gg B/[d(\log B)^{3/2}]\) per label and cofactor. [Half-dimensional sieve and its lower-bound threshold, Theorem 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

The harmonic sum of the eligible \(d\)'s in this exponent band is \(\asymp\sqrt{\log B}\). One way to obtain it is to remove powers of \(2\) and inert squares from Landau’s norm count by Möbius inversion. The split-only count has leading constant \(\frac{\kappa}{2}\prod_{q\equiv3(4)}(1-q^{-2})\) times \(x/\sqrt{\log x}\), and partial summation gives the stated harmonic sum. Also \(p^2\gg B\), so each target–label pair has at most one marked anchor prime in the band. Summation gives the conditional \(\gg BK/\log B\) gap. [Landau norm count, equation (1.1)](https://www.math.purdue.edu/~twooley/publ/2000SUM2S.pdf)

### Where the unconditional switch stops

Take \(d=5^{\lfloor(1-\theta)b\rfloor}\) with \(2/3<\theta<3/4\). On the actual grid,
\[
v_5(k)=v_5((a-x)/4).
\]
Indeed \(v_5(3^{a-x}-1)=1+v_5((a-x)/4)\), while the \(5\)-power difference has depth \(y\gg b\). Hence the common factor \(g=(d,k)\) is \(O(\log B)\). Dividing it out still leaves the partner at size \(B/g\), and the forward Bombieri–Vinogradov level gives
\[
\frac{\log D}{\log\sqrt{B/g}}\le\theta+o(1)<1.
\]

One can sift to \(z=B^\gamma\) with \(1/3<\gamma<\theta/2\) and obtain a positive rough count. Among these survivors, failure of normhood is exactly
\[
(d/g)p+k/g=fq_1q_2,
\]
with distinct inert primes \(q_1,q_2>z\) and \(f\) supported on split primes. Parity gives an even number of inert factors, and \(z^3\gg B/g\) bounds their number by two. Two copies of the same inert prime give a true norm.

In the reverse switch, fixing \(f,q_1\) imposes a reduced residue on \(q_2\) modulo \(d/g\) just to make \(p\) integral. In the balanced sector \(q_1,q_2\asymp\sqrt{B/g}\), the standard reverse Bombieri–Vinogradov level is at most \(B^{1/4}\), whereas \(d/g\gg B^{1-\theta}/\log B\). The integrality modulus alone exceeds that level, before imposing the primality of \(p\). This locates the gap for the two standard switches. Distribution exploiting the special modulus or averaging the coupled primes remains open here. [Buchstab and reverse-switch comparison, Proposition 4.2](https://arxiv.org/html/2501.16723v1)

### Exact real replay

The two targets below share the same label, intermediate split prime \(p\), and class \(r_-\). Both partners are \(1\bmod4\) and clear **every inert prime through \(\sqrt p\)**. One is a genuine norm. The other has exact valuation one at both \(131071\) and \(524287\), above that panel. This is a finite marked-prime control, with \(p>B^{1/40}\) and \(p^2<B\).

```python
from math import gcd, isqrt, prod

p = 14697662461
z = isqrt(p)
s = bytearray([1]) * (z+1)
s[:2] = bytes(2)
for j in range(2,isqrt(z)+1):
    if s[j]:
        s[j*j::j] = bytes((z-j*j)//j+1)
pr = [j for j in range(2,z+1) if s[j]]
Q = (131071,524287)
assert p%4 == 1 and all(p%j for j in pr)
assert all(q>z and q%4==3 and all(q%d for d in pr if d*d<=q) for q in Q)
panel = prod(q for q in pr if q%4==3)

A,B = 3**712,5**486
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
k,rem = divmod(S0-3**160-5**146,45)
assert 39*A<40*B and 125*B<122*A and p**40>B and p*p<B
assert rem==k%8==0
mid = ((lo-S0)//45+(hi-S0)//45)//2
m = (isqrt(mid+k)-isqrt(mid))//2+1
w,e = divmod(k//4,m)
w,e = w+5,e-5*m
x,y = w-m,e-1
u = x*x+y*y
assert u+k == (w+m)**2+(e+1)**2

g,h = 60106,-105285
c,rc = divmod(x*g+y*h,p)
d,rd = divmod(y*g-x*h,p)
assert g*g+h*h==p and rc==rd==0 and u==p*(c*c+d*d)
c += 69972458531454342882396+2*925566176643030306521284
d += 726985966980049183235808
u_bad = p*(c*c+d*d)
for v in (u,u_bad):
    n = S0+45*v
    assert lo<n<=hi and n%49==(pow(3,716,49)+pow(5,488,49)+7)%49
    assert (v+k)%4==1 and gcd(v+k,panel)==1
assert all((u_bad+k)%q**2==q for q in Q)
```

Independent BigInt verified the split-prime anchor, all inert primes below the finite square-root panel on both targets, the same-class true pair, and the two exact late odd valuations. The positive band asymptotic is conditional on prime-count Elliott–Halberstam and restricted to the blocked phases. The Bombieri–Vinogradov comparison describes the standard switches' level gap, not a general impossibility theorem for alternate averaging.
