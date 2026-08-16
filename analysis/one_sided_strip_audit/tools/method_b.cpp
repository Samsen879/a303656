#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using u64 = std::uint64_t;
static constexpr std::uint8_t INF = 255;

static std::vector<u64> powers_le(u64 base, u64 limit) {
    std::vector<u64> out;
    for (u64 value = 1; value <= limit;) {
        out.push_back(value);
        if (value > limit / base) break;
        value *= base;
    }
    return out;
}

static std::vector<std::uint32_t> primes_upto(std::uint32_t N) {
    std::vector<std::uint8_t> composite(static_cast<std::size_t>(N) + 1, 0);
    composite[0] = 1;
    if (N >= 1) composite[1] = 1;
    std::vector<std::uint32_t> primes;
    for (std::uint32_t p = 2; p <= N; ++p) {
        if (composite[p]) continue;
        primes.push_back(p);
        if (static_cast<u64>(p) * p <= N) {
            for (u64 m = static_cast<u64>(p) * p; m <= N; m += p) composite[static_cast<std::size_t>(m)] = 1;
        }
    }
    return primes;
}

static std::vector<std::uint8_t> fermat_s2(std::uint32_t N, const std::vector<std::uint32_t>& primes) {
    std::vector<std::uint8_t> good(static_cast<std::size_t>(N) + 1, 1);
    for (std::uint32_t p : primes) {
        if ((p & 3U) != 3U) continue;
        u64 odd_power = p;
        while (odd_power <= N) {
            const u64 next = odd_power * p;
            for (u64 m = odd_power; m <= N; m += odd_power) {
                if (next > N || m % next != 0) good[static_cast<std::size_t>(m)] = 0;
            }
            if (odd_power > static_cast<u64>(N) / (static_cast<u64>(p) * p)) break;
            odd_power *= static_cast<u64>(p) * p;
        }
    }
    good[0] = 1;
    return good;
}

static std::vector<std::uint8_t> minimum_outer(
    std::uint32_t N,
    const std::vector<std::uint8_t>& s2,
    const std::vector<u64>& outer,
    const std::vector<u64>& inner
) {
    std::vector<std::uint8_t> answer(static_cast<std::size_t>(N) + 1, INF);
    for (std::uint32_t n = 2; n <= N; ++n) {
        bool found = false;
        for (std::size_t e = 0; e < outer.size() && outer[e] + 1 <= n && !found; ++e) {
            for (u64 inner_power : inner) {
                const u64 shift = outer[e] + inner_power;
                if (shift > n) break;
                if (s2[static_cast<std::size_t>(n - shift)]) {
                    answer[n] = static_cast<std::uint8_t>(e);
                    found = true;
                    break;
                }
            }
        }
    }
    return answer;
}

static void write_raw(const std::string& path, const std::vector<std::uint8_t>& data) {
    std::ofstream stream(path, std::ios::binary);
    if (!stream) {
        std::cerr << "cannot open " << path << "\n";
        std::exit(2);
    }
    stream.write(reinterpret_cast<const char*>(data.data()), static_cast<std::streamsize>(data.size()));
}

int main(int argc, char** argv) {
    if (argc != 3) {
        std::cerr << "usage: method_b N OUTDIR\n";
        return 2;
    }
    const auto parsed = std::stoull(argv[1]);
    if (parsed < 2 || parsed > UINT32_MAX) {
        std::cerr << "N outside supported domain\n";
        return 2;
    }
    const auto N = static_cast<std::uint32_t>(parsed);
    const std::string outdir = argv[2];
    const auto p3 = powers_le(3, static_cast<u64>(N) - 1);
    const auto p5 = powers_le(5, static_cast<u64>(N) - 1);
    const auto primes = primes_upto(N);
    const auto s2 = fermat_s2(N, primes);
    const auto c3 = minimum_outer(N, s2, p3, p5);
    const auto c5 = minimum_outer(N, s2, p5, p3);
    write_raw(outdir + "/method_b_S2.uint8", s2);
    write_raw(outdir + "/method_b_C3.uint8", c3);
    write_raw(outdir + "/method_b_C5.uint8", c5);
    std::size_t s2_count = 0, uncovered_c3 = 0, uncovered_c5 = 0;
    int max_c3 = -1, max_c5 = -1;
    for (auto value : s2) s2_count += value;
    for (std::uint32_t n = 2; n <= N; ++n) {
        if (c3[n] == INF) ++uncovered_c3; else max_c3 = std::max(max_c3, static_cast<int>(c3[n]));
        if (c5[n] == INF) ++uncovered_c5; else max_c5 = std::max(max_c5, static_cast<int>(c5[n]));
    }
    std::ofstream summary(outdir + "/method_b_summary.json");
    summary << "{\n"
            << "  \"N\": " << N << ",\n"
            << "  \"method\": \"fermat_odd_valuation_sieve_then_n_first_search\",\n"
            << "  \"prime_count\": " << primes.size() << ",\n"
            << "  \"s2_count\": " << s2_count << ",\n"
            << "  \"uncovered_C3\": " << uncovered_c3 << ",\n"
            << "  \"uncovered_C5\": " << uncovered_c5 << ",\n"
            << "  \"max_C3\": " << max_c3 << ",\n"
            << "  \"max_C5\": " << max_c5 << "\n"
            << "}\n";
    return 0;
}
