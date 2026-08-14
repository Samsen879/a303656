// Clean-room independent exact scanner for the unrestricted valuation-one
// certificate family.  This implementation intentionally does not share the
// packed-bit machinery or helper code of search_all_exact_one.cpp.  It uses a
// byte classification array and compacts an explicit vector of surviving
// offsets after each translated shift condition.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

static uint64_t floor_root(uint64_t x) {
    uint64_t a = 0, b = (x < (uint64_t(1) << 32) ? x : (uint64_t(1) << 32));
    while (a < b) {
        uint64_t m = a + (b - a + 1) / 2;
        if (m != 0 && m <= x / m) a = m; else b = m - 1;
    }
    return a;
}

static std::vector<uint32_t> make_primes(uint64_t limit64) {
    if (limit64 > std::numeric_limits<uint32_t>::max()) throw std::runtime_error("prime limit too large");
    uint32_t limit = static_cast<uint32_t>(limit64);
    std::vector<uint8_t> composite(static_cast<size_t>(limit) + 1, 0);
    std::vector<uint32_t> out;
    for (uint32_t x = 2; x <= limit; ++x) {
        if (composite[x]) continue;
        out.push_back(x);
        if (uint64_t(x) * x <= limit) {
            uint64_t y = uint64_t(x) * x;
            while (y <= limit) {
                composite[static_cast<size_t>(y)] = 1;
                y += x;
            }
        }
    }
    return out;
}

static uint64_t power_u64(uint64_t b, int e) {
    uint64_t x = 1;
    for (int i = 0; i < e; ++i) {
        if (x > std::numeric_limits<uint64_t>::max() / b) throw std::runtime_error("power overflow");
        x *= b;
    }
    return x;
}

struct Counters {
    uint64_t progression_visits = 0;
    uint64_t residual_divisions = 0;
    uint64_t small_marks = 0;
    uint64_t residual_marks = 0;
    uint64_t prefix_tests = 0;
    uint64_t full_tests = 0;
};

