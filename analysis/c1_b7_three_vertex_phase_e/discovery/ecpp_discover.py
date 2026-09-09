"""Discovery only. All claims require the separate exact certificate verifier.
CM parameters are hints, never assumed correct by the verifier.
"""
import math,json,time,sys,signal
from pathlib import Path
import sympy as S
import mpmath as mp
P=Path(__file__).resolve().parent
DB=P/'prime_certificates.json'
certs=json.loads(DB.read_text()) if DB.exists() else {}
start=time.monotonic(); deadline=start+float(sys.argv[2] if len(sys.argv)>2 else 35)

def save(): DB.write_text(json.dumps(certs,indent=2))
def tick():
 if time.monotonic()>deadline: save(); raise TimeoutError('discovery budget reached; certified nodes saved')
def sqrtmod(a,n):
 a%=n
 if a==0:return 0
 if pow(a,(n-1)//2,n)!=1:return None
 if n%4==3:return pow(a,(n+1)//4,n)
 d=n-1;s=0
 while not d&1:d//=2;s+=1
 z=2
 while pow(z,(n-1)//2,n)!=n-1:z+=1
 c=pow(z,d,n);x=pow(a,(d+1)//2,n);t=pow(a,d,n);m=s
 for _ in range(s+1):
  if t==1:return x
  i=1;u=t*t%n
  while i<m and u!=1:u=u*u%n;i+=1
  if i==m:return None
  b=pow(c,1<<(m-i-1),n);x=x*b%n;t=t*b*b%n;c=b*b%n;m=i
 return None

def add(Pt,Qt,a,n):
 if Pt is None:return Qt
 if Qt is None:return Pt
 x,y=Pt;u,v=Qt
 if x==u:
  if (y+v)%n==0:return None
  if y!=v:raise ArithmeticError('ambiguous addition')
  den=2*y%n;num=(3*x*x+a)%n
 else:den=(u-x)%n;num=(v-y)%n
 if math.gcd(den,n)!=1:raise ArithmeticError('nonunit denominator')
 t=num*pow(den,-1,n)%n
 z=(t*t-x-u)%n
 return (z,(t*(x-z)-y)%n)
def mul(k,Pt,a,n):
 R=None
 while k:
  if k&1:R=add(R,Pt,a,n)
  k//=2
  if k:Pt=add(Pt,Pt,a,n)
 return R

def corn(n,D):
 if D%4==0:
  d=(-D)//4;r=sqrtmod(-d,n)
  if r is None:return None
  for b in [r,n-r]:
   a=n
   while b*b>n:a,b=b,a%b
   if b==0:continue
   z=n-b*b
   if z%d:continue
   y=math.isqrt(z//d)
   if y*y*d==z:return 2*b,y
 else:
  d=-D;r=sqrtmod(D,n)
  if r is None:return None
  for b in [r,n-r,n+r,2*n-r]:
   if b%2==0:continue
   a=2*n
   while b*b>4*n:a,b=b,a%b
   if b==0:continue
   z=4*n-b*b
   if z%d:continue
   y=math.isqrt(z//d)
   if y*y*d==z:return b,y
 return None

def forms(D):
 out=[]
 for a in range(1,math.isqrt((-D)//3)+1):
  for b in range(-a,a+1):
   if (b*b-D)%(4*a):continue
   c=(b*b-D)//(4*a)
   if a>c or math.gcd(a,math.gcd(b,c))!=1:continue
   if (abs(b)==a or a==c) and b<0:continue
   out.append((a,b,c))
 return out
H_PATH=P/'class_polys.json'
def buildH():
 if H_PATH.exists():return {int(k):v for k,v in json.loads(H_PATH.read_text()).items()}
 H={};mp.mp.dps=130
 for D in range(-3,-501,-1):
  if D%4 not in (0,1):continue
  fs=forms(D)
  if not fs or len(fs)>2:continue
  cs=[mp.mpc(1)]
  for a,b,c in fs:
   z=(-mp.mpf(b)+mp.sqrt(mp.mpc(D)))/(2*a);q=mp.exp(2*mp.pi*1j*z)
   e4=mp.mpc(1);de=mp.mpc(q)
   for k in range(1,80):
    e4+=240*sum(d**3 for d in S.divisors(k))*q**k
    de*=(1-q**k)**24
   j=e4**3/de
   new=[mp.mpc(0)]*(len(cs)+1)
   for i,c0 in enumerate(cs):new[i]+=c0;new[i+1]-=j*c0
   cs=new
  ints=[]
  for c0 in cs:
   v=int(mp.nint(c0.real))
   if abs(c0-v)>mp.mpf('1e-30'):raise ArithmeticError(('rounding',D,c0))
   ints.append(v)
  H[D]=ints
 H_PATH.write_text(json.dumps(H,indent=2));return H
H=buildH()
def getH(D):
 if D in H:return H[D]
 fs=forms(D)
 dps=int(math.pi*math.sqrt(-D)*sum(1/a for a,b,c in fs)/math.log(10))+80
 with mp.workdps(dps):
  cs=[mp.mpc(1)]
  for a,b,c in fs:
   z=(-mp.mpf(b)+mp.sqrt(mp.mpc(D)))/(2*a)
   j=1728*mp.kleinj(z)
   new=[mp.mpc(0)]*(len(cs)+1)
   for i,c0 in enumerate(cs):new[i]+=c0;new[i+1]-=j*c0
   cs=new
  out=[]
  for c0 in cs:
   v=int(mp.nint(c0.real))
   if abs(c0-v)>mp.mpf('1e-25'):raise ArithmeticError(('class poly precision',D))
   out.append(v)
 H[D]=out;H_PATH.write_text(json.dumps(H,indent=2));return out

def polyroot(h,n):
 from sympy.polys.galoistools import gf_pow_mod,gf_gcd,gf_sub_ground
 from sympy.polys.domains import ZZ
 h=[v%n for v in h]
 for k in range(1,200):
  if len(h)==2:return -h[1]*pow(h[0],-1,n)%n
  g=gf_pow_mod([1,k],(n-1)//2,h,n,ZZ)
  g=gf_sub_ground(g,1,n,ZZ)
  f=gf_gcd(h,g,n,ZZ)
  if 1<len(f)<len(h):h=list(map(int,f))
 return None


def cm_candidates(n):
 path=P/f'cm_candidates_{n}.json'
 if path.exists():return [(int(q),D,int(m)) for q,D,m in json.loads(path.read_text())]
 bound=(math.isqrt(math.isqrt(n))+2)**2
 candidates=[]
 for D in range(-3,-1501,-1):
  if D%4 not in (0,1):continue
  fs=forms(D)
  if not fs or len(fs)>12:continue
  tick();cv=corn(n,D)
  if cv is None:continue
  u,v=cv
  traces={u,-u}
  if D==-3:traces.update([(u+3*v)//2,-(u+3*v)//2,(u-3*v)//2,-(u-3*v)//2])
  if D==-4:traces.update([2*v,-2*v])
  for t in traces:
   m=n+1-t
   fac=S.factorint(m,limit=3000)
   for q in fac:
    q=int(q)
    if bound<q<n and S.isprime(q):candidates.append((q,D,m))
 candidates=sorted(set(candidates))
 path.write_text(json.dumps([[str(q),D,str(m)] for q,D,m in candidates]))
 return candidates

def curve_cert(n,q,D,m):
 h=getH(D)
 if len(h)==2:js=[-h[1]%n]
 elif len(h)==3:
  disc=(h[1]*h[1]-4*h[2])%n;rt=sqrtmod(disc,n)
  if rt is None:return None
  js=[(-h[1]+rt)*pow(2,-1,n)%n] # either root suffices
 else:
  j=polyroot(h,n)
  if j is None:return None
  js=[j]
 for j in js:
  if j==0:curves=[(0,b) for b in range(1,16)]
  elif j==1728:curves=[(a,0) for a in range(1,16)]
  else:
   k=j*pow(1728-j,-1,n)%n;a=3*k%n;b=2*k%n;d=2
   while pow(d,(n-1)//2,n)!=n-1:d+=1
   curves=[(a,b),(a*d*d%n,b*d*d*d%n)]
  for a,b in curves:
   tick()
   if math.gcd(4*a*a*a+27*b*b,n)!=1:continue
   for x in range(1,30):
    y=sqrtmod((x*x*x+a*x+b)%n,n)
    if y is None:continue
    Pt=(x,y)
    try:
     M=mul(m//q,Pt,a,n)
     if M is not None and mul(q,M,a,n) is None:
      return {'kind':'ec','a':str(a),'b':str(b),'x':str(M[0]),'y':str(M[1]),'q':str(q),'discovery_D':D,'discovery_m':str(m)}
    except ArithmeticError:pass
    break # wrong twist/order, another point very unlikely to help
 return None

failed=set()
def prove(n,level=0):
 tick();key=str(n)
 if key in certs:return True
 if n<1000000:
  if n<2 or any(n%d==0 for d in range(2,math.isqrt(n)+1)):return False
  certs[key]={'kind':'trial'};save();return True
 if n in failed:return False
 if not S.isprime(n):return False
 # Fast partial n-1 Pocklington. Recursively prove the largest PRP divisor first.
 fac=S.factorint(n-1,limit=5000)
 known={};wits={};F=1
 for q,e in sorted(fac.items(),reverse=True):
  q=int(q);e=int(e)
  if not S.isprime(q):continue
  # Avoid spending many levels on a factor unless it has meaningful leverage.
  if q>1000000 and len(str(q))>15:
   f2=S.factorint(q-1,limit=1500)
   if not any(S.isprime(p) and p>math.isqrt(q) for p in f2) and len(str(q))>30:continue
  if prove(q,level+1):
   for a in range(2,100):
    if pow(a,n-1,n)==1 and math.gcd(pow(a,(n-1)//q,n)-1,n)==1:
     F*=q**e;known[str(q)]=e;wits[str(q)]=a;break
   if F*F>n:
    certs[key]={'kind':'pocklington','factors':known,'witnesses':wits};save();return True
 print('CM SEARCH',' '*min(level,6),len(str(n)),n,flush=True)
 cand=cm_candidates(n)
 print('CM CANDIDATES',len(str(n)),[(len(str(q)),D) for q,D,m in cand[:8]],flush=True)
 for q,D,m in cand:
  tick();rec=curve_cert(n,q,D,m)
  if rec is not None and prove(q,level+1):
   certs[key]=rec;save();print('EC CERTIFIED',len(str(n)),n,flush=True);return True
 failed.add(n);return False

if __name__=='__main__':
 n=int(sys.argv[1])
 def alarm_handler(*_):
  save();raise TimeoutError("hard discovery budget; nodes saved")
 signal.signal(signal.SIGALRM,alarm_handler);signal.alarm(int(max(1,deadline-time.monotonic()))+1)
 try:print('RESULT',prove(n),'nodes',len(certs),flush=True)
 except TimeoutError as e:print(e,flush=True)
 save()
