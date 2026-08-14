#include <gmpxx.h>
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using u64 = std::uint64_t;
using u128 = __uint128_t;

struct Factor { u64 p; unsigned e; };
struct Row {
    u64 p, r, s, r2, s2, maxfiber;
    mpq_class alpha;
    mpq_class loose;
};

static u64 mul_mod(u64 a, u64 b, u64 m) {
    return static_cast<u64>((static_cast<u128>(a) * b) % m);
}

static u64 pow_mod(u64 a, u64 e, u64 m) {
    u64 out = 1 % m;
    while (e) {
        if (e & 1) out = mul_mod(out, a, m);
        a = mul_mod(a, a, m);
        e >>= 1;
    }
    return out;
}

static bool is_prime_trial(u64 n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (u64 q = 3; q * q <= n; q += 2) {
        if (n % q == 0) return false;
    }
    return true;
}

static std::vector<u64> distinct_prime_factors(u64 n) {
    std::vector<u64> f;
    if (n % 2 == 0) {
        f.push_back(2);
        while (n % 2 == 0) n /= 2;
    }
    for (u64 q = 3; q * q <= n; q += 2) {
        if (n % q == 0) {
            f.push_back(q);
            while (n % q == 0) n /= q;
        }
    }
    if (n > 1) f.push_back(n);
    return f;
}

static u64 order_mod_prime(u64 a, u64 p) {
    u64 ord = p - 1;
    for (u64 q : distinct_prime_factors(p - 1)) {
        while (ord % q == 0 && pow_mod(a, ord / q, p) == 1) ord /= q;
    }
    return ord;
}

static mpz_class product_range(unsigned base, unsigned lo, unsigned hi) {
    if (lo > hi) return 1;
    if (lo == hi) {
        mpz_class x;
        mpz_ui_pow_ui(x.get_mpz_t(), base, lo);
        return x - 1;
    }
    const unsigned mid = lo + (hi - lo) / 2;
    return product_range(base, lo, mid) * product_range(base, mid + 1, hi);
}

static std::vector<Factor> read_certificate(const std::string& path, unsigned& B) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("cannot open factorization certificate: " + path);
    std::string tag;
    if (!(in >> tag >> B) || tag != "B") throw std::runtime_error("bad certificate header");
    std::vector<Factor> fs;
    u64 p; unsigned e;
    while (in >> p >> e) fs.push_back({p, e});
    if (fs.empty()) throw std::runtime_error("empty factorization");
    return fs;
}

