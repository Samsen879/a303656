// Fixed-P4 census adapter for the existing factorization-free direct oracle.
//
// The two-square core is the same exact monotone-boundary method used by
// k4_ap_direct_oracle.cpp: for each remainder it returns the canonical least-a
// witness with 0 <= a <= b.  This adapter changes only the panel contract and
// parallel scheduling; results are serialized in input order.

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <mutex>
#include <optional>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <tuple>
#include <utility>
#include <vector>

namespace {

constexpr const char* IMPLEMENTATION_ID = "p4_census_direct_oracle_adapter_v1";
constexpr std::uint64_t A = UINT64_C(183968950234);
constexpr std::uint64_t B = UINT64_C(246731069451);
constexpr std::uint64_t N0 = UINT64_C(240000005594);
constexpr std::uint32_t CLASS_COUNT = 87;
constexpr std::uint32_t PAIR_COUNT = 407;

struct Options {
    std::string input;
    std::string output;
    std::uint32_t jobs = 1;
};

struct InputPoint {
    std::uint32_t class_index;
    std::uint32_t point_index;
    std::uint64_t n;
    std::uint32_t active_pairs;
    std::uint32_t expected_t;
};

struct SourcePair {
    std::uint32_t c;
    std::uint32_t d;
    std::uint64_t shift;
};

struct Winner {
    SourcePair source;
    std::uint64_t remainder;
    std::uint64_t a;
    std::uint64_t b;
};

struct OutputPoint {
    InputPoint input;
    std::vector<Winner> winners;
};

[[noreturn]] void fail(const std::string& message) { throw std::runtime_error(message); }

std::uint64_t parse_u64(const std::string& text, const char* field) {
    if (text.empty() || (text.size() > 1 && text.front() == '0')) fail(std::string("malformed ") + field);
    std::uint64_t value = 0;
    for (const char ch : text) {
        if (ch < '0' || ch > '9') fail(std::string("malformed ") + field);
        const auto digit = static_cast<std::uint32_t>(ch - '0');
        if (value > (std::numeric_limits<std::uint64_t>::max() - digit) / 10) fail(std::string("overflow in ") + field);
        value = value * 10 + digit;
    }
    return value;
}

std::vector<std::string> split_csv(const std::string& line) {
    std::vector<std::string> fields;
    std::size_t begin = 0;
    while (true) {
        const std::size_t comma = line.find(',', begin);
        fields.push_back(line.substr(begin, comma - begin));
        if (comma == std::string::npos) return fields;
        begin = comma + 1;
    }
}

Options parse_options(int argc, char** argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        const std::string argument = argv[i];
        if (argument != "--input" && argument != "--output" && argument != "--jobs") fail("unknown option: " + argument);
        if (++i >= argc) fail("missing value for " + argument);
        const std::string value = argv[i];
        if (argument == "--input") options.input = value;
        else if (argument == "--output") options.output = value;
        else {
            const auto parsed = parse_u64(value, "jobs");
            if (parsed == 0 || parsed > 256) fail("jobs must be in [1,256]");
            options.jobs = static_cast<std::uint32_t>(parsed);
        }
    }
    if (options.input.empty() || options.output.empty() || options.input == options.output) fail("distinct --input and --output are required");
    return options;
}

