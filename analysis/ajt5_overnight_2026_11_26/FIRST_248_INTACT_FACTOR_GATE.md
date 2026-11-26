# The short-difference square-factor gate cannot use intact large factors

Keep the first-root-248 triple $d=4,e=4+2P,E=4+4P$ and put $H_i=5^{i+1}-239$, $X=H_E/2$, $Y=H_e/2$. In a shear with the short difference fixed, the direct square-factor route requires the squared value $100L=W^2$, where $L=(J-g)^2+gH_E/20$, $J=(5^E-5^e)/16$, and the fixed row has primitive even norm $g>0$. This would give positive integers $A<B$ with
$$
 AB=XY,\qquad A+B=X+Y+40g,\qquad B-A=4W.
$$
In fact multiply $100L=W^2$ by 16 and use $J=(X-Y)/40$ to obtain $(X+Y+40g)^2-16W^2=4XY$. Positivity follows from the positive sum and product; $W$ is integral because its square is an integer.

Write $\lambda=B/X=Y/A=v/u$ reduced. The factors are odd and $X,Y\equiv3\bmod8$ with $v_2(X-Y)=3$. From the sum,
$$
 g=(v-u)(vX-uY)/(40uv).
$$
The even primitive norm has $v_2(g)=1$. If $a=v_2(v-u)<3$, the other factor has the same valuation $a$, so $v_2(g)=2a-3$. If $a\ge3$, both factors are divisible by 8 and $v_2(g)\ge3$. Thus $a=2$, so $\lambda\equiv5\bmod8$ and $A,B\equiv7\bmod8$.

For $S=5^{2P}$, the terms $H_e=3125S-239,H_E=3125S^2-239$ have gcd $\gcd(2886,S-1)=2886$, by subtracting $S H_e$ and noting $239$ is prime to $H_e$. The modular data below then give
$$
 X=1443\cdot109 R_X,\quad Y=1443 R_Y,\qquad (R_X,R_Y)=1,\quad
 (R_X,R_Y)\equiv(5,1)\bmod8.
$$
There is exactly one factor 3 in each of $X,Y$. If split between $A,B$, the sum relation forces $3\mid g$, impossible for a primitive two-square norm. If both factors 3 are on the same side and $R_X,R_Y$ each remain intact, every remaining allocated block or prime is $1$ or $5\bmod8$. This cannot produce $A,B$ both $7\bmod8$. Therefore **every allocation leaving both large factors intact fails**. This forces a genuine factor split; it is not an impossibility proof for arbitrary splits or other three-column constructions.

```python
P=6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
def H(k,m):
    return (pow(5,5+k*P,m)-239)%m
assert pow(5,2*P,2886)==1
assert H(2,16)==H(4,16)==6 and (H(4,32)-H(2,32))%32==16
for p in (3,13,37):
    assert all(H(k,p*p)%p==0 and H(k,p*p)!=0 for k in (2,4))
assert H(4,109**2)%109==0 and H(4,109**2)!=0 and H(2,109)!=0
assert H(4,16*1443*109)==10*1443*109
assert H(2,16*1443)==2*1443
```
