// Algorithm B: odd-only segmented sieve and two base-q digits; not q^2 multiplication.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <stdexcept>
struct Pair{uint64_t a,b;};
Pair product(Pair x,Pair y,uint64_t q){
 uint64_t t=x.a*y.a;
 uint64_t upper=t/q+x.a*y.b+x.b*y.a; // <=2q^2-3q <8e18 for q<=2e9
 return {t%q,upper%q};
}
uint64_t fermat(uint64_t q){
 Pair r{1,0},x{5%q,5/q}; uint64_t e=q-1;
 // Left-to-right exponentiation, unlike A.
 int bit=63;while(bit>0&&!(e&(uint64_t(1)<<bit)))--bit;
 for(;bit>=0;--bit){r=product(r,r,q);if((e>>bit)&1)r=product(r,x,q);}
 if(r.a!=1)throw std::runtime_error("Fermat residue/primality invariant failed");
 return r.a+q*r.b;
}
int main(int argc,char**argv){try{
 if(argc!=2)throw std::runtime_error("usage: scan_b upper");
 uint64_t limit=std::stoull(argv[1]);if(limit<3||limit>2000000000ULL)throw std::runtime_error("invalid upper");
 // Independently enumerate base primes by trial division, not A's sieve.
 std::vector<uint64_t> base;
 for(uint64_t v=3;v*v<=limit;v+=2){bool prime=true;for(auto d:base){if(d*d>v)break;if(v%d==0){prime=false;break;}}if(prime)base.push_back(v);}
 auto start=std::chrono::steady_clock::now();uint64_t total=0;
 const uint64_t STEP=10000000;
 for(uint64_t lower=0;lower<=limit;lower+=STEP){uint64_t upper=std::min(limit,lower+STEP-1),first=lower|1ULL;
  size_t n=upper>=first?(upper-first)/2+1:0;std::vector<uint8_t> composite(n,0);
  for(auto p:base){if(p*p>upper)break;uint64_t j=std::max(p*p,((first+p-1)/p)*p);if(!(j&1))j+=p;for(;j<=upper;j+=2*p)composite[(j-first)/2]=1;}
  uint64_t count=0,sum=0,digest=0;std::vector<uint64_t> hits;
  for(size_t i=0;i<n;++i){uint64_t q=first+2*i;if(q<3||q%4!=3||composite[i])continue;++count;sum+=q;uint64_t r=fermat(q);digest^=r+q*0x9e3779b97f4a7c15ULL;if(r==1)hits.push_back(q);}
  total+=count;
  std::cout<<"{\"lo\":"<<lower<<",\"hi\":"<<upper<<",\"count\":"<<count<<",\"sum\":"<<sum<<",\"digest\":"<<digest<<",\"hits\":[";
  for(size_t i=0;i<hits.size();++i){if(i)std::cout<<',';std::cout<<hits[i];}std::cout<<"]}"<<std::endl;
 }
 std::cerr<<"candidates="<<total<<" elapsed_seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
