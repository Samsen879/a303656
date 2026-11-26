# A two-candidate norm test for power differences in imaginary quadratic fields

Let $\Delta<0$ be a fundamental discriminant of class number one. For an integer $b>1$ with $b\equiv1\bmod|\Delta|$, we give an existence test for whether any $b^n-1$, $n\ge1$, is an integral norm from the maximal order. Write $L_0$ for the product of odd inert primes with odd valuation in $b-1$.

- If $2$ is not inert, test $n=L_0$ only.
- If $2$ is inert and $b$ is even, again test $L_0$ only; no even exponent works.
- If $2$ is inert and $b$ is odd, the odd branch is impossible when $v_2(b-1)$ is odd, and otherwise its only required test is $L_0$. The even branch has one candidate $2^jL_0$, where $j\in\{1,2\}$ uniquely makes $v_2(b-1)+v_2(b+1)+j-1$ even.

A branch has a solution precisely when its candidate is a norm; passing candidates are the respective minimal exponents. This classifies existence and branch minima, not all multiples of a good seed.

In class number one, a positive integer is an integral norm exactly when its inert valuations are even: a split or ramified prime has a principal prime ideal of norm that prime, and any even power of an inert prime is the norm of a rational integer. At an odd inert prime dividing $b-1$, lifting the exponent gives $v_p(b^n-1)=v_p(b-1)+v_p(n)$. This forces $L_0\mid n$ and gives the correct parity at those primes for the seed. The listed conditions at 2 follow from the usual dyadic valuation formula, apart from the prohibition on a dyadic factor of $n$ when $b$ is even and 2 is inert.

Here is the obstruction that supplies that prohibition and handles all other primes. For an inert $p\nmid b-1$, the factor $\Phi_p(b)=1+b+\cdots+b^{p-1}$ is congruent to $p\bmod|\Delta|$, so the quadratic character of this factor is $-1$. It is coprime to the discriminant and has an inert prime $q$ to odd valuation. The prime $q$ cannot divide $b-1$: otherwise $\Phi_p(b)\equiv p\bmod q$, forcing $q=p$, which is impossible because $\Phi_p(b)\equiv1\bmod p$ when $b\not\equiv1\bmod p$. Thus the order of $b\bmod q$ is $p$, giving $q>p$ and $v_q(b^p-1)$ odd. If a successful $n$ were divisible by $p$, lifting at the odd prime $q$ would force $q\mid n$. Iteration contradicts finiteness of the prime divisors of $n$. The initial step also works at $p=2$ when $b$ is even, since $\Phi_2(b)=b+1$ is odd.

All successful exponents in a given branch are multiples of its candidate. If the candidate has an odd inert valuation, the obstructing prime must be odd and outside $b-1$, because the base-prime and dyadic parities were already imposed. This valuation cannot change parity when lifted from the candidate to a successful multiple: that multiple cannot contain the obstructing prime, by the increasing-prime argument. This proves the test.

Controls: for the Eisenstein form $x^2+xy+y^2$, base 7 succeeds only in the even branch, starting with $48=4^2+4\cdot4+4^2$. Base 13 has the odd seed $12=2^2+2\cdot2+2^2$ and no even solution: the even seed $13^4-1=2^4\cdot3\cdot5\cdot7\cdot17$ has odd valuations at inert primes 5 and 17. In discriminant $-7$, base 22 has minimal exponent 3: $22^3-1=7\cdot39^2$ is the norm of $39\sqrt{-7}$, and the odd inert prime 3 forces $3\mid n$. These examples contrast inequivalent dyadic branches and a different norm field. No generalization to nonprincipal orders or conclusion about A303656 is asserted.
