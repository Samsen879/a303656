// Independent clean-room finite scanner for cross-checking Method C results.
// No code is shared with search_bitset.cpp.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

static bool primality(uint64_t x) {
    if (x < 2) return false;
    if ((x & 1U) == 0) return x == 2;
    for (uint64_t q = 3; q <= x / q; q += 2) if (x % q == 0) return false;
    return true;
}
static std::vector<uint64_t> read_pool(const std::string& arg) {
    std::string text = arg;
    std::ifstream in(arg);
    if (in) { std::ostringstream b; b << in.rdbuf(); text = b.str(); }
    for (char& ch : text) if (ch=='\n'||ch=='\r'||ch==' '||ch=='\t') ch=',';
    std::stringstream ss(text); std::string cell; std::vector<uint64_t> out; std::set<uint64_t> seen;
    while (std::getline(ss,cell,',')) if (!cell.empty()) {
        uint64_t p=std::stoull(cell);
        if (!seen.insert(p).second || !primality(p) || p%4!=3 || p>0xffffffffULL) throw std::runtime_error("bad prime pool");
        out.push_back(p);
    }
    if (out.empty()) throw std::runtime_error("empty pool");
    return out;
}
static uint64_t ipow(uint64_t b,int e) {
    __uint128_t y=1;
    for(int i=0;i<e;++i){y*=b;if(y>UINT64_MAX)throw std::runtime_error("power overflow");}
    return static_cast<uint64_t>(y);
}
int main(int argc,char**argv) {
    try {
        uint64_t lo=0,hi=0; int C=-1,D=-1; std::string pool_arg,json_file;
        for(int i=1;i<argc;++i){
            std::string a=argv[i]; auto val=[&](){if(++i>=argc)throw std::runtime_error("missing value");return std::string(argv[i]);};
            if(a=="--low")lo=std::stoull(val()); else if(a=="--high")hi=std::stoull(val());
            else if(a=="--C")C=std::stoi(val()); else if(a=="--D")D=std::stoi(val());
            else if(a=="--primes")pool_arg=val(); else if(a=="--json")json_file=val();
            else throw std::runtime_error("unknown argument");
        }
        if(lo==0||hi==0||lo>hi||C<0||D<0||pool_arg.empty()||json_file.empty())throw std::runtime_error("missing required arguments");
        uint64_t cap3=ipow(3,C+1),cap5=ipow(5,D+1);
        if(hi>=cap3+1||hi>=cap5+1)throw std::runtime_error("finite exponent bound failure");
        auto P=read_pool(pool_arg);
        std::vector<uint64_t>a(C+1),b(D+1);a[0]=b[0]=1;
        for(int i=1;i<=C;++i) a[i]=3*a[i-1];
        for(int j=1;j<=D;++j) b[j]=5*b[j-1];
        std::set<uint64_t> shift_set;
        for(uint64_t x:a)for(uint64_t y:b){__uint128_t z=(__uint128_t)x+y;if(z<=hi)shift_set.insert((uint64_t)z);}
        std::vector<uint64_t> shifts(shift_set.begin(),shift_set.end());
        std::vector<uint64_t> candidates;
        uint64_t shift_checks=0,prime_checks=0;
        std::vector<uint64_t> first_failure_count(shifts.size(),0);
        std::vector<uint64_t> chosen_prime_count(P.size(),0);
        auto t0=std::chrono::steady_clock::now();
        for(uint64_t n=lo;;++n){
            bool all=true;
            for(size_t si=0; si<shifts.size(); ++si){
                uint64_t s=shifts[si];
                if(s>n) break;
                ++shift_checks;
                bool one=false;
                size_t chosen_index=P.size();
                if(n>s){
                    uint64_t r=n-s;
                    for(size_t pi=0; pi<P.size(); ++pi){
                        uint64_t p=P[pi];
                        ++prime_checks;
                        uint64_t p2=p*p;
                        if(r%p==0 && r%p2!=0){
                            one=true;
                            chosen_index=pi;
                            break;
                        }
                    }
                }
                if(one) ++chosen_prime_count[chosen_index];
                if(!one){
                    ++first_failure_count[si];
                    all=false;
                    break;
                }
            }
            if(all)candidates.push_back(n);
            if(n==hi)break;
        }
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count();
        std::ofstream out(json_file); if(!out)throw std::runtime_error("cannot write json");
        out<<"{\n \"method\":\"independent_clean_room_cpp_exhaustive\",\n \"low\":\""<<lo<<"\",\n \"high\":\""<<hi<<"\",\n \"C\":"<<C<<",\n \"D\":"<<D<<",\n \"prime_count\":"<<P.size()<<",\n \"distinct_shift_count_relevant_to_high\":"<<shifts.size()<<",\n \"integers_tested\":"<<(hi-lo+1)<<",\n \"shift_checks\":"<<shift_checks<<",\n \"prime_checks\":"<<prime_checks<<",\n \"candidate_count\":"<<candidates.size()<<",\n \"candidates\":[";
        for(size_t i=0;i<candidates.size();++i){if(i)out<<',';out<<'"'<<candidates[i]<<'"';}
        out<<"],\n \"elapsed_seconds\":"<<sec<<",\n";
        std::vector<size_t> order(shifts.size());
        for(size_t i=0;i<order.size();++i) order[i]=i;
        std::sort(order.begin(),order.end(),[&](size_t i,size_t j){
            return first_failure_count[i]==first_failure_count[j]
                ? shifts[i]<shifts[j]
                : first_failure_count[i]>first_failure_count[j];
        });
        out<<" \"first_failure_histogram\":[";
        bool first=true;
        for(size_t idx:order){
            if(first_failure_count[idx]==0) continue;
            if(!first) out<<',';
            first=false;
            out<<"{\"shift\":\""<<shifts[idx]<<"\",\"count\":"<<first_failure_count[idx]<<"}";
        }
        out<<"],\n \"chosen_prime_counts\":[";
        first=true;
        for(size_t i=0;i<P.size();++i){
            if(chosen_prime_count[i]==0) continue;
            if(!first) out<<',';
            first=false;
            out<<"{\"prime\":"<<P[i]<<",\"count\":"<<chosen_prime_count[i]<<"}";
        }
        out<<"],\n \"classification\":\"EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL\"\n}\n";
        std::cout<<"integers_tested="<<(hi-lo+1)<<"\nshift_checks="<<shift_checks<<"\nprime_checks="<<prime_checks<<"\ncandidate_count="<<candidates.size()<<"\nelapsed_seconds="<<sec<<"\n"<<(candidates.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";
        return candidates.empty()?1:0;
    } catch(std::exception const&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
