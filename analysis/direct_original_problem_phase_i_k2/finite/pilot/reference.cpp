#include <algorithm>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
using namespace std;using U=uint64_t;using T=__uint128_t;using F=vector<pair<U,unsigned>>;
U isqrt(U x){U r=sqrtl((long double)x);while(T(r+1)*(r+1)<=x)++r;while(T(r)*r>x)--r;return r;}
vector<U> pows(U b,U n){vector<U> a;U x=1;while(x<=n){a.push_back(x);if(x>n/b)break;x*=b;}return a;}
// Independent full deterministic factorization: exact trial through every integer 6k +/- 1.
F factor(U n){F a;for(U p:{U(2),U(3)}){unsigned e=0;while(n&&n%p==0)n/=p,++e;if(e)a.push_back({p,e});}for(U p=5;p<=n/p;p+=6){for(U q:{p,p+2}){unsigned e=0;while(n%q==0)n/=q,++e;if(e)a.push_back({q,e});}}if(n>1)a.push_back({n,1});sort(a.begin(),a.end());return a;}
unsigned val(U n,U p){unsigned e=0;while(n&&n%p==0)n/=p,++e;return e;}
bool local(U m){if(!m)return false;U odd=m;while(odd%2==0)odd/=2;return odd%4==1&&val(m,3)%2==0;}
bool norm(const F&f){for(auto [p,e]:f)if(p%4==3&&e%2)return false;return true;}
U modpow(U a,U e,U m){U r=1;while(e){if(e&1)r=T(r)*a%m;a=T(a)*a%m;e>>=1;}return r;}
pair<int64_t,int64_t> primepair(U p){if(p==2)return {1,1};for(U z=2;;++z){U t=modpow(z,(p-1)/4,p);if(T(t)*t%p!=p-1)continue;U a=p,b=t;while(T(b)*b>p){U r=a%b;a=b;b=r;}U y=isqrt(p-b*b);if(y*y+b*b==p)return {(int64_t)b,(int64_t)y};}}
pair<U,U> squarepair(const F&f){int64_t a=1,b=0;for(auto [p,e]:f){if(p%4==3){U t=1;for(unsigned j=0;j<e/2;++j)t*=p;a*=t;b*=t;continue;}auto [x,y]=primepair(p);for(unsigned j=0;j<e;++j){int64_t aa=a*x-b*y,bb=a*y+b*x;a=aa;b=bb;}}U x=llabs(a),y=llabs(b);return {min(x,y),max(x,y)};}
void jf(ostream&o,const F&f){o<<"[";bool c=false;for(auto [p,e]:f){if(c)o<<",";c=true;o<<"["<<p<<","<<e<<"]";}o<<"]";}
struct Row{unsigned c,d;U m,s,x,y;F f;bool ok,bulk,l23;};
int main(int argc,char**argv){try{if(argc!=4)throw runtime_error("reference points.txt out.jsonl counts|details");ifstream in(argv[1]);ofstream out(argv[2]);bool details=string(argv[3])=="details";U n;
 while(in>>n){vector<Row> rows;auto a=pows(3,n),b=pows(5,n);unsigned zeros=0,R=0,Rbulk=0,A23=0;U minres=0;
 for(unsigned c=0;c<a.size();++c)for(unsigned d=0;d<b.size();++d){U s=a[c]+b[d];if(s==n)++zeros;if(s>=n)continue;U m=n-s;F f=factor(m);bool ok=norm(f),bulk=a[c]<=n/4&&b[d]<=n/4,l23=local(m);rows.push_back({c,d,m,s,a[c],b[d],f,ok,bulk,l23});if(ok){++R;if(!minres||m<minres)minres=m;if(bulk)++Rbulk;}if(bulk&&l23)++A23;}
 out<<"{\"n\":"<<n<<",\"R\":"<<R<<",\"R_inclusive\":"<<R+zeros<<",\"active\":"<<rows.size()<<",\"zero_pairs\":"<<zeros<<",\"R_bulk\":"<<Rbulk<<",\"A23\":"<<A23<<",\"minres\":"<<minres<<",\"pairs\":[";bool comma=false;for(auto&r:rows)if(r.ok){if(comma)out<<",";comma=true;out<<"["<<r.c<<","<<r.d<<"]";}out<<"]";
 if(details){F nf=factor(n);out<<",\"n_factors\":";jf(out,nf);out<<",\"rows\":[";comma=false;for(auto&r:rows){if(comma)out<<",";comma=true;out<<"{\"c\":"<<r.c<<",\"d\":"<<r.d<<",\"residual\":"<<r.m<<",\"shift\":"<<r.s<<",\"power3\":"<<r.x<<",\"power5\":"<<r.y<<",\"factors\":";jf(out,r.f);out<<",\"success\":"<<(r.ok?"true":"false")<<",\"bulk\":"<<(r.bulk?"true":"false")<<",\"L23\":"<<(r.l23?"true":"false");vector<U> bad;U kernel=1;for(auto [p,e]:r.f)if(p%4==3&&e%2)bad.push_back(p),kernel*=p;out<<",\"bad_primes\":[";for(unsigned j=0;j<bad.size();++j){if(j)out<<",";out<<bad[j];}out<<"],\"bad_kernel\":"<<kernel;if(r.ok){auto [aa,bb]=squarepair(r.f);if(T(aa)*aa+T(bb)*bb!=r.m)throw runtime_error("squarepair identity");out<<",\"a\":"<<aa<<",\"b\":"<<bb;}out<<"}";}out<<"]";}
 out<<"}\n";if(!out)throw runtime_error("reference output failure");}
 }catch(exception&e){cerr<<e.what()<<"\n";return 2;}}
