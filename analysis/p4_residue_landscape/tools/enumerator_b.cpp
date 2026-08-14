// Independent pair-centric / meet-in-the-middle enumerator for the fixed-P4
// residue landscape.  This program never evaluates T(n), scans progression
// points, or invokes a two-square implementation.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <sys/resource.h>
#include <utility>
#include <vector>

namespace {

constexpr std::uint64_t kCellLow = 183968950234ULL;
constexpr std::uint64_t kCellHigh = 246731069451ULL;
constexpr std::array<unsigned, 4> kPrimes{{3, 7, 11, 23}};
constexpr std::array<unsigned, 4> kModuli{{9, 49, 121, 529}};
constexpr std::uint64_t kM4 = 28227969ULL;
constexpr std::uint64_t kFullRows = 28227969ULL;
constexpr std::uint64_t kSliceRows = 3136441ULL;
constexpr std::size_t kPairCount = 407;
constexpr std::size_t kWords = (kPairCount + 63U) / 64U;

struct ExponentPair {
  std::uint16_t c;
  std::uint16_t d;
  std::uint64_t shift;

  bool operator==(const ExponentPair& other) const {
    return c == other.c && d == other.d && shift == other.shift;
  }
};

struct Mask {
  std::array<std::uint64_t, kWords> word{};
};

struct Tuple4 {
  std::array<std::uint16_t, 4> value{};
};

// Small self-contained SHA-256 implementation.  It has no dependency on a
// precompiled library and consumes the canonical bytes incrementally.
class Sha256 {
 public:
  Sha256() { reset(); }

  void reset() {
    state_ = {{0x6a09e667U, 0xbb67ae85U, 0x3c6ef372U, 0xa54ff53aU,
               0x510e527fU, 0x9b05688cU, 0x1f83d9abU, 0x5be0cd19U}};
    buffer_.fill(0);
    buffered_ = 0;
    bytes_ = 0;
  }

  void update(const std::uint8_t* data, std::size_t size) {
    bytes_ += static_cast<std::uint64_t>(size);
    while (size != 0U) {
      const std::size_t take = std::min(size, buffer_.size() - buffered_);
      std::copy(data, data + take, buffer_.begin() +
                                      static_cast<std::ptrdiff_t>(buffered_));
      buffered_ += take;
      data += take;
      size -= take;
      if (buffered_ == buffer_.size()) {
        compress(buffer_.data());
        buffered_ = 0;
      }
    }
  }

  std::string finish_hex() {
    const std::uint64_t bit_length = bytes_ * 8ULL;
    const std::uint8_t marker = 0x80U;
    update(&marker, 1);
    const std::uint8_t zero = 0;
    while (buffered_ != 56U) {
      update(&zero, 1);
    }
    std::uint8_t encoded_length[8];
    for (unsigned i = 0; i < 8; ++i) {
      encoded_length[7U - i] =
          static_cast<std::uint8_t>((bit_length >> (8U * i)) & 0xffU);
    }
    update(encoded_length, sizeof(encoded_length));

    std::ostringstream out;
    out << std::hex << std::setfill('0');
    for (std::uint32_t x : state_) {
      out << std::setw(8) << x;
    }
    return out.str();
  }

 private:
  static std::uint32_t rotate_right(std::uint32_t x, unsigned n) {
    return (x >> n) | (x << (32U - n));
  }

  void compress(const std::uint8_t* block) {
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
        0x90befffaU, 0xa4506cebU, 0xbef9a3f7U, 0xc67178f2U}};

    std::array<std::uint32_t, 64> schedule{};
    for (unsigned i = 0; i < 16; ++i) {
      const unsigned j = 4U * i;
      schedule[i] = (static_cast<std::uint32_t>(block[j]) << 24U) |
                    (static_cast<std::uint32_t>(block[j + 1U]) << 16U) |
                    (static_cast<std::uint32_t>(block[j + 2U]) << 8U) |
                    static_cast<std::uint32_t>(block[j + 3U]);
    }
    for (unsigned i = 16; i < 64; ++i) {
      const std::uint32_t s0 = rotate_right(schedule[i - 15U], 7U) ^
                               rotate_right(schedule[i - 15U], 18U) ^
                               (schedule[i - 15U] >> 3U);
      const std::uint32_t s1 = rotate_right(schedule[i - 2U], 17U) ^
                               rotate_right(schedule[i - 2U], 19U) ^
                               (schedule[i - 2U] >> 10U);
      schedule[i] = schedule[i - 16U] + s0 + schedule[i - 7U] + s1;
    }

