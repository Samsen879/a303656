#include <gmpxx.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <chrono>
#include <string>
using Z=mpz_class;Z N;
Z mod(const Z&a){Z b;mpz_mod(b.get_mpz_t(),a.get_mpz_t(),N.get_mpz_t());return b;}
Z gcd(const Z&a){Z b;mpz_gcd(b.get_mpz_t(),a.get_mpz_t(),N.get_mpz_t());return b;}
std::vector<int> primes(int b){std::vector<bool>s(b+1,true);std::vector<int>ps;for(int p=2;p<=b;++p)if(s[p]){ps.push_back(p);if(1LL*p*p<=b)for(int j=p*p;j<=b;j+=p)s[j]=false;}return ps;}
Z lucas(const Z&P,const Z&k){Z a=2,b=P;for(long j=mpz_sizeinbase(k.get_mpz_t(),2)-1;j>=0;--j){Z ab=mod(a*b-P);if(mpz_tstbit(k.get_mpz_t(),j)){b=mod(b*b-2);a=ab;}else{a=mod(a*a-2);b=ab;}}return a;}
int main(int argc,char**argv){if(argc<5)return 2;std::ifstream f(argv[1]);f>>N;std::string mode=argv[2];int B=std::stoi(argv[3]);unsigned long seed=std::stoul(argv[4]);int B2=argc>5?std::stoi(argv[5]):B;auto t=std::chrono::steady_clock::now();Z g=1;
 if(mode=="rho"){
  Z y=seed+2,c=seed,q=1,x,ys;unsigned long r=1,used=0;
  while(g==1&&used<(unsigned long)B){x=y;for(unsigned long i=0;i<r&&used<(unsigned long)B;++i){y=mod(y*y+c);++used;}unsigned long k=0;
   while(k<r&&g==1&&used<(unsigned long)B){ys=y;unsigned long stop=std::min(128UL,r-k);q=1;for(unsigned long i=0;i<stop;++i){y=mod(y*y+c);q=mod(q*(x-y));++used;}g=gcd(q);k+=stop;}r*=2;}
  if(g==N){for(int i=0;i<128;++i){ys=mod(ys*ys+c);g=gcd(x-ys);if(g>1)break;}}
  std::cout<<"RHO seed "<<seed<<" max_evaluations "<<B<<" actual_evaluations "<<used<<" gcd "<<g<<"\n";
 }else{
  auto ps=primes(B2);Z M=1;for(int p:ps){if(p>B)break;unsigned long pe=p;while(pe<=B/p)pe*=p;M*=pe;}
  if(mode=="pm1"){
   Z a=seed;mpz_powm(a.get_mpz_t(),a.get_mpz_t(),M.get_mpz_t(),N.get_mpz_t());g=gcd(a-1);
   std::cout<<"PM1 base "<<seed<<" B1 "<<B<<" stage1_gcd "<<g<<"\n";
   if(g==1&&B2>B){int last=0;Z aq=1,prod=1;std::vector<Z>powers(1000);std::vector<bool>ready(1000,false);
    for(int p:ps)if(p>B){int gap=p-last;Z term;if(gap<1000&&ready[gap])term=powers[gap];else{mpz_powm_ui(term.get_mpz_t(),a.get_mpz_t(),gap,N.get_mpz_t());if(gap<1000){powers[gap]=term;ready[gap]=true;}}aq=mod(aq*term);last=p;prod=mod(prod*(aq-1));}g=gcd(prod);std::cout<<"B2 "<<B2<<" stage2_gcd "<<g<<"\n";}
  }else if(mode=="pp1"){
   Z v=lucas(Z(seed),M);g=gcd(v-2);std::cout<<"PP1 seed "<<seed<<" B1 "<<B<<" B2 NOT_RUN gcd "<<g<<"\n";
  }else return 2;
 }
 if(g>1&&g<N)std::cout<<"FACTOR "<<g<<"\n";
 std::cout<<"SECONDS "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";
}
