# Isolating the true origin in a growing active prefix

Let the fixed inert panel and the true-origin model \(n=2+u^2+v^2\) be as in [the proportional-box cover](PROPORTIONAL_BOX_EXTERNAL_COVER.md), including its fixed phase \(n\equiv0\pmod{p^2}\) at every panel prime p and \(u\equiv1,\ v\equiv0\pmod8\). Put \(z=\sqrt{\log X}\), \(R=\lfloor\sqrt{z/(8\log z)}\rfloor\). For every sufficiently large \(X\) there is an \(n\in[X,2X)\) for which every even-even cell \((c,d)=(2i,2j)\), \(0\le i,j<R\), other than \((0,0)\) has a bad valuation exactly one at an external prime \(q\in(z/2,z]\), \(q\equiv3\bmod4\). The origin is a true norm; it is the only true norm in this prefix. All its cells pass the fixed panel and the 2-adic square test.

For each non-origin cell let \(\delta=9^i+25^j-2>0\). It excludes at most \(\log\delta/\log(z/2)=O(R/\log z)\) primes in the upper half-window through divisibility. By the [prime number theorem for arithmetic progressions](https://books.google.com/books/about/Recherches_analytiques_sur_la_th%C3%A9orie_d.html?id=7e0GAAAAYAAJ), the upper half-window has \((1+o(1))z/(4\log z)\) inert primes. This exceeds \(R^2+O(R/\log z)\), so choose a different nondivisor for each cell greedily. At its assigned q a nonzero norm fiber represents \(\delta\) modulo q and lifts to some pair \((u,v)\bmod q^2\) of exact residual valuation one. The chosen classes are independent across the distinct primes. The CRT modulus, including panel and 2-adic conditions, still has logarithm \(O(z\log z)=o(\log X)\). As before, choose \(u=\sqrt X+O(M)\), \(0\le v<M\), to get the true-origin integer in the height band. The prefix is active for large X because \(\log(9^R+25^R)=O(R)=o(\log X)\).

Moreover this prefix claim and the original near-total external coverage of the full proportional box hold for the **same n**. First apply the average argument using only the lower half-window (cutoff \(z/2\)), which still gives the same \(O((\log\log X)^{-1/2})\) upper bound on the missed fraction. Keep those residues as the upper-half cells are assigned. Additional certificates cannot erase existing ones, and CRT still has the same height cost. Neither conclusion proves that the full proportional box has no second survivor or that the original conjecture fails.

## A finite phase interaction, separate from growing-window bounds

If 7 and 11 are not in the fixed panel, the legal phases \(n\equiv3\bmod49,\ n\equiv2\bmod121\) have respective exact-valuation-one hits 84 of \(21^2\) and 330 of \(55^2\) on the even-even index grid. These periods apply to both axes and are coprime. The joint miss fraction on complete periods is \((17/21)(49/55)=119/165\), strictly below the product \((1-a_7)(1-a_{11})=51035/65219\) of the two nonzero norm-fiber miss probabilities. This calculation is for just these two primes; it does not give a constant for the full expanding prime window.

~~~python
from fractions import Fraction as F
for q, period, phase, expected in [(7,21,3,84),(11,55,2,330)]:
    Q=q*q
    assert pow(9,period,Q)==pow(25,period,Q)==1
    assert any((2+u*u+v*v)%Q==phase for u in range(Q) for v in range(Q))
    hits=0
    for i in range(period):
        for j in range(period):
            a=phase-pow(9,i,Q)-pow(25,j,Q)
            hits += (a%q==0 and a%Q!=0)
    assert hits==expected
assert F(17,21)*F(49,55)==F(119,165)<F(51035,65219)
~~~
