#!/usr/bin/env python3
"""Independent, fail-closed verifier for the frozen Phase I evidence.

Standard library only. Does not import reference.py. This verifies a PARTIAL
actual ledger and CONDITIONAL guard architectures; it does not certify any
uninstantiated terminal. Normal and python -O runs have identical checks.
"""
from __future__ import annotations
import argparse, copy, itertools, json, math, sys, time
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
if hasattr(sys, 'set_int_max_str_digits'): sys.set_int_max_str_digits(100000)
ROOT=Path(__file__).resolve().parent

def insist(ok, message):
    if not ok: raise ValueError(message)

def read(name): return json.loads((ROOT/name).read_text())

@lru_cache(None)
def is_prime(n):
    if n<2: return False
    if n in (2,3): return True
    if n%2==0 or n%3==0: return False
    a=5
    while a*a<=n:
        if n%a==0 or n%(a+2)==0: return False
        a+=6
    return True

@lru_cache(None)
def factors(n):
    insist(n>=1,'factor domain')
    fs={}
    for p in (2,3):
        while n%p==0: fs[p]=fs.get(p,0)+1; n//=p
    d=5
    while d*d<=n:
        for p in (d,d+2):
            while n%p==0: fs[p]=fs.get(p,0)+1; n//=p
        d+=6
    if n>1: fs[n]=fs.get(n,0)+1
    return fs

