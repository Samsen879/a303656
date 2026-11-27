# Four all-distinct labels: exact edge gluing and a factor character test

Use the four surviving permutations in [the original height-band reduction](ALL_DISTINCT_SHARED_MATCHING.md). Let \(A=3^a\), \(B=5^b\) with \(a,b\) even and at least two. The shifts are \(9^i A+5^{p_i}B\). Sort the rows by the \(5\)-offsets \(0,2,3,4\), and denote the ordered shifts by \(S_0,\ldots,S_3\).

For a cyclic edge \((e,e+1)\) put \(D_e=(S_{e+1}-S_e)/4\). Its two even nonnegative roots have the form \(x_e=v+u,\ x_{e+1}=v-u\), with \(uv=D_e,\ v\ge |u|,\ u\equiv v\bmod2\). This gives the exact height key
\[
 K=\frac{S_e+S_{e+1}}2+u^2+v^2.
\]
For fixed \(A,B\), intersect the height keys of any opposite pair of edges, retaining the band's height restriction. This is equivalent to the four simultaneous square conditions, since each edge represents two disjoint rows at the same \(K\). The edges used here have nonzero difference: two equal shifts would equate a difference of powers of \(3\) of \(3\)-adic valuation at least \(a\ge2\) with a difference of powers of \(5\) at offset distance at most four, which has valuation at most one.

Two parity exclusions do not depend on the size cap once the corresponding shifts and even-root pattern have been fixed:

* For \(p=(4,3,0,2)\), necessarily \(a\equiv0\bmod4\).
* For \(p=(3,0,2,4)\), necessarily \(a\equiv2\bmod4\).

Indeed, put \(U=3^{a/2}, V=5^{b/2}\). The edge from offset \(2\) to offset \(3\) has \(D=5(5V^2-36U^2)\) in the first case and \(D=5(5V^2-4U^2)\) in the second. Its bracket is odd, prime to \(3,5\), and every prime \(q\) in it has \(5\) a quadratic residue. Quadratic reciprocity yields \(q\equiv\pm1\bmod5\). Exactly one half-factor is divisible by \(5\), so the other half-factor, even if negative, is a square class modulo \(5\). Their sum \(x_{25}\), the root of the offset-\(2\) row, is therefore in the square unit class. Meanwhile the four \(3\)-powers modulo \(5\) include both \(1\) and \(4\), and the corresponding shifted square sets intersect only at \(K\equiv0\bmod5\). Thus \(x_{25}\equiv\pm2\cdot27U\) in the first case and \(\pm2\cdot9U\) in the second. These give opposite restrictions on the parity of \(a/2\).

## Local checks need not detect the exclusion

For the first permutation and \((a,b)=(542,370)\) there is a height key passing the square-residue tests modulo \(256,27,25,49,11,13,17,19\) with \(v_3(K-125B)=2,\ v_5(K)=1\), even though \(a\equiv2\bmod4\) prohibits all exact lifts at these labels.

~~~python
A,B = 3**542, 5**370
S = [9**i*A + 5**d*B for i,d in enumerate((4,3,0,2))]
m, M, k0 = min(A,B), 391091500800, 35554989830
K = k0 + M*((max(S)+m-k0+M-1)//M)
assert 6*A < 7*B and 10*B < 11*A
assert max(S)+m <= K < max(S)+2*m and K < 3125*m
assert (K-125*B)%27 == 9 and K%25 == 5
for q in (256,27,25,49,11,13,17,19):
    assert all((K-s)%q in {x*x%q for x in range(q)} for s in S)
~~~

These obstructions concern specified shifts inside a shared-coordinate model. They do not supply any nonrepresentable \(n\) for the original conjecture.
