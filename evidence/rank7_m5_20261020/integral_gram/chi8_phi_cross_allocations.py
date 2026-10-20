"""Exact finite conductor-five allocations after the surviving chi(-8) packet.

This is a conditional necessary-data enumeration, not a whole-ring exclusion.
The Gram bound is reconstructed from the canonical source tensor, rather
than copied from a discovery output. All positivity checks use Fraction.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PAIRS = [(i, j) for i in range(6) for j in range(i + 1)]


def require(value, message):
    if not value:
        raise ValueError(message)


def psd(vector):
    matrix = [[F(0) for _ in range(6)] for _ in range(6)]
    for value, (i, j) in zip(vector, PAIRS):
        matrix[i][j] = matrix[j][i] = F(value)
    for k in range(6):
        pivot = matrix[k][k]
        if pivot < 0:
            return False
        if pivot == 0:
            if any(matrix[k][j] for j in range(k + 1, 6)):
                return False
            continue
        for i in range(k + 1, 6):
            for j in range(i, 6):
                matrix[i][j] -= matrix[i][k] * matrix[k][j] / pivot
                matrix[j][i] = matrix[i][j]
    return True


def run(case, with_orbit50=False):
    path = HERE.parent / 'criteria' / f'R7_5_5039_c8_case{case}_chi8_0_system.json'
    raw = path.read_bytes()
    system = json.loads(raw)
    census = json.loads((ROOT / 'supplements/rank7/output/m5/census.json').read_text())
    tensor = next(row['tensor'] for row in census if row['id'] == system['id'])
    digest = hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()
    require(digest == system['source_sha256'], 'canonical source hash')
    bound = [sum(tensor[k][i + 1][j] * tensor[k][h + 1][j]
                 for k in range(7) for j in range(7))
             - sum(v[i + 1] * v[h + 1] for v in system['low'])
             for i, h in PAIRS]
    orbit_grams = [[sum(v[i] * v[j] for v, _, _ in orbit) for i, j in PAIRS]
                   for orbit in system['orbits']]
    require(all(g == [sum(row[1][h] for row in orbit) for h in range(21)]
                for g, orbit in zip(orbit_grams, system['orbits'])), 'raw outer products')
    # Conditional active-packet conclusion from the separate integer-lattice
    # proof: every row in dual orbit 24 occurs eight times.
    chi_orbit, chi_count = 24, 8
    chi_weight = sum((v[0] - v[1]) ** 2 for v, _, _ in system['orbits'][chi_orbit])
    require(chi_count * chi_weight == 16, 'complete chi(-8) square budget')
    residual = [b - chi_count * a for b, a in zip(bound, orbit_grams[chi_orbit])]
    if with_orbit50:
        residual = [b - 16 * a for b, a in zip(residual, orbit_grams[50])]
    require(psd(residual) and all(x >= 0 for x in residual), 'conditional residual Gram')
    candidates = []
    for j, label in enumerate(system['phase_labels']):
        oi, unit = label['orbit'], label['multiplicity_unit']
        weight = unit * sum((v[2] - v[3]) ** 2 for v, _, _ in system['orbits'][oi])
        if not weight:
            continue
        gram = [unit * x for x in orbit_grams[oi]]
        remaining = [b - a for b, a in zip(residual, gram)]
        if min(remaining) >= 0 and psd(remaining):
            candidates.append((j, weight, gram))
    pi = {pair: i for i, pair in enumerate(PAIRS)}
    budget = residual[pi[(2, 2)]] + residual[pi[(3, 3)]] - 2 * residual[pi[(3, 2)]]
    require(budget == 8, 'conductor-five square budget')
    statistics = Counter()
    allocations = []

    def recurse(first, left, used, gram):
        if not left:
            statistics['raw_allocations'] += 1
            remaining = [b - a for b, a in zip(residual, gram)]
            if min(remaining) < 0:
                statistics['negative_entry'] += 1
                return
            if not psd(remaining):
                statistics['not_psd'] += 1
                return
            counts = Counter(used)
            allocations.append([[j, n] for j, n in sorted(counts.items())])
            statistics['remaining'] += 1
            return
        for index in range(first, len(candidates)):
            j, weight, contribution = candidates[index]
            if weight <= left:
                recurse(index, left - weight, used + [j],
                        [a + b for a, b in zip(gram, contribution)])

    recurse(0, budget, [], [0] * 21)
    result = {
        'id': system['id'], 'case': case, 'chi8_branch': 0,
        'scope': 'Conditional exhaustive phi-active allocations; no exclusion claim.',
        'system_sha256': hashlib.sha256(raw).hexdigest(), 'source_sha256': digest,
        'conditional_chi8_orbit': chi_orbit, 'conditional_chi8_count': chi_count,
        'phi_budget': budget, 'candidate_columns': [j for j, _, _ in candidates],
        'statistics': dict(statistics), 'allocations': allocations,
    }
    if with_orbit50:
        result['conditional_orbit50_order320_count'] = 16
    suffix = '_orbit50' if with_orbit50 else ''
    target = HERE / f'R7_5_5039_c8_case{case}_chi8_0_phi_cross_allocations{suffix}.json'
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'allocations'}), flush=True)
    return result


if __name__ == '__main__':
    for case in (0, 1):
        run(case, '--orbit50' in sys.argv)
