// Exact segmented search for true counterexamples using Fermat's two-square criterion.
// For each shift s and every remainder r in the window, it determines exactly whether
// some prime 3 mod 4 has odd valuation. Candidate n survive only if every active r is obstructed.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

static uint64_t ipow(uint64_t b,int e){uint64_t x=1;for(int i=0;i<e;i++){if(x>UINT64_MAX/b)throw std::runtime_error("power overflow");x*=b;}return x;}
static uint64_t isqrt_exact(uint64_t n){
    uint64_t lo=0,hi=uint64_t(1)<<32;
    while(lo+1<hi){uint64_t m=lo+(hi-lo)/2;if(m<=n/m)lo=m;else hi=m;}
    return lo;
}
static std::vector<uint32_t> primes3(uint64_t limit){
    std::vector<unsigned char> sieve((size_t)limit+1,1);if(limit>=0)sieve[0]=0;if(limit>=1)sieve[1]=0;
    for(uint64_t q=2;q<=limit/q;q++)if(sieve[(size_t)q])for(uint64_t k=q*q;k<=limit;k+=q)sieve[(size_t)k]=0;
    std::vector<uint32_t> p;for(uint64_t q=3;q<=limit;q+=4)if(sieve[(size_t)q])p.push_back((uint32_t)q);return p;
}
static inline void setbit(std::vector<uint64_t>&b,uint64_t i){b[i>>6]|=uint64_t(1)<<(i&63);}
static uint64_t bitcount(const std::vector<uint64_t>&b){uint64_t z=0;for(auto x:b)z+=__builtin_popcountll(x);return z;}
static bool nonzero(const std::vector<uint64_t>&b){for(auto x:b)if(x)return true;return false;}
static bool has_odd_three_mod_four_valuation(uint64_t r,const std::vector<uint32_t>&P){
    if(r==0)return false;
    r >>= __builtin_ctzll(r);
    for(uint32_t pp:P){
        uint64_t p=pp;
        if(p>r/p)break;
        if(r%p==0){
            unsigned parity=0;
            do{r/=p;parity^=1;}while(r%p==0);
            if(parity)return true;
        }
    }
    return r%4==3;
}

