# Two marked medium inert factors in the even-seven comparison

The even-7 sector contains an unconditional, natural-scale loss from alternates with **exactly two medium inert primes**. After normalizing the two prime-anchor classes, their early sieve terms agree. The remaining signed term is a count with **at least two further inert factors**. Averaging the seven actual exponent phases does not turn that term into a complete progression average. The sign of the distinct-pair comparison remains open.

### The marked loss

Write \(A=3^a,\ B=5^b\), with \(a,b\) even and \(39/40<B/A<122/125\). Use the original labels
\[
S_0=A+25B,\qquad S=3^c+5^e,\qquad \kappa=(S_0-S)/45,
\]
where \(a/10\le c\le a/3,\ b/5\le e\le b/3,\ c\equiv a\pmod4,\ e\equiv b+2\pmod6\). Retain the seven deep phases \(S\equiv r_-=3^{a+4}+5^{b+2}+7\pmod{49}\). A prime anchor is \(n=S_0+45p\), with \(p\equiv1\pmod4\) prime and
\[
1457A-123B<n\le729A+625B.
\]
In the \(w=1\) class require \(n\equiv0\pmod{49}\). In the \(w=49\) class require \(v_7(p+\kappa)=2\), which gives \(n\equiv r_-\pmod{49}\). In both classes \(x_w=(p+\kappa)/w\) is a \(7\)-adic unit and \(x_w\equiv1\pmod4\). The prime progression densities are \(\alpha_1=1/84\) and \(\alpha_{49}=1/98\). The second density includes all six reduced lifts at modulus \(4\cdot343\).

Fix a sufficiently small constant \(\rho>0\). Let \(T_{\ell,w}\) count prime anchors for label \(\ell=(c,e)\) with
\[
x_w=qrm,\qquad
B^\rho<q\le B^{2\rho}<r\le B^{3\rho},
\]
where \(q,r\equiv3\pmod4\) are prime and every prime factor of \(m\) is \(1\bmod4\). Each anchor is counted once for its label. Both valuations are exactly one, so these are genuine failures of the alternate sum-of-two-squares condition. Put
\[
M_\ell=\frac{B}{(\log B)^{3/2}}
\prod_{\substack{t\mid\kappa\\t\ {\rm prime},\ t\equiv3\ (4)}}
\frac{t-1}{t-2}.
\]
Uniformly over the retained labels and both classes, for sufficiently large \(B\) depending on \(\rho\),
\[
c\sqrt{\rho}\,\frac{M_\ell}{w}\ \le\ T_{\ell,w}\ \le\ C\,\frac{M_\ell}{w}
\]
with absolute positive constants \(c,C\).

