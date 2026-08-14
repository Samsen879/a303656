// Pair-centric meet-in-the-middle exact weighted fixed-P4 enumerator.
#include "sha256_small.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr std::size_t PC=407,WORDS=7; constexpr std::uint64_t TOTAL=28227969ULL;
constexpr std::array<unsigned,4> PRIME{{3,7,11,23}},Q{{9,49,121,529}};
struct EPair{unsigned c,d;std::uint64_t s;bool operator==(const EPair&o)const{return c==o.c&&d==o.d&&s==o.s;}};
struct Bits{std::array<std::uint64_t,WORDS>b{};bool operator==(const Bits&o)const{return b==o.b;}bool operator<(const Bits&o)const{return b<o.b;}};
struct Four{std::array<std::uint16_t,4>v{};bool operator<(const Four&o)const{return v<o.v;}};
struct Triple{std::uint64_t o=0,e=0,p=0;};
struct Table{std::array<std::uint64_t,PC>o{},e{},p{};std::uint64_t od=0,ed=0,pd=0;};
struct Opt{bool init=false;std::uint64_t max=0,n=0;Four first{};Bits bits{};Triple triple{};std::vector<Four>ties;};
struct Lead{std::uint64_t value;Four first;Bits bits;unsigned coverage;Triple triple;};
struct Mark{std::string name;Four t;Bits bits{};unsigned coverage=0;Triple triple{};};
using ResidueBits=std::array<std::vector<Bits>,4>;
void insist(bool ok,const std::string&m){if(!ok)throw std::runtime_error(m);}
std::vector<std::uint64_t> pows(std::uint64_t x,std::uint64_t n){std::vector<std::uint64_t>r;std::uint64_t y=1;for(;;){r.push_back(y);if(y>n/x)break;y*=x;}return r;}
std::vector<EPair> pairs_at(std::uint64_t n){auto x=pows(3,n),y=pows(5,n);std::vector<EPair>r;for(unsigned i=0;i<x.size();++i)for(unsigned j=0;j<y.size();++j)if(x[i]+y[j]<=n)r.push_back({i,j,x[i]+y[j]});return r;}
std::vector<std::string> fields(const std::string&s){std::vector<std::string>v;std::size_t a=0;for(;;){auto b=s.find(',',a);v.push_back(s.substr(a,b-a));if(b==std::string::npos)return v;a=b+1;}}
Table load(const std::string&fn){std::ifstream in(fn);insist(bool(in),"weights open failed");std::string s;insist(bool(std::getline(in,s)),"weights empty");auto h=fields(s);insist(h.size()==13&&h[0]=="pair_index"&&h[4]=="odd_winner_numerator"&&h[12]=="pool_class_prevalence","weights schema");Table t;unsigned i=0;while(std::getline(in,s)){auto z=fields(s);insist(z.size()==13&&std::stoul(z[0])==i,"weight order");t.o[i]=std::stoull(z[4]);t.e[i]=std::stoull(z[6]);t.p[i]=std::stoull(z[8]);auto od=std::stoull(z[5]),ed=std::stoull(z[7]),pd=std::stoull(z[9]);if(i==0){t.od=od;t.ed=ed;t.pd=pd;}insist(od==t.od&&ed==t.ed&&pd==t.pd,"denominator changed");++i;}insist(i==PC&&t.od==2334&&t.ed==2337&&t.pd==4671,"weights dimensions");return t;}
ResidueBits pair_centric(const std::vector<EPair>&pairs){ResidueBits r;for(unsigned k=0;k<4;++k)r[k].resize(Q[k]);for(unsigned i=0;i<PC;++i)for(unsigned k=0;k<4;++k){unsigned base=pairs[i].s%Q[k];for(unsigned lift=1;lift<PRIME[k];++lift){unsigned residue=(base+lift*PRIME[k])%Q[k];r[k][residue].b[i/64]|=1ULL<<(i%64);}}return r;}
Bits join(const Bits&a,const Bits&b){Bits z;for(unsigned i=0;i<WORDS;++i)z.b[i]=a.b[i]|b.b[i];return z;}
unsigned cardinality(const Bits&x){unsigned n=0;for(auto w:x.b)n+=__builtin_popcountll(w);return n;}
// Deliberately independent accumulation: scan all 407 pair positions rather than set bits.
Triple sum_b(const Bits&x,const Table&t){Triple z;for(unsigned i=0;i<PC;++i)if((x.b[i/64]>>(i%64))&1ULL){z.o+=t.o[i];z.e+=t.e[i];z.p+=t.p[i];}return z;}
std::uint64_t component(const Triple&x,unsigned k){return k==0?x.o:k==1?x.e:x.p;}
Four four(unsigned a,unsigned b,unsigned c,unsigned d){return Four{{std::uint16_t(a),std::uint16_t(b),std::uint16_t(c),std::uint16_t(d)}};}
void put16(std::uint8_t*p,std::uint16_t x){p[0]=x&255U;p[1]=(x>>8)&255U;}void put64(std::uint8_t*p,std::uint64_t x){for(unsigned i=0;i<8;++i)p[i]=(x>>(8*i))&255U;}
std::array<std::uint8_t,51> pack(const Bits&x){std::array<std::uint8_t,51>z{};for(unsigned i=0;i<PC;++i)if((x.b[i/64]>>(i%64))&1ULL)z[i/8]|=1U<<(i%8);return z;}
std::string hx(const Bits&x){static constexpr char d[]="0123456789abcdef";std::string s;for(auto y:pack(x)){s+=d[y>>4];s+=d[y&15];}return s;}
std::string ft(const Four&t){std::ostringstream s;s<<t.v[0]<<','<<t.v[1]<<','<<t.v[2]<<','<<t.v[3];return s.str();}
void ordered_hash(Sha256Small&h,const Four&t,const Bits&x,unsigned g,const Triple&s){std::uint8_t row[85]{};for(unsigned i=0;i<4;++i)put16(row+2*i,t.v[i]);auto b=pack(x);std::copy(b.begin(),b.end(),row+8);put16(row+59,g);put64(row+61,s.o);put64(row+69,s.e);put64(row+77,s.p);h.update(row,85);}
void take(Opt&o,std::uint64_t value,const Four&t,const Bits&b,const Triple&s){if(!o.init||value>o.max){o.init=true;o.max=value;o.n=1;o.first=t;o.bits=b;o.triple=s;o.ties.assign(1,t);}else if(value==o.max){++o.n;o.ties.push_back(t);}}
void lead(std::vector<Lead>&v,const Lead&x){for(auto&y:v)if(y.bits==x.bits)return;v.push_back(x);std::sort(v.begin(),v.end(),[](auto&a,auto&b){return a.value!=b.value?a.value>b.value:a.first<b.first;});if(v.size()==9)v.pop_back();}
std::string tie_hash(const std::vector<Four>&v){Sha256Small h;for(auto&t:v){std::uint8_t b[8];for(unsigned i=0;i<4;++i)put16(b+2*i,t.v[i]);h.update(b,8);}return h.hex_digest();}
std::uint64_t place(const std::map<std::uint64_t,std::uint64_t>&h,std::uint64_t x){std::uint64_t r=1;for(auto i=h.rbegin();i!=h.rend()&&i->first>x;++i)r+=i->second;return r;}
void objective(std::ofstream&o,const char*scope,const char*name,const Opt&x,std::uint64_t den){o<<"objective\t"<<scope<<'\t'<<name<<'\t'<<den<<'\t'<<x.max<<'\t'<<x.n<<'\t'<<ft(x.first)<<'\t'<<hx(x.bits)<<'\t'<<cardinality(x.bits)<<'\t'<<x.triple.o<<'\t'<<x.triple.e<<'\t'<<x.triple.p<<'\t'<<tie_hash(x.ties)<<'\n';}
int run(int ac,char**av){insist(ac==3,"usage: enumerator weights.csv certificate.tsv");Sha256Small::self_test();auto pairs=pairs_at(183968950234ULL);insist(pairs.size()==PC&&pairs==pairs_at(246731069451ULL),"fixed domain");std::vector<std::pair<unsigned,unsigned>>same;for(auto&x:pairs)if(x.s==28)same.push_back({x.c,x.d});insist(same==std::vector<std::pair<unsigned,unsigned>>{{1,2},{3,0}},"shift 28 identities");auto weights=load(av[1]);auto base=pair_centric(pairs);
  std::vector<Bits> left(9*49),right(121*529);for(unsigned a=0;a<9;++a)for(unsigned b=0;b<49;++b)left[a*49+b]=join(base[0][a],base[1][b]);for(unsigned c=0;c<121;++c)for(unsigned d=0;d<529;++d)right[c*529+d]=join(base[2][c],base[3][d]);
  std::array<Opt,3> all{},fixed{};std::array<std::vector<Lead>,3> leaders;std::array<std::map<std::uint64_t,std::uint64_t>,3> distribution;Sha256Small stream;std::uint64_t count=0;
  std::vector<Mark> marks;for(const auto&item:std::vector<std::pair<std::string,Four>>{{"CAL-216",four(2,41,74,504)},{"CAL-227",four(2,41,50,504)},{"CAL-230",four(2,7,32,504)},{"G231-COMMON",four(2,7,50,17)}}){Mark z;z.name=item.first;z.t=item.second;marks.push_back(z);}
  for(unsigned ab=0;ab<left.size();++ab){unsigned a=ab/49,b=ab%49;for(unsigned cd=0;cd<right.size();++cd){unsigned c=cd/529,d=cd%529;Four t=four(a,b,c,d);Bits bits=join(left[ab],right[cd]);Triple s=sum_b(bits,weights);unsigned g=cardinality(bits);ordered_hash(stream,t,bits,g,s);++count;for(unsigned k=0;k<3;++k){auto value=component(s,k);++distribution[k][value];take(all[k],value,t,bits,s);lead(leaders[k],{value,t,bits,g,s});if(a==2)take(fixed[k],value,t,bits,s);}for(auto&m:marks)if(m.t.v==t.v){m.bits=bits;m.coverage=g;m.triple=s;}}}
  insist(count==TOTAL,"full row count");std::set<Bits>wanted;for(auto&v:leaders)for(auto&x:v)wanted.insert(x.bits);for(auto&m:marks)wanted.insert(m.bits);std::map<Bits,Four>representative;for(unsigned b=0;b<49;++b)for(unsigned cd=0;cd<right.size();++cd){unsigned c=cd/529,d=cd%529;Bits bits=join(left[2*49+b],right[cd]);if(wanted.count(bits)&&!representative.count(bits))representative[bits]=four(2,b,c,d);}
  std::ofstream out(av[2]);insist(bool(out),"certificate open");out<<"schema\ta303656-weighted-enumerator-certificate-v1\nimplementation\tB-pair-centric-fullscan-accumulation\nrows\t"<<count<<"\nordered_result_digest\t"<<stream.hex_digest()<<"\n";const char*name[3]={"odd","even","pool"};std::uint64_t den[3]={weights.od,weights.ed,weights.pd};for(unsigned k=0;k<3;++k){objective(out,"full",name[k],all[k],den[k]);objective(out,"t3eq2",name[k],fixed[k],den[k]);}
  for(unsigned k=0;k<3;++k)for(unsigned i=0;i<leaders[k].size();++i){auto&x=leaders[k][i];out<<"top\t"<<name[k]<<'\t'<<i+1<<'\t'<<ft(x.first)<<'\t'<<hx(x.bits)<<'\t'<<x.coverage<<'\t'<<x.triple.o<<'\t'<<x.triple.e<<'\t'<<x.triple.p<<'\t';auto r=representative.find(x.bits);out<<(r==representative.end()?"NONE":ft(r->second))<<'\n';}
  for(auto&m:marks)out<<"target\t"<<m.name<<'\t'<<ft(m.t)<<'\t'<<hx(m.bits)<<'\t'<<m.coverage<<'\t'<<m.triple.o<<'\t'<<place(distribution[0],m.triple.o)<<'\t'<<m.triple.e<<'\t'<<place(distribution[1],m.triple.e)<<'\t'<<m.triple.p<<'\t'<<place(distribution[2],m.triple.p)<<'\t'<<ft(representative.at(m.bits))<<'\n';
  for(unsigned k=0;k<3;++k){out<<"cross\t"<<name[k]<<"_opt\t"<<all[k].triple.o<<'\t'<<place(distribution[0],all[k].triple.o)<<'\t'<<all[k].triple.e<<'\t'<<place(distribution[1],all[k].triple.e)<<'\t'<<all[k].triple.p<<'\t'<<place(distribution[2],all[k].triple.p)<<'\n';}
  return 0;}
}
int main(int ac,char**av){try{return run(ac,av);}catch(const std::exception&e){std::cerr<<"weighted_enumerator_b: ERROR: "<<e.what()<<'\n';return 2;}}
