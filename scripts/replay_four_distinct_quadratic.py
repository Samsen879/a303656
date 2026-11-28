"""Exact, standalone replay for analysis/four_distinct_quadratic_labels.md."""
from math import gcd

OFFSETS = ((3, 2), (7, 6), (1, 0), (5, 1))
MULTIPLIERS = (-12, -6, 12)


def norm(z):
    x, y = z
    return x*x + y*y


def verify(n, shifts, rows):
    assert len(shifts) == len(rows) == 4
    for s, z in zip(shifts, rows):
        assert n - s == norm(z) > 0


def layer(U, V):
    T, W = 5**U, 3**V
    p, q = (51*T-19*W)//6, (51*T+19*W)//6
    assert (6*p, 6*q) == (51*T-19*W, 51*T+19*W)
    G, R = norm((p, q)), (T*T+W*W)//2
    assert gcd(p, q) == gcd(2*R, G) == 1 and G % 2
    x = R*pow(p, -1, q) % q
    y = (R-p*x)//q
    assert p*x+q*y == R
    L, C = q*x-p*y, 20821*T*T+2903*W*W
    shifts = tuple(3**(2*V+c) + 5**(2*U+d) for c, d in OFFSETS)
    assert all(s+2*j*R+j*j*G == C
               for s, j in zip(shifts[:3], MULTIPLIERS))
    return p, q, G, R, x, y, L, C, shifts


def generate(U, V, parameter):
    p, q, G, R, x, y, L, C, shifts = layer(U, V)
    s = shifts[-1]
    k = 2*((C-s+4*L)*pow(4*R, -1, G) % G)
    K = k+2*G*parameter
    numerator = s-C-4*L+2*R*K
    assert numerator % (4*G) == 0
    tau = 1+K*K//4+numerator//(4*G)
    x, y = x+tau*q, y-tau*p
    n = C+norm((x, y))
    rows = [(x+j*p, y+j*q) for j in MULTIPLIERS]
    rows.append((x-2*q+K*p, y+2*p+K*q))
    verify(n, shifts, rows)
    return n, rows, K


def lattice_test(p, q, G, longitudinal, transverse):
    J = 2240*transverse+595916
    A = 2240*longitudinal
    return (p*J-q*A) % G == 0


def main():
    n, rows, K = generate(1, 1, 0)
    assert (n, K) == (512258746876272177, 6818)
    assert rows == [(604305197, -383502250), (604305395, -383501938),
                    (604305989, -383501002), (604530483, -383147024)]
    assert (n-3**3-5**3) % 49 == 7
    # Independent exhaustive oracle for the first modular condition.
    p, q, G, R, x, y, L, C, shifts = layer(1, 1)
    assert [j for j in range(0, 2*G, 2)
            if (shifts[-1]-C-4*L+2*R*j) % (4*G) == 0] == [6818]

    for U in range(1, 21):
        for V in range(1, U+1):
            p, q, G, R, x, y, L, C, shifts = layer(U, V)
            s, T, W = shifts[-1], 5**U, 3**V
            a = generate(U, V, T)
            b = generate(U, V, T+1)
            assert a[0] < b[0]
            if V < 2:
                continue
            K = a[2]
            # The two modular oracles are compared on hits and shifted misses.
            for h, j in [(2, K), (2, K+2), (0, 0), (-3, K-1)]:
                raw = (s-C-2*h*L+2*R*j) % G == 0
                assert raw == lattice_test(p, q, G, h, j)
            J, A = 2240*K+595916, 4480
            assert (p*J-q*A) % G == (q*J+p*A) % G == 0
            r, t = (q*J+p*A)//G, (q*A-p*J)//G
            assert p*r+q*t == A and q*r-p*t == J
            if U >= 6:
                assert 560*W*abs(K) >= T*T
                assert a[0]*(560*W)**4 >= T**10

    # An ordinary-height fourth witness on the first-three strand lies
    # outside the step lattice. In fact no step-lattice pair works here.
    p, q, G, R, x, y, L, C, shifts = layer(3, 2)
    base = (x-5*q, y+5*p)
    rows = [(base[0]+j*p, base[1]+j*q) for j in MULTIPLIERS]
    rows.append((19164, 2153))
    n = C+norm(base)
    assert n == 371992113 and 15625*5**6 < n < 5*15625*5**6
    verify(n, shifts, rows)
    dx, dy = rows[-1][0]-base[0], rows[-1][1]-base[1]
    assert (p*dx+q*dy) % G != 0
    for h in range(-46, 47):
        for K in range(-46, 47):
            fourth = (base[0]-h*q+K*p, base[1]+h*p+K*q)
            assert norm(fourth) != n-shifts[-1]
    print("PASS: quadratic witnesses, two residue tests, and ordinary-height controls")


if __name__ == "__main__":
    main()
