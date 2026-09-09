"""Generate Lucas primality certificates; SymPy is discovery only, never the verifier."""
from pathlib import Path
from math import gcd, isqrt
import hashlib, json
import sympy as sp
P=Path(__file__).resolve().parent
KNOWN={903:[149930509,1562986310551],1806:[43,246201060546547]}
NEW=147304138944416276237689
nodes={}
def certify(p):
    if p in nodes:return
    if p==2:
        nodes[p]={'p':'2','base_case':True};return
    fs={int(r):int(e) for r,e in sp.factorint(p-1).items()}
    assert sp.prod(r**e for r,e in fs.items())==p-1
    for r in fs:certify(r)
    for a in range(2,100000):
        if pow(a,p-1,p)==1 and all(gcd(pow(a,(p-1)//r,p)-1,p)==1 for r in fs):break
    else:raise RuntimeError('No Lucas certificate found')
    nodes[p]={'p':str(p),'a':str(a),'factorization_p_minus_one':[[str(r),e] for r,e in sorted(fs.items())]}
for p in sum(KNOWN.values(),[])+[NEW]:certify(p)
certs=[nodes[p] for p in sorted(nodes)]
(P/'primality_certificates.json').write_text(json.dumps({'method':'full-factorization Lucas primality criterion','roots':list(map(str,sum(KNOWN.values(),[])+[NEW])),'nodes':certs},indent=2)+'\n')
with (P/'primality_certificates.tsv').open('w') as f:
    for rec in certs:
        fs=rec.get('factorization_p_minus_one',[])
        f.write(' '.join([rec['p'],rec.get('a','0'),str(len(fs))]+[str(x) for r,e in fs for x in (r,e)])+'\n')

def val(N,p):
    e=0
    while N%p==0:N//=p;e+=1
    return e

def info(N):
    return {'decimal':str(N),'hex':hex(N),'digits':len(str(N)),'bits':N.bit_length(),
            'sha256_decimal_no_newline':hashlib.sha256(str(N).encode()).hexdigest(),
            'mod4':N%4,'mod13':N%13,'isqrt':str(isqrt(N)),
            'fermat_base2_residue':str(pow(2,N-1,N)),
            'fermat_base2_composite':pow(2,N-1,N)!=1}
A={'authority':{'repo':'Samsen879/a303656','main':'fd59aad038a09f2fc6df7039111408fa231c27dd','tree':'afd34fc936f83867758c827bfcd8b7b9d9b8d5b5','phase_e_zip_available':False,'phase_e_binding':'NOT_VERIFIED','date':'2026-09-08'},'values':{},'prime_factors':[],'trial_bound':10**12}
for n in (903,1806):
    N=int((P/f'N{n}.txt').read_text());C=int((P/f'C{n}.txt').read_text())
    assert N==sp.prod(KNOWN[n])*C
    assert gcd(C,n)==1 and C%1806==1
    A['values']['N'+str(n)]=info(N);A['values']['C'+str(n)]=info(C)
    primes=KNOWN[n]+([NEW] if n==1806 else [])
    for q in primes:
        order=42 if q==43 else n
        tests={str(order//l):str(pow(5,order//l,q)) for l in sp.factorint(order)}
        A['prime_factors'].append({'n':n,'p':str(q),'order':order,'mod4':q%4,'mod5':q%5,'multiplicity':val(N,q),
          'order_power_residue':str(pow(5,order,q)), 'proper_order_tests':tests,
          'lift_power_mod_p_squared':str(pow(5,order,q*q)), 'quotient_mod_p':str((N//q)%q),
          'status':'PROVEN_PRIME_BY_ATTACHED_LUCAS_CERTIFICATE',
          'discovery':'fresh_ecm_split_of_reconstructed_C1806' if q==NEW else 'independent_reconstruction_no_Phase_E_inventory_available'})
R=int((P/'R1806_after_new_factor.txt').read_text());C1=int((P/'C903.txt').read_text());C2=int((P/'C1806.txt').read_text())
assert R*NEW==C2 and gcd(R,NEW)==1
A['values']['R1806']=info(R)
A['gcds']={
 'N903_N1806':gcd(int((P/'N903.txt').read_text()),int((P/'N1806.txt').read_text())),
 'C903_C1806':gcd(C1,C2),'C903_903':gcd(C1,903),'C1806_1806':gcd(C2,1806),
 'C903_known_product':gcd(C1,sp.prod(KNOWN[903])),
 'C1806_known_product':gcd(C2,sp.prod(KNOWN[1806])),
 'R1806_new_factor':gcd(R,NEW),'R1806_1806':gcd(R,1806)}
A['gcds']={k:int(v) for k,v in A['gcds'].items()}
for key in ('C903','C1806','R1806'):
    value=int(A['values'][key]['decimal']);L=10**12
    om=0
    while (L+1)**(om+1)<=value:om+=1
    A['values'][key]['omega_upper_bound_from_trial']=om
    A['values'][key]['cube_root_floor']=str(int(sp.integer_nthroot(value,3)[0]))
    A['values'][key]['possible_repeated_prime_upper_bound']=str(isqrt(value//(L+1)))
A['admitted_prime_residues_mod18060']={
 '903':[a for a in range(18060) if a%3612==1807 and a%5 in (1,4)],
 '1806':[a for a in range(18060) if a%3612==1807 and a%5 in (2,3)]}
(P/'arithmetic_audit.json').write_text(json.dumps(A,indent=2)+'\n')
print('Certificate nodes:',len(certs))
for v in ('C903','C1806','R1806'):
    d=A['values'][v];print(v,{k:d[k] for k in ('digits','bits','mod4','mod13','omega_upper_bound_from_trial','cube_root_floor')})
print('Prime roots',[(r['p'],r.get('a')) for r in certs if int(r['p']) in sum(KNOWN.values(),[])+[NEW]])
print('mod18060',A['admitted_prime_residues_mod18060'])
print('new prime predecessor certificate',nodes[NEW])
