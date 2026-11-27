# Exact ordinary-height frontier for two active inert primes

For two distinct primes \(p,q\equiv3\pmod4\) in a fixed native phase, the minimum ordinary shift can be found with at most **\(3pq\) slices**. On each slice, each pair of possible even valuations contributes at most one shift to test. The bound comes from joining the first repair digits before imposing the height cutoff. It uses no full-period enumeration and permits different adjustment depths at the two primes.

The native example below shows that keeping only the independently cheapest escape for each prime is unsound. Both exist at the same target, both fail the other prime, and the joint minimum is a different lift. This extends the one-center reduction in [draft PR #85](https://github.com/Samsen879/a303656/pull/85/files).

## Two-center cutoff and exact search

Fix a rectangular phase that preserves the other rows, and write its shifts as
\[
S(i,j)=XA^i+YB^j,\qquad i,j\ge0,
\]
where \(A,B\) are the actual step powers of 3 and 5. Assume \(A,B\equiv1\pmod{pq}\). We seek \(S<n\) with both valuations of \(R=n-S\) even. If the baseline shift is at least \(n\), every point fails by monotonicity; hence assume its residual is positive.

For \(r\in\{p,q\}\), set \(s_r=\min(v_r(A-1),v_r(B-1))\). If the baseline residual has valuation below \(s_r\), that valuation is constant throughout the phase. An odd value gives immediate infeasibility. An even value imposes no restriction.

At each remaining prime, construct a modular point of exact even valuation as follows:

- For **odd** \(s_r\), impose \(R\equiv0\pmod{r^{s_r+1}}\). This is one affine linear equation in \(i,j\bmod r\) with at least one nonzero coefficient.
- For **even** \(s_r\), the desired first valuation is \(s_r\), so no initial equality is needed.

Join the initial equations by CRT, taking \(0\le i_0,j_0<M\), where \(M\) is the product of the primes with initial equations. In particular \(M\le pq\). Now vary
\[
(i,j)=(i_0,j_0)+Mt(u,v).
\]
For each remaining prime, the digit that must stay nonzero is affine in \(t\). At an even \(s_r\) it is the digit at depth \(s_r\). At an odd \(s_r\) it is the digit at depth \(s_r+1\), since \(r\) divides \(M\) once. The binomial expansion gives a nonzero slope vector in either case. Each prime rules out at most one of the directions \((1,0),(0,1),(1,1)\). Choose a direction allowed by both, then try \(t=0,1,2\). Each prime excludes at most one of those values, so one works. The resulting modular cutoff has both indices at most \(3M-1\).

Slice along the coordinate contributing the larger summand at that cutoff. Increasing its index beyond the cutoff index makes that summand alone exceed the entire cutoff shift: a step multiplies it by at least 3. If the cutoff fits below \(n\), no such point can minimize. If the cutoff is at or above \(n\), no such point fits. Either way, at most \(3M\) slices suffice.

On a slice, the one-axis lifting formula expresses **exact** even valuation \(k\) as a congruence class with one next-digit subclass excluded. Join the two lower congruences by CRT. Starting from their least common index, each excluded subclass rules out at most one of the first three progression indices. The first survivor is the least shift for that valuation pair. Test it against \(n\). Only depths with \(r^k<n\) need consideration, so this uses \(O((1+\log_p n)(1+\log_q n))\) valuation pairs per slice. A modular cutoff above \(n\) can bound the search even when the search returns no ordinary witness.

## Same-target native counterexample

Use \(c=90i,\ d=90j\), with active rows 7 and 11 and a fixed unit residual at 19. Put \(S(i,j)=3^{90i}+5^{90j}\) and take
\[
n=S(6,3)+7\,986\,363.
\]
The adjustment depths of the two axes are \((1,1)\) at 7 and \((2,1)\) at 11. In this phase, the necessary divisibility conditions for even valuation are
\[
i+j\equiv2\pmod7,\qquad j\equiv3\pmod{11}.
\]

| Test | Minimum \((i,j)\) | Valuations at \(7,11,19\) |
|---|---:|---:|
| Even at 7 | \((1,1)\) | \(2,1,0\) |
| Even at 11 | \((0,3)\) | \(1,2,0\) |
| Even at both | \((6,3)\) | \(2,2,0\) |

All three shifts lie below the same \(n\). For a height control, take \(n'=S(0,3)+2\,434\,278\). It has the same residue modulo \(7^3\cdot11^3\cdot19\). Both individual minima still fit, but **no joint ordinary witness** fits in this phase. Testing only these primes does not establish a two-square representation.

## Inline independent replay

The following exact JavaScript replay checks both targets. It joins exact-valuation classes on each slice and compares the result with direct ordinary-height enumeration at both targets.

```javascript
const p=7n, q=11n, r=19n, A=3n**90n, B=5n**90n;
const S=(i,j)=>A**BigInt(i)+B**BigInt(j);
const mod=(x,m)=>(x%m+m)%m;
function ok(b) { if (!b) throw Error("assertion"); }
function val(x,m) {
    ok(x!==0n);
    let k=0;
    while (x%m===0n) { x/=m; k++; }
    return k;
}
function pow(a,e,m) {
    let x=1n;
    while (e) {
        if (e%2n) x=x*a%m;
        a=a*a%m;
        e/=2n;
    }
    return x;
}
function inv(a,m) {
    let b=m,x=1n,y=0n;
    while (b) {
        const q=a/b;
        [a,b]=[b,a%b];
        [x,y]=[y,x-q*y];
    }
    ok(a===1n);
    return mod(x,m);
}

// Each entry is [residue, period, excluded next-digit class].
function classes(n,X,b,l,fits) {
    const s=val(b-1n,l), v=val(n-X-1n,l);
    if (v<s) return v%2===0 ? [[0n,1n,null]] : [];
    let j=0n,T=1n,D=l**BigInt(s),out=[];
    for (let k=s; D<n && fits(j); k++,D*=l) {
        const m=D*l,x=pow(b,j,m),R=mod(n-X-x,m);
        const slope=x*((pow(b,T,m)-1n)/D)%l;
        ok(R%D===0n && slope!==0n);
        const next=j+T*((R/D)*pow(slope,l-2n,l)%l);
        if (k%2===0) out.push([j,T,[next,T*l]]);
        j=next;
        T*=l;
    }
    return out;
}
function bestSlice(n,X,b) {
    const bits=BigInt(n.toString(2).length);
    const fits=j=>j<bits && X+b**j<n;
    const U=classes(n,X,b,p,fits), V=classes(n,X,b,q,fits);
    let best=null;
    for (const [a,m,e] of U) for (const [d,k,f] of V) {
        const j0=k===1n ? a : a+m*mod((d-a)*inv(m,k),k);
        for (let z=0n; z<3n; z++) {
            const j=j0+z*m*k;
            if (!fits(j)) break;
            if ((e && (j-e[0])%e[1]===0n) ||
                (f && (j-f[0])%f[1]===0n)) continue;
            if (best===null || j<best) best=j;
            break;
        }
    }
    return best;
}
function frontier(n) {
    let best=null;
    // The modular cutoff is (6,3), with A^6 > B^3.
    for (let i=0; i<=6 && S(i,0)<n; i++) {
        const j=bestSlice(n,A**BigInt(i),B);
        if (j!==null && (!best || S(i,j)<best[0]))
            best=[S(i,j),i,Number(j)];
    }
    return best;
}
function brute(n,primes) {
    let best=null;
    for (let i=0; S(i,0)<n; i++)
        for (let j=0; S(i,j)<n; j++)
            if (primes.every(l=>val(n-S(i,j),l)%2===0) &&
                (!best || S(i,j)<best[0]))
                best=[S(i,j),i,j];
    return best;
}

const n=S(6,3)+7986363n, low=S(0,3)+2434278n;
const M=p**3n*q**3n*r, same=(a,b)=>String(a)===String(b);
ok(n%M===3483251n && low%M===n%M);
ok([p,q,r].every(l=>A%l===1n && B%l===1n));
ok(val(A-1n,p)===1 && val(B-1n,p)===1);
ok(val(A-1n,q)===2 && val(B-1n,q)===1);
ok(A**6n>B**3n);
for (const t of [n,low]) {
    ok(mod(t-2n,r)!==0n);
    ok(same(brute(t,[p]),[S(1,1),1,1]));
    ok(same(brute(t,[q]),[S(0,3),0,3]));
    ok(val(t-S(1,1),p)===2 && val(t-S(1,1),q)===1);
    ok(val(t-S(0,3),p)===1 && val(t-S(0,3),q)===2);
    ok(same(frontier(t),brute(t,[p,q])));
}
ok(same(frontier(n),[S(6,3),6,3]));
ok(frontier(low)===null);
ok(val(n-S(6,3),p)===2 && val(n-S(6,3),q)===2);
```
