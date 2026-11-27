# Mixed-order cuts for fixed-axis transport

Use the [fixed-axis norm-shell allocation](FIXED_AXIS_NORM_ALLOCATION.md) and the [seven normalized 3-primary classes](FIXED_AXIS_THREE_PRIMARY_TRANSPORT.md). Fix the integer data, \(c=C_*(n)\) at the unit primes, and the parity of \(d\). For a hard inert row \(p\) with collision class \(e_p\bmod o_p\), write
\[
 o_p=2^{\epsilon_p}3^{a_p}\sigma_p m_p
\]
where \(\sigma_p\) contains the odd split prime powers in the order, and \(m_p\) the remaining inert factors other than 3. Let \(I_p\) be the matching ball on the 3-coordinate, and \(J_p\) the product matching ball on the split coordinates. A mismatched parity passes. On the chosen parity, either \(d_3\notin I_p\) or the split-coordinate vector outside \(J_p\) guarantees avoiding the row independent of the remaining digits. This is exact for the hard test if \(m_p=1\), and conservative otherwise.

With \(K=\max(3,\max_p a_p)\), enumerate prefixes \(t\bmod3^K\) that allow the normalized 3-condition; the residue is fixed modulo \(3^{K+1}\) and a zero ball there can be improved by lifting. The hard rows alone leave the guaranteed split set
\[
 U_t=D\setminus\bigcup_{p:\,t\in I_p}J_p .
\]
Use product-ball inclusion–exclusion to count it. A 27-class may be disjoint from a 3-ball, entirely within it, or partially active; the third case must be refined. To find one split-coordinate vector that keeps each of several 27-classes alive, select one allowed prefix per class and intersect their \(U_t\)'s. This is stronger than asking that each class has its own split vector.

A residue-independent sufficient condition for assigning a family of hard rows to split coordinates is a matching with capacity \(\ell-1\) rows at each split prime \(\ell\) in their orders, since a row can forbid only one residue of that first digit. Alternatively, on a colliding parity the normalized 3-allowable set has measure \(1/4\). Thus a sufficient total relative measure bound for leaving at least one phase is
\[
 \sum_p \min(1,4\cdot3^{-a_p})/\sigma_p<1.
\]
Once hard rows pass, repair remaining older inert rows sequentially along their own coordinates when necessary; they preserve all declared hard-row avoidances on 3 and split digits.

At a putatively first growth-box blocker \(q\), add its terminal hard test with the faster of the two lifting depths. Higher free digits at \(q\) can repair the zero case. Consequently exhaustion of the full box implies \(U_t=\varnothing\) for \(t\notin I_q\) and \(U_t\subseteq J_q\) for \(t\in I_q\), or every \(U_t\) empty if there is no hard terminal row. This is a necessary cut condition in the general case and an exact test for this frozen-\(c\) residual system when the ignored \(m_p\)'s are all trivial. It does not establish a global blocker.

The replay below gives a true integer \(n=6+x^2+y^2\) with three actual base-5-only exceptional primes. The first two hard conditions can be read on split coordinates; the third forbids the \(5\bmod27\) class in the conservative split-only cut because its remaining factor \(r\) is inert. Using \(d=2\bmod1429\) makes that \(r\)-condition a unit, and then \(d=1\bmod r\) avoids the third hard row; the shared split choices also serve the other six classes. At 811, a separate ordinary row demonstrates partial activation within the same 27-class. Its collision can be repaired; it is not asserted to be a hard row. No common Wieferich obstruction is constructed.

~~~python
from math import prod
p,q,t,r=20771,40487,1645333507,30469139
rows=((972,1,2),(p*p,1,396223246),(q*q,3,1344791133),
      (t*t,0,970408344854485078),(811**2,0,340431),(r**3,r,r))
M=prod(m for m,_,_ in rows)
def crt(index):
 return sum(row[index]*(M//m)*pow(M//m,-1,m) for row in rows for m in [row[0]])%M
x,y=crt(1),crt(2); n=6+x*x+y*y
assert n%12==11
for s,o,e,fs in [(p,5*31*67,3,(5,31,67)),(q,2*31*653,3,(2,31,653)),
                  (t,2*27*r,5,(2,3,r))]:
 assert pow(5,o,s*s)==1 and all(pow(5,o//f,s)!=1 for f in fs)
 assert (n-1-pow(5,e,s*s))%s==0 and (n-1-pow(5,e,s*s))%(s*s)!=0
 assert pow(3,s-1,s*s)!=1
assert pow(5,1429*1523,r)==1
assert pow(5,1429,r)!=1 and pow(5,1523,r)!=1
assert (n-1)%r==5
d=868674543507221
assert (d%27,d%r,d%1429,d%5,d%653)==(5,1,2,1,1)
assert (n-pow(5,d,243))%243==45
assert (n-1-pow(5,d,t))%t==1284060397
assert all((n-1-pow(5,d,s))%s for s in (p,q,t,r))
assert all((n-pow(5,d,243))%243 in (81,162) for d in (17,71))
assert (n-1-pow(5,17,811))%811==0 and (n-1-pow(5,71,811))%811!=0

~~~
