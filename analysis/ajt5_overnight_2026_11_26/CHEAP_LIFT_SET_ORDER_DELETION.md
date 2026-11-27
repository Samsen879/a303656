# An actual-order deletion certificate for selecting cheap lifting rows

Use a finite inert panel \(Q\) and a compatible seed (periods \(m_3=2,m_5\in\{2,18\}\), \(c\ge3\) if preserving the 3-adic seed). Choose a set \(E\) of rows with at least one ordinary direction. Set \(P_b=\operatorname{lcm}(m_b,\{\operatorname{ord}_{p^3}(b):p\in E\})\) and, for \(q\notin E\), \(D_{b,q}=\operatorname{ord}_q(b^{P_b})\). For the rows still present outside \(E\), delete all rows touching an axis-prime coordinate \((b,\ell)\) whenever
\[
 0<\sum_{q:\ell\mid D_{b,q}}\ell^{-v_\ell(D_{b,q})}<1.
\]
If this process removes every row outside \(E\), there is a finite-panel witness with all valuations 0 or 2 and with its exact-two rows contained in \(E\). For a forward start \((C,D)\), it suffices that \(3^{C+2^rP_3-1}+5^{D+2^rP_5-1}<n\), with \(r=|Q\setminus E|\).

To prove it, fix the phases on \(E\) using increasing prime order and ordinary LTE as in [the deferred-lift construction](DEFERRED_LIFT_HEIGHT_BUDGET.md). At each prime, the old periods from smaller primes and the current mod-prime order are prime-to-\(p\). Preserve these resulting valuations thereafter by keeping the exponents fixed modulo \(P_3,P_5\). Restore the deleted coordinates in reverse order. Every row in the corresponding batch at a coordinate excludes at most one class mod \(\ell^{v_\ell(D_{b,q})}\) once its other relevant coordinates are fixed. The displayed sum is a union bound strictly below one on the finite prime-power coordinate. Previously restored rows do not depend on this coordinate; otherwise they would have been deleted in the current or earlier batch. Hence CRT yields simultaneous units outside \(E\). Finally use the [exponential-frequency compression](EXACT_LIFT_ROWS_ONLY_COMPRESSION.md), with valuations on \(E\) already fully frozen mod \(p^3\), so only the \(r\) unit-row exclusions contribute. Starting from the least forward representatives of the two classes gives the stated budget (including the \(P_b-1\) offset to those representatives). This deletion test is sufficient, not necessary, and imposes no claim about arbitrary panels.

For \(Q=\{7,19,31,271,463,547\}\), choose \(E=\{7\}\), both periods 294, and the outside order pairs are \((3,3),(5,1),(5,9),(11,11),(1,13)\). The base-3 mod-5 coordinate deletes two rows at load \(2/5\). A separate coordinate deletes each of the remaining three.

## Largest-collision-first can fail for all heights

Take \(Q=\{7,463\}\), \(n_0=3^{10}+5^{13}+96^2+139^2=1220790711\) and forward start \((8,13)\) in its parity class. Both rows initially have valuation one; the next available point \((10,13)\) has units at both and is a true norm. However a strategy requiring exact depth two at the larger row and keeping 7 a unit cannot succeed even with unlimited height preserving \(n\equiv0\bmod7\cdot463\). Indeed at 463 the order of 3 is 462 and \(5=3^{125}\), so a collision there requires \(c-125d=231\bmod462\). Reducing mod 6 gives \(c-5d=3\bmod6\), precisely a collision at 7 because \(5=3^5\bmod7\). This is a structural dependency, not merely exhaustion of the forward height window.

```python
def order(b,p):
    return next(k for k in range(1,p+1) if pow(b,k,p)==1)
assert [tuple(order(pow(b,294,p),p) for b in (3,5))
        for p in (19,31,271,463,547)]==[(3,3),(5,1),(5,9),(11,11),(1,13)]
n=3**10+5**13+96**2+139**2
assert n==1220790711 and n%(7*463)==0
for p in (7,463):
    r=n-3**8-5**13
    assert r%p==0 and r%(p*p)!=0 and (n-3**10-5**13)%p!=0
assert 3**12+5**13>=n and 3**8+5**15>=n
assert order(3,463)==462 and pow(3,125,463)==5
assert order(3,7)==6 and pow(3,5,7)==5
assert (125%6,231%6)==(5,3)
```
