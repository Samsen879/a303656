#!/usr/bin/env python3
"""Exact, standalone Phase-C checks. Python standard library only.

Run: python reference.py --output results.json
No network, repository imports, random sampling, or prime scan.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb, gcd, isqrt, lcm
from pathlib import Path

AUTHORITY = {
    'repository': 'Samsen879/a303656',
    'main_sha': '71b8d428b32724c37e593bcfd9d5f06a42e72d21',
    'main_tree': '5609e47eed0c058c190ef59c61644e2fd4b8fad6',
    'github_writes': 'NONE',
}

def factor(n: int) -> dict[int, int]:
    if n < 1: raise ValueError('positive integer required')
    out = {}; p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1; n //= p
        p = 3 if p == 2 else p+2
    if n > 1: out[n] = out.get(n, 0)+1
    return out

def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n)+1))

def order(q: int) -> int:
    assert prime(q) and q != 5
    w = q-1
    for p in factor(w):
        while w % p == 0 and pow(5, w//p, q) == 1: w //= p
    assert pow(5, w, q) == 1
    assert all(pow(5, w//p, q) != 1 for p in factor(w))
    return w

def valuation(n: int, q: int, cap: int) -> int:
    n %= q**cap
    if not n: return cap
    v = 0
    while n % q == 0: n //= q; v += 1
    return v

def signature(q: int) -> dict:
    w = order(q); s = 1
    while pow(5, w, q**(s+1)) == 1: s += 1
    return {'q': q, 'prime': True, 'admitted': q % 4 == 3,
            'w': w, 'order_factors': factor(w), 's': s}

def powers(mod: int, period: int) -> list[int]:
    out = []; a = 1
    for _ in range(period): out.append(a); a = a*5 % mod
    assert a == 1
    return out

def k2_mask(q: int, r: int, period: int) -> tuple[int, int]:
    """Exact full masks, or coarse masks when w*q divides coarse period."""
    assert period % (order(q)*q) == 0
    mm = [0, 0]; a = 1; mod = q*q
    for d in range(period):
        for c, anchor in enumerate((1, 3)):
            t = (r-anchor-a) % mod
            if t != 0 and t % q == 0: mm[c] |= 1 << d
        a = a*5 % mod
    assert not (mm[0] & mm[1])
    return tuple(mm)

def determinant_bareiss(mat: list[list[int]]) -> int:
    a = [row[:] for row in mat]; n = len(a)
    if n == 0: return 1
    sign = 1; prev = 1
    for k in range(n-1):
        if a[k][k] == 0:
            j = next((j for j in range(k+1, n) if a[j][k]), None)
            if j is None: return 0
            a[k], a[j] = a[j], a[k]; sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                num = pivot*a[i][j] - a[i][k]*a[k][j]
                assert num % prev == 0
                a[i][j] = num // prev
            a[i][k] = 0
        prev = pivot
    return sign*a[-1][-1]

def configuration_gap() -> dict:
    P = (3,7,31,43,1303)
    sigs = {q:signature(q) for q in P}
    assert all(s['admitted'] and s['s']==1 for s in sigs.values())
    U = lcm(*(s['w'] for s in sigs.values()))
    L = lcm(*(s['w']*q for q,s in sigs.items()))
    assert U == 1302 and L == U*43*1303
    fam = {3:[2+3*k for k in range(3)],
           7:[a+7*k for a in (2,5,6) for k in range(7)],
           31:[a+31*k for a in (2,6,26) for k in range(31)]}
    masks = {q:{r:k2_mask(q,r,U) for r in fam[q]} for q in fam}
    pooled = {q:{r:a|b for r,(a,b) in masks[q].items()} for q in fam}
    # 43,1303 are genuine, regular support rows. Their beta=0 coarse masks
    # are empty: every active coarse guard admits a private local-zero lift.
    support_receipts = []
    for q in (43,1303):
        assert U % q != 0
        w = sigs[q]['w']; pw = powers(q*q,w*q); logs = {a:d for d,a in enumerate(pw)}
        for c in (0,1):
            t = (2-(1,3)[c]) % (q*q)
            if t % q in {a % q for a in pw[:w]}:
                assert t in logs and (2-(1,3)[c]-pow(5,logs[t],q*q)) % (q*q)==0
        support_receipts.append({'q':q,'beta':0,'coarse_fatal_mask':'empty',
                                  'reason':'regular private center lift'})
    hist = Counter(); best = -1; witness = None; best_count = 0
    full_lift_checks = 0; lift_digest = hashlib.sha256()
    full = (1 << U)-1; all_assignments = 0; hole_digest = hashlib.sha256()
    for r3,r7,r31 in product(fam[3],fam[7],fam[31]):
        union = pooled[3][r3] | pooled[7][r7] | pooled[31][r31]
        missing = U-union.bit_count(); hist[missing] += 1; all_assignments += 1
        assert missing >= 2 and union != full
        holes = full ^ union
        first_hole = (holes & -holes).bit_length()-1
        private = 43*1303
        lifted = first_hole + U*((-first_hole*pow(U,-1,private))%private)
        assert lifted < L and lifted % U == first_hole
        for qq, rr in ((3,r3),(7,r7),(31,r31),(43,2),(1303,2)):
            assert all(valuation(rr-anchor-pow(5,lifted,qq*qq),qq,2)!=1 for anchor in (1,3))
        full_lift_checks += 1
        lift_digest.update(lifted.to_bytes(8,'little'))
        assert any((holes>>d)&1 for d in range(0,U,2))
        assert any((holes>>d)&1 for d in range(1,U,2))
        hole_digest.update(holes.to_bytes((U+7)//8,'little'))
        covered = U-missing
        if covered > best:
            best=covered;best_count=1
            witness={'residues':{'3':r3,'7':r7,'31':r31,'43':2,'1303':2},
                     'coarse_escapes':[d for d in range(U) if (holes>>d)&1]}
        elif covered == best: best_count += 1
    assert all_assignments == 5859 and best == 1300
    # The same distributions on shared whole-row states are used at every cell.
    row_expected = {3:Fraction(2,3),7:Fraction(2,7),31:Fraction(10,31)}
    row_counts = {}
    for q in fam:
        counts = [sum((pooled[q][r]>>d)&1 for r in fam[q]) for d in range(U)]
        assert all(Fraction(n,len(fam[q])) == row_expected[q] for n in counts)
        row_counts[q]={'family_size':len(fam[q]),'covering_states_per_cell':counts[0],
                       'fractional_contribution':str(row_expected[q])}
    fractional_sum=sum(row_expected.values(),Fraction())
    assert fractional_sum==Fraction(830,651)>1
    minor=[[int((pooled[3][r]>>d)&1) for r in (2,5,8)] for d in (0,2,4)]
    det=determinant_bareiss(minor);assert abs(det)==2
    # Source P5 skeleton, without support rows, has full L=1302 but coarse U=6.
    skeleton_union=pooled[3][2]|pooled[7][2]|pooled[31][2]
    skeleton_holes=[d for d in range(U) if not ((skeleton_union>>d)&1)]
    assert skeleton_holes==[0,651]
    return {'signatures':list(sigs.values()),'U':U,'L':L,'full_L_enumerated':False,
            'support_receipts':support_receipts,'state_families':fam,
            'global_assignments':all_assignments,'integer_complete_assignments':0,
            'direct_full_escape_witnesses_checked':full_lift_checks,
            'full_escape_witnesses_sha256':lift_digest.hexdigest(),
            'max_covered_coarse_cells':best,'best_assignment_count':best_count,
            'escape_count_histogram':dict(sorted(hist.items())),
            'all_escape_bitsets_sha256':hole_digest.hexdigest(),'max_coverage_witness':witness,
            'fractional_rows':row_counts,'fractional_sum_every_cell':str(fractional_sum),
            'fractional_feasible':True,'non_TU_minor':minor,'minor_determinant':det,
            'skeleton_only':{'P':[3,7,31],'U':6,'L':1302,'full_escapes':skeleton_holes}}

DEMANDS={'FALSE':(0,0,0,0),'A0':(0,1,0,1),'A1':(0,0,1,1),
         'EITHER':(0,1,1,1),'BOTH':(0,0,0,1),'TRUE':(1,1,1,1)}

def six_demands() -> dict:
    words=checks=0; patterns=set(DEMANDS.values())
    for n in range(1,5):
        for word in product(range(4),repeat=n):
            words+=1
            s0=all(z&1 for z in word);s1=all(z&2 for z in word);so=all(word)
            for name,table in DEMANDS.items():
                residual=tuple(int(all(table[c|z] for z in word)) for c in range(4))
                assert residual in patterns
                for c in range(4):
                    checks+=1
                    if name=='EITHER':assert residual[c]==bool(c or so)
                    if name=='BOTH':assert residual[c]==bool((c&1 or s0) and (c&2 or s1))
    split={name:tuple(int(all(table[c|z] for z in (1,2))) for c in range(4))
           for name,table in DEMANDS.items()}
    assert split['EITHER']==DEMANDS['TRUE'] and split['BOTH']==DEMANDS['BOTH']
    return {'top_words':words,'truth_comparisons':checks,'mismatches':0,'split_residual_tables':split}

def paired_catalog(q: int, h: int) -> dict:
    sig=signature(q);w=sig['w'];assert sig['s']==2 and w%h==0
    u=w//h;tab=powers(q,w);logs={a:b for b,a in enumerate(tab)}
    edges=sorted((a,logs[(x-2)%q]) for a,x in enumerate(tab) if (x-2)%q in logs)
    by_lower=defaultdict(list)
    for a,b in edges:
        if a%u==b%u:by_lower[a%u].append((a,b))
    # Alternative organization: create each coset, then test translated roots.
    for y in range(u):
        coset={tab[b]:b for b in range(y,w,u)}
        alt=sorted((b,coset[(x-2)%q]) for x,b in coset.items() if (x-2)%q in coset)
        assert alt==by_lower[y]
    nonempty=[y for y in range(u) if by_lower[y]]
    chosen=nonempty[:2]; witnesses=[]
    for y in chosen:
        a,b=by_lower[y][0];base=(1+tab[a])%q
        r=next(base+k*q for k in range(3)
               if valuation(base+k*q-1-pow(5,a,q*q),q,2)==1
               and valuation(base+k*q-3-pow(5,b,q*q),q,2)==1)
        assert pow(tab[a],h,q)==pow(5,y*h,q)
        assert pow((tab[a]-2)%q,h,q)==pow(5,y*h,q)
        witnesses.append({'Y':y,'b0':a,'b1':b,'r_mod_q2':r,
                          'top_positions':[a%h,b%h],'resultant_zero_mod_q_by_common_root':True})
    assert (chosen[1]-chosen[0])%u!=0
    # Structured enumeration of *all* q^2 residues, never looping over q^2.
    pw2=powers(q*q,w)
    profile=Counter(); total=0
    for base in range(q):
        active=[];excluded=[]
        for anchor in (1,3):
            b=logs.get((base-anchor)%q)
            active.append(b)
            excluded.append(None if b is None else ((anchor+pw2[b]-base)//q)%q)
        special=sorted({k for k in excluded if k is not None})
        for k in special:
            key=''.join('1' if b is not None and k!=e else '0' for b,e in zip(active,excluded))
            profile[key]+=1;total+=1
        generic=q-len(special)
        key=''.join('1' if b is not None else '0' for b in active)
        profile[key]+=generic;total+=generic
    assert total==q*q
    return {'signature':sig,'original_h':h,'lower_u':u,'all_difference2_pairs':len(edges),
            'same_lower_pairs':sum(map(len,by_lower.values())),
            'nonempty_lower_classes':len(nonempty),'edge_count_histogram':dict(sorted(Counter(len(by_lower[y]) for y in range(u)).items())),
            'incompatible_pairs_of_nonempty_lower_classes':comb(len(nonempty),2),
            'individual_witnesses':witnesses,'global_pair_for_these_two_Y_exists':False,
            'full_K2_state_count_via_structured_lifts':total,'fatal_anchor_profile_counts':dict(profile),
            'same_lower_pair_list_sha256':hashlib.sha256(json.dumps({str(y):by_lower[y] for y in range(u)},sort_keys=True,separators=(',',':')).encode()).hexdigest()}

def order_collapse_checks() -> dict:
    small=[]
    for p in (3,5,7):
        V=(5**p-1)//4
        ff=factor(V)
        assert all(prime(t) for t in ff)
        assert all(e==1 for e in ff.values())
        small.append({'p':p,'e':1,'Y':[0,1,2],'difference_gcd':1,'M':1,
                      'V':V,'complete_factorization':ff,
                      'factor_signatures':[signature(t) for t in ff],
                      'nonregular_paired_candidates':[]})
    q=20771;u=155;h=67;Y1=7;Y2=162;r0=16
    a,b=2177,9772
    assert a%u==b%u==Y1%u==Y2%u
    assert Y1%3410!=Y2%3410 # distinct lower fibers after actual 67-row support
    for Y in (Y1,Y2):
        assert pow(5,a*h,q)==pow(5,Y*h,q)
        assert pow(pow(5,a,q)-2,h,q)==pow(5,Y*h,q)
    numerator=(pow(5,u*h,q*q)-1)%(q*q)
    denominator=(pow(5,u,q*q)-1)%(q*q)
    V_mod_q2=numerator*pow(denominator,-1,q*q)%(q*q)
    assert V_mod_q2==0
    return {'fixed_triple_order_collapse':small,
            'compatible_reuse':{'q':q,'h':h,'u':u,'Y':[Y1,Y2],
                'ambient_lower_modulus_with_actual_67_row':3410,
                'r':r0,'b0':a,'b1':b,'same_global_paired_state':True,
                'V_67_1_155_mod_q2':V_mod_q2,
                'resultant_coefficients_equal_mod_q':pow(5,Y1*h,q)==pow(5,Y2*h,q)}}

def trim(poly: list[Fraction]) -> list[Fraction]:
    while len(poly)>1 and poly[0]==0:poly=poly[1:]
    return poly

def remainder(f: list[Fraction],g: list[Fraction]) -> list[Fraction]:
    f=trim(f[:]);g=trim(g[:]);assert any(g)
    while len(f)>=len(g) and any(f):
        coeff=f[0]/g[0]
        for j in range(len(g)):f[j]-=coeff*g[j]
        f=trim(f)
    return f

def resultant_euclid(f: list[Fraction],g: list[Fraction]) -> Fraction:
    f=trim(f);g=trim(g);m=len(f)-1;n=len(g)-1
    if not any(f) or not any(g):return Fraction(0)
    if n==0:return g[0]**m
    if m<n:return (-1)**(m*n)*resultant_euclid(g,f)
    r=remainder(f,g)
    if not any(r):return Fraction(0)
    k=len(r)-1
    return (-1)**(m*n)*g[0]**(m-k)*resultant_euclid(g,r)

def resultant(h: int,Y: int) -> int:
    A=5**(Y*h);f=[1]+[0]*(h-1)+[-A]
    g=[comb(h,k)*(-2)**k for k in range(h+1)];g[-1]-=A
    syl=[]
    for co in (f,g):
        for shift in range(h):syl.append([0]*shift+co+[0]*(h-1-shift))
    d=determinant_bareiss(syl)
    e=resultant_euclid(list(map(Fraction,f)),list(map(Fraction,g)))
    assert e.denominator==1 and d==e and d!=0
    return d

def resultant_checks() -> dict:
    data={}; gcds={}
    for h in (3,5,7):
        a=[resultant(h,y) for y in (0,1,2)]
        data[h]={y:a[y] for y in (0,1,2)}
        gcds[h]={'pairwise':{f'{i},{j}':gcd(a[i],a[j]) for i,j in combinations(range(3),2)},
                 'all_three':gcd(*a)}
    return {'resultants':data,'fixed_h_gcds':gcds,'crosscheck':'Bareiss == rational Euclid','mismatches':0}

def sphere_solutions(q: int,K: int,constraints: tuple[tuple[int,int],...]) -> list[int]:
    return [r for r in range(q**K) if all(valuation(r-a,q,K)==h for a,h in constraints)]

def sphere_formula(q: int,K: int,constraints: tuple[tuple[int,int],...]) -> list[int]:
    if not constraints:return list(range(q**K))
    H=max(h for a,h in constraints);a0=next(a for a,h in constraints if h==H)
    forbidden=set()
    for a,h in constraints:
        v=valuation(a-a0,q,K)
        if h<H:
            if v!=h:return []
        else:
            if v<H:return []
            forbidden.add(((a-a0)//q**H)%q)
    return sorted({(a0+q**H*t)%q**K for t in range(q**(K-H)) if t%q not in forbidden})

def sphere_checks() -> dict:
    checks=0
    base=tuple((a,1) for a in range(9))
    for n in (1,2,3):
        for cs in combinations(base,n):
            assert sphere_solutions(3,2,cs)==sphere_formula(3,2,cs);checks+=1
    centers=[(1+pow(5,d,9))%9 for d in (0,2,4)]
    triple=tuple((a,1) for a in centers)
    pairs=[sphere_solutions(3,2,c) for c in combinations(triple,2)]
    assert all(pairs) and not sphere_solutions(3,2,triple)
    return {'constraint_families_checked':checks,'mismatches':0,'actual_d':[0,2,4],
            'actual_centers_mod9':centers,'pairwise_legal_residues':pairs,
            'triple_legal_residues':[]}

def regular_width_checks() -> dict:
    systems=normal_cells=width_tests=0
    for q in (3,7,11):
        w=order(q);assert signature(q)['s']==1
        for K in (2,3):
            mod=q**K;ell=w*q**(K-1);pw=powers(mod,ell);logs={a:d for d,a in enumerate(pw)}
            for r in range(mod):
                systems+=1
                centers=[logs.get((r-anchor)%mod) for anchor in (1,3)]
                assert len({b%w for b in centers if b is not None})==sum(b is not None for b in centers)
                for c,anchor in enumerate((1,3)):
                    center=centers[c]
                    for d,a in enumerate(pw):
                        v=valuation(r-anchor-a,q,K)
                        direct=v==1 # Only E={1} is permitted for K=2,3.
                        expected=(center is not None and (d-center)%w==0 and (d-center)%q!=0)
                        assert direct==expected;normal_cells+=1
                for center in centers:
                    if center is None:continue
                    # All q residues above the centered first digit are safe
                    # modulo q^2, including the center itself (local zero).
                    for j in range(q):
                        z=center%q+j*q
                        d=z+q*q*((center-z)*pow(q*q,-1,w)%w) if w>1 else z
                        assert d%w==center%w and d%(q*q)==z
                        assert all(valuation(r-anchor-pow(5,d,mod),q,K)!=1 for anchor in (1,3))
                    width_tests+=1
    return {'systems':systems,'direct_normal_form_anchor_cells':normal_cells,
            'centered_safe_projection_tests':width_tests,'mismatches':0,
            'scope':'q=3,7,11; K=2,3; all shared residues; E={1}; analytic refinement only'}

def accepted_set_checks() -> dict:
    systems=cells=widths=0
    q=3;w=2
    for K in (4,5):
        mod=q**K;ell=w*q**(K-1);pw=powers(mod,ell);logs={a:d for d,a in enumerate(pw)}
        for E in ({1},{3},{1,3}):
            for rr in range(mod):
                systems+=1
                centers=[logs.get((rr-anchor)%mod) for anchor in (1,3)]
                safe=[]
                for d, a in enumerate(pw):
                    fatal=[]
                    for c,anchor in enumerate((1,3)):
                        v=valuation(rr-anchor-a,q,K)
                        direct=v in E
                        center=centers[c]
                        expected=False
                        if center is not None and (d-center)%w==0:
                            j=valuation(d-center,q,K-1)
                            expected=(j<K-1 and 1+j in E)
                        assert direct==expected;cells+=1;fatal.append(direct)
                    if not any(fatal):safe.append(d)
                for center in centers:
                    if center is None:continue
                    sub=[d for d in safe if d%w==center%w]
                    if 1 not in E:assert {d%q for d in sub}==set(range(q))
                    assert {d%9 for d in sub if d%3==center%3}=={center%3+3*k for k in range(3)}
                    widths+=1
    # Negative sensitivity control: forbidden even valuations remove this width.
    invalid_safe=[d for d in range(18) if d%2==0 and
                  all(valuation(2-anchor-pow(5,d,27),3,3) not in {1,2} for anchor in (1,3))]
    assert {d%9 for d in invalid_safe}=={0}
    return {'systems':systems,'direct_normal_form_anchor_cells':cells,
            'safe_projection_checks':widths,'mismatches':0,
            'invalid_even_E_control':{'K':3,'r':2,'E':[1,2],
                                     'admitted':False,'safe_projection_mod9':[0]}}

def hereditary_examples() -> list[dict]:
    def check(p: int) -> dict:
        if p==5 or p%4!=3 or not prime(p):
            return {'p':p,'in_H':False,'reason':'not an admitted regular-support prime'}
        sig=signature(p)
        if sig['s']!=1:
            return {'p':p,'signature':sig,'in_H':False,'reason':'nonregular support'}
        odd={ell:e for ell,e in factor(sig['w']).items() if ell!=2}
        if any(e>1 for e in odd.values()):
            return {'p':p,'signature':sig,'in_H':False,'reason':'nonsquarefree odd order'}
        children=[check(ell) for ell in odd]
        return {'p':p,'signature':sig,'in_H':all(x['in_H'] for x in children),
                'required_children':children}
    data=[check(p) for p in (3,7,11,19,31,43,67,127,1303)]
    assert [x['p'] for x in data if x['in_H']]==[3,7,31,43,127,1303]
    return data

def run() -> dict:
    return {'authority':AUTHORITY,'configuration_gap':configuration_gap(),
            'six_demands':six_demands(),
            'paired_catalogs':[paired_catalog(20771,67),paired_catalog(40487,653)],
            'resultant_checks':resultant_checks(),'order_collapse_checks':order_collapse_checks(),
            'sphere_checks':sphere_checks(),
            'regular_width_checks':regular_width_checks(),'accepted_set_checks':accepted_set_checks(),'hereditary_examples':hereditary_examples(),
            'verdict':'PASS; finite computations are not substitutes for the report proofs'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path('results.json'))
    args=parser.parse_args();data=run()
    payload=json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(payload,encoding='utf-8')
    print(json.dumps({'verdict':data['verdict'],'output':str(args.output),
                      'sha256':hashlib.sha256(payload.encode()).hexdigest(),
                      'global_assignments':data['configuration_gap']['global_assignments'],
                      'integer_complete':data['configuration_gap']['integer_complete_assignments'],
                      'fractional_sum':data['configuration_gap']['fractional_sum_every_cell'],
                      'regular_width':data['regular_width_checks']},indent=2))
