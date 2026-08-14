// Independent exact C++/GMP verifier for bounded A303656 valuation-one certificates.
//
// This program does not call Z3, CP-SAT, MILP, or any search implementation.
// It independently enumerates all powers and all exponent pairs with
// 3^c+5^d <= n, rejects remainder zero, and checks exact divisibility by p
// but not p^2.  Candidate n and remainders use GMP integers.  Obstruction
// primes are accepted throughout the full uint64 range and are checked by a
// deterministic 64-bit Miller--Rabin test.
#include <gmpxx.h>

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct PairShift {
    int c;
    int d;
    mpz_class shift;
};

static uint64_t mul_mod_u64(uint64_t a, uint64_t b, uint64_t mod) {
    return static_cast<uint64_t>((static_cast<__uint128_t>(a) * b) % mod);
}

static uint64_t pow_mod_u64(uint64_t base, uint64_t exponent, uint64_t mod) {
    uint64_t result = 1 % mod;
    uint64_t value = base % mod;
    while (exponent != 0) {
        if (exponent & 1U) result = mul_mod_u64(result, value, mod);
        exponent >>= 1U;
        if (exponent != 0) value = mul_mod_u64(value, value, mod);
    }
    return result;
}

static bool is_prime_u64(uint64_t n) {
    if (n < 2) return false;
    for (uint64_t p : {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 19ULL, 23ULL, 29ULL, 31ULL, 37ULL}) {
        if (n % p == 0) return n == p;
    }
    uint64_t d = n - 1;
    unsigned s = 0;
    while ((d & 1U) == 0U) {
        d >>= 1U;
        ++s;
    }
    // This base set is deterministic for all unsigned 64-bit integers.
    for (uint64_t a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL, 1795265022ULL}) {
        if (a % n == 0) continue;
        uint64_t x = pow_mod_u64(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool witness = true;
        for (unsigned r = 1; r < s; ++r) {
            x = mul_mod_u64(x, x, n);
            if (x == n - 1) {
                witness = false;
                break;
            }
        }
        if (witness) return false;
    }
    return true;
}

static mpz_class mpz_from_u64(uint64_t value) {
    return mpz_class(std::to_string(value));
}

static std::vector<uint64_t> parse_primes(const std::string& text) {
    std::string raw;
    std::ifstream maybe(text);
    if (maybe.good()) {
        std::ostringstream stream;
        stream << maybe.rdbuf();
        raw = stream.str();
    } else {
        raw = text;
    }
    for (char& ch : raw) {
        if (ch == '\n' || ch == '\r' || std::isspace(static_cast<unsigned char>(ch))) ch = ',';
    }
    std::vector<uint64_t> primes;
    std::stringstream stream(raw);
    std::string item;
    while (std::getline(stream, item, ',')) {
        if (item.empty()) continue;
        size_t used = 0;
        uint64_t p = std::stoull(item, &used);
        if (used != item.size()) throw std::runtime_error("invalid prime token: " + item);
        primes.push_back(p);
    }
    if (primes.empty()) throw std::runtime_error("prime pool is empty");
    std::set<uint64_t> seen;
    for (uint64_t p : primes) {
        if (!seen.insert(p).second) throw std::runtime_error("duplicate prime: " + std::to_string(p));
        if (!is_prime_u64(p)) throw std::runtime_error("non-prime in pool: " + std::to_string(p));
        if (p % 4 != 3) throw std::runtime_error("prime not 3 mod 4: " + std::to_string(p));
    }
    std::sort(primes.begin(), primes.end());
    return primes;
}

static std::map<std::pair<int, int>, uint64_t> load_assignment(const std::string& path) {
    std::ifstream file(path);
    if (!file) throw std::runtime_error("cannot open assignment CSV");
    std::string header;
    if (!std::getline(file, header)) throw std::runtime_error("empty assignment CSV");
    std::vector<std::string> columns;
    {
        std::stringstream stream(header);
        std::string value;
        while (std::getline(stream, value, ',')) columns.push_back(value);
    }
    int c_index = -1;
    int d_index = -1;
    int p_index = -1;
    for (int i = 0; i < static_cast<int>(columns.size()); ++i) {
        if (columns[i] == "c") c_index = i;
        else if (columns[i] == "d") d_index = i;
        else if (columns[i] == "prime") p_index = i;
    }
    if (c_index < 0 || d_index < 0 || p_index < 0) {
        throw std::runtime_error("assignment CSV needs c,d,prime columns");
    }
    std::map<std::pair<int, int>, uint64_t> assignment;
    std::string line;
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        std::vector<std::string> fields;
        std::stringstream stream(line);
        std::string value;
        while (std::getline(stream, value, ',')) fields.push_back(value);
        if (static_cast<int>(fields.size()) <= std::max({c_index, d_index, p_index})) {
            throw std::runtime_error("short assignment CSV row");
        }
        int c = std::stoi(fields[c_index]);
        int d = std::stoi(fields[d_index]);
        uint64_t p = std::stoull(fields[p_index]);
        if (!assignment.emplace(std::make_pair(c, d), p).second) {
            throw std::runtime_error("duplicate assignment pair");
        }
    }
    return assignment;
}

