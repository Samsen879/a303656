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
