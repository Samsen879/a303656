// Independent, factorization-free direct oracle for the bounded K4 AP pilot.
//
// This implementation intentionally shares no factorization or two-square
// classification helper with either sparse counting backend.  For every
// remainder it walks the exact monotone boundary a^2 + b^2 = remainder,
// returning the first (and therefore canonical least-a) witness with a <= b.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <optional>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr const char* IMPLEMENTATION_ID = "k4_ap_direct_oracle_v1";
constexpr uint64_t N0 = UINT64_C(240000005594);
constexpr uint64_t M4 = UINT64_C(28227969);
constexpr uint32_t EXPECTED_ACTIVE_PAIRS = 407;
constexpr int64_t K_MIN = -128;
constexpr int64_t K_MAX = 128;
constexpr std::array<int64_t, 5> ALLOWED_H = {-720, -360, 0, 360, 720};

struct InputPoint {
    int64_t h;
    int64_t k;
    uint64_t n;
    uint32_t active_pairs;
    uint32_t expected_T;
};

struct SourcePair {
    uint32_t c;
    uint32_t d;
    uint64_t shift;
};

struct Winner {
    SourcePair source;
    uint64_t remainder;
    uint64_t a;
    uint64_t b;
};

struct OutputPoint {
    InputPoint input;
    uint32_t T;
    std::vector<Winner> winners;
    double elapsed_seconds;
};

[[noreturn]] void fail(const std::string& message) {
    throw std::runtime_error(message);
}

uint64_t parse_u64(const std::string& text, const char* field) {
    if (text.empty()) fail(std::string(field) + " is empty");
    uint64_t value = 0;
    for (char ch : text) {
        if (ch < '0' || ch > '9') fail(std::string(field) + " is not an unsigned decimal integer");
        const uint32_t digit = static_cast<uint32_t>(ch - '0');
        if (value > (std::numeric_limits<uint64_t>::max() - digit) / 10) {
            fail(std::string(field) + " overflows uint64");
        }
        value = value * 10 + digit;
    }
    return value;
}

int64_t parse_i64(const std::string& text, const char* field) {
    if (text.empty()) fail(std::string(field) + " is empty");
    size_t offset = 0;
    bool negative = false;
    if (text[0] == '-') {
        negative = true;
        offset = 1;
    }
    if (offset == text.size()) fail(std::string(field) + " has no decimal digits");
    uint64_t magnitude = 0;
    for (; offset < text.size(); ++offset) {
        const char ch = text[offset];
        if (ch < '0' || ch > '9') fail(std::string(field) + " is not a signed decimal integer");
        const uint32_t digit = static_cast<uint32_t>(ch - '0');
        if (magnitude > (UINT64_C(9223372036854775808) - digit) / 10) {
            fail(std::string(field) + " overflows int64");
        }
        magnitude = magnitude * 10 + digit;
    }
    if (!negative) {
        if (magnitude > static_cast<uint64_t>(std::numeric_limits<int64_t>::max())) {
            fail(std::string(field) + " overflows int64");
        }
        return static_cast<int64_t>(magnitude);
    }
    if (magnitude == UINT64_C(9223372036854775808)) return std::numeric_limits<int64_t>::min();
    return -static_cast<int64_t>(magnitude);
}

std::vector<std::string> split_csv(const std::string& line) {
    std::vector<std::string> fields;
    size_t start = 0;
    for (;;) {
        const size_t comma = line.find(',', start);
        fields.push_back(line.substr(start, comma == std::string::npos ? comma : comma - start));
        if (comma == std::string::npos) break;
        start = comma + 1;
    }
    return fields;
}

uint64_t expected_n(int64_t h, int64_t k) {
    const __int128_t value = static_cast<__int128_t>(N0) + h + static_cast<__int128_t>(k) * M4;
    if (value <= 1 || value > std::numeric_limits<uint64_t>::max()) fail("panel formula overflows uint64");
    return static_cast<uint64_t>(value);
}

