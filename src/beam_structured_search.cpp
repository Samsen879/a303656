// Heuristic CRT beam search for high-coverage bounded A303656 candidates.
// Every final candidate is checked by exact full factorization; beam pruning is
// heuristic and therefore absence of a candidate is not an UNSAT result.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {
constexpr size_t WORDS=7; // enough for <=448 distinct shifts
struct Bits{
 std::array<uint64_t,WORDS>w{};
 void add(size_t i){w[i>>6]|=uint64_t(1)<<(i&63);}
 Bits operator|(Bits const&o)const{Bits z;for(size_t i=0;i<WORDS;++i)z.w[i]=w[i]|o.w[i];return z;}
 int count()const{int z=0;for(auto x:w)z+=__builtin_popcountll(x);return z;}
 bool has(size_t i)const{return(w[i>>6]>>(i&63))&1;}
};
struct State{uint64_t r,M;Bits cov;int score;};
struct MinState{bool operator()(State const&a,State const&b)const{return a.score>b.score||(a.score==b.score&&a.r>b.r);}};
struct NScore{uint64_t n;int score;Bits cov;};
struct MinN{bool operator()(NScore const&a,NScore const&b)const{return a.score>b.score||(a.score==b.score&&a.n>b.n);}};

bool prime_trial(uint64_t n){if(n<2)return false;if(n%2==0)return n==2;for(uint64_t q=3;q<=n/q;q+=2)if(n%q==0)return false;return true;}
std::vector<uint64_t> read_primes(std::string raw){std::ifstream f(raw);if(f){std::ostringstream s;s<<f.rdbuf();raw=s.str();}for(char&c:raw)if(c=='\n'||c=='\r'||c==' '||c=='\t')c=',';std::stringstream ss(raw);std::string x;std::vector<uint64_t>P;std::set<uint64_t>seen;while(std::getline(ss,x,','))if(!x.empty()){uint64_t p=std::stoull(x);if(!seen.insert(p).second||!prime_trial(p)||p%4!=3)throw std::runtime_error("bad prime pool");P.push_back(p);}if(P.empty())throw std::runtime_error("empty pool");return P;}
uint64_t ipow(uint64_t b,int e){__uint128_t x=1;for(int i=0;i<e;++i){x*=b;if(x>UINT64_MAX)throw std::runtime_error("overflow");}return(uint64_t)x;}
uint64_t isqrt(uint64_t n){uint64_t l=0,h=std::min<uint64_t>(n,uint64_t(1)<<32);while(l<h){uint64_t m=l+(h-l+1)/2;if(m<=n/m)l=m;else h=m-1;}return l;}
std::vector<uint32_t> sieve_primes(uint64_t lim){std::vector<uint8_t>a(lim+1,1);a[0]=a[1]=0;for(uint64_t p=2;p<=lim/p;++p)if(a[p])for(uint64_t m=p*p;m<=lim;m+=p)a[m]=0;std::vector<uint32_t>v;for(uint64_t p=2;p<=lim;++p)if(a[p])v.push_back((uint32_t)p);return v;}
uint64_t egcd_inv(uint64_t a,uint64_t m){ // m is small, a and m coprime
 int64_t t=0,nt=1;int64_t r=(int64_t)m,nr=(int64_t)(a%m);while(nr){int64_t q=r/nr;int64_t z=t-q*nt;t=nt;nt=z;z=r-q*nr;r=nr;nr=z;}if(r!=1)throw std::runtime_error("noncoprime CRT");if(t<0)t+=(int64_t)m;return(uint64_t)t;}
State extend(State const&s,uint64_t p,uint64_t t,Bits const&pcov){uint64_t m=p*p;uint64_t inv=egcd_inv(s.M%m,m);uint64_t delta=(t+m-(s.r%m))%m;uint64_t k=(uint64_t)((__uint128_t)delta*inv%m);__uint128_t rr=(__uint128_t)s.r+(__uint128_t)s.M*k;__uint128_t MM=(__uint128_t)s.M*m;if(MM>UINT64_MAX||rr>UINT64_MAX)throw std::runtime_error("CRT overflow");Bits c=s.cov|pcov;return{(uint64_t)rr,(uint64_t)MM,c,c.count()};}
std::vector<Bits> covers_for(uint64_t p,std::vector<uint64_t>const&sh){uint64_t m=p*p;std::vector<Bits>o(m);for(uint64_t t=0;t<m;++t)for(size_t i=0;i<sh.size();++i)if(t%p==sh[i]%p&&t!=sh[i]%m)o[t].add(i);return o;}