    std::uint32_t a = state_[0];
    std::uint32_t b = state_[1];
    std::uint32_t c = state_[2];
    std::uint32_t d = state_[3];
    std::uint32_t e = state_[4];
    std::uint32_t f = state_[5];
    std::uint32_t g = state_[6];
    std::uint32_t h = state_[7];
    for (unsigned i = 0; i < 64; ++i) {
      const std::uint32_t sigma1 =
          rotate_right(e, 6U) ^ rotate_right(e, 11U) ^ rotate_right(e, 25U);
      const std::uint32_t choice = (e & f) ^ ((~e) & g);
      const std::uint32_t temp1 =
          h + sigma1 + choice + constants[i] + schedule[i];
      const std::uint32_t sigma0 =
          rotate_right(a, 2U) ^ rotate_right(a, 13U) ^ rotate_right(a, 22U);
      const std::uint32_t majority = (a & b) ^ (a & c) ^ (b & c);
      const std::uint32_t temp2 = sigma0 + majority;
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

  std::array<std::uint32_t, 8> state_{};
  std::array<std::uint8_t, 64> buffer_{};
  std::size_t buffered_ = 0;
  std::uint64_t bytes_ = 0;
};

void encode_u16_le(std::uint8_t* destination, std::uint16_t value) {
  destination[0] = static_cast<std::uint8_t>(value & 0xffU);
  destination[1] = static_cast<std::uint8_t>((value >> 8U) & 0xffU);
}

void hash_full_row(Sha256& digest, const Tuple4& tuple, unsigned coverage) {
  std::uint8_t row[10];
  for (unsigned i = 0; i < 4; ++i) {
    encode_u16_le(row + 2U * i, tuple.value[i]);
  }
  encode_u16_le(row + 8U, static_cast<std::uint16_t>(coverage));
  digest.update(row, sizeof(row));
}

void hash_argmax_tuple(Sha256& digest, const Tuple4& tuple) {
  std::uint8_t row[8];
  for (unsigned i = 0; i < 4; ++i) {
    encode_u16_le(row + 2U * i, tuple.value[i]);
  }
  digest.update(row, sizeof(row));
}

void verify_sha256_implementation() {
  static constexpr std::uint8_t message[] = {'a', 'b', 'c'};
  Sha256 digest;
  digest.update(message, sizeof(message));
  if (digest.finish_hex() !=
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad") {
    throw std::runtime_error("internal SHA-256 known-answer test failed");
  }
}

std::vector<std::uint64_t> integer_powers(std::uint64_t base,
                                         std::uint64_t limit) {
  std::vector<std::uint64_t> result;
  std::uint64_t value = 1;
  for (;;) {
    result.push_back(value);
    if (value > limit / base) {
      break;
    }
    value *= base;
  }
  return result;
}

std::vector<ExponentPair> make_domain(std::uint64_t n) {
  const std::vector<std::uint64_t> powers3 = integer_powers(3, n);
  const std::vector<std::uint64_t> powers5 = integer_powers(5, n);
  std::vector<ExponentPair> pairs;
  for (std::size_t c = 0; c < powers3.size(); ++c) {
    for (std::size_t d = 0; d < powers5.size(); ++d) {
      if (powers3[c] <= n - powers5[d]) {
        pairs.push_back(ExponentPair{static_cast<std::uint16_t>(c),
                                     static_cast<std::uint16_t>(d),
                                     powers3[c] + powers5[d]});
      }
    }
  }
  return pairs;
}

using PrimeMasks = std::array<std::vector<Mask>, 4>;

PrimeMasks construct_pair_centric_masks(const std::vector<ExponentPair>& pairs) {
  PrimeMasks result;
  for (unsigned prime_index = 0; prime_index < kPrimes.size(); ++prime_index) {
    result[prime_index].resize(kModuli[prime_index]);
  }

  // This is deliberately pair-centric.  For a fixed pair and prime, exactly
  // the p-1 nonzero multiples k*p modulo p^2 give valuation exactly one.
  for (std::size_t pair_index = 0; pair_index < pairs.size(); ++pair_index) {
    const std::size_t lane = pair_index / 64U;
    const std::uint64_t bit = 1ULL << (pair_index % 64U);
    for (unsigned prime_index = 0; prime_index < kPrimes.size(); ++prime_index) {
      const unsigned p = kPrimes[prime_index];
      const unsigned modulus = kModuli[prime_index];
      const unsigned base = static_cast<unsigned>(pairs[pair_index].shift % modulus);
      for (unsigned nonzero_lift = 1; nonzero_lift < p; ++nonzero_lift) {
        const unsigned residue = (base + nonzero_lift * p) % modulus;
        result[prime_index][residue].word[lane] |= bit;
      }
    }
  }
  return result;
}

void verify_domain(const std::vector<ExponentPair>& pairs) {
  if (pairs.size() != kPairCount) {
    throw std::runtime_error("activation-cell domain does not contain 407 pairs");
  }
  if (pairs != make_domain(kCellHigh)) {
    throw std::runtime_error("exponent-pair domain is not constant on the cell");
  }
  for (std::size_t i = 1; i < pairs.size(); ++i) {
    if (std::pair<std::uint16_t, std::uint16_t>(pairs[i - 1].c, pairs[i - 1].d) >=
        std::pair<std::uint16_t, std::uint16_t>(pairs[i].c, pairs[i].d)) {
      throw std::runtime_error("domain is not in strict lexicographic order");
    }
  }
  std::vector<std::pair<std::uint16_t, std::uint16_t>> shift28;
  for (const ExponentPair& pair : pairs) {
    if (pair.shift == 28U) {
      shift28.emplace_back(pair.c, pair.d);
    }
  }
  const std::vector<std::pair<std::uint16_t, std::uint16_t>> expected{{1, 2},
                                                                      {3, 0}};
  if (shift28 != expected) {
    throw std::runtime_error("duplicate shift 28 pairs were not retained exactly");
  }
}

void verify_pair_centric_masks(const std::vector<ExponentPair>& pairs,
                               const PrimeMasks& masks) {
  for (unsigned prime_index = 0; prime_index < kPrimes.size(); ++prime_index) {
    const unsigned p = kPrimes[prime_index];
    const unsigned modulus = kModuli[prime_index];
    if (masks[prime_index].size() != modulus) {
      throw std::runtime_error("coverage-mask residue count mismatch");
    }
    for (unsigned residue = 0; residue < modulus; ++residue) {
      for (std::size_t pair_index = 0; pair_index < pairs.size(); ++pair_index) {
        const unsigned shift_mod =
            static_cast<unsigned>(pairs[pair_index].shift % modulus);
        const unsigned difference = (residue + modulus - shift_mod) % modulus;
        const bool expected = (difference % p == 0U) && (difference != 0U);
        const bool present =
            ((masks[prime_index][residue].word[pair_index / 64U] >>
              (pair_index % 64U)) &
             1ULL) != 0ULL;
        if (expected != present) {
          throw std::runtime_error("pair-centric mask fails exact-one semantics");
        }
      }
    }
    if ((masks[prime_index].back().word.back() & (~0ULL << (kPairCount % 64U))) !=
        0ULL) {
      throw std::runtime_error("bits beyond the 407-pair domain are nonzero");
    }
  }
}

struct LandscapeSummary {
  std::array<std::uint64_t, kPairCount + 1U> histogram{};
  unsigned minimum = static_cast<unsigned>(kPairCount + 1U);
  unsigned maximum = 0;
  std::uint64_t rows = 0;
  std::uint64_t argmax_count = 0;
  std::vector<Tuple4> first_argmax;
  Sha256 argmax_digest;

