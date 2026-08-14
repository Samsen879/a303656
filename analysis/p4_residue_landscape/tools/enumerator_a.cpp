// Enumerator A for the exact fixed-P4 residue landscape.
//
// This implementation deliberately constructs all valuation-exactly-one
// coverage masks residue-centrically and performs direct lexicographic tuple
// enumeration.  It does not evaluate the original representation-count
// function, scan integers, or import any prior coverage helper.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include <sys/resource.h>

namespace {

constexpr std::uint64_t kLow = 183968950234ULL;
constexpr std::uint64_t kHigh = 246731069451ULL;
constexpr std::array<unsigned, 4> kPrimes{{3, 7, 11, 23}};
constexpr std::array<unsigned, 4> kModuli{{9, 49, 121, 529}};
constexpr std::uint64_t kExpectedM4 = 28227969ULL;
constexpr std::size_t kPairCount = 407;
constexpr std::size_t kWords = 7;
constexpr unsigned kN0Coverage = 216;
constexpr std::array<std::uint16_t, 4> kN0Tuple{{2, 41, 74, 504}};

[[noreturn]] void fail(const std::string& message) {
    throw std::runtime_error(message);
}

void require(bool condition, const std::string& message) {
    if (!condition) fail(message);
}

bool isPrime(unsigned value) {
    if (value < 2) return false;
    for (unsigned divisor = 2; divisor <= value / divisor; ++divisor) {
        if (value % divisor == 0) return false;
    }
    return true;
}

class Sha256 {
public:
    Sha256() { reset(); }

    void reset() {
        state_ = {{0x6a09e667U, 0xbb67ae85U, 0x3c6ef372U, 0xa54ff53aU,
                   0x510e527fU, 0x9b05688cU, 0x1f83d9abU, 0x5be0cd19U}};
        buffer_.fill(0);
        buffer_size_ = 0;
        total_bytes_ = 0;
    }

    void update(const std::uint8_t* data, std::size_t size) {
        total_bytes_ += static_cast<std::uint64_t>(size);
        while (size != 0) {
            const std::size_t take = std::min(size, buffer_.size() - buffer_size_);
            std::copy(data, data + take, buffer_.begin() + buffer_size_);
            buffer_size_ += take;
            data += take;
            size -= take;
            if (buffer_size_ == buffer_.size()) {
                transform(buffer_.data());
                buffer_size_ = 0;
            }
        }
    }

    std::string hexDigest() const {
        Sha256 copy = *this;
        return copy.finishHex();
    }

private:
    static std::uint32_t rotateRight(std::uint32_t value, unsigned shift) {
        return (value >> shift) | (value << (32U - shift));
    }

