"""Lift the R5 W1 cover and find two square identities on the same CRT progression."""
import json
from math import prod
from sympy import isprime, primerange
from sympy.solvers.diophantine.diophantine import cornacchia

from paths import HERE,R5
from low_verify import cover_rows, window

def coordinates(factors):
    a,b = 1,0
    for p,h in factors:
        scale=p**(h//2)
        a,b=a*scale,b*scale
        if h%2:
            u,v=(1,1) if p==2 else sorted(cornacchia(1,1,p))[0]
            a,b=a*u-b*v,a*v+b*u
    return sorted([abs(int(a)),abs(int(b))])

SMALL=list(primerange(2,500))
def factors(n):
    result=[]
    for p in SMALL:
        if n%p:
            continue
        h=0
        while n%p==0:
            h+=1
            n//=p
        if p%4==3 and h%2:
            return None
        result.append((p,h))
    if n==1:
        return result
    if n%4==1 and isprime(n):
        return result+[(n,1)]
    return None

def main():
    z=json.loads((R5/'low_control.json').read_bytes())
    m,q=z['m'],z['palette']
    rows=window()
    _,powers=cover_rows(m,q,rows)
    step=prod(p**h for p,h in powers.items())
    p=47
    tail=5**0+3**11-4
    k=((tail+p-5*m)*pow(5*step,-1,p*p))%(p*p)
    m+=step*k
    q=q+[p]
    rows["child",0,11]=tail
    _,powers=cover_rows(m,q,rows)
    step=prod(p**h for p,h in powers.items())
    start=m%step
    lo=(2**262-start+step-1)//step
    for i in range(100000):
        n=start+(lo+i)*step
        if n.bit_length()!=263:
            break
        pa=factors(n-4)
        if pa is None:
            continue
        ch=factors(5*n+4-1-3**12)
        if ch is None:
            continue
        record=dict(m=n,r=4,palette=q,parent=coordinates(pa),child=coordinates(ch),
                    crt_residue=start,crt_modulus=step,translates_checked=i+1)
        print(json.dumps(record,sort_keys=True))
        return
    raise RuntimeError("no two norms in search cap")

if __name__=="__main__":
    main()
