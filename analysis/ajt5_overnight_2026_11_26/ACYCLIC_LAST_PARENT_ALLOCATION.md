# Acyclic last-parent allocation for a terminal-blind menu

**Last-parent allocation needs an ordering constraint in addition to capacity.** I obtained an exact test for whether an allocation is realizable by sequential repairs. It gives a necessary obstruction for first blocking of the whole terminal-blind menu. Actual orders at \(163,379,370663,3583067\) show why a matching that checks capacities alone can certify the wrong thing. No density charge changes. [Verified single-parent fiber bound](https://github.com/Samsen879/a303656/commit/b02e45616a61d7d413bc260aa36ec71c2355bb0d)

### Exact allocation test

Fix a legal ternary probe and a closed repair plan. Let \(P\) be its adjustable ordinary parents. Include every earlier row affected by their moves or by restoration. Ordinary repairs required before other parents give precedence constraints. Ordinary clean-up after certification must preserve the certified shifts, the head, and the terminal value.

For each physical exceptional reader \(h\) still requiring a unit test, let \(A_h\subseteq P\) contain **every** parent whose allowed repair digits can change its shift. Compute this from both base orders and the actual digits being moved, including second digits when visible. A reader with empty support requires its own fixed-phase check. For \(r\in A_h\), give the edge a uniform cost \(w_{rh}\) in excluded repair choices when all other parents of \(h\) are fixed. Set the cost to infinity if that edge cannot certify the reader. Let \(c_r\) be a uniform budget below the number of available repair choices. For a doubly ordinary rooted parent with its whole shallow line available, one can take \(c_r=r-1\) and the verified nonzero-reader cost
\[
K_r=\left\lfloor(1+\sqrt{4r-3})/2\right\rfloor.
\]
Single-character edges can use cost one. An axis fixed by a singly ordinary repair does not earn this bound merely because its order contains \(r\).

An allocation \(a(h)\in A_h\) with loads within budget is realizable **exactly when** adding the arrows
\[
r\longrightarrow a(h)\qquad(r\in A_h\setminus\{a(h)\})
\]
to the ordinary precedence graph leaves it acyclic. Necessity follows because the assigned parent must be last. For sufficiency, process a topological order. At each parent, use the union bound on its assigned readers, then complete the even lift using digits covered by the preservation hypotheses. Every reader is certified once, after its other modifying parents are fixed.

There is an equivalent greedy test that avoids guessing an allocation. Work **backwards**. Remove any remaining precedence sink \(r\) whose load from **all** still-unassigned readers containing \(r\) is at most \(c_r\). Assign those readers to \(r\) and delete them. Any feasible ordering has such a last parent. Choosing any eligible sink is safe because moving it to the end only transfers its incident readers to it and reduces other loads. Hence the procedure is exact for this uniform-budget method. This extends the fixed last-parent rule to selectable orders and retains the distinction between physical rows and their axis incidences. [Earlier fixed last-parent budget](https://github.com/Samsen879/a303656/blob/9edc3c4f3d9f06c107f8594583c8791cdead8d5f/analysis/ajt5_overnight_2026_11_26/LARGE_COMPLEMENT_SOURCE_RELEASE.md)

**Consequence for actual first blocking.** Take two legal probes from the full menu with distinct terminal residues and valid restoration boundaries. If both pass the backwards test, the terminal cannot first block. Thus, for every such pair at a first blocker, at least one probe must have a fixed-row failure or a nonempty remaining set in which every precedence sink is overloaded or ineligible. The certificate concerns the uniform-budget repair method. An overloaded set may still have a solution by exact hit-set intersection.

For two parents \(r,s\), the number of physical shared inert readers below \(q\) is bounded without finding primes. Each is \(1\bmod rs\) and \(3\bmod4\), so it lies in the progression \(2rs+1+4rsj\). In the fixture below there are at most 15 candidates below \(q=3638251\). With no private load at parent \(379\), even charging all 15 shared readers the worst shallow nonzero cost gives \(15\cdot19<379\). Hence the shared part alone cannot prevent backwards elimination there.

### Actual order-cycle control

Both readers \(370663,3583067\) read both first digits at both parents \(163,379\). Assigning the first reader to \(163\) and the second to \(379\) requires **both** orders of processing. The same positive integer realizes the loss of either early certificate. Starting at \((i,j)=(0,0)\), both readers are units. Moving only the \(379\)-repair digit to \(1\) gives exact valuation one at \(370663\). Moving only the \(163\)-repair digit to \(1\) gives exact valuation one at \(3583067\). The two parents have exact valuation two throughout these comparisons, and the terminal shift and legal head are preserved.

All primes in the fixture are ordinary. The two reader coordinates are frozen for the comparison. This is a real order constraint and a counterexample to precedence-free certification, while the shared readers are jointly avoidable in the fixture.

```python
from math import isqrt, lcm

r,s,p,t,q = 163,379,370663,3583067,3638251
head = (7,11,19,23)

def prime(v):
    return v > 1 and all(v % j for j in range(2, isqrt(v)+1))

def order(b,v,factors):
    d = v-1
    for f in factors:
        while d%f==0 and pow(b,d//f,v)==1:
            d //= f
    return d

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

rows = (r,s,p,t,q)
factors = ((2,3),(2,3,7),(2,3,r,s),(2,29,r,s),(2,3,5,7,11))
assert all(prime(v) and v%4==3 for v in rows)
orders = [tuple(order(b,v,F) for b in (3,5))
          for v,F in zip(rows,factors)]
assert orders == [(162,54),(378,21),(370662,370662),
                  (1791533,3583066),(134750,1819125)]
assert all(pow(b,v-1,v*v)!=1 for v in rows for b in (3,5))
assert all(o%(r*s)==0 for pair in orders[2:4] for o in pair)
assert all((v-1)%(a*a) for v in (p,t) for a in (r,s))

M = lcm(3960,(r-1)*r*r,(s-1)*s*s,(p-1)*p,(t-1)*t,q-1)

def step(a):
    d = M//(a*a)
    return d*pow(d,-1,a*a)

U,V = step(r),step(s)
c,d = 2,3
n = 1261206327675456504225656084640427765225538883
assert (n%3,n%32)==(0,3)

def slope(a,W):
    f,g = [((pow(b,W,a*a)-1)//a)*pow(b,e,a)%a
           for b,e in ((3,c),(5,d))]
    return -f*pow(g,-1,a)%a

lr,ls = slope(r,U),slope(s,V)
assert (lr,ls)==(27,224)
assert all(pow(b,a*W,h*h)==1 for a,W in ((r,U),(s,V))
           for h in (p,t) for b in (3,5))

def R(c,d,m):
    return (n-S(c,d,m))%m

def repair(i,j):
    x = c+U*i+V*j
    y = d+U*(lr*i%r)+V*(ls*j%s)
    for a,W in ((r,U),(s,V)):
        assert R(x,y,a*a)==0
        if not R(x,y,a**3):
            x += a*W
        assert R(x,y,a**3) in range(a*a,a**3,a*a)
    assert (x%3960,y%3960)==(c,d)
    assert R(x,y,32)%4==1 and (n-pow(5,y,3))%3
    assert all(R(x,y,h) for h in head)
    assert S(x,y,q)==S(c,d,q)
    return x,y

z00,z01,z10 = [repair(i,j) for i,j in ((0,0),(0,1),(1,0))]
assert (n%p,n%t)==(142152,3078720)
assert R(*z00,p) and R(*z00,t)
assert R(*z01,p*p)==p and R(*z10,t*t)==t
assert S(*z10,p)!=S(*z00,p) and S(*z01,t)!=S(*z00,t)

scopes = {p:{r,s},t:{r,s}}
K = {a:(1+isqrt(4*a-3))//2 for a in (r,s)}

def peel(cap):
    left = dict(scopes)
    remaining = set(cap)
    out = []
    while remaining:
        for a in sorted(remaining):
            fan = tuple(h for h,A in left.items() if a in A)
            if len(fan)*K[a]<=cap[a]:
                out.append((a,fan))
                remaining.remove(a)
                for h in fan:
                    del left[h]
                break
        else:
            return None
    return out

# One-reader quotas permit a matching but no last-parent ordering.
assert peel(K) is None
assert peel({r:r-1,s:s-1})==[(r,(p,t)),(s,())]
assert (q-2*r*s-2)//(4*r*s)+1==15
assert 15*K[s]<s
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

function gcd(a,b){while(b)[a,b]=[b,a%b];return a;}
const lcm=(a,b)=>a/gcd(a,b)*b;
const r=163n,s=379n,p=370663n,t=3583067n,q=3638251n;
const rows=[r,s,p,t,q],fac=[[2n,3n],[2n,3n,7n],[2n,3n,r,s],[2n,29n,r,s],[2n,3n,5n,7n,11n]];
function order(a,p,fac){let o=p-1n;for(const f of fac)while(o%f===0n&&pw(a,o/f,p)===1n)o/=f;return o;}
const o=rows.map((u,i)=>[order(3n,u,fac[i]),order(5n,u,fac[i])]);
check(o.flat().map(String).join()==="162,54,378,21,370662,370662,1791533,3583066,134750,1819125");
check(rows.every(u=>isPrime(u)&&u%4n===3n&&pw(3n,u-1n,u*u)!==1n&&pw(5n,u-1n,u*u)!==1n));
const M=[3960n,(r-1n)*r*r,(s-1n)*s*s,(p-1n)*p,(t-1n)*t,q-1n].reduce(lcm,1n);
const step=a=>{const z=M/(a*a);return z*iv(z,a*a);};
const U=step(r),V=step(s),c=2n,d=3n,n=1261206327675456504225656084640427765225538883n;
const S=(x,y,m)=>mod(pw(3n,x,m)+pw(5n,y,m),m);
const rr=(x,y,m)=>mod(n-S(x,y,m),m);
function slope(a,W){
 const f=(pw(3n,W,a*a)-1n)/a*pw(3n,c,a)%a,
       g=(pw(5n,W,a*a)-1n)/a*pw(5n,d,a)%a;
 return mod(-f*iv(g,a),a);
}
const lr=slope(r,U),ls=slope(s,V);check(lr===27n&&ls===224n);
function repair(i,j){
 let x=c+U*i+V*j,y=d+U*(lr*i%r)+V*(ls*j%s);
 for(const [a,W] of [[r,U],[s,V]]){
   check(rr(x,y,a*a)===0n);
   if(rr(x,y,a**3n)===0n)x+=a*W;
   const z=rr(x,y,a**3n);check(z>0n&&z%(a*a)===0n);
 }
 check(x%3960n===c&&y%3960n===d&&S(x,y,q)===S(c,d,q));
 check([7n,11n,19n,23n].every(u=>rr(x,y,u))&&rr(x,y,32n)%4n===1n);
 return [x,y];
}
const z00=repair(0n,0n),z01=repair(0n,1n),z10=repair(1n,0n);
check(rr(...z00,p)&&rr(...z00,t)&&rr(...z01,p*p)===p&&rr(...z10,t*t)===t);
check(S(...z10,p)!==S(...z00,p)&&S(...z01,t)!==S(...z00,t));
check((q-2n*r*s-2n)/(4n*r*s)+1n===15n&&15n*19n<s);
```
