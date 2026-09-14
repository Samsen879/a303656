#!/usr/bin/env python3
"""Independent exact trial-factor replay and Decimal outward interval proof.

Only the fixed saved candidate is evaluated. No SPF, ranking, or n-scan.
Decimal ln/exp are correctly rounded (nearest); one adjacent representable
number on each side encloses the exact value. All other operations are
directed ROUND_FLOOR/ROUND_CEILING. Divisors are enumerated here solely as
an independent cross-check of the search evaluator's multiplicative method.
"""
import argparse, json, math, time
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PREC=80
def require(ok,message):
    if not ok: raise ValueError(message)
def context(up): return Context(prec=PREC,rounding=ROUND_CEILING if up else ROUND_FLOOR)
class I:
    def __init__(self,a,b=None): self.lo=Decimal(a); self.hi=Decimal(a if b is None else b)
    def __add__(self,o):
        o=o if isinstance(o,I) else I(o)
        return I(context(False).add(self.lo,o.lo),context(True).add(self.hi,o.hi))
    __radd__=__add__
    def __neg__(self): return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,o): return self+(-o if isinstance(o,I) else -I(o))
    def __mul__(self,o):
        o=o if isinstance(o,I) else I(o)
        low=[context(False).multiply(x,y) for x in (self.lo,self.hi) for y in (o.lo,o.hi)]
        high=[context(True).multiply(x,y) for x in (self.lo,self.hi) for y in (o.lo,o.hi)]
        return I(min(low),max(high))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=o if isinstance(o,I) else I(o)
        require(not o.lo<=0<=o.hi,'division across zero')
        inverse=I(context(False).divide(Decimal(1),o.hi),context(True).divide(Decimal(1),o.lo))
        return self*inverse
    def ln(self):
        require(self.lo>0,'nonpositive log')
        a=context(False).ln(self.lo); b=context(True).ln(self.hi)
        return I(context(False).next_minus(a),context(True).next_plus(b))
    def exp(self):
        a=context(False).exp(self.lo); b=context(True).exp(self.hi)
        return I(context(False).next_minus(a),context(True).next_plus(b))
    def obj(self): return {'lower':str(self.lo),'upper':str(self.hi)}
def trial_factor(n):
    out=[]; p=2
    while p*p<=n:
        e=0
        while n%p==0: n//=p; e+=1
        if e: out.append([p,e])
        p=3 if p==2 else p+2
    if n>1: out.append([n,1])
    return out
def powers(b,lim):
    out=[]; x=1
    while x<=lim: out.append(x); x*=b
    return out
def admissible(m):
    if m<=0: return False
    u=m
    while not u&1: u//=2
    v=0
    while m%3==0: v+=1; m//=3
    return u%4==1 and not v&1
def odd_divisors(f):
    ds=[1]
    for p,e in f:
        if p!=2: ds=[h*p**j for h in ds for j in range(e+1)]
    return ds
def evaluate(n,rows):
    s=I(1)/I(n).ln(); totals=[]
    for k in [1,2]:
        total=I(0)
        for row in rows:
            subtotal=I(0)
            for h in odd_divisors(row['factors']):
                sign=1 if h%4==1 else -1
                subtotal=subtotal+sign*(-k*s*I(h).ln()).exp()
            total=total+subtotal
        totals.append(total)
    require(totals[0].lo>0,'D1 positive')
    return {'precision':PREC,'D1':totals[0].obj(),'D2':totals[1].obj(),'rho_interval':(totals[1]/totals[0]).obj()}
def main():
    global PREC
    ap=argparse.ArgumentParser(); ap.add_argument('--n',type=int,default=3920); a=ap.parse_args(); start=time.monotonic()
    cert=json.loads((ROOT/f'counterexample_{a.n}.json').read_text())
    rows=json.loads((ROOT/f'counterexample_{a.n}_residuals.json').read_text())
    n=a.n; require(cert['n']==n and cert['literal_bases']==[3,5],'literal identity')
    p3,p5=powers(3,n//4),powers(5,n//4)
    expected={(c,d):n-x-y for c,x in enumerate(p3) for d,y in enumerate(p5) if admissible(n-x-y)}
    require(len(rows)==len(expected)==cert['A23_size'],'A23 count')
    require({(r['c'],r['d']):r['residual'] for r in rows}==expected,'all A23 pairs')
    require(cert['C']==len(p3)-1 and cert['D']==len(p5)-1,'exact bulk bounds')
    for r in rows:
        m=r['residual']; require(n//2<=m<n,'bulk size')
        require(trial_factor(m)==r['factors'],'exact deterministic prime factorization')
        success=not any(p%4==3 and e%2 for p,e in r['factors'])
        require(success==r['success'],'norm indicator')
    witness=cert['original_representation']
    require(witness is not None,'representation witness missing')
    require(witness['a']**2+witness['b']**2+3**witness['c']+5**witness['d']==n,'original representation identity')
    escalations=[]
    for PREC in [80,120,180,250]:
        value=evaluate(n,rows); lo=Decimal(value['rho_interval']['lower']); hi=Decimal(value['rho_interval']['upper'])
        require(lo>2,'rho lower fails separation')
        require(lo<=Decimal(cert['rho_interval']['upper']) and hi>=Decimal(cert['rho_interval']['lower']),'independent mpmath/Decimal enclosure disjoint')
        if escalations:
            prev=escalations[-1]['rho_interval']
            require(lo<=Decimal(prev['upper']) and hi>=Decimal(prev['lower']),'precision instability')
        escalations.append(value)
    result={'status':'PASS','n':n,'exact_factorization_method':'independent integer trial division',
            'all_A23_pairs_verified':len(rows),'original_representation_verified':True,
            'independent_evaluator':'Decimal direct divisor enumeration with directed interval arithmetic',
            'transcendental_error_enclosure':'correctly-rounded ln/exp padded by next_minus/next_plus; monotone endpoints',
            'precision_escalation':escalations,'rho_interval':escalations[-1]['rho_interval'],
            'rho_lower_gt_2':True,'wall_seconds':time.monotonic()-start,
            'finite_violation_only':'Does not by itself refute the existence of an unspecified eventual N_star.'}
    (ROOT/'candidate_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
