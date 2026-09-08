// Independent replay: only admitted divisors q=2*n*k+1 with odd k.
// GMP modular exponentiation, arbitrary-size candidate q; no A arithmetic reused.
#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <chrono>
#include <stdexcept>
int main(int argc,char**argv){try{
 if(argc!=3)throw std::runtime_error("usage: target_divisors_gmp prime_exponent k_max");
 mpz_class n(argv[1]),Kz(argv[2]);
 if(n<3 || Kz<1 || !Kz.fits_ulong_p())throw std::runtime_error("invalid bounds");
 unsigned long K=Kz.get_ui();
 std::vector<unsigned long> small;
 for(unsigned long v=3;v<=97;v+=2){bool ok=true; for(auto p:small)if(v%p==0){ok=false;break;}if(ok&&v!=5)small.push_back(v);}
 mpz_class q=2*n+1,step=4*n,r,base=5;
 unsigned long tests=0,hits=0;auto start=std::chrono::steady_clock::now();
 std::cout<<"n,k,q\n";
 for(unsigned long k=1;k<=K;k+=2,q+=step){
  auto m5=mpz_fdiv_ui(q.get_mpz_t(),5);if(m5!=1&&m5!=4)continue;
  bool composite=false;for(auto p:small)if(q!=p&&mpz_divisible_ui_p(q.get_mpz_t(),p)){composite=true;break;}if(composite)continue;
  ++tests;mpz_powm(r.get_mpz_t(),base.get_mpz_t(),n.get_mpz_t(),q.get_mpz_t());
  if(r==1){++hits;std::cout<<n<<","<<k<<","<<q<<"\n";}
  if(k>K-2)break;
 }
 std::cerr<<"{\"n\":\""<<n<<"\",\"K\":"<<K<<",\"modular_tests\":"<<tests<<",\"admitted_divisor_hits\":"<<hits<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
