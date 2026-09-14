#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sys/resource.h>
using namespace std;
using U=uint64_t; using T=__uint128_t;
struct Shift{U s,x,y; unsigned c,d;};
U root(U x){U r=sqrtl((long double)x);while(T(r+1)*(r+1)<=x)++r;while(T(r)*r>x)--r;return r;}
vector<U> powers(U b,U lim){vector<U> v;for(U x=1;x<=lim;){v.push_back(x);if(x>lim/b)break;x*=b;}return v;}
vector<unsigned> badprimes(U max){unsigned lim=root(max);vector<bool> mark(lim+1,true);vector<unsigned> ps;if(lim>=0)mark[0]=false;if(lim>=1)mark[1]=false;for(unsigned p=2;p<=lim;++p)if(mark[p]){if(p%4==3)ps.push_back(p);if(U(p)*p<=lim)for(U j=U(p)*p;j<=lim;j+=p)mark[j]=false;}return ps;}
vector<Shift> shifts(U upper){vector<Shift> v;auto a=powers(3,upper),b=powers(5,upper);for(unsigned c=0;c<a.size();++c)for(unsigned d=0;d<b.size();++d)if(a[c]+b[d]<upper)v.push_back({a[c]+b[d],a[c],b[d],c,d});return v;}
template<class V>void binary(string path,const vector<V>& v){ofstream f(path,ios::binary);f.write((const char*)v.data(),v.size()*sizeof(V));if(!f)throw runtime_error("binary output failure");}
struct Result{U L,W,classified=0,blocks=0,induced=0,unions=0;unsigned words;vector<Shift> ss;vector<uint16_t> R,active,bulk,A23,zero;vector<U> minres,bits;double seconds;};
Result scan(U L,U W,bool merged){
 auto start=chrono::steady_clock::now();U upper=L+W;Result z;z.L=L;z.W=W;z.ss=shifts(upper);z.words=(z.ss.size()+63)/64;
 z.R.resize(W);z.active.resize(W);z.bulk.resize(W);z.A23.resize(W);z.zero.resize(W);z.minres.resize(W);z.bits.resize(W*z.words);
 auto ps=badprimes(upper-1);vector<pair<U,U>> ranges;
 for(auto h:z.ss){U low=L>h.s?L-h.s:1,hi=upper-h.s;if(low<hi)ranges.push_back({low,hi});}
 z.induced=ranges.size();
 if(merged){sort(ranges.begin(),ranges.end());vector<pair<U,U>> q;for(auto r:ranges){if(q.empty()||q.back().second<r.first)q.push_back(r);else q.back().second=max(q.back().second,r.second);}ranges=q;}
 z.unions=ranges.size();
 // Exact active and zero-residual counts are separate from positive-residual classification.
 for(auto h:z.ss){for(U n=max(L,h.s+1);n<upper;++n)++z.active[n-L];if(h.s>=L&&h.s<upper)++z.zero[h.s-L];}
 auto consume=[&](U low,U hi,int only){
   U len=hi-low;vector<U> rem(len);vector<uint8_t> fail(len),v3odd(len);++z.blocks;z.classified+=len;
   for(U i=0;i<len;++i){U m=low+i;while(m%2==0)m/=2;rem[i]=m;}
   for(unsigned p:ps){if(U(p)*p>=hi)break;U first=low%p?low+(p-low%p):low;for(U m=first;m<hi;m+=p){U i=m-low;unsigned e=0;while(rem[i]%p==0){rem[i]/=p;++e;}if(e%2)fail[i]=1;if(p==3)v3odd[i]=e%2;}}
   for(U i=0;i<len;++i)if(rem[i]%4==3)fail[i]=1;
   for(unsigned k=0;k<z.ss.size();++k){if(only>=0&&unsigned(only)!=k)continue;auto h=z.ss[k];U a=max(low,L>h.s?L-h.s:1),b=min(hi,upper-h.s);if(a>=b)continue;
    for(U m=a;m<b;++m){U j=m+h.s-L,i=m-low;bool bulk=h.x<=(m+h.s)/4&&h.y<=(m+h.s)/4;
     if(bulk){U odd=m;while(odd%2==0)odd/=2;unsigned v=0;U t=m;while(t%3==0)t/=3,++v;if(odd%4==1&&v%2==0)++z.A23[j];}
     if(!fail[i]){++z.R[j];z.bits[j*z.words+k/64]|=U(1)<<(k%64);if(!z.minres[j]||m<z.minres[j])z.minres[j]=m;if(bulk)++z.bulk[j];}
    }
   }
 };
 if(merged){for(auto r:ranges)for(U low=r.first;low<r.second;){U hi=min(r.second,low+(U(1)<<18));consume(low,hi,-1);low=hi;}}
 else{for(unsigned k=0;k<z.ss.size();++k){auto h=z.ss[k];U low=L>h.s?L-h.s:1,hi=upper-h.s;if(low<hi)consume(low,hi,k);}}
 z.seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();return z;
}
void point_json(const Result& z){cout<<"{\"n\":"<<z.L<<",\"R\":"<<z.R[0]<<",\"R_inclusive\":"<<z.R[0]+z.zero[0]<<",\"active\":"<<z.active[0]<<",\"R_bulk\":"<<z.bulk[0]<<",\"A23\":"<<z.A23[0]<<",\"minres\":"<<z.minres[0]<<",\"pairs\":[";bool comma=false;for(unsigned k=0;k<z.ss.size();++k)if(z.bits[k/64]&(U(1)<<(k%64))){if(comma)cout<<",";comma=true;cout<<"["<<z.ss[k].c<<","<<z.ss[k].d<<"]";}cout<<"]}\n";}
int main(int argc,char**argv){try{
 if(argc<2)throw runtime_error("usage scan L W merged|per_shift prefix; points file");
 if(string(argv[1])=="points"){ifstream in(argv[2]);U n;while(in>>n)point_json(scan(n,1,true));return 0;}
 if(argc!=7)throw runtime_error("usage scan L W merged|per_shift prefix extra_label");
 U L=stoull(argv[2]),W=stoull(argv[3]);if(W>(U(1)<<18)||L+W>1000000262144ULL)throw runtime_error("bounded domain");auto z=scan(L,W,string(argv[4])=="merged");string p=argv[5];
 binary(p+"_R.bin",z.R);binary(p+"_active.bin",z.active);binary(p+"_bulk.bin",z.bulk);binary(p+"_A23.bin",z.A23);binary(p+"_zero.bin",z.zero);binary(p+"_minres.bin",z.minres);binary(p+"_bits.bin",z.bits);
 struct rusage ru;getrusage(RUSAGE_SELF,&ru);ofstream f(p+"_meta.json");f<<"{\"L\":"<<L<<",\"U\":"<<L+W<<",\"width\":"<<W<<",\"design\":\""<<argv[4]<<"\",\"complete\":true,\"wall_seconds\":"<<z.seconds<<",\"peak_rss_kib\":"<<ru.ru_maxrss<<",\"classified_residuals\":"<<z.classified<<",\"blocks\":"<<z.blocks<<",\"induced_segments\":"<<z.induced<<",\"union_segments\":"<<z.unions<<",\"words\":"<<z.words<<",\"shifts\":[";
 for(unsigned k=0;k<z.ss.size();++k){if(k)f<<",";auto h=z.ss[k];f<<"["<<h.s<<","<<h.c<<","<<h.d<<"]";}f<<"]}\n";cout<<"COMPLETE "<<p<<" "<<z.seconds<<"s RSS "<<ru.ru_maxrss<<"KiB\n";
 }catch(exception&e){cerr<<e.what()<<"\n";return 2;}}
