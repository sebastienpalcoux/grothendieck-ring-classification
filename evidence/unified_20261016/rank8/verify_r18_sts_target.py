#!/usr/bin/env python3
"""Independent exact source-character audit of the R18 relative STS target.

No numerical field calculations or external packages are used.  The full
categorical identity is proved in R18_STS_INDEPENDENT_AUDIT.md.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path

EXPECTED_SHA = "cdd3aa4477861e8521c75ac63cb0f9e4e5d0a021073d1619aae358a0850704f2"
ZERO = (0, 0, 0, 0)
ONE = (1, 0, 0, 0)

def require(test, message):
    if not test:
        raise RuntimeError(message)

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def scale(n, a):
    return tuple(n * x for x in a)

def mul(a, b):
    out = [0] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            n = i + j
            out[n % 4] += x * y * (-1 if n >= 4 else 1)
    return tuple(out)

def power(n):
    n %= 8
    out = [0] * 4
    out[n % 4] = -1 if n >= 4 else 1
    return tuple(out)

def conjugate(a):
    return tuple(sum(a[j] * power(-j)[i] for j in range(4)) for i in range(4))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path)
    args = parser.parse_args()
    repo = args.repo
    if repo is None:
        for parent in Path(__file__).resolve().parents:
            for candidate in (parent, parent / 'repo'):
                if (candidate / 'supplements/rank8/data/rank8_tables.txt.gz').is_file():
                    repo = candidate
                    break
            if repo is not None:
                break
    require(repo is not None, 'repository source must be available; use --repo')
    source = repo / "supplements/rank8/data/rank8_tables.txt.gz"
    flatten = lambda t: tuple(x for row in t for product in row for x in product)
    with gzip.open(source, "rt") as handle:
        tensors = [json.loads(line.replace("{", "[").replace("}", "]")) for line in handle]
    N = sorted((t for t in tensors if max(flatten(t)) == 1), key=flatten)[17]
    digest = hashlib.sha256(json.dumps(N, separators=(",", ":")).encode()).hexdigest()
    require(digest == EXPECTED_SHA, "immutable R8_1_18 source digest")
    model = [0, 1, 7, 2, 3, 6, 5, 4]
    chars = []
    for k in [1, 2, 3]:
        for sign in [1, -1]:
            row = [None] * 8
            for j in range(4):
                row[model[j]] = power(2 * k * j)
                row[model[j + 4]] = scale(sign, power(k + 2 * k * j))
            chars.append(row)
    require(len({tuple(row) for row in chars}) == 6, "six distinct non-FP characters")
    for row in chars:
        for i, j in itertools.product(range(8), repeat=2):
            value = ZERO
            for k in range(8):
                value = add(value, scale(N[i][j][k], row[k]))
            require(value == mul(row[i], row[j]), "source character multiplication")
        f = ZERO
        for value in row:
            f = add(f, mul(value, conjugate(value)))
        require(f == (8, 0, 0, 0), "formal codegree eight")
    # Normalized Q(zeta_8)/Q trace is the coefficient of 1.
    averaged = [[(v[0], 0) for v in row] for row in chars]
    averaged = [[(1, 0) if i in [0, 1, 2, 7] else (0, 1) for i in range(8)],
                [(1, 0) if i in [0, 1, 2, 7] else (4, -1) for i in range(8)]] + averaged
    profiles = [p for p in itertools.product(range(3), repeat=4) if sum(p) == 2]
    values = [[sum_vectors(scale(n, row[model[4+j]]) for j, n in enumerate(p))
               for p in profiles] for row in chars]
    dual = [5, 4, 3, 2, 1, 0]
    dualprofile = lambda p: tuple(p[(-1-j) % 4] for j in range(4))
    solutions = []
    def search(chosen, sums):
        i = len(chosen)
        if i == 6:
            if sums == [3] * 4:
                solutions.append(chosen[:])
            return
        for index, p in enumerate(profiles):
            if any(sums[j] + p[j] > 3 for j in range(4)):
                continue
            if any(values[j][index] != values[i][chosen[j]] for j in range(i)):
                continue
            if any(i == dual[j] and p != dualprofile(profiles[chosen[j]]) for j in range(i)):
                continue
            search(chosen + [index], [sums[j] + p[j] for j in range(4)])
    search([], [0] * 4)
    require(len(solutions) == 8, "eight complete reciprocity/duality assignments")
    targets = []
    for solution in solutions:
        low = [[1] + [0] * 7, [1, 0, 0, 1, 1, 1, 1, 0]]
        for index in solution:
            row = [1] + [0] * 7
            for j, n in enumerate(profiles[index]):
                row[model[4+j]] = n
            low.append(row)
        target = [[tuple(sum(low[a][i] * averaged[a][j][h] for a in range(8))
                         for h in range(2)) for j in range(8)] for i in range(8)]
        for i, j in itertools.product(range(1, 8), repeat=2):
            expected = (4, -1) if i in [3, 4, 5, 6] and j in [3, 4, 5, 6] else (0, 0)
            require(target[i][j] == expected, "full relative STS source target")
        targets.append(target)
    print(json.dumps({"status": "PASS", "criterion": "independent_relative_STS_target",
                      "case": "R8_1_18", "source_sha256": digest,
                      "source_character_product_checks": 384,
                      "formal_codegrees": [8] * 6, "low_assignments": 8,
                      "target": "4-d on nonpointed block; zero on other nonunit pairs",
                      "nonunit_target_entry_checks": 392}, indent=2))

def sum_vectors(values):
    result = ZERO
    for value in values:
        result = add(result, value)
    return result

if __name__ == "__main__":
    main()
