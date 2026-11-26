# One deep exception in a finite exponential valuation column

Fix integers $A$, $B\ge2$ and an odd prime $p\nmid B$. Consider the exact values of $v_p(A-B^c)$ for $0\le c\le C$, with a zero residual handled separately. If $A\bmod p$ is outside $\langle B\rangle$, all residuals are units. Otherwise there is a single matching class $c=a\bmod t$ for $t=\operatorname{ord}_p B$, with $0\le a<t$, and only indices $c=a+tk$ can be nonunits. If this class does not intersect the window, again all entries are units.

Write $w=v_p(B^t-1)$ and $K=\lfloor(C-a)/t\rfloor$. If $v_p(A-B^a)<w$, all matching entries have that fixed valuation. In the other case, let $E$ be the least nonnegative integer with $p^E>K$. There is a unique $\kappa\bmod p^E$ such that
$$
 B^{a+t\kappa}\equiv A\bmod p^{w+E}.
$$
Indeed $k\mapsto(B^t)^k$ maps the $p^E$ residue classes bijectively to $1+p^w\mathbb Z\bmod p^{w+E}$ by the lifting formula $v_p((B^t)^k-1)=w+v_p(k)$ for nonzero $k$. For every $k$ in the window except possibly $k=\kappa$, the congruence and the same identity give
$$
 v_p(A-B^{a+tk})=w+v_p(k-\kappa).
$$
Here $\kappa$ is its least nonnegative representative. At most one matching cell needs a separate exact valuation or literal-zero record. This is a finite encoding for the same integer $A$, not a global construction of a norm or a uniform bound independent of the input bit length.

For an actual base-3 column, take $m_h=(7+11^h)^2+13^2+26$. It has a positive square-sum anchor at offset $26=1+25$. In the actual parent column $d=0$, the $c=5$ residual is $m_h-1-3^5=11^h(14+11^h)$ with valuation exactly $h$. For $h=101,102$ the strict cutoffs are respectively $440,445$, the matching exponent class is $c=0\bmod5$, and the exceptional representative is $\kappa=1$ with $E=2$. Thus arbitrarily deep odd and even states can agree with the literal zero $m=244$ to any prescribed finite 11-adic precision. A fixed truncated precision cannot replace the exact deep-state check.

```python
p,B=11,3
t=5
assert pow(B,t,p)==1 and all(pow(B,j,p)!=1 for j in range(1,t))
assert (B**t-1)%p**2==0 and (B**t-1)%p**3!=0
for h,C in ((101,440),(102,445)):
    u=p**h
    m=(7+u)**2+13**2+26
    assert B**C<m-1<=B**(C+1)
    A=m-1
    assert A%p==1 and (C//t)<p*p
    assert A%p**4==pow(B,t,p**4)
    assert (A-B**5)%p**h==0 and (A-B**5)%p**(h+1)!=0
```