  void observe(const Tuple4& tuple, unsigned coverage) {
    if (coverage > kPairCount) {
      throw std::runtime_error("coverage exceeds pair count");
    }
    ++rows;
    ++histogram[coverage];
    minimum = std::min(minimum, coverage);
    if (coverage > maximum) {
      maximum = coverage;
      argmax_count = 1;
      first_argmax.clear();
      first_argmax.push_back(tuple);
      argmax_digest.reset();
      hash_argmax_tuple(argmax_digest, tuple);
    } else if (coverage == maximum) {
      ++argmax_count;
      if (first_argmax.size() < 100U) {
        first_argmax.push_back(tuple);
      }
      hash_argmax_tuple(argmax_digest, tuple);
    }
  }
};

struct RankCounts {
  std::uint64_t above = 0;
  std::uint64_t equal = 0;
  std::uint64_t below = 0;
};

RankCounts rank_counts(const LandscapeSummary& summary, unsigned coverage) {
  RankCounts result;
  for (unsigned g = 0; g < summary.histogram.size(); ++g) {
    if (g < coverage) {
      result.below += summary.histogram[g];
    } else if (g == coverage) {
      result.equal = summary.histogram[g];
    } else {
      result.above += summary.histogram[g];
    }
  }
  if (result.above + result.equal + result.below != summary.rows) {
    throw std::runtime_error("rank-count total mismatch");
  }
  return result;
}

std::vector<Mask> make_left_partials(const PrimeMasks& masks) {
  std::vector<Mask> left(kModuli[0] * kModuli[1]);
  std::size_t index = 0;
  for (unsigned t3 = 0; t3 < kModuli[0]; ++t3) {
    for (unsigned t7 = 0; t7 < kModuli[1]; ++t7, ++index) {
      for (std::size_t lane = 0; lane < kWords; ++lane) {
        left[index].word[lane] =
            masks[0][t3].word[lane] | masks[1][t7].word[lane];
      }
    }
  }
  return left;
}

std::vector<Mask> make_right_partials(const PrimeMasks& masks) {
  std::vector<Mask> right(kModuli[2] * kModuli[3]);
  std::size_t index = 0;
  for (unsigned t11 = 0; t11 < kModuli[2]; ++t11) {
    for (unsigned t23 = 0; t23 < kModuli[3]; ++t23, ++index) {
      for (std::size_t lane = 0; lane < kWords; ++lane) {
        right[index].word[lane] =
            masks[2][t11].word[lane] | masks[3][t23].word[lane];
      }
    }
  }
  return right;
}

struct SubsetOptimum {
  unsigned subset_mask = 0;
  std::vector<unsigned> primes;
  std::uint64_t modulus_product = 1;
  unsigned maximum = 0;
  std::uint64_t argmax_count = 0;
  std::vector<unsigned> first_argmax;
};

std::vector<SubsetOptimum> optimize_subsets(const PrimeMasks& masks,
                                            const LandscapeSummary& full) {
  std::vector<SubsetOptimum> results;
  for (unsigned subset = 1; subset < 16; ++subset) {
    SubsetOptimum item;
    item.subset_mask = subset;
    std::vector<unsigned> selected;
    for (unsigned prime_index = 0; prime_index < 4; ++prime_index) {
      if ((subset & (1U << prime_index)) != 0U) {
        selected.push_back(prime_index);
        item.primes.push_back(kPrimes[prime_index]);
        item.modulus_product *= kModuli[prime_index];
      }
    }

    if (subset == 15U) {
      item.maximum = full.maximum;
      item.argmax_count = full.argmax_count;
      for (unsigned x : full.first_argmax.front().value) {
        item.first_argmax.push_back(x);
      }
      results.push_back(std::move(item));
      continue;
    }

    std::vector<unsigned> residues(selected.size(), 0U);
    bool done = false;
    while (!done) {
      unsigned coverage = 0;
      for (std::size_t lane = 0; lane < kWords; ++lane) {
        std::uint64_t bits = 0;
        for (std::size_t j = 0; j < selected.size(); ++j) {
          bits |= masks[selected[j]][residues[j]].word[lane];
        }
        coverage += static_cast<unsigned>(__builtin_popcountll(bits));
      }

      if (item.argmax_count == 0U || coverage > item.maximum) {
        item.maximum = coverage;
        item.argmax_count = 1;
        item.first_argmax = residues;
      } else if (coverage == item.maximum) {
        ++item.argmax_count;
      }

      std::size_t position = residues.size();
      while (position != 0U) {
        --position;
        ++residues[position];
        if (residues[position] < kModuli[selected[position]]) {
          break;
        }
        residues[position] = 0;
      }
      if (position == 0U && residues[0] == 0U) {
        done = true;
      }
    }
    results.push_back(std::move(item));
  }
  return results;
}

void write_tuple(std::ostream& out, const Tuple4& tuple) {
  out << '[' << tuple.value[0] << ',' << tuple.value[1] << ',' << tuple.value[2]
      << ',' << tuple.value[3] << ']';
}

void write_tuples(std::ostream& out, const std::vector<Tuple4>& tuples) {
  out << '[';
  for (std::size_t i = 0; i < tuples.size(); ++i) {
    if (i != 0U) {
      out << ',';
    }
    write_tuple(out, tuples[i]);
  }
  out << ']';
}

void write_histogram(std::ostream& out, const LandscapeSummary& summary) {
  out << '{';
  bool first = true;
  for (unsigned g = 0; g < summary.histogram.size(); ++g) {
    if (summary.histogram[g] == 0U) {
      continue;
    }
    if (!first) {
      out << ',';
    }
    first = false;
    out << '"' << g << "\":" << summary.histogram[g];
  }
  out << '}';
}

void write_rank_counts(std::ostream& out, const RankCounts& rank,
                       std::uint64_t rows) {
  out << "{\"above\":" << rank.above << ",\"equal\":" << rank.equal
      << ",\"below\":" << rank.below << ",\"rank_interval\":["
      << (rank.above + 1U) << ',' << (rank.above + rank.equal)
      << "],\"percentile_definition\":\"100*(below+equal/2)/total; "
         "higher means greater coverage\",\"percentile\":{";
  out << "\"numerator\":" << (100ULL * (2ULL * rank.below + rank.equal))
      << ",\"denominator\":" << (2ULL * rows) << "}}";
}

void write_landscape(std::ostream& out, LandscapeSummary& summary,
                     Sha256& stream_digest, const RankCounts& rank) {
  out << "{\"tuple_count\":" << summary.rows << ",\"minimum\":"
      << summary.minimum << ",\"maximum\":" << summary.maximum
      << ",\"histogram\":";
  write_histogram(out, summary);
  out << ",\"argmax_count\":" << summary.argmax_count
      << ",\"argmax_digest\":\"" << summary.argmax_digest.finish_hex()
      << "\",\"first_100_argmax\":";
  write_tuples(out, summary.first_argmax);
  out << ",\"stream_digest\":\"" << stream_digest.finish_hex()
      << "\",\"n0_counts\":";
  write_rank_counts(out, rank, summary.rows);
  out << '}';
}

double elapsed_seconds(std::chrono::steady_clock::time_point start,
                       std::chrono::steady_clock::time_point end) {
  return std::chrono::duration<double>(end - start).count();
}

std::uint64_t peak_rss_kib() {
  struct rusage usage {};
  if (getrusage(RUSAGE_SELF, &usage) != 0) {
    throw std::runtime_error("getrusage failed");
  }
  // Linux reports ru_maxrss in KiB.  This program's supported replay target is
  // Linux, as recorded by the repository's environment audit.
  return static_cast<std::uint64_t>(usage.ru_maxrss);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 2) {
      std::cerr << "usage: enumerator_b OUTPUT_JSON\n";
      return 2;
    }

