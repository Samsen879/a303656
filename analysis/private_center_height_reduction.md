# Ordinary-height escape from a private center row

**The private-center gcd does not by itself rule out a finite cover at ordinary height.** It counts prime-level matches across a full period, where the available exponents may exceed the height bound. It does give an exact reduction: after fixing the other rows’ exponent residues and the passive coordinate’s required \(p\)-digits, one can test escape from the center row using at most one candidate shift per surviving phase and even valuation depth. The reduction also works when some active lift digits are pinned.

## Exact reduction at ordinary height

Consider \(R=n-3^c-5^d>0\) and a center prime \(p>5\). Choose \(K\) with \(p^K\ge n\), so \(v_p(R)<K\). On a fixed CRT class, write the exponent periods as \(A_3,A_5\). Include the periods needed to preserve all other rows’ residual congruences. Refine the class by fixing \(d\bmod p^{K-1}\), so \(A_5\) includes that factor. This suffices to preserve \(5^d\bmod p^K\) within each prime-level phase. One can use a smaller passive period when the actual order permits it.

Put \(h_b=\operatorname{ord}_p(b)\) and \(H_b=\operatorname{lcm}(A_b,h_b)\). For each compatible prime-level phase with \(p\mid R\), let \(e,f\) be its least nonnegative exponent representatives modulo \(H_3,H_5\). When \(p\mid n\), the phase count is either zero or exactly
\[
G=\gcd\!\left(\frac{h_3}{\gcd(h_3,A_3)},\frac{h_5}{\gcd(h_5,A_5)}\right).
\]
This follows by intersecting the two allowed multiplicative cosets after negating one of them. For a unit target modulo \(p\), use the actual shifted-coset intersection instead.

The passive exponent can be kept at \(f\), since increasing it within the phase preserves the tested residual congruences and increases the shift. Let
\[
R(j)=n-3^{e+H_3j}-5^f,\qquad s=v_p(3^{H_3}-1).
\]
If \(v_p(R(0))<s\), all \(j\) have that same valuation. Otherwise, for each \(k\ge s\), divisibility by \(p^k\) gives a unique residue
\[
j\equiv j_k\pmod{p^{k-s}},\qquad 0\le j_k<p^{k-s}.
\]
The next lift digit is obtained by one linear equation modulo \(p\). This follows from \(v_p(3^{H_3m}-1)=s+v_p(m)\). The least \(j\) giving **exactly** valuation \(k\) is \(j_k\) if \(R(j_k)\not\equiv0\bmod p^{k+1}\), and \(j_k+p^{k-s}\) otherwise. Test its shift against \(3^c+5^d<n\). This includes higher even valuations and uses the actual \(s\), including when pins force \(s>1\).

Valuation zero needs at most three candidates: the least pair in the CRT class and that pair with one period added to either coordinate. If the least pair has \(p\mid R\), only a coordinate whose period changes its power modulo \(p\) can produce a unit residual. Its first increment already does so, at the smallest height possible using that coordinate.

Thus a finite panel covers the positive residuals only if, in every CRT class that survives the other rows, **all** these center escape candidates miss the ordinary height bound. For a complete finite test, take each other row’s modulus high enough to distinguish all valuations below \(n\), and inspect its surviving classes. The reduction does not bound how many such classes there are.

## Native height control

Take the actual panel \(\{7,11\}\) and the class \(c\equiv0,\ d\equiv3\pmod5\). Both orders at 11 are 5, so this class fixes the shift modulo 11. At 7 both orders are 6 and \(G=6\).

| Target | Ordinary result in this class |
|---:|---|
| \(133\) | Only \((0,3)\) lies below the target. Its shift is \(126\), and the residual \(7\) is covered by row 7. |
| \(3906=133+11\cdot7^3\) | The same modular data modulo \(11\cdot7^3\) now allow the shift \(368\) at \((5,3)\). This is the least escape, with valuation zero at both rows. |
| \(2527=126+7^4\) | The least shift \(126\) escapes with valuation **four** at 7 and valuation zero at 11. |

