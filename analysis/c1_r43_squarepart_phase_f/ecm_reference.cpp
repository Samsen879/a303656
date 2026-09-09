// Reference two-stage ECM with Suyama parametrisation.
// Stage-two layout is a port of SymPy ntheory.ecm, not GMP-ECM.
// All reported factors require independent exact verification.
#include <gmpxx.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <set>
#include <cmath>
#include <chrono>
#include <stdexcept>
using Z=mpz_class;
Z N,A;
Z mod(const Z&x){Z y;mpz_mod(y.get_mpz_t(),x.get_mpz_t(),N.get_mpz_t());return y;}
Z gcd(const Z&x){Z g;mpz_gcd(g.get_mpz_t(),x.get_mpz_t(),N.get_mpz_t());return g;}
struct P{Z x,z;};
P dbl(const P&p){Z u=mod((p.x+p.z)*(p.x+p.z)),v=mod((p.x-p.z)*(p.x-p.z)),d=u-v;return {mod(u*v),mod(d*(v+A*d))};}
P add(const P&p,const P&q,const P&diff){Z u=mod((p.x-p.z)*(q.x+q.z)),v=mod((p.x+p.z)*(q.x-q.z)),a=u+v,b=u-v;return {mod(diff.z*a*a),mod(diff.x*b*b)};}
P mul(const P&p,const Z&k){P q=p,r=dbl(p);for(long j=mpz_sizeinbase(k.get_mpz_t(),2)-2;j>=0;--j){if(mpz_tstbit(k.get_mpz_t(),j)){q=add(r,q,p);r=dbl(r);}else{r=add(q,r,p);q=dbl(q);}}return q;}
std::vector<int> primes(int b){std::vector<bool>s(b+1,true);std::vector<int>p;for(int i=2;i<=b;++i)if(s[i]){p.push_back(i);if(1LL*i*i<=b)for(int j=i*i;j<=b;j+=i)s[j]=false;}return p;}
int main(int argc,char**argv){try{
 if(argc!=6)throw std::runtime_error("usage: input B1 B2 curves sigma_start");
 std::ifstream f(argv[1]);if(!(f>>N)||N<9)throw std::runtime_error("bad input");
 int b1=std::stoi(argv[2]),b2=std::stoi(argv[3]),curves=std::stoi(argv[4]);unsigned long ss=std::stoul(argv[5]);
 if(b1<10||b1%2||b2<=b1||b2%2)throw std::runtime_error("bad bounds");
 int D=std::min((int)std::sqrt(b2),b1/2-1);auto ps=primes(b2+4*D);Z k=1;for(int p:ps){if(p>b1)break;unsigned long pe=p;while(pe<=b1/p)pe*=p;k*=pe;}
 std::vector<std::vector<int>> ds;size_t pi=0;for(int r=b1+2*D;r<b2+2*D;r+=4*D){std::set<int>d;while(pi<ps.size()&&ps[pi]<r-2*D)++pi;for(size_t j=pi;j<ps.size()&&ps[j]<r+2*D;++j)d.insert(std::abs(ps[j]-r)>>1);ds.emplace_back(d.begin(),d.end());}
 std::cout<<"ECM_REFERENCE B1 "<<b1<<" B2 "<<b2<<" D "<<D<<" curves "<<curves<<" sigma_start "<<ss<<"\n";
 auto start=std::chrono::steady_clock::now();
 for(int c=0;c<curves;++c){auto t=std::chrono::steady_clock::now();unsigned long sig=ss+c;Z sigma=sig,u=mod(sigma*sigma-5),v=4*sigma,u3=mod(u*u*u),den=mod(16*u3*v),iv;
 if(!mpz_invert(iv.get_mpz_t(),den.get_mpz_t(),N.get_mpz_t())){Z g=gcd(den);std::cout<<"CURVE "<<c<<" SIGMA "<<sig<<" SETUP_GCD "<<g<<std::endl;if(g>1&&g<N){std::cout<<"FACTOR "<<g<<std::endl;return 0;}continue;}
 A=mod((v-u)*(v-u)*(v-u)*(3*u+v)*iv);P q={u3,mod(v*v*v)};q=mul(q,k);Z g=gcd(q.z);
 if(g>1&&g<N){std::cout<<"CURVE "<<c<<" SIGMA "<<sig<<" STAGE 1 FACTOR "<<g<<std::endl;return 0;}
 if(g==N){std::cout<<"CURVE "<<c<<" SIGMA "<<sig<<" DEGENERATE_STAGE1\n";continue;}
 std::vector<P>S(D);std::vector<Z>beta(D);S[0]=q;P q2=dbl(q);S[1]=add(q2,q,q);beta[0]=mod(S[0].x*S[0].z);beta[1]=mod(S[1].x*S[1].z);
 for(int d=2;d<D;++d){S[d]=add(S[d-1],q2,S[d-2]);beta[d]=mod(S[d].x*S[d].z);}
 P w=mul(q,Z(4*D)),tpt=mul(q,Z(b1-2*D)),r=mul(q,Z(b1+2*D));Z prod=1;bool all=false;
 for(const auto&deltas:ds){Z alpha=mod(r.x*r.z);for(int d:deltas){Z h=(r.x-S[d].x)*(r.z+S[d].z)-alpha+beta[d];prod=mod(prod*h);}P next=add(r,w,tpt);tpt=r;r=next;}
 g=gcd(prod);double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count();
 std::cout<<"CURVE "<<c<<" SIGMA "<<sig<<" STAGE2_GCD "<<g<<" SECONDS "<<sec<<std::endl;
 if(g>1&&g<N){std::cout<<"FACTOR "<<g<<std::endl;return 0;}
 }
 std::cout<<"NO_FACTOR COMPLETE "<<curves<<" SECONDS "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<std::endl;
}catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 2;}}
