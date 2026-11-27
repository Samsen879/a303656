# Genuine Pell activation and a bounded-overlap mass obstruction

At \(K=10936\) along [the actual Pell orbit](JOINT_LABEL_PELL_ORBIT.md), \(R_n=5p_n^2+K=X_n^2+12\) and \(R_0=12794941\) is prime, 1 modulo 4. We give an exact activation condition, two genuine positive examples, and an unconditional constraint on any selection of such primes with bounded period overlap. No positive-density assertion for the activation condition is used or claimed.

## An algebraic activation condition at one residue place

Let \(\alpha=3577+1599\sqrt5\), \(\phi=(1+\sqrt5)/2\), so \(G=(9+4\sqrt5)^{387860}=\phi^{6\cdot387860}\). In the field \(E=\mathbb Q(\sqrt5,\sqrt{-3},\sqrt{-2734})\), put \(\beta=(2\sqrt{-3}+2\sqrt{-2734})/\alpha\). Suppose an odd unramified prime q is \(-1\bmod387860\) and splits in E, and at one place above it \(\phi\) generates \(\mathbb F_q^\times\) while \(\beta\) is a sixth power. Then \((q-1,6\cdot387860)=6\), since it splits in \(\mathbb Q(\sqrt{-3})\) and \(387860\) is prime to 3. The prime q is inert in the Gaussian integers, and \(G\) generates the sixth-power subgroup of order \(m=(q-1)/6\); m is odd since \(q\equiv3\bmod4\). There is then an actual \(n\bmod m\) with \(G^n=\beta\). At that place \(u_n=\alpha G^n\) specializes to \(2\sqrt{-3}+2\sqrt{-2734}\), whose complementary factor \(2\sqrt{-3}-2\sqrt{-2734}\) makes product 10924. Hence \(X_n=(u_n+10924/u_n)/2\) specializes to \(2\sqrt{-3}\), giving \(q\mid R_n\). Splitting alone does not imply that the same-place subgroup condition holds. At 31, for example, the actual step \(G\) is the identity and the orbit has \(R_n\equiv1\pmod{31}\).

Finite exact examples at period \(m=(q-1)/6\): \(q=5042179,\ n=781774\) gives valuation one and an index in the same coarse class gives exactly valuation two. At \(q=354757260218899,\ n=38125102841913\) the valuation is one and m is coprime to \(3\cdot2731\). The replay verifies primality, exact odd period and exact valuations; these examples do not imply equidistribution or a non-Wieferich density.

## Bounded overlap cannot drive the sieve mass to zero

Take any distinct sequence of genuinely active inert primes of the above period type \(m_j=(q_j-1)/6\), not necessarily arising from the sufficient field condition, and suppose \(g_j=\gcd(m_j,\operatorname{lcm}_{i<j}m_i)\) is bounded by a fixed constant \(B_0\). Even if each prime deletes **all** its weak hits, the finite-stage CRT densities have a positive common lower bound. This concerns finite-stage densities and does not claim a natural density for the infinite intersection.

Indeed each prime \(p>B_0\) can occur in at most one \(m_j\). For each \(p\le B_0\), the smallest power \(p^a>B_0\) can likewise occur only once. Removing these finitely many exceptional steps, write \(m_j=d_js_j\) where \(d_j\) ranges over a finite set of bounded small-prime parts and the \(s_j\) are pairwise coprime. Composite \(s_j\) have convergent reciprocal sum since each is at least the square of its mutually distinct smallest prime; \(s_j=1\) occurs only finitely often as the q are distinct. For prime \(s_j\) each fixed \(d_j\) requires both \(s_j\) and \(6d_js_j+1\) prime. The two-linear-form [Selberg upper sieve](https://arxiv.org/pdf/2211.11012), applied for each fixed d, gives \(O_d(x/\log^2 x)\) such primes up to x, making their reciprocal sum converge by partial summation. Thus \(\sum_j g_j/m_j<\infty\).

The [quadratic residue equation for activation](PELL_OVERLAPPING_PERIOD_SIEVE_AND_ANCHOR.md) gives at most two residues modulo any \(m_j\), because \(G^{2n}\) runs through the full odd-order subgroup. Within any previous surviving class the next weak-hit deletion rate is at most \(2g_j/m_j\). The anchor \(n=0\) survives every finite stage because its prime residual is split, so no finite stage deletes everything. Summability now leaves a uniform positive lower bound on the finite-stage CRT masses. In particular a search for ever-new pairwise coprime periods alone cannot produce a zero-density proof in this period family. Unbounded overlaps and existence of suitable dense activation families remain distinct problems.

### Exact finite replay

~~~javascript
const x0=3577n,p0=1599n,K=10936n,C=10924n;
const mod=(a,q)=>(a%q+q)%q;
function mul([a,b],[c,d],q){return [mod(a*c+5n*b*d,q),mod(a*d+b*c,q)]}
function pow(e,q){let u=[1n,0n],w=[9n,4n];while(e){if(e&1n)u=mul(u,w,q);w=mul(w,w,q);e>>=1n}return u}
function ok(x){if(!x)throw Error("certificate mismatch")}
function prime(q){if(q<2n||q%2n===0n)return q===2n;for(let d=3n;d*d<=q;d+=2n)if(q%d===0n)return false;return true}
function res(n,q){const P=mul([x0,p0],pow(387860n*n,q),q)[1];return mod(5n*P*P+K,q)}
ok(C===x0*x0-5n*p0*p0&&prime(5n*p0*p0+K)&&(5n*p0*p0+K)%4n===1n);
let q=5042179n;
ok(prime(q)&&q%4n===3n&&mod(q,387860n)===387859n);
ok(res(781774n,q*q)===1537948n*q);
const b=res(3901013728465n,q**3n);
ok(b%q**2n===0n&&b!==0n&&3901013728465n%840363n===781774n);
const q2=354757260218899n,a=38125102841913n;
ok(prime(q2)&&q2%4n===3n&&res(a,q2*q2)%q2===0n&&res(a,q2*q2)!==0n);
ok(((q2-1n)/6n)%3n!==0n&&((q2-1n)/6n)%2731n!==0n);
ok(pow(387860n,31n).join(",")==="1,0"&&res(0n,31n)===1n);

for(const q of [5042179n,q2]){
  ok((q-1n)%6n===0n);
  const m=(q-1n)/6n;
  ok(pow(387860n*m,q).join(",")==="1,0");
  let n=m,fs=[];
  for(let p=2n;p*p<=n;p++)if(n%p===0n){fs.push(p);while(n%p===0n)n/=p}
  if(n>1n)fs.push(n);
  for(const p of fs)ok(pow(387860n*m/p,q).join(",")!=="1,0");
}

~~~
