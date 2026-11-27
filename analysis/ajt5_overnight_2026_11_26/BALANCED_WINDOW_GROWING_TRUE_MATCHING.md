# Positive-density true matchings in each balanced ordinary window

A positive proportion of the targets in every sufficiently large balanced ordinary window have \(\gg b\) genuine representations with **pairwise distinct \(3\)-exponents and pairwise distinct \(5\)-exponents**. The proof counts actual integer square pairs. The divisors of the actual label differences control how much those counts can overlap. [Verified starting point](https://github.com/Samsen879/a303656/commit/2c2da24ad99ddf3e7e3cc51c5c489020cdd7e794)

### The positive-density statement

Write \(A=3^a,\ B=5^b\), with the baseline exponent classes and \(39/40<B/A<122/125\). Put
\[
S_0=A+25B,\quad P=A+125B,\quad S_3=729A+B,\quad U=729A+625B.
\]
Use the ordinary target window \(I=(2S_3-P,U]\), of length \(748B-728A\asymp B\). Restrict targets by \(n\equiv S_0\pmod{625}\) and \(n-S_0\equiv1\pmod4\). Sample the labels \(S_{x,y}=3^x+5^y\) on the grid
\[
a/5\le x\le a/3,\quad x\equiv a-400\pmod{500},
\qquad
b/5\le y\le b/3,\quad y\equiv0\pmod2.
\]
Both axes have \(\asymp b\) entries. The labels are distinct as integers. A collision with both axes different would equate a \(3\)-power difference of \(5\)-adic depth at most \(1+\log_5 a\) with a \(5\)-power difference of depth at least \(b/5\).

Every quotient \(Q_{x,y}=(n-S_{x,y})/125\) is a positive integer of size \(\asymp B\). LTE gives exact \(5\)-adic depth three in the original remainder. The quotients all have the same residue modulo \(20\), which is \(1\bmod4\) and is representable by two squares modulo \(5\).

### Why the actual offsets give enough true norms

Let \(r_2(u)\) count ordered signed integer square pairs of norm \(u\). The elementary correlation bound, for positive arguments \(u,u+h\ll X\), is
\[
\sum_u r_2(u)r_2(u+h)\ll
\begin{cases}
X\sigma_{-1}(|h|),&h\ne0,\\
X\log X,&h=0.
\end{cases}
\]
Indeed, the difference vector between the two square pairs has gcd \(g\mid h\). After dividing by \(g\), a primitive difference vector of sup norm \(k\) puts the second pair on a line with \(O(1+\sqrt X/k)\) lattice points in the box. There are \(O(k)\) such vectors and \(k\ll\sqrt X/g\). Summing gives \(O(X/g)\) for each \(g\). For \(h=0\), sum over all \(g\ll\sqrt X\) and add the coincident pairs.

For the grid, the average off-diagonal \(\sigma_{-1}(|S-S'|/125)\) is bounded. Expand the upper bound \(\prod_{p\mid S-S'}(1-1/p)^{-1}\) over squarefree divisors \(d\), absorbing the factor at \(5\). With the other three exponents fixed, \(d\mid S-S'\) allows at most one class of the varying \(5\)-exponent index modulo \(\operatorname{ord}_d(25)\). For \(N_y\) entries on that axis, the resulting bound is
\[
\ll \sum_{\substack{d\ {\rm squarefree}\\(d,5)=1}}
       \frac1{\varphi(d)\operatorname{ord}_d(25)}
   +\frac{\log B}{N_y}=O(1).
\]
Here \(\sum_{d\le z}1/\varphi(d)\ll\log z\) follows by expanding \(d/\varphi(d)\) over squarefree divisors. For the order sum, primes in terms of order at most \(T\) divide \(\prod_{j\le T}(25^j-1)\). Their Euler product is (O(\log(2T))): for small factors at most the logarithm of this integer product use Mertens' product bound; the sum of the reciprocals of the remaining prime factors is bounded by the logarithm of the integer product divided by the splitting point and its logarithm. Summing in dyadic order ranges proves convergence. The same argument works with base \(3^{500}\) when the \(3\)-axis varies.

Let \(W(n)=\sum_{x,y}r_2(Q_{x,y})\). Each label contributes \(\gg B\) to the first moment over the target class, by counting lattice points in one compatible coordinate class modulo \(20\) in an annulus of area \(\asymp B\). The correlation bounds give \(\sum_n W(n)^2\ll B N_x^2N_y^2\). They also give
\[
\sum_n\sum_x W_x(n)^2\ll B N_x N_y^2,\qquad
\sum_n\sum_y W_y(n)^2\ll B N_y N_x^2,
\]
where \(W_x,W_y\) are the row and column weights.

For each target, draw an edge for every label with \(r_2(Q_{x,y})>0\). The endpoints of a maximal matching cover every edge. If its size is below \(\epsilon b\), Cauchy–Schwarz on the covering rows and columns, using the last two bounds, gives total weight \(O(\sqrt\epsilon\,B N_xN_y)\) over those targets. Choose \(\epsilon\) small. The remaining targets retain a positive fraction of the first moment, and the second moment then gives \(\gg B\) such targets. Their matchings supply the claimed pairwise distinct exponents at each individual \(n\).

For ordinary height, orient a quotient witness as \(h\ge k\ge0\) and multiply \(h-ik\) by \(5(2+i)\). Its first coordinate squared is at least \(4(n-S_{x,y})/5\), so the height key lies in \((S_3,U]\). Thus the density is for genuine ordinary witnesses. It is measured over the target window, with membership of a prescribed target left to an actual witness check.

### Short exact replay

This constructs one target in the stated class and checks two matched labels at that same integer. The density result comes from the proof above.

```python
from math import isqrt

a, b, c = 574422, 392104, 125
A, B = 3**a, 5**b
assert 39*A < 40*B and 125*B < 122*A
S0, P, S3, U = A+25*B, A+125*B, 729*A+B, 729*A+625*B
lo = 2*S3-P

x = a//4 - (a//4-a+400)%500
y = 2*(b//8)
labels = [(x, y), (x+500, y+2)]
assert all(5*i >= a >= 3*i and 5*j >= b >= 3*j for i,j in labels)
S, T = [3**i+5**j for i,j in labels]
assert (T-S) % (20*c) == 0
d = (T-S)//(4*c)
base = S+c*(d+1)**2
w = 10*(isqrt((lo-base)//c)//10+1)
n = base+c*w*w
assert lo < n <= U and (n-S0)%625 == 0 and (n-S0)%4 == 1

for label, z in ((S,d+1), (T,d-1)):
    h,k = sorted((w,abs(z)), reverse=True)
    p,q = 5*(2*h+k), 5*(h-2*k)
    assert n-label == p*p+q*q
    assert (n-label)%125 == 0 and (n-label)%625 != 0
    assert S3 < label+p*p <= n

print(n.bit_length(), labels)
# 910448 [(143522, 98026), (144022, 98028)]
```

For the order series, one may directly bound the product of reciprocal Euler factors for prime divisors of \(\prod_{j\le T}(b_0^j-1)\) by \(O_{b_0}(\log(2T))\). Its logarithmic size is \(O_{b_0}(T^2)\); split prime divisors at that logarithmic size and apply Mertens to the smaller ones, while the larger reciprocal sum is \(O(1)\). This supplies the requisite summable dyadic order tail for both strides. When the 3-axis varies, the single prime 3 is absorbed into a constant. These matched labels share the exact 5-part 125 of their remainders. The theorem does not certify a prescribed target merely for being in the window.

```javascript

const mod=(x,m)=>(x%m+m)%m;
function pw(x,n,m){let r=1n;x=mod(x,m);for(;n;n>>=1n,x=x*x%m)if(n&1n)r=r*x%m;return r;}
function iv(a,m){let b=m,x=1n,y=0n;a=mod(a,m);
  while(b){const q=a/b;[a,b]=[b,a-q*b];[x,y]=[y,x-q*y];}
  if(a!==1n)throw Error("inverse");return mod(x,m);}
const check=(x)=>{if(!x)throw Error("assert");};
const isPrime=(p)=>{for(let i=2n;i*i<=p;++i)if(p%i===0n)return false;return p>1n;};
function crt(rows){let x=0n,M=1n;for(const [m,v] of rows){x+=M*mod((v-x)*iv(M,m),m);M*=m;}return [x,M];}

function root(n){if(n<0n)throw Error("negative");if(n<2n)return n;
let a=1n<<BigInt(Math.ceil(n.toString(2).length/2));
while(true){let b=(a+n/a)/2n;if(b>=a)return a;a=b;}}

const a=574422n,b=392104n,c=125n;
const A=3n**a,B=5n**b;
check(39n*A<40n*B&&125n*B<122n*A);
const S0=A+25n*B,P=A+125n*B,S3=729n*A+B,U=729n*A+625n*B,lo=2n*S3-P;
const x=a/4n-mod(a/4n-a+400n,500n),y=2n*(b/8n);
const labs=[[x,y],[x+500n,y+2n]];
check(labs.every(([i,j])=>5n*i>=a&&a>=3n*i&&5n*j>=b&&b>=3n*j));
const [S,T]=labs.map(([i,j])=>3n**i+5n**j);
check((T-S)%(20n*c)===0n);
const d=(T-S)/(4n*c),base=S+c*(d+1n)**2n,w=10n*(root((lo-base)/c)/10n+1n);
const n=base+c*w*w;
check(lo<n&&n<=U&&(n-S0)%625n===0n&&(n-S0)%4n===1n);
for(const [label,Z] of [[S,d+1n],[T,d-1n]]){
 const z=Z<0n?-Z:Z,[h,k]=w>=z?[w,z]:[z,w];
 const p=5n*(2n*h+k),q=5n*(h-2n*k);
 check(n-label===p*p+q*q&&(n-label)%125n===0n&&(n-label)%625n!==0n);
 check(S3<label+p*p&&label+p*p<=n);
}
text(n.toString(2).length);
```
