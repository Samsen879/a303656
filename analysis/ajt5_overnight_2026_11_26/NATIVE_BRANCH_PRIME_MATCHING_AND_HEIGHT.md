# Native prime matching for a quadratic map with branch value 1

Continue [the preceding quadratic branch obstructions](https://github.com/Samsen879/a303656/commit/a4a5541b31935dd5829e54161d7d5f5ba31e3d7b). For \(d=17^j,\ j\ge1\), put \(L=\mathbb Q(\zeta_d)\), \(u_\pm=\mp(3/5)\zeta_d\), and \(H_d^\pm=\Phi_d(5,\mp3)=(5^d\pm3^d)/(5^{d/17}\pm3^{d/17})\). Suppose a quadratic rational map has two branch values \(1,v=m/n\ne1\) with \(n>0,(m,n)=1\). A necessary condition for both pulled-back signed shells to be norms is
\[
 \prod_{p:\ v_p(H_d^-H_d^+)\ {\rm odd}}p\ \mid\ m-n .
\]
This is independent of the scalar in the quadratic discriminant. It is a necessary arithmetic condition for the formal rational pullback, not a construction of a mixed numerical generator.

Every prime occurring in either native shell is primitive by LTE: the only possible exceptional prime is 17, and \(5/3\) has order 4 modulo 17. The two shells are coprime and their primes are odd, prime to 15, and congruent to 1 modulo \(2d\). Thus they split completely in \(L\); at exactly one prime above such a \(p\) the corresponding \(u_\pm-1\) has positive valuation, equal to the rational shell valuation. The criterion requires \(\tfrac a{-3}(u_\pm-1)(u_\pm-v)\) to be a square for both signs, where \(a\in\mathbb Q^\times\) is the discriminant coefficient. If \(v\) is not \(p\)-integral, the second factor has uniform valuation at all the primes above \(p\), which leaves the isolated odd valuation unmatched. If \(v\) is integral, each branch can vanish at at most one prime above \(p\). A prime above \(p\) where neither vanishes then forces the rational scalar to have even valuation. It follows that both branches must vanish at the same prime above \(p\), giving \(v\equiv1\bmod p\) for every odd native valuation.

For \(d=17\) the exact factors are \(2347,162507523\) on the minus side and \(95383574161\) on the plus side. All three are independently certified prime by trial division. The product is \(36379787028593273287441\), so \(\max(|m|,n)\) is at least half that number. Across the entire tower, the minus shell is a nonsquare modulo 7 and the plus shell a nonsquare modulo 19. Indeed seventeenth powering inverts the base units at both primes, reducing the two signed quotients to \(\pm(AB)^{-1}\) (minus/plus respectively), where \(A=5^{d/17},B=3^{d/17}\). Hence each sign supplies at least one distinct primitive odd-valuation prime. This proves the factorization-free bound \(|m-n|\ge(2d+1)(4d+1)\), excluding any fixed rational \(v\ne1\) sufficiently far up the tower. We do not assert an independently verified full squarefree factorization at \(d=289\).

## Two false positives for weaker tests

For a 7-adic unit \(v\) the separate square-character tests at 7 for both signs hold exactly when \(v\bmod7\in\{1,2,4\}\) and \(v_7(a)\) is even. The residue degree is \(\varphi(d)\), by the order of 7 modulo powers of 17. The finite-field square character is the rational norm's character over \(\mathbb F_7\). Away from the coincident-base residues \(v=2,5\bmod7\), the same inversions evaluate the homogeneous quotients. At each coincident residue the quotient is the derivative value \(17\,A^{16}\) instead. The finite checks below cover both possible exponents \(d/17\bmod6\).

First, \(v=9/25\) is an exact false positive for rational resultant testing. Reciprocity gives \(\Phi_d(45,\mp75)=15^{\varphi(d)}H_d^\pm\), so multiplying by each native shell gives a square. However \(m-n=-16\) fails native prime matching.

Second, let \(p=2347,\ M=H_{17}^-H_{17}^+\), and let \(u\) be the actual minus-shell root in the \(p\)-adic field reducing to 1. Hensel arithmetic gives \(u\equiv1+600p\bmod p^2\). Set \(D=3\cdot7\cdot17\cdot p(M/p)^2\) and \(v=1+D(1167+pt)\) for any \(t\ge0\). The maps \((1+3vT^2)/(1+3T^2)\) have these branch values and \(a/(-3)=4\). They pass prime matching and the other native-prime local square tests (there \(v-1\) is divisible by the prime squared). At the critical embedding over \(p\),
\[
 (u-v)/(u-1)\equiv1-1200/600=-1\bmod2347,
\]
which is a nonsquare. This supplies a true family after the first divisibility threshold and a sharp false positive for that threshold alone.


```python
from math import isqrt
def H(d,s):
    return (5**d+s*3**d)//(5**(d//17)+s*3**(d//17))
def prime(n):
    return n>1 and n%2 and all(n%p for p in range(3,isqrt(n)+1,2))
ps=(2347,162507523,95383574161)
assert all(map(prime,ps))
assert H(17,-1)==ps[0]*ps[1] and H(17,1)==ps[2]
M=H(17,-1)*H(17,1)
assert M==36379787028593273287441
assert pow(7,8,17)==16 and pow(7,16,289)!=1
p=2347
u=1+600*p
assert pow(u,17,p*p)==pow(3*pow(5,-1,p*p),17,p*p)
D=3*7*17*p*(M//p)**2
assert D*1167//p%p==1200 and pow(-1,(p-1)//2,p)==p-1

def phi17(a,b,p):
    return sum(pow(a,16-j,p)*pow(b,j,p) for j in range(17))%p
for r in (1,5):
    good=[]
    for v in range(1,7):
        s=[phi17(pow(5,r,7),pow(e*3,r,7),7)*
           phi17(pow(5*v,r,7),pow(e*3,r,7),7) for e in (1,-1)]
        if all(pow(x,3,7)==1 for x in s):
            good.append(v)
    assert good==[1,2,4]
```
