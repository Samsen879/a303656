#!/usr/bin/env python3
"""Exact, standard-library reference checks for A303656 terminal Phase E.

No network, no repository imports, no prime-range scan, no probable-prime test.
Finite checks certify only the statements explicitly listed in evidence.json.
They do not prove B7 emptiness or instantiate a complete C=1 certificate.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

R = (43, 127, 379, 7603, 19531, 519499)
D = (1, 2, 3, 6, 7, 14, 21, 42)
EXPECTED_ORDERS = (42, 42, 21, 42, 7, 21)
EXPECTED_KAPPA = (
    (31,35,1,4,6,34,16,24),
    (13,51,84,113,77,103,113,20),
    (367,371,93,196,374,152,278,14),
    (421,2815,6729,2894,3194,4141,2316,2810),
    (13950,9300,269,18334,5579,10229,19258,1193),
    (109652,419434,105361,262189,258050,432861,344114,222192),
)
EXCLUDED_BY_PHASE_D = (43, 86, 127, 129, 258)

class CheckFailure(ValueError):
    pass

def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)

@lru_cache(None)
def factors(n: int) -> tuple[tuple[int, int], ...]:
    """Complete factorization by integer trial division; input is small here."""
    require(n >= 1, 'factorization input must be positive')
    out: list[tuple[int,int]] = []
    p = 2
    while p*p <= n:
        e = 0
        while n % p == 0:
            e += 1
            n //= p
        if e:
            out.append((p,e))
        p = 3 if p == 2 else p + 2
    if n > 1:
        out.append((n,1))
    return tuple(out)

def prime(n: int) -> bool:
    return n >= 2 and factors(n) == ((n,1),)

@lru_cache(None)
def divisors(n: int) -> tuple[int, ...]:
    out = [1]
    for p,e in factors(n):
        out = [a*p**k for a in out for k in range(e+1)]
    return tuple(sorted(out))

def mobius(n: int) -> int:
    ff = factors(n)
    return 0 if any(e>1 for _,e in ff) else (-1)**len(ff)

def valuation(n: int, p: int) -> int:
    require(n != 0, 'valuation(0) not allowed')
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e

def exact_order_check(a: int, q: int, n: int) -> dict[str,int]:
    require(prime(q) and math.gcd(a,q)==1, 'prime/unit precondition')
    require(n >= 1 and (q-1)%n==0, 'order must divide q-1')
    require(pow(a,n,q)==1, 'claimed order fails main power')
    drops = {str(p):pow(a,n//p,q) for p,_ in factors(n)}
    require(all(v != 1 for v in drops.values()), 'claimed order not exact')
    return drops

@lru_cache(None)
def order(a: int, q: int) -> int:
    require(prime(q) and math.gcd(a,q)==1, 'order prime/unit precondition')
    n=q-1
    for p,_ in factors(q-1):
        while n%p==0 and pow(a,n//p,q)==1:
            n//=p
    exact_order_check(a,q,n)
    return n

def lift_record(a: int, q: int) -> dict[str,Any]:
    n=order(a,q)
    s=1
    while s < 6 and pow(a,n,q**(s+1)) == 1:
        s+=1
    require(s<6, 'precision cap exceeded, not silently clipped')
    return dict(base=a, q=q, order=n, order_factors=dict(factors(n)),
                q_minus_1_factors=dict(factors(q-1)),
                order_drop_residues=exact_order_check(a,q,n),
                s=s, next_lift_coefficient=(pow(a,n,q**(s+1))-1)//q**s,
                fermat_quotient=(pow(a,q-1,q*q)-1)//q,
                admitted=q%4==3)

# Low-to-high polynomial coefficients, monic exact division.
def trim(a: list[int]) -> list[int]:
    while len(a)>1 and a[-1]==0:
        a.pop()
    return a

def multiply(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    c=[0]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):
            c[i+j]+=u*v
    return tuple(trim(c))

def divide_monic(a: tuple[int,...], b: tuple[int,...]) -> tuple[int,...]:
    require(b[-1]==1 and len(a)>=len(b), 'monic division precondition')
    z=list(a)
    out=[0]*(len(a)-len(b)+1)
    while len(z)>=len(b) and any(z):
        j=len(z)-len(b)
        c=z[-1]
        out[j]=c
        for k,v in enumerate(b):
            z[j+k]-=c*v
        trim(z)
    require(not any(z), 'nonzero polynomial remainder')
    return tuple(trim(out))

@lru_cache(None)
def cyclotomic(n: int) -> tuple[int,...]:
    require(1<=n<=60, 'only small index polynomials may be expanded')
    a=(-1,)+(0,)*(n-1)+(1,)
    for d in divisors(n):
        if d<n:
            a=divide_monic(a,cyclotomic(d))
    return a

def evaluate(c: tuple[int,...], a: int, modulus: int|None=None) -> int:
    out=0
    for k in reversed(c):
        out=out*a+k
        if modulus is not None:
            out%=modulus
    return out

def derivative(c: tuple[int,...]) -> tuple[int,...]:
    return tuple(i*c[i] for i in range(1,len(c))) or (0,)

def normalized_polynomial_route(r: int, d: int, f: int) -> tuple[int,int]:
    """Phi_(rd)(5)/r^[d=f] modulo r^2, by exact modular division."""
    eps=int(d==f)
    den=evaluate(cyclotomic(d),5)*r**eps
    modulus=den*r*r
    z=pow(5,r,modulus)
    num=evaluate(cyclotomic(d),z,modulus)
    require(num%den==0, 'modular numerator must be exactly divisible')
    return num//den,eps

def normalized_mobius_route(r: int, n: int) -> tuple[int,int]:
    """Independent algebraic organization: unit parts of 5^a-1, a|n.

    No large Phi polynomial/value is built. The r-adic valuations are obtained
    from modular powers, not from the polynomial route's expected exception.
    """
    unit=1
    val=0
    for a in divisors(n):
        mu=mobius(n//a)
        if not mu:
            continue
        v=0
        while v<5 and pow(5,a,r**(v+1))==1:
            v+=1
        require(v<5, 'Mobius valuation precision cap')
        raw=(pow(5,a,r**(v+2))-1)%(r**(v+2))
        require(raw%r**v==0, 'unit extraction exact division')
        u=(raw//r**v)%(r*r)
        require(math.gcd(u,r)==1, 'unit extraction failed')
        unit=unit*(u if mu==1 else pow(u,-1,r*r))%(r*r)
        val+=mu*v
    return unit,val

def primitive_phi_mod(a: int, q: int, n: int, precision: int) -> tuple[int,int]:
    """Return Phi_n(a) mod q^precision and Phi'_n(a) mod q at exact order n."""
    exact_order_check(a,q,n)
    mod=q**precision
    u=1
    uq=1
    for d in divisors(n):
        if d==n:
            continue
        mu=mobius(n//d)
        if not mu:
            continue
        z=(pow(a,d,mod)-1)%mod
        require(math.gcd(z,q)==1, 'proper-order factor is not a unit')
        u=u*(z if mu==1 else pow(z,-1,mod))%mod
        uq=uq*(z if mu==1 else pow(z,-1,q))%q
    ph=((pow(a,n,mod)-1)*u)%mod
    der=n*pow(a,n-1,q)*uq%q
    require(der!=0, 'primitive root derivative must be a unit')
    return ph,der

def hensel_record(q: int) -> dict[str,int]:
    n=order(5,q)
    ph,der=primitive_phi_mod(5,q,n,2)
    Q=(pow(5,q-1,q*q)-1)//q
    A=(pow(5,n,q*q)-1)//q
    require(Q == ((q-1)//n*A)%q, 'Fermat quotient factor')
    require(Q == (-ph//q*pow(5*der,-1,q))%q,
            'normalized cyclotomic/Fermat identity')
    t=-(ph//q)*pow(der,-1,q)%q
    require(t==5*Q%q, 'Hensel identity')
    omega=pow(5,q,q*q)
    require(omega==(5+q*t)%(q*q), 'Teichmuller congruence')
    require(pow(omega,n,q*q)==1, 'lift is not an n-th root')
    # Exact order persists because reduction modulo q has order n.
    return dict(q=q,n=n,phi_mod_q2=ph,derivative_mod_q=der,
                Q=Q,hensel_digit=t,omega_mod_q2=omega)

def closure(q: int) -> tuple[list[int], list[dict[str,Any]]]:
    terminals:set[int]=set()
    seen:set[int]=set()
    records:list[dict[str,Any]]=[]
    def walk(p: int) -> None:
        require(prime(p), 'closure label not prime')
        if p==3 or p%4==1:
            terminals.add(p)
            return
        if p in seen:
            return
        seen.add(p)
        rec=lift_record(5,p)
        records.append(rec)
        for k,_ in factors(rec['order']):
            if k!=2:
                require(k<p, 'order edge not descending')
                walk(k)
    walk(q)
    return sorted(terminals),sorted(records,key=lambda t:t['q'])

def pairwise_family_check() -> int:
    """Symbolic exact-index tests, not 1128 huge-integer gcd computations."""
    ns=sorted(r*d for r in R for d in D)
    require(len(set(ns))==48, 'family indices collide')
    for a,b in itertools.combinations(ns,2):
        if b%a:
            continue
        ff=factors(b//a)
        if len(ff)!=1:
            continue
        p=ff[0][0]
        # Only this prime could be shared, by the cyclotomic resultant theorem.
        require(p in (2,3,7), 'unexpected prime-power ratio')
        if p==2:
            require(a & (a-1) != 0, 'smaller index is a power of two')
        else:
            f=order(5,p)
            m=a
            while m%p==0:
                m//=p
            require(m!=f, 'possible common index prime not excluded')
    return len(ns)*(len(ns)-1)//2

def small_valuation_checks() -> dict[str,int]:
    # A bounded unit test of the universal valuation formula; not its proof.
    count=0
    pp=[2,3,7,11,13,19,31,43]
    for n in range(1,61):
        v=evaluate(cyclotomic(n),5)
        for p in pp:
            actual=valuation(v,p)
            if p==2:
                expected=2 if n==1 else (1 if n&(n-1)==0 else 0)
            else:
                f=order(5,p)
                if n==f:
                    expected=lift_record(5,p)['s']
                elif n%f==0 and n//f>1 and set(dict(factors(n//f)))=={p}:
                    expected=1
                else:
                    expected=0
            require(actual==expected, 'cyclotomic valuation regression')
            count+=1
    return {'indices':60,'valuation_equalities':count}

def mutation_tests() -> int:
    n=0
    cases=[lambda:exact_order_check(5,7,42),
           lambda:exact_order_check(5,43,21),
           lambda:exact_order_check(5,49,42),
           lambda:require(EXPECTED_KAPPA[0][0]+1==31,'wrong kappa'),
           lambda:require(pow(5,42,43*43)==1,'regular 43 mislabeled'),
           lambda:require(2882381==5,'variable base mislabeled as base five')]
    for fn in cases:
        try:
            fn()
        except CheckFailure:
            n+=1
        else:
            raise CheckFailure('mutation was not rejected')
    return n

def run() -> dict[str,Any]:
    require(D==divisors(42), 'multiplier set is not the divisor set')
    # Rebuild the six-relay gate from four complete SMALL products.
    first={7:(19531,),14:(29,449),21:(379,519499),42:(7,43,127,7603)}
    recovered=set()
    first_rows=[]
    for d,ps in first.items():
        require(all(prime(p) for p in ps), 'first-layer factor primality')
        require(math.prod(ps)==evaluate(cyclotomic(d),5),'first-layer product')
        for p in ps:
            nn=order(5,p)
            first_rows.append(dict(index=d,p=p,order=nn,admitted=p%4==3))
            if p%4==3 and nn==d:
                require(lift_record(5,p)['s']==1, 'first relay nonregular')
                recovered.add(p)
    require(recovered==set(R), 'recovered relay set mismatch')
    require(tuple(order(5,r) for r in R)==EXPECTED_ORDERS,'relay orders')
    prod=(1,)
    for d in D:
        prod=multiply(prod,cyclotomic(d))
    require(prod==(-1,)+(0,)*41+(1,), 'small cyclotomic product identity')
    rows=[]
    for ir,r in enumerate(R):
        f=order(5,r)
        rr=[]
        for j,d in enumerate(D):
            C,e=normalized_polynomial_route(r,d,f)
            C2,e2=normalized_mobius_route(r,r*d)
            require((C,e)==(C2,e2), 'two normalization routes disagree')
            require(C%r==1, 'normalized primitive product not 1 mod r')
            k=(C-1)//r
            require(k==EXPECTED_KAPPA[ir][j] and k!=0,'kappa mismatch/zero')
            if not e:
                F=evaluate(cyclotomic(d),5)
                der=evaluate(derivative(cyclotomic(d)),5)
                require(math.gcd(F*der,r)==1,'nonexceptional derivative/unit')
                Q=(pow(5,r-1,r*r)-1)//r
                require(k==5*Q*der*pow(F,-1,r)%r,'Taylor coefficient formula')
            rr.append(dict(d=d,n=r*d,index_prime_exponent=e,
                           C_mod_r2=C,kappa=k))
        H=(pow(5,42,r*r)-1)//r
        require(H!=0,'42-lifting coefficient vanishes')
        aggregate=(-H*pow(2,-1,r))%r
        require(sum(t['kappa'] for t in rr)%r==aggregate,'aggregate balance')
        require(math.prod([t['C_mod_r2'] for t in rr])%(r*r)==1+r*aggregate,
                'aggregate unit product')
        rows.append(dict(r=r,order=f,relay_record=lift_record(5,r),
                         H_42=H,aggregate_kappa=aggregate,cases=rr))
    controls=[]
    expected={20771:(10385,[3,5],10626),40487:(40486,[3,653],12312),
              1645333507:(1645333506,[3,761,1429],1624266569)}
    for q,(n,tt,coef) in expected.items():
        rec=lift_record(5,q)
        require(rec['order']==n and rec['s']==2,'known nonregular order/s')
        require(rec['next_lift_coefficient']==coef,'known q^3 coefficient')
        t,cc=closure(q)
        require(t==tt,'terminal closure mismatch')
        require(all(z['s']==1 for z in cc if z['q']!=q),
                'proper admitted descendant unexpectedly nonregular')
        controls.append(dict(**rec,terminals=t,admitted_closure=cc))
    hs=[hensel_record(q) for q in (3,7,*R,*expected)]
    unique=[]
    for q in (7,43):
        n=order(5,q)
        hits=[t for t in range(q) if pow(5+q*t,n,q*q)==1]
        require(hits==[5*((pow(5,q-1,q*q)-1)//q)%q], 'unique Hensel lift')
        unique.append(dict(q=q,digits_checked=q,hits=hits))
    base=2882381
    require(base!=5 and (base-5)%(4*3**2*7**2)==0,'CRT lower preservation')
    require(base%(43*43)==pow(5,43,43*43),'CRT upper lift')
    cr=[lift_record(base,p) for p in (3,7,43)]
    require([(z['order'],z['s']) for z in cr]==[(2,1),(6,1),(42,2)],
            'variable-base countermodel fails')
    require(cr[-1]['next_lift_coefficient']==27,'countermodel exact s')
    return {
        'schema':'A303656_C1_TERMINAL_PHASE_E_REFERENCE_V1',
        'status':'PASS',
        'authority':{'repository':'Samsen879/a303656',
                     'main_sha':'fd59aad038a09f2fc6df7039111408fa231c27dd',
                     'main_tree':'afd34fc936f83867758c827bfcd8b7b9d9b8d5b5'},
        'multiplier_divisors_42':D,'relays':R,
        'first_layer_complete_factor_occurrences':first_rows,
        'family_rows':rows,'pairwise_index_checks':pairwise_family_check(),
        'known_nonregular_sanity':controls,'hensel_checks':hs,
        'unique_lift_enumerations':unique,
        'variable_base_countermodel':{'base':base,'NOT_BASE_FIVE':True,'rows':cr},
        'small_valuation_regressions':small_valuation_checks(),
        'rejected_mutations':mutation_tests(),
        'inherited_phase_d_exclusions_NOT_REPROVED':EXCLUDED_BY_PHASE_D,
        'new_excluded_indices':[],
        'remaining_three_vertex_indices':[r*d for r in R for d in D
                                            if r*d not in EXCLUDED_BY_PHASE_D],
        'claims':{'any_new_complete_B7_family_dead':False,
                  'B7_empty_proved':False,'new_terminal_pruning':False,
                  'general_B7_height_bounded':False,
                  'full_repository_replay':False,
                  'all_files_in_requested_directories_read':False,
                  'github_writes':False}
    }

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('evidence.json'))
    p.add_argument('--self-test',action='store_true',help='All tests also run by default.')
    a=p.parse_args()
    try:
        out=run()
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    except (CheckFailure,OSError,ValueError) as e:
        print(f'FAIL: {e}',file=sys.stderr)
        return 1
    print('PASS: 48 two-route residue cases; 1128 structural index-pair checks;')
    print('3 mandatory nonregular controls and closures; 11 Hensel identities;')
    print('50 lift digits; 480 valuation checks; 6 rejected mutations.')
    print('New B7 excluded indices: NONE. GitHub writes: NONE.')
    print(f'Evidence: {a.output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
