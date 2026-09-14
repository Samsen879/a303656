# M-D1 — away-from-5 Hurwitz content and infinite target-free components

This is a route-pruning theorem. The underlying preservation of local lattice
content under local units is elementary and is not claimed to be new in the
literature. The explicit application to this target and this move family is
a proved asset of the present report.

## Statement

For 0≠q=a+bi+xj+tk∈H define

    cont_H(q)=gcd(a-t,b-t,x-t,2t)>0,
    kappa_5(q)=cont_H(q)/5^v5(cont_H(q)).

The arguments of the gcd are integers even for a half-integral q.
Every legal norm-5 neighbor, every Hurwitz-unit multiplication, every signed
coordinate permutation, and quaternion conjugation preserves kappa_5.
Every target q∈H with N(w)=5^d has kappa_5(q)=1.

Consequently, every component with kappa_5>1 is target-free. Infinitely many
norm shells have such a component even though a target exists elsewhere on
the same shell.

## Proof of preservation

For each rational prime ell≠5, put H_ell=H⊗Z_ell and

    nu_ell(q)=max{r≥0:q∈ell^r H_ell}.

If N(alpha)=5, then alpha^(-1)=bar(alpha)/5∈H_ell. The same is true of beta,
and 5 is a scalar unit in Z_ell. Thus q↦alpha q beta/5 is a Z_ell-linear
bijection of H_ell preserving every lattice ell^r H_ell. Its inverse has the
same property. It follows that nu_ell(q')=nu_ell(q) for every ell≠5.
Taking the product of ell^nu_ell gives kappa_5 preservation. This argument
includes ell=2 in the Hurwitz lattice; no assertion of coordinatewise
Lipschitz divisibility at 2 is used.

Every listed finite symmetry is a Z-linear automorphism of H, so it preserves
cont_H itself. This proves the assertion for the symmetry-augmented graph.

## Proof that targets have kappa_5=1

A target is integral, as established in QUATERNION_REFORMULATION.md.
If an odd ell≠5 divides cont_H(q), then q∈ell H_ell. Since 2 is invertible at
ell, its four Hamilton coordinates are divisible by ell, hence ell² divides
x²+t²=5^d, a contradiction.

If 2 divides cont_H(q), then the integral q belongs to 2H. The integral vectors
in 2H have either all coordinates even or all coordinates odd. In either case
x²+t² is even, again contradicting 5^d. Thus no rational prime other than 5
divides cont_H(q).

## Infinite family with a target on the same norm shell

For every integer k≥0 set

    M_k=9·25^k,
    q_0=3·5^k,
    q_*=5^k(2+2i+j).

Both states have norm M_k. The first has kappa_5=3. The second has
kappa_5=1 and second-pair norm 25^k=5^(2k), so it is a target. The entire
component containing q_0 is nevertheless target-free. This is an infinite
obstruction to reaching a target from an **arbitrary** four-square
representation. It is not merely a shell on which no target exists.

No globally defined, target-terminating, strictly decreasing well-founded
height can therefore work on every nonterminal state using only these moves.
Otherwise descent from q_0 would have to terminate at a forbidden target.

## Primitive and 2-adic qualifications

Ordinary coordinate gcd and Hurwitz content differ. For example
(1,1,1,1) is primitive in Z⁴ but has cont_H=2. So stating a theorem for
'primitive quaternions' without naming the lattice leaves a real gap.

Full Hurwitz primitivity cont_H=1 is not preserved by all 5-neighbors:
5-primary content can change. The proved invariant is specifically the
away-from-5 part. The laboratory therefore reports primitive induced
subgraphs separately from full components.

Conversely kappa_5=1 is only necessary, not sufficient. At M=47 all states
are Hurwitz-primitive, yet no target exists. The only possible powers are
1,5,25; the complementary norms are 46,42,22. Each has a prime 3 mod 4 to
odd exponent. The elementary proof of this obstruction is that for such a
prime ell, ell|a²+b² implies ell|a,b, so a norm has even ell-adic valuation.

If 4|M there is no target on the entire shell, because M-5^d≡3 (mod 4)
cannot be a sum of two squares. This is a separate elementary obstruction.
Neither statement rules out the original problem, where c can change M.

## What has NOT been proved

There is no theorem here saying kappa_5 completely classifies all components
for arbitrary M. Nor is there a proof that some choice of c always yields a
target-containing component. General unquotiented connectivity remains outside
the established results. These limitations prevent claiming Level C.
