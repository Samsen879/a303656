// Exact unrestricted valuation-one shifted factor sieve for A303656.
//
// Unlike a finite-pool sieve, this implementation factors every integer in the
// needed remainder segment.  Therefore good(r) is true iff there exists ANY
// prime p == 3 (mod 4) with v_p(r)=1.  A surviving n is then checked against
// every active shift by an independent per-integer exact factorization routine.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

uint64_t ipow(uint64_t b, int e) {
    __uint128_t x=1;
    for(int i=0;i<e;++i){x*=b;if(x>std::numeric_limits<uint64_t>::max())throw std::runtime_error("power overflow");}
    return static_cast<uint64_t>(x);
}

uint64_t floor_sqrt(uint64_t n) {
    uint64_t lo=0, hi=std::min<uint64_t>(n, uint64_t(1)<<32);
    while(lo<hi){
        uint64_t mid=lo+(hi-lo+1)/2;
        if(mid<=n/mid)lo=mid;else hi=mid-1;
    }
    return lo;
}

std::vector<uint32_t> primes_up_to(uint64_t limit64) {
    if(limit64>std::numeric_limits<uint32_t>::max())throw std::runtime_error("prime sieve limit too large");
    uint32_t limit=static_cast<uint32_t>(limit64);
    std::vector<uint8_t> isprime(static_cast<size_t>(limit)+1,1);
    isprime[0]=0;
    if(limit>=1)isprime[1]=0;
    for(uint32_t p=2;p<=limit/p;++p)if(isprime[p]){
        uint64_t start=uint64_t(p)*p;
        for(uint64_t m=start;m<=limit;m+=p)isprime[static_cast<size_t>(m)]=0;
    }
    std::vector<uint32_t> out;
    for(uint32_t p=2;p<=limit;++p)if(isprime[p])out.push_back(p);
    return out;
}

inline void set_bit(std::vector<uint64_t>& b,uint64_t i){b[static_cast<size_t>(i>>6)]|=uint64_t(1)<<(i&63U);}
inline bool any_bits(const std::vector<uint64_t>& b){for(uint64_t w:b)if(w)return true;return false;}
uint64_t popcount_bits(const std::vector<uint64_t>& b){uint64_t z=0;for(uint64_t w:b)z+=__builtin_popcountll(w);return z;}
uint64_t slice_word(const std::vector<uint64_t>& src,uint64_t start){size_t wi=static_cast<size_t>(start>>6);unsigned off=start&63U;uint64_t a=wi<src.size()?src[wi]:0;if(!off)return a;uint64_t b=wi+1<src.size()?src[wi+1]:0;return(a>>off)|(b<<(64U-off));}

bool allowed_odd_exponent(int e, int max_odd) { return (e & 1) && (max_odd == 0 || e <= max_odd); }

bool unrestricted_obstruction(uint64_t r,const std::vector<uint32_t>& primes,int max_odd,uint64_t& obstruction,int& obstruction_v) {
    if(r==0)return false;
    uint64_t x=r;
    for(uint32_t q:primes){
        uint64_t p=q;
        if(p>x/p)break;
        if(x%p)continue;
        int e=0;
        do{x/=p;++e;}while(x%p==0);
        if((p&3U)==3U && allowed_odd_exponent(e,max_odd)){obstruction=p;obstruction_v=e;return true;}
    }
    if(x>1 && (x&3U)==3U){obstruction=x;obstruction_v=1;return true;}
    return false;
}

struct Args{
 uint64_t low=0,high=0,window=5000000;int C=-1,D=-1,max_odd=1;size_t prefix=64;std::string json,candidates;bool quiet=false;
};
Args args(int argc,char**argv){Args a;for(int i=1;i<argc;++i){std::string k=argv[i];auto v=[&](const char*n){if(i+1>=argc)throw std::runtime_error(std::string("missing ")+n);return std::string(argv[++i]);};
 if(k=="--low")a.low=std::stoull(v("low"));else if(k=="--high")a.high=std::stoull(v("high"));else if(k=="--C")a.C=std::stoi(v("C"));else if(k=="--D")a.D=std::stoi(v("D"));else if(k=="--window")a.window=std::stoull(v("window"));else if(k=="--prefix-shifts")a.prefix=std::stoull(v("prefix"));else if(k=="--max-odd-valuation")a.max_odd=std::stoi(v("max odd valuation"));else if(k=="--json")a.json=v("json");else if(k=="--candidates")a.candidates=v("candidates");else if(k=="--quiet")a.quiet=true;else throw std::runtime_error("unknown argument "+k);}
 if(!a.low||!a.high||a.low>a.high||a.C<0||a.D<0||!a.window||!a.prefix||a.json.empty()) throw std::runtime_error("bad/missing arguments");
 if(a.max_odd<0 || (a.max_odd!=0 && (a.max_odd%2)==0)) throw std::runtime_error("--max-odd-valuation must be 0 (all odd) or a positive odd integer");
 return a;
}

} // namespace

