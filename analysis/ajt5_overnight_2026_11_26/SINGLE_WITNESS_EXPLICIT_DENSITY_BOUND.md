# Explicit coverage: more than 98.4% in lower density

The upper density of integers without a representation \(a^2+b^2+3^c+5^d\) with nonnegative exponents is less than \(0.016\). In fact the *limiting miss density in the two-growth-axis box* of [the finite-obstruction theorem](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md) is at most the rational upper bound reproduced below (approximately \(0.015812126768\)). This number is an asymptotic bound on an exceptional set; it is neither a density-one theorem nor a pointwise proof.

The calculation uses the published [Dorais–Klyve search, §§4.1, 5, Table 2, and Table 5](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf) as a finite input. Their base-3 search covers through \(150000\cdot6469693230=970453984500000\); the solutions \(11,1006003\) both fail the base-5 test, whose explicit residues are replayed below. Use the smaller cutoff \(B=9\cdot10^{14}\). There is no assumption on the distribution of simultaneous Wieferich primes beyond that range.

## A finite-depth probability with one reset axis

Write \(E_q\) for first blocking at inert \(q\), \(\lambda_q=\min_{b=3,5} v_q(b^{q-1}-1)\). After all earlier observations, a fixed old survivor can vary its \(q\)-primary digits to make any residue of valuation at least \(\lambda_q\) good. Thus the conditional chance of first blocking is at most the Haar probability of an odd valuation less than \(\lambda_q\),
\[
 \beta_q=(1-q^{-2\lfloor\lambda_q/2\rfloor})/(q+1).
\]
The head \(2,3,5\) never blocks. A prime with \(\lambda_q=1\) cannot block, so it suffices to sum over \(q>B\).

Take any odd prime power \(D=r^a\mid\operatorname{ord}_q(b)\) on either axis \(b=3,5\). Let \(\mathcal D\) be the earlier inert primes \(p\ne r\) where \(D\mid\operatorname{ord}_p(b)\), only where \(b\) is a unit, and put \(S=\sum_{p\in\mathcal D}(p+1)^{-1}\). Remove these tests and the test at \(r\), retaining the other older observations. A reset adds \(jr^{a-1}\), \(0\le j<r\), on the \(r\)-primary coordinate of the chosen axis. No dropped-row observations are used in selecting the base phase except at \(r\). The \(r\) variants retain all kept tests, and give distinct shifts at \(q\) and at each \(p\in\mathcal D\).

If \(r\) is split or the changing power is zero there in the growth limit, its test need not be charged: in the latter case reinsert the unchanged \(r\)-test before selecting the phase. Otherwise put \(d=a-1+v_r(b^{r-1}-1)\). Any phase that gives even valuation less than \(d\) at \(r\) is robust under the reset, by lifting the exponent. Given the kept observations, let \(V\) be the base-phase shift set modulo \(r^d\). If there is no robust choice but some survivor remains after reinserting \(r\), \(n_r\bmod r^d\) lies in \(V\). Distinct exceptional residues must differ at an odd valuation: otherwise the shift represented by one would give a robust choice for the other. Their digit tree branches only at odd levels, with at most \(r^{\lfloor d/2\rfloor}\) residues. Thus the unconditional exception cost given the kept tests is \(\eta_r\le r^{-\lceil a/2\rceil}\) for inert \(r\), zero for split \(r\).

In the robust case a dropped \(p\)-row can remove at most one of the variants. The Haar chance it removes any is \(r/(p+1)\); the rows are independent after selecting the base phase. For first blocking, at least \(r-1\) of the variants must be removed by the earlier rows, since two survivors give two distinct terminal shift residues. Markov, and separately summing products over \((r-1)\)-element subsets of rows, give
\[
 \Pr(E_q)\le\beta_q\left[\eta_r+
 \min\left(1,\frac r{r-1}S,\frac{(rS)^{r-1}}{(r-1)!}\right)\right].
\]
The factor \(\beta_q\) is a bound after the actual earlier observations, so it multiplies either earlier-event cost. Phase selection can be made measurably via nested cylinders of the compact survivor set; the robust condition itself is clopen for fixed \(n_r\bmod r^d\).

