#include <chrono>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

#include <unistd.h>

namespace {

constexpr const char* kBackendIdentity =
    "k4_ap_backend_a_trial_division_v1";
constexpr std::uint64_t kMaximumSupportedN = 1'000'000'000'000ULL;

struct Options {
  std::string input_path;
  std::string output_path;
  std::string diagnostics_path;
};

struct PanelRow {
  std::int64_t h;
  std::int64_t k;
  std::uint64_t n;
  std::uint64_t expected_active_pairs;
};

struct CountRow {
  PanelRow panel;
  std::uint64_t t;
  std::uint64_t active_pairs;
};

struct Power {
  std::uint32_t exponent;
  std::uint64_t value;
};

std::string usage(const char* argv0) {
  return std::string("usage: ") + argv0 +
         " --input PANEL.csv --output COUNTS.csv"
         " [--diagnostics DIAG.csv]";
}

Options parse_options(int argc, char** argv) {
  Options options;
  for (int i = 1; i < argc; ++i) {
    const std::string arg = argv[i];
    if (arg != "--input" && arg != "--output" &&
        arg != "--diagnostics") {
      throw std::runtime_error("unknown argument: " + arg);
    }
    if (++i >= argc) {
      throw std::runtime_error("missing value for " + arg);
    }
    const std::string value = argv[i];
    if (value.empty()) {
      throw std::runtime_error("empty value for " + arg);
    }
    if (arg == "--input") {
      if (!options.input_path.empty()) {
        throw std::runtime_error("duplicate --input");
      }
      options.input_path = value;
    } else if (arg == "--output") {
      if (!options.output_path.empty()) {
        throw std::runtime_error("duplicate --output");
      }
      options.output_path = value;
    } else {
      if (!options.diagnostics_path.empty()) {
        throw std::runtime_error("duplicate --diagnostics");
      }
      options.diagnostics_path = value;
    }
  }
  if (options.input_path.empty() || options.output_path.empty()) {
    throw std::runtime_error("both --input and --output are required");
  }
  if (options.input_path == options.output_path) {
    throw std::runtime_error("input and output paths must differ");
  }
  if (!options.diagnostics_path.empty() &&
      (options.diagnostics_path == options.input_path ||
       options.diagnostics_path == options.output_path)) {
    throw std::runtime_error("diagnostics path must be distinct");
  }
  return options;
}

std::vector<std::string> split_csv_numeric_row(const std::string& line) {
  std::vector<std::string> fields;
  std::size_t begin = 0;
  while (true) {
    const std::size_t comma = line.find(',', begin);
    fields.push_back(line.substr(begin, comma - begin));
    if (comma == std::string::npos) {
      return fields;
    }
    begin = comma + 1;
  }
}

std::uint64_t parse_u64(const std::string& text, const std::string& field,
                        std::size_t line_number) {
  if (text.empty()) {
    throw std::runtime_error("empty " + field + " at input line " +
                             std::to_string(line_number));
  }
  std::uint64_t value = 0;
  for (const char ch : text) {
    if (ch < '0' || ch > '9') {
      throw std::runtime_error("malformed " + field + " at input line " +
                               std::to_string(line_number));
    }
    const std::uint64_t digit = static_cast<std::uint64_t>(ch - '0');
    if (value > (std::numeric_limits<std::uint64_t>::max() - digit) / 10) {
      throw std::runtime_error("overflow in " + field + " at input line " +
                               std::to_string(line_number));
    }
    value = value * 10 + digit;
  }
  return value;
}

std::int64_t parse_i64(const std::string& text, const std::string& field,
                       std::size_t line_number) {
  if (text.empty()) {
    throw std::runtime_error("empty " + field + " at input line " +
                             std::to_string(line_number));
  }
  const bool negative = text.front() == '-';
  const std::size_t first_digit = negative ? 1 : 0;
  if (first_digit == text.size()) {
    throw std::runtime_error("malformed " + field + " at input line " +
                             std::to_string(line_number));
  }
  const std::uint64_t positive_limit =
      static_cast<std::uint64_t>(std::numeric_limits<std::int64_t>::max());
  const std::uint64_t limit = negative ? positive_limit + 1 : positive_limit;
  std::uint64_t magnitude = 0;
  for (std::size_t i = first_digit; i < text.size(); ++i) {
    const char ch = text[i];
    if (ch < '0' || ch > '9') {
      throw std::runtime_error("malformed " + field + " at input line " +
                               std::to_string(line_number));
    }
    const std::uint64_t digit = static_cast<std::uint64_t>(ch - '0');
    if (magnitude > (limit - digit) / 10) {
      throw std::runtime_error("overflow in " + field + " at input line " +
                               std::to_string(line_number));
    }
    magnitude = magnitude * 10 + digit;
  }
  if (!negative) {
    return static_cast<std::int64_t>(magnitude);
  }
  if (magnitude == positive_limit + 1) {
    return std::numeric_limits<std::int64_t>::min();
  }
  return -static_cast<std::int64_t>(magnitude);
}

std::vector<PanelRow> read_panel(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    throw std::runtime_error("cannot open input panel: " + path);
  }
  std::string line;
  if (!std::getline(input, line)) {
    throw std::runtime_error("input panel is empty");
  }
  if (!line.empty() && line.back() == '\r') {
    line.pop_back();
  }
  if (line != "h,k,n,active_pairs") {
    throw std::runtime_error(
        "input header must be exactly h,k,n,active_pairs");
  }