std::vector<InputPoint> read_points(const std::string& path) {
    std::ifstream stream(path);
    if (!stream) fail("cannot open input CSV: " + path);
    std::string line;
    if (!std::getline(stream, line) || line != "h,k,n,active_pairs,expected_T") {
        fail("input CSV header must be exactly h,k,n,active_pairs,expected_T");
    }
    std::vector<InputPoint> result;
    std::set<uint64_t> seen_n;
    std::set<std::pair<int64_t, int64_t>> seen_hk;
    size_t line_number = 1;
    while (std::getline(stream, line)) {
        ++line_number;
        if (line.empty()) fail("blank input CSV row at line " + std::to_string(line_number));
        const auto fields = split_csv(line);
        if (fields.size() != 5) fail("input CSV row must have five fields at line " + std::to_string(line_number));
        const int64_t h = parse_i64(fields[0], "h");
        const int64_t k = parse_i64(fields[1], "k");
        const uint64_t n = parse_u64(fields[2], "n");
        const uint64_t active = parse_u64(fields[3], "active_pairs");
        const uint64_t expected_T = parse_u64(fields[4], "expected_T");
        if (std::find(ALLOWED_H.begin(), ALLOWED_H.end(), h) == ALLOWED_H.end()) fail("altered h in direct panel");
        if (k < K_MIN || k > K_MAX) fail("altered/out-of-range k in direct panel");
        if (n != expected_n(h, k)) fail("n does not equal n0+h+k*M4 in direct panel");
        if (active != EXPECTED_ACTIVE_PAIRS) fail("incorrect active-pair count in direct panel");
        if (expected_T > EXPECTED_ACTIVE_PAIRS) fail("expected_T exceeds active-pair count");
        if (!seen_n.insert(n).second) fail("duplicated n in direct panel");
        if (!seen_hk.insert({h, k}).second) fail("duplicated h,k in direct panel");
        result.push_back(InputPoint{h, k, n, static_cast<uint32_t>(active), static_cast<uint32_t>(expected_T)});
    }
    if (!stream.eof()) fail("I/O error while reading input CSV");
    if (result.empty()) fail("direct panel must contain at least one point");
    return result;
}

uint64_t floor_sqrt(uint64_t value) {
    // Restoring binary square root.  Every comparison is performed in
    // uint128, so no rounded floating-point value participates.
    uint64_t low = 0;
    uint64_t high = UINT64_C(1) << 32;
    while (low + 1 < high) {
        const uint64_t middle = low + (high - low) / 2;
        if (static_cast<__uint128_t>(middle) * middle <= value) low = middle;
        else high = middle;
    }
    return low;
}

std::optional<std::pair<uint64_t, uint64_t>> canonical_two_squares(uint64_t remainder) {
    if (remainder == 0) return std::make_pair(UINT64_C(0), UINT64_C(0));
    uint64_t a = 0;
    uint64_t b = floor_sqrt(remainder);
    __uint128_t a2 = 0;
    __uint128_t b2 = static_cast<__uint128_t>(b) * b;
    while (a <= b) {
        const __uint128_t sum = a2 + b2;
        if (sum == remainder) return std::make_pair(a, b);
        if (sum > remainder) {
            // (b-1)^2 = b^2 - (2b-1), with b>0 in this branch.
            if (b == 0) fail("internal monotone square-search underflow");
            b2 -= static_cast<__uint128_t>(2) * b - 1;
            --b;
        } else {
            // (a+1)^2 = a^2 + (2a+1).
            a2 += static_cast<__uint128_t>(2) * a + 1;
            ++a;
        }
    }
    return std::nullopt;
}

std::vector<uint64_t> powers(uint64_t base, uint64_t limit) {
    std::vector<uint64_t> values;
    uint64_t value = 1;
    for (;;) {
        values.push_back(value);
        if (value > limit / base) break;
        value *= base;
        if (value > limit) break;
    }
    return values;
}

std::vector<SourcePair> active_sources(uint64_t n) {
    const auto threes = powers(3, n);
    const auto fives = powers(5, n);
    std::vector<SourcePair> result;
    for (size_t c = 0; c < threes.size(); ++c) {
        for (size_t d = 0; d < fives.size(); ++d) {
            const __uint128_t shift = static_cast<__uint128_t>(threes[c]) + fives[d];
            if (shift <= n) {
                if (c > std::numeric_limits<uint32_t>::max() || d > std::numeric_limits<uint32_t>::max()) {
                    fail("exponent index overflow");
                }
                result.push_back(SourcePair{static_cast<uint32_t>(c), static_cast<uint32_t>(d), static_cast<uint64_t>(shift)});
            }
        }
    }
    return result;
}

OutputPoint evaluate(const InputPoint& input) {
    const auto started = std::chrono::steady_clock::now();
    const auto sources = active_sources(input.n);
    if (sources.size() != input.active_pairs) fail("independently generated active-pair count mismatch");

    std::map<uint64_t, std::vector<SourcePair>> by_shift;
    for (const auto& source : sources) by_shift[source.shift].push_back(source);
    if (by_shift.size() != EXPECTED_ACTIVE_PAIRS - 1) fail("expected exactly one duplicate shift in activation cell");
    const auto duplicate = by_shift.find(28);
    if (duplicate == by_shift.end() || duplicate->second.size() != 2) fail("duplicate shift 28 source multiplicity mismatch");

    std::vector<Winner> winners;
    for (const auto& [shift, source_list] : by_shift) {
        const uint64_t remainder = input.n - shift;
        const auto witness = canonical_two_squares(remainder);
        if (!witness.has_value()) continue;
        for (const auto& source : source_list) {
            winners.push_back(Winner{source, remainder, witness->first, witness->second});
        }
    }
    std::sort(winners.begin(), winners.end(), [](const Winner& left, const Winner& right) {
        return std::tie(left.source.c, left.source.d) < std::tie(right.source.c, right.source.d);
    });
    if (winners.size() > std::numeric_limits<uint32_t>::max()) fail("T overflows uint32");
    const uint32_t T = static_cast<uint32_t>(winners.size());
    const double elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    return OutputPoint{input, T, std::move(winners), elapsed};
}

