"""Independent, exact, standard-library-only certificate verifier.
Does NOT import the discovery code, SymPy, mpmath, or CM polynomials.
Certificate types: bounded trial division, partial n-1 Pocklington,
and elliptic-curve prime-order point + Hasse bound.
"""
from pathlib import Path
from math import gcd,isqrt,prod
import json,sys

class InvalidCertificate(ValueError):pass

def require(condition,message):
 if not condition:raise InvalidCertificate(message)

def ec_sum(U,V,A,N):
 if U is None:return V
 if V is None:return U
 x1,y1=U;x2,y2=V
 if x1==x2 and (y1+y2)%N==0:return None
 if x1==x2:
  require(y1==y2,'same-x noninverse ambiguity')
  numerator=(3*x1*x1+A)%N;denominator=(2*y1)%N
 else:numerator=(y2-y1)%N;denominator=(x2-x1)%N
 require(gcd(denominator,N)==1,'noninvertible EC denominator')
 slope=(numerator*pow(denominator,-1,N))%N
 x3=(slope*slope-x1-x2)%N
 return x3,(slope*(x1-x3)-y1)%N

def left_multiply(k,U,A,N):
 V=None
 for bit in bin(k)[2:]:
  V=ec_sum(V,V,A,N)
  if bit=='1':V=ec_sum(V,U,A,N)
 return V

def verify_all(records):
 accepted=set();visiting=set()
 def prove(N):
  if N in accepted:return
  require(N not in visiting,'certificate cycle')
  require(N>=2 and str(N) in records,'missing certificate')
  visiting.add(N);r=records[str(N)];kind=r['kind']
  if kind=='trial':
   require(N<1000000,'trial leaf exceeds limit')
   require(all(N%d for d in range(2,isqrt(N)+1)),'composite trial leaf')
  elif kind=='pocklington':
   F=1
   for qs,e in r['factors'].items():
    q=int(qs);require(q<N and isinstance(e,int) and e>0,'bad Pocklington child')
    prove(q);F*=q**e
    a=int(r['witnesses'][qs])
    require(pow(a,N-1,N)==1,'Fermat witness failure')
    require(gcd(pow(a,(N-1)//q,N)-1,N)==1,'order witness failure')
   require((N-1)%F==0 and F*F>N,'Pocklington bound failure')
  elif kind=='ec':
   require(N>3 and gcd(N,6)==1,'bad EC modulus')
   A=int(r['a']);B=int(r['b']);x=int(r['x']);y=int(r['y']);q=int(r['q'])
   require(all(0<=z<N for z in (A,B,x,y)),'noncanonical EC coordinates')
   require(q<N and q>(isqrt(isqrt(N))+2)**2,'EC Hasse bound failure')
   prove(q)
   require(gcd(4*A**3+27*B**2,N)==1,'singular EC reduction')
   require((y*y-x*x*x-A*x-B)%N==0,'point not on curve')
   require(left_multiply(q,(x,y),A,N) is None,'prime-order EC witness failure')
  else:raise InvalidCertificate('unknown certificate type')
  visiting.remove(N);accepted.add(N)
 for key in records:prove(int(key))
 return accepted

if __name__=='__main__':
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('primality_certificates.json')
 data=json.loads(path.read_text());ok=verify_all(data)
 print('PASS:',len(ok),'proven primes;', {k:sum(r['kind']==k for r in data.values()) for k in ('trial','pocklington','ec')})