  std::vector<PanelRow> rows;
  std::unordered_set<std::uint64_t> seen_n;
  std::size_t line_number = 1;
  while (std::getline(input, line)) {
    ++line_number;
    if (!line.empty() && line.back() == '\r') {
      line.pop_back();
    }
    if (line.empty()) {
      throw std::runtime_error("blank input line " +
                               std::to_string(line_number));
    }
    const std::vector<std::string> fields = split_csv_numeric_row(line);
    if (fields.size() != 4) {
      throw std::runtime_error("expected four fields at input line " +
                               std::to_string(line_number));
    }
    PanelRow row{
        parse_i64(fields[0], "h", line_number),
        parse_i64(fields[1], "k", line_number),
        parse_u64(fields[2], "n", line_number),
        parse_u64(fields[3], "active_pairs", line_number),
    };
    if (row.n <= 1) {
      throw std::runtime_error("n must be greater than 1 at input line " +
                               std::to_string(line_number));
    }
    if (row.n > kMaximumSupportedN) {
      throw std::runtime_error(
          "n exceeds backend A declared domain at input line " +
          std::to_string(line_number));
    }
    if (!seen_n.insert(row.n).second) {
      throw std::runtime_error("duplicated n at input line " +
                               std::to_string(line_number));
    }
    rows.push_back(row);
  }
  if (!input.eof()) {
    throw std::runtime_error("I/O error while reading input panel");
  }
  if (rows.empty()) {
    throw std::runtime_error("input panel has no data rows");
  }
  return rows;
}

std::uint64_t integer_sqrt(std::uint64_t value) {
  std::uint64_t low = 0;
  std::uint64_t high = (1ULL << 32);
  while (low + 1 < high) {
    const std::uint64_t middle = low + (high - low) / 2;
    if (middle <= value / middle) {
      low = middle;
    } else {
      high = middle;
    }
  }
  return low;
}

std::vector<std::uint32_t> generate_primes(std::uint64_t max_n) {
  const std::uint64_t limit_u64 = integer_sqrt(max_n);
  if (limit_u64 > std::numeric_limits<std::uint32_t>::max()) {
    throw std::runtime_error("prime-table limit overflow");
  }
  const std::uint32_t limit = static_cast<std::uint32_t>(limit_u64);
  std::vector<bool> composite(static_cast<std::size_t>(limit) + 1, false);
  for (std::uint32_t candidate = 2;
       candidate <= limit / candidate; ++candidate) {
    if (composite[candidate]) {
      continue;
    }
    const std::uint64_t start =
        static_cast<std::uint64_t>(candidate) * candidate;
    for (std::uint64_t multiple = start; multiple <= limit;
         multiple += candidate) {
      composite[static_cast<std::size_t>(multiple)] = true;
    }
  }
  std::vector<std::uint32_t> primes;
  for (std::uint32_t candidate = 2; candidate <= limit; ++candidate) {
    if (!composite[candidate]) {
      primes.push_back(candidate);
    }
  }
  if (limit >= 2 && (primes.empty() || primes.front() != 2)) {
    throw std::runtime_error("internal prime-table construction failure");
  }
  return primes;
}

