# One candidate per extra prime after uniform height truncation

In [the fixed-109 model](SPLIT109_CRT_AND_QUARTIC_FILTER.md), keep \(X=3^u,Z=5^v,\ \Delta=Z-X\), \(R_s=n-1-Z,\ R_d=n-1-X\), and the same balanced high powers, positive residuals, negative cross offset, and strong rough-product window. For fixed \(\eta>0,\tau,\gamma\ge0\), assume \(109^f\ge n^\eta,\ p^t\le n^\tau,\ Y\le n^\gamma,\ \tau+4\gamma<\eta\). The deep valuation \(E\) at the additional inert prime \(p\) is even.

Choose a constant \(a<1-\tau-4\gamma\) with \(a+\eta>1\). In any sufficiently large dyadic block \([N,2N)\), take \(P_0=p^{E_0}\) to be the least even power at least \(N^a\), and \(Q_0=109^{F_0}\) to be the least integer power at least \(N^\eta\). The [fixed-support rough-product bound](FIXED_SUPPORT_CROSS_SUM_OBSTRUCTION.md) gives \(p^E\gg_\epsilon n^{1-\tau-4\gamma-\epsilon}\) for any fixed \(\epsilon>0\); hence \(E\ge E_0,\ f\ge F_0\) uniformly over candidates in the block. Thus without choosing the exact depths we already have \(R_d\equiv0\bmod P_0,\ R_d\equiv\Delta\bmod Q_0\) and \(P_0Q_0>2N\). The only possible nonnegative representative below the height bound is
\[
r_0=\Delta P_0^{-1}\bmod Q_0,\qquad n_0=X+1+P_0r_0
\]
using the least nonnegative residue. This gives at most one actual candidate per prespecified label and prime. The number per block is \(O(\pi(Y_{\max}))\) rather than this bound times the possible depths, since the balanced powers allow only \(O(1)\) actual label pairs. For one label these candidates all obey \(n\equiv Z+1\bmod Q_0\), so distinct ones are spaced by at least \(N^\eta\). The bound is ineffective in its starting height and permits sparse infinite families.

For \(d=v_{109}(\Delta)<F_0\), write \(h=F_0-d,\ \delta=\Delta/109^d\). The normalized representative \(r=r_0/109^d\) is \(\delta p^{-E_0}\bmod109^h\). Its allowed interval has relative length \(O(N^{1-a-\eta})\). For actually qualifying \(n\) the quartic filter is \(w_d^{27}\equiv r^{27}(p^{54})^{-(E-E_0)/2}\bmod109\); substituting a provisional exponent for \(E\) without the correction need not preserve it. For comparison, a fixed \(E_0\) acting on the **full** group of square units modulo \(109^h\) has uniform output on its power-map image. On the principal units that image consists of complete lifts of classes modulo \(109^{\min(h,1+v_{109}(E_0))}\), by the cyclic group structure. An interval of length \(H\) therefore receives frequency \(H/109^h+O(109^{\min(h,1+v_{109}(E_0))-h})\). This gives no such estimate on small prime inputs, especially with \(E_0\) changing across primes.

## Exact lower-modulus control

At \(u=80,v=55,p=11,f=10\), the depth-18 representative gives \(n=327791597785373499258059333029444990119\) with actual \(11\)-depths \((2,18)\), \(109\)-depths \((10,0)\). It is only a local candidate: the rough parts and true norm tests fail. At truncated depth 16 the least representative is below the eligible interval; the true congruence still contains the large candidate in a later period. This shows why the lower-bound check on the full CRT modulus is necessary.

```python
def v(n,p):
    c=0
    while n%p==0:
        n//=p; c+=1
    return c
X,Z=3**80,5**55
q=109**10
def rep(E):
    p=11**E
    return X+1+p*((Z-X)*pow(p,-1,q)%q)
n=327791597785373499258059333029444990119
assert rep(18)==n and max(X,Z)+1<n<X+Z
assert rep(16)<max(X,Z)+1 and (n-rep(16))%(11**16*q)==0
rs,rd=n-1-Z,n-1-X
assert (v(rs,11),v(rd,11),v(rs,109),v(rd,109))==(2,18,10,0)
assert v(rs,139)%2==v(rd,2063)%2==1
```
