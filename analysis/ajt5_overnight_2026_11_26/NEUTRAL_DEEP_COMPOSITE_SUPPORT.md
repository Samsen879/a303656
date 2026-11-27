# Exact composite-support tests for the neutral deep chart

These are representative certificates supplementing the [necessary finite reduction](https://github.com/Samsen879/a303656/commit/127f12218184d3880aa8f0ac1da0a643c4c1a9f2). They do not give an exhaustive partition of all the resultants.

For any eligible inert prime \(q\equiv687\bmod1372\), \(7\) is coprime to \(q+1\). In \(\mathbb F_{q^2}\), the ratio \(\theta=(2+i)/(2-i)\) belongs to the norm-one group of order \(q+1\). The imaginary part of \((2+i)^m\) vanishes precisely when \(\theta^m=1\); both \(2+i\) and its conjugate are units since \(q\ne5\). Hence, if the imaginary part vanishes after the \(343\)-power, it had to vanish before. On an entire composite component one can test the after condition by congruence and disprove the before condition at every prime divisor by a single gcd. This rules out every eligible prime support of \(20742644645455372414347049\) in the example below, without factoring it. The same Gaussian arithmetic can split a component by a gcd even if it does not rule it out outright.

For the ordinary multiplicative part, a 7-free mask \(L\) and \(3^{49L}=1\bmod p\) exclude exact 7-primary order 343 at that prime. Repeated gcd and exact division remove all copies rather than assuming squarefree input. Conversely, an exact 7-primary order of 343 for each base does not require \(v_7(q-1)=3\). The actual prime 2693923 has \(q-1=7^4\cdot1122\). Raising to the full 7-free part 1122 gives order 343 for both bases; using \((q-1)/343\) instead gives order 49.

~~~python
from math import gcd, isqrt

def gp(z, e, m):
    def mul(a,b):
        x,y=a
        u,v=b
        return ((x*u-y*v)%m,(x*v+y*u)%m)
    a=(1,0)
    while e:
        if e & 1:
            a=mul(a,z)
        z=mul(z,z)
        e//=2
    return a

R,L=20742644645455372414347049,60474182639811581382936
z=gp((2,1),L,R)
assert z==(11044710378365824772402509,15704354568277709751191947)
assert gcd(z[1],R)==1 and gp(z,343,R)==(1,0)

W=10592185593611726147
assert W==312896263*33852068069
assert gcd(W,gp((2,1),312896264,W)[1])==312896263
# At a cutoff of 4*10**9, any remaining eligible q in the second
# factor would have a complementary divisor at most 8, but congruent to 687.
D=33852068069
assert D//(4*10**9)==8 and D*pow(687,-1,1372)%1372==687

p=56365634482019
H=179078397768493558513103039634424612012859
L=522094454135549733274352885231558635606
assert H==p**3 and L%7
for _ in range(3):
    t=gcd(H,pow(3,49*L,H)-1)
    assert t==p
    H//=t
assert H==1

q=2693923
assert all(q%d for d in range(2,isqrt(q)+1))
assert q-1==7**4*1122 and q%1372==687
for b in (3,5):
    u,v=pow(b,1122,q),pow(b,(q-1)//343,q)
    assert pow(u,343,q)==1!=pow(u,49,q)
    assert pow(v,49,q)==1!=pow(v,7,q)
~~~
