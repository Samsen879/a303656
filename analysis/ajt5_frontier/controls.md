## Five actual bridges at the R4 integer

The R4 [integer fixture](../ajt5_integer_certificates/fixtures/no3_23_window.json) blocks the 91 parent rows with d≤6 and c≤12 using 23 primes excluding 3. Its positive parent witness has d=7, c=0. The following child rows extend this seed to an actual bridge for every digit. The [child square coordinates](controls_five_digits.json) were constructed independently and verified by exact multiplication. Each two-witness submission receives `REFUTED` from the integer NO_BRIDGE checker.

| Digit r | Parent d | Child e | Child c′ |
|---:|---:|---:|---:|
| 0 | 7 | 7 | 326 |
| 1 | 7 | 7 | 48 |
| 2 | 7 | 8 | 354 |
| 3 | 7 | 7 | 231 |
| 4 | 7 | 8 | 2 |

For the first four rows, remove small prime powers from the child residual, find a square root of −1 modulo the remaining split prime, and use Euclidean descent until the remainder is at most the square root of the prime. Checking that the complementary difference is a square yields a pair of coordinates. Multiply the two-square factors by the Gaussian norm identity. For r=4 the R4 seed gives the child coordinates directly from the norm of 5. Replay needs only the resulting square identities.

## The local tests at 2 and 3

For m≥135 and any digit r, some adjacent parent and child rows with d≤3, e≤4 and independently chosen c,c′≤2 have positive residuals whose odd parts are 1 modulo 4 and whose 3-adic valuations are even. With the 3-adic condition alone, e≤3 suffices. Neither conclusion establishes that a surviving residual is a sum of two squares.

At x=5m use K=5(5^d+3^c) on the parent and K=5^e+3^c−r on the child. Every selected difference x−K is positive. Multiplication by 5 preserves the 3-adic valuation and the odd part modulo 4. For each x modulo 2048, retain each row when its nonzero residue, after removing factors of 2, is fixed to 1 modulo 4. For each x modulo 729, retain each row when its nonzero residue has even 3-adic valuation. Discard rows with insufficient digits to certify the condition. The actual surviving set includes every retained row at the corresponding residue. The program intersects every pair of masks **on row labels** before projecting onto exponent columns. Every intersection has a bridge with e≤4. Every 3-adic mask has a bridge with e≤3.

The distinction in child caps is necessary for the joint test. At (m,r)=(770,2), the surviving parent columns through 3 are {3}. The child columns through 4 are {0,1,2,4}, so the bridge uses 3→4. All column sets here use only c≤2.

Run `python3 -O analysis/ajt5_frontier/controls.py` from the repository root to check the five square identities, checker verdicts, prefix covers, and the child-cap counterexample.