int main(int argc,char**argv){
 try{
    uint64_t L=0,U=0,W=100000;int C=-1,D=-1;std::string json,candidates;bool quiet=false;
    for(int i=1;i<argc;i++){
        std::string a=argv[i];auto v=[&](){if(++i>=argc)throw std::runtime_error("missing value");return std::string(argv[i]);};
        if(a=="--low")L=std::stoull(v());else if(a=="--high")U=std::stoull(v());else if(a=="--C")C=std::stoi(v());else if(a=="--D")D=std::stoi(v());
        else if(a=="--window")W=std::stoull(v());else if(a=="--json")json=v();else if(a=="--candidates")candidates=v();else if(a=="--quiet")quiet=true;else throw std::runtime_error("unknown option");
    }
    if(!L||!U||L>U||!W||C<0||D<0||json.empty())throw std::runtime_error("required arguments missing");
    uint64_t c3=ipow(3,C+1),c5=ipow(5,D+1);if(U>=c3+1||U>=c5+1)throw std::runtime_error("finite exponent bound failed");
    std::vector<uint64_t>a(C+1),b(D+1);a[0]=b[0]=1;for(int i=1;i<=C;i++)a[i]=3*a[i-1];for(int j=1;j<=D;j++)b[j]=5*b[j-1];
    std::map<uint64_t,unsigned> mult;uint64_t pair_count=0;
    for(auto x:a)for(auto y:b){if(x<=U-y){mult[x+y]++;pair_count++;}}
    std::vector<uint64_t>S;for(auto const&kv:mult)S.push_back(kv.first);
    uint64_t maxrem=U-S.front();uint64_t root=isqrt_exact(maxrem);auto P=primes3(root);
    std::ofstream cf;if(!candidates.empty()){cf.open(candidates);if(!cf)throw std::runtime_error("cannot write candidates");}
    uint64_t A=L,tested=0,windows=0,shift_factorizations=0,division_events=0;std::vector<uint64_t>found;
    auto t0=std::chrono::steady_clock::now();
    while(A<=U){
        uint64_t B=U;if(W-1<=U-A)B=std::min(B,A+W-1);auto nxt=std::upper_bound(S.begin(),S.end(),A);if(nxt!=S.end())B=std::min(B,*nxt-1);
        uint64_t len=B-A+1,words=(len+63)/64;std::vector<uint64_t>alive(words,~uint64_t(0));if(len&63)alive.back()=(uint64_t(1)<<(len&63))-1;
        size_t active=std::upper_bound(S.begin(),S.end(),A)-S.begin();
        for(size_t si=0;si<active;si++){
            uint64_t s=S[si],r0=A-s,rmax=B-s;++shift_factorizations;
            uint64_t alive_before=bitcount(alive);
            if(alive_before<=64){
                // Sparse exact path: independently factor only the still-possible n values.
                for(size_t wi=0;wi<alive.size();wi++){
                    uint64_t word=alive[wi];
                    while(word){
                        unsigned bit=__builtin_ctzll(word);uint64_t idx=(uint64_t)wi*64+bit;
                        if(idx<len && !has_odd_three_mod_four_valuation(r0+idx,P))alive[wi]&=~(uint64_t(1)<<bit);
                        word&=word-1;
                    }
                }
            }else{
                // Dense exact path: segmented valuation sieve for the full window.
                std::vector<uint64_t>rem((size_t)len);std::vector<unsigned char>odd((size_t)len,0);
                for(uint64_t i=0;i<len;i++){
                    uint64_t r=r0+i;
                    if(r==0){rem[(size_t)i]=0;continue;}
                    rem[(size_t)i]=r>>__builtin_ctzll(r);
                }
                for(uint32_t pp:P){
                    uint64_t p=pp;if(p>rmax/p)break;
                    uint64_t delta=(p-(r0%p))%p;
                    for(uint64_t idx=delta;idx<len;idx+=p){
                        if(odd[(size_t)idx])continue;
                        uint64_t x=rem[(size_t)idx];unsigned parity=0;
                        while(x%p==0){x/=p;parity^=1;division_events++;}
                        rem[(size_t)idx]=x;if(parity)odd[(size_t)idx]=1;
                    }
                }
                std::vector<uint64_t>obstruct(words,0);
                for(uint64_t i=0;i<len;i++)if(odd[(size_t)i] || (rem[(size_t)i]>0 && rem[(size_t)i]%4==3))setbit(obstruct,i);
                for(size_t w=0;w<words;w++)alive[w]&=obstruct[w];
            }
            if(!nonzero(alive))break;
        }
        uint64_t local=bitcount(alive);if(!quiet)std::cout<<"WINDOW low="<<A<<" high="<<B<<" active="<<active<<" survivors="<<local<<"\n";
        for(size_t wi=0;wi<alive.size();wi++)for(uint64_t x=alive[wi];x;x&=x-1){unsigned bit=__builtin_ctzll(x);uint64_t idx=(uint64_t)wi*64+bit;if(idx<len){uint64_t n=A+idx;found.push_back(n);if(cf)cf<<n<<'\n';}}
        tested+=len;windows++;if(B==UINT64_MAX)break;A=B+1;
    }
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();std::ofstream out(json);if(!out)throw std::runtime_error("cannot write json");
    out<<"{\n \"method\":\"exact_segmented_two_square_parity_search\",\n \"low\":\""<<L<<"\",\n \"high\":\""<<U<<"\",\n \"C\":"<<C<<",\n \"D\":"<<D<<",\n \"pair_count_at_high\":"<<pair_count<<",\n \"distinct_shift_count_at_high\":"<<S.size()<<",\n \"trial_prime_bound\":"<<root<<",\n \"three_mod_four_prime_count\":"<<P.size()<<",\n \"integers_tested\":"<<tested<<",\n \"windows\":"<<windows<<",\n \"shift_factorizations\":"<<shift_factorizations<<",\n \"division_events\":"<<division_events<<",\n \"candidate_count\":"<<found.size()<<",\n \"candidates\":[";
    for(size_t i=0;i<found.size();i++){if(i)out<<',';out<<'"'<<found[i]<<'"';}
    out<<"],\n \"elapsed_seconds\":"<<sec<<",\n \"classification\":\""<<(found.empty()?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE ORIGINAL TWO-SQUARE CONDITION":"CANDIDATES REQUIRE FACTORIZATION CERTIFICATE")<<"\"\n}\n";
    std::cout<<"integers_tested="<<tested<<"\nshift_factorizations="<<shift_factorizations<<"\ndivision_events="<<division_events<<"\ncandidate_count="<<found.size()<<"\nelapsed_seconds="<<sec<<"\n"<<(found.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";
    return found.empty()?1:0;
 }catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
