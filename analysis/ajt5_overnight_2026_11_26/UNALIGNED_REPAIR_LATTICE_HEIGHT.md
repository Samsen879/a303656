# Unaligned affine repair lattices and ordinary exponent height

A short lattice basis can certify a small representative that survives both higher-reader deletions and the exact valuation-two tests. Merely ruling out local slopes ±1 does not certify height; an actual short dual character can still obstruct the full ordinary index box.

## Reduced-basis box

Let the tested repair primes \(p\) be odd, with squarefree product \(P\), and use \(c=c_0+Au,d=d_0+Bv\). Assume both increments preserve the native readings modulo \(p\), their first lifting digits are ordinary and free, and the target collides at each \(p\). The joint residue-zero conditions modulo \(p^2\) give one coset of a lattice \(L=\{(u,v):v-su\equiv0\pmod P\}\). Assume the higher-reader exclusions are covered by at most \(b_p\) forbidden classes of \(u\) modulo \(p\) at each source. Set \(d_p=1\) if \(n\equiv0\pmod p\) and \(d_p=2\) otherwise.

For a basis \(w_1,w_2\) of \(L\), write \(W_i=|(w_1)_i|+|(w_2)_i|\) for each coordinate. If
\[
\sum_{p\mid P}(b_p+d_p)\lceil K/p\rceil<K,
\]
there is a surviving repair with exact valuation two at every source and \(0\le u\le KW_u,\;0\le v\le KW_v\).

To put a \(K\)-by-\(K\) basis-step block inside the box, choose its initial coset point using the centered fundamental parallelogram around the box center minus \((K-1)(w_1+w_2)/2\). For each coordinate the sum of the centering error and block radius is at most \(KW_i/2\). At least one basis direction has unit first coordinate modulo each \(p\), since \(L\) projects onto every first coordinate. Thus each forbidden class deletes at most \(K\lceil K/p\rceil\) points.

Write the nonzero first reading digits as \(\alpha=(3^A-1)/p\bmod p,\beta=(5^B-1)/p\bmod p\), and put \(r=3^{c_0},t=5^{d_0}\bmod p\). After dividing the repaired remainder by \(p^2\), its residue modulo \(p\) is quadratic in the step indices. Along a direction \((h,j)\), the quadratic coefficient up to sign is \((r(\alpha h)^2+t(\beta j)^2)/2=r(r+t)(\alpha h)^2/(2t)\), using the first-digit relation. For \(r+t\ne0\), a direction with unit first coordinate gives at most two roots per parallel line. For \(r+t=0\), the quadratic part vanishes identically; the affine polynomial is nonconstant because the lattice step \((P,0)\) changes the divided remainder by a nonzero residue. Some basis direction then gives at most one root per line. Union bounding the deletion counts proves the claim.

## Actual controls

* Positive: with strides 522, offsets (99,0), the repair line is \(27u+v\equiv380\pmod{413}\), with basis (15,8), (16,−19). The actual higher readers 43 and 1063 each delete only their source class \(u=0\). Here \(d_7=1,d_{59}=2\), so \(K=6\) suffices. At the pinned target (29,10) lies in the ordinary quarter-height box and passes all four tests. At the same target (14,2) has both exact native valuations but fails the higher reader 43.
* Negative: with strides 174, offsets (96,68), the line is \(u+4v\equiv412\pmod{413}\). Local slopes are 5 modulo 7 and 44 modulo 59, neither ±1. The actual quarter-height box \(u\le110,v\le75\) has \(u+4v\le410\), so no pair in this chart can repair both native primes. The pair (80,83) repairs both to exact valuation two outside the box.

The theorem is conditional on the stipulated deletion structure and lattice basis. The positive control certifies its listed local panel only, not a complete two-square test. The negative control excludes one anchored chart, not other exponent phases.

```python
R = (7, 59)

def off(A,c,d,m,u,v):
    return (pow(3,c+A*u,m) + pow(5,d+A*v,m)) % m

def coeff(A,g,c,p):
    return ((pow(g,A,p*p)-1)//p)*pow(g,c,p) % p

def exact(n,A,c,d,u,v):
    return all((z := (n-off(A,c,d,p**3,u,v)) % p**3)
               and z%p**2 == 0 for p in R)

A,c,d = 522,99,0
n = 33665234458065 + 4*38639644414476*3**(c+A*29)
f = lambda m,u,v: off(A,c,d,m,u,v)
for p,q in [(7,43),(59,1063)]:
    assert pow(3,A,p) == pow(5,A,p) == 1
    a,b = coeff(A,3,c,p),coeff(A,5,d,p)
    assert b and a == 27*b%p
    assert (n-f(p*p,0,0))%p**2 == p*b*380%p**2
    assert all(pow(g,A,q)!=1 and pow(g,A*p,q)==1 for g in (3,5))
    assert [x for x in range(p) if (n-f(q,x,(380-27*x)%p))%q==0] == [0]
assert (n%7,n%59) == (0,29)
assert (f(343,0,380)-f(343,15,388))%343 == 2*49
assert exact(n,A,c,d,14,2) and (n-f(43,14,2))%43 == 0
assert exact(n,A,c,d,29,10) and all((n-f(q,29,10))%q for q in (43,1063))
assert 4*max(3**(c+A*29),5**(d+A*10)) <= n

A,c,d = 174,96,68
n = 830088327 + 4*845339964*5**(d+A*75)
for p in R:
    assert pow(3,A,p) == pow(5,A,p) == 1
    a,b = coeff(A,3,c,p),coeff(A,5,d,p)
    assert a and b == 4*a%p
    assert (n-off(A,c,d,p*p,0,0))%p**2 == p*a*412%p**2
assert 3**(c+A*110) <= n//4 < 3**(c+A*111)
assert 5**(d+A*75) <= n//4 < 5**(d+A*76)
assert 110+4*75 < 412 and exact(n,A,c,d,80,83)
```
