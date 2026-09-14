#!/usr/bin/env python3
"""Phase I: exact, bounded reference generator. Python 3.10+, standard library.

This generates ONE ACTUAL PARTIAL ledger with N=3, and separately records
conditional N=8/N=9 architectures. Uninstantiated slots are never prime rows.
No network, no GitHub writes, no unbounded prime scan.
"""
from __future__ import annotations
import itertools, json, math, sys, time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(100000)
HERE = Path(__file__).resolve().parent
BOUND = 970453984500000
ROOTS = (20771, 40487, 1645333507)

def require(ok: bool, message: str) -> None:
    if not ok: raise ValueError(message)

def dump(name: str, obj: object) -> None:
    (HERE/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

@lru_cache(None)
def factor(n: int) -> dict[int,int]:
    require(n >= 1, 'factor domain')
    ans = {}; d = 2
    while d*d <= n:
        if n % d == 0:
            e=0
            while n%d==0: n//=d; e+=1
            ans[d]=e
        d = 3 if d==2 else d+2
    if n>1: ans[n]=1
    return ans

@lru_cache(None)
def prime(p: int) -> bool:
    return p >= 2 and factor(p)=={p:1}

@lru_cache(None)
def arithmetic(p: int) -> dict:
    require(prime(p) and p!=5, f'not an eligible prime: {p}')
    w=p-1
    for ell in factor(w):
        while w%ell==0 and pow(5,w//ell,p)==1: w//=ell
    s=1
    while pow(5,w,p**(s+1))==1: s+=1
    return {'p':p,'prime_proof':'complete trial division through integer square root',
            'admitted':p%4==3,'w':w,'order_factorization':factor(w),
            's':s,'kind':'nonregular' if s>=2 else 'regular',
            'pow_5_w_mod_p2':pow(5,w,p*p),
            'pow_5_w_mod_p3':pow(5,w,p**3),
            'order_minimality_residues':{ell:pow(5,w//ell,p) for ell in factor(w)}}

@lru_cache(None)
def closure(q: int) -> tuple[tuple[int,...],tuple[int,...]]:
    if q==3 or q%4==1: return (), (q,)
    require(prime(q) and q%4==3, 'bad admitted closure label')
    vertices={q}; terminals=set()
    for p in factor(arithmetic(q)['w']):
        if p==2: continue
        vs,ts=closure(p); vertices.update(vs); terminals.update(ts)
    return tuple(sorted(vertices)), tuple(sorted(terminals))

def crt(pairs: list[tuple[int,int]]) -> tuple[int,int]:
    x=0; M=1
    for modulus,residue in pairs:
        require(math.gcd(M,modulus)==1, 'CRT moduli are not coprime')
        x += M*((residue-x)*pow(M,-1,modulus)%modulus)
        M *= modulus
    return x%M, M

def crt_weights(moduli: list[int]) -> tuple[int,list[int]]:
    M=math.prod(moduli)
    return M, [(M//m)*pow(M//m,-1,m) for m in moduli]

def canonical_module(q: int, parity: int, terminal_residues: dict[int,int]) -> dict:
    vs,ts=closure(q); R=[p for p in vs if p!=q]
    require(arithmetic(q)['s']>=2, 'root is not nonregular')
    require(all(arithmetic(p)['s']==1 for p in R), 'nonregular interior')
    W=math.lcm(*(arithmetic(p)['w'] for p in vs))
    wf=factor(W)
    require(all(wf.get(p,0)<=1 for p in R), 'private depth is not one')
    boundary={p:p**e for p,e in wf.items() if p not in R}
    # A parity is retained even if all row periods happen to be odd.
    constraints=[(2,parity)]
    for t in ts:
        require(t in terminal_residues,'missing terminal state')
        constraints.append((boundary[t], terminal_residues[t]))
    constraints += [(p,0) for p in R]
    a,A=crt(constraints)
    local={p:(3+pow(5,a,p*p)+(p if p==q else 0))%(p*p) for p in vs}
    profile=[{'modulus':m,'residue':a%m} for p,m in sorted(boundary.items())]
    return {'module_id':f'q{q}', 'root':q, 'actual':True,
            'vertices':list(vs),'regular_helpers':R,'terminals':list(ts),
            'all_orders_odd':all(arithmetic(p)['w']%2 for p in vs),
            'boundary_log_modulus':math.prod(boundary.values()),
            'canonical_a':a,'canonical_a_modulus':A,'local_residues':local,
            'whole_private_fiber_profile':profile,
            'private_centers':{p:0 for p in R},
            'earliest_terminal_count_eligibility':max(ts)}

def event(row: dict,c: int,d: int) -> bool:
    p=row['p']; v=(row['r']-3**c-pow(5,d,p*p))%(p*p)
    return v!=0 and v%p==0

def module_profile(module: dict,d: int) -> bool:
    return all(d%x['modulus']==x['residue'] for x in module['whole_private_fiber_profile'])

def cylinder_hit(d: int, cylinder: list[dict]) -> bool:
    return all(d%x['modulus']==x['residue'] for x in cylinder)

def raw_normal(row: dict,d: int) -> bool:
    if d%row['w'] != row['log_c1']: return False
    return row['s']>=2 or d%row['p']!=row['center_c1']

@lru_cache(None)
def divisors(n: int) -> tuple[int,...]:
    ds=[1]
    for p,e in factor(n).items(): ds=[d*p**j for d in ds for j in range(e+1)]
    return tuple(sorted(ds))

@lru_cache(None)
def phi_value(n: int) -> int:
    z=5**n-1
    for d in divisors(n):
        if d<n:
            y=phi_value(d); z,r=divmod(z,y)
            require(r==0,'cyclotomic division failed')
    return z

def conditional_architecture(N: int) -> dict:
    require(N in (8,9),'only frozen N=8/9 architectures')
    # Each tuple: slot name, exact root order, actual regular support,
    # retained 3-depth, leaf, chosen parity. Slots are NOT original prime rows.
    common=[('B7',903,[7,43],1,1,0),('H19',191,[19,191],2,2,0),
            ('H5167',5167,[5167],2,5,0),('H271',271,[271],3,8,0),
            ('H4159',4159,[4159],3,17,0),('H31051',31051,[31051],3,26,0)]
    if N==8:
        specs=[('31-even',1303,[31,1303],1,0,0),
               ('31-odd',258065887,[31,258065887],1,0,1)]+common
    else:
        specs=[(f'31-split-{j}',279,[31],2,3*j,0) for j in range(3)]+common
    rows={}; slots=[]
    for name,n,R,e,leaf,b in specs:
        a,A=crt([(2,b),(3**e,leaf)]+[(p,0) for p in R])
        for p in R:
            require(arithmetic(p)['s']==1,'conditional helper not regular')
            r=(3+pow(5,a,p*p))%(p*p)
            if p in rows: require(rows[p]['r']==r,'shared helper state conflict')
            rows[p]={'p':p,'K':2,'E':[1],'r':r,'w':arithmetic(p)['w'],
                     'log_c1':a%arithmetic(p)['w'],'center_c1':a%p,
                     's':1,'original_row':True}
        qR=set()
        for p in factor(n):
            if p!=2: qR.update(closure(p)[0])
        require(qR==set(R),'frozen root-order closure does not equal support')
        slots.append({'slot_id':name,'entry_type':'UNINSTANTIATED_TERMINAL_SLOT',
                      'original_row':False,'prime_value':None,
                      'required_exact_order':n,'required_s_min':2,
                      'required_prime_congruence':[4,3], 'regular_support':R,
                      'root_log_c1':a%n,'canonical_a':a,'canonical_a_modulus':A,
                      'local_residue_recipe':'(3 + pow(5, a, q*q) + q) % (q*q)',
                      'designated_even_leaf':{'depth':e,'residue':leaf},
                      'designated_parity':b})
    private=sorted(rows)
    roots_counter={}
    for s in slots:
        n=s['required_exact_order']; roots_counter[n]=roots_counter.get(n,0)+1
    return {'N':N,'actual_complete_certificate':False,'conditional_only':True,
            'scope':'IFF for instantiating THIS frozen architecture, not all N certificates',
            'regular_rows':list(rows.values()),'terminal_slots':slots,
            'private_primes':private,
            'square_hit_demands':[{'n':n,'distinct_admitted_primitive_square_divisors_required':k}
                                  for n,k in sorted(roots_counter.items())],
            'root_in_B31_odd_required':False,
            'conditional_odd_row_count':N+len(private)+1,
            'materialize_largest_target': N==9}

def check_conditional(arch: dict) -> dict:
    R=arch['private_primes']; moduli=[2,27]+R; L,weights=crt_weights(moduli)
    checks=0
    for b,z in itertools.product(range(2),range(27)):
        for bits in itertools.product(range(2),repeat=len(R)):
            d=sum(x*w for x,w in zip((b,z)+bits,weights))%L
            regular=any(raw_normal(r,d) for r in arch['regular_rows'])
            # These are FORMAL GUARDS with an explicit square-hit hypothesis.
            terminal=any(d%s['required_exact_order']==s['root_log_c1']
                         for s in arch['terminal_slots'])
            row3=b==1 and z%3!=0
            require(regular or terminal or row3, f'conditional coverage hole N={arch["N"]}')
            checks+=1
    return {'N':arch['N'],'formal_guard_cells':checks,
            'conditional_BOTH_mask_identity':True,'actual_terminal_primes_verified':0,
            'actual_complete_certificate':False}

def terminal_peel(signatures: dict[str,list[int]]) -> dict:
    S=set(signatures); history=[]
    while S:
        m=len(S); remove=sorted(q for q in S if max(signatures[q])>m)
        history.append({'current_count':m,'removed':remove})
        if not remove: break
        S.difference_update(remove)
    return {'remaining':sorted(S),'history':history}

def main() -> None:
    (HERE/'targets').mkdir(exist_ok=True)
    start=time.monotonic()
    modules=[canonical_module(20771,0,{3:0,5:0}),
             canonical_module(40487,1,{3:0,653:0}),
             canonical_module(1645333507,0,{3:1,761:0,1429:0})]
    residues={3:2}; provenance={3:['boundary-row-3']}; log={3:1}; center={3:0}
    for m in modules:
        for p,r in m['local_residues'].items():
            if p in residues: require(residues[p]==r,'actual shared-state conflict')
            residues[p]=r; provenance.setdefault(p,[]).append(m['module_id'])
            log[p]=m['canonical_a']%arithmetic(p)['w']; center[p]=0
    rows=[]
    for p,r in sorted(residues.items()):
        a=arithmetic(p)
        rows.append({'row_id':f'p{p}','p':p,'entry_type':'ACTUAL_ORIGINAL_PRIME_ROW',
                     'original_row':True,'K':2,'E':[1],'r':r,'w':a['w'],'s':a['s'],
                     'log_c1':log[p],'center_c1':center[p], 'module_membership':provenance[p]})
    r,M=crt([(4,1)]+[(x['p']**2,x['r']) for x in rows])
    U=math.lcm(*(x['w'] for x in rows))
    L=math.lcm(*(x['w']*x['p']**max(0,2-x['s']) for x in rows))
    require(U==L,'unexpected ambient inequality')
    boundary=[2,27,5,653,761,1429]; private=[11,31,67,1523,30469139]
    qmod=boundary+private; LL,weights=crt_weights(qmod); require(LL==L,'quotient period mismatch')
    false_cells=0; true_cells=0; weight_all=0; weight_true=0; boundary_true=0; boundary_mass=0
    for b,z,free in itertools.product(range(2),range(27),itertools.product(range(2),repeat=4)):
        vals=(b,z)+free; alld=True
        bw=math.prod(m-1 if v else 1 for m,v in zip(boundary[2:],free))
        for bits in itertools.product(range(2),repeat=len(private)):
            allvals=vals+bits; d=sum(x*w for x,w in zip(allvals,weights))%L
            normal=any(raw_normal(x,d) for x in rows)
            actual=any(event(x,1,d) for x in rows)
            require(actual==normal,'actual versus normal form disagreement')
            # c=0 is always covered by the original two-adic row r2=1 mod4.
            require((1-1-pow(5,d,4))%4==3,'A0 two-adic failure')
            wt=bw*math.prod(p-1 if bit else 1 for p,bit in zip(private,bits))
            weight_all+=wt; weight_true+=wt*actual
            true_cells+=actual; false_cells+=not actual; alld &= actual
        d0=sum(x*w for x,w in zip(vals+(0,)*len(private),weights))%L
        expected=(b==1 and z%3!=0) or any(module_profile(m,d0) for m in modules)
        require(alld==expected,'universal private-profile identity failed')
        boundary_true+=alld; boundary_mass+=bw*alld
    require(weight_all==L,'quotient multiplicities do not cover the full period')
    # One full exponent witnessing failure of BOTH, but success of EITHER.
    escape_values=[0,2,1,1,1,1]+[0]*len(private)
    d=sum(x*w for x,w in zip(escape_values,weights))%L
    require(not any(event(x,1,d) for x in rows),'escape not safe')
    escape={'d':d,'modulus':L,'primary_coordinates':dict(zip(qmod,escape_values)),
            'anchor0_covered':True,'anchor1_covered':False,'EITHER':True,'BOTH':False,
            'local_values_c1_mod_p2':{x['p']:(x['r']-3-pow(5,d,x['p']**2))%(x['p']**2) for x in rows}}
    ledger={'schema':'a303656-phase-i-actual-partial-v1','status':'ACTUAL_PARTIAL_NOT_COMPLETE',
            'N_nonregular_original_rows':3,'regular_original_odd_rows':6,
            'total_original_odd_rows':9,'total_original_rows_including_two_adic':10,
            'anchors':[0,1],'demand':'BOTH','local_zero_accepted':False,
            'actual_complete_certificate':False,'two_adic_row':{'K':2,'r':1,'modulus':4},
            'odd_rows':rows,'global_residue':r,'global_modulus':M,'U':U,'L':L,
            'modules':modules,'boundary_moduli':boundary,'private_primes':private,
            'escape':escape}
    archs=[conditional_architecture(8),conditional_architecture(9)]
    cond=[check_conditional(a) for a in archs]
    extras=[7,19,43,191,271,1303,4159,5167,31051,258065887,21207101,28086211607]
    inventory=sorted(set(residues)|set(extras))
    terminal_primes=sorted({t for m in modules for t in m['terminals']})
    require(all(prime(p) for p in terminal_primes),'terminal not prime')
    library={'actual_modules':modules,'arithmetic_records':[arithmetic(p) for p in inventory],
             'terminal_prime_proofs':[{'p':p,'method':'complete trial division'} for p in terminal_primes],
             'later_new_nonregular_primes_instantiated':[],
             'explicit_inventory_scope':'listed primes only; no whole-range scan was rerun',
             'phi62_complete_factorization':{'value':phi_value(62),'factors':[1303,21207101,28086211607]}}
    target_metadata=[]
    for n,k in [(279,3),(903,1),(191,1),(5167,1),(271,1),(4159,1),(31051,1)]:
        C=phi_value(n); text=str(C)+'\n'; (HERE/'targets'/f'phi_{n}.txt').write_text(text)
        target_metadata.append({'n':n,'decimal_digits':len(str(C)),
                                'required_distinct_admitted_square_hits':k,
                                'file':f'targets/phi_{n}.txt'})
    C=phi_value(279); witness=pow(2,C-1,C)
    require(witness!=1,'need a separate composite certificate')
    core=terminal_peel({str(q):list(closure(q)[1]) for q in ROOTS})
    result={'success_level_unqualified':'C',
            'additional_result':'architecture-specific finite reduction for N=9; not a global completeness classification',
            'actual_complete_certificate':False,'A303656':'UNRESOLVED','github_writes_performed':'NONE',
            'actual_nonregular_origins':list(ROOTS),'actual_original_odd_rows':9,
            'actual_original_rows_including_two_adic':10,'N_actual':3,
            'actual_quotient_cells':true_cells+false_cells,
            'actual_quotient_cells_passing_BOTH':true_cells,
            'actual_quotient_cells_failing_BOTH':false_cells,
            'boundary_quotient_cells':864,'whole_private_fiber_covered_cells':boundary_true,
            'pointwise_full_period_covered_residues':weight_true,'L':L,
            'pointwise_density':str(Fraction(weight_true,L)),
            'whole_private_fiber_boundary_density':str(Fraction(boundary_mass,math.prod(boundary))),
            'conditional_architecture_checks':cond,'targets':target_metadata,
            'phi279_composite_certificate':{'base':2,'pow_base_Cminus1_mod_C':witness},
            'phi279_small_factor_trial_limit':10000,
            'phi279_no_small_factor_up_to_limit':all(C%p for p in range(2,10001) if prime(p)),
            'phi279_squarepart_status':'UNRESOLVED',
            'published_bound_dependency':BOUND,'published_bound_search_rerun':False,
            'mass_gate_minimum_for_three_unlisted_square_hits':(BOUND+1)**6,
            'terminal_peeling_of_actual_inventory':core,
            'reference_runtime_seconds':round(time.monotonic()-start,6)}
    receipts=[]
    for module in modules:
        q=module['root']; a=module['canonical_a']; current=arithmetic(q)['w']
        support={q}; steps=[]; parent={}
        for h in sorted(module['regular_helpers'],reverse=True):
            require(current%h==0 and current%(h*h)!=0,'nonlinear private step in actual module')
            provider=min(p for p in support if arithmetic(p)['w']%h==0)
            after=math.lcm(current//h,arithmetic(h)['w'])
            parent[h]=provider; ancestry=[h]
            while ancestry[-1]!=q: ancestry.append(parent[ancestry[-1]])
            steps.append({'eliminate':h,'incoming_guard_modulus':current,
                          'incoming_guard_residue':a%current,'private_center':a%h,
                          'exact_provider_original_prime':provider,'center_ancestry_path':ancestry,
                          'actual_helper_original_prime':h,
                          'accepted_shell_valuation':1,'outgoing_guard_modulus':after,
                          'outgoing_guard_residue':a%after,
                          'support_before':sorted(support),'support_after':sorted(support|{h})})
            current=after; support.add(h)
        require(current==module['boundary_log_modulus'],'linear residual differs from module profile')
        receipts.append({'module_id':module['module_id'],'root':q,'steps':steps,
                         'final_guard_modulus':current,'final_guard_residue':a%current,
                         'claim':'exact single-module whole-private-fiber residual at anchor 1; not TRUE'})
    dump('LINEAR_RECEIPTS.json',receipts)
    dump('candidate_ledger.json',ledger); dump('ACTUAL_BASIN_LIBRARY.json',library)
    dump('conditional_architectures.json',archs); dump('results.json',result)
    print(json.dumps({k:result[k] for k in ['N_actual','actual_quotient_cells','conditional_architecture_checks','reference_runtime_seconds']},indent=2))
    print('global residue',r,'mod',M,'period',L)
    print('escape',d,'whole-fiber density',result['whole_private_fiber_boundary_density'])

if __name__=='__main__': main()
