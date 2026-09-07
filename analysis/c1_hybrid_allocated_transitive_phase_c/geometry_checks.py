"""Exact finite regressions. Abstract tests do not assert prime realizability."""
from itertools import product
from pathlib import Path
import json

def mask(cs,p=3,beta=3):
    return sum(1<<z for z in range(p**beta) if any(z%p**e==a for e,a in cs))

def prefix_units(cs,p=3,beta=3):
    kept=set();total=0
    for e,a in sorted(set(cs)):
        if e<1 or e>beta or not 0<=a<p**e:raise ValueError('invalid cylinder')
        if not any((d,a%p**d) in kept for d in range(1,e)):
            kept.add((e,a));total+=p**(beta-e)
    return total

def shells(center,J,p=3):
    return [(j+1,(center%p**(j+1)+t*p**j)%p**(j+1)) for j in J for t in range(1,p)]

def union_audit():
    catalog=[(e,a) for e in (1,2) for a in range(3**e)]
    Bs=[]
    for i in range(1<<len(catalog)):
        cs=[v for k,v in enumerate(catalog) if (i>>k)&1]
        m=mask(cs)
        assert prefix_units(cs)==m.bit_count()
        Bs.append((cs,m))
    cases=strict=improved=full=0
    for center in range(27):
        for J in [(),(0,),(2,),(0,2),(1,)]:
            D=shells(center,J);dm=mask(D)
            # Independent valuation definition for dynamic bits.
            raw=0
            for z in range(27):
                t=(z-center)%27;j=0
                if t==0:continue
                while t%3==0:t//=3;j+=1
                if j in J:raw|=1<<z
            assert raw==dm
            for B,bm in Bs:
                u=prefix_units(B+D);v=(bm|dm).bit_count()
                assert u==v
                mass=bm.bit_count()+dm.bit_count()
                if mass<27:
                    assert v<27;strict+=1
                if mass>=27 and v<27:improved+=1
                full+=v==27;cases+=1
    return dict(scope='All subsets of 12 depth1/2 cylinders, 27 centers, five parity bundles; abstract geometry',
                cases=cases,strict_mass_applicable=strict,exact_pass_mass_fail=improved,
                full_unions=full,mismatches=0,
                overlap_example=dict(D='S0(0)',B=['C1(1)','C1(2)'],mass_sum='4/3',union='2/3'),
                depth_example=dict(D='S0(0)',B=['C2(0)'],exact_union='7/9',first_digit_union='1'))

def direct_fatal(x,y,z,a,b,c,g,center5,d3):
    return ((d3 is not None and x!=d3) or (x==g and y!=center5)
            or (x==0 and z!=0) or (x==a and y==b and z==c))

def one_root_audit():
    checked=passed=direct_cells=failed_but_escape=0
    for a,b,c,g,center5,d3,receiver,release in product(range(3),range(5),range(7),range(3),range(5),[None,0,1,2],(3,5),(False,True)):
        checked+=1
        B3=({a} if receiver==3 else set()) | ({g} if release else set())
        B5={b} if receiver==5 else set()
        D3=set() if d3 is None else set(range(3))-{d3}
        D5=set() if release else set(range(5))-{center5}
        certificate=len(B3|D3)<3 and len(B5|D5)<5
        if certificate:
            passed+=1
            x=min(set(range(3))-B3-D3)
            if release:assert x!=g
            y=min(set(range(5))-B5-(set(range(5))-{center5} if x==g else set()))
            z=0
            assert not direct_fatal(x,y,z,a,b,c,g,center5,d3)
        escaped=False
        for x,y,z in product(range(3),range(5),range(7)):
            fatal=direct_fatal(x,y,z,a,b,c,g,center5,d3);direct_cells+=1
            escaped|=not fatal
            inplan=(x not in B3|D3 and y not in B5 and
                    (x!=g or y==center5) and (x!=0 or z==0))
            if inplan:assert not fatal
        if not certificate and escaped:failed_but_escape+=1
    return dict(scope='Synthetic triangular three-coordinate normal forms; no arithmetic realization claimed',
                systems=checked,certificate_pass=passed,direct_cells=direct_cells,
                certificate_fail_but_escape=failed_but_escape,mismatches=0)

def coalescence_audit():
    checked=passed=cells=collisions=0
    for a0,a1,b0,b1,g,center5,d3 in product(range(3),range(3),range(5),range(5),range(3),range(5),[None,0,1,2]):
        checked+=1
        B3={g};B5={b0,b1};D3=set() if d3 is None else set(range(3))-{d3}
        certificate=len(B3|D3)<3
        assert len(B3)==1 # ONE outgoing relay guard, not two path units.
        collisions+=b0==b1
        if certificate:
            passed+=1
            x=min(set(range(3))-B3-D3);y=min(set(range(5))-B5);z=0
            assert x!=g
            assert not ((x==a0 and y==b0 and z==0) or (x==a1 and y==b1 and z==1))
        for x,y,z in product(range(3),range(5),range(7)):
            cells+=1
            fatal=((d3 is not None and x!=d3) or (x==g and y!=center5)
              or (x==a0 and y==b0 and z==0) or (x==a1 and y==b1 and z==1))
            inplan=x not in B3|D3 and y not in B5
            if inplan:assert not fatal
    return dict(scope='Two DISTINCT synthetic root rows coalescing at one relay; target guard charged once',
                systems=checked,certificate_pass=passed,direct_cells=cells,
                coincident_incoming_geometry_cases=collisions,mismatches=0)

def counterchecks():
    X={0,1,2};objects={'a':{0,1},'b':{2},'c':{1,2}}
    def feasible(names):return set().union(*(objects[n] for n in names))!=X
    assert feasible({'a'}) and feasible({'b','c'})
    assert not feasible({'a','b'}) and not feasible({'a','c'})
    # Fractional log/state choice is NOT one shared state.
    allowed_x={0:{0},1:{1}};allowed_y={0:{1},1:{0}}
    desired=(0,0)
    assert any(0 in v for v in allowed_x.values()) and any(0 in v for v in allowed_y.values())
    assert not any(desired[0] in allowed_x[s] and desired[1] in allowed_y[s] for s in (0,1))
    # Whole paired state configuration, standard four-demand integrality gap.
    options=[[{'a','u'},{'b','v'}],[{'a','v'},{'b','u'}]]
    assert all(a|b!={'a','b','u','v'} for a in options[0] for b in options[1])
    assert all(sum(v in s for row in options for s in row)==2 for v in ['a','b','u','v'])
    # K2=2,r2=1: two-square residues {0,1,2}; c0 fatal,c1 safe for every d.
    sq={(a*a+b*b)%4 for a in range(4) for b in range(4)}
    assert (1-1-1)%4 not in sq and (1-3-1)%4 in sq
    return dict(nonmatroid_exchange='PASS (abstract union bundles)',
                shared_state_conflict='PASS (abstract)',fractional_integral_gap='PASS (abstract)',
                two_adic_no_common_safe='PASS (actual K2=2 residue1)',
                interpretation='Failures of relaxations or proof invariants, NOT an actual complete odd certificate')

def run():
    return dict(unions=union_audit(),one_root=one_root_audit(),coalescence=coalescence_audit(),counterexamples=counterchecks())

if __name__=='__main__':
    result=run()
    (Path(__file__).parent/'geometry_results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))
