# Reciprocal second remainder in the literal prime loss

This follows [the first quotient–remainder sector](https://github.com/Samsen879/a303656/commit/fd5ac266be08940f93d54d6e2e7791d71fc164c6). The bound is absolute counting within the specified coordinate sector, not digit cancellation, and does not assert that a fully legal finite overlap exists. The size bounds on the pinned bands are as in that setup.

### Second-remainder bound

Keep \(p=\lambda v=49gts-\kappa\) in the original sharp window, with \(g=qrh_0P\). Write
\[
n=\operatorname{nint}(v/\lambda),\qquad d=v-n\lambda,\qquad
\sigma=1-\frac{95699}{384000}-\frac{699}{2000}
      =\frac{154093}{384000}.
\]
On the **complement** of the previous cutoff \(n(1+|d|)\le B^{\sigma-\epsilon}\), define
\[
a_2=\left\lfloor\frac{\lambda}{|d|}\right\rfloor,\qquad
e_2=\lambda-a_2|d|,\qquad \delta=\operatorname{sgn}(d).
\]
For \(0<\epsilon\le1/100\), the matched-digit sum on the new sector
\[
a_2 n(1+e_2)\le B^{\sigma-\epsilon}
\tag{1}
\]
is \(O(B^{1-\epsilon}(\log B)^2)\). This holds separately for either literal marked loss and for the genuine semiprime overlap. It is below the secondary scale when the row harmonic factor is at least inverse-polylogarithmic.

An explicit sector that needs no adaptive cutoff is
\[
|d|\ge B^{9/20},\qquad e_2\le B^{1/3}.
\]
Its bound is \(O(B^{1-29609/4992000})\). It lies wholly beyond the old cutoff since \(9/20>\sigma\). For example, \(a_2=2\) places this sector near \(|d|=\lambda/2\). The first remainder can be of the same order as \(\lambda\).

**Proof.** The exact equation becomes
\[
a_2p=(a_2n+\delta)\lambda^2-\delta e_2\lambda.
\]
Thus for fixed \(g,t,n,a_2,e_2,\delta\), a legal anchor must solve
\[
(a_2n+\delta)\lambda^2-\delta e_2\lambda+a_2\kappa\equiv0\pmod{Pt}.
\tag{2}
\]
As before \(n\ll B^\theta\) with \(\theta=5/416\). Outside the old cutoff, \(|d|\gg B^{\sigma-\epsilon-\theta}\), so
\[
a_2n\ll B^{1/2-\sigma+\epsilon+2\theta}.
\]
The exponent is less than \(0.133\). The positive leading coefficient in (2) is therefore smaller than both primes \(P,t\). There are at most four CRT roots modulo \(Pt\), and \(\lambda\le2\sqrt B<Pt\) gives at most one representative per root. Once \(\lambda\) is known, recover \(d=\delta(\lambda-e_2)/a_2\), \(v=n\lambda+d\), and \(s=(\lambda v+\kappa)/(49gt)\). The full window, lift, divisibility, and prime tests are checked on these reconstructed integers. Each marked semiprime allows at most two choices of designated factor.

The number of \((a_2,n,e_2)\) in (1) is \(O(B^{\sigma-\epsilon}(\log B)^2)\) by summing \(B^{\sigma-\epsilon}/(a_2n)\). Multiplying by the row and \(t\) counts proves the bound. For the explicit sector, use \(a_2\le2B^{1/20}\), so the parameter cost instead has exponent \(5/416+1/20+1/3\).

On that explicit sector, (2) has **at most two** admissible roots. Two reflected roots would require \(Pt\) to divide
\[
(a_2n+\delta)(\lambda_1+\lambda_2)-\delta e_2.
\]
This integer is positive and \(O(B^{1/2+1/20+5/416})<Pt\). The same argument excludes a fixed point of the reflection in the legal band. Thus the reciprocal step reduces the signed problem on a new sector by counting actual incidences, but the reflection does not furnish a digit pairing. The region with both adaptive remainders large remains open.

## Exact arithmetic negative control

The pinned integers in the replay below exclude all 262,144 odd anchors in the specified interval by a sharp-window congruence alone, before requiring any prime test. There are 174,074 invertible cells and zero hits; the noninvertible cells are impossible since the shift is coprime to the coefficient. This makes no claim about other rows or the rest of the band.

```python
from math import gcd

A, B = 3**712, 5**486
S0, S = A+25*B, 3**80+5**122
k, rem = divmod(S0-S,45)
lo = (1457*A-123*B-S0)//45+1
hi = (729*A+625*B-S0)//45
assert rem==0 and 39*A<40*B and 125*B<122*A
assert S%49==(pow(3,716,49)+pow(5,488,49)+7)%49==27

g0 = 59*67*25
W = 514*((1<<127)-1)
t = W*((1<<394)//W+114)+1
R, J = (1<<157)+(307<<90)+1, 1<<89
M = 2*J*R
z = 1+J + 2*J*((((k+1)*pow(49*g0*t,-1,R)-(1+J))
                 * pow(2*J,-1,R)) % R)
P = (1<<259)+(z-(1<<259))%M+52*M
g = g0*P
assert gcd(g*t,k)==1 and t%4==3 and P%4==1
assert B<59**375<B**2<67**375<B**3 and 25**1024<=B**5
assert B**87<t**250 and t**2000<=B**699
assert B**57<P**250 and P**1000<=B**231

D = 49*g*t
slo, shi = (lo+k+D-1)//D, (hi+k)//D
start = (1<<559)+1
stop = start+(1<<19)
assert B**411<start**832 and stop*stop<=4*B
assert 0<slo<=shi<start and max(t,P,67)<start and gcd(D,k)==1
tested = unit = hits = 0
for l in range(start,stop,2):
    tested += 1
    if gcd(D,l)==1:
        unit += 1
        hits += (slo<=k*pow(D,-1,l)%l<=shi)
assert (tested,unit,hits)==(262144,174074,0)
```