static Row compute_row(u64 p, std::vector<std::uint16_t>& counts) {
    const u64 r = order_mod_prime(3, p);
    const u64 s = order_mod_prime(5, p);
    const u64 pp = p * p;
    const u64 r2 = (pow_mod(3, r, pp) == 1 ? r : p * r);
    const u64 s2 = (pow_mod(5, s, pp) == 1 ? s : p * s);

    std::vector<u64> a(r), b(s);
    u64 x = 1;
    for (u64 i = 0; i < r; ++i) { a[i] = x; x = (x * 3) % p; }
    x = 1;
    for (u64 j = 0; j < s; ++j) { b[j] = x; x = (x * 5) % p; }

    std::vector<u64> touched;
    touched.reserve(static_cast<std::size_t>(std::min<u64>(p, r * s)));
    u64 maxfiber = 0;
    for (u64 av : a) {
        for (u64 bv : b) {
            u64 z = av + bv;
            if (z >= p) z -= p;
            auto& c = counts[z];
            if (c == 0) touched.push_back(z);
            ++c;
            if (c > maxfiber) maxfiber = c;
        }
    }
    for (u64 z : touched) counts[z] = 0;

    mpq_class alpha(mpz_class(maxfiber), mpz_class(r * s));
    alpha.canonicalize();
    mpq_class loose(1, static_cast<unsigned long>(std::max(r, s)));
    loose.canonicalize();
    return {p, r, s, r2, s2, maxfiber, alpha, loose};
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) {
            std::cerr << "usage: verify_pruning FACTORIZATION_CERT OUTPUT_CSV\n";
            return 2;
        }
        const auto started = std::chrono::steady_clock::now();
        unsigned B = 0;
        auto fs = read_certificate(argv[1], B);

        u64 previous = 0;
        mpz_class factored = 1;
        for (const auto& f : fs) {
            if (f.p <= previous || f.e == 0) throw std::runtime_error("factors not strictly increasing / zero exponent");
            if (!is_prime_trial(f.p)) throw std::runtime_error("composite listed as prime: " + std::to_string(f.p));
            previous = f.p;
            mpz_class pe;
            mpz_ui_pow_ui(pe.get_mpz_t(), f.p, f.e);
            factored *= pe;
        }

        mpz_class A = product_range(3, 1, B);
        mpz_class C = product_range(5, 1, B);
        mpz_class G;
        mpz_gcd(G.get_mpz_t(), A.get_mpz_t(), C.get_mpz_t());
        if (G != factored) throw std::runtime_error("factorization product does not equal gcd product");

        std::vector<u64> target;
        for (const auto& f : fs) {
            if (f.p % 4 == 3 && f.p != 3 && f.p != 5) target.push_back(f.p);
        }
        const u64 maxp = *std::max_element(target.begin(), target.end());
        std::vector<std::uint16_t> counts(maxp + 1, 0);
        std::vector<Row> rows;
        rows.reserve(target.size());
        for (u64 p : target) {
            Row row = compute_row(p, counts);
            if (std::max(row.r, row.s) > B) throw std::runtime_error("factor has order above B");
            rows.push_back(std::move(row));
        }

        mpq_class sum_alpha(0), sum_loose(0), strong_sum(0);
        const mpq_class outside_cap(1, B + 1);
        std::size_t strong_count = 0;
        for (const auto& row : rows) {
            sum_alpha += row.alpha;
            sum_loose += row.loose;
            if (row.alpha > outside_cap) {
                ++strong_count;
                strong_sum += row.alpha;
            }
        }
        sum_alpha.canonicalize();
        sum_loose.canonicalize();
        strong_sum.canonicalize();

        if (!(sum_alpha < 1)) throw std::runtime_error("expected exact local-capacity sum < 1");

        std::vector<mpq_class> loose_terms;
        loose_terms.reserve(rows.size());
        for (const auto& row : rows) loose_terms.push_back(row.loose);
        std::sort(loose_terms.begin(), loose_terms.end(), [](const mpq_class& a, const mpq_class& b) { return a > b; });
        mpq_class top65_loose(0), top66_loose(0);
        for (std::size_t i = 0; i < 66; ++i) {
            top66_loose += loose_terms[i];
            if (i < 65) top65_loose += loose_terms[i];
        }
        if (!(top65_loose < 1)) throw std::runtime_error("top-65 loose-capacity check failed");
        if (!(top66_loose >= 1)) throw std::runtime_error("top-66 loose-capacity threshold check failed");

        if (strong_count != 388) throw std::runtime_error("unexpected count alpha > 1/(B+1)");
        const mpq_class bound597 = strong_sum + mpq_class(209, B + 1);
        const mpq_class bound598 = strong_sum + mpq_class(210, B + 1);
        if (!(bound597 < 1)) throw std::runtime_error("597-prime lower-bound inequality failed");
        if (!(bound598 >= 1)) throw std::runtime_error("598 threshold check failed");
        mpq_class high_needed_q = (1 - sum_alpha) * (B + 1);
        high_needed_q.canonicalize();
        mpz_class high_needed;
        mpz_cdiv_q(high_needed.get_mpz_t(), high_needed_q.get_num_mpz_t(), high_needed_q.get_den_mpz_t());
        if (high_needed != 135) throw std::runtime_error("unexpected minimum count of >B-order primes");

        std::ofstream out(argv[2]);
        if (!out) throw std::runtime_error("cannot open output CSV");
        out << "p,ord_p_3,ord_p_5,ord_p2_3,ord_p2_5,weight_1_over_max,maxfiber,alpha_exact\n";
        for (const auto& row : rows) {
            out << row.p << ',' << row.r << ',' << row.s << ',' << row.r2 << ',' << row.s2 << ','
                << row.loose.get_num() << '/' << row.loose.get_den() << ',' << row.maxfiber << ','
                << row.alpha.get_num() << '/' << row.alpha.get_den() << '\n';
        }

        const double seconds = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
        std::cout << "VERIFIED\n";
        std::cout << "B=" << B << "\n";
        std::cout << "gcd_bits=" << mpz_sizeinbase(G.get_mpz_t(), 2) << "\n";
        std::cout << "factor_count_all=" << fs.size() << "\n";
        std::cout << "eligible_prime_count=" << rows.size() << "\n";
        std::cout << "eligible_prime_max=" << maxp << "\n";
        std::cout << std::setprecision(17);
        std::cout << "sum_loose_decimal=" << sum_loose.get_d() << "\n";
        std::cout << "top65_loose_decimal=" << top65_loose.get_d() << "\n";
        std::cout << "top66_loose_decimal=" << top66_loose.get_d() << "\n";
        std::cout << "loose_bound_cardinality_lower_bound=66\n";
        std::cout << "sum_exact_alpha_decimal=" << sum_alpha.get_d() << "\n";
        std::cout << "alpha_above_1_over_5001_count=" << strong_count << "\n";
        std::cout << "alpha_above_1_over_5001_sum_decimal=" << strong_sum.get_d() << "\n";
        std::cout << "upper_capacity_597_primes_decimal=" << bound597.get_d() << "\n";
        std::cout << "upper_capacity_598_primes_decimal=" << bound598.get_d() << "\n";
        std::cout << "minimum_primes_with_max_order_above_B=" << high_needed << "\n";
        std::cout << "cardinality_lower_bound=598\n";
        std::cout << "elapsed_seconds=" << seconds << "\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "VERIFICATION FAILED: " << e.what() << '\n';
        return 1;
    }
}
