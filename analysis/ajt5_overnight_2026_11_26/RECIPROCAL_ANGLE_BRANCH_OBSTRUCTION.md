# A whole-circle obstruction to the reciprocal angle branch

On the genuine labels (d,c;e,f)=(24u+10,8u+4;24u+11,8u+5), write A=5^d+3^c−131779 and B=(5^e+3^f−658897)/5. For u≡23 mod 1155, A≡31 and B≡44 mod 121. Thus v_11(B)=1 and −A is the nonsquare 2 mod 11.

For the reciprocal branch take any admissible rational h, L=4A−2B, R=(h+L/h)/2, Y0=(h−L/h)/2, r=B/R, X0=r, and S=r+R. The initial circle has X0²+Y0²=S²−4A. With ell=S+X0, the half-angle [a:b] gives
```
mu = (S-X)/(2r) = ((ell*a+Y0*b)^2+4*A*b^2)/(2*r*ell*(a^2+b^2))
2*r*ell = 2*B*(Y0^2+4*A)/R^2 .
```
The first equality follows by completing the numerator's square using the circle equation; the second uses R²−Y0²=L. Since −A is nonsquare in the residue field, the quadratic form in the numerator has even valuation at 11. The same holds for Y0²+4A, and for a²+b² since −1 is nonsquare. The factor B contributes odd valuation, hence **mu has odd valuation at 11 for every angle**. It cannot satisfy the joint-square-cover condition in JOINT_SQUARE_ANGLE_COVER.md. This is a uniform exclusion over this whole reciprocal branch, not over all choices of r or all quartic trajectories.

The nonreciprocal branch r=R, X0=B/r has an easy rational seed to the norm condition: mu=1/2 at half-angle zero, represented by (1/2)²+(1/2)². This observation alone does not guarantee that the fixed exceptional primes pass or that a global integer anchor exists.

```python
M,u,S=121,23,1155
A=(pow(5,24*u+10,M)+pow(3,8*u+4,M)-131779)%M
B=((pow(5,24*u+11,M)+pow(3,8*u+5,M)-658897)*pow(5,-1,M))%M
assert (A,B)==(31,44)
assert pow(5,24*S,M)==pow(3,8*S,M)==1
assert pow((-A)%11,5,11)==10
```
