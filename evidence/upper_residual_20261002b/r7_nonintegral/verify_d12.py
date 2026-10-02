"""Construct the D12 even fusion tensor from its published fusion formulas."""
import argparse
import itertools
import json
import sys
from pathlib import Path
from case_source import ROOT, SOFTWARE, read_cases, require, fingerprint

sys.path.insert(0, str(SOFTWARE))
from rings import validate, dual

MODEL_TO_CENSUS = [0, 5, 3, 6, 4, 1, 2]
CASE_ID = 'R7_2_240'

def model_tensor():
    # Basis f0, f2, f4, f6, f8, P, Q.  In the SU(2)_20
    # bosonic quotient f_(20-a)=f_a and f10=P+Q.
    tensor = [[[0] * 7 for _ in range(7)] for _ in range(7)]
    for i, j in itertools.product(range(5), repeat=2):
        for label in range(abs(i - j), i + j + 1):
            folded = min(label, 10 - label)
            if folded == 5:
                tensor[i][j][5] += 1
                tensor[i][j][6] += 1
            else:
                tensor[i][j][folded] += 1
    for exceptional in (5, 6):
        for j in range(5):
            for k in range(5 - j, 5):
                tensor[exceptional][j][k] = tensor[j][exceptional][k] = 1
            target = exceptional if j % 2 == 0 else 11 - exceptional
            tensor[exceptional][j][target] = tensor[j][exceptional][target] = 1
    for k in (1, 3, 6):
        tensor[5][5][k] = 1
    for k in (1, 3, 5):
        tensor[6][6][k] = 1
    for k in (0, 2, 4):
        tensor[5][6][k] = tensor[6][5][k] = 1
    return tensor

def verify():
    tensor = model_tensor()
    validate(tensor)
    require(dual(tensor) == [0, 1, 2, 3, 4, 6, 5], 'D12 exceptional duality changed')
    source = read_cases({CASE_ID})[CASE_ID]
    census = source['tensor']
    require(sorted(MODEL_TO_CENSUS) == list(range(7)), 'basis map is not a bijection')
    for i, j, k in itertools.product(range(7), repeat=3):
        require(tensor[i][j][k] == census[MODEL_TO_CENSUS[i]][MODEL_TO_CENSUS[j]][MODEL_TO_CENSUS[k]],
                'D12 full tensor comparison failed')
    # Independent elementary associativity check in integer lists, avoiding
    # reliance on the symbolic matrix implementation used above.
    for i, j, k, output in itertools.product(range(7), repeat=4):
        left = sum(tensor[i][j][a] * tensor[a][k][output] for a in range(7))
        right = sum(tensor[j][k][a] * tensor[i][a][output] for a in range(7))
        require(left == right, 'D12 integer associativity failed')
    return {'status': 'PASS', 'id': CASE_ID, 'scope': 'unitary_modular',
            'source_line': source['source_line'], 'census_tensor_sha256': source['tensor_sha256'],
            'model_tensor_sha256': fingerprint(tensor), 'model_to_census': MODEL_TO_CENSUS,
            'coefficients_compared': 343, 'associativity_equalities': 2401,
            'model_tensor': tensor}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'model_tensor'}, sort_keys=True))

if __name__ == '__main__':
    main()
