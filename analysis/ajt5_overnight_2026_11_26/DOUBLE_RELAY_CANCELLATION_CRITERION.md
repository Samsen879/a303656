# Higher-order cancellation for two ordinary relay digits

**The higher-order bound transfers to a reader that sees both axes of two ordinary relays.** The condition is that two of the reader’s three terms have the same dependence on the moving relay digits. Those two terms can be factored together even when their spare-phase characters differ. I verified this on the actual \(3,5\) graph \(3\to\{7,79\}\to3319\), with a direct \(3\to3319\) read. Changing the repair slopes at the same target gives an actual control where the factorization fails. [Pinned higher-order argument](https://github.com/Samsen879/a303656/blob/ac9c768797937e6455c6149d0f4f36a8287ee758/analysis/ajt5_overnight_2026_11_26/HIGHER_ORDER_READER_ESCAPE.md)

### Exact cancellation criterion

Write the nonzero-observation hit equation as \(T_0+T_1+T_2=0\), where \(T_0=-N\) and each term has the form
\[
T_i(j)=A_i\chi_i(j)\prod_\ell G_\ell^{a_{i\ell}C_\ell w_\ell^j}.
\]
Here \(j\in\mathbb Z/h\), \(G_\ell\) has order \(p_\ell\) in the reader field, and \(w_\ell\) has order \(h\) modulo the distinct relay prime \(p_\ell\). The constants \(C_\ell\) are nonzero. This describes first digits on common-scaling repair rays. The exact even lifts must be invisible to the reader.

Suppose two terms, numbered 1 and 2 after relabelling, have equal vectors \((a_{i\ell})_\ell\). Divide by \(T_1\) and set
\[
Z(j)=\frac{A_2}{A_1}(\chi_2/\chi_1)(j),\qquad
\rho=\chi_2/\chi_1,\qquad \eta=\chi_0/\chi_1.
\]
For offsets \(t_i\) and integers \(e_i\) with \(\sum e_i=0\), the remaining digit factors cancel **exactly when**
\[
\sum_i e_iw_\ell^{t_i}=0\pmod{p_\ell}
\quad\text{for each }\ell\text{ with }a_{0\ell}\ne a_{1\ell}.
\]
The orders \(p_\ell\) are coprime, so cancellation at one relay cannot compensate for failure at another. A simultaneous hit then implies
\[
\prod_i(1+\rho(t_i)Z)^{e_i}=\eta\!\left(\sum_i e_it_i\right).
\]
The rational function on the left is nonconstant exactly when some group of offsets with equal \(\rho(t_i)\) has nonzero total exponent. This follows from the multiplicity at \(-1/\rho(t_i)\). In particular, a moving \(\rho\) of prime order \(h\) and distinct offsets make every nonzero relation usable. Clearing denominators gives a nonzero polynomial of degree at most \(\sum_{e_i>0}e_i\).

For \(s\) offsets, let \(P\) be the product of the relay primes in the cancellation test. The same pigeonhole proof as in the pinned argument, now over the product of the residue fields, gives degree at most \((s-1)\lfloor P^{1/(s-1)}\rfloor\). The translated-subset count therefore gives a sublinear hit bound for a fixed number of readers when \(\log P=o((\log h)^2)\). This is a uniform estimate for graphs satisfying the stated conditions.

**Where the method stops.** If all three digit vectors differ, every choice of a pair leaves a Laurent binomial \(1+cZ^bX^{\mathbf v}\) with \(\mathbf v\ne0\), where the \(X\)’s are formal digit variables. At any nonzero \(Z=z_0\), this binomial has order zero along the divisor \(Z=z_0\). Products and quotients preserve that fact. Thus if such a product eliminates the \(X\)’s formally, its remaining rational function of \(Z\) is a monomial. For a fixed oriented pair and a zero-sum relation, that monomial is constant. This is a no-go for the binomial-product proof. Special identities on the finite, coupled orbit remain possible.

### Actual controls and replay

In the two-relay example, slopes \((2,70)\) align both relay factors at \(3319\). The slow ratio has order 3. The relation \((1,23,-24)\) cancels both relay factors, and its degree-24 polynomial has no roots on the three actual slow values. At the same \(n\), slopes \((3,71)\) keep both relay valuations exactly two and make all three digit vectors distinct. The replay also checks a degree-3 example on \(7\to43\to3011\), where **both** direct spare characters move. The example reuses the actual primes from the earlier nested graph. [Nested relay control](https://github.com/Samsen879/a303656/blob/9f2a7f96a3203534da04365d588c7cfa091b90ca/analysis/ajt5_overnight_2026_11_26/NESTED_TRIANGULAR_RELAY_AVOIDANCE.md)

```python
from math import isqrt, lcm, prod

def check(h, P, r, n, C, D, slopes, e, expected):
    H = lcm(*(p*p*(p-1) for p in P), r*(r-1))

    def step(m):
        b = H//m
        return b*pow(b, -1, m)

    J, U = step(h), [step(p*p) for p in P]
    assert all(all(z%i for i in range(2, isqrt(z)+1)) for z in (h,*P,r))
    assert all(z%4 == 3 and all(pow(a,z-1,z*z) != 1 for a in (3,5))
               for z in (*P,r))
    A,B,alpha,beta = pow(3,C,r),pow(5,D,r),pow(3,J,r),pow(5,2*J,r)
    rho = beta*pow(alpha,-1,r)%r
    if h==7: assert alpha != 1 and beta != 1
    assert n%r and rho != 1 and pow(alpha,h,r) == pow(beta,h,r) == 1
    w = [pow(3,-J,p) for p in P]
    assert all(x != 1 and pow(x,h,p) == 1 for p,x in zip(P,w))
    assert sum(e) == 0
    assert all(sum(a*pow(x,i,p) for i,a in enumerate(e))%p == 0
               for p,x in zip(P,w))

    for k,rays in enumerate((slopes, tuple(b+1 for b in slopes))):
        hits,base_digits = [],[]
        for j in range(h):
            c,d = C+J*j,D+2*J*j
            def rem(m):
                return (n-pow(3,c,m)-pow(5,d,m))%m
            for i,(p,u,b,x) in enumerate(zip(P,U,rays,w)):
                assert rem(p*p) == p
                g,s = pow(3,u,r),pow(5,b*u,r)
                assert g != 1 and s != 1 and pow(g,p,r) == pow(s,p,r) == 1
                assert (g == s) == (k == 0)
                a3,a5 = ((pow(a,u,p*p)-1)//p for a in (3,5))
                f = pow((a3*pow(3,c,p)+b*a5*pow(5,d,p))%p,-1,p)
                if j == 0:
                    base_digits.append(f)
                assert f == base_digits[i]*pow(x,j,p)%p
                c,d = c+u*f,d+u*b*f
                if rem(p**3) == 0:
                    c += p*u
            assert all(rem(p**3) in range(p*p,p**3,p*p) for p in P)
            assert rem(3) == rem(4) == 1 and rem(h)
            if rem(r) == 0:
                assert rem(r*r) == r
                hits.append(j)
        assert hits == (expected if k == 0 else [])

    coeff = pow(alpha,-sum(i*a for i,a in enumerate(e)),r)
    for j in range(h):
        Z = B*pow(A,-1,r)*pow(rho,j,r)%r
        factors = [1+Z*pow(rho,i,r) for i in range(len(e))]
        lhs = prod(pow(z,a,r) for z,a in zip(factors,e) if a > 0)
        rhs = coeff*prod(pow(z,-a,r) for z,a in zip(factors,e) if a < 0)
        assert (lhs-rhs)%r

check(3,(7,79),3319,16548479088281,214742619,79168445538,
      (2,70),(1,23,-24),[1])
check(7,(43,),3011,92767221879,1169141190,2718933,
      (25,),(-2,-1,2,1),[0])
print('OK')
```

A sufficiently large multiple of \(12hr^2\prod_\ell p_\ell^3\) added to each target makes every remainder positive simultaneously and preserves the exact tests. Zero observations instead give a two-term character quotient. The certificates concern the tested finite panels, so a full square-sum witness still requires controlling the other inert primes.

The scope of the formal no-go is the use of products or quotients of translated Laurent binomials with the same oriented pair and a zero-sum offset relation. It does not preclude specialized elimination on the finite orbit. In the case of several readers satisfying the factorization, their relations can be chosen separately for each reader before applying the union bound.
