"""Direct truth-table checks, separate from the guarded-slice implementation.

No contraction, slice-cover, antichain, or residue-trie implementation is
imported here. Common inputs are only finite domains and original event data.
"""
from itertools import product


def direct_masks(dims, shapes):
    points = list(product(*(range(n) for n in dims)))
    result = []
    for shape in shapes:
        positions = []
        if shape is not None:
            for k, point in enumerate(points):
                if all((shape[j] // (2 ** value)) % 2 for j, value in enumerate(point)):
                    positions.append(k)
        result.append(sum(2 ** k for k in positions))
    return result


def direct_minimal_covers(dims, shapes):
    masks = direct_masks(dims, shapes)
    n = 1
    for size in dims:
        n *= size
    target = (1 << n) - 1
    good = []
    for enabled in range(1 << len(shapes)):
        union = 0
        for row, mask in enumerate(masks):
            if enabled & (1 << row):
                union |= mask
        if union == target:
            good.append(enabled)
    minimal = [s for s in good if not any(t != s and t & s == t for t in good)]
    return frozenset(frozenset(i for i in range(len(shapes)) if s >> i & 1) for s in minimal)


def initial_rank_saturations(dims, shapes):
    """Rank-specific original rows only; lower-row coverage is NOT inserted."""
    result = {}
    fulls = [(1 << n) - 1 for n in dims]
    for k in range(len(dims)):
        top = []
        for shape in shapes:
            if shape is not None and shape[k] != fulls[k] and all(shape[j] == fulls[j] for j in range(k + 1, len(dims))):
                top.append(shape)
        lower_points = list(product(*(range(n) for n in dims[:k])))
        saturated = []
        for y in lower_points:
            if all(any(all(s[j] >> y[j] & 1 for j in range(k)) and s[k] >> z & 1
                       for s in top) for z in range(dims[k])):
                saturated.append(y)
        result[k] = saturated
    return result


def direct_csp(state_masks, domain_size):
    target = (1 << domain_size) - 1
    anchor_counts = [0, 0]
    solutions = []
    for choices in product(*(range(len(s)) for s in state_masks)):
        unions = [0, 0]
        for row, state in enumerate(choices):
            pair = state_masks[row][state]
            for c in (0, 1):
                unions[c] |= pair[c]
        for c in (0, 1):
            anchor_counts[c] += unions[c] == target
        if unions[0] == unions[1] == target:
            solutions.append(choices)
    return {'anchor_counts': anchor_counts, 'solutions': solutions}
