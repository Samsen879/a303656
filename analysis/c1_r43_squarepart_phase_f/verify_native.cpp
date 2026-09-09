// Independent GMP arithmetic/certificate checker. No probable-prime oracle.
// Reconstructs the cyclotomic integers from explicit quotient identities,
// not the Python generator's polynomial evaluation or Mobius loop.
#include <gmpxx.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <set>
#include <vector>
#include <stdexcept>
#include <string>
using Z=mpz_class;
void check(bool b,const std::string&s){if(!b)throw std::runtime_error(s);}
Z pw(const Z&a,unsigned long b){Z r;mpz_pow_ui(r.get_mpz_t(),a.get_mpz_t(),b);return r;}
Z pm(const Z&a,const Z&e,const Z&m){Z r;mpz_powm(r.get_mpz_t(),a.get_mpz_t(),e.get_mpz_t(),m.get_mpz_t());return r;}
Z gc(const Z&a,const Z&b){Z r;mpz_gcd(r.get_mpz_t(),a.get_mpz_t(),b.get_mpz_t());return r;}
Z readnum(const std::string&path){std::ifstream f(path);Z x;check(bool(f>>x),"read "+path);return x;}
Z reconstruct(int sign){Z top=1,bot=1;for(unsigned long e:{903UL,43UL,7UL,3UL})top*=pw(Z(5),e)+sign;for(unsigned long e:{301UL,129UL,21UL,1UL})bot*=pw(Z(5),e)+sign;check(top%bot==0,"quotient exact");return top/bot;}
int main(int argc,char**argv){try{
 std::string dir=argc>1?argv[1]:".";std::ifstream cert(dir+"/primality_certificates.tsv");check(bool(cert),"open cert");std::string line;std::set<Z>proven;
 while(std::getline(cert,line)){if(line.empty())continue;std::istringstream in(line);Z p,a;int k;check(bool(in>>p>>a>>k),"parse prime");
  if(p==2){check(a==0&&k==0,"base2");proven.insert(p);continue;}
  check(p>2&&p%2==1&&k>0&&!proven.count(p),"prime node");Z product=1;std::set<Z>seen;std::vector<Z>rs;
  for(int i=0;i<k;i++){Z r;unsigned long e;check(bool(in>>r>>e),"parse predecessor");check(e>0&&proven.count(r)&&!seen.count(r),"predecessor");seen.insert(r);product*=pw(r,e);rs.push_back(r);}
  check(product==p-1,"p-1 factorization");check(a>1&&a<p&&pm(a,p-1,p)==1,"prime Fermat");for(const Z&r:rs)check(gc(pm(a,(p-1)/r,p)-1,p)==1,"prime Lucas gcd");proven.insert(p);
 }
 std::cout<<"PRIME_CERTIFICATES PASS "<<proven.size()<<" nodes\n";
 Z N903=reconstruct(-1),N1806=reconstruct(1),C903=readnum(dir+"/C903.txt"),C1806=readnum(dir+"/C1806.txt"),R=readnum(dir+"/R1806_after_new_factor.txt");
 check(N903==readnum(dir+"/N903.txt")&&N1806==readnum(dir+"/N1806.txt"),"integer reconstruction");
 check(N903==Z("149930509")*Z("1562986310551")*C903,"903 factor product");check(N1806==43*Z("246201060546547")*C1806,"1806 factor product");check(C1806==Z("147304138944416276237689")*R,"fresh split");
 std::cout<<"INTEGER_RECONSTRUCTION_AND_PRODUCTS PASS\n";
 std::vector<std::pair<Z,unsigned long>> factors={{Z("149930509"),903},{Z("1562986310551"),903},{Z(43),42},{Z("246201060546547"),1806},{Z("147304138944416276237689"),1806}};
 for(auto&[p,w]:factors){check(proven.count(p),"unproved root");Z v=w==903?N903:N1806;check(v%p==0&&(v/p)%p!=0,"multiplicity one");check(pm(5,Z(w),p)==1,"order divides");for(unsigned long l:{2UL,3UL,7UL,43UL})if(w%l==0)check(pm(5,Z(w/l),p)!=1,"exact order");check(pm(5,Z(w),p*p)!=1,"regular factor");std::cout<<"FACTOR "<<p<<" PRIME_PROVED ORDER "<<w<<" MOD4 "<<p%4<<" MULTIPLICITY 1 LIFT_RESIDUE "<<pm(5,Z(w),p*p)<<"\n";}
 check(gc(N903,N1806)==1&&gc(C903,C1806)==1,"pair gcd");check(gc(C903,903)==1&&gc(C1806,1806)==1&&gc(R,1806)==1,"order exceptions");check(gc(R,Z("147304138944416276237689"))==1,"new factor disjoint");
 for(const auto&v:std::vector<Z>{C903,C1806,R}){check(v%1806==1,"progression");check(pm(2,v-1,v)!=1,"composite Fermat witness");check(mpz_perfect_square_p(v.get_mpz_t())==0,"non-square");std::cout<<"COMPOSITE_NONSQUARE PASS FERMAT2 "<<pm(2,v-1,v)<<"\n";}
 check(C903%4==3&&C1806%13==5&&R%13==5,"small modular nonsquare certificates");std::cout<<"ALL_NATIVE_CHECKS PASS\n";return 0;
 }catch(const std::exception&e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
