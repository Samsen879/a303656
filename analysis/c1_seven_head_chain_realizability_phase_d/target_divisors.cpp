// Read-only targeted trial division of Phi_n(5), for a fixed prime n.
// Does not enumerate nonregular primes independently of an order target.
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <chrono>
using u64=uint64_t; using u128=__uint128_t;
u64 modpow(u64 a,u64 e,u64 m){u64 r=1;while(e){if(e&1)r=(u128)r*a%m;a=(u128)a*a%m;e>>=1;}return r;}
int main(int argc,char**argv){
 if(argc!=3)return 2;
 u64 n=std::strtoull(argv[1],0,10), K=std::strtoull(argv[2],0,10);
 if(!n||!K||(u128)2*n*K+1>UINT64_MAX)return 3;
 const unsigned wheel[]={3,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97};
 auto t=std::chrono::steady_clock::now();u64 tested=0,hits=0;
 std::cout<<"n,k,q\n";
 for(u64 k=1;k<=K;++k){u64 q=2*n*k+1;
   if(q%5!=1&&q%5!=4)continue;
   bool skip=false;for(auto z:wheel){if(q!=z&&q%z==0){skip=true;break;}}if(skip)continue;
   ++tested;
   if(modpow(5,n,q)==1){++hits;std::cout<<n<<","<<k<<","<<q<<"\n";}
 }
 std::cerr<<"{\"n\":"<<n<<",\"K\":"<<K<<",\"modular_tests\":"<<tested<<",\"divisor_hits\":"<<hits<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"}\n";
}
