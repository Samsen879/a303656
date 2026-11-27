# Effective reader depth with smaller, reader-prime-free strides

**The strides can be bounded effectively and can omit every higher reader’s own prime.** For \(T=7^k\), there is an unconditional version of the depth-\(k\) obstruction with
\[
\log A,\ \log B=O(T(\log T)^2).
\]
The construction still uses \(6k\) actual inert readers. It enforces odd valuation throughout the finite active box by choosing the target lifts modulo \(q^2\). This saves the factors \(q\) previously used to freeze the readers’ own primary digits.

### Effective choice of readers

At depth \(j\), put \(m=7^j\) and use
\[
F=\mathbb Q(\zeta_{4\cdot59\cdot13\cdot7m}),
\qquad L=F(3^{1/7},5^{1/m}).
\]
The seventh root of \(3\) suffices. Once \(v_7(q-1)=j\), the condition \(3^{(q-1)/7}\ne1\bmod q\) gives exact order \(m\) for the \(7\)-primary projection. The \(m\)-th root of \(5\) makes its corresponding projection trivial.

Prescribe \(q\equiv3\bmod4,\ q\equiv2\bmod59,\ q\equiv1+m\bmod7m\), and use six distinct nonzero classes modulo \(13\). The radical multipliers can be prescribed as \(\zeta_7,1\). Independence follows from valuations at \(3,5\) in \(F\), where both primes are unramified. Frobenius reduction then gives the two required power conditions.

All \(6k\) readers can be taken in one interval \((Y,2Y]\) with \(\log Y=O(T\log T)\). To apply effective Chebotarev, let \(J=\operatorname{Gal}(L/F)\) and let \(\tau\) be the prescribed lift. The subgroup \(H=\langle J,\tau\rangle\) is abelian because \(\tau\) fixes \(\mu_m\). Its fixed field \(K\) lies in \(F\), so \([K:\mathbb Q]=O(m)\) and \(\log|D_K|=O(m\log m)\).