void validate_prime_table(const std::vector<std::uint32_t>& primes) {
  std::uint32_t previous = 0;
  for (std::size_t i = 0; i < primes.size(); ++i) {
    const std::uint32_t prime = primes[i];
    if (prime <= previous) {
      throw std::runtime_error("prime table is not strictly increasing");
    }
    for (std::size_t j = 0; j < i; ++j) {
      const std::uint32_t divisor = primes[j];
      if (divisor > prime / divisor) {
        break;
      }
      if (prime % divisor == 0) {
        throw std::runtime_error("composite entry in prime table");
      }
    }
    previous = prime;
  }
}

std::uint64_t fingerprint_prime_table(
    const std::vector<std::uint32_t>& primes) {
  std::uint64_t hash = 14695981039346656037ULL;
  for (const std::uint32_t prime : primes) {
    for (unsigned shift = 0; shift < 32; shift += 8) {
      hash ^= static_cast<std::uint8_t>(prime >> shift);
      hash *= 1099511628211ULL;
    }
  }
  return hash;
}

std::vector<Power> generate_powers(std::uint64_t base,
                                   std::uint64_t maximum) {
  std::vector<Power> powers;
  std::uint64_t value = 1;
  std::uint32_t exponent = 0;
  while (value <= maximum) {
    powers.push_back(Power{exponent, value});
    if (value > maximum / base) {
      break;
    }
    value *= base;
    if (exponent == std::numeric_limits<std::uint32_t>::max()) {
      throw std::runtime_error("power exponent overflow");
    }
    ++exponent;
  }
  return powers;
}

bool is_sum_of_two_squares_by_trial_division(
    std::uint64_t remainder, const std::vector<std::uint32_t>& primes) {
  if (remainder == 0) {
    return true;
  }
  std::uint64_t residual = remainder;
  for (const std::uint32_t prime32 : primes) {
    const std::uint64_t prime = prime32;
    if (prime > residual / prime) {
      break;
    }
    if (residual % prime != 0) {
      continue;
    }
    std::uint32_t valuation = 0;
    do {
      residual /= prime;
      ++valuation;
    } while (residual % prime == 0);
    if (prime % 4 == 3 && valuation % 2 == 1) {
      return false;
    }
  }
  // At this point residual is 1 or prime: every possible factor not exceeding
  // sqrt(residual) was deterministically tested using the validated sieve.
  return residual == 1 || residual % 4 != 3;
}

class AtomicCsv {
 public:
  explicit AtomicCsv(const std::string& final_path)
      : final_path_(final_path),
        temporary_path_(final_path + ".tmp." + std::to_string(::getpid())),
        output_(temporary_path_, std::ios::out | std::ios::trunc) {
    if (!output_) {
      throw std::runtime_error("cannot open temporary output: " +
                               temporary_path_);
    }
  }

  AtomicCsv(const AtomicCsv&) = delete;
  AtomicCsv& operator=(const AtomicCsv&) = delete;

  ~AtomicCsv() {
    if (!published_) {
      output_.close();
      std::remove(temporary_path_.c_str());
    }
  }

  std::ofstream& stream() { return output_; }

  void publish() {
    output_.flush();
    if (!output_) {
      throw std::runtime_error("failed writing temporary output: " +
                               temporary_path_);
    }
    output_.close();
    if (std::rename(temporary_path_.c_str(), final_path_.c_str()) != 0) {
      throw std::runtime_error("failed publishing output: " + final_path_);
    }
    published_ = true;
  }

 private:
  std::string final_path_;
  std::string temporary_path_;
  std::ofstream output_;
  bool published_ = false;
};

