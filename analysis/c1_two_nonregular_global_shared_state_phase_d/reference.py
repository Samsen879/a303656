#!/usr/bin/env python3
"""Deterministic Phase-D laboratory. Does not import any repository code.
Python >=3.10. SymPy is used only for exact integer resultants.
Run: python reference.py --output /path/to/new-output
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb, gcd, isqrt, lcm, prod
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def is_prime(n: int) -> bool:
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, isqrt(n) + 1, 2))


def factors(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1: out[n] = out.get(n, 0) + 1
    return out


def order(q: int) -> int:
    assert is_prime(q) and q != 5
    w = q-1
    for p in factors(w):
        while w % p == 0 and pow(5, w//p, q) == 1: w //= p
    assert pow(5, w, q) == 1
    assert all(pow(5, w//p, q) != 1 for p in factors(w))
    return w


def lift(q: int, w: int) -> int:
    s = 1
    while pow(5, w, q**(s+1)) == 1: s += 1
    return s


def crt(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    g = gcd(m,n)
    if (b-a) % g: raise ValueError('inconsistent CRT')
    v = n//g
    k = ((b-a)//g * pow(m//g,-1,v)) % v if v > 1 else 0
    return (a+m*k) % lcm(m,n), lcm(m,n)


def fatal(q: int, r: int, c: int, d: int) -> bool:
    v = (r-(1 if c == 0 else 3)-pow(5,d,q*q)) % (q*q)
    return v != 0 and v % q == 0


def powers(q: int, n: int, K: int = 2) -> list[int]:
    x, out = 1, []
    for _ in range(n):
        out.append(x)
        x = (5*x) % (q**K)
    return out


def named_arithmetic() -> list[dict]:
    out=[]
    for q in (3,7,11,19,31,67,20771,40487):
        w=order(q); s=lift(q,w)
        out.append(dict(q=q,w=w,s=s,order_factors=factors(w)))
    assert [(x['q'],x['w'],x['s']) for x in out[-2:]] == [(20771,10385,2),(40487,40486,2)]
    return out


def fiber_audit() -> dict:
    U=lcm(2,3,10385,40486); M=U//31
    fixed={3:2,20771:20773,40487:40493}
    ds=[[crt(y,M,x,31)[0] for x in range(31)] for y in (0,437511)]
    rigid=[[[q for q,r in fixed.items() if any(fatal(q,r,c,d) for c in (0,1))]
            for d in f] for f in ds]
    assert [i for i,x in enumerate(rigid[0]) if x] == [0]
    assert [i for i,x in enumerate(rigid[1]) if x] == [1]
    choices=[[],[]]; hist=Counter()
    for r in range(961):
        covered=[sum(bool(rigid[j][k]) or any(fatal(31,r,c,d) for c in (0,1))
                     for k,d in enumerate(f)) for j,f in enumerate(ds)]
        for j,n in enumerate(covered):
            if n==31: choices[j].append(r)
        hist[sum(covered)]+=1
    assert choices==[[2,4],[684,686]]
    assert hist=={2:899,60:58,61:4}
    return dict(U=U,L=U,lower_modulus=M,lower_representatives=[0,437511],
                fixed_residues=fixed,individual_complete_states=choices,
                combined_complete_states=0,coverage_histogram=dict(sorted(hist.items())),
                tested_states=961,tested_cells_per_state=62)


def center_role_audit() -> dict:
    totals=[]
    for p,K in ((3,3),(7,3),(11,2)):
        w=order(p); period=w*p**(K-1)
        # Build masks from directly enumerated full zero centers, not CRT targets.
        actual={}
        for c in (0,1):
            for d,a in enumerate(powers(p,period,K)):
                r=((1 if c==0 else 3)+a)%(p**K)
                for m in range(1,K):
                    role=(c,d%w,d%(p**m),m)
                    actual[role]=actual.get(role,0)|(1<<r)
        predicted={}
        for role,mask in actual.items():
            c,b,z,m=role
            t,_=crt(b,w,z,p**m)
            A=((1 if c==0 else 3)+pow(5,t,p**(m+1))) % (p**(m+1))
            expected=sum(1<<r for r in range(A,p**K,p**(m+1)))
            assert mask==expected
            predicted[role]=(A,p**(m+1))
        checks=0
        for (role1,mask1),(role2,mask2) in combinations(actual.items(),2):
            A,m=predicted[role1]; B,n=predicted[role2]
            assert bool(mask1&mask2) == ((A-B)%gcd(m,n)==0)
            checks+=1
        totals.append(dict(p=p,K=K,roles=len(actual),pair_checks=checks))
    assert pow(5,21,49)==48
    assert (1+pow(5,0,49))%49 == (3+pow(5,21,49))%49 == 2
    return dict(enumerations=totals,compatible_mixed_anchor_example=dict(p=7,K=2,r=2,d0=0,d1=21,center=0))


def terminal_pair_audit() -> dict:
    out=[]
    for q in (20771,40487):
        w=order(q); pw=powers(q,w)
        log={a%q:b for b,a in enumerate(pw)}
        pairs=[]
        for b,a in enumerate(pw):
            b1=log.get((a-2)%q)
            if b1 is None: continue
            A0=(1+a)%(q*q); A1=(3+pw[b1])%(q*q)
            assert (A0-A1)%q==0
            residues=[(A0+q*k)%(q*q) for k in range(3)]
            good=[r for r in residues if r!=A0 and r!=A1]
            assert good
            r=good[0]
            assert fatal(q,r,0,b) and fatal(q,r,1,b1)
            pairs.append((b,b1))
        assert len(pairs)==(5192 if q==20771 else 40485)
        out.append(dict(q=q,w=w,legal_oriented_pairs=len(pairs),constructed_all=True))
    return dict(K=2,E=[1],roots=out)


def two_root_configuration() -> dict:
    q1,q2=20771,40487; w1,w2=order(q1),order(q2)
    U=lcm(w1,w2); g=gcd(w1,w2)
    states1=[16,17555,20773]; states2=[25919,40493,40489]
    allsets=[]
    for q,w,states in ((q1,w1,states1),(q2,w2,states2)):
        pw=powers(q,w)
        allsets.append([{b for b,a in enumerate(pw)
                         if any(0!=(r-h-a)%(q*q) and (r-h-a)%q==0 for h in (1,3))}
                        for r in states])
    rows=[]
    for i,r1 in enumerate(states1):
        B1=allsets[0][i]
        # For each q2-log, explicitly count compatible q1 safe logs.
        trace={b for b in range(w2) if w1//g > sum(a%g==b%g for a in B1)}
        assert len(trace)==w2
        for j,r2 in enumerate(states2):
            B2=allsets[1][j]
            intersections=sum((a-b)%g==0 for a in B1 for b in B2)
            covered=len(B1)*(U//w1)+len(B2)*(U//w2)-intersections
            assert (covered==U) == trace.issubset(B2)
            rows.append(dict(r1=r1,r2=r2,B1=sorted(B1),B2=sorted(B2),
                             covered=covered,full_period=U,complete=False))
    return dict(scope='ACTUAL whole-domain two-root K2 ledger, no regular support',
                states=len(rows),trace_size=w2,rows=rows)


def fractional_regression() -> dict:
    U=1302
    fams={3:[2+3*k for k in range(3)],
          7:[a+7*k for a in (2,5,6) for k in range(7)],
          31:[a+31*k for a in (2,6,26) for k in range(31)]}
    masks={}; inc={}
    for q,fam in fams.items():
        pw=powers(q,U); masks[q]=[]; inc[q]=[0]*U
        for r in fam:
            mask=0
            for d,a in enumerate(pw):
                yes=any(0!=(r-h-a)%(q*q) and (r-h-a)%q==0 for h in (1,3))
                if yes: mask|=1<<d;inc[q][d]+=1
            masks[q].append(mask)
    for d in range(U):
        assert sum(Fraction(inc[q][d],len(fams[q])) for q in fams)==Fraction(830,651)
    hist=Counter(); full=(1<<U)-1; count=0
    for i,j,k in product(range(3),range(21),range(93)):
        bad=full^(masks[3][i]|masks[7][j]|masks[31][k])
        hist[bad.bit_count()]+=1
        assert bad
        a=(bad&-bad).bit_length()-1
        d,_=crt(a,U,0,43*1303)
        rs={3:fams[3][i],7:fams[7][j],31:fams[31][k],43:2,1303:2}
        assert not any(fatal(q,r,c,d) for q,r in rs.items() for c in (0,1))
        count+=1
    assert dict(hist)=={2:217,14:434,38:868,62:434,218:868,224:868,248:868,434:1302}
    # Exactly-two extension uses honest but deliberately inert nonregular rows.
    zero_states={}
    for q in (20771,40487):
        w=order(q); pw=powers(q,w)
        bs=[b for b,a in enumerate(pw) if a%q==(q-2)]
        assert len(bs)==1
        r=(3+pw[bs[0]])%(q*q)
        assert r%q==1
        assert all(not any(0!=(r-h-a)%(q*q) and (r-h-a)%q==0 for h in (1,3)) for a in pw)
        zero_states[q]=r
    U2=lcm(U,10385,40486);L2=U2*43*1303
    return dict(source_regression=dict(states=count,U=U,escape_histogram=dict(sorted(hist.items())),
                                       uniform_fraction='830/651',full_witnesses=count),
                exactly_two_extension=dict(nonregular_zero_states=zero_states,U=U2,L=L2,
                                            coarse_pooled_incidence_kernel=1302,complete_integral=False,
                                            caveat='Both added nonregular rows are inert; not a cooperative-cover example.'))


def resultants_audit() -> dict:
    import sympy as sp
    T,Z=sp.symbols('T Z');h=67
    E=sum(comb(h,2*k)*Z**k for k in range((h-1)//2+1))
    O=sum(comb(h,2*k+1)*Z**k for k in range((h-1)//2+1))
    remainder=sp.Poly(Z*O**2,Z,domain=sp.QQ).rem(sp.Poly(E,Z,domain=sp.QQ))
    vals=[];bits=[]
    for Y in (7,8):
        A=5**(Y*h)
        direct=int(sp.resultant(T**h-A,(T-2)**h-A,T))
        P=sp.Poly(A*A,Z,domain=sp.QQ)-remainder
        half=(-2)**h*sp.resultant(E,P,Z)*h**(h-P.degree())
        assert half.q==1 and direct==int(half)
        stored=int((HERE/f'R67_{Y}.hex').read_text().strip(),16)
        assert direct==stored
        vals.append(direct);bits.append(abs(direct).bit_length())
    G=gcd(*vals)
    f={2:67,269:15,1609:3,1877:4,3083:1,4289:1,4691:1,5897:1,7639:1,20771:1,27337:1}
    assert all(is_prime(p) for p in f)
    assert G==prod(p**e for p,e in f.items())
    assert G==int((HERE/'R67_7_8_gcd.txt').read_text())
    V=(5**67-1)//4
    assert gcd(G,V)==269*1609==432821
    assert all(p%4==1 for p in (269,1609))
    q=20771
    paired=[]
    for Y,b0,b1,r in ((7,2177,9772,16),(8,1558,10238,17555)):
        assert b0%155==b1%155==Y
        assert (pow(5,b0,q)-pow(5,b1,q))%q==2
        assert fatal(q,r,0,b0) and fatal(q,r,1,b1)
        paired.append(dict(Y=Y,b0=b0,b1=b1,r=r))
    assert (162-7)%155==0
    assert G%q==0 and (8-7)%155!=0
    return dict(h=67,Y=[7,8],signed_hex_files=['R67_7.hex','R67_8.hex'],bits=bits,
                exact_gcd=str(G),gcd_factorization=f,gcd_with_V67_1=432821,
                admitted_common_order_suppliers=0,paired_individual_examples=paired,
                compatible_reuse_lower_classes=[7,162],
                cross_checks=['direct integer resultant','half-degree exact resultant identity',
                              'Euclidean integer gcd','trial-division factor primality'],
                sympy_version=sp.__version__)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--skip-resultants',action='store_true')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    checks=[('named_arithmetic',named_arithmetic),('two_fiber_collision',fiber_audit),
            ('center_roles',center_role_audit),('terminal_pairs',terminal_pair_audit),
            ('two_root_configuration',two_root_configuration),('fractional_regression',fractional_regression)]
    if not args.skip_resultants: checks.append(('resultants',resultants_audit))
    out={}
    for name,fn in checks:
        out[name]=fn()
        print(name+': PASS',flush=True)
    out['scope']={'GitHub_writes':'NONE','repository_native_replay':False,
                  'unbounded_theorems_proved_by_finite_tests':False,
                  'actual_whole_odd_pooled_cover_found':False}
    (args.output/'RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
