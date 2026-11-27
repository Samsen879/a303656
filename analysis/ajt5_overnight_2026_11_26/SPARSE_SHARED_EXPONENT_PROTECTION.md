# A sparse shared-exponent protection lemma

This is a structured local result, with no priority claim. Fix an integer m ≡ 2 (mod 11). The probability space is the common periodic exponent pair (c,d), conditioned on 5|c,d. Below, all conditions on q concern divisibility modulo q, and only the indicated 11-adic tests need higher powers. The estimates for arbitrary odd-valuation blocking follow by inclusion in the divisibility events, without assuming independence of primes or different rows.

An offset pair (u,w) gives old residual m−3^(c+u)−5^(d+w+10), and new residuals m−3^(c+u)−5^(d+w) and 5m−3^(c+u)−5^(d+w). Initially take U=(220i), V=(1210i), 0≤i<8.

Let A say the central old residual has v11=1, and B say the central new parent has v11=2. Every offset that is respectively a multiple of 220 and 1210 preserves both tests. All new child residuals are 11-adic units. Given c and uniform d in the 5-multiple class, P(A)=10/11, P(B)=10/121, and B⊂A. Moreover, if A fails, some old residual in the initial 8×8 core has valuation exactly 4: conditional on c, the old divisibility tests concern Y=5^(d+10). Their roots in Y are (m−3^(c+u))5^(−w). After translating by m−3^c and dividing by 11³, these roots occupy at least two classes mod 121 above every class mod 11. Thus if Y meets their common residue mod 11³, some root difference has valuation exactly 4. The root test can use c=0: modulo 11⁵, the offsets satisfy 3^u≡1 mod 11³, so multiplying their deviations by 3^c≡1 mod 11 affects the tests only by a bijection within the child classes. More explicitly, writing a=3^c and b=5^(−w), the normalized roots are a(1−3^u b)/11³ + m(b−1)/11³, hence a times the c=0 calculation with m replaced by m/a≡2 mod 11. Both normalized terms depend on m/a only mod 121. These finite facts can be checked by:

```python
L = 11**5
for m in range(2, 121, 11):
    values = [((m-pow(3,220*i,L))*pow(5,-1210*j,L)-(m-1)) % L
              for i in range(8) for j in range(8)]
    assert all(v % 1331 == 0 for v in values)
    R = {v//1331 for v in values}
    assert all(sum(z % 11 == b for z in R) >= 2 for b in range(11))
Y = {pow(5,5*j,1331) for j in range(121)}
for x in {pow(3,5*i,1331) for i in range(11)}:
    A = {y for y in Y if (2-x-y*5**10) % 121}
    B = {y for y in Y if (2-x-y) % 121 == 0 and (2-x-y) % 1331}
    assert (len(Y), len(A), len(B), B <= A) == (121,110,10,True)
assert pow(3,220,1331) == pow(5,1210,1331) == pow(5,605,1331) == 1
```

Now choose distinct primes q_k ≡ 3 (mod 4), q_k>5 and q_k≠11, with o_k=ord_{q_k}(5^605)≥4·2^k(k+7)^2, k≥1. A prime with order bounded by L divides the fixed product of the integers 5^(605j)−1 for 1≤j≤L, and there are infinitely many primes 3 mod 4. At step k, append one offset to each list, preserving strict increase and its required divisibility by 220 or 1210, and divisible by every q_j−1 for j≤k. For q_k, all offsets appended at step k or later are indistinguishable from the zero offset. Each coordinate thus has at most k+7 factors modulo q_k in any final window.

Hold c and d mod 605 fixed. These fibers fix A and B. As d varies along the fiber, 5^d runs over a genuine orbit of size o_k; no independence from the other primes is asserted. Any offset-factor pair and one fixed endpoint can contact q_k on at most one orbit value, since its coefficient of 5^d is nonzero mod q_k. Union bounds summed over k cost at most 1/4 for the old rows and 1/2 for the two new endpoints together. These bounds hold for every fiber, including the fibers picked by A or B.

Let E be the event that each old row has a finite odd valuation at some prime in {11}∪Q, possibly a different prime for each row; let S be the event that all new residuals pass the selected primes. Within A all old rows are blocked by 11. Outside A at least one is not blocked by 11, so E then needs at least one q-contact. On B, S holds if the new residuals avoid all q-contacts. Therefore P(E)≤10/11+1/44 and P(E∩S)≥(10/121)/2, yielding **P(S|E)≥20/451** for every finite prefix. The q_k need not divide m; one can even force finite odd valuation at every q_k on the same center (c,d)=(0,0), by imposing m≡2+q_k mod q_k² and m≡123 mod 1331. The latter class has B on the same center before imposing q_k. The positive survival fraction gives another exponent pair within c=0, d≡0 mod 605 for that fixed finite panel. Taking a representative and then lifting m in the combined congruence class makes all residuals strictly positive. Use the common period including q_k² if preserving the separate odd-valuation witness.

This argument uses sparse chosen primes and freely enlarged offsets; the estimates are over whole periods. It gives no short-exponent guarantee for a prescribed m, no control of unselected primes, and no bound on the fraction of m represented in the original problem.