std::vector<CountRow> evaluate_panel(
    const std::vector<PanelRow>& panel,
    const std::vector<std::uint32_t>& primes,
    const std::vector<Power>& powers3, const std::vector<Power>& powers5,
    AtomicCsv* diagnostics) {
  std::vector<CountRow> results;
  results.reserve(panel.size());
  if (diagnostics != nullptr) {
    diagnostics->stream()
        << "h,k,n,c,d,shift,remainder,winner\n";
  }

  for (const PanelRow& row : panel) {
    std::uint64_t t = 0;
    std::uint64_t active_pairs = 0;
    for (const Power& power3 : powers3) {
      if (power3.value > row.n) {
        break;
      }
      for (const Power& power5 : powers5) {
        if (power5.value > row.n - power3.value) {
          break;
        }
        const std::uint64_t shift = power3.value + power5.value;
        const std::uint64_t remainder = row.n - shift;
        const bool winner =
            is_sum_of_two_squares_by_trial_division(remainder, primes);
        if (active_pairs == std::numeric_limits<std::uint64_t>::max()) {
          throw std::runtime_error("active-pair counter overflow");
        }
        ++active_pairs;
        if (winner) {
          if (t == std::numeric_limits<std::uint64_t>::max()) {
            throw std::runtime_error("T counter overflow");
          }
          ++t;
        }
        if (diagnostics != nullptr) {
          diagnostics->stream()
              << row.h << ',' << row.k << ',' << row.n << ','
              << power3.exponent << ',' << power5.exponent << ',' << shift
              << ',' << remainder << ',' << (winner ? 1 : 0) << '\n';
          if (!diagnostics->stream()) {
            throw std::runtime_error("failed writing diagnostics");
          }
        }
      }
    }
    if (active_pairs != row.expected_active_pairs) {
      throw std::runtime_error(
          "active-pair count mismatch for n=" + std::to_string(row.n) +
          ": expected " + std::to_string(row.expected_active_pairs) +
          ", computed " + std::to_string(active_pairs));
    }
    results.push_back(CountRow{row, t, active_pairs});
  }
  return results;
}

void write_counts(const std::string& path,
                  const std::vector<CountRow>& rows) {
  AtomicCsv output(path);
  output.stream() << "h,k,n,T,active_pairs\n";
  for (const CountRow& row : rows) {
    output.stream() << row.panel.h << ',' << row.panel.k << ',' << row.panel.n
                    << ',' << row.t << ',' << row.active_pairs << '\n';
  }
  output.publish();
}

}  // namespace

int main(int argc, char** argv) {
  const auto started = std::chrono::steady_clock::now();
  try {
    if (argc == 2 && std::string(argv[1]) == "--implementation-id") {
      std::cout << kBackendIdentity << '\n';
      return 0;
    }
    const Options options = parse_options(argc, argv);
    const std::vector<PanelRow> panel = read_panel(options.input_path);
    std::uint64_t maximum_n = 0;
    for (const PanelRow& row : panel) {
      if (row.n > maximum_n) {
        maximum_n = row.n;
      }
    }

    const std::vector<std::uint32_t> primes = generate_primes(maximum_n);
    validate_prime_table(primes);
    const std::vector<Power> powers3 = generate_powers(3, maximum_n);
    const std::vector<Power> powers5 = generate_powers(5, maximum_n);

    std::vector<CountRow> counts;
    if (options.diagnostics_path.empty()) {
      counts = evaluate_panel(panel, primes, powers3, powers5, nullptr);
    } else {
      AtomicCsv diagnostics(options.diagnostics_path);
      counts =
          evaluate_panel(panel, primes, powers3, powers5, &diagnostics);
      diagnostics.publish();
    }
    write_counts(options.output_path, counts);

    const auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
        std::chrono::steady_clock::now() - started);
    std::cerr << "backend_identity=" << kBackendIdentity << '\n'
              << "maximum_supported_n=" << kMaximumSupportedN << '\n'
              << "panel_rows=" << panel.size() << '\n'
              << "prime_limit=" << integer_sqrt(maximum_n) << '\n'
              << "prime_count=" << primes.size() << '\n'
              << "prime_table_fingerprint_fnv1a64="
              << fingerprint_prime_table(primes) << '\n'
              << "elapsed_ms=" << elapsed.count() << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "backend_identity=" << kBackendIdentity << '\n'
              << "error=" << error.what() << '\n'
              << usage(argv[0]) << '\n';
    return 2;
  }
}