## Infinite summation with explicit constants

In each \([Y,2Y)\) with \(Y\ge B\), let \(T=\lfloor(4/5)\log Y\rfloor\). When all order prime powers on both axes are \(\le T\), \(q\mid3^L-1\) for \(L=\operatorname{lcm}(1,\ldots,T)\). Using [Rosser–Schoenfeld, Theorem 12](https://doi.org/10.1215/ijm/1255631807), \(L\le Y^{104/125}\). Counting prime divisors and summing the dyadic bound gives \(\log(3)B^{-21/125}/[\log B(1-2^{-21/125})]\).

Otherwise choose an order prime power \(D>T\). It is odd since \(v_2(q-1)=1\); moreover \(D\ge28\), \(D>(3/4)\log q\) and \(q\equiv1\bmod D\). Old rows counted in \(S\) and terminal \(q\) both lie in the unique class \(1\bmod D,\ 3\bmod4\). Let \(H_D(x)\) be its reciprocal-prime sum through \(x\). Through \(128D\) sum the candidates \((4j+2)D+1\), \(0\le j<32\), giving \(A/D\) with \(A=\sum(4j+2)^{-1}\). Above that threshold [Montgomery–Vaughan Brun–Titchmarsh](https://doi.org/10.1112/S0025579300004708) and partial summation add at most \((1/L_x+\log L_x-\log\log32)/\varphi(D)\), \(L_x=\log(x/4D)\). The function \(1/u+\log u\) is increasing for \(u>1\). Since \(A-\log\log32+1/34<1/5\), this gives \(H_D(x)\le(\log\log x+1/5)/\varphi(D)\) for \(\log x\ge34\) (the short range uses \(A<\log34\)). Thus \(S\le S_D=(\log D+1/2)/\varphi(D)\); the terminal reciprocal sum \(R_D\) on \(B<q\le e^{4D/3}\) also satisfies \(R_D\le S_D\). When \(V_0=34-\log(4D)>0\), directly summing from \(B\) gives \(R_D\le(1/U+\log(U/V_0))/\varphi(D)\), \(U=4D/3-\log(4D)\). Both upper endpoints include the positive \(1/U\)-type term.

Use \(\beta_q\le1/q\) and sum the reset bound with \(S_D,R_D\) over all \(D\). One bound suffices per \(D\) even if it is present on both axes; counting a given \(q\) again under another \(D\) only increases the bound. For \(r\ge29\) the factorial term is at most \(2^{1-r}\), from \((r-1)!\ge((r-1)/e)^{r-1}\), \(D\ge r\), \(e<3\) and the monotone endpoint test in the script. Each \(r\) contributes at most 13 finite powers, giving \(13/2^{27}\) for the finite part's \(r\ge29\) kill cost. Beyond the prime cutoff \(P=10^5\), bound the \(D=r\) terms by \((1+1/r)(\log r+1/2)/[r(r-1)]\) and integrate the decreasing all-integer upper bound, using \((r+1)/(r-1)\le10001/10000\). Beyond \(H=10^6\) for higher powers \(D\), both the depth cost and the Markov cost are at most \(D^{-1/2}\); each summand is at most \(3(\log D+1/2)D^{-3/2}\). Each dyadic interval \([Y,2Y]\) has at most \(3\sqrt{2Y}\) perfect powers, by counting squares and powers of exponent at least 3. Apply this with \(Y=2^jH\) and sum the geometric series and its first moment. The full finite calculation and both analytic tails are rounded upwards below. This establishes the quoted bound over all first blocking primes, and the box-miss theorem transfers it to ordinary integers.

~~~python
from fractions import Fraction as Q
from math import ceil, factorial, floor, isqrt, prod

B, P, H, W = 9*10**14, 10**5, 10**6, 10**11

def series(y):
    z = (y-1)/(y+1)
    x = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return x, x+2*z**25/(25*(1-z*z))

L2, U2 = series(Q(2))

def log_bounds(x):
    y = Q(x)
    assert y >= 1
    k = 0
    while y >= 2:
        y /= 2
        k += 1
    lo, hi = series(y)
    return Q(floor(W*(lo+k*L2)),W), Q(ceil(W*(hi+k*U2)),W)

def lower(x): return log_bounds(x)[0]
def upper(x): return log_bounds(x)[1]
def exp_lower(x,n): return sum(x**j/factorial(j) for j in range(n))
def round_up(x): return Q(ceil(W*x),W)

assert 150000*prod((2,3,5,7,11,13,17,19,23,29)) == 970453984500000 > B
assert lower(B) > 34
for p,residue in [(11,78),(1006003,31695130519)]:
    assert pow(3,p-1,p*p)==1 and pow(5,p-1,p*p)==residue!=1
for n in range(216):
    m,u = (4,1) if n%2 else (8,2)
    assert any((n-pow(3,c,m)-pow(5,d,m))%m==u
               and ((n-pow(5,d,27))%3!=0 or
                    (n-pow(5,d,27))%27 in (9,18))
               for c in (3,4) for d in range(1,19))

A = sum(Q(1,4*j+2) for j in range(32))
assert A < lower(34)
assert A-lower(lower(32))+Q(1,34) < Q(1,5)
assert upper(Q(4,3)) < Q(3,10)
assert Q(3,2)*(upper(28)+Q(1,2))/28 < 1
assert 3*Q(29,28)**2*(upper(29)+Q(1,2))/29 < Q(1,2)

def bounds(D,r):
    phi = D-D//r
    l,u = log_bounds(4*D)
    Um, Up, Vm = Q(4*D,3)-u, Q(4*D,3)-l, 34-u
    assert 0 < Vm < Um
    S = (upper(D)+Q(1,2))/phi
    R = min(S,(1/Um+upper(Up/Vm))/phi)
    return S,R

flags = bytearray(b'\x01')*(P+1)
flags[:2] = b'\x00\x00'
for r in range(2,isqrt(P)+1):
    if flags[r]:
        flags[r*r::r] = b'\x00'*((P-r*r)//r+1)

primes = powers = Q(0)
for r in range(3,P+1,2):
    if not flags[r]:
        continue
    if r>=29 and r%4==3:
        primes += round_up(bounds(r,r)[1]/r)
    D,a = r*r,2
    while D<=H:
        if D>=28:
            S,R = bounds(D,r)
            eta = Q(1,r**((a+1)//2)) if r%4==3 else Q(0)
            G = min(Q(1),(r*S)**(r-1)/factorial(r-1)) if r<29 else Q(0)
            powers += round_up(R*(eta+G))
        D,a = D*r,a+1

gamma = Q(21,125)
low = upper(3)/(34*exp_lower(34*gamma,32)*(1-1/exp_lower(gamma*L2,12)))
assert 3**13>H and 2**28>=29**2
kill = Q(13,2**27)

assert Q(P+1,P-1)<Q(10001,10000)
prime_tail = Q(10001,10000)*(upper(P)+Q(3,2))/P
assert Q(9,4)*(upper(H)+Q(1,2))<isqrt(H)
assert lower(2*H)>6 and 11**6<2*H<2**21
power_tail = Q(27,2)/H*(2*(upper(2*H)+Q(1,2))+2*U2)

parts = (low,primes,powers,kill,prime_tail,power_tail)
assert all(x < Q(y,10**8) for x,y in zip(parts,
    (97200,436127,992486,10,13015,42395)))
assert sum(parts)<Q(15813,10**6)<Q(16,1000)
print(*(f"{float(x):.12f}" for x in parts))
print(f"Total upper bound: {float(sum(parts)):.12f}")

~~~