    verify_sha256_implementation();

    const auto total_start = std::chrono::steady_clock::now();
    if (kPrimes != std::array<unsigned, 4>{{3, 7, 11, 23}} ||
        kModuli != std::array<unsigned, 4>{{9, 49, 121, 529}}) {
      throw std::runtime_error("fixed P4 constants changed");
    }
    std::uint64_t checked_m4 = 1;
    for (unsigned modulus : kModuli) {
      checked_m4 *= modulus;
    }
    if (checked_m4 != kM4 || checked_m4 != kFullRows) {
      throw std::runtime_error("M4 runtime verification failed");
    }

    const auto coverage_start = std::chrono::steady_clock::now();
    const std::vector<ExponentPair> pairs = make_domain(kCellLow);
    verify_domain(pairs);
    const PrimeMasks masks = construct_pair_centric_masks(pairs);
    verify_pair_centric_masks(pairs, masks);
    const auto coverage_end = std::chrono::steady_clock::now();
    const std::uint64_t coverage_rss = peak_rss_kib();

    const auto partial_start = coverage_end;
    const std::vector<Mask> left = make_left_partials(masks);
    const std::vector<Mask> right = make_right_partials(masks);
    if (left.size() != 441U || right.size() != 64009U) {
      throw std::runtime_error("2+2 partial-union dimensions are wrong");
    }
    const auto partial_end = std::chrono::steady_clock::now();
    const std::uint64_t partial_rss = peak_rss_kib();

