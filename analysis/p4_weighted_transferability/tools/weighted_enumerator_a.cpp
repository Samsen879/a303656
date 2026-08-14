// Direct residue-centric exact weighted fixed-P4 enumerator.
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
#include <tuple>
#include <vector>

namespace {
constexpr std::uint64_t LOW=183968950234ULL,HIGH=246731069451ULL,ROWS=28227969ULL;
constexpr std::array<unsigned,4> P{{3,7,11,23}}, MOD{{9,49,121,529}};
constexpr std::size_t N=407,W=7;
struct Pair { unsigned c,d; std::uint64_t shift; bool operator==(const Pair&o)const{return c==o.c&&d==o.d&&shift==o.shift;} };
struct Mask { std::array<std::uint64_t,W> w{}; bool operator==(const Mask& o)const{return w==o.w;} bool operator<(const Mask&o)const{return w<o.w;} };
struct Tup { std::array<std::uint16_t,4> x{}; bool operator<(const Tup&o)const{return x<o.x;} };
struct Score { std::uint64_t odd=0,even=0,pool=0; };
struct Weights { std::array<std::uint64_t,N> odd{},even{},pool{}; std::uint64_t do_=0,de=0,dp=0; };
struct Best { std::uint64_t value=0,count=0; bool set=false; Tup first{}; Mask mask{}; Score cross{}; std::vector<Tup> args; };
struct Candidate { std::uint64_t value; Tup tuple; Mask mask; unsigned g; Score score; };
struct Target { std::string label; Tup tuple; Mask mask; unsigned g=0; Score score{}; };
using PMasks=std::array<std::vector<Mask>,4>;
[[noreturn]] void fail(const std::string&s){throw std::runtime_error(s);} void req(bool x,const std::string&s){if(!x)fail(s);}
std::vector<std::uint64_t> powers(std::uint64_t b,std::uint64_t lim){std::vector<std::uint64_t>v;for(std::uint64_t x=1;;x*=b){v.push_back(x);if(x>lim/b)break;}return v;}
std::vector<Pair> domain(std::uint64_t n){auto a=powers(3,n),b=powers(5,n);std::vector<Pair>r;for(unsigned c=0;c<a.size();++c)for(unsigned d=0;d<b.size();++d)if(a[c]<=n-b[d])r.push_back({c,d,a[c]+b[d]});return r;}
std::vector<std::string> split(const std::string&s,char sep){std::vector<std::string>r;std::stringstream q(s);for(std::string x;std::getline(q,x,sep);)r.push_back(x);return r;}
Weights read_weights(const std::string&path){std::ifstream f(path);req(bool(f),"cannot open weights");std::string line;req(bool(std::getline(f,line)),"empty weights");auto h=split(line,',');
  const std::vector<std::string> wanted={"pair_index","c","d","shift","odd_winner_numerator","odd_denominator","even_winner_numerator","even_denominator","pool_winner_numerator","pool_denominator","odd_class_prevalence","even_class_prevalence","pool_class_prevalence"};req(h==wanted,"weight header mismatch");
  Weights z;unsigned row=0;while(std::getline(f,line)){auto v=split(line,',');req(v.size()==h.size(),"weight row width");req(std::stoul(v[0])==row&&row<N,"pair index mismatch");z.odd[row]=std::stoull(v[4]);z.even[row]=std::stoull(v[6]);z.pool[row]=std::stoull(v[8]);auto a=std::stoull(v[5]),b=std::stoull(v[7]),c=std::stoull(v[9]);if(!row){z.do_=a;z.de=b;z.dp=c;}req(a==z.do_&&b==z.de&&c==z.dp,"denominator drift");++row;}req(row==N,"weight row count");req(z.do_==2334&&z.de==2337&&z.dp==4671,"unexpected fold denominator");return z;}
PMasks residue_centric(const std::vector<Pair>&pairs){PMasks out;for(unsigned q=0;q<4;++q){out[q].resize(MOD[q]);for(unsigned r=0;r<MOD[q];++r)for(unsigned i=0;i<N;++i){auto diff=(r+MOD[q]-unsigned(pairs[i].shift%MOD[q]))%MOD[q];if(diff%P[q]==0&&diff!=0)out[q][r].w[i/64]|=1ULL<<(i%64);}}return out;}
Mask uni(const Mask&a,const Mask&b){Mask r;for(unsigned j=0;j<W;++j)r.w[j]=a.w[j]|b.w[j];return r;}
unsigned pop(const Mask&m){unsigned n=0;for(auto x:m.w)n+=__builtin_popcountll(x);return n;}
Score accumulate_a(const Mask&m,const Weights&w){Score s;for(unsigned lane=0;lane<W;++lane){auto x=m.w[lane];while(x){unsigned b=__builtin_ctzll(x),i=64*lane+b;if(i<N){s.odd+=w.odd[i];s.even+=w.even[i];s.pool+=w.pool[i];}x&=x-1;}}return s;}
std::uint64_t pick(const Score&s,unsigned obj){return obj==0?s.odd:obj==1?s.even:s.pool;}
void enc16(std::uint8_t*p,std::uint16_t x){p[0]=x&255;p[1]=(x>>8)&255;} void enc64(std::uint8_t*p,std::uint64_t x){for(unsigned i=0;i<8;++i)p[i]=(x>>(8*i))&255;}
std::array<std::uint8_t,51> bytes(const Mask&m){std::array<std::uint8_t,51>b{};for(unsigned i=0;i<N;++i)if((m.w[i/64]>>(i%64))&1)b[i/8]|=1U<<(i%8);return b;}
std::string hexmask(const Mask&m){static const char*h="0123456789abcdef";auto b=bytes(m);std::string s;for(auto x:b){s.push_back(h[x>>4]);s.push_back(h[x&15]);}return s;}
void hash_row(Sha256Small&h,const Tup&t,const Mask&m,unsigned g,const Score&s){std::array<std::uint8_t,85>b{};for(unsigned i=0;i<4;++i)enc16(b.data()+2*i,t.x[i]);auto mb=bytes(m);std::copy(mb.begin(),mb.end(),b.begin()+8);enc16(b.data()+59,g);enc64(b.data()+61,s.odd);enc64(b.data()+69,s.even);enc64(b.data()+77,s.pool);h.update(b.data(),b.size());}
std::string tuple_text(const Tup&t){std::ostringstream o;o<<t.x[0]<<','<<t.x[1]<<','<<t.x[2]<<','<<t.x[3];return o.str();}
void update_best(Best&b,std::uint64_t v,const Tup&t,const Mask&m,const Score&s){if(!b.set||v>b.value){b={v,1,true,t,m,s,{t}};}else if(v==b.value){++b.count;b.args.push_back(t);}}
void update_top(std::vector<Candidate>&v,const Candidate&c){for(const auto&x:v)if(x.mask==c.mask)return;v.push_back(c);std::sort(v.begin(),v.end(),[](const auto&a,const auto&b){return a.value!=b.value?a.value>b.value:a.tuple<b.tuple;});if(v.size()>8)v.resize(8);}
std::string argdigest(const std::vector<Tup>&v){Sha256Small h;for(auto&t:v){std::uint8_t b[8];for(unsigned i=0;i<4;++i)enc16(b+2*i,t.x[i]);h.update(b,8);}return h.hex_digest();}
std::uint64_t rank_of(const std::map<std::uint64_t,std::uint64_t>&hist,std::uint64_t value){std::uint64_t r=1;for(auto it=hist.rbegin();it!=hist.rend()&&it->first>value;++it)r+=it->second;return r;}
Tup make_tup(unsigned a,unsigned b,unsigned c,unsigned d){return Tup{{std::uint16_t(a),std::uint16_t(b),std::uint16_t(c),std::uint16_t(d)}};}
void emit_obj(std::ofstream&o,const char*scope,const char*name,const Best&b,std::uint64_t den){o<<"objective\t"<<scope<<'\t'<<name<<'\t'<<den<<'\t'<<b.value<<'\t'<<b.count<<'\t'<<tuple_text(b.first)<<'\t'<<hexmask(b.mask)<<'\t'<<pop(b.mask)<<'\t'<<b.cross.odd<<'\t'<<b.cross.even<<'\t'<<b.cross.pool<<'\t'<<argdigest(b.args)<<'\n';}
int main_impl(int argc,char**argv){req(argc==3,"usage: enumerator weights.csv certificate.tsv");Sha256Small::self_test();auto pairs=domain(LOW);req(pairs.size()==N&&pairs==domain(HIGH),"domain mismatch");std::vector<std::pair<unsigned,unsigned>>dup;for(auto&p:pairs)if(p.shift==28)dup.push_back({p.c,p.d});req(dup==std::vector<std::pair<unsigned,unsigned>>{{1,2},{3,0}},"duplicate shift drift");auto w=read_weights(argv[1]);auto m=residue_centric(pairs);
  std::array<Best,3> full{},slice{};std::array<std::vector<Candidate>,3> top;std::array<std::map<std::uint64_t,std::uint64_t>,3> hist;Sha256Small ordered;std::uint64_t rows=0;
  std::vector<Target> targets;for(const auto&item:std::vector<std::pair<std::string,Tup>>{{"CAL-216",make_tup(2,41,74,504)},{"CAL-227",make_tup(2,41,50,504)},{"CAL-230",make_tup(2,7,32,504)},{"G231-COMMON",make_tup(2,7,50,17)}}){Target z;z.label=item.first;z.tuple=item.second;targets.push_back(z);}
  for(unsigned a=0;a<9;++a)for(unsigned b=0;b<49;++b)for(unsigned c=0;c<121;++c)for(unsigned d=0;d<529;++d){Tup t=make_tup(a,b,c,d);Mask x=uni(uni(m[0][a],m[1][b]),uni(m[2][c],m[3][d]));Score s=accumulate_a(x,w);unsigned g=pop(x);hash_row(ordered,t,x,g,s);++rows;
    for(unsigned q=0;q<3;++q){auto v=pick(s,q);++hist[q][v];update_best(full[q],v,t,x,s);update_top(top[q],{v,t,x,g,s});if(a==2)update_best(slice[q],v,t,x,s);}for(auto&z:targets)if(t.x==z.tuple.x){z.mask=x;z.g=g;z.score=s;}}
  req(rows==ROWS,"row count mismatch");
  std::set<Mask> candidate_masks;for(auto&v:top)for(auto&x:v)candidate_masks.insert(x.mask);for(auto&z:targets)candidate_masks.insert(z.mask);std::map<Mask,Tup> slice_reps;
  for(unsigned b=0;b<49;++b)for(unsigned c=0;c<121;++c)for(unsigned d=0;d<529;++d){Tup t=make_tup(2,b,c,d);Mask x=uni(uni(m[0][2],m[1][b]),uni(m[2][c],m[3][d]));if(candidate_masks.count(x)&&!slice_reps.count(x))slice_reps[x]=t;}
  std::ofstream o(argv[2]);req(bool(o),"cannot write certificate");o<<"schema\ta303656-weighted-enumerator-certificate-v1\nimplementation\tA-residue-centric-ctz-accumulation\nrows\t"<<rows<<"\nordered_result_digest\t"<<ordered.hex_digest()<<"\n";
  const char*names[3]={"odd","even","pool"};std::uint64_t den[3]={w.do_,w.de,w.dp};for(unsigned q=0;q<3;++q){emit_obj(o,"full",names[q],full[q],den[q]);emit_obj(o,"t3eq2",names[q],slice[q],den[q]);}
  for(unsigned q=0;q<3;++q)for(unsigned i=0;i<top[q].size();++i){auto&x=top[q][i];o<<"top\t"<<names[q]<<'\t'<<i+1<<'\t'<<tuple_text(x.tuple)<<'\t'<<hexmask(x.mask)<<'\t'<<x.g<<'\t'<<x.score.odd<<'\t'<<x.score.even<<'\t'<<x.score.pool<<'\t';auto it=slice_reps.find(x.mask);o<<(it==slice_reps.end()?"NONE":tuple_text(it->second))<<'\n';}
  for(auto&z:targets)o<<"target\t"<<z.label<<'\t'<<tuple_text(z.tuple)<<'\t'<<hexmask(z.mask)<<'\t'<<z.g<<'\t'<<z.score.odd<<'\t'<<rank_of(hist[0],z.score.odd)<<'\t'<<z.score.even<<'\t'<<rank_of(hist[1],z.score.even)<<'\t'<<z.score.pool<<'\t'<<rank_of(hist[2],z.score.pool)<<'\t'<<tuple_text(slice_reps.at(z.mask))<<'\n';
  for(unsigned q=0;q<3;++q)o<<"cross\t"<<names[q]<<"_opt\t"<<full[q].cross.odd<<'\t'<<rank_of(hist[0],full[q].cross.odd)<<'\t'<<full[q].cross.even<<'\t'<<rank_of(hist[1],full[q].cross.even)<<'\t'<<full[q].cross.pool<<'\t'<<rank_of(hist[2],full[q].cross.pool)<<'\n';
  return 0;}
}
int main(int argc,char**argv){try{return main_impl(argc,argv);}catch(const std::exception&e){std::cerr<<"weighted_enumerator_a: ERROR: "<<e.what()<<'\n';return 2;}}
