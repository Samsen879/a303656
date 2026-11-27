# Exact-order charging gives representation density above 99.999783317%

The exception-density upper bound drops from **0.000863195841% to below 0.000216683%**, a 74.9% reduction at the same cutoff \(B=9\cdot10^{14}\). The low-order charge falls by a factor of about 73. The bound applies to misses in the two-growth-axis box and hence to all-exponent exceptions. The pointwise conjecture remains open. [Pinned ranked envelope](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_RANKED_TERMINAL_DENSITY_BOUND.md) · [All-exponent density theorem](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/EXACT_DENSITY_ALL_EXPONENTS.md)

The main saving comes from **charging each exact order once across the finite dyadic range**. The simultaneous base-3/base-5 gcd deletes all 695 charged exact-order classes with \(d\le8192\), saving a further \(4.46\cdot10^{-12}\) in density units. The replay enumerates orders and computes gcds. The published prime search is inherited through the same cutoff. [Published search, §§4.1 and 5](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

| Charge, in density units | Previous | Revised |
|---|---:|---:|
| Low-order finite part | \(4.853312241994\cdot10^{-6}\) | \(8.913313083030\cdot10^{-8}\) |
| Low-order analytic tail | \(1.701434700494\cdot10^{-6}\) | \(4.777152461590\cdot10^{-10}\) |
| All other charges and inherited slack | \(2.077211457835\cdot10^{-6}\) | same |
| **Total** | **\(8.631958400323\cdot10^{-6}\)** | **\(2.166822303911\cdot10^{-6}\)** |

The retained subtotal consists of \(125047/10^{11}\) in finite high-order charges, \(8953/10^{11}\) in the two other tails, \(14/2^{27}\) in the large-source reader allowance, and \(6.329033294780848\ldots\cdot10^{-7}\) in inherited slack. The replay subtracts the original low-order rational directly. [Original low-order calculation](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md)

### Exact-order bound

Write \(Y_j=B2^j\) and \(T_j=\lfloor(4/5)\log Y_j\rfloor\). In the low-order branch both orders divide \(\operatorname{lcm}(1,\ldots,T_j)\). Let \(d=\operatorname{ord}_q(3)\) and let \(Y(d)\) be the first \(Y_j\) whose \(T_j\) allows every prime power in \(d\). Since \(q\equiv3\bmod4\), \(v_2(d)\le1\). Quadratic reciprocity gives \(q\equiv11\bmod12\) for odd \(d\), and \(q\equiv7\bmod12\) for even \(d\). Thus odd \(d\) is coprime to \(3\). Together with \(q\equiv1\bmod d\), this puts each exact-order class in one progression of spacing \(M=\operatorname{lcm}(12,d)\).

At a genuine terminal \(q^2\mid3^d-1\), by lifting from \(q-1\) to the exact order. As \(q\) divides none of the smaller-order factors, \(q^2\mid\Phi_d(3)\). The product of the squared primes in the entire class therefore divides this **one integer**, even when the primes lie in different dyadic intervals. Put
\[
C_d=\varphi(d)\log3+\tfrac34 .
\]
The cyclotomic product formula gives \(\log\Phi_d(3)\le C_d\), since \(\sum_{m\ge1}|\log(1-3^{-m})|\le3/4\). The class has at most \(N=\lfloor C_d/(2\log Y(d))\rfloor\) terminals. For \(N\ge1\), packing \(N\) terms as early as the spacing allows bounds their total \(1/q\) charge by
\[
\min\left\{\frac{N}{Y(d)},\ \frac1{Y(d)}+
 \frac1M\log\left(1+\frac{(N-1)M}{Y(d)}\right)\right\}.
\]

For the first 48 intervals, let \(L_o=\operatorname{lcm}(1,3,\ldots,53)\). The simultaneous certificate replaces \(\Phi_d(3)\) by \(\gcd(\Phi_d(3),5^e-1)\). Start with \(e=2L_o\). If \(5\mid d\), then \(q\equiv1\bmod5\) and base \(5\) has odd order, so take \(e=L_o\). If \(d\) is odd, \(q\equiv11\bmod12\) forces \(3\nmid q-1\), so remove the full \(3\)-power from \(e\). The replay computes each gcd by modular exponentiation and deletes a class when its gcd is below \(Y(d)^2\). A true-order control is \(q=11\), where both orders are \(5\), \(\Phi_5(3)=121\), and \(\gcd(121,5^5-1)=11\). The base-3 square divisibility holds there and the simultaneous square divisibility fails.

For the tail, write \(L=2\operatorname{lcm}(1,3,\ldots,T_j)\). The inert progression has spacing at least \(2d\). The per-class charge is at most \(\sqrt{\log3/(4Y_j\log Y_j)}+1/Y_j\), by taking the minimum of the divisor-product and progression counts. The replay verifies \(\tau(L)\le70L^{1/6}\) from the primewise maxima of \((a+1)^6/p^a\), using \(v_2(L)=1\). Rosser–Schoenfeld gives \(L\le Y_j^{104/125}\). The resulting two geometric exponents are \(271/750\) and \(323/375\), so the finite gcd cutoff requires no assumption on larger gcds. [Rosser–Schoenfeld, Theorem 12](https://doi.org/10.1215/ijm/1255631807)

### Standalone replay

The predecessor denominator below is written as `59266799168786352*10**45`. I checked exact equality against the integer copied from the pinned note. All certificate comparisons use rational arithmetic. The replay below independently reconstructs both the removed charge and the exact carried-forward predecessor.

```python
from fractions import Fraction as Q
from math import ceil, floor, gcd, isqrt, lcm, prod

B, W, Z = 9*10**14, 10**11, 10**25
J, K = 48, 8192

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

l2, u2 = series(Q(2))

def logs(x):
    y, k = Q(x), 0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    a, b = series(y)
    return Q(floor(W*(a+k*l2)),W), Q(ceil(W*(b+k*u2)),W)

def fast_hi(n,d):
    assert n >= d
    k = n.bit_length()-d.bit_length()
    if n < d << k:
        k -= 1
    z = Q(n-(d << k), n+(d << k))
    return k*u2+2*z+2*z**3/(3*(1-z*z))

def exp_lo(x,n):
    s = t = Q(1)
    for k in range(1,n):
        t *= x/k
        s += t
    return s

def primes(T):
    return [p for p in range(2,T+1)
            if all(p%d for d in range(2,isqrt(p)+1))]

def divisors(T):
    ds = [1]
    for p in primes(T):
        pp = [1]
        while pp[-1]*p <= T:
            pp.append(pp[-1]*p)
        ds = [d*t for d in ds for t in pp]
    return ds

Y = [B*2**j for j in range(J)]
L, U = logs(B)
ln3 = logs(3)[1]
tlo = [L+j*l2 for j in range(J+1)]
T = [floor(Q(4,5)*(U+j*u2)) for j in range(J)]
assert T == [floor(Q(4,5)*t) for t in tlo[:-1]]
assert T[-1] == 53

def tail(j,m,C,inert):
    cap2 = (Q(2**(m-1)) if inert else
            max(Q((a+1)**m,2**a) for a in range(7)))
    assert cap2*prod(
        max(Q((a+1)**m,p**a) for a in range(7))
        for p in primes(2**m-1) if p>2
    ) < C**m
    assert 8**m < (3 if inert else 2)*7**m
    a, x = Q(104,125*m), tlo[j]

    def geom(z):
        return 1/(exp_lo(z*x,100)*(1-1/exp_lo(z*l2,12)))

    root = Q(isqrt(floor(ln3*Z*Z/((4 if inert else 2)*x)))+1,Z)
    return C*(root*geom(Q(1,2)-a)+geom(1-a))

old_count = 0
for j in range(24):
    A = ln3/(2*tlo[j]*Y[j])
    old_count += sum(ceil(Z*min(A*d,Q(1,d)+Q(1,Y[j])))
                     for d in divisors(T[j]))
old_finite = Q(old_count,Z)
old_tail = tail(24,4,9,False)
old = old_finite+old_tail
assert floor(W*old) == 655474

# Odd part, its totient, largest prime power, and prime support.
orders = [(1,1,1,())]
for p in primes(T[-1])[1:]:
    additions = []
    m = p
    while m <= T[-1]:
        additions.extend((d*m,ph*(m-m//p),max(k,m),ps+(p,))
                         for d,ph,k,ps in orders)
        m *= p
    orders.extend(additions)
Lodd = lcm(*range(1,T[-1]+1,2))
M3 = max(3**k for k in range(T[-1]) if 3**k <= T[-1])
entry = {k:next(j for j,t in enumerate(T) if t>=k)
         for k in range(1,T[-1]+1)}

def cyclo3(d,ps):
    terms = [(d,1)]
    for p in ps:
        terms += [(m//p,-s) for m,s in terms]
    return (prod(3**m-1 for m,s in terms if s==1) //
            prod(3**m-1 for m,s in terms if s==-1))

def packed(Y0,M,N):
    if not N:
        return 0
    if (N-1)*M*2 <= Y0:
        return ceil(Z*Q(N,Y0))
    integral = Q(1,Y0)+fast_hi(Y0+(N-1)*M,Y0)/M
    return ceil(Z*min(Q(N,Y0),integral))

new_count = plain_count = gcd_classes = gcd_zeros = 0
for m,phi,k,ps in orders:
    cases = [(2*m,lcm(12,2*m),ps+(2,))]
    if m%3:
        cases.append((m,12*m,ps))
    j = entry[max(k,2)]
    cap = phi*ln3+Q(3,4)  # phi(2*m) = phi(m) for odd m
    N = floor(cap/(2*tlo[j]))
    for d,M,support in cases:
        v = packed(Y[j],M,N)
        plain_count += v
        if v and d<=K:
            A = cyclo3(d,support)
            e = Lodd if d%5==0 else 2*Lodd
            if d%2:
                e //= M3
            G = gcd(A,pow(5,e,A)-1)
            gcd_classes += 1
            if G < Y[j]**2:
                gcd_zeros += 1
                v = 0
            else:
                capG = min(cap,fast_hi(G,1))
                v = packed(Y[j],M,floor(capG/(2*tlo[j])))
        new_count += v

new_finite = Q(new_count,Z)
new_tail = tail(J,6,70,True)

pre81 = Q(8401430807510648551056610750957092065253478722474169318289,
          59266799168786352*10**45)
prev = pre81-Q(9636386-19019,W)-Q(3695048,W)
assert Q(863195,W) < prev < Q(863196,W)
retained = prev-old
fixed = Q(77796+21648+25603+1633+7320,W)+Q(14,2**27)
assert floor(W*(retained-fixed)) == 63290
assert (gcd_classes,gcd_zeros) == (695,695)
answer = retained+new_finite+new_tail
assert answer < Q(216683,10**11)

q = 11
assert all(b%q != 1 and pow(b,5,q)==1 for b in (3,5))
assert [pow(b,5,q*q) for b in (3,5)] == [1,100]
assert cyclo3(5,(5,)) == q*q and gcd(q*q,5**5-1) == q

print("old finite and tail",float(old_finite),float(old_tail))
print("new finite before gcd",float(Q(plain_count,Z)))
print("new finite and tail",float(new_finite),float(new_tail))
print("retained",float(retained))
print("exception density percent",float(100*answer))
```

In the tail, the inert odd-order lcm with its single factor of two divides \(\operatorname{lcm}(1,\ldots,T_j)\), so the same Rosser–Schoenfeld upper bound applies. To see the cyclotomic error bound, use \(-\log(1-3^{-m})\le(3/2)3^{-m}\) and sum over all positive \(m\). The standard-library rational replay was run on the previously published denominator; it gives the outward upper bound of \(0.000216683\%\). The two retained infinite tails and inherited slack are charged in full.