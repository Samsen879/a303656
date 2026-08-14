// Exact segmented residue sieve for the bounded A303656 valuation-one certificate.
// Independent of search_bitset.cpp: it marks G_s by arithmetic progressions.
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
#include <vector>

static bool prime_trial(uint64_t n){
    if(n<2) return false; if((n&1)==0) return n==2;
    for(uint64_t q=3;q<=n/q;q+=2) if(n%q==0) return false;
    return true;
}
static std::vector<uint64_t> read_pool(const std::string& arg){
    std::string text=arg; std::ifstream f(arg); if(f){std::ostringstream o;o<<f.rdbuf();text=o.str();}
    for(char&c:text) if(c=='\n'||c=='\r'||c==' '||c=='\t') c=',';
    std::stringstream ss(text); std::string cell; std::vector<uint64_t>P; std::set<uint64_t>seen;
    while(std::getline(ss,cell,',')) if(!cell.empty()){
        uint64_t p=std::stoull(cell);
        if(!seen.insert(p).second) throw std::runtime_error("duplicate prime");
        if(p>0xffffffffULL || p%4!=3 || !prime_trial(p)) throw std::runtime_error("invalid obstruction prime "+std::to_string(p));
        P.push_back(p);
    }
    if(P.empty()) throw std::runtime_error("empty prime pool");
    return P;
}
static uint64_t upow(uint64_t b,int e){__uint128_t x=1;for(int i=0;i<e;i++){x*=b;if(x>UINT64_MAX)throw std::runtime_error("power overflow");}return(uint64_t)x;}
static inline void setbit(std::vector<uint64_t>&v,uint64_t i){v[i>>6]|=uint64_t(1)<<(i&63);}
static bool anybit(const std::vector<uint64_t>&v){for(uint64_t x:v)if(x)return true;return false;}
static uint64_t pop(const std::vector<uint64_t>&v){uint64_t z=0;for(uint64_t x:v)z+=__builtin_popcountll(x);return z;}

