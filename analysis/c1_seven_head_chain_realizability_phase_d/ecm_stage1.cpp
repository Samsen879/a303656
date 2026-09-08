// Bounded stage-1 ECM factor discovery only. No negative/exhaustive claims.
// Montgomery x:z arithmetic with Suyama parametrization. Every output factor
// is checked by exact division and a separate primality/order verifier.
#include <gmpxx.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <stdexcept>
struct P {mpz_class x,z;};
mpz_class N,A24;
mpz_class mod(const mpz_class&a){mpz_class r;mpz_mod(r.get_mpz_t(),a.get_mpz_t(),N.get_mpz_t());return r;}
mpz_class gcd(const mpz_class&a){mpz_class g;mpz_gcd(g.get_mpz_t(),a.get_mpz_t(),N.get_mpz_t());return g;}
P dbl(const P&p){mpz_class aa=mod((p.x+p.z)*(p.x+p.z)),bb=mod((p.x-p.z)*(p.x-p.z)),c=mod(aa-bb);return {mod(aa*bb),mod(c*(bb+A24*c))};}
P add(const P&p,const P&q,const P&dif){mpz_class da=mod((q.x-q.z)*(p.x+p.z)),cb=mod((q.x+q.z)*(p.x-p.z));return {mod(dif.z*(da+cb)*(da+cb)),mod(dif.x*(da-cb)*(da-cb))};}
P mul(P p,unsigned long k){if(k==1)return p;P r0=p,r1=dbl(p);int b=63;while(b>0&&!(k&(1UL<<b)))--b;for(--b;b>=0;--b){if((k>>b)&1){r0=add(r0,r1,p);r1=dbl(r1);}else{r1=add(r0,r1,p);r0=dbl(r0);}}return r0;}
int main(int argc,char**argv){try{
 if(argc!=4)throw std::runtime_error("usage: ecm_stage1 decimal_input B1 curves");
 std::ifstream f(argv[1]);f>>N;if(!f||N<3)throw std::runtime_error("bad input");
 unsigned long B1=std::stoul(argv[2]),curves=std::stoul(argv[3]);
 if(B1<2||B1>1000000||curves>10000)throw std::runtime_error("out of discovery gate");
 std::vector<unsigned long> primes;for(unsigned long p=2;p<=B1;++p){bool yes=true;for(auto v:primes){if(v*v>p)break;if(p%v==0){yes=false;break;}}if(yes)primes.push_back(p);}
 auto start=std::chrono::steady_clock::now();
 for(unsigned long c=0;c<curves;++c){mpz_class s=6+c,u=mod(s*s-5),v=mod(4*s),u3=mod(u*u*u),v3=mod(v*v*v),den=mod(16*u3*v),inv,g;
  g=gcd(den);if(g>1&&g<N){std::cout<<g<<"\n";return 0;}if(g==N)continue;
  if(!mpz_invert(inv.get_mpz_t(),den.get_mpz_t(),N.get_mpz_t()))throw std::runtime_error("invert invariant");
  A24=mod((v-u)*(v-u)*(v-u)*(3*u+v)*inv);P p{u3,v3};bool unusable=false;
  unsigned ctr=0;for(auto ell:primes){unsigned long e=ell;while(e<=B1/ell)e*=ell;p=mul(p,e);
   if(++ctr%16==0){g=gcd(p.z);if(g>1&&g<N){std::cout<<g<<"\n";std::cerr<<"sigma="<<s<<" B1="<<B1<<" elapsed="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";return 0;}if(g==N){unusable=true;break;}}}
  if(!unusable){g=gcd(p.z);if(g>1&&g<N){std::cout<<g<<"\n";return 0;}}
  std::cerr<<"curve="<<c+1<<" sigma="<<s<<" B1="<<B1<<" elapsed="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"\n";
 }
 std::cout<<"NO_FACTOR_FOUND_NOT_EXHAUSTIVE\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