To prove this, let \(R_{\ell,w}(z)\) impose that \(m\) has no inert prime through \(z\), and take \(z_*=B^{1/2-12\rho}\). For each \(q,r\), Bombieri–Vinogradov gives the remaining divisor level \(D=B^{1/2-5\rho}(\log B)^{-C_0}\). The full modulus includes the class modulus, \(qr\), and the sieve divisor. At the marked primes the additional divisibility costs \(1/q\) or \(1/r\), since it imposes a second power. Other inert primes outside \(7\kappa\) cost \(1/(t-1)\). The number of times a modulus is used is bounded in terms of \(\rho\), since both marked primes exceed \(B^\rho\). The two prime harmonic sums tend to \(\tfrac12\log 2\) and \(\tfrac12\log(3/2)\). The half-dimensional lower sieve has \(s=\log D/\log z_*=1+\Theta(\rho)\) and \(f_{1/2}(s)\asymp\sqrt{s-1}\). Its upper sieve is bounded at this \(s\). [Nath and Xie, §5](https://arxiv.org/html/2501.16723v1#S5).

Any \(m\) surviving \(z_*\) that still has an inert factor has exactly two, counting multiplicity. This follows from \(m\equiv1\pmod4\) and \(z_*^3\gg B\). A repeated factor costs \(O(B/z_*+\sqrt B)\) by counting square divisors of \(x_w\). For distinct factors, write \(m=h\,t_1t_2\) with \(h\) split-supported. Apply the two-linear-form upper sieve in \(t_2\) to \(t_2\) and \(wqrht_1t_2-\kappa\). The harmonic sum over \(t_1\) costs \(O(\rho)\), and \(h\ll B^{24\rho}\) gives a split harmonic cost \(O(\sqrt{\rho\log B})\). At a split prime \(t\nmid\kappa\) the latter Euler factor is \(1+1/(t-2)\). At \(t\mid\kappa\) the cofactor \(h\) must omit \(t\), which cancels the corresponding split singular factor. Thus \(R_{\ell,w}(z_*)-T_{\ell,w}\ll \rho^{3/2}M_\ell/w+o_\rho(M_\ell)\). This loss is smaller than the lower main term for small fixed \(\rho\).

### The signed estimate that is still needed

Set \(y=B^{4\rho}\) and \(K_{\ell,w}=R_{\ell,w}(y)-R_{\ell,w}(z_*)\). At \(y\), the local densities after division by \(\alpha_w\) are the same for both classes. The same divisor level gives \(s\asymp1/\rho\), so the fundamental lemma bounds the relative sieve error by \(O(s^{-s/2})\). Together with the terminal estimate above, this gives
\[
\boxed{\displaystyle
\Delta T=-\Delta K+O\!\left(\rho^{3/2}\sum_\ell M_\ell\right)
              +o_\rho\!\left(\sum_\ell M_\ell\right),\qquad
\Delta X=\sum_\ell\left(\frac{X_{\ell,1}}{\alpha_1}
                       -\frac{X_{\ell,49}}{\alpha_{49}}\right).}
\]
Outside \(O(B/y+\sqrt B)\) square-divisor exceptions per label, \(K\) has at least two additional distinct inert factors, with the least in \((y,z_*]\). This is a specific switched comparison of \(qrtv-\kappa\) and \(49qrtv-\kappa\), with \(t\) the least additional inert prime and \(v\) free of inert primes below \(t\). A signed estimate for that remainder with a margin larger than the displayed error settles the sign of this marked component. It would still leave the other medium-loss components in the original comparison. [Kurlberg, Lester and Rosenzweig, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136).

There is an exact obstruction to using the label average as complete residue averaging. The \(J\asymp(\log B)^2\) shifts are distinct for large \(B\). Indeed, equality for two labels with \(c<c'\) and \(e>e'\) would give \(c=v_3(5^{e-e'}-1)=1+v_3(e-e')\), contradicting \(c\ge a/10\). Each nonzero shift difference is \(O(B^{1/3})\), so it contains only \(O_\rho(1)\) prime divisors exceeding \(B^\rho\). Consequently, outside \(O_\rho(J^2)\) moduli \(qr\), all the shift residues are distinct and occupy just \(J/(qr)\) of the classes. Their empirical distribution has total variation distance \(1-J/(qr)\) from uniform. This rules out the complete-residue shortcut. A signed prime estimate adapted to these sparse residues could still give cancellation.

### Exact same-label controls

For \((a,b,c,e)=(712,486,80,122)\), the replay certifies four 1134-bit prime anchors in the sharp window. Each class has a true alternate and an alternate with its only odd inert valuations at \(59\) and \(67\). Both depth-two controls use the same lift \(p+\kappa\equiv49\pmod{343}\). The finite band check uses \(\rho=1/375\).

The primality check is elementary. For \(Q=2^{378}\), the modular witness forces every prime divisor of \(p\) to be \(1\bmod Q\). If \(p<Q^3\) were composite, writing \(p=(1+Qu)(1+Qv)\) would give \(uv<Q\) and \(u+v<Q\), directly by expanding the product and using \(u,v\ge1\) (when \(u+v\ge Q\), \(uv\ge Q-1\) already forces \(p>Q^3\)). The two base-\(Q\) digits of \((p-1)/Q\) would then be \(uv,u+v\), whose discriminant must be a square.

```python
from math import gcd, isqrt

A, B = 3**712, 5**486
S0, S = A + 25*B, 3**80 + 5**122
k, rem = divmod(S0-S, 45)
L = (1457*A-123*B-S0)//45 + 1
U = (729*A+625*B-S0)//45
r = (pow(3,716,49) + pow(5,488,49) + 7) % 49
Q = 1 << 378
assert 39*A < 40*B and 125*B < 122*A and S % 49 == r == 27
assert rem == k % 8 == 0 and B < 59**375 < B**2 < 67**375 < B**3
assert all(t % 4 == 3 and all(t%d for d in range(2,isqrt(t)+1))
           for t in (59,67))

for w,F,j,s in [(1,1,1088,5), (1,3953,429,5),
                (49,1,88,5), (49,3953,952,13)]:
    G = w*F
    f = 4*((isqrt((L+k)//G)+4)//4+j)
    h, rem = divmod(((k+1+Q)*pow(G,-1,2*Q)-f*f-1) % (2*Q), 8)
    assert rem == 0
    v = h % 2
    for i in range(2,377):
        v += ((h-2*v*v-v) % (1<<i))
    x = 1+4*v
    mod = 49 if w == 1 else 7
    want = -S*pow(45*F,-1,49) if w == 1 else pow(F,-1,7)
    z = next(t for t in range(mod) if (t*t+f*f-want)%mod == 0)
    x += Q*((z-x)*pow(Q,-1,mod)%mod)
    m = x*x+f*f
    p = G*m-k
    a0,b0 = divmod((p-1)//Q,Q)
    disc = b0*b0-4*a0
    assert L <= p <= U < Q**3 and p%Q == 1 and ((p-1)//Q)%2
    assert pow(s,(p-1)//2,p) == p-1 and (disc < 0 or isqrt(disc)**2 != disc)
    assert gcd(x,f) == gcd(m,7*59*67) == 1 and m%2 == 1
    assert (S0+45*p)%49 == (0 if w == 1 else r)
    assert ((p+k)%7 != 0) if w == 1 else ((p+k)%343 == 49)
    print(w, F, p.bit_length(), (p+k)%343)
```

The cofactor \(m\) is an odd primitive sum of two squares, so it has no inert prime divisor. Thus \(F=1\) certifies true alternates and \(F=3953=59\cdot67\) certifies the two exact odd valuations.