    void transform(const std::uint8_t* block) {
        static constexpr std::array<std::uint32_t, 64> constants{{
            0x428a2f98U, 0x71374491U, 0xb5c0fbcfU, 0xe9b5dba5U,
            0x3956c25bU, 0x59f111f1U, 0x923f82a4U, 0xab1c5ed5U,
            0xd807aa98U, 0x12835b01U, 0x243185beU, 0x550c7dc3U,
            0x72be5d74U, 0x80deb1feU, 0x9bdc06a7U, 0xc19bf174U,
            0xe49b69c1U, 0xefbe4786U, 0x0fc19dc6U, 0x240ca1ccU,
            0x2de92c6fU, 0x4a7484aaU, 0x5cb0a9dcU, 0x76f988daU,
            0x983e5152U, 0xa831c66dU, 0xb00327c8U, 0xbf597fc7U,
            0xc6e00bf3U, 0xd5a79147U, 0x06ca6351U, 0x14292967U,
            0x27b70a85U, 0x2e1b2138U, 0x4d2c6dfcU, 0x53380d13U,
            0x650a7354U, 0x766a0abbU, 0x81c2c92eU, 0x92722c85U,
            0xa2bfe8a1U, 0xa81a664bU, 0xc24b8b70U, 0xc76c51a3U,
            0xd192e819U, 0xd6990624U, 0xf40e3585U, 0x106aa070U,
            0x19a4c116U, 0x1e376c08U, 0x2748774cU, 0x34b0bcb5U,
            0x391c0cb3U, 0x4ed8aa4aU, 0x5b9cca4fU, 0x682e6ff3U,
            0x748f82eeU, 0x78a5636fU, 0x84c87814U, 0x8cc70208U,
            0x90befffaU, 0xa4506cebU, 0xbef9a3f7U, 0xc67178f2U,
        }};

        std::array<std::uint32_t, 64> schedule{};
        for (std::size_t i = 0; i < 16; ++i) {
            const std::size_t j = 4 * i;
            schedule[i] = (static_cast<std::uint32_t>(block[j]) << 24U) |
                          (static_cast<std::uint32_t>(block[j + 1]) << 16U) |
                          (static_cast<std::uint32_t>(block[j + 2]) << 8U) |
                          static_cast<std::uint32_t>(block[j + 3]);
        }
        for (std::size_t i = 16; i < 64; ++i) {
            const std::uint32_t s0 = rotateRight(schedule[i - 15], 7) ^
                                     rotateRight(schedule[i - 15], 18) ^
                                     (schedule[i - 15] >> 3U);
            const std::uint32_t s1 = rotateRight(schedule[i - 2], 17) ^
                                     rotateRight(schedule[i - 2], 19) ^
                                     (schedule[i - 2] >> 10U);
            schedule[i] = schedule[i - 16] + s0 + schedule[i - 7] + s1;
        }

        std::uint32_t a = state_[0];
        std::uint32_t b = state_[1];
        std::uint32_t c = state_[2];
        std::uint32_t d = state_[3];
        std::uint32_t e = state_[4];
        std::uint32_t f = state_[5];
        std::uint32_t g = state_[6];
        std::uint32_t h = state_[7];
        for (std::size_t i = 0; i < 64; ++i) {
            const std::uint32_t sum1 = rotateRight(e, 6) ^ rotateRight(e, 11) ^
                                       rotateRight(e, 25);
            const std::uint32_t choose = (e & f) ^ ((~e) & g);
            const std::uint32_t temp1 = h + sum1 + choose + constants[i] + schedule[i];
            const std::uint32_t sum0 = rotateRight(a, 2) ^ rotateRight(a, 13) ^
                                       rotateRight(a, 22);
            const std::uint32_t majority = (a & b) ^ (a & c) ^ (b & c);
            const std::uint32_t temp2 = sum0 + majority;
            h = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }
        state_[0] += a;
        state_[1] += b;
        state_[2] += c;
        state_[3] += d;
        state_[4] += e;
        state_[5] += f;
        state_[6] += g;
        state_[7] += h;
    }

    std::string finishHex() {
        const std::uint64_t original_bits = total_bytes_ * 8ULL;
        std::array<std::uint8_t, 64> padding{};
        padding[0] = 0x80U;
        const std::size_t padding_size =
            buffer_size_ < 56 ? 56 - buffer_size_ : 120 - buffer_size_;
        update(padding.data(), padding_size);

        std::array<std::uint8_t, 8> length_bytes{};
        for (unsigned i = 0; i < 8; ++i) {
            length_bytes[7 - i] =
                static_cast<std::uint8_t>((original_bits >> (8U * i)) & 0xffU);
        }
        update(length_bytes.data(), length_bytes.size());
        require(buffer_size_ == 0, "internal SHA256 finalization error");

        std::ostringstream out;
        out << std::hex << std::setfill('0');
        for (const std::uint32_t word : state_) out << std::setw(8) << word;
        return out.str();
    }

