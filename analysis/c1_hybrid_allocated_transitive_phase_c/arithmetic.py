from math import isqrt

def factor(n):
    out={}; p=2
    while p*p<=n:
        if n%p==0:
            e=0
            while n%p==0: n//=p; e+=1
            out[p]=e
        p=3 if p==2 else p+2
    if n>1: out[n]=1
    return out

def order(p):
    if p == 5:
        raise ValueError("base 5 has no multiplicative order modulo 5")
    assert factor(p)=={p:1}
    w=p-1
    for l in factor(w):
        while w%l==0 and pow(5,w//l,p)==1: w//=l
    assert pow(5,w,p)==1
    return w

def log_bsgs(a,p,w):
    m=isqrt(w)+1; baby={}; z=1
    for j in range(m):
        baby.setdefault(z,j); z=z*5%p
    step=pow(pow(5,m,p),-1,p); cur=a%p
    for i in range(m+1):
        if cur in baby:
            b=i*m+baby[cur]
            if b<w and pow(5,b,p)==a%p: return b
        cur=cur*step%p
    return None

if __name__=='__main__':
    for p in [3,67,1429,1523,20771,40487,30469139,1645333507]:
        w=order(p); s=1
        while pow(5,w,p**(s+1))==1: s+=1
        print(p, factor(p-1), w, factor(w),s)
    q=1645333507; w=order(q)
    for r in range(2,65):
        a,b=r-1,r-3
        if a%q==0 or b%q==0: continue
        if pow(a,(q-1)//2,q)!=pow(b,(q-1)//2,q): continue
        x,y=log_bsgs(a,q,w),log_bsgs(b,q,w)
        if x is not None and y is not None and x%27!=y%27:
            print('PAIR',r,x,y,x%2,y%2,x%27,y%27); break
