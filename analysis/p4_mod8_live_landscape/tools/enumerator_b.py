#!/usr/bin/env python3
"""Enumerator B: independently indexed live-only masks and separate dead masks."""
import argparse, hashlib, json, struct
from collections import Counter

P=(3,7,11,23); Q=(9,49,121,529); LOW=183968950234

def make_pairs():
    # Independent closed rectangle construction: 24 by 17 minus (23,16).
    a=[1]
    for _ in range(23): a.append(a[-1]*3)
    b=[1]
    for _ in range(16): b.append(b[-1]*5)
    pairs=[]
    for c in range(24):
      for d in range(17):
       if (c,d)!=(23,16): pairs.append((c,d,a[c]+b[d]))
    if any(s>LOW for _,_,s in pairs) or a[23]+b[16]<=LOW: raise SystemExit('activation-cell rectangle error')
    return pairs

def build(subdomain,p):
    result=[0]*(p*p)
    # Pair-centric: the p-1 exact-one residues are shift+k*p mod p^2.
    for j,(_,_,s) in enumerate(subdomain):
      for k in range(1,p): result[(s+k*p)%(p*p)] |= 1<<j
    return result

def scatter(mask, positions):
    full=0
    while mask:
      lsb=mask & -mask; j=lsb.bit_length()-1; full |= 1<<positions[j]; mask-=lsb
    return full

def idx_digest(x): return hashlib.sha256(b''.join(struct.pack('<H',i) for i in x)).hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('output');a=ap.parse_args()
 pairs=make_pairs(); live_pos=[i for i,(c,d,_) in enumerate(pairs) if not(c&1 and not(d&1))]
 dead_pos=[i for i,(c,d,_) in enumerate(pairs) if c&1 and not(d&1)]
 live_pairs=[pairs[i] for i in live_pos]; dead_pairs=[pairs[i] for i in dead_pos]
 if len(live_pairs)!=300 or len(dead_pairs)!=107: raise SystemExit('partition count error')
 lm=[build(live_pairs,p) for p in P]; dm=[build(dead_pairs,p) for p in P]
 hist=Counter();sh=Counter();hs=hashlib.sha256();ss=hashlib.sha256();mx=-1;ac=0;first=None;sm=-1;sac=0;sf=None;top={}
 for x0 in range(Q[0]):
  for x1 in range(Q[1]):
   l01=lm[0][x0]|lm[1][x1]; d01=dm[0][x0]|dm[1][x1]
   for x2 in range(Q[2]):
    l012=l01|lm[2][x2]; d012=d01|dm[2][x2]
    for x3 in range(Q[3]):
     t=(x0,x1,x2,x3); l=l012|lm[3][x3]; d=d012|dm[3][x3]; h=l.bit_count()
     hs.update(struct.pack('<5H',*t,h));hist[h]+=1
     if h>mx: mx=h;ac=1;first=t;top={k:v for k,v in top.items() if v['H8']>=mx-2}
     elif h==mx:ac+=1
     if h>=mx-2:
      full=scatter(l,live_pos)|scatter(d,dead_pos); raw=full.to_bytes(51,'little');key=hashlib.sha256(raw).hexdigest()
      e=top.get(key)
      if e is None:
       e={'mask_digest':key,'mask_hex':raw.hex(),'H8':h,'raw_G':h+d.bit_count(),'covered_dead':d.bit_count(),
          'tuple_multiplicity':0,'first_tuple':list(t)};top[key]=e
      e['tuple_multiplicity']+=1
     if x0==2:
      ss.update(struct.pack('<5H',*t,h));sh[h]+=1
      if h>sm:sm=h;sac=1;sf=t
      elif h==sm:sac+=1
 top=[v for v in top.values() if v['H8']>=mx-2];top.sort(key=lambda v:(-v['H8'],v['mask_digest']))
 out={'schema':'a303656-p4-mod8-live-enumerator-b-v1','method':'independent live-only pair indexing plus separate dead reconstruction',
  'tuple_count':9*49*121*529,'histogram':{str(k):hist[k] for k in sorted(hist)},'minimum':min(hist),'maximum':mx,
  'argmax_count':ac,'first_argmax':list(first),'stream_digest':hs.hexdigest(),
  't3eq2':{'tuple_count':49*121*529,'histogram':{str(k):sh[k] for k in sorted(sh)},'minimum':min(sh),'maximum':sm,
   'argmax_count':sac,'first_argmax':list(sf),'stream_digest':ss.hexdigest()},
  'partition':{'dead_count':107,'live_count':300,'dead_indices_digest':idx_digest(dead_pos),'live_indices_digest':idx_digest(live_pos)},
  'top_band_masks':top}
 with open(a.output,'w') as f:json.dump(out,f,sort_keys=True,separators=(',',':'))
if __name__=='__main__':main()
