"""Exact final-domain obstruction to a common R1154/R1795 Drinfeld center.

The categorical induction theorem and the completeness of the earlier
R1154 center sieves are inputs, not claims proved by this arithmetic replay.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'evidence/rank8_next_20261021/r1154'))
import low_action_bounds as l

ZERO, ONE = (F(0), F(0)), (F(1), F(0))


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    return x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def scale(n, x):
    return n * x[0], n * x[1]


def total(xs):
    value = ZERO
    for x in xs:
        value = add(value, x)
    return value


def decode(coefficients, generator):
    result = ZERO
    for coefficient in coefficients:
        result = add(mul(result, generator), (F(str(coefficient)), F(0)))
    return result


def encode(x):
    return [str(c) for c in x]


def character(tensor, values):
    need(values[0] == ONE, 'unital character')
    for i in range(8):
        for j in range(8):
            need(mul(values[i], values[j]) == total(
                scale(tensor[i][j][k], values[k]) for k in range(8)),
                'character multiplication identity')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    census_path = ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    character_path = ROOT / ('evidence/rank8_frontier_20261021/global_induction/'
                            'complete_results/R8_3_1795_atomic_real_sts_h4.json')
    galois_path = ROOT / 'evidence/rank8_postpublication_20261021/r1154_galois_review/review.json'
    gate_path = ROOT / 'evidence/rank8_frontier_20261021/central_integrality/general_galois_pu_gate.json'
    census = {r['id']: r for r in json.loads(census_path.read_text())}
    hashes = {'R8_3_1154': 'c399505be76a64c8aba65feaf2cd55125dc7132f5894b74e58b64473d1387e25',
              'R8_3_1795': 'feddd2934d44be4872c82ed6c5650bf9d8aac2bc87b72778d88b375726f4cd1f'}
    for ring, expected in hashes.items():
        row = census[ring]
        digest = hashlib.sha256(json.dumps(row['tensor'], separators=(',', ':')).encode()).hexdigest()
        need(digest == expected == row['tensor_sha256'], ring + ' canonical tensor binding')

    # Recheck all eight scalar characters directly against the R1795 tensor.
    tensor = census['R8_3_1795']['tensor']
    need(all(tensor[i][j] == tensor[j][i] for i in range(8) for j in range(8)), 'commutative R1795')
    dual = [next(j for j in range(8) if tensor[i][j][0]) for i in range(8)]
    saved = json.loads(character_path.read_text())
    need(saved['tensor_sha256'] == hashes['R8_3_1795'], 'character table tensor binding')
    table = saved['metadata']['character_table']
    generator = (F(818), F(378))
    need(decode(table['field_polynomial'], generator) == ZERO, 'character field polynomial')
    rows = [tuple(decode(value, generator) for value in row) for row in table['characters']]
    need(len(rows) == len(set(rows)) == 8, 'all eight distinct scalar characters')
    codegrees = []
    for row, saved_degree in zip(rows, table['codegrees']):
        character(tensor, row)
        degree = total(mul(row[i], row[dual[i]]) for i in range(8))
        need(degree == decode(saved_degree, generator), 'formal codegree replay')
        codegrees.append(degree)
    fp = tuple((F(a), F(b)) for a, b in
               [(1, 0), (1, 0), (6, 3), (7, 3), (7, 3), (7, 3), (7, 3), (6, 3)])
    character(tensor, fp)
    need(all(a > 0 and b >= 0 for a, b in fp), 'positive FP character')
    D = total(mul(x, x) for x in fp)
    need(D == (540, 240), 'common Frobenius-Perron dimension')
    degree10 = [i for i, degree in enumerate(codegrees) if degree == (10, 0)]
    need(len(degree10) == 4, 'four distinct degree-ten characters')
    required = scale(F(1, 10), D)

    # Convert the R1154 center domain from u=842+369 sqrt(5), and verify
    # its only possible center dimension D/10 is high-column 2.
    need(l.r['tensor_sha256'] == hashes['R8_3_1154'], 'R1154 domain tensor binding')
    gen1154 = (F(842), F(369))
    need(decode(l.K.mod.to_list(), gen1154) == ZERO, 'R1154 dimension-field polynomial')
    need(decode(l.c.ec(l.a['D']), gen1154) == D, 'equal source FP dimensions')
    dimensions = [decode(l.c.ec(d), gen1154) for d in l.dims]
    possible_types = [i for i, d in enumerate(dimensions) if d == required]
    need(possible_types == [7], 'unique D/10 dimension type, global 7 = high 2')
    galois = json.loads(galois_path.read_text())
    need(galois['tensor_sha256'] == hashes['R8_3_1154'], 'latest review tensor binding')
    surviving = [r for r in galois['results'] if r['witness'] is not None]
    indices = sorted({r['index'] for r in surviving})
    need(indices == [6971, 8766, 8772] and len(surviving) == 25, 'current exhaustive accepted center domain')
    patterns = []
    for index in indices:
        high = l.domain['completions'][index]
        counts = [1] * 5 + high
        multiplicity = sum(counts[i] for i in possible_types)
        need(multiplicity == 0, 'D/10 absent from every possible R1154 center')
        patterns.append({'index': index, 'rank': sum(counts), 'high_type_2_multiplicity': high[2],
                         'dimension_D_over_10_multiplicity': multiplicity})
    gate = next(r for r in json.loads(gate_path.read_text()) if r['id'] == 'R8_3_1154')
    need(gate['tensor_sha256'] == hashes['R8_3_1154'] and
         gate['scope'] == 'general_complex_fusion_category' and
         gate['outcome'] == 'Galois_pseudo_unitary_reduction', 'existing general Galois reduction binding')
    sources = [census_path, character_path, galois_path, gate_path, l.domainpath,
               ROOT / 'evidence/rank8_next_20261021/r1154/low_action_bounds.py']
    result = {
        'schema': 'r1154-r1795-common-center-obstruction/v1', 'status': 'PASS',
        'conclusion': 'No categorifications of R8_3_1154 and R8_3_1795 can be categorically Morita equivalent.',
        'scope': 'General complex categorifications, using the existing R1154 Galois-pseudo-unitary reduction and Morita invariance of global and FP dimensions. Neither ring is excluded individually.',
        'tensor_sha256': hashes, 'quadratic_encoding': 'a+b*sqrt(5)',
        'common_FP_dimension': encode(D), 'required_center_dimension': encode(required),
        'R1795_formal_codegrees': [encode(d) for d in codegrees],
        'R1795_degree_10_character_indices': degree10,
        'R1795_required_number_of_distinct_center_simples': 4,
        'R1154_all_dimension_types_matching_D_over_10': possible_types,
        'R1154_surviving_patterns': patterns,
        'source_sha256': {p.relative_to(ROOT).as_posix(): sha(p) for p in sources},
        'verifier_sha256': sha(Path(__file__))}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
