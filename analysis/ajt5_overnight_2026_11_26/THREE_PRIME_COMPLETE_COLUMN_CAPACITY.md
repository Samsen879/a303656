# At most two complete even-3-depth negative columns in a three-prime model

For the actual integer \(n\equiv73\bmod100\), let \(t=n-5^d>0\) at a positive column. A column is certified negative in this model if every actual residual \(t-3^c\ge0\) is blocked either by odd part \(3\bmod4\), by odd 3-adic valuation, or by an odd valuation at one of at most three distinct inert primes \(p\ge7\). Allow each column to choose its own primes and depths. Among columns with even \(v_3(t)\), at most two have such certificates. This is not an upper bound on the number of true negative columns with unrestricted certificates.

Here \(t\equiv0\bmod4\). If \(v_3(t)=2s\), put \(u=t/9^s\). Even values of \(c\) are negative already modulo 4 and odd \(c<2s\) by their exact 3-adic valuation. Thus the remaining positive rows are \(9^s(u-3\cdot9^j)\), with \(j\ge0\) and \(3\cdot9^j<u\); \(u\equiv0\bmod4\) rules out a zero here. For any inert \(p\ge7\), \(\operatorname{ord}_p9\) is odd, cannot be one, and equals three only for 7 by \(9^3-1=2^3\cdot7\cdot13\). On five consecutive \(j\) values, three primes therefore cover at most \(2+1+1\) of the rows, even before testing valuation parity. Hence a three-prime certificate needs \(u<3\cdot9^4=19683\).

The following exact enumeration finds the possible normalized cores. Because \(u\) must be 2 or 3 modulo 5 from \(n-5^d\) and \(9^s\), the surviving cores are \(9572,10132,10748,14752,16208\).
```javascript
function support(n) {
  const out=[];
  for(let p=2;p*p<=n;p++) if(n%p===0){
    let e=0; while(n%p===0){n/=p;e++}
    if(p%4===3 && e%2) out.push(p);
  }
  if(n%4===3) out.push(n);
  return out;
}
const tally=Array.from({length:4},()=>[0,0,0,0]), cores=[];
for(let u=4;u<19683;u+=4){
  if(u%3===0) continue;
  let rows=[]; for(let a=3;a<u;a*=9) rows.push(support(u-a));
  let t=tally[rows.length-1]; t[0]++;
  if(rows.some(x=>!x.length)){t[1]++;continue}
  let dp=Array(1<<rows.length).fill(99);dp[0]=0;
  for(const p of new Set(rows.flat())){
    let m=rows.reduce((x,row,j)=>row.includes(p)?x|(1<<j):x,0);
    for(let j=0;j<dp.length;j++)dp[j|m]=Math.min(dp[j|m],dp[j]+1);
  }
  if(dp.at(-1)===3){t[2]++;if([2,3].includes(u%5))cores.push(u)}
  else {if(dp.at(-1)!==4)throw Error('unexpected cover');t[3]++}
}
if(JSON.stringify(tally)!=='[[4,4,0,0],[36,36,0,0],[324,322,2,0],[2916,2878,21,17]]'
   ||cores.join()!=='9572,10132,10748,14752,16208') throw Error('certificate');
```

All deep columns, \(5^d\le n/2\), have \(n/(2\cdot16208)\le9^s<n/9572\). This interval has ratio less than nine, so two deep columns would use the same \(s\). Since \(n\equiv23\bmod25\), allowable values of \(u9^s\bmod25\) are 22,18,23 for \(d=0,1,\ge2\), respectively. Looping \(s\bmod10\) (the order of 9 modulo 25) and requiring a lower \(d\) to have a larger \(u\) leaves:
- \(s=1\bmod10\): cores \(16208,9572\) at \(d=0,\ge2\), or \(14752,9572\) at \(d=1,\ge2\).
- \(s=9\bmod10\): cores \(10748,10132\) at \(d=0,\ge2\).
The case of \(16208,14752\) at \(d=0,1\) is impossible directly, since their difference times \(9^s\) would have to be four.

The remaining equations are \(5^K-1=C9^s\) with \(s\ge1\) and \(C=6636,1036,616\), where in the \(d=1\) case we divided by 5. All three \(C\) are multiples of 7, so \(6\mid K\). The identity \(v_3(5^{6j}-1)=2+v_3(j)\) yields \(K\ge6\cdot3^{v_3(C)}9^{s-1}\). But \(5^{6\cdot3^{v_3(C)}}-1>9C\) in each case, and raising to the \(9^{s-1}\)-th power and using Bernoulli's inequality contradicts \(5^K-1=C9^s\). Thus there is at most one deep column. There can be at most one shallow column, since \(n/2<5^d<n\) is shorter than a factor of five. The stated capacity follows.

For an explicit complete negative column allowed by the model, at \(n=11373,d=4\) the core is \(10748\). Its four nonautomatic rows are \(10745,10721,10505,8561\), with odd witnesses \(7,71,11,7\), respectively (all valuation one). This is not a nonrepresentation of the whole integer.
