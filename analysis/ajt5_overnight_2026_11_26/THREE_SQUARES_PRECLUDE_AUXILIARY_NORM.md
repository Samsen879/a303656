# Three synchronized squares preclude an auxiliary second norm

Consider either of the patterns \(P=(0,2,4,3),(2,4,3,0)\) from [the shared-height reduction](ALL_DISTINCT_SHARED_MATCHING.md). Let \(A=3^a,\ B=5^b\) with \(a,b\ge0\), and index the shifts by \(T_{P_i}=9^iA+5^{P_i}B\). Assume \(K-T_d\) are integer squares for \(d=2,3,4\). Then the auxiliary second norm in [the prime criterion](SECOND_GAUSSIAN_REPRESENTATION_CRITERION.md) cannot occur.

The shifts at offsets \(2,4\) each differ by \(4\bmod8\) from the shift at offset \(3\). Hence the three square roots are even; call their halves \(R,h,Y\). The exact differences are
\[
 R^2-h^2=\gamma A+25B,\qquad Y^2-h^2=\eta A-125B,\qquad
 (\gamma,\eta)=(180,162)\text{ or }(20,18).
\]
The finite congruences modulo \(32\), then modulo \(9\), force \(a\) and \(b\) even, respectively (replay below). As \(A,B\equiv1\bmod8\), the first difference forces \(h^2\equiv4\bmod8\), so \(h\equiv2\bmod4\). The shifts \(T_3,T_4\) reduce to \(1,4\bmod5\) in some order, and their translated square sets intersect only at \(K\equiv0\bmod5\). Thus \(5\nmid h\).

Put \(C=5^{b/2+1}\) and \(Z=6\cdot3^{a/2}\) or \(2\cdot3^{a/2}\), according to the pattern. The very same integer
\[
 N=h^2+C^2=R^2-5Z^2
\]
is a primitive Gaussian norm. Every prime factor is \(1\bmod4\), is not \(5\), and is prime to \(Z\), whose support is contained in \(\{2,3\}\). The second identity makes \(5\) a square modulo each such prime, hence all are \(1,9\bmod20\). The prime criterion now excludes an auxiliary representation \(N=L^2+25k^2,\ L\equiv C\bmod16,\ k\equiv2\bmod4\). Thus an obstruction that required such an auxiliary representation does not reach genuinely synchronized candidates of this type. The existence of a fourth square is still open in the specified growing height band.

~~~python
from math import isqrt
P = ((0,2,4,3), (2,4,3,0))
def rows(p,a,b):
    return {d: 3**(a+2*i)+5**(b+d) for i,d in enumerate(p)}
for p in P:
    # First determine a even mod 32 (3 and 5 have periods dividing 8).
    for modulus,aa,bb in ((32,range(8),range(8)), (9,(0,2),range(6))):
        # In the second pass, a is already even. Mod 9, all a >= 2
        # give the same 3-powers as a=2.
        sq = {x*x % modulus for x in range(modulus)}
        for a in aa:
            for b in bb:
                T = rows(p,a,b)
                for K in range(modulus):
                    if all((K-T[d])%modulus in sq for d in (2,3,4)):
                        assert (a if modulus==32 else b)%2==0
T = rows(P[0],2,0)
assert [6830-T[d] for d in (3,2,4,0)] == [12**2,82**2,74**2,6820]
assert isqrt(6820)**2 != 6820
assert 6**2+5**2 == 41**2-5*18**2 == 61
T = rows(P[1],1,2)
assert [20792-T[d] for d in (3,2,4)] == [132**2,142**2,5140]
assert 66**2+25**2 == 17*293 == 9**2+25*14**2
~~~

The controls are outside the balanced growing band. The first synchronizes three squares only; the second illustrates that the excluded auxiliary norm can occur when only two squares synchronize.