std::vector<InputPoint> read_points(const std::string& path) {
    std::ifstream stream(path);
    if (!stream) fail("cannot open direct-oracle panel: " + path);
    std::string line;
    if (!std::getline(stream, line) || line != "class_index,point_index,n,active_pairs,expected_T") fail("direct-oracle panel header mismatch");
    std::vector<InputPoint> points;
    std::set<std::pair<std::uint32_t, std::uint32_t>> identities;
    std::set<std::uint64_t> integers;
    while (std::getline(stream, line)) {
        if (line.empty()) fail("blank direct-oracle panel row");
        const auto fields = split_csv(line);
        if (fields.size() != 5) fail("direct-oracle panel row width mismatch");
        const auto class_index64 = parse_u64(fields[0], "class_index");
        const auto point_index64 = parse_u64(fields[1], "point_index");
        const auto n = parse_u64(fields[2], "n");
        const auto active64 = parse_u64(fields[3], "active_pairs");
        const auto expected64 = parse_u64(fields[4], "expected_T");
        if (class_index64 >= CLASS_COUNT || point_index64 > std::numeric_limits<std::uint32_t>::max()) fail("direct-oracle panel identity outside domain");
        if (n < A || n > B || n % 40 != N0 % 40) fail("direct-oracle n outside fixed cell/modulo-40 domain");
        if (active64 != PAIR_COUNT || expected64 > PAIR_COUNT) fail("direct-oracle pair/T field outside domain");
        const auto class_index = static_cast<std::uint32_t>(class_index64);
        const auto point_index = static_cast<std::uint32_t>(point_index64);
        if (!identities.insert({class_index, point_index}).second || !integers.insert(n).second) fail("duplicate direct-oracle panel point");
        points.push_back({class_index, point_index, n, PAIR_COUNT, static_cast<std::uint32_t>(expected64)});
    }
    if (!stream.eof() || points.empty()) fail("direct-oracle panel read failure/empty panel");
    return points;
}

std::uint64_t floor_sqrt(std::uint64_t value) {
    std::uint64_t low = 0;
    std::uint64_t high = UINT64_C(1) << 32;
    while (low + 1 < high) {
        const std::uint64_t middle = low + (high - low) / 2;
        if (static_cast<__uint128_t>(middle) * middle <= value) low = middle;
        else high = middle;
    }
    return low;
}

std::optional<std::pair<std::uint64_t, std::uint64_t>> canonical_two_squares(std::uint64_t remainder) {
    if (remainder == 0) return std::make_pair(UINT64_C(0), UINT64_C(0));
    std::uint64_t a = 0;
    std::uint64_t b = floor_sqrt(remainder);
    while (a <= b) {
        const __uint128_t sum = static_cast<__uint128_t>(a) * a + static_cast<__uint128_t>(b) * b;
        if (sum == remainder) return std::make_pair(a, b);
        if (sum > remainder) --b;
        else ++a;
    }
    return std::nullopt;
}

std::vector<std::pair<std::uint32_t, std::uint64_t>> powers(std::uint64_t base, std::uint64_t n) {
    std::vector<std::pair<std::uint32_t, std::uint64_t>> result;
    std::uint32_t exponent = 0;
    std::uint64_t value = 1;
    while (value <= n) {
        result.push_back({exponent, value});
        if (value > n / base) break;
        value *= base;
        ++exponent;
    }
    return result;
}

std::vector<SourcePair> active_sources(std::uint64_t n) {
    std::vector<SourcePair> result;
    for (const auto& [c, p3] : powers(3, n)) {
        for (const auto& [d, p5] : powers(5, n)) {
            if (p3 <= n - p5) result.push_back({c, d, p3 + p5});
        }
    }
    if (result.size() != PAIR_COUNT) fail("direct-oracle active-pair count is not 407");
    std::size_t duplicate = 0;
    for (const auto& pair : result) if (pair.shift == 28) ++duplicate;
    if (duplicate != 2) fail("direct-oracle duplicate shift 28 invariant failed");
    return result;
}

OutputPoint evaluate(const InputPoint& input) {
    const auto sources = active_sources(input.n);
    std::vector<Winner> winners;
    for (const auto& source : sources) {
        const std::uint64_t remainder = input.n - source.shift;
        const auto witness = canonical_two_squares(remainder);
        if (witness.has_value()) winners.push_back({source, remainder, witness->first, witness->second});
    }
    if (winners.size() != input.expected_t) fail("direct-oracle T differs from declared backend T at n=" + std::to_string(input.n));
    return {input, std::move(winners)};
}

