# Rigidity and exact cost of unweighted relative-trace matching

Equating the **sum** of the short and long relative traces already forces both composing elements into \(\mathbb Q(\sqrt{15})\). This gives an exact norm penalty and rules out every bounded-inflation implementation of this trace condition at ordinary height. The trace condition can pass even when the actual integer edge sums differ.

### Trace rigidity and exact cost

Let \(F=\mathbb Q(\sqrt{-3},\sqrt{-5})\), \(K_j=\mathbb Q(\sqrt{-j})\), and \(T_j(\alpha)=\operatorname{Tr}_{K_j/\mathbb Q}N_{F/K_j}(\alpha)\). Write \(\alpha=a+b\sqrt{-3}+c\sqrt{-5}+d\sqrt{15}\). Direct expansion gives
\[
T_3(\alpha)-T_5(\alpha)=4(5c^2-3b^2).
\]
Thus the unweighted condition
\[
T_3(\alpha_s)+T_3(\alpha_l)=T_5(\alpha_s)+T_5(\alpha_l)
\]
implies \(3(b_s^2+b_l^2)=5(c_s^2+c_l^2)\). A nonzero sum of two rational squares has even \(3\)-adic valuation. The two sides would therefore have opposite parity of valuation. All four coefficients vanish, and both composing elements are real. This argument allows cancellation between the short and long traces from the outset.

For either pair, let \(D,C\) be its two coprime oriented norms after removing the primes above \(30\). Let \(M=\lambda DC\), with \(\lambda\) the product of the odd-depth primes inert in the opposite quadratic field. For a real composing element, both relative norms equal the scalar \(m=N_{\mathbb Q(\sqrt{15})/\mathbb Q}(\alpha)\). Carrying the oriented ideals requires \(DC\mid m\), and the inert valuations require \(M\mid m\). The quartic norm is \(m^2\). [Prior composition theorem](https://github.com/Samsen879/a303656/commit/12c82eab0c24479909fc041be7c2a3478f3236ff)

The exact minima under the trace condition are
\[
\begin{array}{c|cc}
 & (M/5)=1 & (M/5)=-1\\ \hline
\text{No sign requirement} & M^2 & 4M^2\\
\text{Positive relative trace on each element} & M^2 & 9M^2 .
\end{array}
\]
Indeed, the Minkowski bound for \(\mathbb Q(\sqrt{15})\) is \(\sqrt{60}/2<4\). The ramified ideals of norms \(2,3\) have the same class by \(N(3+\sqrt{15})=-6\). That class is nontrivial since neither \(2\) nor \(-2\) is a square modulo \(5\). The class of an ideal of norm \(M\) is consequently detected by \((M/5)\): a generator in the trivial class has norm \(\pm M\), and multiplying an ideal in the other class by the prime above \(2\) gives a generator of norm \(\pm2M\). Also \(M\equiv1\bmod3\), since its odd-depth primes split in both imaginary fields. Hence \(M\) has positive sign when principal, while \(2M\) can occur only with negative sign. Multiplying in the nontrivial case by the prime above \(3\) gives absolute norm \(3M\), with positive sign forced by \((x^2-15y^2)/3\equiv y^2\bmod3\). [Minkowski bound](https://www.jmilne.org/math/CourseNotes/ANT.pdf)

### Consequences for the pinned edges

At ordinary height both factor pairs have entries \(\asymp\sqrt A\). Removing \(2,3,5\) costs bounded factors, so \(DC\asymp A\) for each composition. The trace condition forces a quartic norm of at least \((DC)^2\), hence **an inflation factor \(\gg A\)** relative to \(DC\) on each pair. It also makes the two traces agree *term by term*. A literal decoding of their halves as \(v,z\) on the short pair and \(u,w\) on the long pair would give \(v=z,\ u=w\), impossible for \(d\ne e\).

There is also an actual cofinal control on the checked phase with \(q=126736826507\) and \(v_q(e)=3\). Take the true divisors \(v=H,\ z=q^3\). Positive trace compositions exist at the stated minima, and the short composition alone costs a multiplier \(\gg H\). Yet \(v+d/v\asymp A^{1-\mu}\) and \(z+e/z\asymp A\), where \(\mu=28088000/56717661\). The sums differ for all sufficiently large members. This unbounded cost comes from imposing the trace condition. It does not establish an unbounded multiplier for unconstrained composition.

### Runnable \(3,5\) control

For \(A=3^6,\ B=5^4\), the true pairs are \((24,3967)\) and \((35,863)\). Both positive trace minima are attained below, while the edge sums differ.

```python
def traces(a, b, c, d):
    return (2*(a*a-3*b*b+5*c*c-15*d*d),
            2*(a*a+3*b*b-5*c*c-15*d*d))

A, B = 3**6, 5**4
v, u, z, w = 24, 3967, 35, 863
assert v*u == 2*(A+75*B)
assert z*w == 20*A+25*B
assert pow(-3,(w-1)//2,w) == w-1

Ms, Ml = 7, u*w*w
assert Ms % 3 == Ml % 3 == 1
assert Ms % 5 == 2 and Ml % 5 == 3
assert traces(6,0,0,1) == (6*Ms,6*Ms)
assert traces(171*w,0,0,34*w) == (6*Ml,6*Ml)
assert (v+u, z+w) == (3991,898)

K = A+25*B+(z+w)**2
assert K == 822758
assert K-81*A-125*B == (w-z)**2
assert 652**2 < K-9*A-625*B < 653**2
p = traces(10,1,3,0)
q = traces(10,2,1,0)
assert min(*p,*q)>0 and p[0]-p[1]+6*(q[0]-q[1])==0
```

Rigidity is specific to the unweighted condition: take the integral short and long elements with coordinate tuples (10,1,3,0) and (10,2,1,0), respectively. Their trace differences add to zero with weights 1 and 6 and both elements are nonreal, although all four traces are positive. I found no matched integer height in this branch. For a prescribed \(n\), the shared-coordinate construction still needs exact equal edge sums at a common \(K\), followed by \(n-K=t^2\) for an integer \(t\). Trace composition alone supplies neither condition.

For the real-field norm minimum, split primes allow any required depth by choosing an ideal on either branch; primes inert in the real field have even degree and require the rounding already encoded by the factor λ. Scalar relative norms then carry either imaginary orientation at that underlying prime. A norm −1 unit would contradict reduction modulo 3, so changing generator within its ideal class cannot undo the required sign. This argument is scoped to the prime-to-30 oriented factors and the unweighted trace condition.