This is a cover of one actual valuation-preserving CRT class at \(133\). The full exponent window has an escape: \(133=11^2+2^2+3^1+5^1\). The example shows why the gcd count cannot replace the height test.

## Inline replay

This JavaScript replay uses exact `BigInt` arithmetic. It checks the three targets and two deeper lift cases, including one where pinning \(c\bmod7\) makes the first adjustable depth \(s=2\).

```javascript
const p = 7n;
const mod = (x,m) => (x%m+m)%m;
function check(ok) { if (!ok) throw Error("assertion"); }
function gcd(a,b) { while (b) [a,b]=[b,a%b]; return a; }
function lcm(a,b) { return a/gcd(a,b)*b; }

function pow(a,k,m) {
    let x=1n;
    while (k) {
        if (k%2n) x=x*a%m;
        a=a*a%m;
        k/=2n;
    }
    return x;
}
function ord(a,q) {
    let h=1n,x=a%q;
    while (x!==1n) { x=x*a%q; h++; }
    return h;
}
function val(x,K) {
    let k=0;
    while (k<K && x%p===0n) { k++; x/=p; }
    return k;
}

// The test class is c=0 mod A, d=3 mod 5.
// Refine d to the phase containing d=3 modulo p^(K-1).
function solve(n,A=5n,onlyPositiveEven=false) {
    let K=0,P=1n;
    while (P<n) { P*=p; K++; }
    const B=lcm(5n,P/p), h3=ord(3n,p), h5=ord(5n,p);
    const H=lcm(A,h3), J=lcm(B,h5);
    const G=gcd(h3/gcd(h3,A),h5/gcd(h5,B));
    const s=val(mod(pow(3n,H,P)-1n,P),K);
    let best=null;

    function offer(c,d,k) {
        const bits=BigInt(n.toString(2).length);
        if ((onlyPositiveEven && k===0) || c>=bits || d>=bits) return;
        const shift=3n**c+5n**d;
        if (shift<n && (best===null || shift<best[0])) {
            check(val(n-shift,K)===k);
            best=[shift,c,d,k];
        }
    }

    for (const [c,d] of [[0n,3n],[A,3n],[0n,3n+B]])
        if (mod(n-pow(3n,c,p)-pow(5n,d,p),p)!==0n) offer(c,d,0);

    const X=new Map();
    for (let c=0n;c<H;c+=A) X.set(pow(3n,c,p),c);
    let count=0n;
    for (let d=3n;d<J;d+=B) {
        const c=X.get(mod(n-pow(5n,d,p),p));
        if (c===undefined) continue;
        count++;
        const k0=val(mod(n-pow(3n,c,P)-pow(5n,d,P),P),K);
        if (k0<s || s===K) {
            if (k0<K && k0%2===0) offer(c,d,k0);
            continue;
        }
        let j=0n,T=1n;
        for (let k=s;k<K;k++) {
            const Pk=p**BigInt(k), m=Pk*p;
            const x=pow(3n,c+H*j,m);
            const r=mod(n-x-pow(5n,d,m),m);
            const slope=x*((pow(3n,H*T,m)-1n)/Pk)%p;
            check(r%Pk===0n && slope!==0n);
            const digit=(r/Pk)*pow(slope,p-2n,p)%p;
            if (k%2===0) offer(c+H*(j+(digit===0n ? T : 0n)),d,k);
            j+=T*digit;
            T*=p;
        }
    }
    check(count===G);  // All targets in this replay are zero mod 7.
    return {best,G,s};
}

check(ord(3n,11n)===5n && ord(5n,11n)===5n);
for (const n of [133n,3906n,2527n]) check((n-126n)%11n!==0n);
check(3906n-133n===11n*7n**3n && 5n**8n>3906n);
check(solve(133n).best===null && solve(133n).G===6n);
check(solve(3906n).best[0]===368n && solve(3906n).best[3]===0);
check(solve(2527n,5n,true).best[0]===126n);
check(solve(2527n,5n,true).best[3]===4);
check(11n**2n+2n**2n+3n+5n===133n);

const shift=3n**30n+125n;
check(solve(shift+49n,5n,true).best[0]===shift);
check(solve(shift+49n,5n,true).best[3]===2);

const later=3n**210n+125n;
let t=mod(-(later-126n)/49n,7n);
check(t!==0n);
if (val(later+49n*t-126n,5)>3) t+=7n;
const pinned=solve(later+49n*t,35n,true);
check(pinned.s===2 && pinned.best[0]===later && pinned.best[3]===2);
```

