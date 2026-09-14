# Exact reformulation and coordinate conventions

## 1. Orders and multiplication

Work in Hamilton's rational quaternion algebra, with i²=j²=k²=-1 and ij=k=-ji.
Write

    q = a + bi + xj + tk = z + jw,
    z = a+bi,  w = x-ti.

The minus sign in w is necessary for this **left-j** convention. Then

    N(q)=a²+b²+x²+t²=N(z)+N(w).

The Lipschitz order is L=Z⁴. The Hurwitz order is

    H = Z⁴ ∪ (Z+1/2)⁴,

with integral basis 1,i,j,h, h=(1+i+j+k)/2. The coordinates of q in this basis
are (a-t,b-t,x-t,2t). All subsequent divisibility by a rational integer in H
refers to this lattice, not blindly to the four Hamilton coordinates.

## 2. Exact equivalence

For every n>1, the following statements are equivalent:

(A) n=a²+b²+3^c+5^d for nonnegative integers a,b,c,d.

(B) For some c,d≥0 there is q=z+jw in L with
    N(q)=n-3^c and N(w)=5^d.

(A)⇒(B): take z=a+bi and any Gaussian integer w of norm 5^d.
For example w=(2+i)^d is available, but it is not a restriction on the target.
(B)⇒(A): use |Re z| and |Im z| for the two nonnegative square coordinates.

Gaussian unique factorization gives the entire target set

    w=u(2+i)^r(2-i)^(d-r),  u∈{1,-1,i,-i}, 0≤r≤d.

Indeed every Gaussian prime divisor of a Gaussian integer whose norm is 5^d
lies over 5; conversely the displayed factors have norm 5^d. This includes
mixed allocations between the two primes over 5, not only a single ray.
The Euclidean property of Z[i] follows by nearest-integer rounding of real
and imaginary parts, with squared distance at most 1/2; this suffices for the
unique-factorization step used here.

## 3. Hurwitz states and integrality recovery

Allowing intermediate q∈H does not create a spurious target: when all four
coordinates are half-integers, a pair norm is (odd²+odd²)/4, which is a
half-integer, never the integer 5^d. Thus every H-state satisfying the literal
pair-norm target is automatically in L.

Every q∈H has an integral unit associate. To prove this, only consider
q=X/2 with all entries of X odd. Choose s_i∈{±1} with s_i≡X_i (mod 4), put
s=s_0+s_1i+s_2j+s_3k, and u=bar(s)/2. Then N(u)=1 and

    uq=bar(s)X/4 ∈ L,

because bar(s)X≡bar(s)s=4 (mod 4L), coordinatewise. This is a recovery of
integrality, not a claim that a selected coordinate-pair norm is preserved.
Units can mix the coordinates. Target tests are therefore performed on actual
integral members of each allowed symmetry orbit.

## 4. Boundaries

The useful state range is 3^c≤n-1, because the desired pair norm is at least 1.
If M=n-3^c<0 there are no states. If M=0, q=0 is not a target. This is distinct
from the permitted original residual n-3^c-5^d=0, which means z=0 and is valid.
For d=0, w is a Gaussian unit. The n=2 boundary is represented by z=0,w=1,c=0.

The height and content definitions in this package are only made for M>0.
A zero coordinate pair is excluded from `bad5`; it is not assigned height zero.

## 5. Matrix-convention correction in the task

For q=z+jw the matrix in the task,

    Psi(q) = [[z,w],[-bar(w),bar(z)]],

is an anti-homomorphism: Psi(q1 q2)=Psi(q2)Psi(q1). Its determinant is still
N(q), so the norm reformulation remains valid. To use multiplication in its
ordinary order, this package uses

    Phi(q) = [[z,-bar(w)],[w,bar(z)]].

Direct expansion gives Phi(q1q2)=Phi(q1)Phi(q2). In Gaussian coordinates,

    q1q2 = (z1z2-bar(w1)w2) + j(bar(z1)w2+w1z2).

This correction matters when translating a proposed left/right matrix action
back into an exact quaternion move. It is not an alteration of the target.
