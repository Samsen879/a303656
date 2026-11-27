# Target-adjusted eighteen-source bound and terminal capacity

The load and eighteen-source bounds apply to the **same divisor-minimal tail modulus**. Exact precision strengthens their combination in two ways. A common Wieferich row can absorb terminal load only if both bases already have enough intrinsic precision there. And a common row whose target valuation makes its rigid seed disappear on the selected slice must be counted **in addition to** the eighteen.

### The combined condition

Fix \(n>1\), a threshold \(A\), and a divisor-minimal modulus \(M\) excluding all square-sum residues \(n-3^c-5^d\) with \(c\ge A,\ d\ge0\). Assume \(A\ge v_3(M)\) and keep \(A\) fixed when reducing \(M\). For an inert prime \(r>3\), write \(e_r=v_r(M)\) and \(s_a(r)=v_r(a^{r-1}-1)\). Let \(\mathcal C\) be the primes with \(e_r,s_3(r),s_5(r)\ge2\). Define
\[
k_r=\min(e_r,s_5(r)),\qquad
Z=\{r\in\mathcal C:r\mid n,\ 
        v_r(n)\text{ is even or }v_r(n)\ge k_r\}.
\]
Then
\[
|\mathcal C\setminus Z|\ge18.
\]
Every \(r\in Z\) has \(e_r\ge4\) and requires a strictly larger reader on at least one base. Thus with the published cutoff \(C=970453984500000\),
\[
M\ \ge\ \prod_{r\in Z}r^4
          \prod_{j=0}^{17}(C+3+4j)^2.
\]
Dorais and Klyve report a complete base-3 search through \(C\). Its only two hits, \(11\) and \(1006003\), both fail the base-5 test. The replay checks those two residues and uses the published search completeness as input. [Dorais–Klyve, §4.1](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

**Why the eighteen survive the extra locks.** The published proof reserves \(c\bmod800730\), fixes the parity of \(d\), and makes its base-3 repairs in increasing prime order. Interleave the additional lock \(r^{\max(0,k_r-s_3(r))}\mid c\) at each \(r\in Z\). Earlier locks and repair periods have prime factors smaller than \(r\), and the reservation is prime to \(r\). The new lock is therefore available, and later repairs preserve it. After all locks, take \(c\ge\max(A,1)\) in the resulting progression and choose the passing binary class of \(d\) as in the original proof. [Eighteen-source proof](https://github.com/Samsen879/a303656/commit/2316089)

On a collision modulo \(r\in Z\), the two powers reduce to opposites because \(r\mid n\). Both are \((r-1)\)-st roots of unity modulo \(r^{k_r}\) after the lock. Unique lifting of these roots gives \(3^c+5^d\equiv0\pmod{r^{k_r}}\). The residual is therefore \(n\bmod r^{k_r}\), which has no odd valuation below \(k_r\). There is no rigid seed at this row. The eighteen-source proof counts the remaining rigid seeds, including when rows without a seed still act as dynamic helpers. [Exact modulus bridge](https://github.com/Samsen879/a303656/commit/1c648df4be90efe9065023067ec0125f4d1dbf59)

### Which rows can absorb load

Define \(T=\{r\in\mathcal C:e_r\le\min(s_3(r),s_5(r))\}\). At a retained inert row, reducing the precision by one must admit an exponent pair whose residual has exact valuation \(e_r-1\). Hence \(e_r\) is even. At a row in \(T\) dividing \(n\), the two powers already cancel modulo \(r^{e_r}\) on every collision, so this witness requires **\(v_r(n)=e_r-1\)**. In particular \(T\cap Z=\varnothing\). Any row of \(Z\) must exceed intrinsic precision on at least one base. That forces \(e_r\ge4\) and, by precision closure, an actual higher reader of \(r^{e_r-s_a(r)}\) in that base’s order. [Two-base precision closure](https://github.com/Samsen879/a303656/commit/fac27d29f366a0aed19e2ce917577d8084e9166e)

Now take a retained inert gate \(q>3\) ordinary to both bases with \(v_q(n)=1\). In the verified load proof, continue each path through any common row outside \(T\), using an edge on a base where precision is deficient. The edges strictly increase, so the paths end in \(T\). The merge argument is unchanged. Distinct incoming primes divide the receiving prime minus one, with an extra factor \(q\) if the receiving prime is itself a direct reader. If \(r_0\) is a lower bound on a direct reader, a terminal carrying \(j\ge2\) readers is strictly larger than \(r_0(2q)^{j-1}\). Thus the verified demand \(b_q\) must fit into the capacities of the **reachable rows of \(T\)**. Rows of \(Z\) can relay load but cannot discharge it. [Verified terminal-load bound](https://github.com/Samsen879/a303656/commit/7fdedcdbb4842a0a5f372337a19d4b2920b0f272)

For the actual doubly ordinary prime \(q=6823\), the demand is \(83\) and \(r_0=13647\) is a valid lower bound. If every common prime is at most \(10^{15}\), each terminal carries at most three readers, so **at least 28 reachable terminals** are required. With only eighteen common primes, one terminal must instead be at least \(473215170913354286833\). For \(q=379\), a slot just above the published cutoff already has capacity four under the size inequality. The height and count bounds alone can therefore accommodate its demand of twenty in eighteen slots. To extract an additional count in that case requires actual reachability restrictions or a target-dependent exclusion such as \(Z\). A terminal in \(T\) may also be one of the eighteen sources, so those counts cannot simply be added.

### Replay

The control below uses the actual base-5-only exceptional prime \(40487\). On the same target, the lock preserves the head reservation and turns a valuation-one collision into zero modulo \(p^2\). At precision four, the same collision class still has both a passing lift and an exact odd valuation. This checks why removing a rigid seed does not justify removing the row.

```python
from math import isqrt, lcm, prod

C = 150000 * prod((2,3,5,7,11,13,17,19,23,29))
assert C == 970453984500000
for p, residue in ((11,78), (1006003,31695130519)):
    assert pow(3,p-1,p*p) == 1
    assert pow(5,p-1,p*p) == residue != 1

q = 6823
assert q % 4 == 3 and all(q % d for d in range(2,isqrt(q)+1))
assert [pow(a,q-1,q*q) for a in (3,5)] == [38372553,8644742]
B = (1 + isqrt(4*q-3)) // 2
assert (q+B-1)//B == 83
assert 13647*13646**2 < 10**15 < 13647*13646**3
assert (83+2)//3 == 28
assert 13647*13646**4 + 1 == 473215170913354286833

p, c, d = 40487, 12772308906631, 13461
assert c % p == 0 and (c-1) % lcm(800730,20243) == 0
assert pow(3,20243,p) == 1
assert pow(5,p-1,p**2) == 1 != pow(5,p-1,p**3)

def R(c, d, e):
    m = p**e
    return (p*p-pow(3,c,m)-pow(5,d,m)) % m

assert (R(1,d,2), R(c,d,2)) == (24025*p,0)
good, bad = 44193343681405, 46566842556941
assert good % (p-1) == bad % (p-1) == d
assert (R(c,good,4), R(c,bad,4)) == (0,p**3)
```

For an all-exponent certificate \(M_0\), one can take \(A=v_3(M_0)\) and minimize among its divisors on that fixed tail. The resulting conditions are necessary for \(M_0\). The argument does not assert that a tail obstruction covers the omitted small exponents or establish a density or pointwise result.

The 40487 fixture is a singly exceptional analogy and does not exhibit a common prime or a finite obstruction. The count of eighteen is applied to the remaining rigid seeds on the fixed slice; zero-seed higher-precision rows may still be used as the helper rows permitted in its projection argument.
