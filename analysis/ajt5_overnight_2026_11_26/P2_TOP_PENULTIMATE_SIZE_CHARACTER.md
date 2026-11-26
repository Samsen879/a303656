# A top/penultimate size separation and a whole-block character identity

### An ordinary-height exclusion

Let \(L=24D_0\cdots D_{r-2}C_{r-1}\), \(F=F_{r-1}\), and let \(w=cz\) be the **actual** short-side top share, with \(c\mid C_r\) and \(z\mid F_r\). On the pinned balanced strip, \(1000A<K\le1100A\) is inside the ordinary window. Write its exact short-factor interval as \([V_-,V_+)\), where
\[
V_- = V(1100A),\quad V_+=V(1000A),\qquad
V(K)=\frac{\sqrt{K-S_0}-\sqrt{K-S_1}}2.
\]

If \(F\) goes wholly to the long side, then \(v\le Lw\). If it goes wholly to the short side, then \(v\ge Fw\). Therefore
\[
\boxed{\quad \frac{V_+}{F}\le w<\frac{V_-}{L}
       \quad\Longrightarrow\quad F\text{ must split nontrivially.}\quad}
\]
If \(F\) is certified indivisible in the allocation, this excludes the stated height subinterval for that \(w\). The gap is nonempty for every balanced member with even \(a\ge312\), since \(F/L>A^{7/363}/96>21/8>V_+/V_-\).

If \(C_r\) is also allocated whole, a given true \(z\mid F_r\) can support at most one pair of sides for \(C_r\) and \(F\) in this subinterval. For a multiplier \(M\in\{1,F,C_r,C_rF\}\), the allowed interval for \(z\) is \([V_-/(LM),V_+/M)\). These four intervals are disjoint by the same bound on \(F/L\) and by \(C_r/(FL)>A^{77/363}/384>21/8\). Neither test assumes a distribution for the largest prime factors.

### Why the aggregate character cannot choose a side

For a prime \(p\mid D_j\), \(j<r\), put \(h=(x/y)^{11^{r-1}}\bmod p\). The pinned orders give \(h=-1\) or \(h\) of order \(6\). After removing the square homogeneity factors, the top quotients \(C_r,F_r\) have values
\[
\begin{array}{c|cc}
h & C_r & F_r\\ \hline
-1 & 11 & 1\\
\operatorname{ord}(h)=6 & h^{-1} & 11h
\end{array}
\]
at \(p\). The \(11h\) entry follows by differentiating the polynomial identity for \((h^{22}-h^{11}+1)/(h^2-h+1)\) at the simple root. As \(p\equiv1\bmod11\), this gives
\[
(F_r/p)=1,\qquad (C_r/p)=(-1/p).
\]
Since \(C_r\equiv3\bmod4\) and \(F_r\equiv1\bmod4\), reciprocity gives \((R/C_r)=(R/F_r)=1\) for **every** divisor \(R\mid D_j\). Thus these whole-block Jacobi symbols supply no additional condition tying the two allocations together.


On \(0.9\le B/A\le1.1\), the necessary short-factor bounds from the previous result give \(4\sqrt A<V_-<V_+<21\sqrt A/2\). To verify the new constants, use \(L<72A^{13/363}\) and put \(M=\max((A/3)^{1/363},(25B)^{1/363})\). The defining quotient for \(F\) lies between \(3M^{20}/4\) and \(4M^{20}/3\); since \(22.5A\le25B\le27.5A\), this gives \(F/L>A^{7/363}/96\) and \(F<2A^{20/363}\). Likewise \(C_r>\tfrac12 A^{10/33}\), giving the stated lower bound on \(C_r/(FL)\). The total-block character argument uses \(p=1\bmod11\), and the parity identity for an order-six element \(h\) gives \((h/p)=(-1/p)\).

The independent replay checks both order types at two actual lower levels and the exact exponent cutoffs. No claim about the unpublished relocated prime control or a complete ordinary window is made.

```python
s,t=1273865740071,681186
assert s%3==t%3==0
for p,o in ((67,22),(7789,66),(1453,242),(727,726)):
    x,y=pow(3,s//3,p),pow(5,t//3,p)
    h=pow(x*pow(y,-1,p),121,p)
    z=x*pow(y,-1,p)%p
    assert pow(z,o,p)==1 and all(pow(z,o//l,p)!=1 for l in (2,3,11) if o%l==0)
    C=sum((-1)**j*pow(h,10-j,p) for j in range(11))%p
    if h==p-1:
        F=pow(h*h-h+1,-1,p)*(pow(h,22,p)-pow(h,11,p)+1)%p
        assert (C,F)==(11,1)
    else:
        F=(22*pow(h,21,p)-11*pow(h,10,p))*pow(2*h-1,-1,p)%p
        assert (C,F)==(pow(h,-1,p),11*h%p)
    assert pow(C,(p-1)//2,p)==pow(-1,(p-1)//2,p) and pow(F,(p-1)//2,p)==1
assert 3**(312*7)*8**363>(21*96)**363
assert 3**(312*77)*8**363>(21*384)**363
print("OK")
```
