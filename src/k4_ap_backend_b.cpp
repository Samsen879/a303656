#include <algorithm>
#include <charconv>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <optional>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = __uint128_t;

constexpr std::string_view kBackendIdentity =
    "k4_ap_backend_b_cpp17_mr7_brent_rho_v1";
constexpr u64 kDeterministicSeed = UINT64_C(0x6b345a1d93e4c8f7);
constexpr unsigned kMaximumFactorDepth = 128;
constexpr unsigned kRhoAttempts = 96;
constexpr u64 kRhoIterationLimit = UINT64_C(1) << 22;

struct Options {
  std::filesystem::path input;
  std::filesystem::path output;
  std::optional<std::filesystem::path> diagnostics;
};

struct PanelRow {
  std::int64_t h;
  std::int64_t k;
  u64 n;
  std::uint32_t active_pairs;
};

struct CountRow {
  PanelRow input;
  u64 t;
};

struct PrimeMultiplicity {
  u64 prime;
  std::uint32_t multiplicity;
};

struct TwoSquareClassification {
  bool winner;
  std::vector<PrimeMultiplicity> prime_multiplicities;
};

class SplitMix64 {
 public:
  explicit SplitMix64(u64 state) : state_(state) {}

  u64 next() {
    u64 z = (state_ += UINT64_C(0x9e3779b97f4a7c15));
    z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
    return z ^ (z >> 31);
  }

 private:
  u64 state_;
};

[[noreturn]] void fail(const std::string& message) {
  throw std::runtime_error(message);
}

u64 mul_mod(u64 a, u64 b, u64 modulus) {
  if (modulus == 0) {
    fail("internal error: zero modulus");
  }
  return static_cast<u64>((static_cast<u128>(a) * b) % modulus);
}

u64 pow_mod(u64 base, u64 exponent, u64 modulus) {
  u64 result = 1 % modulus;
  base %= modulus;
  while (exponent != 0) {
    if ((exponent & 1U) != 0) {
      result = mul_mod(result, base, modulus);
    }
    exponent >>= 1U;
    if (exponent != 0) {
      base = mul_mod(base, base, modulus);
    }
  }
  return result;
}

bool is_prime_u64(u64 n) {
  if (n < 2) {
    return false;
  }
  constexpr u64 small_primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                                  31, 37};
  for (u64 p : small_primes) {
    if (n == p) {
      return true;
    }
    if (n % p == 0) {
      return false;
    }
  }

  u64 d = n - 1;
  unsigned s = 0;
  while ((d & 1U) == 0) {
    d >>= 1U;
    ++s;
  }

  // This base set is deterministic for every unsigned 64-bit integer.
  constexpr u64 bases[] = {2,       325,      9375,    28178,
                           450775,  9780504,  1795265022};
  for (u64 base : bases) {
    if (base % n == 0) {
      continue;
    }
    u64 x = pow_mod(base, d, n);
    if (x == 1 || x == n - 1) {
      continue;
    }
    bool strong_witness_passed = false;
    for (unsigned r = 1; r < s; ++r) {
      x = mul_mod(x, x, n);
      if (x == n - 1) {
        strong_witness_passed = true;
        break;
      }
    }
    if (!strong_witness_passed) {
      return false;
    }
  }
  return true;
}

u64 absolute_difference(u64 a, u64 b) { return a >= b ? a - b : b - a; }

u64 rho_polynomial(u64 x, u64 c, u64 modulus) {
  const u64 square = mul_mod(x, x, modulus);
  return static_cast<u64>((static_cast<u128>(square) + c) % modulus);
}

