#pragma once

#include <algorithm>
#include <charconv>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <stdexcept>
#include <string>
#include <system_error>
#include <vector>

namespace a303656_tn {

struct Config {
    uint64_t low = 0;
    uint64_t high = 0;
    std::string interval_id;
    std::filesystem::path out_dir;
    bool emit_all_records = false;
};

struct SourcePair {
    uint32_t c;
    uint32_t d;
    uint64_t power3;
    uint64_t power5;
    uint64_t shift;
};

struct Winner {
    SourcePair source;
    uint64_t remainder;
    uint64_t a;
    uint64_t b;
};

inline uint64_t decimal_u64(const std::string& text, const char* label) {
    if (text.empty()) throw std::runtime_error(std::string(label) + " requires a value");
    uint64_t result = 0;
    const auto converted = std::from_chars(text.data(), text.data() + text.size(), result, 10);
    if (converted.ec == std::errc::result_out_of_range) {
        throw std::runtime_error(std::string(label) + " out of uint64 range");
    }
    if (converted.ec != std::errc() || converted.ptr != text.data() + text.size()) {
        throw std::runtime_error(std::string(label) + " must be unsigned decimal");
    }
    return result;
}

inline std::string json_escape(const std::string& text) {
    std::string result;
    for (const unsigned char ch : text) {
        switch (ch) {
            case '\\': result += "\\\\"; break;
            case '"': result += "\\\""; break;
            case '\n': result += "\\n"; break;
            case '\r': result += "\\r"; break;
            case '\t': result += "\\t"; break;
            default:
                if (ch < 0x20) throw std::runtime_error("control character in JSON string");
                result += static_cast<char>(ch);
        }
    }
    return result;
}

inline Config parse_config(int argc, char** argv) {
    Config config;
    for (int i = 1; i < argc; ++i) {
        const std::string argument = argv[i];
        auto value = [&](const char* option) -> std::string {
            if (i + 1 >= argc) throw std::runtime_error(std::string("missing value for ") + option);
            return argv[++i];
        };
        if (argument == "--low") config.low = decimal_u64(value("--low"), "--low");
        else if (argument == "--high") config.high = decimal_u64(value("--high"), "--high");
        else if (argument == "--interval-id") config.interval_id = value("--interval-id");
        else if (argument == "--out-dir") config.out_dir = value("--out-dir");
        else if (argument == "--emit-all-records") config.emit_all_records = true;
        else throw std::runtime_error("unknown argument: " + argument);
    }
    if (config.low <= 1 || config.high <= config.low || config.interval_id.empty() || config.out_dir.empty()) {
        throw std::runtime_error(
            "required: --low L --high U --interval-id ID --out-dir DIR [--emit-all-records]"
        );
    }
    const uint64_t width = config.high - config.low;
    if (width > 200000) throw std::runtime_error("bounded pilot width exceeds 200000");
    if (!std::filesystem::is_directory(config.out_dir)) {
        throw std::runtime_error("output directory must already exist");
    }
    return config;
}

inline uint64_t checked_lhs(const Winner& winner) {
    const __uint128_t value = static_cast<__uint128_t>(winner.a) * winner.a
                            + static_cast<__uint128_t>(winner.b) * winner.b
                            + winner.source.power3 + winner.source.power5;
    if (value > UINT64_MAX) throw std::runtime_error("witness equation overflow");
    return static_cast<uint64_t>(value);
}

template <typename WinnerFinder>
void write_outputs(
    const Config& config,
    const std::string& implementation_id,
    const std::string& algorithm,
    const std::vector<SourcePair>& sources,
    const std::vector<uint32_t>& counts,
    const std::vector<uint32_t>& active_counts,
    WinnerFinder find_winners
) {
    const uint64_t width64 = config.high - config.low;
    if (width64 > std::numeric_limits<size_t>::max()) throw std::runtime_error("width exceeds size_t");
    const size_t width = static_cast<size_t>(width64);
    if (counts.size() != width || active_counts.size() != width) {
        throw std::runtime_error("count vector width mismatch");
    }

    uint32_t minimum = std::numeric_limits<uint32_t>::max();
    std::map<uint32_t, uint64_t> histogram;
    uint32_t active_minimum = std::numeric_limits<uint32_t>::max();
    uint32_t active_maximum = 0;
    for (size_t index = 0; index < width; ++index) {
        minimum = std::min(minimum, counts[index]);
        ++histogram[counts[index]];
        active_minimum = std::min(active_minimum, active_counts[index]);
        active_maximum = std::max(active_maximum, active_counts[index]);
        if (counts[index] > active_counts[index]) throw std::runtime_error("T exceeds active pair count");
    }

    uint64_t argmin_count = 0;
    uint64_t first_argmin = 0;
    uint64_t last_argmin = 0;
    for (size_t index = 0; index < width; ++index) {
        if (counts[index] == minimum) {
            const uint64_t n = config.low + index;
            if (argmin_count == 0) first_argmin = n;
            last_argmin = n;
            ++argmin_count;
        }
    }

    const auto counts_path = config.out_dir / "counts.csv";
    std::ofstream counts_file(counts_path);
    if (!counts_file) throw std::runtime_error("cannot create counts.csv");
    counts_file << "n,T\n";
    for (size_t index = 0; index < width; ++index) {
        counts_file << config.low + index << ',' << counts[index] << '\n';
    }
    counts_file.close();
    if (!counts_file) throw std::runtime_error("failed writing counts.csv");

    const auto low_path = config.out_dir / "low_t.jsonl";
    std::ofstream low_file(low_path);
    if (!low_file) throw std::runtime_error("cannot create low_t.jsonl");
    uint64_t low_record_count = 0;
    for (size_t index = 0; index < width; ++index) {
        const uint32_t count = counts[index];
        if (!config.emit_all_records && count > 3 && count != minimum) continue;
        const uint64_t n = config.low + index;
        const std::vector<Winner> winners = find_winners(n);
        if (winners.size() != count) throw std::runtime_error("winner list length differs from exact T");
        low_file << "{\"schema\":\"a303656-tn-low-record-v1\""
                 << ",\"interval_id\":\"" << json_escape(config.interval_id) << "\""
                 << ",\"implementation_id\":\"" << implementation_id << "\""
                 << ",\"n\":\"" << n << "\",\"T\":" << count
                 << ",\"active_exponent_pair_count\":" << active_counts[index]
                 << ",\"classification\":\""
                 << (count == 0 ? "UNVERIFIED CANDIDATE" : "EXACT BOUNDED T(n) OBSERVATION")
                 << "\",\"winning_exponent_pairs\":[";
        for (size_t winner_index = 0; winner_index < winners.size(); ++winner_index) {
            if (winner_index) low_file << ',';
            const Winner& winner = winners[winner_index];
            if (winner.a > winner.b) throw std::runtime_error("noncanonical witness ordering");
            if (checked_lhs(winner) != n) throw std::runtime_error("invalid witness equation");
            const uint64_t a_squared = winner.a * winner.a;
            const uint64_t b_squared = winner.b * winner.b;
            low_file << "{\"c\":" << winner.source.c << ",\"d\":" << winner.source.d
                     << ",\"shift\":\"" << winner.source.shift
                     << "\",\"remainder\":\"" << winner.remainder
                     << "\",\"a\":\"" << winner.a << "\",\"b\":\"" << winner.b
                     << "\",\"witness_equation\":{\"a_squared\":\"" << a_squared
                     << "\",\"b_squared\":\"" << b_squared
                     << "\",\"three_power\":\"" << winner.source.power3
                     << "\",\"five_power\":\"" << winner.source.power5
                     << "\",\"lhs\":\"" << n << "\",\"verified\":true}}";
        }
        low_file << "]}\n";
        ++low_record_count;
    }
    low_file.close();
    if (!low_file) throw std::runtime_error("failed writing low_t.jsonl");

    std::ofstream metadata(config.out_dir / "metadata.json");
    if (!metadata) throw std::runtime_error("cannot create metadata.json");
    metadata << "{\n"
             << "  \"schema\": \"a303656-tn-pilot-metadata-v1\",\n"
             << "  \"classification\": \"EXACT BOUNDED PILOT OUTPUT; NOT A GLOBAL PROOF\",\n"
             << "  \"implementation_id\": \"" << implementation_id << "\",\n"
             << "  \"algorithm\": \"" << json_escape(algorithm) << "\",\n"
             << "  \"interval\": {\"id\": \"" << json_escape(config.interval_id)
             << "\", \"low\": \"" << config.low << "\", \"high_exclusive\": \""
             << config.high << "\", \"number_of_n\": " << width << "},\n"
             << "  \"T_semantics\": \"counts active source exponent pairs (c,d), not distinct shifts and not (a,b) multiplicity\",\n"
             << "  \"canonical_witness\": \"minimum a, then minimum b, with 0 <= a <= b\",\n"
             << "  \"all_active_pairs_processed\": true,\n"
             << "  \"early_termination\": false,\n"
             << "  \"source_exponent_pair_count_at_upper_minus_one\": " << sources.size() << ",\n"
             << "  \"emit_all_records_fixture_mode\": " << (config.emit_all_records ? "true" : "false") << ",\n"
             << "  \"obstruction_data_status\": \"NOT_COLLECTED_IN_TN_PILOT\"\n"
             << "}\n";

    std::ofstream summary(config.out_dir / "summary.json");
    if (!summary) throw std::runtime_error("cannot create summary.json");
    summary << "{\n"
            << "  \"schema\": \"a303656-tn-pilot-summary-v1\",\n"
            << "  \"implementation_id\": \"" << implementation_id << "\",\n"
            << "  \"interval\": {\"id\": \"" << json_escape(config.interval_id)
            << "\", \"low\": \"" << config.low << "\", \"high_exclusive\": \""
            << config.high << "\", \"number_of_n\": " << width << "},\n"
            << "  \"minimum_T\": " << minimum << ",\n"
            << "  \"argmin_count\": " << argmin_count << ",\n"
            << "  \"first_argmin_n\": \"" << first_argmin << "\",\n"
            << "  \"last_argmin_n\": \"" << last_argmin << "\",\n"
            << "  \"count_T0\": " << histogram[0] << ",\n"
            << "  \"count_T1\": " << histogram[1] << ",\n"
            << "  \"count_T2\": " << histogram[2] << ",\n"
            << "  \"count_T3\": " << histogram[3] << ",\n"
            << "  \"exact_histogram\": {";
    bool first = true;
    for (const auto& [value, frequency] : histogram) {
        if (!first) summary << ',';
        summary << "\"" << value << "\":" << frequency;
        first = false;
    }
    summary << "},\n"
            << "  \"active_pair_range\": {\"minimum\": " << active_minimum
            << ", \"maximum\": " << active_maximum << "},\n"
            << "  \"low_t_record_count\": " << low_record_count << ",\n"
            << "  \"counts_csv_sha256\": \"PENDING_AUTOMATIC_PROVENANCE\",\n"
            << "  \"low_t_jsonl_sha256\": \"PENDING_AUTOMATIC_PROVENANCE\"\n"
            << "}\n";
}

}  // namespace a303656_tn