static std::vector<mpz_class> exact_powers(unsigned base, const mpz_class& limit) {
    std::vector<mpz_class> values;
    mpz_class value = 1;
    while (value <= limit) {
        values.push_back(value);
        value *= base;
    }
    return values;
}

static bool exact_one_obstruction(const mpz_class& remainder, uint64_t p) {
    if (remainder <= 0) return false;
    const mpz_class prime = mpz_from_u64(p);
    if (!mpz_divisible_p(remainder.get_mpz_t(), prime.get_mpz_t())) return false;
    const mpz_class square = prime * prime;
    return !mpz_divisible_p(remainder.get_mpz_t(), square.get_mpz_t());
}

static int exact_valuation(const mpz_class& input, uint64_t p) {
    if (input <= 0) return -1;
    const mpz_class prime = mpz_from_u64(p);
    mpz_class remainder = input;
    int exponent = 0;
    while (mpz_divisible_p(remainder.get_mpz_t(), prime.get_mpz_t())) {
        mpz_divexact(remainder.get_mpz_t(), remainder.get_mpz_t(), prime.get_mpz_t());
        ++exponent;
    }
    return exponent;
}

static mpz_class integer_power(unsigned base, int exponent) {
    if (exponent < 0) throw std::runtime_error("negative exponent");
    mpz_class value;
    mpz_ui_pow_ui(value.get_mpz_t(), base, static_cast<unsigned long>(exponent));
    return value;
}