u64 pollard_rho_split(u64 n) {
  if (n < 4 || is_prime_u64(n)) {
    fail("internal error: Pollard-Rho called on a non-composite");
  }
  constexpr u64 immediate_divisors[] = {2, 3, 5, 7, 11, 13, 17, 19, 23,
                                        29, 31, 37, 41, 43, 47, 53};
  for (u64 p : immediate_divisors) {
    if (n % p == 0) {
      return p;
    }
  }

  SplitMix64 random(kDeterministicSeed ^ n ^ (n << 17U) ^ (n >> 11U));
  constexpr u64 batch_size = 128;

  for (unsigned attempt = 0; attempt < kRhoAttempts; ++attempt) {
    u64 y = random.next() % (n - 1) + 1;
    const u64 c = random.next() % (n - 1) + 1;
    u64 g = 1;
    u64 r = 1;
    u64 q = 1;
    u64 x = 0;
    u64 ys = 0;
    u64 iterations = 0;

    while (g == 1 && iterations < kRhoIterationLimit) {
      x = y;
      for (u64 i = 0; i < r; ++i) {
        y = rho_polynomial(y, c, n);
      }

      u64 k = 0;
      while (k < r && g == 1) {
        ys = y;
        const u64 block = std::min(batch_size, r - k);
        for (u64 i = 0; i < block; ++i) {
          y = rho_polynomial(y, c, n);
          q = mul_mod(q, absolute_difference(x, y), n);
        }
        iterations += block;
        g = std::gcd(q, n);
        k += block;
        if (iterations >= kRhoIterationLimit) {
          break;
        }
      }

      if (r > kRhoIterationLimit / 2) {
        break;
      }
      r <<= 1U;
    }

    if (g == n) {
      do {
        ys = rho_polynomial(ys, c, n);
        g = std::gcd(absolute_difference(x, ys), n);
        ++iterations;
      } while (g == 1 && iterations < kRhoIterationLimit);
    }

    if (g > 1 && g < n && n % g == 0) {
      return g;
    }
  }

  fail("deterministic Pollard-Rho budget exhausted for " +
       std::to_string(n));
}

std::vector<PrimeMultiplicity> factor_completely(u64 value) {
  if (value == 0) {
    fail("internal error: zero has no finite prime factorization");
  }
  if (value == 1) {
    return {};
  }

  struct PendingFactor {
    u64 value;
    unsigned depth;
  };
  std::vector<PendingFactor> pending{{value, 0}};
  std::vector<u64> prime_factors;

  while (!pending.empty()) {
    const PendingFactor current = pending.back();
    pending.pop_back();
    if (current.value == 1) {
      continue;
    }
    if (is_prime_u64(current.value)) {
      prime_factors.push_back(current.value);
      continue;
    }
    if (current.depth >= kMaximumFactorDepth) {
      fail("factorization depth bound exceeded for " +
           std::to_string(value));
    }
    const u64 divisor = pollard_rho_split(current.value);
    if (divisor <= 1 || divisor >= current.value ||
        current.value % divisor != 0) {
      fail("invalid factor returned while factoring " +
           std::to_string(value));
    }
    pending.push_back({divisor, current.depth + 1});
    pending.push_back({current.value / divisor, current.depth + 1});
  }

  std::sort(prime_factors.begin(), prime_factors.end());
  u128 reconstructed = 1;
  for (u64 prime : prime_factors) {
    if (!is_prime_u64(prime)) {
      fail("composite terminal factor while factoring " +
           std::to_string(value));
    }
    reconstructed *= prime;
    if (reconstructed > std::numeric_limits<u64>::max()) {
      fail("factor reconstruction overflow for " + std::to_string(value));
    }
  }
  if (static_cast<u64>(reconstructed) != value) {
    fail("factor reconstruction mismatch for " + std::to_string(value));
  }

  std::vector<PrimeMultiplicity> result;
  for (u64 prime : prime_factors) {
    if (result.empty() || result.back().prime != prime) {
      result.push_back({prime, 1});
    } else {
      if (result.back().multiplicity ==
          std::numeric_limits<std::uint32_t>::max()) {
        fail("factor multiplicity overflow");
      }
      ++result.back().multiplicity;
    }
  }
  return result;
}

TwoSquareClassification classify_two_squares(u64 remainder) {
  if (remainder == 0) {
    return {true, {}};
  }
  auto factors = factor_completely(remainder);
  bool winner = true;
  for (const auto& factor : factors) {
    if (factor.prime % 4 == 3 && (factor.multiplicity & 1U) != 0) {
      winner = false;
    }
  }
  return {winner, std::move(factors)};
}

std::string strip_carriage_return(std::string line) {
  if (!line.empty() && line.back() == '\r') {
    line.pop_back();
  }
  return line;
}

std::vector<std::string_view> split_csv_row(const std::string& line) {
  std::vector<std::string_view> fields;
  std::size_t start = 0;
  while (true) {
    const std::size_t comma = line.find(',', start);
    if (comma == std::string::npos) {
      fields.emplace_back(line.data() + start, line.size() - start);
      break;
    }
    fields.emplace_back(line.data() + start, comma - start);
    start = comma + 1;
  }
  return fields;
}

template <typename Integer>
Integer parse_integer(std::string_view text, const std::string& context) {
  if (text.empty()) {
    fail("empty integer field: " + context);
  }
  Integer value{};
  const char* begin = text.data();
  const char* end = begin + text.size();
  const auto parsed = std::from_chars(begin, end, value, 10);
  if (parsed.ec != std::errc{} || parsed.ptr != end) {
    fail("malformed or out-of-range integer '" + std::string(text) +
         "': " + context);
  }
  return value;
}