template<class Heap,class Item,class Cmp>void keep(Heap&h,Item const&x,size_t K,Cmp){if(h.size()<K)h.push(x);else{auto const&z=h.top();bool better=x.score>z.score||(x.score==z.score&&x.r<z.r);if(better){h.pop();h.push(x);}}}

bool exact1(uint64_t r,std::vector<uint32_t>const&P,uint64_t&ob){if(!r)return false;uint64_t x=r;for(uint32_t qq:P){uint64_t p=qq;if(p>x/p)break;if(x%p)continue;int e=0;do{x/=p;++e;}while(x%p==0);if(p%4==3&&e==1){ob=p;return true;}}if(x>1&&x%4==3){ob=x;return true;}return false;}
struct Entry{uint16_t idx;uint64_t modp2;};
struct PData{uint64_t p,p2;std::vector<std::vector<Entry>>bucket;};
Bits pool_cover(uint64_t n,std::vector<PData>const&pd,std::vector<uint64_t>const&sh){Bits z;for(auto const&q:pd){uint64_t r=n%q.p,r2=n%q.p2;for(auto const&e:q.bucket[(size_t)r])if(sh[e.idx]<=n&&e.modp2!=r2)z.add(e.idx);}return z;}

struct Args{uint64_t L=0,U=0;int C=-1,D=-1;size_t beam=20000,top=5000,exact=1000;std::string primes,json;};
Args parse(int ac,char**av){Args a;for(int i=1;i<ac;++i){std::string k=av[i];auto v=[&](){if(++i>=ac)throw std::runtime_error("missing arg");return std::string(av[i]);};if(k=="--low")a.L=std::stoull(v());else if(k=="--high")a.U=std::stoull(v());else if(k=="--C")a.C=std::stoi(v());else if(k=="--D")a.D=std::stoi(v());else if(k=="--primes")a.primes=v();else if(k=="--beam")a.beam=std::stoull(v());else if(k=="--top-n")a.top=std::stoull(v());else if(k=="--exact-check")a.exact=std::stoull(v());else if(k=="--json")a.json=v();else throw std::runtime_error("unknown arg");}if(!a.L||!a.U||a.L>a.U||a.C<0||a.D<0||a.primes.empty()||a.json.empty())throw std::runtime_error("bad args");return a;}
}

