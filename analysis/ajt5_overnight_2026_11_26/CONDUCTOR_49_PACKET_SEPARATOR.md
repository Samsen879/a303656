# Why reweighting the original lifts cannot match conductor 49

In the switched-prime comparison, write \(x=ds=(p+\kappa)/w\), where \(w=1,49\), \(n=S+45(p+\kappa)\), and the compatible deep labels have \(S\equiv r_-\bmod49\). Assume \(7\nmid r_-\) and set \(u_0=-45^{-1}r_-\bmod49\). This note concerns the local progression coefficients only; the [original character comparison](https://github.com/Samsen879/a303656/commit/8e1722f8104b008bcb88c21f788a76f1c0654b90) also has auxiliary divisibility conditions and different windows.

On the shallow side \(n\equiv0\bmod49\) forces \(x\equiv u_0\bmod49\). An original deep lift \(p+\kappa\equiv49j\bmod343\) only fixes \(x\equiv j\bmod7\); its principal progression coefficient splits equally over the seven lifts modulo 49. After matching positive total mass \(M\), arbitrary nonnegative constant weights on existing lifts produce the local measures
\[
\mu_1=M\delta_{u_0},\qquad
\mu_{49}=\sum_{j=1}^6 \frac{b_j}{7}\sum_{i=0}^6\delta_{j+7i},
\qquad \sum_j b_j=M,\quad b_j\ge0.
\]

Matching all characters modulo 7 requires \(b_{u_0\bmod7}=M\) by Fourier inversion on the six units; this choice suffices. Matching conductor 49 is impossible even then. The function \(x\mapsto (x^6-1)/7\bmod7\) on units modulo 49 is an additive homomorphism under multiplication, since products of the two deviations are multiples of 49. Its associated character is nontrivial on \(1+7\), so has conductor 49 and zero mean on every deep fibre. On the shallow point its absolute mean is one after normalizing mass. The integer witness \(7\,1_{x=u_0\bmod49}-1_{x=u_0\bmod7}\) has normalized means 6 and 0. The minimum total variation distance is \(6/7\), since the deep mass at \(u_0\) is at most \(M/7\). Averaging phase labels with the same \(r_-\) cannot change the conclusion.

An extra digit \(p+\kappa\equiv49u_0\bmod2401\) on the deep side would isolate the desired point in the local measure. After rescaling this refinement by seven, its local coefficients match. It is a new condition rather than a weighting of the original whole lift. It does not resolve the auxiliary character factor, prime correlations, or the original signed difference.

For the actual phase example \((a,b)=(712,486)\), the replay checks all seven phase classes in the compatible grid, the fibre separation, and the precise one-digit refinement.

~~~python
a,b=712,486
r=(pow(3,a+4,49)+pow(5,b+2,49)+7)%49
u=-r*pow(45,-1,49)%49
phases={((c-a)//4%21,(e-b-2)//6%7)
        for c in range((a+9)//10,a//3+1) if (c-a)%4==0
        for e in range((b+4)//5,b//3+1) if (e-b-2)%6==0
        if (pow(3,c,49)+pow(5,e,49))%49==r}
assert (r,u,len(phases))==(27,19,7)
def exponent(x): return ((pow(x,6,49)-1)//7)%7
units=[x for x in range(1,49) if x%7]
assert all(exponent(x*y)==(exponent(x)+exponent(y))%7
           for x in units for y in units)
assert all({exponent(j+7*i) for i in range(7)}==set(range(7))
           for j in range(1,7))
assert 49*(u%7)==245 and 49*u==931
~~~
