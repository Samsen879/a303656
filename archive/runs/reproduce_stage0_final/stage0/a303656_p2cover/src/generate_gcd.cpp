// Generate G_B = gcd(prod_{k<=B}(3^k-1), prod_{k<=B}(5^k-1)) in hexadecimal.
#include <gmpxx.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

static mpz_class product_range(unsigned base, unsigned lo, unsigned hi) {
    if (lo > hi) return 1;
    if (lo == hi) {
        mpz_class x;
        mpz_ui_pow_ui(x.get_mpz_t(), base, lo);
        return x - 1;
    }
    unsigned mid = lo + (hi - lo) / 2;
    return product_range(base, lo, mid) * product_range(base, mid + 1, hi);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: generate_gcd B OUTPUT_HEX\n";
        return 2;
    }
    unsigned B = std::stoul(argv[1]);
    auto started = std::chrono::steady_clock::now();
    mpz_class A = product_range(3, 1, B);
    mpz_class C = product_range(5, 1, B);
    mpz_class G;
    mpz_gcd(G.get_mpz_t(), A.get_mpz_t(), C.get_mpz_t());
    FILE* out = std::fopen(argv[2], "w");
    if (!out) throw std::runtime_error("cannot open output");
    mpz_out_str(out, 16, G.get_mpz_t());
    std::fputc('\n', out);
    std::fclose(out);
    std::cerr << "B=" << B
              << " A_bits=" << mpz_sizeinbase(A.get_mpz_t(), 2)
              << " C_bits=" << mpz_sizeinbase(C.get_mpz_t(), 2)
              << " G_bits=" << mpz_sizeinbase(G.get_mpz_t(), 2)
              << " seconds=" << std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count()
              << "\n";
}
