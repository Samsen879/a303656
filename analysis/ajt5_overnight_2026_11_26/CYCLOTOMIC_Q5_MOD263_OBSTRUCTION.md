# A second disjoint infinite obstruction for the fixed slope q=5

Use the fixed-$q$ chart from CYCLOTOMIC_Q5_UNIFORM_HEIGHT.md, with $U=5^{73^k}$, $A=5U-131770$, $x=365U^5$, $r=A/x$ and $H=r+x-4$. At the prime $263$, for every $k\equiv6\bmod10$,
$$
 U\equiv53,\quad A\equiv-5,\quad x\equiv5,\quad r\equiv-1,\quad H\equiv0.
$$
This follows because $73^{10}\equiv1\bmod262$, $73^6\equiv189\bmod262$, and $5^{189}\equiv53\bmod263$.

An integral $w=((rt^2+2)^2+(H/2)^2+A-4)/H$ would force $t$ to be 263-adically integral: a pole of $t$ would make the quartic term dominate the numerator. Reducing modulo 263 now forces $(2-t^2)^2=9$, or $t^2=-1,5$. Neither is a square modulo 263, so there is no such rational $t$. This progression contains only even $k$, and is disjoint from the earlier mod-107 obstruction $k\equiv15\bmod52$. Both exclude this particular fixed slope, not all slopes or all labels.

```python
p=263
assert pow(73,6,262)==189 and pow(73,10,262)==1
u=pow(5,189,p)
a=(5*u-131770)%p
x=365*pow(u,5,p)%p
r=a*pow(x,-1,p)%p
assert (u,a,x,r,(r+x-4)%p)==(53,258,5,262,0)
assert pow(-1,131,p)==pow(5,131,p)==p-1
```
