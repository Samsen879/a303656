#!/usr/bin/env python3
"""Exact, bounded replay for A303656 Thread 3.

No web access; no repository mutation; no floating-point fitting.
Requires Python 3.10+, NumPy and SymPy.  The analytic and asymptotic
proofs are in research_report_zh.md, not certified by this script.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import platform
from math import isqrt
from pathlib import Path
import numpy as np
import sympy as sp

PINNED_SHA = '8f17e88e517720f61f3c21d58d91c04cd6fa11b5'


def powers(base: int, limit: int, multiplier: int = 1) -> list[int]:
    if base < 2 or multiplier < 1:
        raise ValueError('Invalid base or multiplier')
    out: list[int] = []
    p = multiplier
    while p <= limit:
        out.append(p)
        p *= base
    return out


def two_square_coefficients(N: int) -> np.ndarray:
    t = np.zeros(N+1, dtype=np.int64)
    for a in range(isqrt(N)+1):
        for b in range(isqrt(N-a*a)+1):
            t[a*a+b*b] += (1 if a == 0 else 2)*(1 if b == 0 else 2)
    assert int(t[0]) == 1 and int(t[1]) == 4
    return t


def independent_coefficient_checks(t: np.ndarray, F: np.ndarray) -> dict:
    """Two separately implemented arithmetic crosschecks.
    Jacobi divisor formula: DLMF 27.13.7, with n=0 handled separately.
    The second loop is signed four-variable enumeration, not convolution.
    """
    N = len(t)-1
    d = np.zeros(N+1,dtype=np.int64)
    d[0] = 1
    for k in range(1,N+1,2):
        d[k::k] += 4 if k%4 == 1 else -4
    assert np.array_equal(d,t)
    M = min(N,400)
    brute = np.zeros(M+1,dtype=np.int64)
    x = 1
    while x <= M:
        y = 1
        while x+y <= M:
            L = isqrt(M-x-y)
            for a in range(-L,L+1):
                B = isqrt(M-x-y-a*a)
                for b in range(-B,B+1):
                    brute[a*a+b*b+x+y] += 1
            y *= 5
        x *= 3
    assert np.array_equal(brute,F[:M+1])
    return {'jacobi_divisor_formula_checked_through':N,
            'r2_hash':coefficient_hash(d),
            'signed_four_variable_enumeration_checked_through':M,
            'small_F_hash':coefficient_hash(brute)}


def add_shift(out: np.ndarray, source: np.ndarray, shift: int) -> None:
    if shift < 0:
        raise ValueError('Negative shifts are not used in series replay')
    if shift < len(out):
        out[shift:] += source[:len(out)-shift]


def product_lacunary(t: np.ndarray, A: int, B: int) -> np.ndarray:
    N = len(t)-1
    out = np.zeros_like(t)
    for x in powers(3, N, A):
        for y in powers(5, N, B):
            add_shift(out, t, x+y)
    return out


def dilate(t: np.ndarray, K: int) -> np.ndarray:
    out = np.zeros_like(t)
    out[::K] = t[:(len(t)-1)//K+1]
    return out


def coefficient_hash(t: np.ndarray) -> str:
    # Stable textual encoding, independent of machine byte order.
    return hashlib.sha256(','.join(map(str, map(int, t))).encode()).hexdigest()


def symbolic_checks() -> dict:
    a,b,X,Y,u,v,w,z,r,s,K,R,alpha,beta = sp.symbols(
        'a b X Y u v w z r s K R alpha beta')
    expression = sp.expand((u*a+v*b+r)**2 + (w*a+z*b+s)**2
                           + alpha*X+beta*Y-K*(a*a+b*b+X+Y)-R)
    p = sp.Poly(expression, a,b,X,Y)
    constraints = {str(m): str(c) for m,c in p.terms()}
    assert sp.expand((a-2*b)**2+(2*a+b)**2+X+5*Y
                     -(5*(a*a+b*b+X+Y)-4*X)) == 0
    assert sp.expand((3*a)**2+(3*b)**2+9*X+Y
                     -(9*(a*a+b*b+X+Y)-8*Y)) == 0
    assert sp.expand((3*a-4*b)**2+(4*a+3*b)**2+X+25*Y
                     -(25*(a*a+b*b+X+Y)-24*X)) == 0
    assert sp.expand((5*a)**2+(5*b)**2+X+25*Y
                     -(25*(a*a+b*b+X+Y)-24*X)) == 0
    # The affine polynomial coefficients are checked, not fitted to data.
    assert p.coeff_monomial(a*a) == u*u+w*w-K
    assert p.coeff_monomial(a*b) == 2*(u*v+w*z)
    assert p.coeff_monomial(b*b) == v*v+z*z-K
    assert p.coeff_monomial(a) == 2*(u*r+w*s)
    assert p.coeff_monomial(b) == 2*(v*r+z*s)
    assert p.coeff_monomial(X) == alpha-K
    assert p.coeff_monomial(Y) == beta-K
    t = sp.symbols('t')
    ra = ((1-t*t)*a-2*t*b)/(1+t*t)
    rb = (2*t*a+(1-t*t)*b)/(1+t*t)
    assert sp.cancel(ra*ra+rb*rb-a*a-b*b) == 0
    # The grid is linearly independent as proved in the report, but has
    # genuine nonlinear relations: do NOT infer algebraic independence.
    T,P0,P1,Q0,Q1 = sp.symbols('T P0 P1 Q0 Q1')
    assert sp.expand((T*P0*Q0)*(T*P1*Q1)-(T*P1*Q0)*(T*P0*Q1)) == 0
    # General positive binary quadratic forms: an affine shift does not
    # change the determinant obstruction for a nonzero norm defect.
    g11,g12,g22,h1,h2,eta = sp.symbols('g11 g12 g22 h1 h2 eta')
    H = sp.Matrix([[g11,g12,g11*h1+g12*h2],
                   [g12,g22,g12*h1+g22*h2],
                   [g11*h1+g12*h2,g12*h1+g22*h2,
                    g11*h1*h1+2*g12*h1*h2+g22*h2*h2+eta]])
    assert sp.expand(H.det()-eta*(g11*g22-g12*g12)) == 0
    return {'coefficient_constraints': constraints,
            'centered_binary_quadric_homogenized_determinant':'eta*(g11*g22-g12**2)',
            'catalogue_identities_verified': 6,
            'additional_checks':['rational norm-preserving rotation',
                                 'quadratic rank-one identity for H-grid']}


def enumerate_similitudes(bound: int = 100) -> dict:
    counts = {}
    matrices = {}
    for K in range(1,bound+1):
        q = isqrt(K)
        cols = [(a,b) for a in range(-q,q+1) for b in range(-q,q+1)
                if a*a+b*b == K]
        found = set()
        for a,b in cols:
            for c,d in cols:
                if a*c+b*d == 0:
                    found.add((a,c,b,d))
        predicted = {(a,-sig*b,b,sig*a) for a,b in cols for sig in (-1,1)}
        assert found == predicted
        counts[str(K)] = len(found)
        if K in (3,5,9,15,25):
            matrices[str(K)] = sorted(map(list,found))
    assert [counts[str(k)] for k in (3,5,9,15,25)] == [0,16,8,0,24]
    return {'K_max': bound, 'counts': counts, 'selected_matrices': matrices}


def grid_series_checks(t: np.ndarray, max_state: int = 3) -> dict:
    N = len(t)-1
    D5, D9 = t-dilate(t,5), t-dilate(t,9)
    assert np.all(D5 >= 0) and np.all(D9 >= 0)
    records = []
    for u in range(max_state):
        for v in range(max_state):
            A, B = 5**u, 9**v
            source = product_lacunary(t,A,B)
            lhs5 = product_lacunary(t,5*A,B)
            E5 = product_lacunary(D5,5*A,5*B)
            for x in powers(3,N,5*A):
                add_shift(E5,t,x+B)
            assert np.all(E5 >= 0)
            assert np.array_equal(lhs5,dilate(source,5)+E5)
            lhs9 = product_lacunary(t,A,9*B)
            E9 = product_lacunary(D9,9*A,9*B)
            for y in powers(5,N,9*B):
                add_shift(E9,t,A+y)
                add_shift(E9,t,3*A+y)
            assert np.all(E9 >= 0)
            assert np.array_equal(lhs9,dilate(source,9)+E9)
            records.append({'u':u,'v':v,'E5_hash':coefficient_hash(E5),
                            'E9_hash':coefficient_hash(E9),
                            'checked_through':N})
    nodes = [(u,v) for u in range(max_state+1) for v in range(max_state+1)]
    edges = [(s,(s[0]+1,s[1]),5) for s in nodes if s[0]<max_state]
    edges += [(s,(s[0],s[1]+1),9) for s in nodes if s[1]<max_state]
    assert all(a[0]+a[1]<b[0]+b[1] for a,b,_ in edges)
    assert not any(b == (0,0) for _,b,_ in edges)
    return {'identities_checked':len(records)*2,'records':records,
            'finite_graph':{'nodes':nodes,'edges':edges,'cycle':False,
                            'incoming_edge_to_original_state':False},
            'D3_at_3':int(t[3]-dilate(t,3)[3]),
            'D15_at_15':int(t[15]-dilate(t,15)[15])}



def binary_section_checks(t: np.ndarray, F: np.ndarray) -> dict:
    """Exact positive contraction on every original residue class.
    The three auxiliary states do NOT constitute a closed automaton.
    """
    N = len(t)-1
    L = N//2
    Ge = np.zeros(L+1,dtype=np.int64)
    for x in powers(3,2*L):
        for y in powers(5,2*L):
            assert (x+y)%2 == 0
            add_shift(Ge,t[:L+1],(x+y)//2)
    assert np.array_equal(F[::2],Ge)
    result = {'even':{'target':'2m','factor':1,'checked_m_max':L,
                      'auxiliary_hash':coefficient_hash(Ge)}}
    for eps,r in ((1,1),(0,3)):
        L = (N-r)//4
        theta = np.zeros(L+1,dtype=np.int64)
        for a in range(isqrt(L)+1):
            theta[a*a] = 1 if a==0 else 2
        thetaU = np.zeros(L+1,dtype=np.int64)
        for u in range(isqrt(L)+1):
            if u*(u+1)<=L:
                add_shift(thetaU,2*theta,u*(u+1))
        G = np.zeros(L+1,dtype=np.int64)
        for x in powers(9,4*L+r,3**eps):
            for y in powers(5,4*L+r):
                assert (x+y+1-r)%4 == 0
                add_shift(G,thetaU,(x+y+1-r)//4)
        assert np.array_equal(F[r::4],2*G)
        result[str(r)+'_mod_4']={'target':'4m+'+str(r),'factor':2,
                                 'checked_m_max':L,'auxiliary_hash':coefficient_hash(G)}
    result['guards_exhaustive'] = True
    result['finite_state_closure_proved'] = False
    return result


def nonlinear_theta_checks(N: int) -> dict:
    """Finite nonlinear functional closure, not a positive automaton.
    Phi(x)=Phi(x^4)+2*x*Psi(x^8); Psi(x)^2=Phi(x)*Psi(x^2).
    """
    phi = np.zeros(N+1,dtype=np.int64)
    for a in range(isqrt(N)+1):
        phi[a*a] = 1 if a == 0 else 2
    psi = np.zeros(N+1,dtype=np.int64)
    tri = []
    j = 0
    while j*(j+1)//2 <= N:
        v = j*(j+1)//2
        psi[v] = 1
        tri.append(v)
        j += 1
    rhs_phi = dilate(phi,4)
    add_shift(rhs_phi,2*dilate(psi,8),1)
    assert np.array_equal(phi,rhs_phi)
    psi_sq = np.zeros(N+1,dtype=np.int64)
    phi_psi2 = np.zeros(N+1,dtype=np.int64)
    for v in tri:
        add_shift(psi_sq,psi,v)
        add_shift(phi_psi2,phi,2*v)
    assert np.array_equal(psi_sq,phi_psi2)
    # Reconstruct the functions by the nonlinear recurrence alone.
    M = min(N,512)
    rp,rq = [0]*(M+1),[0]*(M+1)
    rp[0] = rq[0] = 1
    for n in range(1,M+1):
        rp[n] = (rp[n//4] if n%4 == 0 else 0)
        if n%8 == 1:
            rp[n] += 2*rq[(n-1)//8]
        positive_rhs = sum(rp[n-2*j]*rq[j] for j in range(n//2+1))
        removed_convolution = sum(rq[j]*rq[n-j] for j in range(1,n))
        value = positive_rhs-removed_convolution
        assert value%2 == 0
        rq[n] = value//2
    assert rp == [int(v) for v in phi[:M+1]]
    assert rq == [int(v) for v in psi[:M+1]]
    assert int(phi_psi2[2]) == 1 and int(psi[1])**2 == 1 and int(psi[2]) == 0
    return {'identities_checked':2,'checked_through':N,
            'isolated_coefficient_reconstruction_through':M,
            'Phi_hash':coefficient_hash(phi),'Psi_hash':coefficient_hash(psi),
            'cancellation_at_2':{'positive_product_coefficient':1,
                                 'removed_convolution_coefficient':1,
                                 'twice_Psi_coefficient':0},
            'positivity_preserving':False,
            'bounded_fanout_coefficient_automaton':False}


def first_witness(n: int, fixed_c: int | None = None):
    cs = []
    if fixed_c is None:
        for c,x in enumerate(powers(3,n)):
            cs.append((c,x))
    else:
        cs.append((fixed_c,3**fixed_c))
    for c,x in cs:
        for d,y in enumerate(powers(5,n)):
            m = n-x-y
            if m < 0: continue
            for a in range(isqrt(m)+1):
                b = isqrt(m-a*a)
                if a*a+b*b == m:
                    return [a,b,c,d]
    return None


def countermodels(t: np.ndarray, F: np.ndarray) -> dict:
    examples = []
    for n in (5,21):
        fixed = first_witness(n,0)
        free = first_witness(n)
        assert fixed is None and free is not None
        examples.append({'n':n,'fixed_c0_witness':fixed,'original_witness':free,
                         'F_coefficient':int(F[n])})
    assert (21+4)//5 == 5
    # Coefficient domination is stronger than support domination.
    count_failures = {}
    for q in (3,5,9,15,25):
        record = None
        for n in range(2*q,len(F)):
            if F[n] < F[n//q]:
                record = {'n':n,'m':n//q,'F_n':int(F[n]),'F_m':int(F[n//q])}
                break
        count_failures[str(q)] = record
    return {'narrowed_state_countermodels':examples,
            'first_bounded_floor_count_domination_failures':count_failures}


def rank_certificate(F: np.ndarray, degree: int = 12, forcing: bool = False) -> dict:
    """Exact finite-field full column rank -> no complex polynomial relation
    of this degree for these dilates. Row witnesses and pivots are exported.
    """
    mod = 1_000_000_007
    ks = [1,3,5,9,15,25]
    cols = ([(0,r) for r in range(degree+1)] if forcing else [])
    cols += [(k,r) for k in ks for r in range(degree+1)]
    def coefficient(n: int, k: int, r: int) -> int:
        if k == 0:  # Polynomial forcing column x^r.
            return int(n == r)
        return int(F[(n-r)//k]) if n>=r and (n-r)%k == 0 else 0
    rows = []
    basis: dict[int,list[int]] = {}
    pivots = []
    det = 1
    for n in range(min(len(F),5000)):
        vec = [coefficient(n,k,r) % mod for k,r in cols]
        for j in sorted(basis):
            if vec[j]:
                m = vec[j]
                bj = basis[j]
                vec = [(a-m*b)%mod for a,b in zip(vec,bj)]
        j = next((j for j,a in enumerate(vec) if a), None)
        if j is None: continue
        pivot = vec[j]
        inv = pow(pivot,-1,mod)
        basis[j] = [(a*inv)%mod for a in vec]
        rows.append(n)
        pivots.append({'row':n,'column':j,'pivot_before_normalization':pivot})
        det = det*pivot % mod
        if len(basis) == len(cols): break
    assert len(basis) == len(cols), (len(basis),len(cols))
    # Account for the column permutation, since pivots need not appear in order.
    pc = [p['column'] for p in pivots]
    invs = sum(pc[i]>pc[j] for i in range(len(pc)) for j in range(i+1,len(pc)))
    if invs % 2: det = -det % mod
    sub = sp.Matrix([[coefficient(n,k,r) for k,r in cols] for n in rows])
    # Independent exact rank of the selected integer submatrix, modulo mod.
    from sympy.polys.matrices import DomainMatrix
    from sympy import GF
    dm = DomainMatrix.from_Matrix(sub).convert_to(GF(mod))
    independent_det = int(dm.det()) % mod
    assert independent_det == det and det != 0
    return {'dilations':ks,'polynomial_forcing_included':forcing,
            'polynomial_degree_max':degree,'prime':mod,
            'columns':cols,'rank':len(cols),'pivot_rows':rows,
            'pivot_data':pivots,'selected_square_minor_determinant_mod_prime':det,
            'scope':'Exact finite-degree exclusion; not a computational proof of the unbounded analytic theorem.'}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--N',type=int,default=20000)
    ap.add_argument('--output',type=Path,default=Path(__file__).with_name('certificate.json'))
    args = ap.parse_args()
    if args.N < 1000 or args.N > 200000:
        raise SystemExit('Use 1000 <= N <= 200000. No large scan is intended.')
    t = two_square_coefficients(args.N)
    F = product_lacunary(t,1,1)
    result = {'scope':'Bounded exact identity and coefficient replay, not universal verification.',
              'repository_sha':PINNED_SHA,'N':args.N,
              'environment':{'python':platform.python_version(),
                             'numpy':np.__version__,'sympy':sp.__version__},
              'symbolic':symbolic_checks(),
              'independent_coefficients':independent_coefficient_checks(t,F),
              'similitudes':enumerate_similitudes(),
              'positive_grid':grid_series_checks(t),
              'binary_sections':binary_section_checks(t,F),
              'finite_nonlinear_theta':nonlinear_theta_checks(args.N),
              'countermodels':countermodels(t,F),
              'linear_relation_exclusion':rank_certificate(F),
              'linear_relation_exclusion_with_forcing':rank_certificate(F,forcing=True),
              'F_coefficient_hash':coefficient_hash(F)}
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':'PASS','output':str(args.output),'N':args.N,
                      'matrix_counts':{k:result['similitudes']['counts'][str(k)] for k in (3,5,9,15,25)},
                      'positive_identities':result['positive_grid']['identities_checked'],
                      'binary_sections':result['binary_sections'],
                      'nonlinear_theta':result['finite_nonlinear_theta'],
                      'rank':result['linear_relation_exclusion']['rank'],
                      'minor_det':result['linear_relation_exclusion']['selected_square_minor_determinant_mod_prime'],
                      'forcing_rank':result['linear_relation_exclusion_with_forcing']['rank'],
                      'forcing_minor_det':result['linear_relation_exclusion_with_forcing']['selected_square_minor_determinant_mod_prime'],
                      'countermodels':result['countermodels']},ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