## Two free lift coordinates: at most \(2p\) slices

The passive-coordinate refinement in draft PR #85 can be removed for a fixed prime-level phase with two free lift coordinates. **At most \(2p\) slices suffice to find the minimum ordinary shift with positive residual of even valuation.** Each slice has an exact one-axis minimum that takes at most two further height checks after its baseline. A native \(7,11\) example also shows that the minimizing lift can require **both** axes. [Draft PR #85](https://github.com/Samsen879/a303656/pull/85/files)

## A bounded search with both coordinates free

Fix the target \(n\), preserve the other rows’ residues, and work in a single prime-level phase
\[
c=c_0+H_3i,\qquad d=d_0+H_5j,\qquad i,j\ge0.
\]
Write \(X=3^{c_0},\,Y=5^{d_0},\,A=3^{H_3},\,B=5^{H_5}\). Both \(A\) and \(B\) are \(1\bmod p\). The ordinary shift is \(XA^i+YB^j\), and we require it to be strictly below \(n\).

First consider one axis, with the other summand held fixed. Let \(R_0>0\) be the residual at index zero, and let \(s=v_p(A-1)\) for the moving axis.

- If \(v_p(R_0)\) is even, index zero is the minimum. If \(v_p(R_0)<s\) is odd, that valuation is constant along the axis.
- If \(v_p(R_0)\ge s\) is odd and \(s\) is even, index 1 gives exact valuation \(s\), provided it lies below the height bound.
- If both \(v_p(R_0)\ge s\) and \(s\) are odd, solve
  \[
  X\frac{A-1}{p^s}\,i_0\equiv R_0/p^s\pmod p,\qquad 0\le i_0<p.
  \]
  Every index below \(i_0\) has valuation \(s\). If \(i_0\) gives a positive residual of any even valuation, it is the minimum. If it gives a positive residual of odd valuation, the next possible index is \(i_0+p\), which gives exact valuation \(s+1\). The indices strictly between them have valuation \(s\). If \(i_0\) reaches or exceeds \(n\) in shift, the axis has no witness.

For the two-axis search, if the baseline residual has odd valuation below both adjustment depths, the entire phase has that odd valuation. Otherwise choose an axis whose adjustment depth is at most the baseline valuation. On that axis, the same lifting argument supplies a **modular cutoff index** \(J\le2p-1\): use index 1 when its depth \(s\) is even, or the first of \(i_0,i_0+p\) giving exact valuation \(s+1\) when \(s\) is odd. The cutoff may be above the ordinary height bound.

Any point with index greater than \(J\) on the chosen axis has shift greater than the cutoff shift. If the cutoff is below \(n\), that larger point cannot be a minimum. If the cutoff is at or above \(n\), the larger point is outside the ordinary window anyway. Thus it suffices to inspect indices \(0,\ldots,J\) on that axis and solve the other axis exactly on each slice. If both axes supply cutoffs, use the smaller index bound. This argument permits unequal adjustment depths and partially pinned lift digits.

## Native mixed minimum

Use center 7, preserve a unit residual at 11, and take \(c=30i,\ d=30j\). Both bases have order 6 modulo 7 and order 5 modulo 11. At
\[
n=867361737988403547205962240695953369142978
\]
the residual is a unit at 11 throughout the phase. At 7, divisibility by \(7^2\) is equivalent to \(i+j\equiv2\bmod7\). The three smallest possible shifts under that condition are the two axis points and the mixed point below. All three lie below the **same** target and give exact valuation two.

| Lift | Exponents \((c,d)\) | Shift |
|---|---:|---:|
| Mixed minimum | \((30,30)\) | \(931322780506610610274\) |
| First axis minimum | \((60,0)\) | \(42391158275216203514294433202\) |
| Second axis minimum | \((0,60)\) | \(867361737988403547205962240695953369140626\) |