std::vector<PanelRow> read_panel(const std::filesystem::path& path) {
  std::ifstream input(path);
  if (!input) {
    fail("cannot open input: " + path.string());
  }

  std::string line;
  if (!std::getline(input, line)) {
    fail("empty input file: " + path.string());
  }
  line = strip_carriage_return(std::move(line));
  if (line != "h,k,n,active_pairs") {
    fail("input header must be exactly h,k,n,active_pairs");
  }

  std::vector<PanelRow> rows;
  std::unordered_set<u64> seen_n;
  std::size_t line_number = 1;
  while (std::getline(input, line)) {
    ++line_number;
    line = strip_carriage_return(std::move(line));
    if (line.empty()) {
      fail("blank input row at line " + std::to_string(line_number));
    }
    const auto fields = split_csv_row(line);
    if (fields.size() != 4) {
      fail("expected four CSV fields at line " +
           std::to_string(line_number));
    }
    const std::string prefix = "line " + std::to_string(line_number) + " ";
    PanelRow row{
        parse_integer<std::int64_t>(fields[0], prefix + "h"),
        parse_integer<std::int64_t>(fields[1], prefix + "k"),
        parse_integer<u64>(fields[2], prefix + "n"),
        parse_integer<std::uint32_t>(fields[3], prefix + "active_pairs")};
    if (row.n == 0) {
      fail("n must be positive at line " + std::to_string(line_number));
    }
    if (row.active_pairs == 0) {
      fail("active_pairs must be positive at line " +
           std::to_string(line_number));
    }
    if (!seen_n.insert(row.n).second) {
      fail("duplicated n input: " + std::to_string(row.n));
    }
    rows.push_back(row);
  }
  if (!input.eof()) {
    fail("I/O failure while reading input: " + path.string());
  }
  if (rows.empty()) {
    fail("input contains no panel rows");
  }
  return rows;
}

std::vector<u64> powers_not_exceeding(u64 base, u64 limit) {
  if (base < 2) {
    fail("internal error: invalid power base");
  }
  std::vector<u64> powers;
  u64 value = 1;
  while (value <= limit) {
    powers.push_back(value);
    if (value > limit / base) {
      break;
    }
    value *= base;
  }
  return powers;
}

std::string factor_string(const TwoSquareClassification& classification,
                          u64 remainder) {
  if (remainder == 0) {
    return "ZERO";
  }
  if (classification.prime_multiplicities.empty()) {
    return "1";
  }
  std::string result;
  for (const auto& entry : classification.prime_multiplicities) {
    if (!result.empty()) {
      result.push_back(';');
    }
    result += std::to_string(entry.prime);
    result.push_back('^');
    result += std::to_string(entry.multiplicity);
  }
  return result;
}

CountRow evaluate_row(const PanelRow& row, std::ofstream* diagnostics) {
  const auto powers3 = powers_not_exceeding(3, row.n);
  const auto powers5 = powers_not_exceeding(5, row.n);
  std::unordered_map<u64, TwoSquareClassification> per_point_cache;
  per_point_cache.reserve(row.active_pairs);

  u64 t = 0;
  u64 enumerated_pairs = 0;
  for (std::size_t c = 0; c < powers3.size(); ++c) {
    for (std::size_t d = 0; d < powers5.size(); ++d) {
      if (powers3[c] > row.n - powers5[d]) {
        continue;
      }
      const u64 shift = powers3[c] + powers5[d];
      const u64 remainder = row.n - shift;
      ++enumerated_pairs;

      auto found = per_point_cache.find(remainder);
      if (found == per_point_cache.end()) {
        found = per_point_cache
                    .emplace(remainder, classify_two_squares(remainder))
                    .first;
      }
      const TwoSquareClassification& classification = found->second;
      if (classification.winner) {
        ++t;
      }
      if (diagnostics != nullptr) {
        *diagnostics << row.h << ',' << row.k << ',' << row.n << ',' << c
                     << ',' << d << ',' << shift << ',' << remainder << ','
                     << (classification.winner ? "WINNER" : "LOSER") << ','
                     << factor_string(classification, remainder) << '\n';
        if (!*diagnostics) {
          fail("I/O failure while writing diagnostics");
        }
      }
    }
  }

  if (enumerated_pairs != row.active_pairs) {
    fail("active-pair mismatch for n=" + std::to_string(row.n) +
         ": input=" + std::to_string(row.active_pairs) +
         " enumerated=" + std::to_string(enumerated_pairs));
  }
  return {row, t};
}

