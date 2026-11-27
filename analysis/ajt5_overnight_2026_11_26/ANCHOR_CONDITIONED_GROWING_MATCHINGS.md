# Growing ordinary matchings conditioned on a true anchor norm

**Yes. A positive fraction of the targets with a true \(S_0\) witness also have a growing distinct-axis matching of true alternative witnesses.** The argument counts distinct targets. Plaksin’s two-norm lower bound supplies the first moment, and Henriot’s discriminant-uniform upper bound supplies the second moment. [Starting point](https://github.com/Samsen879/a303656/commit/a56d290c26e8d2a2e97a91474cd4738ceae783d3)

### Statement and arithmetic setup

Keep \(A=3^a,\ B=5^b\), the balanced strip, and the ordinary window \(I=(2S_3-P,U]\). Put \(C=cE\), where \(c=5^j\), \(j\ge1\), and \(E\) is supported on a fixed finite set of split primes other than \(5\). Among targets \(n\in I\) with \(C\mid n-S_0\) and \(n-S_0\) a sum of two squares, a positive fraction have a matching of size
\[
\gg \min\!\left(\frac{b}{cE},\frac{b^{3/2}}{cE^2}\right).
\]
The constants are uniform in the prescribed powers when \(cE=o(b)\) and \(cE^2=o(b^{3/2})\). Taking \(C=5\) gives \(\gg b\) matched labels for a positive fraction of **all** true \(S_0\) targets in the window. The growing-\(C\) statement prescribes common divisibility.

Use the lower exponent rectangle \(a/10\le x\le a/3,\ b/5\le y\le b/3\), with
\[
x\equiv a\pmod{\operatorname{lcm}(4c/5,\varphi(E))},\qquad
y\equiv b+2\pmod{\operatorname{lcm}(2,\varphi(E))}.
\]
Every label \(S=3^x+5^y\) is \(S_0\bmod C\). The axis lengths are \(N_x\asymp b/(cE)\) and \(N_y\asymp b/E\), and the labels are distinct by the \(5\)-adic depth comparison of the two power differences.

Write \(t=(n-S_0)/C\), \(h_i=(S_0-S_i)/C\), \(X=B/C\), and \(K=N_xN_y\). The actual condition is that \(t\) is a norm, and an alternative succeeds precisely when \(t+h_i\) is a norm. Division by \(C\) preserves normhood in both directions because \(C\) has only split prime factors. The \(t\)-interval starts at \(\asymp X\), has length \(\asymp X\), and all shifts satisfy \(0<h_i<27X\), well below the interval start.

### Conditional moments

Let \(\beta\) be the indicator of sums of two squares and \(W(t)=\sum_i\beta(t+h_i)\). Plaksin’s theorem on p. 145 gives
\[
\sum_t\beta(t)\beta(t+h_i)\gg X/b
\]
uniformly for the shifts above. The interval has fixed positive proportional length, and the theorem’s shift factor is at least one. Thus \(\sum_t\beta(t)W(t)\gg XK/b\). [Plaksin’s theorem](https://www.mathnet.ru/php/getFT.phtml?jrnid=mzm&paperid=5142&what=fullt)

For \(r=2,3\) distinct monic shifts, Henriot’s upper bound gives
\[
\sum_t\prod_{\nu=1}^r\beta(t+d_\nu)
 \ll \frac{X}{b^{r/2}}\prod_{p\mid\Delta}(1+O_r(1)/p),
 \qquad \Delta=\prod_{\mu<\nu}(d_\mu-d_\nu)^2.
\]
At an unexceptional split prime, the sieve and multiplicative factors cancel to first order. At an inert prime, the local factor is \(1-r/p+O_r(p^{-2})\). The linear forms are monic, their coefficient norm is \(O(X^r)\), and the interval is long enough for the uniform bound. Only the upper-bound corollary is used. [Henriot, Corollary 2](https://arxiv.org/pdf/1102.1643#page=7) · [Erratum](https://doi.org/10.1017/S0305004114000280)

The discriminant factor averages over the **actual** offsets. Factor it into contributions from \(h_i,h_j,h_i-h_j\) and apply Hölder. For each resulting fixed power, expand over squarefree divisors with weight \(A_0^{\omega(d)}/d\), for a constant \(A_0\). On an axis of length \(N\), fixing the other exponents leaves at most one class modulo \(\operatorname{ord}_d(g^L)\), where \(g^L\) is the stride power. The fixed-support order argument from the baseline also works with this weight: the small smooth-order part costs \((\log(2T))^{O(1)}\) up to order \(T\), and the large smooth-order part has bounded reciprocal sum. For an actual difference \(|h|\ll B\), Rankin’s inequality with \(s=1/\lceil\log_2 b\rceil\) bounds the divisor tail above \(b^{O(\log b)}\) by \(O(b^{-2})\), taking the implied exponent sufficiently large. Below that cutoff, the one-class rounding error is \(O((\log b)^{O(1)}/N)\). This gives a bounded average over the full grid and the \(y\)-fibers. In the shorter \(x\)-fibers, the rounding term is absorbed by the diagonal bound.

Consequently,
\[
\sum_t\beta(t)W(t)^2\ll \frac{XK^2}{b^{3/2}},
\qquad
\sum_t\beta(t)\left(\sum_x W_x(t)^2+\sum_y W_y(t)^2\right)
 \ll \frac{XK(N_y+\sqrt b)}{b^{3/2}},
\]
where \(W_x,W_y\) count successful labels in a row or column. There are \(O(X/\sqrt b)\) true base targets. If a maximal matching has size below \(\epsilon K/(N_y+\sqrt b)\), its endpoints cover the successful labels. Cauchy–Schwarz with the row and column estimate bounds their total first-moment contribution by \(O(\sqrt\epsilon\,XK/b)\). For small \(\epsilon\), the remaining targets retain a constant fraction of the first moment. The second moment then gives \(\gg X/\sqrt b\) distinct targets with the claimed matching size.

For each genuine quotient witness, multiply by a Gaussian integer of norm \(C/5\), orient the result as \(u-iv\) with \(u\ge v\ge0\), and multiply by \(2+i\). The first coordinate squared is at least \(4(n-S)/5\), which puts its height key in \((S_3,U]\). This applies to the initial and alternative witnesses.

### Short exact control

This constructs one even balanced target, verifies \(S_0\) and two alternatives with distinct axes, and checks a nearby target with the same shared-divisor congruence but an actual \(S_0\) obstruction.

```python
a,b = 7864,5368
A,B = 3**a,5**b
assert 39*A < 40*B and 125*B < 122*A
S0,P,S3,U = A+25*B,A+125*B,729*A+B,729*A+625*B
lo = 2*S3-P

u,v,r,s = 1429620,1428400,17335,17051
assert 1+u*u == 3**20+v*v and 1+r*r == 5**10+s*s
L,M = 3**((a-20)//2),5**((b-8)//2)
n = (1+u*u)*L*L + (1+r*r)*M*M
assert lo < n <= U

xs = [(a,v*L),(a-20,u*L)]
ys = [(b+2,s*M),(b-8,r*M)]
for x,p in xs:
    for y,q in ys:
        S = 3**x+5**y
        assert n-S == p*p+q*q and (n-S)%5 == 0
        assert S3 < S+q*q <= U

bad = lo+1+(S0+15-lo-1)%45
assert lo < bad <= U and (bad-S0)%45 == 15  # exact v_3=1
print(n.bit_length(), [(a,b-8),(a-20,b+2)])
# 12475 [(7864, 5360), (7844, 5370)]
```

Plaksin's theorem, as printed on p. 145 of the original, is used for positive shift up to the interval's left endpoint and length between a fixed power \(x^{5/6+\varepsilon}\) and \(x\). Here the shift is \(<27X\), the left endpoint is above \(1300X\), and the length is a fixed positive proportion of \(X\) well below the endpoint. The norm-correlation factor contains 1. For Henriot, the polynomials are distinct monic linear forms, hence their product is primitive; choose the fixed exponent in the coefficient-size hypothesis less than \(1/3\). Only Corollary 2's upper bound is needed, which the erratum retains. In the shorter column direction, the bounded divisor expansions give at worst \(1+(\log b)^M/N_x\) after Hölder for a fixed \(M\). Multiplying by the number of ordered pairs yields an extra \(O(XK(\log b)^M/b^{3/2})\), absorbed by the diagonal. The exact finite control checks the arithmetic at a near-full-height pair, not membership in the inner counting grid.

```javascript

const ck=x=>{if(!x)throw Error("assert");};
const a=7864n,b=5368n,A=3n**a,B=5n**b;
ck(39n*A<40n*B&&125n*B<122n*A);
const S0=A+25n*B,P=A+125n*B,S3=729n*A+B,U=729n*A+625n*B,lo=2n*S3-P;
const [u,v,r,s]=[1429620n,1428400n,17335n,17051n],L=3n**((a-20n)/2n),M=5n**((b-8n)/2n);
ck(1n+u*u===3n**20n+v*v&&1n+r*r===5n**10n+s*s);
const n=(1n+u*u)*L*L+(1n+r*r)*M*M;
ck(lo<n&&n<=U);
for(const [x,p] of [[a,v*L],[a-20n,u*L]])for(const [y,q] of [[b+2n,s*M],[b-8n,r*M]]){
 const S=3n**x+5n**y;
 ck(n-S===p*p+q*q&&(n-S)%5n===0n&&S3<S+q*q&&S+q*q<=U);
}
const mod=(a,b)=>(a%b+b)%b;
const bad=lo+1n+mod(S0+15n-lo-1n,45n);
ck(lo<bad&&bad<=U&&mod(bad-S0,45n)===15n);
```
