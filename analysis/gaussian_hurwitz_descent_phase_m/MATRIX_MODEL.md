# M-D2 — the universal integral matrix subgroup is finite

This diagnosis belongs to the factor-transfer/Euclidean mechanism, not to a
fourth research mainline. Use the homomorphism Phi from
QUATERNION_REFORMULATION.md, and let Q_H be its real quaternion matrix algebra.

## Proposition

Suppose A,B∈SL2(C) satisfy A Q_H B=Q_H as sets. Then A,B∈SU2. Conversely any
such pair of SU2 matrices preserves Q_H and determinant. Therefore if
A,B∈SL2(Z[i]), each is one of the eight Lipschitz norm-one matrices. Universal
Gaussian integral row/column reduction within this class has only finitely
many actions.

## Proof

Putting the identity matrix into the condition shows C=AB∈Q_H and det C=1.
Every quaternion matrix X satisfies X*X=(det X)I, so C∈SU2. It follows that
A Q_H A^(-1)=Q_H. Let I_0=Phi(i), J_0=Phi(j). Their conjugates by A belong
to Q_H and have determinant 1, hence are unitary. Set P=A*A, positive Hermitian.
The unitarity equalities give I_0* P I_0=P and J_0* P J_0=P. Since I_0,J_0 are
unitary, P commutes with each. Commutation with I_0 makes P diagonal, and
commutation with J_0 makes its diagonal entries equal. Thus P=rI, r>0.
Since det P=|det A|²=1, r=1 and A∈SU2. Then B=A^(-1)C∈SU2.

For A∈SL2(Z[i])∩SU2, a column has two Gaussian integer entries whose squared
absolute values sum to 1. One entry is zero and the other a Gaussian unit.
The second column is forced by orthogonality and determinant 1. This yields
exactly eight possibilities. The converse follows by direct multiplication
in the quaternion algebra.

## Consequence and exact scope

A nontrivial transvection [[1,u],[0,1]], u≠0, is not unitary, so it cannot serve
as a universally shape-preserving Gaussian Euclidean row operation in a pair
A,B both of determinant 1. The norm-preserving Hurwitz integral isometry group
is also finite because it preserves a positive-definite lattice.

The proposition does NOT prohibit matrices selected for a single state
A(q),B(q), other determinant conventions with compensating scalar factors,
or localized groups. With denominators at 5, an infinite group is available,
but the away-from-5 content obstruction applies to the norm-5-generated
subgroup. Other-prime denominators require a different, explicit integrality
and termination argument and are not excluded by this proposition.