int main(int argc,char**argv){
 try{
  Args a=args(argc,argv);uint64_t b3=ipow(3,a.C+1),b5=ipow(5,a.D+1);if(a.high>=b3+1||a.high>=b5+1)throw std::runtime_error("finite exponent bound failure");
  uint64_t global_max_remainder=a.high-2;uint64_t root=floor_sqrt(global_max_remainder);auto primes=primes_up_to(root);
  std::vector<uint64_t> p3(a.C+1),p5(a.D+1);p3[0]=p5[0]=1;for(int i=1;i<=a.C;++i)p3[i]=p3[i-1]*3;for(int i=1;i<=a.D;++i)p5[i]=p5[i-1]*5;
  std::map<uint64_t,std::vector<std::pair<int,int>>> mp;for(int c=0;c<=a.C;++c)for(int d=0;d<=a.D;++d){__uint128_t s=(__uint128_t)p3[c]+p5[d];if(s<=a.high)mp[(uint64_t)s].push_back({c,d});}
  std::vector<uint64_t> shifts;size_t pair_count=0;for(auto const&kv:mp){shifts.push_back(kv.first);pair_count+=kv.second.size();}
  std::ofstream cf;if(!a.candidates.empty()){cf.open(a.candidates);if(!cf)throw std::runtime_error("cannot write candidates");}
  struct NearMiss { uint64_t n; size_t passed; uint64_t failing_shift; uint64_t failing_remainder; };
  uint64_t tested=0,windows=0,activation=0,sieve_hits=0,sieve_divisions=0,residual_prime_hits=0,word_ands=0,prefix_survivors_total=0,full_shift_checks=0,full_factor_calls=0;
  std::vector<uint64_t> found; std::vector<NearMiss> near_misses; size_t max_prefix=0;
  auto t0=std::chrono::steady_clock::now();uint64_t cur=a.low;
  while(cur<=a.high){
   uint64_t end=a.high;if(a.window-1<=a.high-cur)end=std::min(end,cur+a.window-1);auto ni=std::upper_bound(shifts.begin(),shifts.end(),cur);if(ni!=shifts.end()&&*ni<=end){end=*ni-1;++activation;}
   size_t active=std::upper_bound(shifts.begin(),shifts.end(),cur)-shifts.begin();size_t pref=std::min(a.prefix,active);max_prefix=std::max(max_prefix,pref);uint64_t len=end-cur+1;tested+=len;++windows;
   std::vector<uint64_t> cand((len+63)/64,~uint64_t(0));if(len&63)cand.back()=(uint64_t(1)<<(len&63))-1;
   if(pref){uint64_t smin=shifts[0],smax=shifts[pref-1];if(cur<smax)throw std::runtime_error("activation invariant");uint64_t A=cur-smax,B=end-smin,R=B-A+1;
    std::vector<uint64_t> residual(static_cast<size_t>(R));for(uint64_t i=0;i<R;++i)residual[static_cast<size_t>(i)]=A+i;
    std::vector<uint64_t> good((R+63)/64,0);
    for(uint32_t q:primes){uint64_t p=q;if(p>B/p)break;uint64_t k=A/p+(A%p!=0);if(k>B/p)continue;uint64_t m=k*p;
     for(;;){size_t idx=static_cast<size_t>(m-A);uint64_t &x=residual[idx];int e=0;while(x%p==0){x/=p;++e;++sieve_divisions;}if((p&3U)==3U&&allowed_odd_exponent(e,a.max_odd)){set_bit(good,m-A);++sieve_hits;}if(B-m<p)break;m+=p;}
    }
    for(uint64_t i=0;i<R;++i){uint64_t x=residual[static_cast<size_t>(i)];if(x>1&&(x&3U)==3U){set_bit(good,i);++residual_prime_hits;}}
    for(size_t si=0;si<pref&&any_bits(cand);++si){uint64_t off=smax-shifts[si];for(size_t wi=0;wi<cand.size();++wi){cand[wi]&=slice_word(good,off+uint64_t(wi)*64);++word_ands;}if(len&63)cand.back()&=(uint64_t(1)<<(len&63))-1;}
   }
   uint64_t survivors=popcount_bits(cand);prefix_survivors_total+=survivors;
   for(size_t wi=0;wi<cand.size();++wi){
    uint64_t w=cand[wi];
    while(w){
     unsigned bit=__builtin_ctzll(w); uint64_t idx=uint64_t(wi)*64+bit;
     if(idx<len){
      uint64_t n=cur+idx; bool all=true; size_t passed=0; uint64_t fail_shift=0,fail_rem=0;
      size_t na=std::upper_bound(shifts.begin(),shifts.end(),n)-shifts.begin();
      for(size_t si=0;si<na;++si){
       ++full_shift_checks; ++full_factor_calls; uint64_t ob=0; int obv=0;
       if(!unrestricted_obstruction(n-shifts[si],primes,a.max_odd,ob,obv)){all=false;fail_shift=shifts[si];fail_rem=n-shifts[si];break;}
       ++passed;
      }
      if(all){found.push_back(n);if(cf)cf<<n<<'\n';}
      else if(near_misses.size()<1000){near_misses.push_back({n,passed,fail_shift,fail_rem});}
     }
     w&=w-1;
    }
   }
   if(!a.quiet)std::cout<<"WINDOW low="<<cur<<" high="<<end<<" active="<<active<<" prefix="<<pref<<" survivors="<<survivors<<" candidates="<<found.size()<<"\n";
   if(end==std::numeric_limits<uint64_t>::max()) break;
   cur=end+1;
  }
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();std::ofstream js(a.json);if(!js)throw std::runtime_error("cannot write json");
  js<<"{\n \"method\":\"exact_unrestricted_valuation_one_shifted_factor_sieve\",\n \"low\":\""<<a.low<<"\",\n \"high\":\""<<a.high<<"\",\n \"C\":"<<a.C<<",\n \"D\":"<<a.D<<",\n \"prime_sieve_limit\":"<<root<<",\n \"prime_count_up_to_limit\":"<<primes.size()<<",\n \"admissible_pair_count_at_high\":"<<pair_count<<",\n \"distinct_shift_count_at_high\":"<<shifts.size()<<",\n \"requested_prefix_shifts\":"<<a.prefix<<",\n \"maximum_prefix_shifts_used\":"<<max_prefix<<",\n \"window_size\":"<<a.window<<",\n \"windows\":"<<windows<<",\n \"activation_splits\":"<<activation<<",\n \"integers_tested\":"<<tested<<",\n \"sieve_divisions\":"<<sieve_divisions<<",\n \"small_prime_exact_one_hits\":"<<sieve_hits<<",\n \"large_residual_prime_hits\":"<<residual_prime_hits<<",\n \"prefix_word_ands\":"<<word_ands<<",\n \"survivors_after_prefix_total\":"<<prefix_survivors_total<<",\n \"full_shift_checks\":"<<full_shift_checks<<",\n \"full_factor_calls\":"<<full_factor_calls<<",\n \"candidate_count\":"<<found.size()<<",\n \"candidates\":[";for(size_t i=0;i<found.size();++i){if(i)js<<',';js<<'\"'<<found[i]<<'\"';}js<<"],\n \"near_misses\":[";
  for(size_t i=0;i<near_misses.size();++i){if(i)js<<',';auto const&m=near_misses[i];js<<"{\"n\":\""<<m.n<<"\",\"passed_distinct_shifts\":"<<m.passed<<",\"failing_shift\":\""<<m.failing_shift<<"\",\"failing_remainder\":\""<<m.failing_remainder<<"\"}";}
  js<<"],\n \"elapsed_seconds\":"<<sec<<",\n \"classification\":\""<<(found.empty()?(a.max_odd==1?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR UNRESTRICTED VALUATION-ONE CERTIFICATES":(a.max_odd==0?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR ALL ODD VALUATIONS":"EXACT EXHAUSTIVE FINITE COMPUTATION FOR BOUNDED ODD VALUATIONS")):"CANDIDATES REQUIRE TWO INDEPENDENT VERIFIERS")<<"\"\n}\n";
  std::cout<<"integers_tested="<<tested<<"\nsurvivors_after_prefix_total="<<prefix_survivors_total<<"\ncandidate_count="<<found.size()<<"\nelapsed_seconds="<<sec<<"\n"<<(found.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";return found.empty()?1:0;
 }catch(std::exception const&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
