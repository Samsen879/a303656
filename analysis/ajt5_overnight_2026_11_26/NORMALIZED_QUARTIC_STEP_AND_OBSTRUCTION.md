# Shorter integral step and an infinite obstruction for the normalized quartic

Keep the normalized moving-parent construction in MOVING_PARENT_QUARTIC.md. For even $d\ge8$ and label $(d,2;d+1,3)$ it has $H=5^d-131765$, $A=H-5$, $B=H-9$, $m=H/2$ and
$$
 w=\frac{(t^2-2)^2+m^2+B}{H}.
$$
For the concrete $d=10$ orbit in that note, one can replace the original sufficient step $30HL$ by $T=5H/2=24084650$, using the exact same anchor and rotation. The replay below interpolates all five rational polynomials of degree at most four in the new progression and verifies that their coefficients are integers. Since polynomial evaluation modulo 30 depends only on the residue of the integer parameter, checking all 30 residues then suffices to preserve $w\equiv26\bmod30$. This verifies a shorter step for this label, without claiming its minimality or validity for every label.

On the other hand, every $d=8+6j$ with $j\ge0$ has $7\mid H$. Then modulo $7$ the numerator of $w$ reduces to $(t^2+1)(t^2-5)$: both $m$ and $H$ vanish modulo $7$. Neither $-1$ nor $5$ is a square modulo $7$, so there is no integer $t$ giving integer $w$ under this normalization. This excludes this entire infinite label subfamily from the normalized integer-parameter construction. It leaves other slopes and other constructions open.

```python
from fractions import Fraction as F
H=5**10-131765
A,B=H-5,H-9
m=H//2
T,t0=5*H//2,8404257
a,b,L=-1647087,1757216,2408465
def vector(t):
 z=t*t-2
 w=F(z*z+m*m+B,H)
 D=F(t*t+A,m)
 P,Q=w-D,t*(D-1)
 return w,(a*P-b*Q)/L,(b*P+a*Q)/L,w-m-2*z,2*(w-m)+z
# Recover coefficients exactly by interpolation at n=0,...,4.
def coeff(vals):
 out=[F(0)]*5
 basis=[F(1)]
 for d in range(5):
  for i,x in enumerate(basis):out[i]+=vals[0]*x
  vals=[y-x for x,y in zip(vals,vals[1:])]
  nxt=[F(0)]*(len(basis)+1)
  for i,x in enumerate(basis):
   nxt[i]-=x*d/(d+1)
   nxt[i+1]+=x/(d+1)
  basis=nxt
 return out
wc,*cs=[coeff(list(v)) for v in zip(*(vector(t0+T*n) for n in range(5)))]
assert all(x.denominator==1 for row in (wc,*cs) for x in row)
assert wc[-1]==F(T**4,H) and wc[-1]>0
assert all(vector(t0+T*n)[0]%30==26 for n in range(30))
assert pow(5,6,7)==1 and pow(5,8,7)==131765%7
assert all((t*t+1)*(t*t-5)%7 for t in range(7))
```
