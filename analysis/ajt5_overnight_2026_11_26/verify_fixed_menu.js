function check(ok) { if (!ok) throw new Error("failed exact control"); }
const square = n => n >= 0 && Number.isInteger(Math.sqrt(n));
function labels(base, scale) {
  const D = 3081, cap = base + Math.floor(D * D / scale), hits = [];
  let count = 0;
  for (let c = 0, a = 1; a + 1 <= cap; c++, a *= 3)
    for (let d = 0, b = 1; a + b <= cap; d++, b *= 5) {
      count++;
      const K = scale * (base - a - b), v = D * D + K;
      if (square(K) || (square(v) &&
          [Math.sqrt(v), -Math.sqrt(v)].some(q => square(2 * (D - q)))))
        hits.push([c, d]);
    }
  return [cap, count, hits];
}
check(JSON.stringify(labels(12, 20)) === "[474640,107,[[1,4]]]");
check(JSON.stringify(labels(64, 4)) === "[2373204,138,[[1,2],[3,0]]]");
for (const [p, k] of [[7, 3], [11, 2]]) {
  const n = 2060 ** 2 + k;
  check(n % p === 0 && n % (p * p) !== 0);
}
check(5929 === 7 ** 2 * 11 ** 2);
function pattern(n) {
  return [2, 5, 11].map(p => {
    let q = n, e = 0;
    while (q % p === 0) { q /= p; e++; }
    return e % 2;
  });
}
for (const rows of [[22, 55, 6], [462, 495, 414]])
  check(JSON.stringify(rows.map(pattern)) === "[[1,0,1],[0,1,1],[1,0,0]]");
console.log("PASS: fixed polynomial menu and Eisenstein cover controls");
