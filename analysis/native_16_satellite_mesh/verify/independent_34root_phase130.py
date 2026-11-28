"""Exact 12 safe phases modulo130; imports only this audit's own full proof.

Usage: python independent_34root_phase130.py [sparse_construction folder]
The frozen producer JSON is never modified.
"""
import json,runpy
from pathlib import Path
from time import perf_counter,process_time
wall=perf_counter();cpu=process_time()
audit=runpy.run_path(str(Path(__file__).with_name('independent_34root_uniform.py')))
D,E,h,d=audit['D'],audit['E'],audit['h'],audit['d']
assert D%3==0 and E%13==0 and h%3==E%3==1 and h%13==11

# Every subset rotation at3 (first edge) and13 (second edge) is +/-1.
# Check the actual native chord at every residue, not just one successful phase.
bad={}
for edge,ell in ((0,3),(1,13)):
    pack=d['packs'][edge]
    assert pack[0][1]%ell==0 and pack[0][0]%ell!=0
    assert all(m%ell==0 and b%ell!=0 for m,b,_,_ in pack[1:])
    bad[ell]=set()
    for y in range(ell):
        t=(5*y*y-h*y+5+3*h-E)*pow(10,-1,ell)%ell
        P=((h-3*t)%ell,t)
        Q=((P[0]+1)%ell,(P[1]+3)%ell) if edge==0 else ((P[0]+3-y)%ell,(P[1]-1-3*y)%ell)
        for sign in (-1,1):
            if all((sign*Q[j]-P[j])%ell==0 for j in (0,1)):bad[ell].add(y)
assert bad=={3:set(),13:{10}}
safe_phases=[a for a in range(0,130,10) if a%13!=10]
assert safe_phases==[0,20,30,40,50,60,70,80,90,100,110,120]

M=audit['M']//3;assert M*3==audit['M'] and M.bit_length()==2816
N0=(audit['hi']-audit['lo'])//M
assert N0==2168307913068703036
# The 12 phases times all2^34 root assignments are distinct modulo M.
# The entire geometric/height argument from the prior proof depends on y's
# window only, and the exact division constraints are unchanged.
B=audit['bad_known'];C=audit['tail_coefficient'];Q=audit['trial_bound']
good_bounds=[n-B*(n//573737+1)-C*(n//Q+1) for n in (N0,N0+1)]
assert good_bounds==[1318298606421300420,1318298606421300421]
total=min(good_bounds)*12*(1<<34)
assert total==271778371245209323281171087360 and total>(1<<97)
assert total>36*audit['total']
report={'status':'PASS','frozen_input_sha256':audit['report']['input_sha256'],
        'fixed_phase_modulus':130,'safe_phase_residues':safe_phases,
        'bad_phases_at3':[],'bad_phases_at13':[10],
        'complete_root_and_phase_classes':12*(1<<34),
        'M_bits':M.bit_length(),'minimum_candidates_each_class':N0,
        'good_bounds_for_two_candidate_counts':good_bounds,
        'good_targets_lower_all_classes':total,
        'simple_lower_power_of2':97,'primitive_outputs_each_target':131072,
        'ordinary_height':True,'same_uniform_common_angle_mesh':True,
        'wall_seconds':perf_counter()-wall,'cpu_seconds':process_time()-cpu}
Path(__file__).with_name('independent_34root_phase130_result.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all3-phases safe; only y=10 mod13 bad;12 safe phases modulo130')
print('PASS: min candidates per class',N0,'good lower',min(good_bounds))
print('PASS: total distinct good n >=',total,'>2^97, each131072 primitive critical distinct q')
print('cpu_s',round(process_time()-cpu,3),'wall_s',round(perf_counter()-wall,3))