    std::array<std::uint32_t, 8> state_{};
    std::array<std::uint8_t, 64> buffer_{};
    std::size_t buffer_size_ = 0;
    std::uint64_t total_bytes_ = 0;
};

void verifySha256Implementation() {
    Sha256 empty;
    require(empty.hexDigest() ==
                "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "SHA256 empty-string self-test failed");
    Sha256 abc;
    const std::array<std::uint8_t, 3> bytes{{'a', 'b', 'c'}};
    abc.update(bytes.data(), bytes.size());
    require(abc.hexDigest() ==
                "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            "SHA256 abc self-test failed");
}

struct ExponentPair {
    unsigned c = 0;
    unsigned d = 0;
    std::uint64_t shift = 0;

    bool operator==(const ExponentPair& other) const {
        return c == other.c && d == other.d && shift == other.shift;
    }
};

std::vector<std::uint64_t> exactPowers(std::uint64_t base, std::uint64_t limit) {
    std::vector<std::uint64_t> powers;
    std::uint64_t value = 1;
    while (true) {
        powers.push_back(value);
        if (value > limit / base) break;
        value *= base;
    }
    return powers;
}

std::vector<ExponentPair> generateDomain(std::uint64_t n) {
    const auto powers3 = exactPowers(3, n);
    const auto powers5 = exactPowers(5, n);
    std::vector<ExponentPair> pairs;
    for (std::size_t c = 0; c < powers3.size(); ++c) {
        for (std::size_t d = 0; d < powers5.size(); ++d) {
            if (powers3[c] <= n - powers5[d]) {
                pairs.push_back(ExponentPair{static_cast<unsigned>(c),
                                             static_cast<unsigned>(d),
                                             powers3[c] + powers5[d]});
            }
        }
    }
    return pairs;
}

void verifyDomain(const std::vector<ExponentPair>& pairs) {
    require(pairs.size() == kPairCount, "active exponent-pair count is not 407");
    for (std::size_t i = 1; i < pairs.size(); ++i) {
        require(std::pair<unsigned, unsigned>{pairs[i - 1].c, pairs[i - 1].d} <
                    std::pair<unsigned, unsigned>{pairs[i].c, pairs[i].d},
                "domain is not strictly lexicographic in (c,d)");
    }
    std::vector<std::pair<unsigned, unsigned>> shift28;
    std::map<std::uint64_t, unsigned> shift_counts;
    for (const auto& pair : pairs) {
        ++shift_counts[pair.shift];
        if (pair.shift == 28) shift28.emplace_back(pair.c, pair.d);
    }
    const std::vector<std::pair<unsigned, unsigned>> expected{{1, 2}, {3, 0}};
    require(shift28 == expected, "duplicate shift 28 exponent pairs are incorrect");
    require(shift_counts.size() == 406, "expected exactly 406 distinct shifts");
    unsigned duplicated_shift_count = 0;
    for (const auto& item : shift_counts) {
        if (item.second > 1) {
            ++duplicated_shift_count;
            require(item.first == 28 && item.second == 2,
                    "unexpected duplicate shift in active domain");
        }
    }
    require(duplicated_shift_count == 1, "shift 28 is not the unique duplicate shift");
}

struct PackedMask {
    std::array<std::uint64_t, kWords> words{};
};

PackedMask maskUnion(const PackedMask& left, const PackedMask& right) {
    PackedMask result;
    for (std::size_t i = 0; i < kWords; ++i) {
        result.words[i] = left.words[i] | right.words[i];
    }
    return result;
}

unsigned maskPopcount(const PackedMask& mask) {
    unsigned count = 0;
    for (const std::uint64_t word : mask.words) {
        count += static_cast<unsigned>(__builtin_popcountll(word));
    }
    return count;
}

unsigned unionPopcount(const PackedMask& left, const PackedMask& right) {
    unsigned count = 0;
    for (std::size_t i = 0; i < kWords; ++i) {
        count += static_cast<unsigned>(
            __builtin_popcountll(left.words[i] | right.words[i]));
    }
    return count;
}

using CoverageMasks = std::array<std::vector<PackedMask>, 4>;

CoverageMasks constructCoverageMasks(const std::vector<ExponentPair>& pairs) {
    CoverageMasks coverage;
    for (std::size_t prime_index = 0; prime_index < kPrimes.size(); ++prime_index) {
        const unsigned p = kPrimes[prime_index];
        const unsigned modulus = kModuli[prime_index];
        require(modulus == p * p, "prime-square modulus mismatch");
        coverage[prime_index].resize(modulus);
        for (unsigned residue = 0; residue < modulus; ++residue) {
            PackedMask mask;
            for (std::size_t pair_index = 0; pair_index < pairs.size(); ++pair_index) {
                const unsigned shift_mod =
                    static_cast<unsigned>(pairs[pair_index].shift % modulus);
                const unsigned difference_mod = (residue + modulus - shift_mod) % modulus;
                const bool valuation_exactly_one =
                    difference_mod % p == 0 && difference_mod != 0;
                if (valuation_exactly_one) {
                    mask.words[pair_index / 64] |=
                        std::uint64_t{1} << (pair_index % 64);
                }
            }
            coverage[prime_index][residue] = mask;
        }
    }

    constexpr unsigned used_bits_in_last_word = kPairCount - 64U * (kWords - 1U);
    static_assert(used_bits_in_last_word == 23, "unexpected packed-mask width");
    const std::uint64_t unused_mask = ~((std::uint64_t{1} << used_bits_in_last_word) - 1U);
    for (const auto& prime_masks : coverage) {
        for (const auto& mask : prime_masks) {
            require((mask.words.back() & unused_mask) == 0,
                    "coverage mask has a bit beyond the 407-pair domain");
        }
    }
    return coverage;
}

using Tuple = std::array<std::uint16_t, 4>;

std::array<std::uint8_t, 8> serializeTuple(const Tuple& tuple) {
    std::array<std::uint8_t, 8> bytes{};
    for (std::size_t i = 0; i < tuple.size(); ++i) {
        bytes[2 * i] = static_cast<std::uint8_t>(tuple[i] & 0xffU);
        bytes[2 * i + 1] = static_cast<std::uint8_t>((tuple[i] >> 8U) & 0xffU);
    }
    return bytes;
}

std::array<std::uint8_t, 10> serializeRow(const Tuple& tuple, unsigned coverage) {
    require(coverage <= std::numeric_limits<std::uint16_t>::max(),
            "coverage does not fit canonical uint16 field");
    std::array<std::uint8_t, 10> bytes{};
    const auto tuple_bytes = serializeTuple(tuple);
    std::copy(tuple_bytes.begin(), tuple_bytes.end(), bytes.begin());
    const auto coverage16 = static_cast<std::uint16_t>(coverage);
    bytes[8] = static_cast<std::uint8_t>(coverage16 & 0xffU);
    bytes[9] = static_cast<std::uint8_t>((coverage16 >> 8U) & 0xffU);
    return bytes;
}

struct LandscapeResult {
    std::uint64_t tuple_count = 0;
    std::array<std::uint64_t, kPairCount + 1> histogram{};
    unsigned minimum = kPairCount + 1;
    unsigned maximum = 0;
    std::uint64_t argmax_count = 0;
    std::vector<Tuple> first_100_argmax;
    Sha256 stream_sha;
    Sha256 argmax_sha;
    std::uint64_t above_n0 = 0;
    std::uint64_t equal_n0 = 0;
    std::uint64_t below_n0 = 0;

    void observe(const Tuple& tuple, unsigned value) {
        require(value <= kPairCount, "coverage exceeds active-pair count");
        const auto row = serializeRow(tuple, value);
        stream_sha.update(row.data(), row.size());
        ++tuple_count;
        ++histogram[value];
        minimum = std::min(minimum, value);

        if (value > maximum) {
            maximum = value;
            argmax_count = 0;
            first_100_argmax.clear();
            argmax_sha.reset();
        }
        if (value == maximum) {
            ++argmax_count;
            if (first_100_argmax.size() < 100) first_100_argmax.push_back(tuple);
            const auto tuple_bytes = serializeTuple(tuple);
            argmax_sha.update(tuple_bytes.data(), tuple_bytes.size());
        }

        if (value > kN0Coverage) {
            ++above_n0;
        } else if (value == kN0Coverage) {
            ++equal_n0;
        } else {
            ++below_n0;
        }
    }

    void validate(std::uint64_t expected_count) const {
        require(tuple_count == expected_count, "landscape tuple count mismatch");
        std::uint64_t histogram_total = 0;
        for (const auto count : histogram) histogram_total += count;
        require(histogram_total == tuple_count, "histogram total does not match tuple count");
        require(above_n0 + equal_n0 + below_n0 == tuple_count,
                "n0 comparison counts do not match tuple count");
        require(argmax_count == histogram[maximum],
                "argmax count does not match maximum histogram bin");
        require(minimum <= maximum, "invalid landscape minimum/maximum");
    }
};

LandscapeResult enumerateFull(const CoverageMasks& coverage) {
    LandscapeResult result;
    for (std::uint16_t t3 = 0; t3 < kModuli[0]; ++t3) {
        for (std::uint16_t t7 = 0; t7 < kModuli[1]; ++t7) {
            const PackedMask union37 = maskUnion(coverage[0][t3], coverage[1][t7]);
            for (std::uint16_t t11 = 0; t11 < kModuli[2]; ++t11) {
                const PackedMask union3711 = maskUnion(union37, coverage[2][t11]);
                for (std::uint16_t t23 = 0; t23 < kModuli[3]; ++t23) {
                    const unsigned value = unionPopcount(union3711, coverage[3][t23]);
                    result.observe(Tuple{{t3, t7, t11, t23}}, value);
                }
            }
        }
    }
    result.validate(kExpectedM4);
    return result;
}

LandscapeResult enumerateT3Equals2(const CoverageMasks& coverage) {
    LandscapeResult result;
    constexpr std::uint16_t t3 = 2;
    for (std::uint16_t t7 = 0; t7 < kModuli[1]; ++t7) {
        const PackedMask union37 = maskUnion(coverage[0][t3], coverage[1][t7]);
        for (std::uint16_t t11 = 0; t11 < kModuli[2]; ++t11) {
            const PackedMask union3711 = maskUnion(union37, coverage[2][t11]);
            for (std::uint16_t t23 = 0; t23 < kModuli[3]; ++t23) {
                const unsigned value = unionPopcount(union3711, coverage[3][t23]);
                result.observe(Tuple{{t3, t7, t11, t23}}, value);
            }
        }
    }
    constexpr std::uint64_t expected = 49ULL * 121ULL * 529ULL;
    static_assert(expected == 3136441ULL, "unexpected t3=2 slice size");
    result.validate(expected);
    return result;
}

unsigned tupleCoverage(const CoverageMasks& coverage, const Tuple& tuple) {
    PackedMask combined = coverage[0][tuple[0]];
    for (std::size_t i = 1; i < tuple.size(); ++i) {
        combined = maskUnion(combined, coverage[i][tuple[i]]);
    }
    return maskPopcount(combined);
}

struct SubsetResult {
    unsigned subset_mask = 0;
    std::vector<unsigned> primes;
    std::uint64_t modulus_product = 1;
    unsigned maximum = 0;
    std::uint64_t argmax_count = 0;
    std::vector<unsigned> first_argmax;
};

void enumerateSubsetRecursive(const CoverageMasks& coverage,
                              const std::vector<unsigned>& selected_indices,
                              std::size_t depth,
                              const PackedMask& accumulated,
                              std::vector<unsigned>& residues,
                              SubsetResult& result) {
    if (depth == selected_indices.size()) {
        const unsigned value = maskPopcount(accumulated);
        if (value > result.maximum) {
            result.maximum = value;
            result.argmax_count = 1;
            result.first_argmax = residues;
        } else if (value == result.maximum) {
            ++result.argmax_count;
        }
        return;
    }

    const unsigned prime_index = selected_indices[depth];
    for (unsigned residue = 0; residue < kModuli[prime_index]; ++residue) {
        residues[depth] = residue;
        const PackedMask next = maskUnion(accumulated, coverage[prime_index][residue]);
        enumerateSubsetRecursive(coverage, selected_indices, depth + 1, next,
                                 residues, result);
    }
}

std::vector<SubsetResult> optimizeAllSubsets(const CoverageMasks& coverage) {
    std::vector<SubsetResult> results;
    for (unsigned subset_mask = 1; subset_mask < 16; ++subset_mask) {
        SubsetResult result;
        result.subset_mask = subset_mask;
        std::vector<unsigned> selected_indices;
        for (unsigned i = 0; i < 4; ++i) {
            if ((subset_mask & (1U << i)) != 0) {
                selected_indices.push_back(i);
                result.primes.push_back(kPrimes[i]);
                result.modulus_product *= kModuli[i];
            }
        }
        std::vector<unsigned> residues(selected_indices.size(), 0);
        PackedMask empty;
        enumerateSubsetRecursive(coverage, selected_indices, 0, empty, residues, result);
        require(result.argmax_count > 0, "subset optimization produced no maximizer");
        results.push_back(std::move(result));
    }
    require(results.size() == 15, "did not optimize all 15 nonempty subsets");
    return results;
}

void emitTuple(std::ostream& out, const Tuple& tuple) {
    out << '[' << tuple[0] << ',' << tuple[1] << ',' << tuple[2] << ',' << tuple[3]
        << ']';
}

void emitTupleList(std::ostream& out, const std::vector<Tuple>& tuples) {
    out << '[';
    for (std::size_t i = 0; i < tuples.size(); ++i) {
        if (i != 0) out << ',';
        emitTuple(out, tuples[i]);
    }
    out << ']';
}

void emitUnsignedList(std::ostream& out, const std::vector<unsigned>& values) {
    out << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i != 0) out << ',';
        out << values[i];
    }
    out << ']';
}

void emitHistogram(std::ostream& out, const LandscapeResult& result) {
    out << '{';
    bool first = true;
    for (std::size_t value = 0; value < result.histogram.size(); ++value) {
        if (result.histogram[value] == 0) continue;
        if (!first) out << ',';
        first = false;
        out << '\"' << value << "\":" << result.histogram[value];
    }
    out << '}';
}

void emitN0Counts(std::ostream& out, const LandscapeResult& result) {
    const std::uint64_t percentile_numerator =
        100ULL * (2ULL * result.below_n0 + result.equal_n0);
    const std::uint64_t percentile_denominator = 2ULL * result.tuple_count;
    out << "{\"above\":" << result.above_n0 << ",\"equal\":" << result.equal_n0
        << ",\"below\":" << result.below_n0 << ",\"rank_interval\":["
        << (result.above_n0 + 1) << ',' << (result.above_n0 + result.equal_n0)
        << "],\"percentile_definition\":\"midrank share: 100 * (below + equal / 2) / total\""
        << ",\"percentile\":{\"numerator\":" << percentile_numerator
        << ",\"denominator\":" << percentile_denominator << "}}";
}

void emitLandscape(std::ostream& out, const LandscapeResult& result) {
    out << "{\"tuple_count\":" << result.tuple_count << ",\"minimum\":"
        << result.minimum << ",\"maximum\":" << result.maximum << ",\"histogram\":";
    emitHistogram(out, result);
    out << ",\"argmax_count\":" << result.argmax_count << ",\"argmax_digest\":\""
        << result.argmax_sha.hexDigest() << "\",\"first_100_argmax\":";
    emitTupleList(out, result.first_100_argmax);
    out << ",\"stream_digest\":\"" << result.stream_sha.hexDigest()
        << "\",\"n0_counts\":";
    emitN0Counts(out, result);
    out << '}';
}

double secondsSince(const std::chrono::steady_clock::time_point& start) {
    return std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
}

long peakRssKib() {
    struct rusage usage {};
    require(getrusage(RUSAGE_SELF, &usage) == 0, "getrusage(RUSAGE_SELF) failed");
    return usage.ru_maxrss;
}

void writeCertificate(const std::string& path,
                      const LandscapeResult& full,
                      const LandscapeResult& slice,
                      const std::vector<SubsetResult>& subsets,
                      double coverage_seconds,
                      double full_seconds,
                      double slice_seconds,
                      double subset_seconds,
                      long coverage_rss_kib,
                      long full_rss_kib,
                      long slice_rss_kib,
                      long subset_rss_kib,
                      double total_seconds) {
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    require(static_cast<bool>(out), "cannot open output certificate: " + path);
    out << std::setprecision(9);
    out << '{';
    out << "\"schema\":\"a303656-fixed-p4-residue-landscape-certificate-v1\","
        << "\"implementation\":\"enumerator_a_direct_lexicographic_bitset\","
        << "\"domain\":{\"low\":" << kLow << ",\"high\":" << kHigh
        << ",\"pair_count\":" << kPairCount
        << ",\"duplicate_shift_28_pairs\":[[1,2],[3,0]]},"
        << "\"primes\":[3,7,11,23],\"moduli\":[9,49,121,529],\"M4\":"
        << kExpectedM4 << ','
        << "\"serialization\":{"
        << "\"description\":\"Stream rows are t3,t7,t11,t23,G as five uint16 values in canonical lexicographic tuple order. Argmax rows omit G. All fields are little-endian with no padding.\","
        << "\"fields\":[\"t3\",\"t7\",\"t11\",\"t23\",\"G\"],"
        << "\"integer_width_bits\":16,\"byte_order\":\"little\","
        << "\"row_bytes\":10,\"padding_bytes\":0,"
        << "\"tuple_order\":\"lexicographic\",\"row_count\":"
        << kExpectedM4 << ",\"struct_format\":\"<5H\","
        << "\"argmax\":{\"fields\":[\"t3\",\"t7\",\"t11\",\"t23\"],"
        << "\"integer_width_bits\":16,\"byte_order\":\"little\","
        << "\"row_bytes\":8,\"padding_bytes\":0,"
        << "\"tuple_order\":\"lexicographic\",\"includes_G\":false,"
        << "\"struct_format\":\"<4H\"}},"
        << "\"full\":";
    emitLandscape(out, full);
    out << ",\"t3eq2\":";
    emitLandscape(out, slice);
    out << ",\"n0\":{\"tuple\":[2,41,74,504],\"coverage\":" << kN0Coverage
        << "},\"subset_optima\":[";
    for (std::size_t i = 0; i < subsets.size(); ++i) {
        if (i != 0) out << ',';
        const auto& subset = subsets[i];
        out << "{\"subset_mask\":" << subset.subset_mask << ",\"primes\":";
        emitUnsignedList(out, subset.primes);
        out << ",\"modulus_product\":" << subset.modulus_product
            << ",\"maximum\":" << subset.maximum << ",\"argmax_count\":"
            << subset.argmax_count << ",\"first_argmax\":";
        emitUnsignedList(out, subset.first_argmax);
        out << '}';
    }
    out << "],\"timings_seconds\":{\"coverage_set_generation\":"
        << coverage_seconds << ",\"full_landscape\":" << full_seconds
        << ",\"constrained_slice\":" << slice_seconds
        << ",\"subset_optimization\":" << subset_seconds << ",\"total\":"
        << total_seconds << "},\"resources\":{"
        << "\"rss_definition\":\"getrusage(RUSAGE_SELF) ru_maxrss KiB; peak-to-date at stage end\","
        << "\"coverage_generation\":{\"wall_seconds\":" << coverage_seconds
        << ",\"ru_maxrss_kib_at_stage_end\":" << coverage_rss_kib << "},"
        << "\"full_landscape\":{\"wall_seconds\":" << full_seconds
        << ",\"ru_maxrss_kib_at_stage_end\":" << full_rss_kib << "},"
        << "\"constrained_slice\":{\"wall_seconds\":" << slice_seconds
        << ",\"ru_maxrss_kib_at_stage_end\":" << slice_rss_kib << "},"
        << "\"subset_optimization\":{\"wall_seconds\":" << subset_seconds
        << ",\"ru_maxrss_kib_at_stage_end\":" << subset_rss_kib << "}}}\n";
    out.flush();
    require(static_cast<bool>(out), "failed while writing output certificate: " + path);
}

}  // namespace