void write_json(const std::string& path, const std::vector<OutputPoint>& points, bool agreement) {
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) fail("cannot open output JSON: " + path);
    out << "{\n"
        << "  \"schema\": \"a303656-k4-ap-direct-verification-v1\",\n"
        << "  \"implementation_id\": \"" << IMPLEMENTATION_ID << "\",\n"
        << "  \"method\": \"factorization-free exact monotone boundary enumeration; canonical least-a witness\",\n"
        << "  \"n0\": " << N0 << ",\n"
        << "  \"M4\": " << M4 << ",\n"
        << "  \"expected_active_pair_count\": " << EXPECTED_ACTIVE_PAIRS << ",\n"
        << "  \"point_count\": " << points.size() << ",\n"
        << "  \"all_points_processed\": true,\n"
        << "  \"expected_T_agreement\": " << (agreement ? "true" : "false") << ",\n"
        << "  \"points\": [\n";
    for (size_t index = 0; index < points.size(); ++index) {
        const auto& point = points[index];
        out << "    {\"h\": " << point.input.h
            << ", \"k\": " << point.input.k
            << ", \"n\": " << point.input.n
            << ", \"active_pair_count\": " << point.input.active_pairs
            << ", \"expected_T\": " << point.input.expected_T
            << ", \"T\": " << point.T
            << ", \"expected_T_match\": " << (point.T == point.input.expected_T ? "true" : "false")
            << ", \"elapsed_seconds\": " << std::fixed << std::setprecision(9) << point.elapsed_seconds
            << ", \"winning_exponent_pairs\": [";
        for (size_t winner_index = 0; winner_index < point.winners.size(); ++winner_index) {
            const auto& winner = point.winners[winner_index];
            if (winner_index) out << ',';
            out << "{\"c\":" << winner.source.c
                << ",\"d\":" << winner.source.d
                << ",\"shift\":" << winner.source.shift
                << ",\"remainder\":" << winner.remainder
                << ",\"a\":" << winner.a
                << ",\"b\":" << winner.b << '}';
        }
        out << "]}" << (index + 1 == points.size() ? "\n" : ",\n");
    }
    out << "  ]\n}\n";
    if (!out) fail("I/O error while writing output JSON");
}

void self_test() {
    const std::array<std::tuple<uint64_t, bool, uint64_t, uint64_t>, 12> cases = {{
        {0, true, 0, 0}, {1, true, 0, 1}, {2, true, 1, 1}, {3, false, 0, 0},
        {4, true, 0, 2}, {5, true, 1, 2}, {7, false, 0, 0}, {8, true, 2, 2},
        {25, true, 0, 5}, {50, true, 1, 7}, {65, true, 1, 8}, {67, false, 0, 0},
    }};
    for (const auto& [remainder, represented, a, b] : cases) {
        const auto actual = canonical_two_squares(remainder);
        if (actual.has_value() != represented) fail("self-test representability mismatch");
        if (actual.has_value() && *actual != std::make_pair(a, b)) fail("self-test canonical witness mismatch");
    }
    const auto source = active_sources(N0);
    if (source.size() != EXPECTED_ACTIVE_PAIRS) fail("self-test active-pair count mismatch");
    size_t duplicate_28 = 0;
    for (const auto& item : source) if (item.shift == 28) ++duplicate_28;
    if (duplicate_28 != 2) fail("self-test duplicate shift mismatch");
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--implementation-id") {
            std::cout << IMPLEMENTATION_ID << '\n';
            return 0;
        }
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            self_test();
            std::cout << "K4_AP_DIRECT_ORACLE_SELF_TEST_PASS\n";
            return 0;
        }
        if (argc != 5 || std::string(argv[1]) != "--input" || std::string(argv[3]) != "--output") {
            std::cerr << "usage: k4_ap_direct_oracle --input DIRECT_PANEL.csv --output DIRECT.json\n";
            return 2;
        }
        const auto inputs = read_points(argv[2]);
        std::vector<OutputPoint> outputs;
        outputs.reserve(inputs.size());
        bool agreement = true;
        for (const auto& input : inputs) {
            auto output = evaluate(input);
            if (output.T != input.expected_T) agreement = false;
            outputs.push_back(std::move(output));
        }
        write_json(argv[4], outputs, agreement);
        if (!agreement) {
            std::cerr << "ERROR direct T disagrees with expected_T; discrepancy JSON retained\n";
            return 3;
        }
        std::cout << "K4_AP_DIRECT_ORACLE_PASS points=" << outputs.size() << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR " << error.what() << '\n';
        return 2;
    }
}
