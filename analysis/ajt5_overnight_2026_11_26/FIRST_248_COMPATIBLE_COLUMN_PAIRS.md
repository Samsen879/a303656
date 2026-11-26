# Any two fixed compatible-parity columns coexist at first root 248

Use the $M,P$ and seed class of FIRST_248_PRIMITIVE_SIEVE_SEED.md. The exact mod-16 separation in FIRST_248_PARITY_SEPARATION.md forbids any pair of columns with opposite parity of $k$ in $d=4+kP$. In the other direction, **every fixed distinct pair $d<e$ whose indices $k,l$ have the same parity does occur together with first root 248**, on at least $\gg_{M,d,e}\sqrt X/\sqrt{\log X}$ distinct positive $m\le X$ for sufficiently large $X$. This is a fixed-pair bound, without uniformity for growing indices.

Locally, a nonzero $z=2^v u$ with $u$ odd is a sum of two squares in $\mathbb Z_2$ if and only if $u\equiv1\bmod4$. Necessity follows by extracting a common factor of two and comparing the parities of the two coordinates. For sufficiency, an odd unit $1\bmod8$ is a 2-adic square; when it is $5\bmod8$, subtract $4$. Restore the factor $2^v$ by repeatedly applying $(a+b)^2+(a-b)^2=2(a^2+b^2)$. Thus, for stipulated valuations $v_i$ of $n-h_i$, the full local compatibility condition is just the simultaneous congruences $n\equiv h_i+2^{v_i}\bmod2^{v_i+2}$. Here the first norm forces $n\equiv2\bmod8$, each shift $H_d$ is $6\bmod8$, and each candidate column residual has exact valuation 2. Beyond mod 16, no additional 2-adic obstruction arises within one parity.

For a simultaneous integer construction, take the following fixed primitive vector $G=(a,b)$:

```text
a = 6811918216041124403700397103601028830525174978030000905528965990358259114044364962057597094745929327290959321080
b = 30388097967093902909201365319469695531860124853939056352648624771768668496132910360416344264549213326154248207397
```

Integer arithmetic verifies $\gcd(a,b)=1$, $G\equiv(0,1)\bmod4$, and $4\|G\|^2\equiv5150158917-626\bmod M$. Let $g=\|G\|^2$, $j=(5^e-5^d)/16$, $K=4M$, and $\eta=(-b,a)$. The chosen parity guarantees $j\in\mathbb Z$, and the fixed period gives $j\equiv0\bmod M$. Use CRT to choose $R\equiv-G\bmod M$, $R_2\equiv j-1\bmod4$, and $R_1$ of parity opposite to $R_2$. Then $G\cdot R+g\equiv j\bmod K$. Pick a Bézout vector $E$ with $G\cdot E=1$, and set
$$
 U_*=R+(j-G\cdot R-g)E,\quad U(t)=U_*+Kt\eta,\quad m(t)=5^e+1+4\|U(t)\|^2.
$$
The first and second parent norms are exactly $\|2U(t)\|^2$ and $\|2(U(t)+2G)\|^2$: their difference is $16j=5^e-5^d$. Multiplication by the norm 5 gives both designated child norms at $x=5m(t)+4$. The congruence $m(t)\equiv5150158917\bmod M$ follows from $U(t)\equiv-G\bmod M$ and $5^e\equiv5^4\bmod M$; the earlier-root negative certificates thus persist.

It remains to require that $F(t)=5m(t)-244=20\|U(t)\|^2+H_e$ itself be an actual square sum. This is a quadratic polynomial of positive leading coefficient, with
$$
 \operatorname{disc}(F)=-80K^2\big(20(G\cdot U_*)^2+gH_e\big).
$$
The bracket has exact valuation one at 2, because $g$ is odd and $H_e\equiv6\bmod8$. Since $v_2(K)=2$, the discriminant has valuation 9 and generates an imaginary quadratic field different from $\mathbb Q(i)$. The chosen opposite coordinate parities give $F(t)\equiv2\bmod8$ for all $t$. Apply [Friedlander–Iwaniec, Theorem 2](https://doi.org/10.1007/BF02545740) with quadratic form $y^2+z^2$ of fundamental discriminant $-4$, auxiliary integer 2 supported on its discriminant, and the local representative $(1,1)$ modulo 8 (its norm has gcd 2 with 8). This supplies $\gg_{M,d,e} T/\sqrt{\log T}$ genuine norms at positive parameters $t\le T$. The function $m(t)$ is eventually strictly increasing and quadratic in $t$, so taking $T$ a suitable fixed multiple of $\sqrt X$ proves the stated count. First root 248 then follows from its true norm and the preserved earlier-root obstructions. No assertion about uniformly many columns from each of two subfamilies follows from this fixed-pair argument.