int main(int argc,char**argv){
 try{
    uint64_t L=0,U=0,W=1000000; int C=-1,D=-1; std::string parg,jpath,cpath; bool quiet=false;
    for(int i=1;i<argc;i++){
        std::string a=argv[i]; auto val=[&](){if(++i>=argc)throw std::runtime_error("missing option value");return std::string(argv[i]);};
        if(a=="--low")L=std::stoull(val()); else if(a=="--high")U=std::stoull(val());
        else if(a=="--C")C=std::stoi(val()); else if(a=="--D")D=std::stoi(val());
        else if(a=="--primes")parg=val(); else if(a=="--window")W=std::stoull(val());
        else if(a=="--json")jpath=val(); else if(a=="--candidates")cpath=val(); else if(a=="--quiet")quiet=true;
        else throw std::runtime_error("unknown option "+a);
    }
    if(!L||!U||L>U||!W||C<0||D<0||parg.empty()||jpath.empty()) throw std::runtime_error("missing required arguments");
    uint64_t cap3=upow(3,C+1),cap5=upow(5,D+1);
    if(U>=cap3+1 || U>=cap5+1) throw std::runtime_error("finite exponent-domain inequality failed");
    auto P=read_pool(parg);
    std::vector<uint64_t>a(C+1),b(D+1);a[0]=b[0]=1;for(int i=1;i<=C;i++)a[i]=3*a[i-1];for(int j=1;j<=D;j++)b[j]=5*b[j-1];
    std::map<uint64_t,std::vector<std::pair<int,int>>> byshift;
    uint64_t pair_count=0;
    for(int c=0;c<=C;c++)for(int d=0;d<=D;d++){
        __uint128_t x=(__uint128_t)a[c]+b[d]; if(x<=U){byshift[(uint64_t)x].push_back({c,d});pair_count++;}
    }
    std::vector<uint64_t>S;for(auto const&kv:byshift)S.push_back(kv.first);
    std::ofstream cand;if(!cpath.empty()){cand.open(cpath);if(!cand)throw std::runtime_error("cannot open candidate file");}
    uint64_t tested=0,windows=0,shift_sieves=0,mark_attempts=0; std::vector<uint64_t>found;
    auto t0=std::chrono::steady_clock::now(); uint64_t A=L;
    while(A<=U){
        uint64_t B=U;
        if(W-1<=U-A) B=std::min(B,A+W-1);
        auto nxt=std::upper_bound(S.begin(),S.end(),A);
        if(nxt!=S.end() && *nxt>A) B=std::min(B,*nxt-1); // active-set exact segmentation
        uint64_t len=B-A+1,words=(len+63)/64;
        std::vector<uint64_t>alive(words,~uint64_t(0));if(len&63)alive.back()=(uint64_t(1)<<(len&63))-1;
        size_t active=std::upper_bound(S.begin(),S.end(),A)-S.begin();
        // Ascending shifts reproduce the independently observed strongest-failure order.
        for(size_t si=0;si<active;si++){
            uint64_t s=S[si]; std::vector<uint64_t>good(words,0); ++shift_sieves;
            uint64_t Amod;
            for(uint64_t p:P){
                Amod=A%p; uint64_t smod=s%p; uint64_t delta=(smod>=Amod)?(smod-Amod):(p-(Amod-smod));
                if(delta>=len) continue;
                uint64_t first=A+delta; // first >= A with first == s (mod p)
                uint64_t q=((first-s)/p)%p; // lift index modulo p; q=0 means p^2 divides first-s
                for(uint64_t idx=delta;idx<len;idx+=p){
                    ++mark_attempts;
                    if(q!=0) setbit(good,idx);
                    if(++q==p)q=0;
                }
            }
            for(size_t w=0;w<words;w++)alive[w]&=good[w];
            if(!anybit(alive)) break;
        }
        uint64_t survivors=pop(alive);
        if(!quiet)std::cout<<"WINDOW low="<<A<<" high="<<B<<" active_distinct_shifts="<<active<<" survivors="<<survivors<<"\n";
        for(size_t wi=0;wi<alive.size();wi++)for(uint64_t x=alive[wi];x;x&=x-1){unsigned bit=__builtin_ctzll(x);uint64_t idx=(uint64_t)wi*64+bit;if(idx<len){uint64_t n=A+idx;found.push_back(n);if(cand)cand<<n<<"\n";}}
        tested+=len;windows++; if(B==UINT64_MAX)break; A=B+1;
    }
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
    std::ofstream js(jpath);if(!js)throw std::runtime_error("cannot write json");
    js<<"{\n \"method\":\"C_exact_segmented_residue_bitset\",\n \"low\":\""<<L<<"\",\n \"high\":\""<<U<<"\",\n \"C\":"<<C<<",\n \"D\":"<<D<<",\n \"prime_count\":"<<P.size()<<",\n \"rectangle_pair_count_relevant_to_high\":"<<pair_count<<",\n \"distinct_shift_count_relevant_to_high\":"<<S.size()<<",\n \"integers_tested\":"<<tested<<",\n \"windows\":"<<windows<<",\n \"shift_sieves\":"<<shift_sieves<<",\n \"mark_attempts\":"<<mark_attempts<<",\n \"candidate_count\":"<<found.size()<<",\n \"candidates\":[";
    for(size_t i=0;i<found.size();i++){if(i)js<<',';js<<'"'<<found[i]<<'"';}
    js<<"],\n \"elapsed_seconds\":"<<sec<<",\n \"classification\":\""<<(found.empty()?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL":"CANDIDATES REQUIRE INDEPENDENT VERIFIER")<<"\"\n}\n";
    std::cout<<"integers_tested="<<tested<<"\nshift_sieves="<<shift_sieves<<"\nmark_attempts="<<mark_attempts<<"\ncandidate_count="<<found.size()<<"\nelapsed_seconds="<<sec<<"\n"<<(found.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";
    return found.empty()?1:0;
 }catch(std::exception const&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
