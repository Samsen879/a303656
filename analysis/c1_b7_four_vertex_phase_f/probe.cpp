#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <string>
#include <sstream>
#include <vector>
using U=uint64_t; using W=__uint128_t;
U power(U a,U e,U m){U x=1;for(;e;e>>=1,a=(W)a*a%m)if(e&1)x=(W)x*a%m;return x;}
bool prime(U p){if(p<2)return false;if(!(p&1))return p==2;for(U d=3;d<=p/d;d+=2)if(p%d==0)return false;return true;}
bool presieve(U p){for(U l:{3,5,7,11,13,17,19,23,29,31,37,41,43,47})if(p!=l && p%l==0)return false;return true;}
void run(std::string shape,U r,U s,U B){
 U mandatory=(shape=="fork"?r*s:(shape=="relay"?r:s));
 U M=(shape=="relay"?42*r:42*r*s),tested=0;
 std::vector<U> factors={2,3,7,r};if(s)factors.push_back(s);
 for(U p=2*mandatory+1;p<=B;){
  ++tested;
  if(presieve(p)){
   U e=std::gcd(M,p-1);
   if(power(5,e,p)==1 && prime(p)){
    U n=e;for(U l:factors)while(n%l==0 && power(5,n/l,p)==1)n/=l;
    if(n%mandatory==0)std::cout<<shape<<","<<r<<","<<s<<","<<p<<","<<n<<"\n";
   }
  }
  if(B-p<4*mandatory)break;p+=4*mandatory;
 }
 std::cerr<<shape<<","<<r<<","<<s<<",progression_candidates,"<<tested<<"\n";
}
int main(int argc,char**argv){
 if(argc!=3){std::cerr<<"usage: probe relay|fork B\n";return 2;} U B=std::stoull(argv[2]);
 if(B>1000000000000ULL){std::cerr<<"B exceeds audited cap\n";return 2;}
 std::vector<U>A={43,127,379,7603,19531,519499};
 std::string mode=argv[1];
 if(mode=="relay")for(U r:A)run(mode,r,0,B);
 else if(mode=="fork")for(size_t i=0;i<A.size();i++)for(size_t j=i+1;j<A.size();j++)run(mode,A[i],A[j],B);
 else if(mode=="serial") {
 std::string line;
 while(std::getline(std::cin,line)){
  std::replace(line.begin(),line.end(),',',' ');std::istringstream in(line);
  std::string kind;U r,ignored,s,n;
  if(!(in>>kind>>r>>ignored>>s>>n) || kind!="relay")return 2;
  if(std::find(A.begin(),A.end(),r)==A.end() || s>10000000000ULL || s<=r || s%4!=3 || n==0 || (42*r)%n || n%r)return 2;
  run(mode,r,s,B);
 }
}
 else return 2;
}
