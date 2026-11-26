# A mixed subgroup energy formula and a true middle-order control

Let $p$ be an inert prime for two squares, $H=\langle9\rangle$, $K=\langle25\rangle$ inside $\mathbb F_p^\times$, and let their orders and intersection size be $R,S,g$. Write $a_C,b_C$ for the numbers of $1-h,1-k$ in a coset $C$ of $HK$, with $h\in H-\{1\}$ and $k\in K-\{1\}$. The exact mixed additive energy is
$$
 E(H,K)=RS+g\sum_C a_Cb_C.
$$
Indeed a nonzero equal difference is $x(1-h)=y(1-k)$ with $x\in H,y\in K$. The required ratio belongs to $HK$ precisely for matching cosets, and then there are exactly $g$ pairs with that ratio. The zero difference contributes $RS$.

If $HK$ is the full square subgroup, taking $h\mapsto h^{-1}$ exchanges the two square classes of $1-h$, because $h$ is a square and $-1$ is not. This splits each of $R-1,S-1$ in half and gives the closed formula $E=RS+g(R-1)(S-1)/2$. This is an exact second moment. It is not itself a sharp pointwise bound.

For the actual prime $p=541447$, the orders are $93,8733$, their intersection has size $3$, and $HK$ is the full square subgroup. The exact energy is $2017185$, while the maximum occupied cubic-block count over all phases is only $9$. The calculation is independent of any specific integer lift. For the cubic block count, subtract one from the total roots at $n$ exactly when $-n\in H\cap K$, as shown in CUBIC_PANEL_OCCUPATION_MOMENTS.md.

```python
from math import isqrt
p=541447
assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
def group(a):
    s={1}
    b=a
    while b!=1:
        s.add(b)
        b=b*a%p
    return s
H,K=group(9),group(25)
B=H&K
r,s,g=len(H),len(K),len(B)
assert (r,s,g)==(93,8733,3) and r*s//g==(p-1)//2
T=[0]*p
for h in H:
    for k in K:
        T[(h+k)%p]+=1
assert sum(t*t for t in T)==r*s+g*(r-1)*(s-1)//2==2017185
assert max(t-((-n)%p in B) for n,t in enumerate(T))==9
```