int main(int argc, char** argv) {
    try {
        std::string n_text;
        std::string prime_text;
        std::string assignment_path;
        std::string output_csv;
        std::string interval_low_text;
        std::string interval_high_text;
        int declared_C = -1;
        int declared_D = -1;
        bool quiet_pairs = false;

        for (int i = 1; i < argc; ++i) {
            const std::string argument = argv[i];
            auto value = [&](const char* name) -> std::string {
                if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + name);
                return argv[++i];
            };
            if (argument == "--n") n_text = value("--n");
            else if (argument == "--primes") prime_text = value("--primes");
            else if (argument == "--assignment") assignment_path = value("--assignment");
            else if (argument == "--out-csv") output_csv = value("--out-csv");
            else if (argument == "--interval-low") interval_low_text = value("--interval-low");
            else if (argument == "--interval-high") interval_high_text = value("--interval-high");
            else if (argument == "--C") declared_C = std::stoi(value("--C"));
            else if (argument == "--D") declared_D = std::stoi(value("--D"));
            else if (argument == "--quiet-pairs") quiet_pairs = true;
            else throw std::runtime_error("unknown argument: " + argument);
        }
        if (n_text.empty() || prime_text.empty()) {
            throw std::runtime_error("usage: --n N --primes LIST [--assignment CSV]");
        }
        if (interval_low_text.empty() != interval_high_text.empty()) {
            throw std::runtime_error("--interval-low and --interval-high must be supplied together");
        }
        if ((declared_C < 0) != (declared_D < 0)) {
            throw std::runtime_error("--C and --D must be supplied together");
        }

        const mpz_class n(n_text);
        const std::vector<uint64_t> primes = parse_primes(prime_text);
        const std::set<uint64_t> prime_set(primes.begin(), primes.end());
        const bool has_assignment = !assignment_path.empty();
        std::map<std::pair<int, int>, uint64_t> assignment;
        if (has_assignment) {
            assignment = load_assignment(assignment_path);
            for (const auto& item : assignment) {
                if (!prime_set.count(item.second)) {
                    throw std::runtime_error("assignment uses prime outside P");
                }
            }
        }

        int configuration_errors = 0;
        if (n <= 1) ++configuration_errors;
        if (!interval_low_text.empty()) {
            const mpz_class interval_low(interval_low_text);
            const mpz_class interval_high(interval_high_text);
            if (interval_low > interval_high || n < interval_low || n > interval_high) ++configuration_errors;
            if (declared_C >= 0) {
                const mpz_class bound3 = integer_power(3, declared_C + 1) + 1;
                const mpz_class bound5 = integer_power(5, declared_D + 1) + 1;
                if (!(interval_high < bound3) || !(interval_high < bound5)) ++configuration_errors;
            }
        } else if (declared_C >= 0) {
            const mpz_class bound3 = integer_power(3, declared_C + 1) + 1;
            const mpz_class bound5 = integer_power(5, declared_D + 1) + 1;
            if (!(n < bound3) || !(n < bound5)) ++configuration_errors;
        }

        const std::vector<mpz_class> powers3 = exact_powers(3, n);
        const std::vector<mpz_class> powers5 = exact_powers(5, n);
        if (declared_C >= 0) {
            if (static_cast<int>(powers3.size()) - 1 > declared_C) ++configuration_errors;
            if (static_cast<int>(powers5.size()) - 1 > declared_D) ++configuration_errors;
        }

        std::vector<PairShift> pairs;
        for (int c = 0; c < static_cast<int>(powers3.size()); ++c) {
            for (int d = 0; d < static_cast<int>(powers5.size()); ++d) {
                const mpz_class shift = powers3[c] + powers5[d];
                if (shift > n) break;
                pairs.push_back({c, d, shift});
            }
        }
        std::set<std::pair<int, int>> pair_keys;
        std::set<std::string> distinct_shifts;
        for (const PairShift& pair : pairs) {
            pair_keys.insert({pair.c, pair.d});
            distinct_shifts.insert(pair.shift.get_str());
        }

        int assignment_missing = 0;
        int assignment_extra = 0;
        if (has_assignment) {
            for (const auto& key : pair_keys) if (!assignment.count(key)) ++assignment_missing;
            for (const auto& item : assignment) if (!pair_keys.count(item.first)) ++assignment_extra;
        }

        std::ofstream csv;
        if (!output_csv.empty()) {
            csv.open(output_csv);
            if (!csv) throw std::runtime_error("cannot open output CSV");
            csv << "c,d,shift,remainder,prime,valuation\n";
        }

        int uncovered = 0;
        int zero_remainders = 0;
        for (const PairShift& pair : pairs) {
            const mpz_class remainder = n - pair.shift;
            if (remainder == 0) ++zero_remainders;
            uint64_t chosen = 0;
            int chosen_valuation = -1;
            if (has_assignment) {
                const auto found = assignment.find({pair.c, pair.d});
                if (found != assignment.end() && exact_one_obstruction(remainder, found->second)) {
                    chosen = found->second;
                    chosen_valuation = exact_valuation(remainder, chosen);
                }
            } else {
                for (uint64_t p : primes) {
                    if (exact_one_obstruction(remainder, p)) {
                        chosen = p;
                        chosen_valuation = exact_valuation(remainder, p);
                        break;
                    }
                }
            }
            if (chosen == 0) ++uncovered;
            if (!quiet_pairs) {
                std::cout << "PAIR c=" << pair.c << " d=" << pair.d
                          << " s=" << pair.shift << " r=" << remainder;
                if (chosen != 0) {
                    std::cout << " p=" << chosen << " valuation=" << chosen_valuation << '\n';
                } else {
                    std::cout << " obstruction=NONE\n";
                }
            }
            if (csv) {
                csv << pair.c << ',' << pair.d << ',' << pair.shift << ',' << remainder << ',';
                if (chosen != 0) csv << chosen << ',' << chosen_valuation;
                else csv << ',';
                csv << '\n';
            }
        }

        const bool passed = configuration_errors == 0 && uncovered == 0 && zero_remainders == 0
                            && assignment_missing == 0 && assignment_extra == 0;
        std::cout << "candidate_n=" << n << '\n';
        std::cout << "prime_count=" << primes.size() << '\n';
        std::cout << "max_c=" << (powers3.empty() ? -1 : static_cast<int>(powers3.size()) - 1) << '\n';
        std::cout << "max_d=" << (powers5.empty() ? -1 : static_cast<int>(powers5.size()) - 1) << '\n';
        std::cout << "admissible_pair_count=" << pairs.size() << '\n';
        std::cout << "distinct_shift_count=" << distinct_shifts.size() << '\n';
        std::cout << "zero_remainder_count=" << zero_remainders << '\n';
        std::cout << "uncovered_pair_count=" << uncovered << '\n';
        std::cout << "assignment_missing_count=" << assignment_missing << '\n';
        std::cout << "assignment_extra_count=" << assignment_extra << '\n';
        std::cout << "configuration_error_count=" << configuration_errors << '\n';
        std::cout << (passed ? "PASS" : "FAIL") << '\n';
        return passed ? 0 : 1;
    } catch (const std::exception& error) {
        std::cerr << "FAIL verifier_exception=" << error.what() << '\n';
        return 2;
    }
}
