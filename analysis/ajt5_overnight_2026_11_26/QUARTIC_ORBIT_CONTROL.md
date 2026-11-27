# A quartic control for the two-norm trajectory problem

The mod-8 shift pattern (A,B)≡(7,3) does not prohibit quartic norm identities. On the genuine exponent edge (d,c;e,f)=(14,2;15,3), take A=5^d+3^c−131779 and B=(5^e+3^f−658897)/5. They are positive integers with A=B+4. The actual residuals are w²−A and 5(w²−B), where w=5j+1821.

More generally put b=a+4, M=(b−3)/2, H=2M, and
```
N = (t²+2)²+M²+a
R = (t²−M)²−t²−b(1−t²)
I = 2t(t²−M+b).
```
For W=N/H, the identities are W²−a=(W−M)²+(t²+2)² and W²−b=(R/H)²+(I/H)². Both follow by expansion (the following checks each polynomial after clearing denominators at nine points, more than its degree). Set a=B, b=A and take t≡505240047 mod 5H. Then w=−W is integral and is 1 mod 5, so yields an integral j. Its coordinates for both norms are integral; multiplying the second pair (the one for B) by the Gaussian integer 1+2i supplies the factor 5 in the child residual. All these congruences need only be checked at the initial residue because N,R,I are integer polynomials.

```python
A = 5**14 + 3**2 - 131779
V = 5**15 + 3**3 - 658897
B, rem = divmod(V, 5)
assert rem == 0 and (A%8,B%8,A-B) == (7,3,4)
M = (A-3)//2
H = 2*M
def forms(t):
    x = t*t-M
    return (t*t+2)**2+M*M+B, x*x-t*t-A*(1-t*t), 2*t*(x+A)
for t in range(9):
    N,R,I = forms(t)
    assert N*N-H*H*A == R*R+I*I
    assert N*N-H*H*B == (N-H*M)**2+(H*(t*t+2))**2
N,R,I = forms(505240047)
assert 5*H == 30516919260
assert N%(5*H) == 4*H and R%H == I%H == 0
```

For this fixed edge there are order X^(1/4) distinct j in |j|≤X for all sufficiently large X by the growth of the quartic, not a positive-density set. The edge is outside the original restricted quadratic-obstruction subtables. This control addresses extrapolation from their residue pattern alone, not the existence of quartic trajectories within those subtables or the critical first moment. No novelty claim is made.
