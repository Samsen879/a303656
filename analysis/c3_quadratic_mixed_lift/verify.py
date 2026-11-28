"""Exact replay of the same-target lift and the oriented base-6 obstruction."""
from fractions import Fraction as F
from math import gcd, isqrt, lcm, prod


def norm(z):
    return sum(x*x for x in z)


def parameters(L):
    a, b = 9**L, 25**L
    return a, b, 3*a+25*b, 12*b-3*a, a+10*b


def simultaneous_crt(congruences):
    modulus = prod(m for _, m in congruences)
    residue = 0
    for r, m in congruences:
        other = modulus // m
        assert gcd(other, m) == 1
        residue += r*other*pow(other, -1, m)
    return residue % modulus, modulus


def finite_family():
    a, b, H, D, E = parameters(12)
    h, K = D-5, 1080
    assert (h+8)**2 < h*h+20*E < (h+9)**2
    # edge, Gaussian denominator m - i*b, parameter residue
    pack = ((0, 12224, 1, 69449792), (0, 73339, 6, 2702964291),
            (1, 48889, 4, 1366406856), (1, 61122, 5, 2021034347))
    congruences = [(0, 2), ((3*h-E)*pow(h, -1, 5), 5)]
    angles = []
    for edge, m, b0, r in pack:
        p = m*m+b0*b0
        I = m*pow(b0, -1, p) % p
        numerator = 5*r*r-h*r+5+3*h-E
        raw = h+1+3*I+(-3+I)*numerator*pow(10, -1, p)
        if edge == 1:
            raw = h+(-3+I)*(numerator*pow(10, -1, p)-1+I*r)
        assert I*I % p == p-1 and raw % p == 0
        assert gcd(p, D*E) == 1
        congruences.append((r, p))
        angles.append(F(2*b0*b0, p))

    r, base_period = simultaneous_crt(congruences)
    Y = 1 << 270
    low, high = 13*Y//16, 7*Y//8
    y_initial = low+(r-low) % base_period
    period = base_period*D*E
    count = (high-1-y_initial)//period+1
    assert count == 3875464
    # Uniform height and angle estimates. See README for their use.
    assert 20*h < low and 20*abs(5+3*h-E) < low*low
    assert 10000*h < 49*low*low
    assert F(49, 100)**2*(1+F(299, 100)**2)*F(13, 16)**4 > 1
    assert 10*F(51, 100)**2*F(7, 8)**4 < 2
    assert (25*b)**16 < 2**K and 2**(K+1)+H < a**32
    eps = F(1, 2**260)
    assert F(max(D, E), 2**K)+F(4*Y, 2**540) < eps
    assert all(F(1, 64*K*(K+1))+eps < r < F(1, 64*K*K)-eps
               for r in angles)
    assert all(abs(r-s) > 2*eps for i, r in enumerate(angles)
               for s in angles[i+1:])

    # Replay the endpoints and an interior point of the certified progression.
    base_chords = []
    for index in (0, count//2, count-1):
        y = y_initial+index*period
        assert low <= y < high
        t, rem = divmod(5*y*y-h*y+5+3*h-E, 10)
        assert rem == 0
        P = (h-3*t, t)
        Q = ((P[0]+1, P[1]+3), (P[0]+3-y, P[1]-1-3*y))
        S, n = norm(P), norm(P)+H
        shifts = (9*a+b, a+5*b)
        assert 2**K <= S < 2**(K+1) and (25*b)**16 <= n <= a**32
        assert tuple(norm(z) for z in Q) == tuple(n-s for s in shifts)
        seeds = []
        for k, (edge, m, b0, _) in enumerate(pack):
            p = m*m+b0*b0
            x, z = Q[edge]
            assert (m*x-b0*z) % p == (b0*x+m*z) % p == 0
            # Reverse the orientation adversarially. The norm stays the same.
            assert (m*x+b0*z) % p or (m*z-b0*x) % p
            real, imag = m*m-b0*b0, 2*m*b0
            R = ((real*x-imag*z)//p, (imag*x+real*z)//p)
            assert norm(R) == n-shifts[edge]
            dx, dy = R[0]-P[0], R[1]-P[1]
            D_edge = (D, E)[edge]
            assert gcd(dx, dy) == 1 and dx % 2 == dy % 2 == 1
            q = norm((dx, dy))//2
            det = dx*P[1]-dy*P[0]
            assert det % 2 == 0 and 2*q*S == (D_edge-q)**2+det**2
            assert 64*K*K*q < S < 64*K*(K+1)*q
            if index == 0:
                base_chords.append((dx % D_edge, dy % D_edge))
            assert base_chords[k] == (dx % D_edge, dy % D_edge)
            seeds.append(q)
        assert len(set(seeds)) == 4
    return K, period.bit_length(), count


def oriented_obstruction(sign, rows, expected, omissions):
    period = lcm(*(m for _, _, m in rows))
    good_sets = []
    for p, j, m in rows:
        assert p > 5 and all(p % d for d in range(2, isqrt(p)+1))
        assert pow(9, m, p) == pow(25, m, p) == 1
        I = sign*(-1)**j*pow(6, 2*j+1, p) % p
        assert I*I % p == p-1
        good = set()
        for L in range(period):
            A, B = pow(9, L, p), pow(25, L, p)
            h = 12*B-3*A-5
            discriminant = h*h+20*(A+10*B)-100+20*(h+10)*I
            if pow(discriminant, (p-1)//2, p) != p-1:
                good.add(L)
        good_sets.append(good)
    survivors = set(range(period))
    counts = []
    for good in good_sets:
        survivors &= good
        counts.append(len(survivors))
    assert counts == expected and not survivors
    # An omitted row must leave a survivor for this particular panel.
    for i, witness in enumerate(omissions):
        assert [j for j, good in enumerate(good_sets) if witness not in good] == [i]
    return period, counts


if __name__ == '__main__':
    print('finite:', *finite_family())
    _, _, _, D, E = parameters(6)
    h = D-5
    assert 128*593**2 < 6712**2+1 < 128*593*594
    assert (6712**2+1) % 197 == 0 and pow(h*h+20*E, 98, 197) == 196
    print('base6:', *oriented_obstruction(
        1, [(13,1,6), (97,1,48), (73,4,36), (109,13,27)],
        [72,18,12,0], [14,63,9,57]))
    print('conjugate:', *oriented_obstruction(
        -1, [(13,1,6), (37,0,18), (73,4,36), (61,7,15), (181,7,45), (241,2,60)],
        [120,70,25,10,6,0], [107,7,50,44,12,42]))
