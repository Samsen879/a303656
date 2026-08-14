#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def first_primes_3mod4(count:int)->list[int]:
    if count<=0:return []
    limit=64
    while True:
        sieve=bytearray(b'\x01')*(limit+1);sieve[0:2]=b'\x00\x00'
        p=2
        while p<=limit//p:
            if sieve[p]:
                start=p*p
                sieve[start:limit+1:p]=b'\x00'*(((limit-start)//p)+1)
            p+=1
        out=[n for n in range(3,limit+1,4) if sieve[n]]
        if len(out)>=count:return out[:count]
        limit*=2

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--counts',default='16,32,64,128,256,512,1024,2048,4096,8192')
    ap.add_argument('--out-dir',required=True);ap.add_argument('--json',required=True)
    a=ap.parse_args();counts=sorted(set(int(x) for x in a.counts.split(',') if x.strip()));out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    ps=first_primes_3mod4(max(counts));records=[]
    for k in counts:
        f=out/f'primes_numeric_{k}.txt';f.write_text(','.join(map(str,ps[:k]))+'\n')
        records.append({'count':k,'file':str(f),'maximum_prime':ps[k-1]})
        print(f'count={k} max_prime={ps[k-1]} file={f}')
    Path(a.json).write_text(json.dumps({'method':'exact_integer_sieve_of_eratosthenes','records':records},indent=2)+'\n')
if __name__=='__main__':main()
