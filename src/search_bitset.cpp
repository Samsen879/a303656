#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

struct PS {int c,d; uint64_t s;};
static bool is_prime_trial(uint64_t n){if(n<2)return false;if(n%2==0)return n==2;for(uint64_t f=3;f<=n/f;f+=2)if(n%f==0)return false;return true;}
static std::vector<uint64_t> parse_primes(std::string raw){
    std::ifstream f(raw); if(f.good()){std::ostringstream q;q<<f.rdbuf();raw=q.str();}
    for(char&ch:raw)if(ch=='\n'||ch=='\r'||ch==' '||ch=='\t')ch=',';
    std::vector<uint64_t> v; std::stringstream ss(raw); std::string x;
    while(std::getline(ss,x,','))if(!x.empty())v.push_back(std::stoull(x));
    if(v.empty()) throw std::runtime_error("empty prime pool");
    std::set<uint64_t> z;
    for(auto p:v){if(!z.insert(p).second)throw std::runtime_error("duplicate prime");if(!is_prime_trial(p)||p%4!=3)throw std::runtime_error("invalid prime "+std::to_string(p));if(p>0xffffffffULL)throw std::runtime_error("prime too large");}
    return v;
}
static uint64_t pow_checked(uint64_t b,int e){__uint128_t x=1;for(int i=0;i<e;++i){x*=b;if(x>UINT64_MAX)throw std::runtime_error("power overflow");}return(uint64_t)x;}
static bool exact_one(uint64_t n,uint64_t s,uint64_t p){if(n<=s)return false;uint64_t r=n-s;if(r%p)return false;uint64_t p2=p*p;return r%p2!=0;}
static size_t popcount(const std::vector<uint64_t>&bits){size_t z=0;for(auto w:bits)z+=__builtin_popcountll(w);return z;}
int main(int argc,char**argv){
 try{
  uint64_t L=0,U=0,window=100000;int C=-1,D=-1;std::string ptext,json_path,candidates_path;bool quiet=false;
  for(int i=1;i<argc;++i){std::string a=argv[i];auto need=[&](const char*n){if(i+1>=argc)throw std::runtime_error(std::string("missing ")+n);return std::string(argv[++i]);};
   if(a=="--low")L=std::stoull(need("low"));else if(a=="--high")U=std::stoull(need("high"));else if(a=="--C")C=std::stoi(need("C"));else if(a=="--D")D=std::stoi(need("D"));
   else if(a=="--primes")ptext=need("primes");else if(a=="--window")window=std::stoull(need("window"));else if(a=="--json")json_path=need("json");else if(a=="--candidates")candidates_path=need("candidates");else if(a=="--quiet")quiet=true;else throw std::runtime_error("unknown arg "+a);}
  if(!L||!U||L>U||C<0||D<0||ptext.empty()||json_path.empty())throw std::runtime_error("required: --low --high --C --D --primes --json");
  uint64_t b3=pow_checked(3,C+1),b5=pow_checked(5,D+1);if(U>=b3+1)throw std::runtime_error("N_high finite C inequality fails");if(U>=b5+1)throw std::runtime_error("N_high finite D inequality fails");
  auto primes=parse_primes(ptext);std::vector<uint64_t> p3(C+1),p5(D+1);p3[0]=p5[0]=1;for(int i=1;i<=C;++i)p3[i]=p3[i-1]*3;for(int i=1;i<=D;++i)p5[i]=p5[i-1]*5;
  std::vector<PS> pairs;std::map<uint64_t,std::vector<std::pair<int,int>>> byshift;
  for(int c=0;c<=C;++c)for(int d=0;d<=D;++d){__uint128_t s=(__uint128_t)p3[c]+p5[d];if(s<=U){pairs.push_back({c,d,(uint64_t)s});byshift[(uint64_t)s].push_back({c,d});}}
  std::vector<uint64_t> shifts;for(auto const&kv:byshift)shifts.push_back(kv.first);
  std::ofstream cand;if(!candidates_path.empty()){cand.open(candidates_path);if(!cand)throw std::runtime_error("cannot open candidates");}
  uint64_t cur=L,total_tested=0,segments=0,windows=0;std::vector<uint64_t> found;size_t max_survivors=0;auto t0=std::chrono::steady_clock::now();
  while(cur<=U){
   auto it=std::upper_bound(shifts.begin(),shifts.end(),cur);uint64_t next=(it==shifts.end()?UINT64_MAX:*it);uint64_t end=U;
   if(window-1<U-cur) end=std::min(end,cur+window-1);
   if(next!=UINT64_MAX&&next>cur) end=std::min(end,next-1);
   size_t len=(size_t)(end-cur+1),words=(len+63)/64;std::vector<uint64_t> bits(words,~uint64_t(0));if(len%64)bits.back()=(uint64_t(1)<<(len%64))-1;
   size_t active=std::upper_bound(shifts.begin(),shifts.end(),cur)-shifts.begin();
   // Harder shifts first: deterministic order by a quick residue-diversity signature, then value.
   std::vector<uint64_t> order(shifts.begin(),shifts.begin()+active);
   std::stable_sort(order.begin(),order.end(),[&](uint64_t a,uint64_t b){
      size_t ca=0,cb=0;for(auto p:primes){ca+=(a%p);cb+=(b%p);}return ca==cb?a<b:ca<cb;});
   for(uint64_t s:order){
    std::vector<uint64_t> nextbits(words,0);for(size_t wi=0;wi<words;++wi){uint64_t w=bits[wi];while(w){unsigned bit=__builtin_ctzll(w);size_t idx=wi*64+bit;if(idx<len){uint64_t n=cur+idx;bool ok=false;for(uint64_t p:primes)if(exact_one(n,s,p)){ok=true;break;}if(ok)nextbits[wi]|=uint64_t(1)<<bit;}w&=w-1;}}
    bits.swap(nextbits);if(popcount(bits)==0)break;
   }
   size_t survivors=popcount(bits);max_survivors=std::max(max_survivors,survivors);
   if(!quiet)std::cout<<"WINDOW low="<<cur<<" high="<<end<<" active_distinct_shifts="<<active<<" survivors="<<survivors<<"\n";
   for(size_t wi=0;wi<words;++wi){uint64_t w=bits[wi];while(w){unsigned bit=__builtin_ctzll(w);size_t idx=wi*64+bit;if(idx<len){uint64_t n=cur+idx;found.push_back(n);if(cand)cand<<n<<"\n";}w&=w-1;}}
   total_tested+=len;++windows;if(next!=UINT64_MAX&&end==next-1)++segments;
   if(end==UINT64_MAX) break;
   cur=end+1;
  }
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
  std::ofstream js(json_path);if(!js)throw std::runtime_error("cannot open json");
  js<<"{\n  \"method\": \"C_exact_segmented_candidate_filter\",\n  \"low\": \""<<L<<"\",\n  \"high\": \""<<U<<"\",\n  \"C\": "<<C<<",\n  \"D\": "<<D<<",\n  \"prime_count\": "<<primes.size()<<",\n  \"primes\": [";for(size_t i=0;i<primes.size();++i){if(i)js<<",";js<<primes[i];}js<<"],\n";
  js<<"  \"rectangle_pair_count_relevant_to_high\": "<<pairs.size()<<",\n  \"distinct_shift_count_relevant_to_high\": "<<shifts.size()<<",\n  \"integers_tested\": "<<total_tested<<",\n  \"windows\": "<<windows<<",\n  \"activation_boundaries_crossed\": "<<segments<<",\n  \"candidate_count\": "<<found.size()<<",\n  \"candidates\": [";for(size_t i=0;i<found.size();++i){if(i)js<<",";js<<"\""<<found[i]<<"\"";}js<<"],\n";
  js<<"  \"elapsed_seconds\": "<<sec<<",\n  \"classification\": \""<<(found.empty()?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL":"CANDIDATES REQUIRE INDEPENDENT VERIFIER")<<"\"\n}\n";
  std::cout<<"integers_tested="<<total_tested<<"\n"<<"candidate_count="<<found.size()<<"\n"<<"elapsed_seconds="<<sec<<"\n"<<(found.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";
  return found.empty()?1:0;
 }catch(std::exception const&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