int main(int argc, char** argv) {
    try {
        require(argc == 2, "usage: enumerator_a CERTIFICATE.json");
        const auto total_start = std::chrono::steady_clock::now();
        verifySha256Implementation();

        std::uint64_t modulus_product = 1;
        const std::array<unsigned, 4> expected_primes{{3, 7, 11, 23}};
        const std::array<unsigned, 4> expected_moduli{{9, 49, 121, 529}};
        require(kPrimes == expected_primes, "P4 runtime verification failed");
        require(kModuli == expected_moduli, "P4 modulus list runtime verification failed");
        for (std::size_t i = 0; i < kPrimes.size(); ++i) {
            require(isPrime(kPrimes[i]) && kPrimes[i] % 4 == 3,
                    "P4 contains a value that is not a prime congruent to 3 modulo 4");
            require(kPrimes[i] * kPrimes[i] == kModuli[i],
                    "P4 square modulus runtime verification failed");
            modulus_product *= kModuli[i];
        }
        require(modulus_product == kExpectedM4, "M4 runtime verification failed");

        const auto domain_low = generateDomain(kLow);
        const auto domain_high = generateDomain(kHigh);
        require(domain_low == domain_high,
                "activation-cell exponent-pair domain is not constant at its endpoints");
        verifyDomain(domain_low);

        const auto coverage_start = std::chrono::steady_clock::now();
        const CoverageMasks coverage = constructCoverageMasks(domain_low);
        const double coverage_seconds = secondsSince(coverage_start);
        const long coverage_rss_kib = peakRssKib();

        const unsigned n0_coverage = tupleCoverage(coverage, kN0Tuple);
        require(n0_coverage == kN0Coverage, "N0 tuple coverage is not exactly 216");

        const auto full_start = std::chrono::steady_clock::now();
        const LandscapeResult full = enumerateFull(coverage);
        const double full_seconds = secondsSince(full_start);
        const long full_rss_kib = peakRssKib();

        const auto slice_start = std::chrono::steady_clock::now();
        const LandscapeResult slice = enumerateT3Equals2(coverage);
        const double slice_seconds = secondsSince(slice_start);
        const long slice_rss_kib = peakRssKib();

        const auto subset_start = std::chrono::steady_clock::now();
        const auto subsets = optimizeAllSubsets(coverage);
        const double subset_seconds = secondsSince(subset_start);
        const long subset_rss_kib = peakRssKib();

        writeCertificate(argv[1], full, slice, subsets, coverage_seconds, full_seconds,
                         slice_seconds, subset_seconds, coverage_rss_kib, full_rss_kib,
                         slice_rss_kib, subset_rss_kib, secondsSince(total_start));
        std::cerr << "ENUMERATOR_A_OK rows=" << full.tuple_count
                  << " slice_rows=" << slice.tuple_count << " max=" << full.maximum
                  << " output=" << argv[1] << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ENUMERATOR_A_ERROR: " << error.what() << '\n';
        return 2;
    }
}
