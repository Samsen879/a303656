# Exact common divisor and an \(O(W)\) saving in the \(q=1\) square-modulus slice

Keep the middle ranges of [the dual-coordinate gate](MOVING_SQUARE_DUAL_COORDINATE_GATE.md) and specialize to \(q=1\). Let \(m=p^2\), \(p\nmid2hk\), and \(W=B/H\). The middle range fixes \(u=-1\), hence \(j=2h-m\). Write \(\ell=2k-mV\), \(P=h^2+k^2\), \(F=\gamma-2\delta\), and assume the necessary conditions \(h,k,V\) odd, \(\gcd(h,k)=1\) and \(m\mid 2P-F\).

Define \(d=k-hV\) and
\[
 Z=-\frac{Pj(j-h)+hj\delta-h^2\gamma}{2m}.
\]
This is an integer: its numerator vanishes mod \(m\) since \(j\equiv2h\bmod m\), and it is even by the parity assumptions and even shifts. The determinant is \(D=kj-h\ell=-md\). The vertical numerator is \(N_b=j(\delta-P)+h(j^2+\ell^2-\gamma)\). Direct expansion gives \(hN_b=-2mZ-2kjD+D^2\). Since \(D\) is even and \(\gcd(h,2D)=1\) (use \(j\equiv-m\bmod h\)), \(2D\mid N_b\) is equivalent to \(d\mid Z\). This also forces the first coordinate integral by the previous dual-coordinate gate, or by the first line and \(\gcd(h,2D)=1\). No coprimality of \(d\) with \(m\) is needed.

For fixed \(p,h,k\) and shifts, \(Z\) is fixed. In this middle range \(d=hk(\beta-\alpha)/m\) gives \(B/1500\le d\ll B\). Distinct surviving \(d_i\) are coprime to \(h\), so \(\gcd(d_i,d_j)\mid |V_i-V_j|\), and this difference is \(O(W)\). Four such divisors would force \(\operatorname{lcm}(d_1,d_2,d_3,d_4)\gg B^4/W^6\). But the original shift box and these size bands give \(0<Z\ll HB^2\) uniformly for sufficiently large \(X\): the \(Pj(h-j)\) term has size \(\asymp B^2H^2\), dominates the shift terms of size \(O(X^{1/3}H^2)\), and \(m\asymp H\). The lcm contradicts its divisibility into \(Z\), since \(H/W^4\) tends to infinity. Thus each fixed triple \((p,h,k)\) has at most three passing directions. For each \(p,h\), the original square modulus leaves at most two unit \(k\)-classes by the simple-root lift, and at most \(O(W)\) integers \(k\) in the marked interval per class. Counting \(O(\sqrt H)\) primes and \(O(H)\) possible \(h\) gives \(O_C(H^{3/2}W)\) directions for each specified shift triple. This is an upper bound for the slice, not existence at arbitrary height.

Exact control and a counterexample to \(d\mid mZ\) as a substitute:

~~~python
m = 289
cases = [
    ((163,634621,37,159193), (177148,1594348,177172), 8538, 3248443476738, 0),
    ((159,591605,29,117667), (177148,177152,1594324), 5372, 2282787166636, 5056),
]
for (h,k,j,l), (s0,s1,s2), d0,z0,remainder in cases:
    P,D = h*h+k*k,k*j-h*l
    delta,gamma = s0-s1,s0-s2
    assert (2*P-gamma+2*delta)%m == 0
    d = -D//m
    num = -(P*j*(j-h)+h*j*delta-h*h*gamma)
    assert num%(2*m) == 0
    z = num//(2*m)
    assert (d,z,z%d) == (d0,z0,remainder)
    assert m*z%d == 0
~~~
