// Run with Node.js. These controls do not replay the 28-prime window.
const same = (a,b,p) => (a-b)%p === 0;
function v(a,p) {
  if (!a) return 'Z';
  let j=0; for (; a%p===0; ++j) a/=p;
  return j%2 ? 'O' : 'E';
}
const check = (x) => { if (!x) throw Error('valuation control failed'); };
const roots=[705,3125,20307];
check(same(roots[0], roots[1],121) && same(roots[0],roots[2],121));
check(!same(roots[0],roots[1],1331));
for (let i=0;i<121;i++) {
  const t=roots[0]+11*i;
  const [a,b,c]=roots.map(r=>v(t-r,11));
  if (a==='O' && b==='O') check(c==='O');
}
const p=83, rs=Array.from({length:5},(_,i)=>125+p*i);
const contact=Array.from({length:p},(_,j)=>rs.filter(r=>same(r,125+p*j,p*p)).length);
check(contact.filter(n=>n===1).length===5 && contact.filter(n=>n===0).length===78);
// All weights use denominator p(p+1). Each contact branch contributes p
// units to its single-even state and one unit to the all-odd state.
const allOdd=BigInt(78*(p+1)+5), singleEven=BigInt(p);
check(allOdd===79n*singleEven && allOdd+5n*singleEven===83n*84n);