    Tuple4 n0{{2, 41, 74, 504}};
    unsigned n0_coverage = 0;
    for (std::size_t lane = 0; lane < kWords; ++lane) {
      const std::uint64_t bits = masks[0][n0.value[0]].word[lane] |
                                 masks[1][n0.value[1]].word[lane] |
                                 masks[2][n0.value[2]].word[lane] |
                                 masks[3][n0.value[3]].word[lane];
      n0_coverage += static_cast<unsigned>(__builtin_popcountll(bits));
    }
    if (n0_coverage != 216U) {
      throw std::runtime_error("committed n0 tuple does not have coverage 216");
    }

    const auto full_start = partial_end;
    LandscapeSummary full;
    LandscapeSummary slice;
    Sha256 full_stream;
    Sha256 slice_stream;
    std::size_t left_index = 0;
    for (unsigned t3 = 0; t3 < kModuli[0]; ++t3) {
      for (unsigned t7 = 0; t7 < kModuli[1]; ++t7, ++left_index) {
        std::size_t right_index = 0;
        for (unsigned t11 = 0; t11 < kModuli[2]; ++t11) {
          for (unsigned t23 = 0; t23 < kModuli[3]; ++t23, ++right_index) {
            unsigned coverage = 0;
            for (std::size_t lane = 0; lane < kWords; ++lane) {
              coverage += static_cast<unsigned>(__builtin_popcountll(
                  left[left_index].word[lane] | right[right_index].word[lane]));
            }
            const Tuple4 tuple{{static_cast<std::uint16_t>(t3),
                                static_cast<std::uint16_t>(t7),
                                static_cast<std::uint16_t>(t11),
                                static_cast<std::uint16_t>(t23)}};
            hash_full_row(full_stream, tuple, coverage);
            full.observe(tuple, coverage);
            if (t3 == 2U) {
              hash_full_row(slice_stream, tuple, coverage);
              slice.observe(tuple, coverage);
            }
          }
        }
      }
    }
    const auto full_end = std::chrono::steady_clock::now();
    const std::uint64_t full_rss = peak_rss_kib();
    if (full.rows != kFullRows || slice.rows != kSliceRows) {
      throw std::runtime_error("full or constrained tuple count mismatch");
    }
    std::uint64_t full_histogram_total = 0;
    std::uint64_t slice_histogram_total = 0;
    for (std::size_t g = 0; g <= kPairCount; ++g) {
      full_histogram_total += full.histogram[g];
      slice_histogram_total += slice.histogram[g];
    }
    if (full_histogram_total != kFullRows ||
        slice_histogram_total != kSliceRows) {
      throw std::runtime_error("histogram total mismatch");
    }
    const RankCounts full_rank = rank_counts(full, n0_coverage);
    const RankCounts slice_rank = rank_counts(slice, n0_coverage);

