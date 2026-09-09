"""Exact arithmetic helpers, Python standard library only."""
from fractions import Fraction as F
from functools import lru_cache
from math import prod, gcd

@lru_cache(None)
def factor_small(n):
 out={};p=2
 while p*p<=n:
  while n%p==0:out[p]=out.get(p,0)+1;n//=p
  p=3 if p==2 else p+2
 if n>1:out[n]=out.get(n,0)+1
 return out
@lru_cache(None)
def divisors(n):
 ds=[1]
 for p,e in factor_small(n).items():ds=[a*p**i for a in ds for i in range(e+1)]
 return sorted(ds)
def mobius(n):
 f=factor_small(n)
 return 0 if any(e>1 for e in f.values()) else (-1)**len(f)
@lru_cache(None)
def phi_value(n):
 a=b=1
 for d in divisors(n):
  mu=mobius(n//d)
  if mu==1:a*=5**d-1
  if mu==-1:b*=5**d-1
 q,r=divmod(a,b)
 assert r==0
 return q
@lru_cache(None)
def phi_recursive(n):
 N=5**n-1
 for d in divisors(n)[:-1]:
  a=phi_recursive(d);N,r=divmod(N,a);assert r==0
 return N

def phi_derivative(n):
 N=phi_value(n);z=F(0)
 for d in divisors(n):z+=mobius(n//d)*F(d*5**(d-1),5**d-1)
 z*=N;assert z.denominator==1
 return z.numerator

def strong_mr_composite(N,a):
 """True is an exact compositeness witness; False is NOT a primality proof."""
 if N<3 or N%2==0:return N!=2
 if gcd(N,a)!=1:return 1<gcd(N,a)<N
 d=N-1;s=0
 while d%2==0:s+=1;d//=2
 x=pow(a,d,N)
 if x in (1,N-1):return False
 for _ in range(s-1):
  x=x*x%N
  if x==N-1:return False
 return True

@lru_cache(None)
def atanh_log_bounds(t,K=80):
 """Bounds for log((1+t)/(1-t)), 0<=t<1, using a positive series."""
 assert 0<=t<1
 s=F(0);v=t
 for k in range(K):s+=2*v/(2*k+1);v*=t*t
 return s,s+2*v/((2*K+1)*(1-t*t))
@lru_cache(None)
def log_integer_bounds(N):
 assert N>0
 if N==1:return F(0),F(0)
 e=N.bit_length()-1;v=1<<e
 l2,u2=atanh_log_bounds(F(1,3))
 lo,hi=atanh_log_bounds(F(N-v,N+v),40)
 return e*l2+lo,e*u2+hi
@lru_cache(None)
def small_correction(d):
 # Bounds for log(1-5^(-d)); cap huge d without constructing 5**d.
 if d>40:return -F(1,5**41-1),F(0)
 t=F(1,5**d);s=F(0);v=t
 for k in range(1,41):s-=v/k;v*=t
 return s-v/(41*(1-t)),s

def cofactor_digits(n,known_product=1):
 """Certify decimal digits from rational log intervals; no floating point."""
 degree=prod((p-1)*p**(e-1) for p,e in factor_small(n).items())
 l5,u5=atanh_log_bounds(F(2,3))
 low,high=degree*l5,degree*u5
 for d in divisors(n):
  mu=mobius(n//d);a,b=small_correction(d)
  if mu==1:low+=a;high+=b
  elif mu==-1:low-=b;high-=a
 a,b=log_integer_bounds(known_product);low-=b;high-=a
 l2,u2=atanh_log_bounds(F(1,3));l10=l2+l5;u10=u2+u5
 # Called only on cofactors >1.
 assert low>0
 low/=u10;high/=l10
 f1=low.numerator//low.denominator;f2=high.numerator//high.denominator
 assert f1==f2,('digit interval crosses integer',n)
 return f1+1
