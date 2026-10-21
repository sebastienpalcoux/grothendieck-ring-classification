"""Complete sphericalization gates for the noncommutative rings 721 and 1154.

Conclusion: every categorification is spherical and has a pseudo-unitary
Galois conjugate. This is a scope reduction, not a categorification or an
exclusion, and it does not assert unitarity.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / 'rank8_m3_20261021'
sys.path.insert(0, str(OLD / 'noncommutative'))
import scalar_sieve as scalar


def need(ok, message):
    if not ok:
        raise ValueError(message)


def compute(source):
    R = source['tensor']
    a = scalar.ScalarCharacters(R)
    fp_factor, K, ds, D, dimension_polynomial, embedding = a.fp()
    sphere = scalar.character_obstructions(R, a.cf)
    survivors = [row for row in sphere if row['obstruction'] is None]
    need(len(survivors) == 1 and survivors[0]['factor'] == scalar.pc(fp_factor),
         'Exactly the FP Galois orbit survives ordinary spherical characters')
    values, problem, stats = scalar.enumerate_all(R, timeout=1200)
    branches = []
    for value in values:
        T = scalar.from_values(R, problem, value)
        scalar.validate_general(T)
        signs = scalar.proofs.gauge_original(T, R)
        branch = {'signed_values': list(value)}
        if signs is not None:
            # Check the entire signed tensor and dual-compatible lift choice.
            need(signs[0] == 1 and all(signs[i] == signs[a.du[i]] for i in range(8)), 'Dual-compatible gauge')
            need(all(T[i][j][k] == signs[i] * signs[j] * signs[k] * R[i][j][k]
                     for i in range(8) for j in range(8) for k in range(8)), 'Full signed gauge identity')
            branch.update(kind='spherical_section', gauge_signs=signs)
        else:
            aa = scalar.ScalarCharacters(T)
            obstructions = scalar.character_obstructions(T, a.cf + aa.cf)
            need(all(row['obstruction'] is not None for row in obstructions),
                 'A nongauge signed spherical character survives')
            need(all(row['obstruction']['kind'] in ('zero', 'duality', 'norm') for row in obstructions),
                 'Unexpected scope of signed obstruction')
            branch.update(kind='signed_character_exclusion', scalar_rank=aa.scalar_rank,
                          matrix_formal_codegree=str(aa.matrix_codegree),
                          formal_codegrees=[{'polynomial': scalar.pc(f), 'multiplicity': m} for f, m in aa.cf],
                          characters=obstructions)
        branches.append(branch)
    return {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
            'scope': 'general_complex_fusion_category', 'outcome': 'Galois_pseudo_unitary_reduction',
            'scalar_rank': a.scalar_rank, 'matrix_formal_codegree': str(a.matrix_codegree),
            'formal_codegrees': [{'polynomial': scalar.pc(f), 'multiplicity': m} for f, m in a.cf],
            'ordinary_character_generator': a.k, 'ordinary_characters': sphere,
            'fp_character_factor': scalar.pc(fp_factor), 'fp_dimension_polynomial': scalar.pc(dimension_polynomial),
            'ordered_signed_enumeration': {'complete': True, 'variables': len(problem['domains']),
                                           'statistics': stats, 'count': len(values),
                                           'commutativity_assumed': False},
            'signed_branches': branches,
            'conclusion': 'Every categorification has a spherical structure and a pseudo-unitary Galois conjugate. No unitarity or existence claim.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    census = json.loads((OLD / 'pipeline/census_m3.json').read_text())
    output = [compute(next(row for row in census if row['id'] == rid))
              for rid in ('R8_3_721', 'R8_3_1154')]
    path = HERE / 'general_galois_pu_gate.json'
    if args.write:
        path.write_text(json.dumps(output, indent=2) + '\n')
    else:
        need(output == json.loads(path.read_text()), 'Complete scope-gate replay differs')
    for row in output:
        kinds = [b['kind'] for b in row['signed_branches']]
        print('PASS', row['id'], row['ordered_signed_enumeration']['count'], 'complete signed branches;',
              kinds.count('spherical_section'), 'gauge sections;',
              kinds.count('signed_character_exclusion'), 'excluded nongauge branches; Galois pseudo-unitary gate')


if __name__ == '__main__':
    main()