    const auto subsets_start = full_end;
    const std::vector<SubsetOptimum> subset_optima =
        optimize_subsets(masks, full);
    const auto subsets_end = std::chrono::steady_clock::now();
    const std::uint64_t subsets_rss = peak_rss_kib();
    if (subset_optima.size() != 15U) {
      throw std::runtime_error("did not compute all 15 nonempty subsets");
    }

    std::ofstream output(argv[1], std::ios::binary | std::ios::trunc);
    if (!output) {
      throw std::runtime_error("cannot open output JSON");
    }
    output << "{\n";
    output << "\"schema\":\"a303656-exact-fixed-p4-residue-landscape-certificate-v1\",\n";
    output << "\"implementation\":\"enumerator_b_pair_centric_2plus2_mitm\",\n";
    output << "\"domain\":{\"low\":" << kCellLow << ",\"high\":"
           << kCellHigh << ",\"pair_count\":" << pairs.size()
           << ",\"duplicate_shift_28_pairs\":[[1,2],[3,0]]},\n";
    output << "\"primes\":[3,7,11,23],\n";
    output << "\"moduli\":[9,49,121,529],\n";
    output << "\"M4\":" << checked_m4 << ",\n";
    output << "\"serialization\":{\"description\":\"Each canonical row is "
              "t3,t7,t11,t23,G as five unsigned 16-bit little-endian integers; "
              "tuples are ordered lexicographically with t23 varying fastest; "
              "there is no padding, header, trailer, or extra byte. Argmax digest "
              "rows omit G and are four unsigned 16-bit little-endian integers.\","
              "\"fields\":[\"t3\",\"t7\",\"t11\",\"t23\",\"G\"],"
              "\"integer_width_bits\":16,\"byte_order\":\"little\","
              "\"row_bytes\":10,\"padding_bytes\":0,"
              "\"tuple_order\":\"lexicographic\",\"row_count\":"
           << kFullRows
           << ",\"struct_format\":\"<5H\",\"argmax\":{"
              "\"fields\":[\"t3\",\"t7\",\"t11\",\"t23\"],"
              "\"integer_width_bits\":16,\"byte_order\":\"little\","
              "\"row_bytes\":8,\"padding_bytes\":0,"
              "\"includes_G\":false,\"struct_format\":\"<4H\"}},\n";
    output << "\"full\":";
    write_landscape(output, full, full_stream, full_rank);
    output << ",\n\"t3eq2\":";
    write_landscape(output, slice, slice_stream, slice_rank);
    output << ",\n\"n0\":{\"tuple\":";
    write_tuple(output, n0);
    output << ",\"coverage\":" << n0_coverage << "},\n";
    output << "\"subset_optima\":[";
    for (std::size_t i = 0; i < subset_optima.size(); ++i) {
      if (i != 0U) {
        output << ',';
      }
      const SubsetOptimum& item = subset_optima[i];
      output << "{\"subset_mask\":" << item.subset_mask << ",\"primes\":[";
      for (std::size_t j = 0; j < item.primes.size(); ++j) {
        if (j != 0U) {
          output << ',';
        }
        output << item.primes[j];
      }
      output << "],\"modulus_product\":" << item.modulus_product
             << ",\"maximum\":" << item.maximum << ",\"argmax_count\":"
             << item.argmax_count << ",\"first_argmax\":[";
      for (std::size_t j = 0; j < item.first_argmax.size(); ++j) {
        if (j != 0U) {
          output << ',';
        }
        output << item.first_argmax[j];
      }
      output << "]}";
    }
    output << "],\n";
    output << "\"runtime_checks\":{\"M4_verified\":true,"
              "\"domain_constant_on_cell\":true,"
              "\"all_coverage_bits_exact_one_verified\":true,"
              "\"sha256_known_answer_test_verified\":true,"
              "\"duplicate_shift_28_retained\":true,"
              "\"n0_coverage_216_verified\":true},\n";
    output << "\"timings_seconds\":{" << std::fixed << std::setprecision(6)
           << "\"coverage_set_generation_and_verification\":"
           << elapsed_seconds(coverage_start, coverage_end) << ','
           << "\"partial_union_precomputation\":"
           << elapsed_seconds(partial_start, partial_end) << ','
           << "\"full_landscape_including_t3eq2\":"
           << elapsed_seconds(full_start, full_end) << ','
           << "\"subset_optimization\":"
           << elapsed_seconds(subsets_start, subsets_end) << ','
           << "\"total_before_json_write\":"
           << elapsed_seconds(total_start, subsets_end) << "}\n";
    output << ",\"resources\":{"
              "\"ru_maxrss_unit\":\"KiB; Linux peak-to-date at stage end\","
              "\"coverage_generation\":{"
              "\"wall_seconds\":"
           << elapsed_seconds(coverage_start, coverage_end)
           << ",\"ru_maxrss_kib_at_stage_end\":" << coverage_rss << "},"
              "\"mitm_construction\":{"
              "\"wall_seconds\":"
           << elapsed_seconds(partial_start, partial_end)
           << ",\"ru_maxrss_kib_at_stage_end\":" << partial_rss << "},"
              "\"full_landscape\":{"
              "\"wall_seconds\":"
           << elapsed_seconds(full_start, full_end)
           << ",\"ru_maxrss_kib_at_stage_end\":" << full_rss << "},"
              "\"constrained_slice\":{"
              "\"wall_seconds\":"
           << elapsed_seconds(full_start, full_end)
           << ",\"ru_maxrss_kib_at_stage_end\":" << full_rss
           << ",\"measurement_note\":\"integrated exactly into full landscape pass\"},"
              "\"subset_optimization\":{"
              "\"wall_seconds\":"
           << elapsed_seconds(subsets_start, subsets_end)
           << ",\"ru_maxrss_kib_at_stage_end\":" << subsets_rss << "}}\n";
    output << "}\n";
    output.close();
    if (!output) {
      throw std::runtime_error("failed while writing output JSON");
    }

    std::cerr << "enumerator_b: EXACT FINITE COMPUTATION complete; rows="
              << full.rows << ", max=" << full.maximum
              << ", argmax_count=" << full.argmax_count << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "enumerator_b: ERROR: " << error.what() << '\n';
    return 1;
  }
}
