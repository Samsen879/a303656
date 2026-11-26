# Five true labels by switching the shared Gaussian factor

Take \(k\ge4\), even \(D\ge4\), \(B=3^k\), and positive odd \(x,y\) with \(x^2-10y^2=-B^2\) and \(5\nmid y\). Set \(t=11x,\ u=22y,\ n=3^{2k+5}+5^D+2t^2\).

The source at \((2k+5,D)\) has coordinate \(t(1+i)\). Dropping the first exponent to \(2k+4\) or \(2k\) increases the residual by \(2(9B)^2\) or \(2(11B)^2\), respectively. At the latter point the certificate \(z=(1+i)(t+11Bi)\) has
\[
 N(z)=2\cdot11^2(x^2+B^2)=5u^2.
\]
Since \(5\nmid u\), the Gaussian gcd with 5 extracts a factor \(w\) of norm 5 by [the transfer criterion](GAUSSIAN_GCD_TRANSFER_FAMILY.md). Dropping the first exponent again to \(2k-4\), or lowering \(D\) to \(D-1\) instead, gives respective increases \(5(4\cdot3^{k-2})^2\) and \(5(2\cdot5^{(D-2)/2})^2\). In each case the new certificate is \(w(u+is)\) with the stated square-root factor \(s\). The five labels are distinct on the same actual integer.

One family uses \(x=3B,y=B\), so \(n=269\cdot3^{2k+2}+5^D\), and \(D=2k\) puts both exponents on ordinary logarithmic scale. Here \(n\equiv6\bmod8,1\bmod3\), which forbids a pure two-power representation: the congruence mod 8 requires an even 3 exponent and odd 5 exponent, giving only 0 or 2 mod 3. Another uses \(x+y\sqrt{10}=(1+\sqrt{10})^k\) for odd \(k\ge7,\ 5\nmid k\). Its norm is \(-3^{2k}\); reducing the binomial expansion mod 2 and mod 5 gives odd coordinates and \(y\equiv k\bmod5\). Mod 3, evaluating at \(\sqrt{10}=\pm1\) shows \(3\nmid x\); hence this second family has center \(n-5^D\) coprime to 3.

The remaining opposite corner \((2k-4,D-1)\) is always false for this family: its residual is \(20((u/2)^2+4\cdot3^{2k-4}+5^{D-2})\). The bracket is \(6\bmod8\), so the odd part of the residual is \(3\bmod4\), ruling out a sum of two squares. This excludes that label, not the integer.

```python
def check(k,D,x,y):
    B=3**k
    assert x*x-10*y*y==-B*B and x%2==y%2==1 and y%5
    t,u=11*x,22*y
    n=3**(2*k+5)+5**D+2*t*t
    p,q=t-11*B,t+11*B
    e=next(e for e in (2,-2) if (p+e*q)%5==(q-e*p)%5==0)
    s,h=4*3**(k-2),2*5**((D-2)//2)
    for c,d,a,b in [(2*k+5,D,t,t),(2*k+4,D,t-9*B,t+9*B),
                    (2*k,D,p,q),(2*k-4,D,u-e*s,e*u+s),
                    (2*k,D-1,u-e*h,e*u+h)]:
        assert n-3**c-5**d==a*a+b*b>0
    assert (n-3**(2*k-4)-5**(D-1))%160==120
    return n

assert check(4,4,243,81)==15884806
x,y=1,0
for _ in range(7):
    x,y=x+10*y,x+y
assert check(7,14,x,y)==35029353174
```