int main(int ac,char**av){try{auto a=parse(ac,av);if(a.U>=ipow(3,a.C+1)+1||a.U>=ipow(5,a.D+1)+1)throw std::runtime_error("domain bounds fail");
 std::vector<uint64_t>x(a.C+1),y(a.D+1);x[0]=y[0]=1;for(int i=1;i<=a.C;++i)x[i]=x[i-1]*3;for(int j=1;j<=a.D;++j)y[j]=y[j-1]*5;std::set<uint64_t>S;for(auto q:x)for(auto r:y)if((__uint128_t)q+r<=a.U)S.insert(q+r);std::vector<uint64_t>sh(S.begin(),S.end());if(sh.size()>WORDS*64)throw std::runtime_error("too many shifts for fixed bitset");
 auto pool=read_primes(a.primes);std::vector<uint64_t>base={3,7,11,19,23};for(auto p:base)if(std::find(pool.begin(),pool.end(),p)==pool.end())throw std::runtime_error("pool lacks base prime");
 auto start=std::chrono::steady_clock::now();std::vector<State>states={{0,1,Bits{},0}};
 for(size_t bi=0;bi<base.size();++bi){uint64_t p=base[bi];auto cv=covers_for(p,sh);size_t K=(bi<3?std::numeric_limits<size_t>::max():a.beam);std::priority_queue<State,std::vector<State>,MinState>heap;std::vector<State>all;if(K==std::numeric_limits<size_t>::max())all.reserve(states.size()*cv.size());
  for(auto const&s:states)for(uint64_t t=0;t<cv.size();++t){State z=extend(s,p,t,cv[t]);if(K==std::numeric_limits<size_t>::max())all.push_back(z);else if(heap.size()<K)heap.push(z);else{auto const&w=heap.top();if(z.score>w.score||(z.score==w.score&&z.r<w.r)){heap.pop();heap.push(z);}}}
  if(K==std::numeric_limits<size_t>::max())states.swap(all);else{states.clear();states.reserve(heap.size());while(!heap.empty()){states.push_back(heap.top());heap.pop();}std::sort(states.begin(),states.end(),[](auto const&u,auto const&v){return u.score>v.score||(u.score==v.score&&u.r<v.r);});}
  std::cout<<"BEAM prime="<<p<<" states="<<states.size()<<" best="<<states.front().score<<" modulus="<<states.front().M<<"\n";
 }
 uint64_t M=states.front().M;std::vector<PData>pd;pd.reserve(pool.size());for(uint64_t p:pool){PData q{p,p*p,std::vector<std::vector<Entry>>(p)};for(size_t i=0;i<sh.size();++i)q.bucket[sh[i]%p].push_back({(uint16_t)i,sh[i]%(p*p)});pd.push_back(std::move(q));}
 std::priority_queue<NScore,std::vector<NScore>,MinN>nh;std::unordered_set<uint64_t>seen;uint64_t actual=0;
 for(auto const&s:states){uint64_t n=a.L+((s.r+a.L%M<=s.r?0:M) - a.L%M)%M; // overwritten robustly below
  uint64_t rem=a.L%M;uint64_t delta=(s.r+M-rem)%M;n=a.L+delta;
  for(;n<=a.U;){if(seen.insert(n).second){++actual;Bits c=pool_cover(n,pd,sh);NScore z{n,c.count(),c};if(nh.size()<a.top)nh.push(z);else{auto const&w=nh.top();if(z.score>w.score||(z.score==w.score&&z.n<w.n)){nh.pop();nh.push(z);}}}if(a.U-n<M)break;n+=M;}
 }
 std::vector<NScore>tops;while(!nh.empty()){tops.push_back(nh.top());nh.pop();}std::sort(tops.begin(),tops.end(),[](auto const&u,auto const&v){return u.score>v.score||(u.score==v.score&&u.n<v.n);});
 auto fp=sieve_primes(isqrt(a.U-2));size_t checks=std::min(a.exact,tops.size());struct Exact{uint64_t n;int poolscore,passed;uint64_t failshift,failrem;};std::vector<Exact>ex;uint64_t candidate=0;
 for(size_t k=0;k<checks;++k){auto const&z=tops[k];int passed=0;uint64_t fs=0,fr=0;bool all=true;for(size_t i=0;i<sh.size()&&sh[i]<=z.n;++i){if(z.cov.has(i)){++passed;continue;}uint64_t ob=0;if(!exact1(z.n-sh[i],fp,ob)){all=false;fs=sh[i];fr=z.n-sh[i];break;}++passed;}ex.push_back({z.n,z.score,passed,fs,fr});if(all){candidate=z.n;break;}}
 std::sort(ex.begin(),ex.end(),[](auto const&u,auto const&v){return u.passed>v.passed||(u.passed==v.passed&&u.n<v.n);});double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::ofstream js(a.json);js<<"{\n \"method\":\"heuristic_CRT_beam_structured_search\",\n \"classification\":\""<<(candidate?"CANDIDATE_REQUIRES_INDEPENDENT_VERIFIERS":"HEURISTIC_NO_CANDIDATE")<<"\",\n \"low\":\""<<a.L<<"\",\n \"high\":\""<<a.U<<"\",\n \"C\":"<<a.C<<",\n \"D\":"<<a.D<<",\n \"distinct_shift_count\":"<<sh.size()<<",\n \"base_primes\":[3,7,11,19,23],\n \"beam_size\":"<<a.beam<<",\n \"beam_states_final\":"<<states.size()<<",\n \"base_modulus\":\""<<M<<"\",\n \"actual_integers_scored\":"<<actual<<",\n \"pool_prime_count\":"<<pool.size()<<",\n \"top_n_retained\":"<<tops.size()<<",\n \"exact_candidates_checked\":"<<checks<<",\n \"candidate\":"<<(candidate?"\""+std::to_string(candidate)+"\"":"null")<<",\n \"best_exact_near_misses\":[";for(size_t i=0;i<std::min<size_t>(50,ex.size());++i){if(i)js<<',';auto const&q=ex[i];js<<"{\"n\":\""<<q.n<<"\",\"pool_score\":"<<q.poolscore<<",\"passed_distinct_shifts\":"<<q.passed<<",\"failing_shift\":\""<<q.failshift<<"\",\"failing_remainder\":\""<<q.failrem<<"\"}";}js<<"],\n \"elapsed_seconds\":"<<sec<<"\n}\n";
 std::cout<<"actual_integers_scored="<<actual<<"\nbest_pool_score="<<(tops.empty()?0:tops.front().score)<<"\nbest_exact_passed="<<(ex.empty()?0:ex.front().passed)<<"\ncandidate="<<(candidate?std::to_string(candidate):"NONE")<<"\nelapsed_seconds="<<sec<<"\n";return candidate?0:1;
}catch(std::exception const&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}}
