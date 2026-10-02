"""Source-bound inventory; an inventory entry is not an exclusion certificate."""
import json
import sys
from pathlib import Path
from case_source import ROOT, SOFTWARE, read_cases, require
sys.path.insert(0, str(SOFTWARE))
from rings import Characters, matrices
from exact import embeddings, pc, s, t

HERE = Path(__file__).resolve().parent

def main():
    old = json.loads((ROOT / 'evidence/upper_residual_20261002b_recovery/previous_records.json').read_text())
    records = [record for record in old if record['rank'] == 7]
    require(len(records) == 59, 'baseline rank-seven open inventory changed')
    cases = read_cases({record['id'] for record in records})
    output = []
    for record in records:
        case_id = record['id']
        case = cases[case_id]
        if record['commutative']:
            degree = Characters(case['tensor']).fp()[0].degree()
            method = 'exact_commutative_dimension_character'
        else:
            matrix = sum(matrices(case['tensor']), s.zeros(7))
            require(all(value > 0 for value in matrix), 'PF sum matrix must be strictly positive')
            factors = matrix.charpoly(t).as_poly().factor_list()[1]
            candidates = [(factor, embedding) for factor, multiplicity in factors
                          for embedding in embeddings(factor)]
            factor, embedding = max(candidates, key=lambda pair: pair[1].hi)
            require(all(other.hi < embedding.lo for other_factor, other in candidates
                        if other is not embedding), 'PF root interval is not separated')
            degree = factor.degree()
            method = 'exact_positive_sum_matrix_PF_root'
        if degree == 1:
            continue
        item = {'id': case_id, 'source_line': case['source_line'],
                'tensor_sha256': case['tensor_sha256'], 'commutative': record['commutative'],
                'fp_dimension_field_degree': degree, 'nonintegrality_check': method}
        if case_id in ('R7_3_1036', 'R7_3_1044', 'R7_4_2510', 'R7_4_2706'):
            item.update(status='excluded', scope='general_complex', certificate=f'{case_id}_general.json')
        elif case_id == 'R7_2_240':
            item.update(status='unitarily_realized', scope='unitary_modular', certificate='r7_2_240_source.json')
        elif case_id in ('R7_4_1212', 'R7_4_1213', 'R7_4_1417', 'R7_4_1420'):
            item.update(status='unresolved', scoped_exclusion='pivotal_only', certificate='pivotal_certificates.json')
        else:
            item.update(status='unresolved', new_decision=None)
        output.append(item)
    require(len(output) == 41, 'nonintegral baseline input count changed')
    result = {'rank': 7, 'baseline_general_open': 59, 'nonintegral_inputs': 41,
              'new_general_exclusions': 4, 'new_unitary_models': 1,
              'new_pivotal_only_exclusions': 4, 'cases': output}
    (HERE / 'coverage.json').write_text(json.dumps(result, indent=2) + '\n')
    print('41 source-bound nonintegral inputs; 4 general exclusions, 1 model, 4 pivotal-only obstructions.')

if __name__ == '__main__':
    main()
