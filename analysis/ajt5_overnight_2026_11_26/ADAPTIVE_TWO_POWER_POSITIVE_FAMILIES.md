# Target-only recovery for two actual signed-to-positive families

**Two explicit families admit target-only recovery of a true positive representation, one in each odd class modulo \(4\).** In both families the original signed Gaussian norm and real quadratic norm hold exactly. The two recovered exponents vary, and recovering them requires only finding a power of \(5\), taking an integer square root, and testing a power of \(3\).

### Simultaneous signed and positive norms

Take \(U=3^j,\ V=5^k\) with \(j\ge1\) and \(10U\le V\). Use the following parameters. Here \(P,B\) are the signed powers, \(A,V^2\) are the positive-height powers, and \(g,h\) are the positive square coordinates.

| \(n\bmod4\) | \((P,B,A)\) | \((x,y,r,t)\) | \((g,h)\) |
|---|---|---|---|
| \(1\) | \((9U^2,5V^2,3U^2)\) | \((V+2U,V-U,V-4U,V-U)\) | \((V,V-U)\) |
| \(3\) | \((27U^2,125V^2,9U^2)\) | \((V-2U,5V-U,V+7U,3V)\) | \((7V-2U,7V+3U)\) |

Both rows satisfy the polynomial identities
\[
S=x^2+y^2,\qquad 2P-S=r^2-3t^2,\qquad
S+g^2+h^2=B-V^2+P-A.
\]
Consequently the **same target** satisfies
\[
n=B+P-S=A+V^2+g^2+h^2.
\]
Here \(S\equiv1\pmod4\) and \(P-S\equiv1\pmod3\), so the signed data also meet the previously verified parity-switch criterion. In both rows \(B>n\), whereas \(A+V^2<n\) and the positive residual is the actual integer square sum \(g^2+h^2\). [Signed parity-switch criterion](https://github.com/Samsen879/a303656/commit/113a6db2f798576db459b525e1204d5598ee8d19)

### Recovering the exponents from \(n\)

Choose the row using \(n\bmod4\), then take the least \(V=5^k\) for which the row’s \(B\) exceeds \(n\). The bands \(2.8V^2<n<3V^2\) and \(99V^2<n<101V^2\), respectively, ensure this recovers the original \(V\). Completing the square gives
\[
U=
\begin{cases}
\bigl(V-\sqrt{4n-11V^2}\bigr)/4,&n\equiv1\pmod4,\\[2mm]
\bigl(\sqrt{22n-2129V^2}-7V\bigr)/22,&n\equiv3\pmod4.
\end{cases}
\]
Require the root to be integral and \(U=3^j\) with \(j\ge1,\ 10U\le V\). The recovered exponents are \((2j+1,2k)\) or \((2j+2,2k)\). No signed witness is needed as input.

Recovery also proves distinctness. At each \(k\) there are \(k\log5/\log3+O(1)\) choices of \(j\), and the target-height cutoff changes the largest \(k\) by only \(O(1)\). Thus each row gives
\[
\frac{(\log X)^2}{8\log3\,\log5}+O(\log X)
\]
distinct targets up to \(X\).

### Why the signed \(3\)-power moves

There is an exact obstruction to the analogous **integral affine identity in \(V\)** with the old seed \(P=1\) or \(3\), a fixed opposite-parity exponent \(c\), and \(B=5^\ell V^2\). The constant term of the four-square identity would be \(P-3^c\). This is negative except when \(P=3,c=0\). In that case the signed constant norm can be \(0,1,2\), but \(1\) would require the real constant norm to equal \(5\), impossible modulo \(3\). So the signed constant norm is even. The signed leading norm is also even, since an odd Gaussian norm negates to \(3\) or \(7\bmod8\), neither a residue of \(r^2-3t^2\). Hence \(x+y\) is even for every \(V\) in this affine model, and it cannot yield an odd target.

The explicit families instead use moving \(P\). They do not establish an adaptive success rate on the earlier counted \(P=1,3\) population. [Growing prescribed-menu result](https://github.com/Samsen879/a303656/commit/3b0c773d07202e697b9bf52bb9e99643018554c8)

```python
from math import isqrt

# Recover both powers from the targets, then check both signed norms
# and the true positive representation.
for n in (46161, 38752407):
    first = n % 4 == 1
    scale = 5 if first else 125
    V = 1
    while scale*V*V <= n:
        V *= 5
    if first:
        U = (V-isqrt(4*n-11*V*V))//4
        x,y,r,t,g,h = V+2*U,V-U,V-4*U,V-U,V,V-U
        P,A = 9*U*U,3*U*U
    else:
        U = (isqrt(22*n-2129*V*V)-7*V)//22
        x,y,r,t,g,h = V-2*U,5*V-U,V+7*U,3*V,7*V-2*U,7*V+3*U
        P,A = 27*U*U,9*U*U
    assert U in (3,9) and 10*U <= V
    S, B = x*x+y*y, scale*V*V
    assert n == B+P-S < B and (n-B) % 3 != 0
    assert 2*P-S == r*r-3*t*t
    assert n == A+V*V+g*g+h*h and g*g+h*h > 0
```


### Independent BigInt replay

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
for(const P0 of [1,3])for(let j=1n;j<=6n;j++)for(let k=2n;k<=10n;k++){
 const U=3n**j,V=5n**k;if(10n*U>V)continue;
 const first=P0===1,s=first?5n:125n,B=s*V*V;
 const [P,A,x,y,r,t,g,h]=first?[9n*U*U,3n*U*U,V+2n*U,V-U,V-4n*U,V-U,V,V-U]:
 [27n*U*U,9n*U*U,V-2n*U,5n*V-U,V+7n*U,3n*V,7n*V-2n*U,7n*V+3n*U];
 const S=x*x+y*y,n=B+P-S;
 check(S%4n===1n&&mod(P-S,3n)===1n&&n%4n===BigInt(P0));
 check(n<B&&n>A+V*V&&n===A+V*V+g*g+h*h&&2n*P-S===r*r-3n*t*t);
 let vv=1n;while(s*vv*vv<=n)vv*=5n;
 const D=first?4n*n-11n*vv*vv:22n*n-2129n*vv*vv,z=root(D);
 check(vv===V&&z*z===D&&(first?(vv-z)/4n:(z-7n*vv)/22n)===U);
}
const m=new Set();for(let r=0n;r<8n;r++)for(let t=0n;t<8n;t++)m.add(mod(r*r-3n*t*t,8n));
check(!m.has(3n)&&!m.has(7n));
```