Two controls preserve the same target residue modulo \(11\cdot7^3\). At \(931322780506610610470\), the mixed witness fits but neither axis has a witness. At \(275\), the phase has **no ordinary witness**, although the even-valuation modular lifts still exist. These statements concern the fixed phase and the two tested primes. They do not establish a two-square representation or settle a full finite cover.

## Inline independent replay

An independent JavaScript replay follows. It compares the bounded slice search with direct ordinary-height enumeration for all three targets and separately verifies the axis minima.

```javascript
const p = 7n, A = 3n**30n, B = 5n**30n, M = 11n*p**3n;
const mod = (x,m) => (x%m+m)%m;
function check(ok) { if (!ok) throw Error("assertion"); }

function val(x) {
    check(x !== 0n);
    let v=0;
    while (x%p===0n) { x/=p; v++; }
    return v;
}
function pow(x,e,m) {
    let y=1n;
    while (e) {
        if (e%2n) y=y*x%m;
        x=x*x%m;
        e/=2n;
    }
    return y;
}
function root(X,a,s,R) {
    const D=p**BigInt(s);
    const slope=mod(X*((a-1n)/D),p);
    return mod((R/D)*pow(slope,p-2n,p),p);
}

// Least index with positive residual of even valuation.
function axis(n,X,a,Y) {
    const R=n-X-Y;
    if (R<=0n) return null;
    const v=val(R), s=val(a-1n);
    if (v%2===0) return 0n;
    if (v<s) return null;
    if (s%2===0) return n-X*a-Y>0n ? 1n : null;
    const j=root(X,a,s,R), r=n-X*a**j-Y;
    if (r<=0n) return null;
    if (val(r)%2===0) return j;
    return n-X*a**(j+p)-Y>0n ? j+p : null;
}

function cutoff(n,X,a,Y) {
    const s=val(a-1n), R=n-X-Y;
    if (val(R)<s) return null;
    if (s%2===0) return 1n;
    const j=root(X,a,s,R);
    return (n-X*a**j-Y)%p**BigInt(s+2)===0n ? j+p : j;
}

function solve(n) {
    if (n<=2n) return null;
    if (val(n-2n)%2===0) return [2n,0n,0n];
    const J=cutoff(n,1n,A,1n), K=cutoff(n,1n,B,1n);
    if (J===null && K===null) return null;
    const flip=J===null || (K!==null && K<J);
    const [a,b,last]=flip ? [B,A,K] : [A,B,J];
    let best=null;
    for (let i=0n; i<=last; i++) {
        const X=a**i;
        if (X+1n>=n || (best && X+1n>=best[0])) break;
        const j=axis(n,1n,b,X);
        if (j===null) continue;
        const S=X+b**j;
        if (!best || S<best[0]) best=flip ? [S,j,i] : [S,i,j];
    }
    return best;
}

function brute(n) {
    let best=null;
    for (let i=0n; A**i+1n<n; i++)
        for (let j=0n; A**i+B**j<n; j++) {
            const S=A**i+B**j;
            if (val(n-S)%2===0 && (!best || S<best[0])) best=[S,i,j];
        }
    return best;
}

const n0=275n, tight=931322780506610610470n;
const n=867361737988403547205962240695953369142978n;
for (const t of [n0,tight,n]) {
    check(mod(t-n0,M)===0n && t%11n===0n);
    check(String(solve(t))===String(brute(t)));
}
check([A,B].every(x => x%7n===1n && x%11n===1n && val(x-1n)===1));
check(mod((A-1n)/p,p)===2n && mod((B-1n)/p,p)===2n);
check(solve(n0)===null);
check(axis(tight,1n,A,1n)===null && axis(tight,1n,B,1n)===null);
check(String(solve(tight))===String([A+B,1n,1n]));
check(String(solve(n))===String([A+B,1n,1n]));
check(axis(n,1n,A,1n)===2n && axis(n,1n,B,1n)===2n);
for (const S of [A*A+1n,A+B,1n+B*B])
    check(S<n && val(n-S)===2 && (n-S)%11n!==0n);
check(A+B<A*A+1n && A+B<1n+B*B);
```
