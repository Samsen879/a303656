from math import gcd, lcm, prod
from collections import Counter
import json
from pathlib import Path

def crt(a,m,b,n):
    g=gcd(m,n)
    if (b-a)%g: raise ValueError('Inconsistent CRT')
    k=((b-a)//g * pow(m//g,-1,n//g))%(n//g)
    return (a+m*k)%lcm(m,n),lcm(m,n)

def fatal(q,r,c,d):
    x=(r-(1 if c==0 else 3)-pow(5,d,q*q))%(q*q)
    return x!=0 and x%q==0

U=lcm(2,3,10385,40486); M=U//31
rows={3:2,20771:20773,40487:40493}
fibers=[]
for y in [0,437511]:
    ds=[crt(y,M,x,31)[0] for x in range(31)]
    fixed=[[q for q,r in rows.items() if any(fatal(q,r,c,d) for c in [0,1])] for d in ds]
    fibers.append({'y':y,'exponents':ds,'fixed_cover':fixed})
counts=Counter(); choices=[[],[]]; best=[]; results=[]
for r in range(31**2):
    covered=[]
    for i,f in enumerate(fibers):
        n=sum(bool(f['fixed_cover'][x]) or any(fatal(31,r,c,d) for c in [0,1]) for x,d in enumerate(f['exponents']))
        covered.append(n)
        if n==31:choices[i].append(r)
    counts[sum(covered)]+=1
    results.append((r,covered))
assert choices==[[2,4],[684,686]], choices
assert max(counts)==61 and not(set(choices[0])&set(choices[1]))
assert [i for i,a in enumerate(fibers[0]['fixed_cover']) if a]==[0]
assert [i for i,a in enumerate(fibers[1]['fixed_cover']) if a]==[1]
result={'U':U,'L':U,'M':M,'fixed_rows':rows,'fibers':fibers,'individually_full_states':choices,'coverage_histogram':dict(sorted(counts.items())),'best_total_coverage':61,'mandatory_cells':62,'global_full_states':0}
Path(__file__).with_name('fiber_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fibers'},indent=2))
for p in [7,19]:
    w=6 if p==7 else 9
    same=[]
    for r in range(p*p):
        logs=[]
        for c in [0,1]:
            ds=[d for d in range(w*p) if (r-(1 if c==0 else 3)-pow(5,d,p*p))%(p*p)==0]
            logs.append(ds)
        if all(logs) and logs[0][0]%p==logs[1][0]%p:
            same.append((r,logs[0][0],logs[1][0],logs[0][0]%p))
    print('distinct anchor roles, same center',p,same[:10])
