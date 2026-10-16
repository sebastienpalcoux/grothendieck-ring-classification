#!/usr/bin/env python3
"""Source-bound necessary-condition certificate; no full exclusion claimed."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from verify_R2665_inversion_model import dihedral_model, multiply, unit_vector, require, tensor_hash


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source_path = args.repo / 'supplements/rank7/data/rank7_tables.txt.gz'
    counts = collections.Counter()
    source = None
    for line in gzip.open(source_path, 'rt'):
        if not line.strip():
            continue
        tensor = json.loads(line.replace('{', '[').replace('}', ']'))
        m = max(v for a in tensor for b in a for v in b)
        counts[m] += 1
        if m == 4 and counts[m] == 2053:
            source = tensor
    require(source is not None, 'source found')
    inv, X, Y, Z = [0, 1, 2, 6], 4, 3, 5
    require(sum(source[g][g][0] for g in inv) == 2, 'source pointed group C4')
    require(source[X][X] == [int(i in inv) for i in range(7)], 'integral TY square')
    require(source[Y][Y][0] == source[Z][Z][0] == 1, 'self-dual irrational source simples')
    group, index, mul, phi, tensor = dihedral_model(duality_shift=(0, 0))
    rho = unit_vector(16, 8+index[(0, 0)])
    cube = multiply(tensor, multiply(tensor, rho, rho), rho)
    require(tensor[8][8][0] == 1, 'rho selfdual')
    require(cube[:8] == [int(g[1] == 0) for g in group], 'all rotations occur once in rho cubed')
    require(cube[index[(2, 0)]] == cube[0] == 1, 'unit and r squared odd multiplicity')
    indicators = []
    for sign in (1, -1):
        residues = [0] * 4
        for a, b, c in itertools.product(range(4), repeat=3):
            d = (-a-b-c) % 4
            exponent = sign*(a*b+a*c+a*d+b*c+b*d+c*d)
            residues[exponent % 4] += 1
        require(residues == [8, 24, 8, 24], 'exact Shimizu exponent counts')
        require(residues[0] == residues[2] and residues[1] == residues[3], 'indicator vanishes')
        indicators.append({'bicharacter_sign': sign, 'residue_counts': residues, 'nu8': 0})
    out = {
        'status': 'PASS',
        'scope': 'rotational branch excluded; R7_4_2053 still unresolved',
        'classification_changes': 0,
        'source_id': 'R7_4_2053',
        'source_compressed_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'source_tensor_sha256': tensor_hash(source),
        'dihedral_tensor_sha256': tensor_hash(tensor),
        'group_order': group,
        'rho_cubed': cube,
        'indicator_checks': indicators,
        'remaining_neutral_subcategory': 'R8_1_18',
        'optimizer_used': False,
    }
    args.output.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'source': 'R7_4_2053', 'remaining_neutral': 'R8_1_18'}))


if __name__ == '__main__':
    main()
