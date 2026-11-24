"""Integer replay of a single W0/W1 direction and a genuine bridge at r=4."""
import json
import sys
from collections import Counter, defaultdict
from math import isqrt, prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))
from ajt5_integer_certificates import MAX_BYTES, parse, verify
from verify_ajt5_palette import catalogue, check_tree, pair, require, restrict


def window():
    rows = {}
    for d in range(8):
        if d not in (0, 6):
            for c in range(10 + 2 * (d == 7)):
                rows["parent", d, c] = 5 * (5**d + 3**c)
    for e in sorted({d + offset for d in (0, 6) for offset in (0, 1)}):
        for c in range(11):
            rows["child", e, c] = 5**e + 3**c - 4
    require(len(rows) == 106 and len(set(rows.values())) == 105, "W0 labels or roots")
    return rows


def valuation(value, prime):
    require(value > 0, "odd valuation requires positive residual")
    h = 0
    while value % prime == 0:
        value //= prime
        h += 1
    return h


def check_exclusion(roots):
    groups = catalogue(roots)
    stats = Counter()
    with (HERE / "low_w1.jsonl").open("rb") as f:
        for expected in [None, *range(27)]:
            tag, tree = pair(parse(f.readline(MAX_BYTES + 1)))
            require(tag is None if expected is None else type(tag) is int and tag == expected,
                    "misplaced prefix")
            # The only roots certainly safe from 3 are units and v3 exactly two.
            live = roots if tag is None else {k for k in roots if (tag - k) % 27 in (9, 18)
                                               or (tag - k) % 3 != 0}
            check_tree(tree, live, restrict(groups, live), 15 if tag is None else 14, stats)
        require(not f.read(1), "trailing proof data")
    return stats


def cover_rows(m, palette, rows):
    require(len(set(palette)) == len(palette) and
            all(p > 0 and p % 4 == 3 and all(p % t for t in range(2, isqrt(p) + 1))
                for p in palette), "invalid palette")
    by_column = defaultdict(list)
    powers = {}
    for (side, d, c), k in rows.items():
        for p in palette:
            h = valuation(5*m - k, p)
            if h % 2:
                powers[p] = max(powers.get(p, 0), h + 1)
                by_column[side, d].append({"c": c, "u": p**h})
                break
        else:
            raise ValueError(f"uncovered {side} d={d} c={c}")
    records = [{"side": side, "d": d, "units": units} for (side, d), units in by_column.items()]
    return records, powers


def survivors(x, palette, last_d, last_c):
    return [d for d in range(last_d + 1) if any(
        all(valuation(x - 5**d - 3**c, p) % 2 == 0 for p in palette)
        for c in range(last_c + 1))]


def main():
    data = parse((HERE / "low_control.json").read_bytes())
    m, palette = data["m"], data["palette"]
    require(m.bit_length() == 249 and len(palette) == 15, "W0 control scope")
    rows = window()
    negative, powers = cover_rows(m, palette, rows)
    require(set(powers) == set(palette), "unused W0 prime")
    masks = [survivors(m, palette, 7, 9), survivors(5*m+4, palette, 8, 10),
             survivors(m, palette, 7, 12)]
    require(masks == [[0, 6], [2, 3, 4, 8], [0, 2, 6]], "prefix screen sets")
    require(valuation(m-2, 3) % 2 == 1, "earlier parent c=0")
    positive = [{"side": side, "d": 0, "c": c, "a": data[side][0], "b": data[side][1]}
                for side, c in (("parent", 1), ("child", 11))]
    record = dict(kind="NO_BRIDGE", m=m, r=4, positive=positive, negative=negative)
    require(verify(record) == {"status": "REFUTED", "bridge": [0, 0]}, "actual bridge")
    require(verify(dict(record, positive=positive[:1])) ==
            {"status": "PARTIAL", "uncovered_edge": [0, 0]}, "truncated evidence")

    tail = 5**0 + 3**11 - 4
    require(tail == 177144 and tail not in rows.values(), "strict W1 extension")
    rows["child", 0, 11] = tail
    roots = set(rows.values())
    require(max(roots) < 5*255273, "inactive window row")
    stats = check_exclusion(roots)

    # Preserve each odd prime valuation used at W0 and add a fresh prime at W1.
    step = prod(p**h for p, h in powers.items())
    p = 47
    require(p not in palette, "tail prime already used")
    shift = ((tail + p - 5*m) * pow(5*step, -1, p*p)) % (p*p)
    other = m + step * shift
    _, extended_powers = cover_rows(other, palette + [p], rows)
    require(len(extended_powers) == 16, "W1 support")
    print(json.dumps(dict(parent_C9=masks[0], child_C10=masks[1], parent_C12=masks[2],
                          W0_labels=106, W0_unique_roots=105, W1_unique_roots=len(roots),
                          W0_minimum=15, W1_minimum=16, m_bits=m.bit_length(),
                          W1_cover_m=other, actual_bridge=[0, 0], first_c=[1, 11], **stats),
                     sort_keys=True))


if __name__ == "__main__":
    main()
