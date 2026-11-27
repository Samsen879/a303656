# Fresh split-prime obstructions along actual cubing branch ratios

This follows [the native-prime quadratic matching test](https://github.com/Samsen879/a303656/commit/3b13b7cac8ea3366b3b40bf7a81729333334e226). The new primes are *split* in the quadratic norm field. They obstruct squarehood of the rational resultant of a formal map, not the true Eisenstein-norm admissibility of the specialized integer family. Indeed the native shells at \(d=17,289\) are already true integer norms, and cubing only supplies split primes. No independent non-cubing multiplier follows.

The principal-unit tests at 3 and 5 use different dominant squares: at 3 the branch \(v_k\) itself is a rational square with even negative valuation, and at 5 the square of the target root dominates the product. At 2 the odd-order root reduces to a value different from 1, so the imposed native congruence mod 8 is sufficient. At 7 we check the residue-field norm character explicitly. All displayed finite residue cases, congruences and the two lowest-layer witnesses were independently replayed.

**Actual cubing gives an infinite family that passes every native-prime check and still fails the quadratic pullback.** For \(d=17\) or \(289\), take the second branch
\[
v_k=(5/3)^{3^k-1}.
\]
On an explicit infinite subsequence of \(k\), the branch passes at all primes dividing the native shells and at \(2,3,5,7,17\). Both signed numerator shells at \(v_k\) are genuine integer norms \(x^2+3y^2\). Yet each cubing layer supplies a new odd-valuation prime in **each** sign, so the formal simultaneous square condition fails.

### One new prime per sign per layer

Write \(H_\pm(r)=\Phi_d(5^r,\mp3^r)\) in homogeneous notation. The cyclotomic composition identity gives
\[
H_\pm(3^k)=H_\pm(1)\prod_{j=1}^k C_j^\pm,
\qquad C_j^\pm=\Phi_{3^j d}(5,\mp3).
\]
Every prime factor of \(C_j^\pm\) is primitive. The primes \(2,3,5,17\) are excluded by the shell quotient. In particular, \(5/3\bmod17\) has order \(4\), so neither signed ratio can have the required odd order there. At every other prime the cyclotomic roots have exact order \(3^j d\) for the minus sign and \(2\cdot3^j d\) for the plus sign. Thus these primes split in \(\mathbb Q(\sqrt{-3})\), and the supports are disjoint across signs, layers, and the native shells.

Each \(C_j^\pm\) has an odd-valuation prime, as follows from three fixed residue identities.

- **Minus, every \(j\ge1\).** Modulo \(11\), \(5/3\) has order \(5\). With \(e=17^{a-1}3^k\), \(d=17^a\), and \(t=(5/3)^e\), the shell \(H_-(3^k)\) has the square class of \(1+t\), since \(17\equiv2\bmod5\). On advancing one cube, \(t\) moves to \(t^3\). The identity \((1+t)(1+t^3)=-t^2\) makes the quotient a nonsquare modulo \(11\).
- **Plus, every \(j\ge2\).** Modulo \(31\), \(5/3\) has order \(30\). For \(k\ge1\), \(z=-(5/3)^e\) has order \(5\). The plus shell has the square class of \(1+z\), and the same identity gives a nonsquare quotient modulo \(31\).
- **Plus, the first cube.** Modulo \(19\), \(5/3\) has order \(6\). In the native shell, seventeenth powering inverts the base units, so \(H_+(1)\) has the square class of \(15\), a nonsquare. After cubing, the base ratio is \(-1\), so \(H_+(3)\) has the square class of \(17\), a square. Their quotient is a nonsquare.

This proves at least \(2k\) distinct prospective witnesses at \(v_k\). A witness from the last layer is at least \(2d\,3^k+1\), so the witnesses grow with the branch itself.

### The native checks can all be retained

Put \(M=H_-(1)H_+(1)\) and \(\rho=5/3\). At a native prime \(p\mid M\), the order of \(\rho\bmod p\) divides \(2d\). Therefore \(\rho^{4dM^2}\equiv1\bmod17M^2\). Since \(3\nmid4dM^2\), there are infinitely many even \(k\) with \(3^k\equiv1\bmod4dM^2\). On that subsequence, \(v_k\equiv1\bmod17M^2\).

For the quadratic map \(f_v(T)=(1+3vT^2)/(1+3T^2)\), the discriminant quotient at a target root \(u\) is \(4(u-1)(u-v)\). At every native prime, \((u-v_k)/(u-1)\) is a principal unit, hence a square. The same holds at \(17\) and at \(2\), using \(v_k\equiv1\bmod8\) at \(2\). At \(3\) and \(5\), factoring out the dominant square leaves principal units. At \(7\), the minus and plus products of the native and lifted shell residues are \(4\) and \(1\). The residue degree at \(7\) is \(\varphi(d)\), so these rational residue norms certify both local squares.

The new primes still obstruct the **formal** map. The absolute norm of \(4(u-1)(u-v_k)\) is \(H_\pm(1)H_\pm(3^k)\) times a rational square. A new odd valuation makes this a nonsquare in \(\mathbb Q\). Meanwhile the actual integer \(H_\pm(3^k)\) remains a norm, because the native shell is a norm and every new prime splits in \(\mathbb Q(\sqrt{-3})\).

For an exact \(d=17\) control, the first new minus factor has valuation one at \(103\), and the first new plus factor has valuation one at \(3571\). Both are split and absent from the native shells. A certified choice is any positive multiple of \(k=151966159571027760\). The replay checks the native congruences by modular exponentiation, without expanding the branch.

```python
def H(r,s):
    return (5**(17*r)+s*3**(17*r))//(5**r+s*3**r)

M = H(1,-1)*H(1,1)
E, R, k = 68*M, 17*M*M, 151966159571027760
assert pow(3,k,E) == pow(5*pow(3,-1,R)%R,E,R) == 1
for s,p,c in [(-1,103,36), (1,3571,1447)]:
    assert M%p
    assert (H(3,s)//H(1,s))%(p*p) == c*p
```



```python
from math import isqrt
def P(e,s,p):
    a,b=pow(5,e,p),pow(-s*3,e,p)
    return sum(pow(a,16-j,p)*pow(b,j,p) for j in range(17))%p
def qchar(x,p):
    return pow(x,(p-1)//2,p)
assert all(qchar(P(e,-1,11)*P(3*e,-1,11),11)==10 for e in range(1,5))
assert all(qchar(P(e,1,31)*P(3*e,1,31),31)==30 for e in (3,9,21,27))
assert all([qchar(P(e,1,19),19),qchar(P(3*e,1,19),19)]==[18,1]
           for e in (1,17))
assert all([P(e,s,7)*P(3*e,s,7)%7 for s in (-1,1)]==[4,1] for e in (1,5))
for p in (103,3571):
    assert p%3==1 and all(p%j for j in range(2,isqrt(p)+1))
```
