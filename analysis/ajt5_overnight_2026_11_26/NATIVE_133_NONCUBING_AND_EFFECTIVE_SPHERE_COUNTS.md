# A genuine native 7-by-19 extension and effective restricted sphere counts

The native mixed index \(133=7\cdot19\) passes on both signs, unlike mixing either of these constituents with 17. It is an actual numerical non-cubing extension. Together with the old admissible labels it improves the worst logarithmic height ratio of the restricted six-ray catalogue to \(399/289\), without claiming to improve the bottleneck of the larger catalogue or solve specified-target selection.

For the effective count, the first-three-factor swap preserves each residue zero position because the total sign of their orientations is the same. The two positions can be separated by choosing total sign \(+1\) or \(-1\), since their shifts at 3 and 5 are opposite. In either of the two allowed rotations, the fixed angle difference of the swapped iterates is nonzero modulo \(\pi\), so one of its two choices gives a \(|W|\) lower bound with an effective positive constant. For a given \(L\), the two resulting \(D_L\) values are not divisible by 5 and have different characters there; passing to each discriminant \(-4D_L\) and then to its fundamental discriminant preserves the character. Thus the two class numbers cannot both use Tatuzawa's one possible exceptional fundamental discriminant. No factor-distribution assumption on future mixed exponents is used.

**The native index \(133=7\cdot19\) is admissible.** Both mixed shells have exact integer norm witnesses, so \(19\) genuinely extends the native \(7\)-ray, and \(7\) extends the \(19\)-ray. The new ray improves the worst height ratio for the restricted native catalogue from \(27/17\) to \(399/289\). A fixed orientation rule makes the resulting population bound effective.

### Exact native extension

Call \(r\) admissible when \(5^{2r}-3^{2r}\) is an integer norm \(N(x,y)=x^2+3y^2\). For \(s=\pm1\), the mixed factor is
\[
C_s=\frac{(5^{133}+s3^{133})(5+s3)}
{(5^7+s3^7)(5^{19}+s3^{19})}.
\]
The following coordinates certify \(C_s=N(x,y)\).

| \(s\) | \(x\) | \(y\) |
|---:|---:|---:|
| \(-1\) | 24154595959064041217172862450677597649 | 15107685049824512516701176173004966960 |
| \(+1\) | 23094707327054003888373833473805745703 | 37693776002755681589913911555052785548 |

Multiplying these norms with the two signed factors for each of \(7\) and \(19\), and the initial norm \(16\), certifies \(133\). The cube identity then certifies every \(133\cdot3^k\).

There is an exact restricted classification. Among indices \(3^k7^a17^b19^c\) with \(c\le1\), the admissible ones are precisely
\[
3^k\{1,7,17,19,133,289\}.
\]
The four forbidden divisor patterns \(49,119,323,4913\) have witnesses \(197,239,647,135372803\), respectively. Each witness is inert, has exact squared-ratio order equal to the forbidden divisor, and occurs at valuation one. Each lies outside the restricted prime support, so LTE preserves that odd valuation throughout the indicated family. This classification leaves \(19^2\) open.

### A fixed rule for effective height counts

The rule applies to any seed \(Q_0=5^{2u}>Z_0=3^{2v}\) with \(u,v\) odd and \(4(Q_0-Z_0)=V_0^2+3W_0^2\) with \(8\mid V_0,W_0\). All six native rays satisfy this input.

Write \(J=\sqrt{-3}\) and \(\omega=(1+J)/2\). Cubing \(Q,Z\) multiplies the norm coordinate by
\[
g=\frac{Q-Z}{2}+J\frac{Q+Z}{2}
\]
or its conjugate. At every step, \(g\equiv\omega\bmod3\) and \(g\equiv\omega^{-1}\bmod5\). For any resulting coordinate \(V+JW\), there is exactly one of the three rotations by \(1,\omega,\omega^2\) with \(W=0\bmod3\), and exactly one with \(W=0\bmod5\). For the latter, \(V^2+3W^2\equiv4\bmod5\) gives \(W^2\in\{0,1\}\), and the rotated second coordinates are \((W+V)/2\) and \((V-W)/2\).

