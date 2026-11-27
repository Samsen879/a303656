# Separate wild order-343 axes detect an unsplit native mismatch

Let ζ=ζ₃₄₃ and P(X)=1+X^a−X−X^b. For A=P(ζ), define D(h)=N(P((1+h)ζ)) and T=Tr(ζP′(ζ)/A). [Sen's explicit Hilbert symbol formula, as recorded by Vostokov](https://arxiv.org/pdf/math/0012139), gives the arithmetic-normalized 7-wild log −T log₇(u⁶)/(6·343) for u=3,5. Indeed, use π=ζ−1, the root lift 1+X and the principal unit u⁶; its π-valuation 294 exceeds 98. Dividing by 6 is valid. The minus sign corresponds to the arithmetic convention; on A=ζ its logs (267,50) agree with inverse cyclotomic norm action. The matching global product formula adds this term to the log of the finite-field Euler projection A^((u^294−1)/343).

For both sources D(0)=7N with N a 7-adic unit and D′(0) divisible by 343. Evaluate D(7⁶) modulo 7¹², subtract D(0) modulo 7¹² and divide by 7⁶ to recover D′(0) modulo 7⁶. Then T/49=(D′(0)/343)/N modulo 343. The elementary series log₇(u⁶)/42 modulo 343 gives 127,106. Independently verified exact absolute norms by 27 modular resultants and CRT above 2·4^294, finite differences by the 294-dimensional multiplication determinant modulo 7¹², and both tame field logs directly.

| Source | D′(0) mod 7⁶ | T/49 mod 343 | Tame | Wild | Total |
|---|---:|---:|---:|---:|---:|
| (55,161) | 31213 | 91 | (238,287) | (105,301) | (0,245) |
| (70,180) | 90895 | 265 | (157,201) | (302,36) | (116,237) |

For (55,161), the exact norm, native root, and gcd of ζ⁴⁹−1 with N verify that the root evaluation ideal accounts for the entire non-7 norm and that all its primes have ζ of order 343. Re-running the [frozen three-band enumerator](https://github.com/Samsen879/a303656/commit/26575f9c2ca06e032a2947555db77561d5840438) with requested tags (55,161),(70,180) gives respectively (E=27 mod 49,k=118), and (E=15 mod 49,k=58) or (E=43 mod 49,k=324). If each prime of the unsplit first source passed, its two Euler logs would obey L₅=118L₃ mod 343, and the sum with multiplicities would obey the same identity. It does not: (0,245) violates it, although both logs vanish modulo 49. This guarantees at least one failed prime, without identifying which prime or asserting every prime fails.

At the prime control p=105252402993769124507 of (70,180), elementary Lucas verification uses base 2 and complete factorization of p−1. Actual log pair (50,177) and false lift (E,k)=(239,324) agree after reduction modulo 49 and under the coupled word with coefficients (11,3), giving 52 modulo 343. The first separate log forces E=141, predicting (50,79) with the permitted k. Thus the matched weak tests do not give the stronger primewise condition. This note does not assert new full closure of (70,180).

## Replay (Node.js or modern JS)

~~~javascript
const mod=(a,m)=>(a%m+m)%m;
function inv(a,m){let [x,y,u,v]=[0n,1n,m,mod(a,m)];while(v){let q=u/v;[u,v]=[v,u-q*v];[x,y]=[y,x-q*y]}if(u!==1n)throw Error("inverse");return mod(x,m)}
function pow(a,e,m){let x=1n;for(a=mod(a,m);e;e>>=1n,a=a*a%m)if(e&1n)x=x*a%m;return x}
const assert=x=>{if(!x)throw Error("check failed")};
function norm(a,b,h,m,p){
 let n=294,X=1n+h,cs=[[0,1n],[a,pow(X,BigInt(a),m)],[1,-X],[b,-pow(X,BigInt(b),m)]];
 let A=Array.from({length:n},()=>Array(n).fill(0n));
 for(let c=0;c<n;c++)for(let [j,v] of cs){let i=c+j;if(i<n)A[i][c]=mod(A[i][c]+v,m);else{let r=i%343;if(r<n)A[r][c]=mod(A[r][c]+v,m);else for(let s=r%49;s<n;s+=49)A[s][c]=mod(A[s][c]-v,m)}}
 let det=1n; const vp=x=>{if(!x)return 999;let v=0;while(x%p===0n){v++;x/=p}return v};
 for(let j=0;j<n;j++){
  let bi=j,bj=j,v=vp(A[j][j]);outer:for(let i=j;i<n&&v;i++)for(let k=j;k<n;k++){let w=vp(A[i][k]);if(w<v){v=w;bi=i;bj=k;if(!v)break outer}}
  if(v===999)return 0n;
  if(bi!==j){[A[bi],A[j]]=[A[j],A[bi]];det=-det;}if(bj!==j){for(let i=j;i<n;i++)[A[i][bj],A[i][j]]=[A[i][j],A[i][bj]];det=-det;}
  let pp=p**BigInt(v),u=A[j][j],k=inv(u/pp,m/pp);det=mod(det*u,m);if(!det)return 0n;
  for(let i=j+1;i<n;i++)if(A[i][j]){let t=A[i][j]/pp*k%(m/pp);for(let z=j+1;z<n;z++)if(A[j][z])A[i][z]=mod(A[i][z]-t*A[j][z],m);}
 }
 return det;
}
function logs(a,b,p){
 const n=294,s=49,m=343,z=()=>new Int32Array(n);let f=z(),g=z();f[0]=1;g[0]=g[a]=1;g[1]=g[b]=p-1;
 function mul(a,b){let c=new Int32Array(m);
  for(let i=0;i<n;i++)if(a[i])for(let j=0;j<n;j++)if(b[j])c[i+j<m?i+j:i+j-m]+=a[i]*b[j];
  let u=z();for(let i=0;i<n;i++)u[i]=((c[i]-c[n+i%s])%p+p)%p;return u;
 }
 let k=(BigInt(p)**294n-1n)/343n;
 while(k){if(k&1n)f=mul(f,g);k>>=1n;if(k)g=mul(g,g);}
 for(let i=0;i<m;i++){let ok=true;for(let j=0;j<n;j++){let q=i<n?+(i===j):j%s===i%s?p-1:0;if(q!==f[j]){ok=false;break;}}if(ok)return i;}throw Error("not root")
}
function res(A,B,p){
 const md=x=>(x%p+p)%p;
 const pw=(a,e)=>{let x=1;for(;e;e=Math.floor(e/2),a=md(a*a))if(e%2)x=md(x*a);return x};
 let ans=1;
 while(B.length>1){
  const m=A.length-1,n=B.length-1,k=B[n],iv=pw(k,p-2);
  if(m*n%2)ans=md(-ans);
  let T=A.slice();for(let i=m;i>=n;i--){if(!T[i])continue;const u=md(T[i]*iv);for(let j=0;j<=n;j++)T[i-n+j]=md(T[i-n+j]-u*B[j]);}
  T=T.slice(0,n);while(T.length&&!T.at(-1))T.pop();if(!T.length)return 0;
  ans=md(ans*pw(k,m+1-T.length));[A,B]=[B,T];
 }
 return B.length?md(ans*pw(B[0],A.length-1)):0;
}
const primes=[];
for(let p=10000019;primes.length<27;p+=2){let ok=true;for(let i=3;i*i<=p;i+=2)if(p%i===0){ok=false;break;}if(ok)primes.push(p)}
const P=Array.from({length:295},(_,i)=>Number(i%49===0)), h=7n**6n,M=h*h;
for(const [a,b,N,T0,der0,t3,t5,L3,L5] of [
  [55,161,41972042533351331790887366901335366135158470044034151n,91n,31213n,238,287,0,245],
  [70,180,214728794690927797715992906119172652683368543413295253n,265n,90895n,157,201,116,237]
]){
 let R=0n,S=1n;
 for(const p of primes){const Q=Array(b+1).fill(0),p0=BigInt(p);Q[0]=Q[a]=1;Q[1]=Q[b]=p-1;
   R+=S*mod((BigInt(res(P,Q,p))-R)*inv(S,p0),p0);S*=p0;
 }
 assert(S>2n*4n**294n&&R===7n*N);
 const d=mod(norm(a,b,h,M,7n)-norm(a,b,0n,M,7n),M);
 assert(d%h===0n&&d/h===der0&&der0%343n===0n);
 const T=mod((der0/343n)*inv(N,343n),343n);assert(T===T0);
 for(const [u,l,L] of [[3n,t3,L3],[5n,t5,L5]]){
  const q=(u**6n-1n)/7n, log=mod((q-7n*q*q*inv(2n,343n)+49n*q**3n*inv(3n,343n))*inv(6n,343n),343n);
  assert(logs(a,b,Number(u))===l&&mod(BigInt(l)-T*log,343n)===BigInt(L));
 }
}
function gcd(a,b){while(b)[a,b]=[b,a%b];return a<0n?-a:a}
const N=41972042533351331790887366901335366135158470044034151n,z=30015482896187807087217920276249313249092836022188472n;
assert(pow(z,343n,N)===1n&&gcd(pow(z,49n,N)-1n,N)===1n);
assert(mod(1n+pow(z,55n,N)-z-pow(z,161n,N),N)===0n);
assert((N-1n)/343n%49n===0n&&245n!==mod(118n*0n,343n));
const p=105252402993769124507n,y=35983878305134030475n,s=(p-1n)/343n;
for(const q of [6997,21927848918543])for(let i=2;i*i<=q;i++)assert(q%i!==0);
assert(2n*343n*6997n*21927848918543n===p-1n&&pow(2n,p-1n,p)===1n);
for(const q of [2n,7n,6997n,21927848918543n])assert(gcd(pow(2n,(p-1n)/q,p)-1n,p)===1n);
assert(s%343n===302n&&pow(y,343n,p)===1n&&pow(y,49n,p)!==1n);
assert(pow(3n,s,p)===pow(y,50n,p)&&pow(5n,s,p)===pow(y,177n,p));
assert(mod(239n*s,343n)===148n&&mod(239n*324n*s,343n)===275n);
assert((11*148+3*275)%343===(11*50+3*177)%343&&148%49===50%49&&275%49===177%49);
assert(mod(141n*s,343n)===50n&&mod(141n*324n*s,343n)===79n);
console.log("order-343 derivative, fixed field logs, exact norms and prime control verified");
~~~
