"""Independent integer replay of the budget-16 adaptive cover exclusion."""
import argparse
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from math import isqrt
from pathlib import Path

from paths import HERE,R5
from ajt5_integer_certificates import parse, MAX_BYTES


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rows(r, a, level):
    cells=set()
    for j in range(8):
        if a & 2**j:
            cells.update(("Q",e,c) for e in (j,j+1)
                         for c in range(14+level))
        else:
            end = 11 if j==7 and level==0 else 12+max(0,level-1)
            cells.update(("P",j,c) for c in range(end+1))
    return {5*(5**d+3**c) if side=="P" else 5**d+3**c-r for side,d,c in cells}


def trial_primes(n):
    sieve=bytearray([1])*(n+1)
    for p in range(2,isqrt(n)+1):
        if sieve[p]:
            sieve[p*p::p]=bytes((n-p*p)//p+1)
    return [p for p in range(2,n+1) if sieve[p]]


def catalogue(universe):
    u=sorted(universe)
    divisors=trial_primes(isqrt(u[-1]-u[0]))
    @lru_cache(None)
    def factor(n):
        factors=[]
        for p in divisors:
            if p*p>n:
                break
            if not n%p:
                if p>3 and p%4==3:
                    factors.append(p)
                while not n%p:
                    n//=p
        if n>3 and n%4==3:
            factors.append(n)
        return factors
    byprime=defaultdict(lambda:defaultdict(set))
    for i,k in enumerate(u):
        for j in u[:i]:
            for p in factor(k-j):
                byprime[p][k%p].update((j,k))
    return {p:{v:frozenset(z) for v,z in c.items()} for p,c in byprime.items()}


def incidence(catalog):
    memberships=defaultdict(list)
    for p,classes in catalog.items():
        for residue,group in classes.items():
            for k in group:
                memberships[k].append((p,residue))
    return memberships


def check_tree(node,active,available,budget,stats,memberships=None):
    need(type(node)==list and len(node)==2,"tree node")
    s,data=node
    need(type(s)==int and type(data)==list and len(data)>0,"node type")
    if type(data[0])==int:
        need(s>0 and len(data)==len(active) and all(type(w)==int and 0<=w<=s for w in data),
             "invalid weight or dimension")
        if memberships is None:
            memberships=incidence(available)
        sums=Counter()
        for k,w in zip(sorted(active),data):
            if w:
                for pair in memberships[k]:
                    if pair[0] in available:
                        sums[pair]+=w
        excess=Counter()
        for (p,_),total in sums.items():
            if total-s>excess[p]:
                excess[p]=total-s
        penalty=sum(excess.values())
        surplus=sum(data)-penalty-budget*s
        need(surplus>0,"non-strict integer leaf")
        stats["leaves"]+=1
        margin=Fraction(surplus,s)
        stats["min_margin"]=min(stats.get("min_margin",margin),margin)
        return
    need(s in available,"unavailable prime")
    multi={v:(z&active) for v,z in available[s].items() if len(z&active)>1}
    need(bool(multi),"branch without multiroot class")
    required={None,*multi}
    rest={p:v for p,v in available.items() if p!=s}
    for edge in data:
        need(type(edge)==list and len(edge)==2,"branch edge")
        residue,child=edge
        need((residue is None or type(residue)==int) and residue in required,"invalid branch")
        required.remove(residue)
        if residue is None:
            check_tree(child,active,rest,budget,stats,memberships)
        else:
            check_tree(child,active-multi[residue],rest,budget-1,stats,memberships)
    need(not required,"missing branch")
    stats["multiroot_branches"]+=1


def checked_record(stream,r,a):
    rec=parse(stream.readline(MAX_BYTES+1))
    need(type(rec)==list and len(rec)==3 and type(rec[0])==int and type(rec[1])==int and
         rec[:2]==[r,a],"direction order or duplication")
    return rec[2]


def verify(proof):
    old=R5/"global_all15.jsonl.gz"
    need(hashlib.sha256(old.read_bytes()).hexdigest()==
         "eddd459ce610e60118b6bc6084ee13f8191ed3a6eaa7c65ea45b2318cf372685","R5 proof digest")
    stats=Counter()
    maxroot=0
    with gzip.open(old,"rb") as before,gzip.open(proof,"rb") as after:
        for r in range(5):
            catalogs={}
            for a in range(256):
                original=checked_record(before,r,a)
                # Compute the largest source set inducing the same child endpoints.
                adj={e for j in range(8) if a&2**j for e in (j,j+1)}
                b=sum(2**j for j in range(8) if j in adj and j+1 in adj)
                need(all(rows(r,b,h)<=rows(r,a,h) for h in range(4)), "unsafe direction reduction")
                stats["directions"]+=1
                if a!=b:
                    continue
                branches=checked_record(after,r,a)
                need(type(branches)==list and len(branches)==3,"three alternatives required")
                stats["closed_directions"]+=1
                for t,case in enumerate(branches):
                    if case=="reuse":
                        mode,tree=original[t+1]
                        need(mode=="coarse","coarse reference")
                        leaves=[(t,3,0,tree)]
                        stats["inherited_coarse"]+=1
                    else:
                        need(type(case)==list and len(case)==9,"all mod27 children required")
                        leaves=[]
                        for i,entry in enumerate(case):
                            need(type(entry)==list and len(entry)==2,"tail leaf")
                            level,tree=entry
                            need(type(level)==int and 0<=level<=3,"invalid tail level")
                            leaves.append((t+3*i,27,level,tree))
                            stats["mod27_level_"+str(level)]+=1
                        stats["split_mod3_classes"]+=1
                    for x,mod,level,tree in leaves:
                        universe=rows(r,a,level)
                        maxroot=max(maxroot,max(universe))
                        # Every root removed here might have odd 3-adic valuation.
                        # At depth 3 stop and conservatively remove all matches.
                        keep={k for k in universe if (x-k)%3!=0 or
                              (mod==27 and (x-k)%9==0 and (x-k)%27!=0)}
                        if level not in catalogs:
                            cat=catalogue(rows(r,0,level)|rows(r,255,level))
                            catalogs[level]=(cat,incidence(cat))
                        cat,by_root=catalogs[level]
                        check_tree(tree,keep,cat,15,stats,by_root)
        need(not before.read(1) and not after.read(1),"trailing directions")
    stats["min_margin"]=str(stats["min_margin"])
    return dict(stats,max_normalized_root=maxroot,first_strict_parent=maxroot//5+1,
                proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("proof",nargs="?",type=Path,default=HERE/"proof.jsonl.gz")
    print(json.dumps(verify(parser.parse_args().proof),sort_keys=True))
