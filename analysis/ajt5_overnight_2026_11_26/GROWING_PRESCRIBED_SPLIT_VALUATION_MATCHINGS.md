# Ordinary matchings with growing prescribed split-prime valuations

**The positive-density matching survives prescribed split-prime valuations, even when those valuations grow.** Fix a finite set \(\mathcal P\) of primes \(1\bmod4\) other than \(5\), and put \(c=5^j\), \(E=\prod_{p\in\mathcal P}p^{e_p}\), and \(C=cE\), with \(j\ge1\). If \(cE^2=o(b)\), a positive proportion of a compatible target class in each balanced ordinary window have
\[
\gg_{\mathcal P}\frac{b}{cE^2}
\]
true ordinary witnesses with pairwise distinct \(3\)-exponents and pairwise distinct \(5\)-exponents. Every matched remainder has exactly the prescribed valuations at \(5\) and at the primes in \(\mathcal P\). The density constant is uniform in the growing exponents \(j,e_p\). [Verified matching baseline](https://github.com/Samsen879/a303656/commit/ad89cac980d7aa609299a698e56b77710ae63126)

### Conditioning and ordinary height

Keep \(A=3^a,\ B=5^b\), the balanced strip \(39/40<B/A<122/125\), and the window
\[
I=(2S_3-P,U],\qquad
S_0=A+25B,\quad P=A+125B,\quad S_3=729A+B,\quad U=729A+625B.
\]
Write \(R=\prod_{p\in\mathcal P}p\), \(F=20R\), and take the exponent strides
\[
H=\operatorname{lcm}(4c,\varphi(ER)),\qquad
J=\operatorname{lcm}(2,\varphi(ER)).
\]
Use \(x\in[a/10,a/3]\) in the class \(a-k(4c/5)\bmod H\), where \(3^a k\equiv E\bmod5\) and \(1\le k\le4\). Use \(y\in[b/5,b/3]\) with \(y\equiv0\bmod J\). All labels \(S=3^x+5^y\) agree modulo \(CF\). For one seed label \(S_*\), impose
\[
n\equiv S_*+C\pmod{CF}.
\]
Then every quotient \((n-S)/C\) is \(1\bmod F\), giving the exact prescribed valuations. The choice of \(k\) also retains \(n\equiv S_0\bmod 5^{j+1}\). The grid has \(N_x\asymp_{\mathcal P}b/(cE)\) rows and \(N_y\asymp_{\mathcal P}b/E\) columns. Its labels are distinct by the baseline \(5\)-adic comparison of the two power differences.

For a true quotient witness, first multiply by a Gaussian integer of norm \(C/5\). Orient the resulting coordinates as \(h\ge k'\ge0\), then multiply \(h-ik'\) by \(2+i\). The first coordinate squared is at least \(4(n-S)/5\), so its height key lies in \((S_3,U]\).

### Uniform correlation and matching

Two estimates keep the previous moment argument uniform as the strides grow.

- **Order sums.** For \(g=3\) or \(5\), the sum of \(1/(\varphi(d)\operatorname{ord}_d(g^L))\) over squarefree \(d\) coprime to \(g\) is uniformly bounded when the prime support of \(L\) is fixed. To see this, if \(\operatorname{ord}_d(g^L)\le T\), write each raw prime order \(r=\operatorname{ord}_q(g)\) as \(sv\), where \(s\) uses only that fixed support and \(v\le T\). For \(s\le T^{1/4}\), all such \(q\) divide \(\prod_{r\le T^{5/4}}(g^r-1)\), whose reciprocal Euler product is \(O(\log(2T))\) by the product estimate in the baseline. For larger \(s\), primes of order \(r\) have reciprocal sum \(O(\log(2r)/r)\). They are distinct integers \(1\bmod r\), and only \(O(r)\) can divide \(g^r-1\). Summing over \(s>T^{1/4}\) and \(v\le T\) gives \(O(T^{-1/8}(\log(2T))^2)\), using convergence of \(\sum_s(1+\log s)/\sqrt s\) on the fixed support. Dyadic summation proves the uniform bound.
- **Divisor tails.** For any actual nonzero label difference \(|h|\ll B\), set \(k_b=\lceil\log_2 b\rceil\), \(s=1/k_b\), and \(D=b^{20k_b}\). The squarefree-divisor weight above \(D\) is bounded by
  \[
  D^{-s}\prod_{q\mid h}\left(1+\frac{q^s}{q-1}\right)=O(b^{-4}).
  \]
  For \(q\le b^2\), use \(q^s\le4\) and the harmonic sum. For \(q>b^2\), there are \(O(b)\) prime factors and each contributes \(O(b^{-2})\). Below \(D\), the one-residue-class error in the order count costs only \(O((\log b)^2/N)\) on an axis of length \(N\).

Set \(X=B/C\), \(K=N_xN_y\), and weight each label by its actual integer square-pair count. The annulus count in the coordinate class \((1,0)\bmod F\) gives first moment \(\gg XK\). Using the baseline shifted \(r_2\) bound and the two estimates above, the total second moment is \(O(XK^2)\). Here \(N_y\gg\sqrt b\) and \(K/b\to\infty\). The sums of squared row weights and squared column weights are each \(O(XKb)\), including the diagonal.

For targets with a maximal matching smaller than \(\epsilon K/b\), its covering rows and columns give total weight \(O(\sqrt\epsilon\,XK)\) by Cauchy–Schwarz. Taking \(\epsilon\) small and applying the second moment to the remaining mass gives \(\gg X\) targets with the claimed matching size. This is positive density **relative to the stated target class**. The argument does not settle density conditional on a true \(S_0\) witness.

There is an exact limit if “split part” means the **entire** product of split prime powers. A norm with complete split part \(C\) has quotient \(2^\epsilon u^2\), \(\epsilon\in\{0,1\}\). Across the grid this gives at most \(O(K\sqrt X)=o(X)\) targets with even one such witness. The affirmative result prescribes valuations at selected primes.

### Short exact replay

This uses \(C=5^4\cdot13=8125\) and checks two matched ordinary witnesses at one integer.

```python
from math import isqrt, lcm

a, b, c, E = 574422, 392104, 625, 13
A, B, C, F = 3**a, 5**b, c*E, 260
assert 39*A < 40*B and 125*B < 122*A
S0, P, S3, U = A+25*B, A+125*B, 729*A+B, 729*A+625*B
H, J = lcm(4*c, 39), 52
assert pow(3,H,169) == pow(5,J,169) == 1

k = E*pow(pow(3,a,5),-1,5)%5
l = (a+9)//10
x = l + (a-k*(4*c//5)-l)%H
y = (b//4//J)*J
labels = [(x,y), (x+H,y+J)]
assert all(10*i >= a >= 3*i and 5*z >= b >= 3*z for i,z in labels)
S,T = [3**i+5**z for i,z in labels]
assert (T-S)%(C*F) == 0
d = (T-S)//(4*C)
base = S+C*(d+1)**2
w = 130*(isqrt((2*S3-P-base)//C)//130+1)
n = base+C*w*w
assert 2*S3-P < n <= U and (n-S0)%(5*c) == 0

for label,z in ((S,d+1), (T,d-1)):
    assert (n-label-C)%(C*F) == 0
    # -16+37i has norm C/5.
    h,k = sorted((abs(-16*z-37*w),abs(37*z-16*w)), reverse=True)
    p,q = 2*h+k,h-2*k
    assert n-label == p*p+q*q and S3 < label+p*p <= n

print(n.bit_length(), C, labels)
# 910448 8125 [(85922, 98020), (183422, 98072)]
```

For the 5-adic congruence, \(3^{4c/5}=(1+80)^{5^{j-1}}\equiv1+16c\pmod{5c}\), so \(3^a-3^x\equiv3^a k c\equiv C\pmod{5c}\). The actual quotient step on the restricted target interval is \(F\), which is fixed once \(\mathcal P\) is fixed. The full split part restriction is different: it leaves only a square times a possible single 2, explaining the much smaller population. In particular the theorem does not imply an analogous density when conditioning on the first \(S_0\) remainder already being a norm.

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

function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
const lcm=(a,b)=>a/gcd(a,b)*b;
const a=574422n,b=392104n,c=625n,E=13n,C=c*E,F=260n;
const A=3n**a,B=5n**b;
check(39n*A<40n*B&&125n*B<122n*A);
const S0=A+25n*B,P=A+125n*B,S3=729n*A+B,U=729n*A+625n*B;
const H=lcm(4n*c,39n),J=52n;
check(pw(3n,H,169n)===1n&&pw(5n,J,169n)===1n);
const k=mod(E*iv(pw(3n,a,5n),5n),5n),l=(a+9n)/10n;
const x=l+mod(a-k*(4n*c/5n)-l,H),y=(b/4n/J)*J;
const labels=[[x,y],[x+H,y+J]];
check(labels.every(([i,z])=>10n*i>=a&&a>=3n*i&&5n*z>=b&&b>=3n*z));
const [S,T]=labels.map(([i,z])=>3n**i+5n**z);
check((T-S)%(C*F)===0n);
const d=(T-S)/(4n*C),base=S+C*(d+1n)**2n;
const w=130n*(root((2n*S3-P-base)/C)/130n+1n),n=base+C*w*w;
check(2n*S3-P<n&&n<=U&&(n-S0)%(5n*c)===0n);
for(const [label,z] of [[S,d+1n],[T,d-1n]]){
 check((n-label-C)%(C*F)===0n);
 const w1=-16n*z-37n*w,w2=37n*z-16n*w;
 const abs=z=>z<0n?-z:z;
 const [h,k]=[abs(w1),abs(w2)].sort((u,v)=>u>=v?-1:1);
 const p=2n*h+k,q=h-2n*k;
 check(n-label===p*p+q*q&&S3<label+p*p&&label+p*p<=n);
}
```