The maximum conductor norm \(\mathcal Q\) for the characters of \(H\) also has \(\log\mathcal Q=O(m\log m)\). Locally, a character of order dividing \(|H|\) is trivial on \(|H|\)-th powers. The principal-unit logarithm bounds its conductor exponent at a prime above \(r\) by \(e_r(2+v_r(|H|))\). Summing conductor norms uses only the fixed set \(r\in\{2,3,5,7,13,59\}\). Thus the logarithm of the parameter \( |D_K|\mathcal Q[K:\mathbb Q]^{[K:\mathbb Q]}\) in Theorem 1.4 is \(O(m\log m)\). Its relative error can be made uniformly small at both \(Y\) and \(2Y\). Even for the subtractive exceptional-zero term, the main-term difference is a fixed fraction of the endpoint main terms. This follows by integrating \((1-t^{\beta-1})/\log t\) on \([Y,2Y]\): the numerator is increasing in \(t\), so its value at \(Y\) bounds the endpoint integral from above and bounds the dyadic increment from below, after the corresponding logarithmic-integral factors. Hence each specified class occurs in that interval. [Thorner–Zaman, *A unified and improved Chebotarev density theorem*, Theorem 1.4](https://arxiv.org/pdf/1803.02823)

### Use only the orders read by the chart

Take \(D\) divisible by \(522\) and by the actual factors
\[
\operatorname{ord}_q(3)/7^j,\qquad \operatorname{ord}_q(5)
\]
for all readers. Set \(A=827D,\ B=414D\). No selected reader prime divides these factors. Two odd primes in the common dyadic interval cannot have one dividing the other minus one. The \(7,59\) native slope stays \(v\equiv-27u\bmod413\) because \(A/522\) and \(B/522\) agree modulo \(413\).

At depth \(j\) the six readers still hit exactly the six columns
\[
u\equiv (a+1)7^{j-1}-1\bmod7^j,\qquad 0\le a<6.
\]
Their union leaves \(u\equiv T-1\bmod T\). At a reader \(q\), the offsets along its column may now vary modulo \(q^2\). In the negative box \(0\le u\le T-2,\ 0\le v<2T\), there are fewer than \(2T^2\) offsets. Choose \(Y>2T^2\). Among the \(q\) lifts of the common collision residue, one avoids every offset modulo \(q^2\). All hits in that box then have exact valuation one.

For the height constraint, set \(X=3^{99+A(T-1)}\), and choose the native residues to give exact valuation two at \((T-1,0)\). Take the adjacent targets \(n_-<4X\le n_+\) in the resulting CRT class modulo \(M\). If needed, enlarge \(D\) by a power of \(2\) so that \(D\ge\operatorname{bitlength}(M)\) and \(X>M\). The negative quarter-box then has \(u\le T-2,\ v<2T\), while the witness enters at \(n_+\) and has positive remainder. This padding adds only \(O(\log\log M)\) to the log stride. Summing the log orders of the \(6k\) readers gives the claimed bound.

### Exact two-depth replay

These twelve primes all lie in one dyadic interval. Neither stride is divisible by any of them. At the negative target the ordinary index box is \([0,47]\times[0,65]\), with eight exact-native candidates and no panel survivor. At the adjacent positive target, \((48,0)\) enters and passes. The replay uses symbolic exponent height, so it never materializes the enormous targets.

```python
from math import gcd, isqrt, lcm, prod

G = ((401087,402851,405343,405763,406183,407947),
     (420323,469127,478927,483827,527143,529103))
P,T = 413,49
rows = [(q,7**j,(a+1)*7**(j-1)-1)
        for j,group in enumerate(G,1) for a,q in enumerate(group)]
def order(g,q):
    return min(a for d in range(1,isqrt(q-1)+1) if (q-1)%d==0
               for a in (d,(q-1)//d) if pow(g,a,q)==1)
assert len({q for q,_,_ in rows})==12
assert all(400000<q<800000 and q%4==3 and q>2*T*T
           and (q-1)%m==0 and gcd((q-1)//m,P)==1
           and all(q%d for d in range(2,isqrt(q)+1)) for q,m,_ in rows)
D = lcm(522,*(order(3,q)//m for q,m,_ in rows),
            *(order(5,q) for q,_,_ in rows))
A,B = 827*D,414*D
assert gcd(A*B,P*prod(q for q,_,_ in rows))==1

def off(m,u,v):
    return (pow(3,99+A*u,m)+pow(5,B*v,m)) % m

t = {4:1,3:0}
for q,m,b in rows:
    assert pow(3,A*m,q)==pow(5,B,q)==1
    assert pow(3,A*(m//7),q)!=1
    z=off(q,b,0)
    bad={off(q*q,u,v) for u in range(b,T-1,m) for v in range(2*T)}
    assert all(x%q==z for x in bad)
    t[q*q]=next(z+h*q for h in range(q) if z+h*q not in bad)
    assert (t[q*q]-off(q,T-1,0))%q
assert all(sum(u%m==b for _,m,b in rows)==(u!=T-1) for u in range(T))
for p in (7,59):
    assert pow(3,A,p)==pow(5,B,p)==1
    a=(pow(3,A,p*p)-1)//p*pow(3,99,p)%p
    b=(pow(5,B,p*p)-1)//p%p
    assert b and a==27*b%p
    t[p**3]=(off(p**3,T-1,0)+p*p)%p**3

M=prod(t)
r=sum(a*(M//m)*pow(M//m,-1,m) for m,a in t.items())%M
e=99+A*48                       # X = 3**e
x=pow(3,e,M)
assert e>M.bit_length()         # X > M
assert (r-4*x)%M + 1+(4*x-1-r)%M == M
assert 3**(827*48)>5**(414*65)
assert 3**(99+827*48)<5**(414*66)
S=[(u,v) for u in range(48) if (v:=(27*(48-u))%P)<=65]
assert sum(all((z:=(r-off(p**3,u,v))%p**3) and z%p**2==0
               for p in (7,59)) for u,v in S)==8
```

The result controls the strides and preserves the growing obstruction on an actual anchored quarter-box. It leaves open a fixed-stride construction and any comparable bound at a prescribed target. The positive control passes the specified local panel, with the remaining inert primes unchecked.