static std::vector<uint8_t> classify(uint64_t lo, uint64_t hi,
                                     const std::vector<uint32_t>& primes,
                                     Counters& count) {
    if (lo > hi) throw std::runtime_error("bad factor interval");
    uint64_t width64 = hi - lo + 1;
    if (width64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("width overflow");
    size_t width = static_cast<size_t>(width64);
    std::vector<uint64_t> rest(width);
    std::vector<uint8_t> good(width, 0);
    for (size_t i = 0; i < width; ++i) rest[i] = lo + static_cast<uint64_t>(i);
    if (lo == 0) rest[0] = 1; // zero remainder is deliberately never marked.

    uint64_t root = floor_root(hi);
    for (uint32_t pp : primes) {
        uint64_t p = pp;
        if (p > root) break;
        uint64_t multiplier = lo / p;
        if (lo % p) ++multiplier;
        if (multiplier == 0) multiplier = 1; // do not factor the integer 0
        if (multiplier > hi / p) continue;
        uint64_t value = multiplier * p;
        while (value <= hi) {
            ++count.progression_visits;
            size_t i = static_cast<size_t>(value - lo);
            if (!good[i]) {
                // multiplier == value/p, so multiplier mod p detects p^2.
                if ((p % 4) == 3 && (multiplier % p) != 0) {
                    good[i] = 1;
                    ++count.small_marks;
                } else {
                    // This p-factor is still present: earlier loops only removed
                    // distinct smaller primes.
                    rest[i] /= p;
                    ++count.residual_divisions;
                    while (rest[i] % p == 0) {
                        rest[i] /= p;
                        ++count.residual_divisions;
                    }
                }
            }
            if (hi - value < p) break;
            value += p;
            ++multiplier;
        }
    }
    for (size_t i = 0; i < width; ++i) {
        if (!good[i] && rest[i] > 1 && rest[i] % 4 == 3) {
            good[i] = 1;
            ++count.residual_marks;
        }
    }
    return good;
}

static uint64_t obstruction(uint64_t r, const std::vector<uint32_t>& primes) {
    if (r == 0) return 0;
    uint64_t x = r;
    for (uint32_t pp : primes) {
        uint64_t p = pp;
        if (p > x / p) break;
        if (x % p) continue;
        unsigned e = 0;
        do { x /= p; ++e; } while (x % p == 0);
        if (p % 4 == 3 && e == 1) return p;
    }
    return (x > 1 && x % 4 == 3) ? x : 0;
}

struct Options {
    uint64_t low = 0, high = 0, block = 10000000;
    int C = -1, D = -1;
    size_t prefix = 100;
    std::string json, candidates;
    bool quiet = false;
};

static Options options(int argc, char** argv) {
    Options o;
    for (int i = 1; i < argc; ++i) {
        std::string k = argv[i];
        auto v = [&]() -> std::string {
            if (++i >= argc) throw std::runtime_error("missing command-line value");
            return argv[i];
        };
        if (k == "--low") o.low = std::stoull(v());
        else if (k == "--high") o.high = std::stoull(v());
        else if (k == "--C") o.C = std::stoi(v());
        else if (k == "--D") o.D = std::stoi(v());
        else if (k == "--window") o.block = std::stoull(v());
        else if (k == "--prefix-shifts") o.prefix = static_cast<size_t>(std::stoull(v()));
        else if (k == "--json") o.json = v();
        else if (k == "--candidates") o.candidates = v();
        else if (k == "--quiet") o.quiet = true;
        else throw std::runtime_error("unknown option: " + k);
    }
    if (!o.low || !o.high || o.low > o.high || o.C < 0 || o.D < 0 || !o.block || !o.prefix || o.json.empty()) {
        throw std::runtime_error("missing/invalid required options");
    }
    return o;
}

int main(int argc, char** argv) {
    try {
        Options o = options(argc, argv);
        uint64_t cap3 = power_u64(3, o.C + 1) + 1;
        uint64_t cap5 = power_u64(5, o.D + 1) + 1;
        if (o.high >= cap3 || o.high >= cap5) throw std::runtime_error("finite exponent inequalities fail");

        std::vector<uint64_t> threes(static_cast<size_t>(o.C + 1), 1);
        std::vector<uint64_t> fives(static_cast<size_t>(o.D + 1), 1);
        for (int i = 1; i <= o.C; ++i) threes[static_cast<size_t>(i)] = threes[static_cast<size_t>(i - 1)] * 3;
        for (int i = 1; i <= o.D; ++i) fives[static_cast<size_t>(i)] = fives[static_cast<size_t>(i - 1)] * 5;
        std::map<uint64_t, unsigned> multiplicity;
        for (uint64_t x : threes) for (uint64_t y : fives) {
            if (x <= o.high && y <= o.high - x) ++multiplicity[x + y];
        }
        std::vector<uint64_t> shifts;
        size_t pairs = 0;
        for (auto entry : multiplicity) { shifts.push_back(entry.first); pairs += entry.second; }
        uint64_t root = floor_root(o.high - shifts.front());
        std::vector<uint32_t> primes = make_primes(root);

        std::ofstream cand;
        if (!o.candidates.empty()) {
            cand.open(o.candidates);
            if (!cand) throw std::runtime_error("cannot open candidate output");
        }
        Counters counter;
        uint64_t integers = 0, blocks = 0, boundary_splits = 0, prefix_survivors = 0;
        size_t max_prefix = 0;
        std::vector<uint64_t> answers;
        auto begin = std::chrono::steady_clock::now();

        uint64_t left = o.low;
        while (left <= o.high) {
            uint64_t right = o.high;
            if (o.block - 1 <= o.high - left) right = std::min(right, left + o.block - 1);
            auto next = std::upper_bound(shifts.begin(), shifts.end(), left);
            if (next != shifts.end() && *next <= right) { right = *next - 1; ++boundary_splits; }
            size_t active = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), left) - shifts.begin());
            size_t use = std::min(o.prefix, active);
            max_prefix = std::max(max_prefix, use);
            uint64_t width64 = right - left + 1;
            size_t width = static_cast<size_t>(width64);
            integers += width64;
            ++blocks;

            std::vector<uint32_t> live(width);
            for (size_t i = 0; i < width; ++i) live[i] = static_cast<uint32_t>(i);
            if (use != 0) {
                uint64_t biggest = shifts[use - 1];
                uint64_t A = left - biggest;
                uint64_t B = right - shifts.front();
                std::vector<uint8_t> good = classify(A, B, primes, counter);
                for (size_t si = 0; si < use && !live.empty(); ++si) {
                    size_t write = 0;
                    uint64_t shift = shifts[si];
                    for (uint32_t offset : live) {
                        ++counter.prefix_tests;
                        uint64_t r = (left + offset) - shift;
                        if (good[static_cast<size_t>(r - A)]) live[write++] = offset;
                    }
                    live.resize(write);
                }
            }
            prefix_survivors += live.size();
            for (uint32_t off : live) {
                uint64_t n = left + off;
                size_t nactive = static_cast<size_t>(std::upper_bound(shifts.begin(), shifts.end(), n) - shifts.begin());
                bool pass = true;
                for (size_t si = 0; si < nactive; ++si) {
                    ++counter.full_tests;
                    if (!obstruction(n - shifts[si], primes)) { pass = false; break; }
                }
                if (pass) {
                    answers.push_back(n);
                    if (cand) cand << n << '\n';
                }
            }
            if (!o.quiet) {
                std::cout << "BLOCK low=" << left << " high=" << right << " active=" << active
                          << " prefix=" << use << " prefix_survivors=" << live.size()
                          << " answers=" << answers.size() << '\n';
            }
            if (right == std::numeric_limits<uint64_t>::max()) break;
            left = right + 1;
        }

        double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - begin).count();
        std::ofstream j(o.json);
        if (!j) throw std::runtime_error("cannot write JSON");
        j << "{\n"
          << "  \"method\": \"independent_clean_byte_segmented_factor_scanner\",\n"
          << "  \"low\": \"" << o.low << "\",\n"
          << "  \"high\": \"" << o.high << "\",\n"
          << "  \"C\": " << o.C << ",\n"
          << "  \"D\": " << o.D << ",\n"
          << "  \"next_power_bound_3\": \"" << cap3 << "\",\n"
          << "  \"next_power_bound_5\": \"" << cap5 << "\",\n"
          << "  \"prime_sieve_limit\": " << root << ",\n"
          << "  \"prime_sieve_count\": " << primes.size() << ",\n"
          << "  \"admissible_pair_count_at_high\": " << pairs << ",\n"
          << "  \"distinct_shift_count_at_high\": " << shifts.size() << ",\n"
          << "  \"requested_prefix_shifts\": " << o.prefix << ",\n"
          << "  \"maximum_prefix_shifts_used\": " << max_prefix << ",\n"
          << "  \"window_size\": " << o.block << ",\n"
          << "  \"windows\": " << blocks << ",\n"
          << "  \"activation_splits\": " << boundary_splits << ",\n"
          << "  \"integers_tested\": " << integers << ",\n"
          << "  \"progression_visits\": " << counter.progression_visits << ",\n"
          << "  \"residual_divisions\": " << counter.residual_divisions << ",\n"
          << "  \"small_exact_one_marks\": " << counter.small_marks << ",\n"
          << "  \"large_residual_marks\": " << counter.residual_marks << ",\n"
          << "  \"prefix_membership_tests\": " << counter.prefix_tests << ",\n"
          << "  \"full_shift_factor_tests\": " << counter.full_tests << ",\n"
          << "  \"survivors_after_prefix_total\": " << prefix_survivors << ",\n"
          << "  \"candidate_count\": " << answers.size() << ",\n"
          << "  \"candidates\": [";
        for (size_t i = 0; i < answers.size(); ++i) { if (i) j << ','; j << '"' << answers[i] << '"'; }
        j << "],\n"
          << "  \"elapsed_seconds\": " << sec << ",\n"
          << "  \"classification\": \""
          << (answers.empty() ? "EXACT EXHAUSTIVE FINITE COMPUTATION FOR THE UNRESTRICTED VALUATION-ONE PRIME FAMILY"
                              : "CANDIDATES REQUIRE INDEPENDENT VERIFIERS")
          << "\"\n}\n";
        std::cout << "integers_tested=" << integers << '\n'
                  << "survivors_after_prefix_total=" << prefix_survivors << '\n'
                  << "candidate_count=" << answers.size() << '\n'
                  << "elapsed_seconds=" << sec << '\n'
                  << (answers.empty() ? "EXACT_EMPTY" : "CANDIDATES_FOUND") << '\n';
        return answers.empty() ? 1 : 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR " << e.what() << '\n';
        return 2;
    }
}
