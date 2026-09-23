#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

class Bitset {
 public:
  explicit Bitset(std::uint64_t max_value)
      : max_value_(max_value), words_((max_value + 64) / 64, 0) {}

  void set(std::uint64_t n) { words_.at(n >> 6) |= std::uint64_t{1} << (n & 63); }
  bool get(std::uint64_t n) const {
    return n <= max_value_ && ((words_[n >> 6] >> (n & 63)) & 1U);
  }
  std::uint64_t max_value() const { return max_value_; }

  void or_shifted(const Bitset& source, std::uint64_t shift) {
    if (shift > max_value_) return;
    const std::uint64_t word_shift = shift >> 6;
    const unsigned bit_shift = static_cast<unsigned>(shift & 63);
    for (std::uint64_t i = 0; i < source.words_.size(); ++i) {
      const std::uint64_t value = source.words_[i];
      if (!value) continue;
      const std::uint64_t j = i + word_shift;
      if (j < words_.size()) words_[j] |= value << bit_shift;
      if (bit_shift && j + 1 < words_.size()) words_[j + 1] |= value >> (64 - bit_shift);
    }
    const unsigned used = static_cast<unsigned>((max_value_ + 1) & 63);
    if (used) words_.back() &= (std::uint64_t{1} << used) - 1;
  }

 private:
  std::uint64_t max_value_;
  std::vector<std::uint64_t> words_;
};

static std::vector<std::uint64_t> powers(std::uint64_t base, std::uint64_t bound) {
  std::vector<std::uint64_t> result;
  for (std::uint64_t value = 1; value <= bound;) {
    result.push_back(value);
    if (value > bound / base) break;
    value *= base;
  }
  return result;
}

static Bitset enumerate_sums_of_two_squares(std::uint64_t bound) {
  Bitset result(bound);
  const auto root = static_cast<std::uint64_t>(std::sqrt(static_cast<long double>(bound)));
  std::vector<std::uint64_t> squares(root + 1);
  for (std::uint64_t i = 0; i <= root; ++i) squares[i] = i * i;
  for (std::uint64_t a = 0; a <= root; ++a) {
    const std::uint64_t remaining = bound - squares[a];
    const auto b_max = static_cast<std::uint64_t>(std::sqrt(static_cast<long double>(remaining)));
    for (std::uint64_t b = 0; b <= b_max; ++b) result.set(squares[a] + squares[b]);
  }
  return result;
}

static std::vector<int> compute_D(std::uint64_t m, const Bitset& t3,
                                  const std::vector<std::uint64_t>& powers5) {
  std::vector<int> result;
  for (std::size_t d = 0; d < powers5.size() && powers5[d] <= m; ++d) {
    if (t3.get(m - powers5[d])) result.push_back(static_cast<int>(d));
  }
  return result;
}

static void write_array(std::ostream& out, const std::vector<int>& values) {
  out << '[';
  for (std::size_t i = 0; i < values.size(); ++i) {
    if (i) out << ',';
    out << values[i];
  }
  out << ']';
}

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "usage: support_scanner SCAN_LIMIT SUPPORT_LIMIT OUTPUT_JSON\n";
    return 2;
  }
  const std::uint64_t scan_limit = std::stoull(argv[1]);
  const std::uint64_t support_limit = std::stoull(argv[2]);
  const std::string output = argv[3];
  if (scan_limit < 2 || support_limit < 5 * scan_limit + 3)
    throw std::runtime_error("invalid bounds");

  const auto start = std::chrono::steady_clock::now();
  Bitset s2 = enumerate_sums_of_two_squares(support_limit);
  const auto after_s2 = std::chrono::steady_clock::now();
  Bitset t3(support_limit);
  for (auto p3 : powers(3, support_limit)) t3.or_shifted(s2, p3);
  const auto after_t3 = std::chrono::steady_clock::now();
  const auto p5 = powers(5, support_limit);

  std::uint64_t first_failure = 0;
  std::uint64_t tested_sources = 0;
  for (std::uint64_t m = 2; m <= scan_limit; ++m) {
    bool source = false;
    bool transfer = false;
    const std::uint64_t target = 5 * m + 3;
    for (std::size_t d = 0; d < p5.size() && p5[d] <= m; ++d) {
      if (!t3.get(m - p5[d])) continue;
      source = true;
      if (d + 1 < p5.size() && p5[d + 1] <= target && t3.get(target - p5[d + 1])) {
        transfer = true;
        break;
      }
    }
    if (source) ++tested_sources;
    if (source && !transfer) {
      first_failure = m;
      break;
    }
  }
  const auto finish = std::chrono::steady_clock::now();

  std::vector<std::uint64_t> candidates;
  for (const std::uint64_t candidate : {std::uint64_t{7963079}, std::uint64_t{8984426}})
    if (5 * candidate + 3 <= support_limit) candidates.push_back(candidate);
  std::ofstream out(output);
  out << "{\n"
      << "  \"engine\": \"direct enumeration of x^2+y^2 support plus bitset shifts by 3^c\",\n"
      << "  \"scan_domain\": {\"minimum\": 2, \"maximum\": " << scan_limit
      << ", \"predicate\": \"D(m) nonempty\"},\n"
      << "  \"support_limit\": " << support_limit << ",\n"
      << "  \"tested_representable_sources_through_failure\": " << tested_sources << ",\n"
      << "  \"first_failure\": " << first_failure << ",\n"
      << "  \"candidates\": [\n";
  for (std::size_t i = 0; i < candidates.size(); ++i) {
    const auto m = candidates[i];
    const auto n = 5 * m + 3;
    const auto dm = compute_D(m, t3, p5);
    const auto dn = compute_D(n, t3, p5);
    std::vector<int> shifted;
    for (int d : dm) shifted.push_back(d + 1);
    std::vector<int> intersection;
    std::set_intersection(shifted.begin(), shifted.end(), dn.begin(), dn.end(),
                          std::back_inserter(intersection));
    out << "    {\"m\": " << m << ", \"five_m_plus_three\": " << n << ", \"D_m\": ";
    write_array(out, dm);
    out << ", \"D_5m3\": "; write_array(out, dn);
    out << ", \"shifted_D_m\": "; write_array(out, shifted);
    out << ", \"intersection\": "; write_array(out, intersection);
    out << '}' << (i + 1 == candidates.size() ? "\n" : ",\n");
  }
  out << "  ]\n}\n";
  out.close();
  std::cout << "first_failure=" << first_failure
            << " s2_seconds=" << std::chrono::duration<double>(after_s2 - start).count()
            << " t3_seconds=" << std::chrono::duration<double>(after_t3 - after_s2).count()
            << " scan_seconds=" << std::chrono::duration<double>(finish - after_t3).count()
            << " total_seconds=" << std::chrono::duration<double>(finish - start).count()
            << " output=" << output << "\n";
}
