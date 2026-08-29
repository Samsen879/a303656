# Formal class

Let `P` be a finite set of distinct primes `p == 3 (mod 4)`, `p != 5`.
For each row choose `K_p>=2`, a common residue `r_p mod p^K_p` for both
anchors `c in {0,1}`, and a nonempty set of accepted positive odd valuations
`E_p subset {1,...,K_p-1}`.  A value congruent to zero modulo `p^K_p` is
unresolved and is never accepted.

Put

```text
w_p = ord_p(5),
s_p = v_p(5^w_p-1),
a_p = max(0,K_p-s_p),
ell_p = w_p p^a_p.
```

An optional sound two-adic row has precision `K_2>=2` and exponent period
`t_2=1` for `K_2=2`, otherwise `t_2=2^(K_2-2)`.  When the row is absent,
omit `t_2` from the following LCMs (equivalently put `t_2=1`).  Define

```text
U = lcm(t_2,{w_p}),
beta_p = v_p(U),
L = lcm(t_2,{ell_p}).
```

For `x mod U`, the row-`p` coarse event is fatal if every full lift
`d==x (mod U)` modulo `L` has an accepted row-`p` valuation.  A coarse class
is safe at anchor `c` when it is two-adically safe and no odd row is coarse
fatal.  Existing reverse CRT gives

```text
a coarse safe x mod U exists iff a full safe d mod L exists.
```

For a dynamic row, with `m_p=min(a_p,beta_p)`, its conditional fatal mass in
its own `p` coordinate is

```text
rho_{p,c} = sum_{0<=j<m_p, s_p+j in E_p} (p-1)/p^(j+1).
```

The center digit is excluded because it contains an unresolved local zero.
A rigid fatal row is one congruence class modulo `w_p`.

## Boundary-aware coordinate criterion

Fix an anchor `c`.  A `K_2=2` row is independent of the exponent because
`5^d==1 (mod 4)`.  Before any coordinate induction, require this constant
row to be safe.  Equivalently, its unsafe density `Theta_c` is zero.  If it
is unsafe, then `Theta_c=1` and no safe exponent exists.  This condition is
not assigned to a fictitious coordinate two when `2` does not divide `U`.

If `K_2>=3`, then `2|t_2|U`; the two-adic unsafe event is a genuine event in
the coordinate modulo `2^v_2(U)` and has density `Theta_c`.  With no two-adic
row there is neither a constant boundary condition nor a two-adic hazard.

For every rational prime `l|U`, put

```text
D_{l,c} = rho_{l,c} for a dynamic l-row, otherwise 0,
R_{l,c} = sum_{q rigid fatal, P^+(w_q)=l} l^(-v_l(w_q)),
H_{l,c} = D_{l,c}+R_{l,c}
          + 1_{l=2 and K_2>=3} Theta_c.
```

After the `K_2=2` constant boundary has passed when present, if
`H_{l,c}<1` for every genuine coordinate `l|U`, then a coarse safe class
`x mod U` exists, hence a full safe exponent `d mod L` exists.  This includes
the empty-coordinate case `U=1`.

The dependency graph has an edge `p->q` when `p|w_q`.  Since `w_q|q-1`,
every edge satisfies `p<q`.  Thus the graph is a DAG and
`beta_p=max_q v_p(w_q)`.