void write_json(const std::string& path, const std::vector<OutputPoint>& points) {
    std::ofstream output(path, std::ios::trunc);
    if (!output) fail("cannot open direct-oracle output: " + path);
    output << "{\n  \"schema\": \"a303656-p4-census-direct-oracle-raw-v1\",\n"
           << "  \"implementation_id\": \"" << IMPLEMENTATION_ID << "\",\n"
           << "  \"method\": \"factorization-free exact monotone boundary enumeration; canonical least-a witness\",\n"
           << "  \"points\": [\n";
    for (std::size_t i = 0; i < points.size(); ++i) {
        const auto& point = points[i];
        output << "    {\"class_index\":" << point.input.class_index
               << ",\"point_index\":" << point.input.point_index
               << ",\"n\":" << point.input.n
               << ",\"active_pair_count\":" << point.input.active_pairs
               << ",\"T\":" << point.winners.size() << ",\"winners\":[";
        for (std::size_t j = 0; j < point.winners.size(); ++j) {
            const auto& winner = point.winners[j];
            if (j) output << ',';
            output << "{\"c\":" << winner.source.c << ",\"d\":" << winner.source.d
                   << ",\"shift\":" << winner.source.shift << ",\"remainder\":" << winner.remainder
                   << ",\"a\":" << winner.a << ",\"b\":" << winner.b << '}';
        }
        output << "]}" << (i + 1 == points.size() ? "\n" : ",\n");
    }
    output << "  ]\n}\n";
    if (!output) fail("I/O failure writing direct-oracle output");
}

void self_test() {
    const std::vector<std::tuple<std::uint64_t, bool, std::uint64_t, std::uint64_t>> cases = {
        {0, true, 0, 0}, {1, true, 0, 1}, {2, true, 1, 1}, {3, false, 0, 0},
        {4, true, 0, 2}, {5, true, 1, 2}, {7, false, 0, 0}, {8, true, 2, 2},
        {25, true, 0, 5}, {50, true, 1, 7}, {65, true, 1, 8}, {67, false, 0, 0},
    };
    for (const auto& [remainder, represented, a, b] : cases) {
        const auto actual = canonical_two_squares(remainder);
        if (actual.has_value() != represented) fail("self-test representability mismatch");
        if (actual.has_value() && *actual != std::make_pair(a, b)) fail("self-test canonical witness mismatch");
    }
    if (active_sources(A).size() != PAIR_COUNT || active_sources(B).size() != PAIR_COUNT) fail("self-test activation cell mismatch");
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
            std::cout << "DIRECT_ORACLE_SELF_TEST_PASS\n";
            return 0;
        }
        const Options options = parse_options(argc, argv);
        self_test();
        const auto inputs = read_points(options.input);
        std::vector<std::optional<OutputPoint>> slots(inputs.size());
        std::atomic<std::size_t> next{0};
        std::atomic<bool> failed{false};
        std::string error;
        std::vector<std::thread> workers;
        const std::size_t worker_count = std::min<std::size_t>(options.jobs, inputs.size());
        for (std::size_t worker = 0; worker < worker_count; ++worker) {
            workers.emplace_back([&]() {
                while (!failed.load()) {
                    const std::size_t index = next.fetch_add(1);
                    if (index >= inputs.size()) return;
                    try {
                        slots[index] = evaluate(inputs[index]);
                    } catch (const std::exception& exc) {
                        failed.store(true);
                        // Only the first stored message is diagnostically relevant.
                        static std::mutex mutex;
                        std::lock_guard<std::mutex> guard(mutex);
                        if (error.empty()) error = exc.what();
                        return;
                    }
                }
            });
        }
        for (auto& worker : workers) worker.join();
        if (failed.load()) fail(error.empty() ? "direct-oracle worker failure" : error);
        std::vector<OutputPoint> outputs;
        outputs.reserve(slots.size());
        for (auto& slot : slots) {
            if (!slot.has_value()) fail("direct-oracle scheduling omitted a point");
            outputs.push_back(std::move(*slot));
        }
        write_json(options.output, outputs);
        std::cout << "DIRECT_ORACLE_PASS points=" << outputs.size() << " jobs=" << worker_count << '\n';
        return 0;
    } catch (const std::exception& exc) {
        std::cerr << IMPLEMENTATION_ID << ": ERROR: " << exc.what() << '\n';
        return 2;
    }
}
