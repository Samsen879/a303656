#include <gmpxx.h>
#include <fstream>
#include <iostream>
#include <chrono>
int main(int argc,char**argv){
 if(argc!=3)return 2; std::ifstream f(argv[1]);mpz_class N;f>>N;
 unsigned long lim=std::stoul(argv[2]); unsigned long count=0;
 auto t=std::chrono::steady_clock::now();
 for(unsigned long q=1807;q<=lim;q+=1806){++count;if(mpz_divisible_ui_p(N.get_mpz_t(),q)){int e=0;do{mpz_divexact_ui(N.get_mpz_t(),N.get_mpz_t(),q);++e;}while(mpz_divisible_ui_p(N.get_mpz_t(),q));std::cout<<"FACTOR "<<q<<" "<<e<<"\n";}}
 std::cout<<"BOUND "<<lim<<" COUNT "<<count<<" COFACTOR "<<N<<" SECONDS "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-t).count()<<"\n";
}
