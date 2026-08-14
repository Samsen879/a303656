// Clean-room exact segmented byte sieve for independent cross-validation.
// It does not share bit packing or helper code with search_sieve_bitset.cpp.
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

static bool exact_prime(uint64_t x){
    if(x<2)return false;
    if(x%2==0)return x==2;
    uint64_t f=3;
    while(f<=x/f){if(x%f==0)return false;f+=2;}
    return true;
}
static std::vector<uint64_t> load_primes(const std::string& name){
    std::string raw=name;std::ifstream in(name);if(in){std::ostringstream z;z<<in.rdbuf();raw=z.str();}
    for(char&c:raw){if(c=='\n'||c=='\r'||c==' '||c=='\t')c=',';}
    std::vector<uint64_t> out;std::set<uint64_t> uniq;std::stringstream ss(raw);std::string t;
    while(std::getline(ss,t,',')){
        if(t.empty())continue;uint64_t p=std::stoull(t);
        if(p>0xffffffffULL||p%4!=3||!exact_prime(p)||!uniq.insert(p).second)throw std::runtime_error("bad prime list");
        out.push_back(p);
    }
    if(out.empty())throw std::runtime_error("no primes");return out;
}
static uint64_t power_u64(uint64_t b,int e){uint64_t r=1;for(int k=0;k<e;k++){if(r>UINT64_MAX/b)throw std::runtime_error("power overflow");r*=b;}return r;}

int main(int argc,char**argv){
 try{
    uint64_t lo=0,hi=0,block=1000000;int C=-1,D=-1;std::string primes_arg,json_name,cand_name;bool quiet=false;
    for(int i=1;i<argc;i++){
        std::string a=argv[i];auto take=[&](){if(i+1>=argc)throw std::runtime_error("missing value");return std::string(argv[++i]);};
        if(a=="--low")lo=std::stoull(take());else if(a=="--high")hi=std::stoull(take());
        else if(a=="--C")C=std::stoi(take());else if(a=="--D")D=std::stoi(take());
        else if(a=="--primes")primes_arg=take();else if(a=="--window")block=std::stoull(take());
        else if(a=="--json")json_name=take();else if(a=="--candidates")cand_name=take();else if(a=="--quiet")quiet=true;
        else throw std::runtime_error("unknown argument");
    }
    if(lo==0||hi==0||lo>hi||block==0||C<0||D<0||primes_arg.empty()||json_name.empty())throw std::runtime_error("arguments incomplete");
    uint64_t lim3=power_u64(3,C+1),lim5=power_u64(5,D+1);
    if(!(hi<lim3+1)&&lim3!=UINT64_MAX)throw std::runtime_error("C domain bound rejected");
    if(!(hi<lim5+1)&&lim5!=UINT64_MAX)throw std::runtime_error("D domain bound rejected");
    std::vector<uint64_t>P=load_primes(primes_arg);
    std::vector<uint64_t>three(C+1),five(D+1);three[0]=five[0]=1;
    for(int c=1;c<=C;c++)three[c]=three[c-1]*3;
    for(int d=1;d<=D;d++)five[d]=five[d-1]*5;
    std::vector<uint64_t>all_shifts;uint64_t admissible_pairs=0;
    for(int c=0;c<=C;c++)for(int d=0;d<=D;d++){
        if(three[c]<=hi-five[d]){all_shifts.push_back(three[c]+five[d]);admissible_pairs++;}
    }
    std::sort(all_shifts.begin(),all_shifts.end());all_shifts.erase(std::unique(all_shifts.begin(),all_shifts.end()),all_shifts.end());
    std::ofstream cand;if(!cand_name.empty()){cand.open(cand_name);if(!cand)throw std::runtime_error("candidate output failure");}
    uint64_t count_n=0,count_windows=0,count_sieves=0,count_marks=0;std::vector<uint64_t>hits;
    auto start=std::chrono::steady_clock::now();uint64_t left=lo;
    while(left<=hi){
        uint64_t right=hi;if(block-1<=hi-left)right=std::min(right,left+block-1);
        auto upper=std::upper_bound(all_shifts.begin(),all_shifts.end(),left);
        if(upper!=all_shifts.end())right=std::min(right,*upper-1);
        const size_t length=(size_t)(right-left+1);std::vector<unsigned char>survive(length,1);
        size_t active=(size_t)(std::upper_bound(all_shifts.begin(),all_shifts.end(),left)-all_shifts.begin());
        for(size_t k=0;k<active;k++){
            const uint64_t s=all_shifts[k];std::vector<unsigned char>covered(length,0);count_sieves++;
            for(uint64_t p:P){
                uint64_t remL=left%p,remS=s%p;
                uint64_t offset=(remS+p-remL)%p;
                if(offset>=length)continue;
                uint64_t first=left+offset;
                uint64_t lift=((first-s)/p)%p;
                for(uint64_t pos=offset;pos<length;pos+=p){
                    count_marks++;
                    if(lift!=0)covered[(size_t)pos]=1;
                    lift++;if(lift==p)lift=0;
                }
            }
            bool nonempty=false;
            for(size_t i=0;i<length;i++){survive[i]=(unsigned char)(survive[i]&covered[i]);nonempty|=(survive[i]!=0);}
            if(!nonempty)break;
        }
        uint64_t local=0;
        for(size_t i=0;i<length;i++)if(survive[i]){uint64_t n=left+(uint64_t)i;hits.push_back(n);local++;if(cand)cand<<n<<'\n';}
        if(!quiet)std::cout<<"BLOCK low="<<left<<" high="<<right<<" active="<<active<<" survivors="<<local<<"\n";
        count_n+=(uint64_t)length;count_windows++;
        if(right==UINT64_MAX)break;left=right+1;
    }
    double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    std::ofstream out(json_name);if(!out)throw std::runtime_error("json output failure");
    out<<"{\n \"method\":\"independent_clean_room_segmented_byte_sieve\",\n \"low\":\""<<lo<<"\",\n \"high\":\""<<hi<<"\",\n \"C\":"<<C<<",\n \"D\":"<<D<<",\n \"prime_count\":"<<P.size()<<",\n \"admissible_pair_count_at_high\":"<<admissible_pairs<<",\n \"distinct_shift_count_at_high\":"<<all_shifts.size()<<",\n \"integers_tested\":"<<count_n<<",\n \"windows\":"<<count_windows<<",\n \"shift_sieves\":"<<count_sieves<<",\n \"mark_attempts\":"<<count_marks<<",\n \"candidate_count\":"<<hits.size()<<",\n \"candidates\":[";
    for(size_t i=0;i<hits.size();i++){if(i)out<<',';out<<'"'<<hits[i]<<'"';}
    out<<"],\n \"elapsed_seconds\":"<<elapsed<<",\n \"classification\":\""<<(hits.empty()?"EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS PRIME POOL":"CANDIDATES REQUIRE INDEPENDENT VERIFIER")<<"\"\n}\n";
    std::cout<<"integers_tested="<<count_n<<"\nshift_sieves="<<count_sieves<<"\nmark_attempts="<<count_marks<<"\ncandidate_count="<<hits.size()<<"\nelapsed_seconds="<<elapsed<<"\n"<<(hits.empty()?"EXACT_EMPTY":"CANDIDATES_FOUND")<<"\n";
    return hits.empty()?1:0;
 }catch(const std::exception&e){std::cerr<<"ERROR "<<e.what()<<"\n";return 2;}
}