Options parse_options(int argc, char** argv) {
  Options options;
  bool have_input = false;
  bool have_output = false;
  for (int i = 1; i < argc; ++i) {
    const std::string_view argument(argv[i]);
    auto consume_value = [&](std::string_view name) -> std::filesystem::path {
      if (++i >= argc) {
        fail("missing value for " + std::string(name));
      }
      const std::string_view value(argv[i]);
      if (value.empty()) {
        fail("empty value for " + std::string(name));
      }
      return std::filesystem::path(value);
    };

    if (argument == "--input") {
      if (have_input) {
        fail("duplicate --input option");
      }
      options.input = consume_value(argument);
      have_input = true;
    } else if (argument == "--output") {
      if (have_output) {
        fail("duplicate --output option");
      }
      options.output = consume_value(argument);
      have_output = true;
    } else if (argument == "--diagnostics") {
      if (options.diagnostics.has_value()) {
        fail("duplicate --diagnostics option");
      }
      options.diagnostics = consume_value(argument);
    } else {
      fail("unknown option: " + std::string(argument));
    }
  }
  if (!have_input || !have_output) {
    fail("usage: k4_ap_backend_b --input PANEL.csv --output COUNTS.csv "
         "[--diagnostics DIAGNOSTICS.csv]");
  }
  if (options.input == options.output ||
      (options.diagnostics.has_value() &&
       (options.input == *options.diagnostics ||
        options.output == *options.diagnostics))) {
    fail("input, output, and diagnostics paths must be distinct");
  }
  return options;
}

void replace_file(const std::filesystem::path& temporary,
                  const std::filesystem::path& destination) {
  std::error_code error;
  std::filesystem::rename(temporary, destination, error);
  if (error) {
    fail("cannot install output " + destination.string() + ": " +
         error.message());
  }
}

}  // namespace

int main(int argc, char** argv) {
  if (argc == 2 && std::string_view(argv[1]) == "--implementation-id") {
    std::cout << kBackendIdentity << '\n';
    return 0;
  }
  std::cerr << "backend_identity=" << kBackendIdentity << '\n';
  std::optional<std::filesystem::path> count_temporary;
  std::optional<std::filesystem::path> diagnostic_temporary;
  try {
    const Options options = parse_options(argc, argv);
    const auto panel = read_panel(options.input);

    std::ofstream diagnostics;
    if (options.diagnostics.has_value()) {
      diagnostic_temporary =
          std::filesystem::path(options.diagnostics->string() + ".tmp");
      diagnostics.open(*diagnostic_temporary, std::ios::trunc);
      if (!diagnostics) {
        fail("cannot open diagnostics temporary file: " +
             diagnostic_temporary->string());
      }
      diagnostics
          << "h,k,n,c,d,shift,remainder,classification,prime_factorization\n";
    }

    std::vector<CountRow> counts;
    counts.reserve(panel.size());
    for (const auto& row : panel) {
      counts.push_back(evaluate_row(
          row, options.diagnostics.has_value() ? &diagnostics : nullptr));
    }
    if (diagnostics.is_open()) {
      diagnostics.close();
      if (!diagnostics) {
        fail("I/O failure while closing diagnostics temporary file");
      }
    }

    count_temporary = std::filesystem::path(options.output.string() + ".tmp");
    {
      std::ofstream output(*count_temporary, std::ios::trunc);
      if (!output) {
        fail("cannot open output temporary file: " +
             count_temporary->string());
      }
      output << "h,k,n,T,active_pairs\n";
      for (const auto& count : counts) {
        output << count.input.h << ',' << count.input.k << ',' << count.input.n
               << ',' << count.t << ',' << count.input.active_pairs << '\n';
      }
      output.close();
      if (!output) {
        fail("I/O failure while closing output temporary file");
      }
    }

    replace_file(*count_temporary, options.output);
    count_temporary.reset();
    if (options.diagnostics.has_value()) {
      replace_file(*diagnostic_temporary, *options.diagnostics);
      diagnostic_temporary.reset();
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    std::error_code ignored;
    if (count_temporary.has_value()) {
      std::filesystem::remove(*count_temporary, ignored);
    }
    if (diagnostic_temporary.has_value()) {
      std::filesystem::remove(*diagnostic_temporary, ignored);
    }
    return 2;
  }
}
