"""Exact arithmetic certificate for a rank-six premodular literature bound.

The finite catalogue is Dong--Schopieray, arXiv:2407.15955v1,
Section 5.3, Figures 13--15, 17, 19. It classifies premodular fusion
rules; a bare fusion category is outside this criterion's scope.
No associator, census, or floating-point computation occurs here.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from rings import Characters, fingerprint
from exact import pc, ec


def premodular_obstruction(N):
    """Apply a general necessary criterion; no identifier selects its outcome."""
    if len(N) != 6:
        raise ValueError('the cited catalogue bound has rank-six scope')
    if any(N[i][j] != N[j][i] for i in range(6) for j in range(6)):
        return {'premodular_categorification': 'excluded', 'reason': 'noncommutative_based_ring'}
    arithmetic = Characters(N)
    f, K, dimensions, D, pD, embedding = arithmetic.fp()
    comparison = embedding.sign(D - K(168))
    return {
        'tensor_sha256': fingerprint(N),
        'generator': arithmetic.k,
        'generator_minimal_polynomial': pc(f),
        'positive_embedding_interval': [str(embedding.lo), str(embedding.hi)],
        'dimension_vector_in_generator_field': [ec(x) for x in dimensions],
        'global_FP_dimension_in_generator_field': ec(D),
        'global_FP_dimension_minimal_polynomial': pc(pD),
        'sign_global_FP_dimension_minus_168': comparison,
        'premodular_categorification': 'excluded' if comparison > 0 else 'not_excluded_by_this_bound',
        'reason': 'rank_six_premodular_FP_dimension_bound',
    }


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def scale(n, a):
    return (n * a[0], n * a[1])


def mul(a, b):
    """Arithmetic in Z[sqrt(17)]."""
    return (a[0] * b[0] + 17 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def main():
    # Every catalogue row belongs to one family below. Bounds follow from
    # sin(pi/l) >= 2/l, |sin(k*pi/l)| <= 1, sqrt(5)<3, sqrt(21)<5,
    # and |cos(theta)| <= 1. Equalities at boundary do not affect <=168.
    # The Fib x A1(7)_ad row is bounded from its listed simple FP dimensions,
    # avoiding the inconsistent displayed global-dimension formula in Fig.19.
    bounds = [
        ('integral groups and their listed braided variants', Q(168)),
        ('pointed rank three times Fibonacci', Q(3 * 4)),
        ('Rep(S3) times Fibonacci', Q(6 * 4)),
        ('Ising times rank-two pointed category', Q(8)),
        ('Ising times Fibonacci', Q(4 * 4)),
        ('rank-two pointed times A1(7)_ad', 2 * (1 + 2 * Q(7, 2) ** 2)),
        ('Fibonacci times A1(7)_ad', 4 * (1 + 2 * Q(7, 2) ** 2)),
        ('G2(21)', Q(1 + 3 * 4 ** 2 + 5 ** 2 + 6 ** 2)),
        ('dimension-twenty metaplectic category', Q(20)),
        ('A1(13)_ad', Q(13, 4) * Q(13, 2) ** 2),
        ('B2(9)_ad', Q(9 * 3 ** 2)),
        ('A1(12)_ad', 3 * Q(12, 2) ** 2),
    ]
    if max(bound for _, bound in bounds) != 168:
        raise ValueError('catalogue bound changed')
    rows = json.loads((ROOT / 'data/unresolved_tensors.json').read_text())
    R = min(rows, key=lambda row: (row['m'], row['index']))
    N = R['N']
    census = {row['id']: row for row in json.loads((ROOT / 'data/census.json').read_text())}
    decisions = json.loads((ROOT / 'data/decisions.json').read_text())
    targets = [row for row in decisions if row['status'] != 'excluded']
    scoped_results = [dict(id=row['id'], general_status=row['status'],
                          **premodular_obstruction(census[row['id']]['N'])) for row in targets]
    frontier_result = premodular_obstruction(N)
    d = [(1, 0), (1, 0), (4, 1), (4, 1), (3, 1), (5, 1)]
    for i in range(6):
        for j in range(6):
            rhs = (0, 0)
            for k in range(6):
                rhs = add(rhs, scale(N[i][j][k], d[k]))
            if mul(d[i], d[j]) != rhs:
                raise ValueError('the proposed positive dimension vector does not fit the frontier tensor')
    global_dimension = (0, 0)
    for x in d:
        global_dimension = add(global_dimension, mul(x, x))
    if global_dimension != (136, 32):
        raise ValueError('unexpected global dimension')
    # All d_i are positive. Perron--Frobenius uniqueness therefore identifies
    # this character as FPdim; sqrt(17)>1 proves its total is strictly >168.
    if not (17 > 1 and global_dimension[0] + global_dimension[1] >= 168):
        raise ValueError('the exact strict comparison failed')
    out = {
        'source': 'Dong--Schopieray, Near-integral fusion, arXiv:2407.15955v1',
        'source_url': 'https://arxiv.org/html/2407.15955v1#S5.SS3',
        'locations': 'Section 5.3, Figures 13--15, 17, 19',
        'premodular_rank6_global_FP_dimension_upper_bound': 168,
        'rational_family_upper_bounds': [{'family': name, 'upper_bound': str(value)} for name, value in bounds],
        'frontier_id': R['id'],
        'dimension_vector_in_Z_sqrt17': d,
        'dimension_character_equations_checked': 36,
        'global_dimension_in_Z_sqrt17': global_dimension,
        'automatic_frontier_result': frontier_result,
        'nonexcluded_ledger_tensors_checked': len(scoped_results),
        'scoped_results': scoped_results,
        'premodular_categorification': 'excluded',
        'general_categorification': 'unresolved',
        'scope': 'Braided spherical fusion categories only; no arbitrary fusion-category exclusion follows.',
    }
    (HERE / 'premodular_bound.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'scoped_results'}, indent=2))


if __name__ == '__main__':
    main()