def check_order(p,w,s):
    insist(is_prime(p) and p!=5,'nonprime or base-dividing arithmetic label')
    insist(w>0 and (p-1)%w==0 and pow(5,w,p)==1,'wrong order')
    insist(all(pow(5,w//ell,p)!=1 for ell in factors(w)),'order not minimal')
    insist(s>=1 and pow(5,w,p**s)==1 and pow(5,w,p**(s+1))!=1,'wrong lifting exponent')

@lru_cache(None)
def exact_order(p):
    insist(is_prime(p) and p!=5,'bad prime')
    w=p-1
    # Enumerate divisors independently rather than repeatedly divide a candidate.
    ds=[1]
    for ell,e in factors(w).items(): ds=[d*ell**j for d in ds for j in range(e+1)]
    return next(d for d in sorted(ds) if pow(5,d,p)==1)

@lru_cache(None)
def abs_closure(p):
    insist(is_prime(p),'unproved terminal or vertex')
    if p==3 or p%4==1: return frozenset(),frozenset([p])
    insist(p%4==3,'bad closure vertex')
    vertices={p}; terms=set()
    for ell in factors(exact_order(p)):
        if ell==2: continue
        vv,tt=abs_closure(ell); vertices.update(vv); terms.update(tt)
    return frozenset(vertices),frozenset(terms)

def actual_hit(row,c,d):
    p=row['p']; mod=p**row['K']; v=(row['r']-3**c-pow(5,d,mod))%mod
    if v==0: return False
    h=0
    while v%p==0: h+=1; v//=p
    return h in row['E']

def validate_actual(ledger, full=False):
    insist(ledger['status']=='ACTUAL_PARTIAL_NOT_COMPLETE','wrong status')
    insist(ledger['demand']=='BOTH' and ledger['anchors']==[0,1],'demand/anchor mismatch')
    insist(ledger['local_zero_accepted'] is False,'zero admitted')
    insist(ledger['actual_complete_certificate'] is False,'unsupported completeness claim')
    rows=ledger['odd_rows']; ps=[x['p'] for x in rows]
    insist(len(set(ps))==len(ps),'original prime repeated')
    insist(ledger['N_nonregular_original_rows']==3,'wrong actual N')
    insist(len(rows)==ledger['total_original_odd_rows']==9,'odd row count')
    insist(ledger['regular_original_odd_rows']==6,'regular row count')
    insist(ledger['total_original_rows_including_two_adic']==10,'total row count')
    for x in rows:
        insist(x['original_row'] is True and x['entry_type']=='ACTUAL_ORIGINAL_PRIME_ROW','macro in original slot')
        insist(x['p']%4==3 and x['K']==2 and x['E']==[1],'wrong admitted row parameters')
        insist(0<=x['r']<x['p']**2,'unreduced residue')
        check_order(x['p'],x['w'],x['s'])
        insist(0<=x['log_c1']<x['w'],'bad logarithm')
        insist(x['center_c1']==0,'this quotient requires zero private centers')
        if x['s']==1:
            # With center 0 the unique CRT representative is log modulo w, 0 modulo p.
            p=x['p']; w=x['w']; a=p*((x['log_c1']*pow(p,-1,w))%w)
            insist((3+pow(5,a,p*p))%(p*p)==x['r'],'regular state/log/center mismatch')
        else:
            insist((3+pow(5,x['log_c1'],x['p']**2)+x['p'])%(x['p']**2)==x['r'],'root state/log mismatch')
    insist(sorted(x['p'] for x in rows if x['s']>=2)==[20771,40487,1645333507],'root inventory mismatch')
    insist(ledger['two_adic_row']=={'K':2,'r':1,'modulus':4},'wrong two-adic row')
    M=4*math.prod(p*p for p in ps)
    insist(ledger['global_modulus']==M,'global modulus mismatch')
    r=ledger['global_residue']; insist(0<=r<M and r%4==1,'invalid global CRT residue')
    insist(all(r%(x['p']**2)==x['r'] for x in rows),'CRT state mismatch')
    U=math.lcm(1,*[x['w'] for x in rows]); L=math.lcm(1,*[x['w']*x['p']**max(0,2-x['s']) for x in rows])
    insist(ledger['U']==U and ledger['L']==L,'ambient was changed')
    by_p={x['p']:x for x in rows}
    for mod in ledger['modules']:
        q=mod['root']; vv,tt=abs_closure(q)
        insist(mod['actual'] is True and set(mod['vertices'])==vv,'bad actual module closure')
        insist(set(mod['terminals'])==tt,'bad terminal signature')
        insist(set(mod['regular_helpers'])==vv-{q},'missing regular helper')
        insist(mod['all_orders_odd']==all(exact_order(p)%2 for p in vv),'wrong parity profile')
        a=mod['canonical_a']
        W=math.lcm(*[exact_order(p) for p in vv])
        expected_profile=[]
        for ell,e in sorted(factors(W).items()):
            if ell not in vv-{q}: expected_profile.append({'modulus':ell**e,'residue':a%(ell**e)})
            else: insist(e==1,'private depth quotient invalid')
        insist(mod['whole_private_fiber_profile']==expected_profile,'wrong module boundary')
        for p in vv:
            insist(p in by_p,'missing original row')
            desired=(3+pow(5,a,p*p)+(p if p==q else 0))%(p*p)
            insist(mod['local_residues'][str(p)]==desired==by_p[p]['r'],'shared original state conflict')
    d=ledger['escape']['d']; esc=ledger['escape']
    insist(0<=d<L and esc['modulus']==L,'escape period')
    insist(not any(actual_hit(x,1,d) for x in rows),'claimed escape is fatal')
    insist(esc['anchor1_covered'] is False and esc['anchor0_covered'] is True and esc['BOTH'] is False and esc['EITHER'] is True,'escape demand labels')
    for m,a in esc['primary_coordinates'].items(): insist(d%int(m)==a,'escape CRT coordinate')
    for x in rows:
        insist(esc['local_values_c1_mod_p2'][str(x['p'])]==(x['r']-3-pow(5,d,x['p']**2))%(x['p']**2),'escape local value')
    if not full: return {}
    boundary=ledger['boundary_moduli']; private=ledger['private_primes']; mods=boundary+private
    insist(boundary==[2,27,5,653,761,1429] and private==[11,31,67,1523,30469139],'unexpected quotient domain')
    insist(math.prod(mods)==L,'period is not quotient CRT product')
    weights=[L//m*pow(L//m,-1,m) for m in mods]
    good=bad=weighted_good=weighted_all=whole_count=whole_weight=0
    for b,z in itertools.product(range(2),range(27)):
        for outside in itertools.product((0,1),repeat=4):
            prefix=(b,z)+outside
            weight_b=math.prod(p-1 if digit else 1 for p,digit in zip(boundary[2:],outside))
            saturated=True
            for bits in itertools.product((0,1),repeat=5):
                ds=prefix+bits; d=sum(a*w for a,w in zip(ds,weights))%L
                hits=[actual_hit(x,1,d) for x in rows]
                for x,h in zip(rows,hits):
                    predicted=d%x['w']==x['log_c1'] and (x['s']>=2 or d%x['p']!=0)
                    insist(h==predicted,'direct arithmetic and quotient disagree')
                ok=any(hits); saturated &= ok
                good+=ok; bad+=not ok
                wt=weight_b*math.prod(p-1 if digit else 1 for p,digit in zip(private,bits))
                weighted_all+=wt; weighted_good+=wt*ok
            f5,f653,f761,f1429=outside
            expected=(b==1 and z%3!=0) or (b==0 and z%3==0 and f5==0) or (b==1 and z%3==0 and f653==0) or (b==0 and z==1 and f761==f1429==0)
            insist(saturated==expected,'whole-fiber union mismatch')
            whole_count+=saturated; whole_weight+=weight_b*saturated
    insist(weighted_all==L,'quotient multiplicities incomplete')
    return {'cells':good+bad,'passing_BOTH':good,'failing_BOTH':bad,
            'weighted_passing':weighted_good,'whole_fiber_cells':whole_count,
            'pointwise_density':str(Fraction(weighted_good,L)),
            'whole_fiber_density':str(Fraction(whole_weight,math.prod(boundary)))}

def validate_architecture(arch,full=False):
    N=arch['N']; insist(N in (8,9),'wrong frozen architecture')
    insist(arch['conditional_only'] is True and arch['actual_complete_certificate'] is False,'conditional model mislabeled')
    insist(arch['root_in_B31_odd_required'] is False,'wrong B31 requirement')
    slots=arch['terminal_slots']; rows=arch['regular_rows']; ps=[x['p'] for x in rows]
    insist(len(slots)==N and len(set(ps))==len(ps),'slot/regular identity count')
    insist(arch['private_primes']==sorted(ps),'private prime list')
    insist(arch['conditional_odd_row_count']==N+len(rows)+1,'conditional row count')
    for row in rows:
        insist(row['original_row'] is True and row['K']==2 and row['E']==[1] and row['s']==1,'bad regular row')
        insist(row['p']%4==3,'nonadmitted regular row')
        check_order(row['p'],row['w'],1)
    demands={}
    for slot in slots:
        insist(slot['entry_type']=='UNINSTANTIATED_TERMINAL_SLOT' and slot['prime_value'] is None and slot['original_row'] is False,'unproved terminal promoted to original prime')
        insist(slot['required_s_min']==2 and slot['required_prime_congruence']==[4,3],'missing square-hit/admission hypothesis')
        n=slot['required_exact_order']; a=slot['canonical_a']; R=set(slot['regular_support'])
        vv=set()
        for ell in factors(n):
            if ell!=2: vv.update(abs_closure(ell)[0])
        insist(vv==R,'arithmetic support differs from claimed support')
        insist(slot['root_log_c1']==a%n,'wrong root log')
        for row in rows:
            if row['p'] not in R: continue
            p=row['p']
            insist(row['r']==(3+pow(5,a,p*p))%(p*p),'incompatible shared regular residue')
            insist(row['log_c1']==a%row['w'] and row['center_c1']==a%p,'helper log/center mismatch')
        demands[n]=demands.get(n,0)+1
    stated={x['n']:x['distinct_admitted_primitive_square_divisors_required'] for x in arch['square_hit_demands']}
    insist(stated==demands,'root multiplicity was lost')
    expected={279:3,903:1,191:1,5167:1,271:1,4159:1,31051:1} if N==9 else {1303:1,258065887:1,903:1,191:1,5167:1,271:1,4159:1,31051:1}
    insist(stated==expected,'not the frozen target family')
    if not full: return {}
    # Exact equality/non-equality quotient. No unknown q is used in modular arithmetic.
    mods=[2,27]+sorted(ps); L=math.prod(mods); coefficients=[L//m*pow(L//m,-1,m) for m in mods]
    count=0
    for b,z in itertools.product(range(2),range(27)):
        for bits in itertools.product((0,1),repeat=len(ps)):
            d=sum(a*c for a,c in zip((b,z)+bits,coefficients))%L
            regular=any(actual_hit(row,1,d) for row in rows)
            hypothesized=any(d%s['required_exact_order']==s['root_log_c1'] for s in slots)
            insist(regular or hypothesized or (b==1 and z%3!=0),'conditional guard coverage hole')
            count+=1
    return {'N':N,'conditional_guard_cells':count,'actual_root_certificates_checked':0}

def validate_receipts(ledger, receipts):
    modules={m['module_id']:m for m in ledger['modules']}; by_p={x['p']:x for x in ledger['odd_rows']}; count=0
    insist(len(receipts)==len(modules),'receipt count')
    for rec in receipts:
        mod=modules[rec['module_id']]; q=mod['root']; a=mod['canonical_a']; current=by_p[q]['w']; support={q}
        insist(rec['root']==q,'receipt origin')
        insist([s['eliminate'] for s in rec['steps']]==sorted(mod['regular_helpers'],reverse=True),'receipt elimination order')
        for step in rec['steps']:
            h=step['eliminate']; v=step['exact_provider_original_prime']; path=step['center_ancestry_path']
            insist(step['support_before']==sorted(support),'receipt support before')
            insist(v in support and by_p[v]['w']%h==0,'not an exact original provider')
            insist(path[0]==h and path[-1]==q and all(path[i]<path[i+1] and by_p[path[i+1]]['w']%path[i]==0 for i in range(len(path)-1)),'invalid original ancestry path')
            insist(current%h==0 and current%(h*h)!=0 and step['private_center']==a%h==0,'invalid linear center')
            insist(step['accepted_shell_valuation']==1 and step['actual_helper_original_prime']==h,'invalid dynamic helper')
            insist(step['incoming_guard_modulus']==current and step['incoming_guard_residue']==a%current,'incoming guard mismatch')
            current=math.lcm(current//h,by_p[h]['w']); support.add(h)
            insist(step['outgoing_guard_modulus']==current and step['outgoing_guard_residue']==a%current,'outgoing guard mismatch')
            insist(step['support_after']==sorted(support),'receipt support after'); count+=1
        insist(rec['final_guard_modulus']==current==mod['boundary_log_modulus'] and rec['final_guard_residue']==a%current,'final residual mismatch')
    return count

def mobius(n):
    ff=factors(n)
    return 0 if any(e>1 for e in ff.values()) else (-1)**len(ff)

def cyclotomic(n):
    divs=[1]
    for p,e in factors(n).items(): divs=[d*p**j for d in divs for j in range(e+1)]
    numerator=denominator=1
    for d in divs:
        m=mobius(n//d)
        if m==1: numerator*=5**d-1
        if m==-1: denominator*=5**d-1
    out,rem=divmod(numerator,denominator); insist(rem==0,'Moebius product division')
    return out

def validate_library(lib):
    for rec in lib['arithmetic_records']:
        p,w,s=rec['p'],rec['w'],rec['s']; check_order(p,w,s)
        insist({int(k):v for k,v in rec['order_factorization'].items()}==factors(w),'bad order factorization')
        insist(rec['admitted']==(p%4==3),'admission flag')
        insist(rec['kind']==('nonregular' if s>=2 else 'regular'),'regularity flag')
        insist(rec['pow_5_w_mod_p2']==pow(5,w,p*p) and rec['pow_5_w_mod_p3']==pow(5,w,p**3),'bad lifting receipt')
        insist({int(k):v for k,v in rec['order_minimality_residues'].items()}=={ell:pow(5,w//ell,p) for ell in factors(w)},'minimality receipt')
    insist(all(is_prime(x['p']) for x in lib['terminal_prime_proofs']),'terminal not prime')
    fac=lib['phi62_complete_factorization']; insist(fac['value']==math.prod(fac['factors'])==cyclotomic(62),'Phi62 factor product')
    insist(all(is_prime(p) for p in fac['factors']),'uncertified Phi62 factor')

def mutation_checks(ledger,archs,lib):
    outcomes=[]
    def test(name,obj,mutator,fn):
        x=copy.deepcopy(obj); mutator(x)
        try: fn(x)
        except (ValueError,KeyError,TypeError): outcomes.append({'mutation':name,'rejected':True}); return
        raise ValueError('mutation accepted: '+name)
    test('wrong actual N',ledger,lambda x:x.update(N_nonregular_original_rows=8),validate_actual)
    test('duplicate original row',ledger,lambda x:x['odd_rows'].append(x['odd_rows'][0]),validate_actual)
    test('formal atom in original slot',ledger,lambda x:x['odd_rows'][0].update(entry_type='DERIVED_MACRO'),validate_actual)
    test('unsupported completeness',ledger,lambda x:x.update(actual_complete_certificate=True),validate_actual)
    test('EITHER substituted for BOTH',ledger,lambda x:x.update(demand='EITHER'),validate_actual)
    test('zero counted fatal',ledger,lambda x:x.update(local_zero_accepted=True),validate_actual)
    test('ambient recomputed/changed',ledger,lambda x:x.update(L=x['L']//31),validate_actual)
    test('global residue drift',ledger,lambda x:x.update(global_residue=x['global_residue']+1),validate_actual)
    test('wrong root order',ledger,lambda x:x['odd_rows'][5].update(w=5),validate_actual)
    test('fake lifting status',ledger,lambda x:x['odd_rows'][2].update(s=2),validate_actual)
    test('free terminal silently dropped',ledger,lambda x:x['modules'][0].update(terminals=[3]),validate_actual)
    test('missing required helper',ledger,lambda x:x['modules'][0].update(regular_helpers=[11,31]),validate_actual)
    test('shared row31 reselected per basin',ledger,lambda x:x['modules'][1]['local_residues'].update({'31':5}),validate_actual)
    test('wrong escape exponent',ledger,lambda x:x['escape'].update(d=0),validate_actual)
    test('unknown terminal promoted',archs[1],lambda x:x['terminal_slots'][0].update(prime_value=279,original_row=True),validate_architecture)
    test('square hit replaced by first power',archs[1],lambda x:x['terminal_slots'][0].update(required_s_min=1),validate_architecture)
    test('three distinct roots collapsed to one',archs[1],lambda x:next(y for y in x['square_hit_demands'] if y['n']==279).update(distinct_admitted_primitive_square_divisors_required=1),validate_architecture)
    test('composite labeled prime',lib,lambda x:x['arithmetic_records'][0].update(p=9),validate_library)
    C=cyclotomic(279)
    try: insist(C+1==cyclotomic(279),'altered Phi279 target')
    except ValueError: outcomes.append({'mutation':'altered Phi279 integer','rejected':True})
    return outcomes

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--mutations',action='store_true'); parser.add_argument('--output',default='verification.json'); args=parser.parse_args()
    t=time.monotonic(); ledger=read('candidate_ledger.json'); lib=read('ACTUAL_BASIN_LIBRARY.json'); archs=read('conditional_architectures.json'); results=read('results.json')
    validate_library(lib); actual=validate_actual(ledger,True); conditional=[validate_architecture(a,True) for a in archs]
    linear_steps=validate_receipts(ledger,read('LINEAR_RECEIPTS.json'))
    for a,b in [('cells','actual_quotient_cells'),('passing_BOTH','actual_quotient_cells_passing_BOTH'),('failing_BOTH','actual_quotient_cells_failing_BOTH'),('weighted_passing','pointwise_full_period_covered_residues'),('whole_fiber_cells','whole_private_fiber_covered_cells'),('pointwise_density','pointwise_density'),('whole_fiber_density','whole_private_fiber_boundary_density')]: insist(actual[a]==results[b],'results mismatch: '+b)
    for tar in results['targets']:
        text=(ROOT/tar['file']).read_text().strip(); insist(len(text)==tar['decimal_digits'] and int(text)==cyclotomic(tar['n']),'target integer mismatch')
    insist(math.prod([2,3,5,7,11,13,17,19,23,29])*150000==results['published_bound_dependency'],'published-bound arithmetic')
    insist((results['published_bound_dependency']+1)**6==results['mass_gate_minimum_for_three_unlisted_square_hits'],'mass-gate arithmetic')
    C=cyclotomic(279); comp=results['phi279_composite_certificate']; insist(pow(comp['base'],C-1,C)==comp['pow_base_Cminus1_mod_C']!=1,'invalid composite witness')
    insist(all(C%p!=0 for p in range(2,10001) if is_prime(p)),'small factor receipt false')
    insist(results['actual_complete_certificate'] is False and results['N_actual']==3,'wrong overall scope')
    receipt={'status':'PASS','implementation':'verifier.py; does not import reference.py',
             'mathematical_independence':'second implementation, same research session; not independent-author review',
             'python_optimized':not __debug__,'actual':actual,'conditional':conditional,'linear_steps_verified':linear_steps,
             'actual_complete_certificate':False,'A303656':'UNRESOLVED',
             'mutations':mutation_checks(ledger,archs,lib) if args.mutations else [],
             'runtime_seconds':round(time.monotonic()-t,6)}
    (ROOT/args.output).write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt,indent=2))
if __name__=='__main__': main()
