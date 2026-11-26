# Modular exponent compression with both actual offsets preserved

For a bounded finite Gaussian inert-prime modulus $W$, write $W=3^eR$ with $3\nmid R$. Let $L_3=\operatorname{ord}_R3$ and $L_5=\operatorname{ord}_W5$, with the order at modulus 1 defined as 1. In an actual parent/child label $(c,f,d,\epsilon,r)$ with $\epsilon\in\{0,1\}$, the offsets are $C=3^c+5^d$ and $D=3^f+5^{d+\epsilon}-r$. Replace $c,f$ separately by themselves if below $e$, or by $e+((j-e)\bmod L_3)$ if at least $e$. Replace $d$ by $d\bmod L_5$, keeping $\epsilon,r$ fixed. This preserves both offsets modulo $W$: at $3^e$ the low 3-powers are unchanged and the high powers vanish, and at $R$ there is unit periodicity. Base 5 is a unit throughout, so the same reduction preserves $5^{d+\epsilon}$.

This transfers finite exact valuations only when $W$ includes adequate precision (at least one power above each desired valuation). It stays within a restricted actual menu only if that menu is closed under the replacements, for example coordinatewise downward closure with $\epsilon,r$ fixed. It is not a theorem that the original integer has a norm, or that the compressed rows can all be lifted to a common integer within a fixed height bound.

For $W=343$ and source label $(300,300,295,1,0)$ at $m=3^{300}+5^{295}+49$, the joint residues of $(m,C,D)$ are $(97,48,68)$. The strictly active $r=0$ joint residue interface (both steps $\epsilon=0,1$ allowed) has its first actual two-norm point at $m=783$, label $(6,6,1,1,0)$, with remainders $49=7^2$ and $3161=5^2+56^2$. The replay checks all smaller feasible residue representatives and every active label at them. This is a minimum for the stated interface only.

By contrast, replacing a high even-ball modulus by the order modulo a prime can change a true norm even with the same integer: at $m=1359$ and label $(6,2,2,1,0)$ the parent $605=11^2+22^2$ and child $6661=10^2+81^2$ are real. Reducing $c$ to $1$ using $\operatorname{ord}_{11}(3)=5$ changes the parent to $1331=11^3$, an actual odd-valuation failure.

```python
W=343
C0=(pow(3,300,W)+pow(5,295,W))%W
D0=(pow(3,300,W)+pow(5,296,W))%W
m0=(C0+49)%W
assert (m0,C0,D0)==(97,48,68)
norms={a*a+b*b for a in range(64) for b in range(64)}
hits=[]
for m in range(m0,784,W):
    for d in range(5):
        for c in range(8):
            C=3**c+5**d
            if not (C<m and C%W==C0 and m-C in norms):
                continue
            for eps in (0,1):
                for f in range(9):
                    D=3**f+5**(d+eps)
                    if D<5*m and D%W==D0 and 5*m-D in norms:
                        hits.append((m,c,f,d,eps))
assert hits==[(783,6,6,1,1)]
assert 783-3**6-5==7**2 and 5*783-3**6-25==5**2+56**2
assert 1359-3**6-25==11**2+22**2
assert 5*1359-3**2-125==10**2+81**2
assert 1359-3-25==11**3 and pow(3,5,11)==1
```