Use the first three cubic factors with total sign \(+1\) or \(-1\). Those options shift the two zero positions in opposite directions, so one option separates them. In that option, swapping the first two opposite signs preserves both residue positions. It changes the real angle by a fixed nonzero amount, since the first two cubic factors have distinct arguments. Consequently, for each of the two rotations allowed modulo \(3\), one of the swapped choices gives \(|W|\gg_{\rm seed}\sqrt Q\). The constant is effective from the first two factors. This gives two large orientations with \(3\nmid W\), one with \(5\mid W\) and one with \(5\nmid W\).

For either \(L=1,3\), their sphere values \(D_L=3W^2+2LZ\) have opposite quadratic characters modulo \(5\). Hence their fundamental discriminants are distinct and at most one is Tatuzawa’s possible exception. Gauss’s three-square formula and the quadratic-order class-number formula then give an effective \(\gg_\epsilon Q^{1/2-\epsilon}\) representations on at least one sphere. Here the conductor Euler factors cost at most a smaller power of \(Q\), with an effective constant. [Tatuzawa’s theorem](https://www.jstage.jst.go.jp/article/jjm1924/21/0/21_0_163/_article) · [Gauss’s representation formula](https://pure.mpg.de/pubman/item/item_3118169_2/component/file_3118171/Mortenson_A%2BKronecker-type%2Bidentity_oa_2017.pdf)

In a representation \(D_L=t^2+x^2+y^2\), choose \(t\) as the smaller odd coordinate in absolute value. Then
\[
n=5Q+LZ-x^2-y^2=Q+(4-L)Z+V^2+t^2
\]
lies in \((Q,5Q)\). It has class \(21\bmod24\) for \(L=1\) and \(3\bmod24\) for \(L=3\). Each value of \(t^2\) accounts for at most \(6r_2(D_L-t^2)\ll_\epsilon Q^\epsilon\) representations, so the bound counts distinct integers in each class.

The new normalized phase \(133/81\) splits the former bottleneck from \(289/243\) to \(17/9\). The resulting worst ratio \(399/289\) gives an **effective**
\[
\gg_\epsilon X^{289/798-\epsilon}
\]
generated targets up to \(X\) in each class, improving the restricted exponent \(17/54\). The larger catalogue’s bottleneck lies elsewhere. These are generated targets, and the new certificate supplies a fixed non-cubing extension with no assertion about its higher powers.



```python
from fractions import Fraction
from math import isqrt

P=[(7,-1,137,80),(7,1,74,39),(19,-1,3038279,318864),
   (19,1,89884,889991)]
M=[(-1,24154595959064041217172862450677597649,15107685049824512516701176173004966960),
   (1,23094707327054003888373833473805745703,37693776002755681589913911555052785548)]
def N(x,y): return x*x+3*y*y
def mul(x,y,a,b): return x*a-3*y*b,x*b+y*a

V,W=4,0
for r,s,x,y in P:
    assert (5+s*3)*N(x,y)==5**r+s*3**r
    V,W=mul(V,W,x,y)
for s,x,y in M:
    assert (5**7+s*3**7)*(5**19+s*3**19)*N(x,y)==(5**133+s*3**133)*(5+s*3)
    V,W=mul(V,W,x,y)
V,W=2*V,2*W
Q,Z=5**266,3**266
assert N(V,W)==4*(Q-Z)
if W%3==0:
    V,W=(V-3*W)//2,(V+W)//2
assert W%3 and V%4==W%4==0
for L,h in ((1,21),(3,3)):
    n=Q+(4-L)*Z+V*V+1
    assert Q<n<5*Q and n%24==h
    assert n-V*V-1==5**266+3**(267 if L==1 else 266)

for d,p,s in ((49,197,-1),(119,239,-1),(323,647,1),(4913,135372803,1)):
    assert p%3==2 and all(p%i for i in range(2,isqrt(p)+1))
    q=25*pow(9,-1,p)%p
    assert pow(q,d,p)==1
    assert all(pow(q,d//a,p)!=1 for a in (7,17,19) if d%a==0)
    R=(pow(5,d,p*p)+s*pow(3,d,p*p))%(p*p)
    assert R%p==0 and R!=0

def phase(r):
    d=1
    while 3*d<=r: d*=3
    return Fraction(r,d)
P=sorted(map(phase,(1,7,17,19,133,289)))
assert max(b/a for a,b in zip(P,P[1:]+[3]))==Fraction(399,289)
```
