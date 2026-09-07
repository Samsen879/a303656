from arithmetic import factor, order, log_bsgs
from math import gcd, lcm
import json
from pathlib import Path

def valmod(n,p,K):
    n %= p**K
    if n==0: return 'LOCAL_ZERO_UNRESOLVED'
    v=0
    while n%p==0: v+=1;n//=p
    return v

def crt(residues):
    x,M=0,1
    for n,a in sorted(residues.items()):
        if gcd(M,n)!=1: raise ValueError('CRT moduli not coprime')
        x += ((a-x)*pow(M,-1,n)%n)*M
        M *= n
        x %= M
    return x,M

def arithmetic_record(p):
    assert factor(p)=={p:1}
    if p==5:
        return dict(p=p,admitted=False,p_minus_one=factor(p-1),w=None,s=None,
                    role='free coordinate; base-5 order undefined modulo5')
    w=order(p);s=1
    while pow(5,w,p**(s+1))==1:s+=1
    return dict(p=p,admitted=p%4==3,p_minus_one=factor(p-1),w=w,
                w_factorization=factor(w),s=s,
                order_tests={str(l):pow(5,w//l,p) for l in factor(w)},
                lift_next=pow(5,w,p**(s+1)))

def run():
    roots=[3,11,23,67,20771,40487,30469139,1645333507]
    closure=set(roots);pending=list(roots)
    while pending:
        p=pending.pop()
        for l in factor(order(p)):
            if l==2:continue
            if l not in closure:
                closure.add(l)
                # Continue admitted labels; nonadmitted are free terminals.
                if l%4==3: pending.append(l)
    records={p:arithmetic_record(p) for p in sorted(closure)}
    q=1645333507; p=30469139;w=records[q]['w'];logs=[1,85648253]
    assert [pow(5,b,q) for b in logs]==[5,3]
    h=next(h for h in range(3) if all(valmod(6+h*q-3**c-pow(5,logs[c],q*q),q,2)==1 for c in (0,1)))
    rq=6+h*q
    rowdata={t:dict(K=2,E=[1],r=2) for t in roots}
    rowdata[3]=dict(K=6,E=[1,3,5],r=(1+pow(5,logs[1],3**6))%(3**6))
    for t in [20771,40487]:rowdata[t]['r']=t+2
    rowdata[p]['r']=6;rowdata[q]['r']=rq
    for t,d in rowdata.items():
        d['w']=records[t]['w'];d['s']=records[t]['s']
        d['a']=max(0,d['K']-d['s'])
        d['ell']=d['w']*t**d['a']
        d['logs']=[log_bsgs((d['r']-3**c)%t,t,d['w']) for c in (0,1)]
    assert rowdata[q]['logs']==logs
    U=lcm(*(d['w'] for d in rowdata.values())); L=lcm(*(d['ell'] for d in rowdata.values()))
    Uf=factor(U);Lf=factor(L)
    targets=[]
    def target(t,c,receiver):
        b=rowdata[t]['logs'][c]
        if b is None:return
        e=records[t]['w_factorization'].get(receiver,0)
        assert e>0 and receiver<t
        targets.append(dict(q=t,c=c,p=receiver,e=e,a=b%receiver**e))
    target(q,0,3);target(q,1,p)
    for c in (0,1):target(p,c,1429)
    for t,receiver in [(20771,5),(40487,653),(11,5),(23,11),(67,11)]:
        for c in (0,1):target(t,c,receiver)
    B={}
    for t in targets:B.setdefault(t['p'],set()).add((t['e'],t['a']))
    forbidden1429={a for e,a in B[1429]}
    digit1429=next(z for z in range(1429) if z not in forbidden1429)
    residues={t**e:0 for t,e in Uf.items()}
    residues.update({2:1,27:14,5:1,11:1,653:1,1429:digit1429,1523:1,p:0})
    assert set(residues)=={t**e for t,e in Uf.items()}
    x,M=crt(residues);assert M==U
    for z in targets:assert x%z['p']**z['e']!=z['a']
    lifts={t**e:residues.get(t**e,0) for t,e in Lf.items()}
    # Replace only the private3 digits, retaining all coarse digits.
    lifts[3**Lf[3]]=logs[1]%(3**Lf[3])
    d,ML=crt(lifts);assert ML==L and d%U==x
    vals={str(t):[valmod(rd['r']-3**c-pow(5,d,t**rd['K']),t,rd['K']) for c in (0,1)] for t,rd in rowdata.items()}
    for t,rd in rowdata.items():assert all(v not in rd['E'] for v in vals[str(t)])
    badlifts=dict(lifts);badlifts[3**Lf[3]]=(logs[1]+81)%(3**Lf[3])
    bad,MM=crt(badlifts);assert MM==L and bad%U==x
    badvals={str(t):[valmod(rd['r']-3**c-pow(5,bad,t**rd['K']),t,rd['K']) for c in (0,1)] for t,rd in rowdata.items()}
    assert badvals['3'][0]==5
    assert all(badvals[str(t)]==vals[str(t)] for t in roots if t!=3)
    qmix=20771;wmix=records[qmix]['w'];rmix=(1+pow(5,6528,qmix**4))%(qmix**4)
    dmix=6528+wmix*qmix
    mixedvals=[valmod(rmix-3**c-pow(5,dmix,qmix**4),qmix,4) for c in (0,1)]
    assert dmix%5!=2 and mixedvals==[3,0]
    assert valmod(rmix-3-pow(5,2,qmix**4),qmix,4)==1
    assert log_bsgs((rmix-3)%qmix,qmix,wmix)==2
    assert log_bsgs((rmix-1)%qmix,qmix,wmix)==6528
    localD={z for z in range(27) if valmod(z-14,3,3) in [0,2]}
    assert len(localD)==20 and 1 in localD and 14 not in localD
    for z in range(27):
        expected=z in localD
        lifts3=[t for t in range(486) if t%2==1 and t%27==z]
        actual=all(valmod(rowdata[3]['r']-1-pow(5,t,729),3,6) in [1,3,5] for t in lifts3)
        assert expected==actual
    try:
        order(5)
    except ValueError:
        pass
    else:
        raise AssertionError('illegal base5 order accepted')
    return dict(authority_main='71b8d428b32724c37e593bcfd9d5f06a42e72d21',
      arithmetic_closure=list(records.values()),rows={str(t):rowdata[t] for t in sorted(rowdata)},
      targets=targets,blockers={str(t):[dict(e=e,a=a) for e,a in sorted(v)] for t,v in sorted(B.items())},
      U=U,L=L,U_factorization=Uf,L_factorization=Lf,coarse_x=x,
      coarse_CRT=residues,full_CRT=lifts,full_d=d,full_valuations=vals,
      bad_full_d=bad,bad_full_valuations=badvals,
      q_rigid=dict(q=q,r=rq,high_digit=h,logs=logs,projections27=[b%27 for b in logs],
        valuations_at_logs=[valmod(rq-3**c-pow(5,logs[c],q*q),q,2) for c in (0,1)]),
      local3=dict(D_sorted=sorted(localD),D_mass='20/27',hybrid_B=[1],
        hybrid_union='20/27',P4_both_B=[1,14],P4_both_union='21/27',
        P4_scalar_bound='22/27',uniform_P4_bound='89/108'),
      mixed_anchor_regression=dict(q=qmix,K=4,E=[1,3],r=rmix,d=dmix,logs=[6528,2],
        rigid_anchor1_guard_valuation=1,rigid_blocker=dict(p=5,forbidden=2,chosen=dmix%5),valuations=mixedvals,
        conclusion='Rigid anchor1 blocked, dynamic anchor0 remains FATAL'),
      scope=dict(prime_scan=False,full_period_enumeration=False,actual_anchor_cells_checked=36,
        new_arithmetic_class_separation=False,coarse3_classes_checked=27,coarse3_full_cells_checked=243,
        previous_P4_alternative='20771->5,40487->653,1645333507->3',
        previous_G3_alternative='1645333507->30469139->1429 plus free controls'))

if __name__=='__main__':
    out=run(); path=Path(__file__).parent/'actual_results.json'
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:out[k] for k in ['U','L','coarse_x','full_d','full_valuations','bad_full_d','q_rigid','mixed_anchor_regression']},ensure_ascii=False,indent=2))
