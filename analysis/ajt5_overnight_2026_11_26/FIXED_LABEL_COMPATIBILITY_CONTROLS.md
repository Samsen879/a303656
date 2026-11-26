# One fixed shared label is necessary for a local-to-global inference

Local compatibility at each prime does not let us select a different edge at each prime. An explicit counterexample arises in the class m≡1 mod 6, with r=0, parent exponents (d,c)=(0,1), and child exponents (e,f)=(1,1) or (1,0). Both edges have parent residual m−4. The respective child residuals are 5m−8 and 5m−6.

* At 2, the first edge passes at m=13: 9 and 57 are odd units congruent to 1 mod 4. The second edge never passes for odd m, since its two odd residuals require m≡1 and m≡3 mod 4, respectively.
* At 3, the second edge passes at m=13: 9 has valuation 2 and 59 is a unit. The first edge never passes for m≡1 mod 3, since simultaneous even valuations (or zeros) require m≡4 and m≡7 mod 9, respectively.

At m=13 all residuals in both edges are positive. Nevertheless neither edge is a genuine bridge at any integer in this progression. Thus the quantifier must be “there is a label that passes at every prime,” not “at each prime there is a label that passes.” A cross-prime label-selection obstruction cannot use a modulus with only one prime divisor; 6 is the smallest possible modulus for such an obstruction.

A separate positive control gives a fixed-label genuine high-precision bridge with a negative initial representative:
```python
s = 3**101
t = 2**91 * s * 5**63
A, B = 1+s*s, 5+s*s
N = 2**181 * 3**201 * 5**127
m0, m = A-N, A+5*t*t
assert m0 < 0 and (m-m0) % N == 0 and m.bit_length() == 798
assert m-A == t*t+(2*t)**2 > 0
assert 5*m-B == (2*s)**2+(5*t)**2 > 0
```
The positive control uses (d,c;e,f)=(0,202;1,202), r=0. Neither example certifies a general height bound or the original conjecture.
