# Deep reader capacities and overload order signatures

**A stalled last-parent allocation forces a quantitative order signature**, provided the remaining sinks have their full two-digit repair sets and the unresolved readers are common-Wieferich rows with nonzero observations. Readers that see a second digit on both axes have a stronger capacity bound than readers that see it on only one. The exclusions below concern first blocking of the full terminal-blind menu. The density ledger stays unchanged. [Verified last-parent allocation](https://github.com/Samsen879/a303656/commit/0a568b337e4723487d4e8575fdc2b7e40ff85569)

### Capacity of a physical reader

Let \(r\) be a doubly ordinary rooted parent with both first and second \(r\)-digits available on both axes. Its exact-valuation-two repair set has \(N_r=r^2(r-1)\) points. There are \(r\) first-digit choices on the affine repair line and \(r(r-1)\) legal second-digit pairs above each. Freeze the other parents of a nonzero reader \(p\). Write
\[
K_r=\left\lfloor\frac{1+\sqrt{4r-3}}2\right\rfloor,\qquad
J_r=\left\lfloor\frac{1+\sqrt{1+4(r^3-r)}}2\right\rfloor.
\]

| Reader depths on the two axes | Maximum number of repairs rejected |
|---|---:|
| Maximum depth one | \(K_r\,r(r-1)\) |
| Exactly one axis reads depth two, the other at most one | \(r(r-1)\) |
| Both axes read depth two | \(J_r\) |

The shallow bound is the existing nonzero fiber bound. In the mixed case, fixing the first-digit pair leaves at most one hit on the deeper axis. It admits at most \(r-1\) second digits on the other axis. [Verified shallow fiber bound](https://github.com/Samsen879/a303656/commit/b02e45616a61d7d413bc260aa36ec71c2355bb0d)

For the doubly deep bound, write the two exponent coordinates as \(x,y\bmod r^2\). Every difference \((u,v)\) between repairs satisfies \(v\equiv\lambda u\bmod r\), where \(\lambda\ne0\) is the slope of the first-digit repair line. There are \(r^3\) such differences. The reader sees \(A X^x+B Y^y\), where \(X,Y\) both have order \(r^2\). For a difference with \(X^u\ne Y^v\), the two hit equations determine the two terms uniquely, and therefore determine the ordered pair of repairs. If \(X^u=Y^v\), the difference cannot join two distinct hits at a nonzero target. At least \(r\) differences have equal multipliers. Indeed, writing \(X=Y^\mu\), take \(u\equiv0\bmod r\) and \(v=\mu u\bmod r^2\). Thus a fiber of size \(H\) satisfies \(H(H-1)\le r^3-r\). Discarding the illegal valuation-three lifts can only reduce the fiber.

### Signature forced by a stalled sink

Use the backwards allocation with these capacities, charging each physical reader once at its last parent. At any sink \(r\) where the procedure stalls, let \(m_1,m_2,m_{22}\) count the three reader types above. Then
\[
m_1K_r r(r-1)+m_2r(r-1)+m_{22}J_r\ \ge\ N_r .
\]
In particular, a core with no shallow readers needs at least \(r\) distinct physical readers at that sink. At \(r=31\), a sink supplied entirely by one type needs at least **6 shallow**, **31 mixed**, or **167 doubly deep** readers, respectively.

For an unresolved reader \(p\), let \(A_p\) be its full support in the remaining allocation and \(e_s(p)\) its maximum read depth at \(s\in A_p\). Put
\[
D_p=\prod_{s\in A_p}s^{e_s(p)}.
\]
The actual orders force \(D_p\mid p-1\). Thus its physical prime lies in \(2D_p+1\bmod4D_p\). For \(m\) readers sharing any odd divisor \(D\mid D_p\), their squared product is at least
\[
\prod_{j=0}^{m-1}(a_D+4Dj)^2 ,
\]
where \(a_D\) is the first integer above the existing cutoff \(B\) in that progression. This gives a direct exclusion when the progression has fewer than \(m\) places below the terminal. If a subfamily also has the same full order pair \((d_3,d_5)\), its squared product divides \(\gcd(\Phi_{d_3}(3),\Phi_{d_5}(5))\). That follows from the common-Wieferich condition and exact orders, since no lower-order factor vanishes at those primes. The product lower bound can therefore be checked against a single integer for each exact pair. [Exact-order cyclotomic charging](https://github.com/Samsen879/a303656/blob/9826d9cfa8038c80f460fafe27f24dc2ce99acd6/analysis/ajt5_overnight_2026_11_26/EXACT_ORDER_LOW_DENSITY_BOUND.md)

For two legal probes with distinct terminal residues, if both repair plans meet the preservation hypotheses and all sinks can be peeled, the terminal cannot first block. A first blocker must therefore defeat at least one plan through a fixed-row failure, an unavailable repair set, or an overloaded set satisfying the inequality. The signature covers **nonzero readers of depth at most two** with unlocked repair digits. Zero readers capable of whole-line cancellation, deeper reads, and externally fixed digits require their own capacities. An overload is necessary for failure of this certificate and may still admit an exact repair.

### Standalone arithmetic check

The ordinary controls at \(17299\) and \(21143\) both read a second \(31\)-digit. Their exact maximum nonzero fibers on the **same** 28,830-point repair set are **7** and **60**. The chosen observations realize those maxima as exact valuation-one hits with the reader digits frozen. These are capacity controls and supply no common-Wieferich first blocker.

```python
from collections import Counter
from math import isqrt

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

def order(b,p):
    return next(k for k in range(1,p) if pow(b,k,p)==1)

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

def cap(differences):
    return (1+isqrt(1+4*differences))//2

r,p,t = 31,17299,21143
n,L = 1334256450985389397781457123,1448380917720
assert all(prime(u) and u%4==3 for u in (r,p,t))
assert [tuple(order(b,u) for b in (3,5)) for u in (r,p,t)] == [
    (30,3),(17298,8649),(10571,682)]
assert all(pow(b,u-1,u*u)!=1 for u in (r,p,t) for b in (3,5))
assert L%3960==0 and L%r
assert (n%3,n%32,n%r**3)==(0,3,1095)
assert (n-S(2,3,32))%4==1 and n%3!=pow(5,3,3)
assert all((n-S(2,3,u))%u for u in (7,11,19,23))

grid = []
for i in range(r):
    j, = [j for j in range(r)
          if (n-S(2+L*i,3+L*j,r*r))%(r*r)==0]
    for a in range(r):
        for b in range(r):
            x,y = 2+L*(i+r*a),3+L*(j+r*b)
            z = (n-S(x,y,r**3))%r**3
            if z:
                assert z%(r*r)==0
                grid.append((x,y))

N = r*r*(r-1)
assert len(grid)==N==28830
for u,want in ((p,7),(t,60)):
    hist = Counter(S(x,y,u) for x,y in grid)
    assert n%u and hist[n%u]==max(v for k,v in hist.items() if k)==want
    assert sum((n-S(x,y,u*u))%(u*u) in range(u,u*u,u)
               for x,y in grid)==want

K,J = cap(r-1),cap(r**3-r)
assert (K,J)==(6,173)
assert [(N+C-1)//C for C in (K*r*(r-1),r*(r-1),J)] == [6,31,167]

# Shared-reader count in the earlier two-parent control.
r,s,q = 163,379,3638251
D = r*s
assert max(0,(q-2*D-2)//(4*D)+1)==15
assert 15*cap(s-1)<s
assert min(2*D*r+1,2*D*s+1)>q  # No shared reader can be deep there.
```

For the mixed case, each fixed deeper digit leaves \(r-1\) choices on the other axis because exact valuation two excludes one affine second-digit relation with both coefficients nonzero. For a doubly deep reader, the \(r\) equal-multiplier differences consume at least \(r\) members of the \(r^3\)-element difference set, including zero; the ordered pair count applies only to distinct hits. The resulting overload is a limitation of the allocation certificate rather than an actual finite obstruction.

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

const r=31n,p=17299n,t=21143n,n=1334256450985389397781457123n,L=1448380917720n;
const S=(x,y,m)=>mod(pw(3n,x,m)+pw(5n,y,m),m);
const rr=(x,y,m)=>mod(n-S(x,y,m),m);
check([r,p,t].every(v=>isPrime(v)&&v%4n===3n&&pw(3n,v-1n,v*v)!==1n&&pw(5n,v-1n,v*v)!==1n));
check(n%3n===0n&&n%32n===3n&&n%r**3n===1095n&&L%3960n===0n);
const grid=[];
for(let i=0n;i<r;i++){
  const x=2n+L*i,js=[];
  for(let j=0n;j<r;j++)if(!rr(x,3n+L*j,r*r))js.push(j);
  check(js.length===1);
  const y=3n+L*js[0];
  for(let a=0n;a<r;a++)for(let b=0n;b<r;b++){
    const u=x+L*r*a,v=y+L*r*b,z=rr(u,v,r**3n);
    if(z){check(z%(r*r)===0n);grid.push([u,v]);}
  }
}
check(grid.length===28830);
for(const [q,want] of [[p,7],[t,60]]){
  const hits=new Map();let odd=0;
  for(const [x,y] of grid){
    const a=S(x,y,q);if(a)hits.set(a,(hits.get(a)||0)+1);
    const z=rr(x,y,q*q);if(z&&z%q===0n)odd++;
  }
  check(hits.get(n%q)===want&&Math.max(...hits.values())===want&&odd===want);
}
```
