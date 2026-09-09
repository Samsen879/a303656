#include <gmpxx.h>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
using U=unsigned long;
std::vector<U> factors(U n){std::vector<U>v;for(U p=2;p<=n/p;p++)if(n%p==0){v.push_back(p);while(n%p==0)n/=p;}if(n>1)v.push_back(n);return v;}
mpz_class phi5(U n){auto fs=factors(n);mpz_class a=1,b=1,t;for(U mask=0;mask<(1UL<<fs.size());mask++){U d=n,k=0;for(U j=0;j<fs.size();j++)if(mask&(1UL<<j)){d/=fs[j];k++;}mpz_ui_pow_ui(t.get_mpz_t(),5,d);t-=1;if(k%2)b*=t;else a*=t;}if(!mpz_divisible_p(a.get_mpz_t(),b.get_mpz_t()))throw std::runtime_error("nonintegral phi");return a/b;}
int main(){
 const U B=10000;std::vector<bool>is(B+1,true);std::vector<U>pe;
 for(U p=2;p<=B;p++)if(is[p]){for(U j=p*p;j<=B;j+=p)is[j]=false;U e=p;while(e<=B/p)e*=p;pe.push_back(e);}
 for(U n:{2287,4574,5461,6861,10922,16383}){
  mpz_class N=phi5(n),z,g;
  std::cout<<"INDEX "<<n<<" B1 "<<B<<"\n";
  // Small-prime trial removal is deliberately finite; no squarefree assertion.
  for(U p=2;p<=10000;p++)if(is[p]){
   unsigned e=0;while(mpz_divisible_ui_p(N.get_mpz_t(),p)){N/=p;e++;}
   if(e)std::cout<<"TRIAL "<<p<<" "<<e<<"\n";
  }
  for(U base:{2,3}){
   z=base;
   for(U e:pe)mpz_powm_ui(z.get_mpz_t(),z.get_mpz_t(),e,N.get_mpz_t());
   z-=1;mpz_gcd(g.get_mpz_t(),z.get_mpz_t(),N.get_mpz_t());
   if(g>1 && g<N){std::cout<<"P1 "<<base<<" "<<g<<"\n";N/=g;}
   else std::cout<<"P1 "<<base<<" "<<(g==1?"NO_FACTOR":"GCD_EQUALS_RESIDUAL")<<"\n";
  }
  std::cout<<"RESIDUAL_BITS "<<mpz_sizeinbase(N.get_mpz_t(),2)<<"\n";
 }
}
