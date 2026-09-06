// Algorithm A: all-integer segmented sieve; direct modular arithmetic modulo q^2.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <vector>
#include <chrono>
#include <stdexcept>
using u64=uint64_t; using u128=__uint128_t;
u64 power(u64 a,u64 e,u64 m){u64 r=1;while(e){if(e&1)r=u128(r)*a%m;e>>=1;if(e)a=u128(a)*a%m;}return r;}
int main(int argc,char**argv){try{
 if(argc<2)throw std::runtime_error("usage: scan_a upper [all]");
 u64 limit=std::stoull(argv[1]); bool all=argc>2;
 if(limit<3||limit>2000000000ULL)throw std::runtime_error("upper must be in [3,2e9]");
 u64 root=0;while((root+1)*(root+1)<=limit)++root;
 std::vector<bool> small(root+1,true);small[0]=small[1]=false;
 std::vector<u64> ps;for(u64 p=2;p<=root;++p)if(small[p]){ps.push_back(p);for(u64 j=p*p;j<=root;j+=p)small[j]=false;}
 const u64 STEP=10000000; auto start=std::chrono::steady_clock::now();
 u64 total=0;
 for(u64 lo=0;lo<=limit;lo+=STEP){u64 hi=std::min(limit,lo+STEP-1);
  std::vector<uint8_t> good(hi-lo+1,1);
  for(u64 p:ps){if(p*p>hi)break;u64 b=std::max(p*p,((lo+p-1)/p)*p);for(u64 j=b;j<=hi;j+=p)good[j-lo]=0;}
  if(lo==0){good[0]=good[1]=0;}
  u64 count=0,sum=0,digest=0;std::vector<u64> hits;
  for(u64 q=std::max(u64(3),lo);q<=hi;++q)if(good[q-lo]&&(all||q%4==3)&&q!=5){++count;sum+=q;u64 r=power(5,q-1,q*q);digest^=r+q*0x9e3779b97f4a7c15ULL;if(r==1)hits.push_back(q);}
  total+=count;
  std::cout<<"{\"lo\":"<<lo<<",\"hi\":"<<hi<<",\"count\":"<<count<<",\"sum\":"<<sum<<",\"digest\":"<<digest<<",\"hits\":[";
  for(size_t i=0;i<hits.size();++i){if(i)std::cout<<',';std::cout<<hits[i];}
  std::cout<<"]}"<<std::endl;
 }
 std::cerr<<"candidates="<<total<<" elapsed_seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
