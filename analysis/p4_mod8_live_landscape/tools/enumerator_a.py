#!/usr/bin/env python3
"""Enumerator A: 407-bit coverage masks intersected with the A8 mask."""
import argparse, hashlib, json, struct
from collections import Counter

LOW, HIGH = 183968950234, 246731069451
PRIMES = (3, 7, 11, 23)
MODS = tuple(p*p for p in PRIMES)
ROWS = 9*49*121*529

def domain():
    p3=[]; x=1
    while x <= LOW: p3.append(x); x*=3
    p5=[]; x=1
    while x <= LOW: p5.append(x); x*=5
    return [(c,d,a+b) for c,a in enumerate(p3) for d,b in enumerate(p5) if a+b <= LOW]

def prime_masks(pairs, p):
    out=[]
    for t in range(p*p):
        words=0
        for i,(_,_,s) in enumerate(pairs):
            q=(t-s)%(p*p)
            if q%p == 0 and q != 0: words |= 1<<i
        out.append(words)
    return out

def digest_indices(indices):
    return hashlib.sha256(b''.join(struct.pack('<H',i) for i in indices)).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('output'); args=ap.parse_args()
    pairs=domain()
    if len(pairs)!=407 or pairs[-1][:2]!=(23,15): raise SystemExit('bad 407-pair domain')
    if [(c,d) for c,d,s in pairs if s==28] != [(1,2),(3,0)]: raise SystemExit('duplicate shift merged')
    dead_idx=[i for i,(c,d,_) in enumerate(pairs) if c%2==1 and d%2==0]
    live_idx=[i for i in range(407) if i not in set(dead_idx)]
    dead=sum(1<<i for i in dead_idx); live=((1<<407)-1)^dead
    if len(dead_idx)!=107 or len(live_idx)!=300: raise SystemExit('bad mod-8 partition')
    masks=[prime_masks(pairs,p) for p in PRIMES]
    hist=Counter(); shist=Counter(); stream=hashlib.sha256(); sstream=hashlib.sha256()
    maximum=-1; argmax=0; first=None; smax=-1; sarg=0; sfirst=None; top={}
    for t3 in range(MODS[0]):
      m3=masks[0][t3]
      for t7 in range(MODS[1]):
       m37=m3|masks[1][t7]
       for t11 in range(MODS[2]):
        m3711=m37|masks[2][t11]
        for t23 in range(MODS[3]):
         tup=(t3,t7,t11,t23); full=m3711|masks[3][t23]; h=(full&live).bit_count()
         stream.update(struct.pack('<5H',*tup,h)); hist[h]+=1
         if h>maximum:
             maximum=h; argmax=1; first=tup
             top={k:v for k,v in top.items() if v['H8']>=maximum-2}
         elif h==maximum: argmax+=1
         if h>=maximum-2:
             raw=full.to_bytes(51,'little'); key=hashlib.sha256(raw).hexdigest()
             if key not in top:
                 top[key]={'mask_digest':key,'mask_hex':raw.hex(),'H8':h,'raw_G':full.bit_count(),
                           'covered_dead':(full&dead).bit_count(),'tuple_multiplicity':0,
                           'first_tuple':list(tup)}
             top[key]['tuple_multiplicity']+=1
         if t3==2:
             sstream.update(struct.pack('<5H',*tup,h)); shist[h]+=1
             if h>smax: smax=h; sarg=1; sfirst=tup
             elif h==smax: sarg+=1
    top=[v for v in top.values() if v['H8']>=maximum-2]
    top.sort(key=lambda v:(-v['H8'],v['mask_digest']))
    cert={'schema':'a303656-p4-mod8-live-enumerator-a-v1','method':'407-bit full masks intersect A8',
      'tuple_count':ROWS,'histogram':{str(k):hist[k] for k in sorted(hist)},'minimum':min(hist),'maximum':maximum,
      'argmax_count':argmax,'first_argmax':list(first),'stream_digest':stream.hexdigest(),
      't3eq2':{'tuple_count':49*121*529,'histogram':{str(k):shist[k] for k in sorted(shist)},
       'minimum':min(shist),'maximum':smax,'argmax_count':sarg,'first_argmax':list(sfirst),'stream_digest':sstream.hexdigest()},
      'partition':{'dead_count':107,'live_count':300,'dead_indices_digest':digest_indices(dead_idx),
       'live_indices_digest':digest_indices(live_idx)},'top_band_masks':top}
    with open(args.output,'w') as f: json.dump(cert,f,sort_keys=True,separators=(',',':'))

if __name__=='__main__': main()
