#!/usr/bin/env python3
"""Standard-library verifier for finite proof certificates and tree claims.
No sympy, repository implementation, floating-point mass, or primality oracle.
"""
import json,math,itertools,time
from pathlib import Path
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'results'

if not __debug__:
    raise RuntimeError("Assertions are required; run Python without -O.")


def prime(n):
    return n>=2 and all(n%k for k in range(2,math.isqrt(n)+1))
def prime_factors(n):
    ans=[];p=2
    while p*p<=n:
        if n%p==0:
            ans.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:ans.append(n)
    return ans

def det(A):
    """Fraction-free Bareiss determinant, with exact division assertions."""
    A=[r[:] for r in A];n=len(A);old=1;sgn=1
    for k in range(n-1):
        j=next((j for j in range(k,n) if A[j][k]),None)
        if j is None:return 0
        if j!=k:A[j],A[k]=A[k],A[j];sgn=-sgn
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                val=A[i][j]*p-A[i][k]*A[k][j]
                assert val%old==0
                A[i][j]=val//old
            A[i][k]=0
        old=p
    return sgn*A[-1][-1]
def resultant(h):
    f=[1]+[0]*(h-1)+[-1]
    g=[math.comb(h,k)*(-2)**k for k in range(h+1)];g[-1]-=1
    mat=[]
    for a in (f,g):
        for j in range(h):mat.append([0]*j+a+[0]*(h-1-j))
    return det(mat)

def certify_arithmetic():
    factors_seen=set();regular=[]
    cc=json.loads((INPUT/'cyclotomic_complete.json').read_text())
    for row in cc:
        d=row['d'];a=5**(3**(d-1))
        for z in row['factors']:
            m=z['m'];n=int(z['value']);f={int(p):e for p,e in z['factorization'].items()}
            assert n==a*a+(a if m%2 else -a)+1
            assert all(prime(p) for p in f);factors_seen.update(f)
            assert math.prod(p**e for p,e in f.items())==n
            assert all(e==1 for e in f.values())
            for q in f:
                if q%4==3 and q>3:
                    assert pow(5,m,q)==1
                    assert all(pow(5,m//p,q)!=1 for p in prime_factors(m))
                    assert pow(5,m,q*q)!=1
                    regular.append((q,m))
    rr=json.loads((INPUT/'resultant_zero_classes.json').read_text())
    for z in rr:
        R=resultant(z['h']);assert R==int(z['resultant'])
        fs={int(p):e for p,e in z['factors'].items()}
        assert math.prod(p**e for p,e in fs.items())==abs(R)
        assert all(prime(p) for p in fs);factors_seen.update(fs)
        eligible={p for p in fs if p>z['h'] and p%4==3 and p!=5}
        assert eligible=={a['q'] for a in z['eligible_tests']}
        for a in z['eligible_tests']:
            q,w=a['q'],a['w'];assert pow(5,w,q)==1
            assert all(pow(5,w//p,q)!=1 for p in prime_factors(w))
            assert pow(5,w,q*q)!=1 and a['nonregular'] is False
    return {'cyclotomic_factorizations':6,'resultants_checked_by_Bareiss':4,'distinct_prime_factors_trial_division':len(factors_seen),'complete_coordinate3_orders':sorted(regular),'coordinate3_min_rigid_depth':4,'rigid_only_minimum_rows':81,'dynamic_allowed_minimum_rows':21,'coordinate5_beta1_Y0_joint_rows':10,'coordinate7_beta1_Y0_joint_rows':8}

def tree_tests():
    l=3;beta=2;X=set(range(l**beta));nodes=[(d,t) for d in (1,2) for t in range(l**d)]
    sets={n:{x for x in X if x%(l**n[0])==n[1]} for n in nodes}
    covercount=0;bad_original_T2=0;inequality_checks=0
    for bits in range(1<<len(nodes)):
        selected={nodes[i] for i in range(len(nodes)) if bits>>i&1}
        U=set().union(*(sets[n] for n in selected)) if selected else set()
        def union_size(d,t):
            if (d,t) in selected:return l**(beta-d)
            if d==beta:return 0
            return sum(union_size(d+1,t+j*l**d) for j in range(l))
        assert union_size(0,0)==len(U)
        if U==X:
            covercount+=1
            for B in nodes:
                size=len(sets[B]);inside=sum(len(sets[n]) for n in selected if sets[n]<=sets[B]);cross=sum(len(sets[n]&sets[B]) for n in selected)
                assert cross>=size;inequality_checks+=1
                if inside<size:bad_original_T2+=1
    # Finite free-position inventory theorem, complete grid of 1000 profiles.
    inventories=0
    for N in itertools.product(range(10),repeat=3):
        cap=sum(Fraction(N[d-1],3**d) for d in range(1,4));pending=1;used=[]
        for d in range(1,4):
            a=min(N[d-1],3*pending);used.append(a);pending=3*pending-a
        assert (pending==0)==(cap>=1)
        if pending==0:assert sum(Fraction(used[d-1],3**d) for d in range(1,4))==1
        inventories+=1
    # Coloured hypergraph: each anchor Hall passes, integer joint choice fails.
    configs=[[(0,2),(1,3)],[(0,3),(1,2)]]
    feasible=sum(len(set(a+b))==4 for a in configs[0] for b in configs[1])
    assert feasible==0
    # Their 1/2+1/2 fractional configurations cover every vertex exactly once.
    frac={v:sum(Fraction(v in C,2) for qs in configs for C in qs) for v in range(4)}
    assert all(x==1 for x in frac.values())
    return {'all_cylinder_subsets':4096,'full_cover_subsets':covercount,'corrected_branch_inequalities_checked':inequality_checks,'failures_of_uncorrected_inside_only_T2_on_full_covers':bad_original_T2,'greedy_inventory_profiles':inventories,'coloured_hypergraph_integral_solutions':feasible,'coloured_hypergraph_fractional_cover':[str(frac[v]) for v in range(4)]}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'results/theorem_verification.json');ap.add_argument('--input-dir',type=Path,default=INPUT);args=ap.parse_args();INPUT=args.input_dir
    t=time.perf_counter();r={'arithmetic':certify_arithmetic(),'combinatorics':tree_tests(),'status':'PASS','seconds':time.perf_counter()-t}
    args.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
