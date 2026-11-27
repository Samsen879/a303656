# Fixed-menu limits for transfer from a signed norm to positive height

**No fixed finite menu of lower \(5\)-powers and \(3\)-exponent flips transfers the counted signed family wholesale.** For either odd class modulo \(4\), and for any such menu, there is an exponent progression \(D\) with \(\gg B/(1+\log B)^{15}\) distinct signed targets at each sufficiently large \(B=5^D\) on that progression. Every proposed residual is **positive**, but each has an exact odd valuation at an inert prime. The natural transfer that keeps the old real-norm coordinate \(r\) also has a size limit: it reaches at most \(O_\epsilon(B^{1/2+\epsilon})\) targets, even when all exponent pairs below the target are allowed.

### The coordinate-preserving transfer

The signed parametrization gives \(n=B+P-S\), where \(P=1\) or \(3\), \(S=x^2+y^2\), and \(2P-S=r^2-3t^2\). For a lower \(5\)-power \(5^d\) and a new \(3\)-power \(3^c\), the actual residual is
\[
n-3^c-5^d=r^2+C-3t^2,\qquad C=B-5^d-P-3^c.
\]
Keeping \(r\) as one square is therefore possible **exactly when** \(C=v^2+3t^2\) for an integer \(v\). The signed norm identity does not impose this second, positive-definite norm equation. [Counted signed parametrization](https://github.com/Samsen879/a303656/commit/df03dc909f37a1117a2ba91cd3523f28292a332a)

For \(0<C\le B\), there are at most \(2\tau(C)\) pairs \((v,t)\). Indeed, after removing a common divisor \(g\), each primitive pair determines a root of \(-3\bmod C/g^2\). Pairs with the same \(g\) and root differ by a unit of norm one in \(\mathbb Z[\sqrt{-3}]\), hence by a sign. The root bound \(2^{\omega(C/g^2)}\), summed over \(g^2\mid C\), gives \(\tau(C)\). For each \(t\), the old coordinate box permits only \(O(\sqrt B)\) values of \(r\), and \(r,t\) determine \(S\). The case \(C=0\) has only \(v=t=0\). Summing over the \(O((1+\log B)^2)\) possible exponent pairs gives the claimed upper bound on distinct targets.

### Exact vetoes for any fixed finite menu

Fix a finite list of moves \((c_i,k_i)\), with \(k_i\ge1\), prescribing \(d_i=D-k_i\). Choose a sufficiently large reference \(D_0\) and set
\[
K_i=5^{D_0}-5^{D_0-k_i}+P-3^{c_i}.
\]
Choose distinct inert primes \(q_i>3\) avoiding \(K_i(2P-K_i)\). At \(q_i^2\), prescribe \(S\equiv K_i-q_i\). Both norm equations
\[
x^2+y^2=S,\qquad r^2-3t^2=2P-S
\]
have nonsingular solutions modulo \(q_i\) and lift to \(q_i^2\). We can require \(s=x+y+r-3t\ne0\bmod q_i\): for fixed \(r,t\), the forbidden line meets the first norm conic in at most two points, while that conic has \(q_i+1\) points. These local solutions prescribe unit values of \(m=s/2\) and compatible values of \(a=x-t,\ b=y-t\).

To count integer seeds, take \(m\) in the resulting CRT class and dovetail these phases with the old congruence \(a^2+ab+b^2\equiv P\pmod m\). This retains at least \(\varphi(m)\) choices at each \(m\). More explicitly, with \(Q=\prod_i q_i^2\), use representatives modulo \(6mQ\), add \(12mQ\) to \(a\), and take \(\sqrt B/(2000Q^2)\le m\le\sqrt B/(1000Q^2)\). The same coordinate estimates give \(S\asymp_{\rm menu}B\) and \(S<0.18B\). The totient sum in the fixed unit class gives \(\gg_{\rm menu}B\) quadruples. The original divisor second moment then gives \(\gg_{\rm menu}B/(1+\log B)^{15}\) distinct \(S\), hence distinct \(n\). [Original projection count](https://github.com/Samsen879/a303656/commit/df03dc909f37a1117a2ba91cd3523f28292a332a)

Take \(D\equiv D_0\) modulo the lcm of the actual orders of \(5\bmod q_i^2\). Each proposed residual then satisfies
\[
n-3^{c_i}-5^{D-k_i}\equiv q_i\pmod{q_i^2}.
\]
For large \(B\), \(n>0.82B\) and the proposed shift is at most \(B/5+O_{\rm menu}(1)\). Thus positivity holds throughout. What is missing is the **new Gaussian norm condition** at the lowered height, even though both old norms are genuine.

### True-power controls

- The signed target \(539=3+625-(8^2+5^2)\) has \(2\cdot3-89=(-28)^2-3(-17)^2\). Its first move gives \(539-1-125=413=7\cdot59\), but another move succeeds: \(539=3^2+5^2+21^2+8^2\).
- The coordinate-preserving transfer succeeds at \(611=3+625-(1^2+4^2)\). Here \(r=-1,\ t=-2\), and \(C=496=22^2+3t^2\), so \(611=1+125+1^2+22^2\).

The standalone replay below checks both controls and constructs a single signed target with simultaneous exact vetoes at 7 and 11 for two positive-height moves. The population obstruction applies to the specified menu only.

```python

assert 539==3+625-(8**2+5**2)
assert 6-89==(-28)**2-3*(-17)**2
assert 539-1-125==7*59
assert 539==3**2+5**2+21**2+8**2
assert 611==3+625-(1**2+4**2) and 6-17==(-1)**2-3*(-2)**2
assert 625-125-3-1==22**2+3*(-2)**2
assert 611==1+125+1**2+22**2

# Same signed target and two actual lower-power vetoes.
from math import gcd,lcm
P=3
moves=((0,1,7),(2,2,11))
def kshift(D,c,k):
    return 5**D-5**(D-k)+P-3**c
D0=next(D for D in range(8,100) if all(kshift(D,c,k)%p and
                                      (2*P-kshift(D,c,k))%p for c,k,p in moves))
def crt(rows):
    u,M=0,1
    for m,v in rows:
        u+=M*((v-u)*pow(M,-1,m)%m); M*=m
    return u,M
mr,ar,br=[],[],[]
for c,k,p in moves:
    Q=p*p
    K=5**D0-5**(D0-k)+P-3**c
    S=(K-p)%Q
    def fiber(A,B):
        for x in range(Q):
            for y in range(Q):
                if (x*x+B*y*y-A)%Q==0:yield x,y
    rr,tt=next(fiber(2*P-S,-3))
    xx,yy=next((x,y) for x,y in fiber(S,1) if (x+y+rr-3*tt)%p)
    ss=xx+yy+rr-3*tt
    mr.append((Q,ss*pow(2,-1,Q)%Q))
    ar.append((Q,(xx-tt)%Q));br.append((Q,(yy-tt)%Q))
m,Q=crt(mr+[(6,1)])
assert m and gcd(m,Q//6)==1
a,period=crt(ar+[(6,3),(m,1)])
b,_=crt(br+[(6,0),(m,1)])
a+=2*period
s=2*m
z,rem=divmod(P-a*a-a*b-b*b,s)
assert rem==0
t=z+a+b-s//2
x,y,r=t+a,t+b,t+s-a-b
S=x*x+y*y
D=D0+lcm(*(p*(p-1) for _,_,p in moves))
B=5**D
n=B+P-S
assert S%4==1 and S%3==2 and r*r-3*t*t==2*P-S and 0<n<B
for c,k,p in moves:
    rem=n-3**c-5**(D-k)
    assert rem>0 and rem%(p*p)==p
print("two positive-height exact vetoes on one signed target")
```
