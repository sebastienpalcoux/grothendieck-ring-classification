#!/usr/bin/env python3
"""Audit simple multiplicity-one model rings through rank 11 using exact tensors.

Simplicity means absence of a proper nontrivial based fusion subring containing
the unit. Generator closures and exhaustive subsets are checked independently.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'site/dist/data'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def proper_subring(tensor):
    n = len(tensor)
    dual = [next(j for j in range(n) if tensor[i][j][0]) for i in range(n)]
    closures = []
    for generator in range(1, n):
        closed = {0, generator}
        while True:
            old = set(closed)
            closed.update(dual[i] for i in old)
            closed.update(k for i in old for j in old for k, c in enumerate(tensor[i][j]) if c)
            if closed == old:
                break
        if len(closed) < n:
            closures.append(sorted(closed))
    return min(closures, key=lambda s: (len(s), s)) if closures else None


def exhaustive_proper_subring(tensor):
    n = len(tensor)
    dual = [next(j for j in range(n) if tensor[i][j][0]) for i in range(n)]
    support = [[sum(1 << k for k, c in enumerate(tensor[i][j]) if c) for j in range(n)] for i in range(n)]
    for bits in range(3, (1 << n) - 1, 2):
        subset = [i for i in range(n) if bits >> i & 1]
        if any(not (bits >> dual[i] & 1) for i in subset):
            continue
        if all(support[i][j] & ~bits == 0 for i in subset for j in subset):
            return subset
    return None


def identify(ring):
    n = ring['rank']; tensor = ring['fusion_tensor']
    if len(ring['invariants']['invertible_indices']) == n:
        require(n in (2, 3, 5, 7, 11), 'Unexpected simple pointed rank')
        basis = [0]
        for _ in range(n - 1):
            product = tensor[basis[-1]][1]
            require(sum(product) == 1, 'Pointed product must be a basis element')
            basis.append(product.index(1))
        require(len(set(basis)) == n, 'Cyclic generator does not generate')
        standard = [[[int(k == (i + j) % n) for k in range(n)] for j in range(n)] for i in range(n)]
        name = f'K0(Vec(C{n})) = Z[C{n}]'
    else:
        level = 2 * n - 1
        theta = math.pi / (level + 2)
        dimensions = [math.sin((2 * i + 1) * theta) / math.sin(theta) for i in range(n)]
        source_dims = ring['invariants']['frobenius_perron_dimensions_approx']
        basis = [min(range(n), key=lambda j: abs(source_dims[j] - d)) for d in dimensions]
        require(len(set(basis)) == n and all(abs(source_dims[basis[i]] - dimensions[i]) < 1e-7 for i in range(n)), 'Quantum-dimension matching failed')
        standard = [[[int(abs(2*i - 2*j) <= 2*k <= min(2*i + 2*j, 2*level - 2*i - 2*j)) for k in range(n)] for j in range(n)] for i in range(n)]
        name = f'K0(PSU(2)_{level})' + (' = Fibonacci' if n == 2 else '')
    require(basis[0] == 0 and all(tensor[basis[i]][basis[j]][basis[k]] == standard[i][j][k] for i in range(n) for j in range(n) for k in range(n)), 'Full exact model identification failed: ' + ring['id'])
    return name, basis


def audit():
    source_paths = [DATA / name for name in ('realized_rings.json', 'unresolved_cases.json', 'rank9_rank10_m1.json', 'rank11_m1.json')]
    old, unresolved, *updates = [json.loads(p.read_text()) for p in source_paths]
    models = old['records'] + [r for update in updates for r in update['cases'] if r['status'] == 'unitarily_realized']
    pending = unresolved['cases'] + [r for update in updates for r in update['cases'] if r['status'] == 'unresolved']
    candidates = [r for r in models + pending if r['multiplicity'] == 1 and r['rank'] <= 11]
    require(len({r['id'] for r in candidates}) == len(candidates), 'Duplicate audit input')
    simple, open_witnesses = [], []
    for ring in sorted(candidates, key=lambda r: (r['rank'], r['id'])):
        tensor = ring['fusion_tensor']
        require(max(c for matrix in tensor for row in matrix for c in row) == 1, 'Multiplicity label differs from tensor')
        digest = hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()
        require(digest == ring['tensor_sha256'], 'Tensor digest differs: ' + ring['id'])
        witness = proper_subring(tensor)
        require((witness is None) == (exhaustive_proper_subring(tensor) is None), 'Independent simplicity checks disagree')
        if ring.get('status') == 'unresolved':
            require(witness is not None, 'A simple unresolved case prevents completeness')
            open_witnesses.append({'id': ring['id'], 'proper_fusion_subring_indices': witness})
        elif witness is None:
            name, basis = identify(ring)
            simple.append({'rank': ring['rank'], 'id': ring['id'], 'model': name, 'standard_to_source_basis': basis, 'tensor_sha256': digest})
    require(len(simple) == 15 and not open_witnesses, 'Unexpected simple/open inventory')
    return {'schema': 'simple-multiplicity-one/v1', 'rank_range': [2, 11], 'definition': 'No proper nontrivial based fusion subring containing the unit.',
            'checked_models': len(candidates) - len(open_witnesses), 'simple_models': simple, 'unresolved_nonsimple_witnesses': open_witnesses,
            'sources': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}}


def markdown(result):
    lines = ['# Simple multiplicity-one Grothendieck rings through rank 11', '',
             'There are **15 nontrivial rings** in the current classification. Simplicity means that the distinguished basis has no proper nontrivial subset, containing the unit, closed under products and duality. Rings are counted up to based-ring isomorphism, rather than counting their different categorifications.', '',
             '| Rank | Census identifier | Ring |', '|---:|---|---|']
    for row in result['simple_models']:
        lines.append(f"| {row['rank']} | `{row['id']}` | {row['model']} |")
    lines += ['', 'Here PSU(2)_k is the even-label fusion subcategory of SU(2)_k; k = 2r − 1 gives rank r. The rank-one ring K0(Vec) = Z may be added if the trivial ring is included.', '',
              'Every nonunit basis generator was closed under products and duality. Independent enumeration of all unit-containing subsets gives the same simplicity decisions. The cyclic and quantum-group identifications above were verified against every integer fusion coefficient after the recorded basis permutations. Numerical dimensions only select a candidate permutation; the final identification is exact.', '',
              'Every multiplicity-one candidate in the published rank range is now decided. The newly realized R10_1_189 is nonsimple and adds no row to this list. Its pointed C5 subcategory is proper.', '']
    for row in result['unresolved_nonsimple_witnesses']:
        lines.append(f"| `{row['id']}` | {row['proper_fusion_subring_indices']} |")
    lines += ['', 'Replay from the repository root:', '', '```bash', 'python tools/list_simple_multiplicity_one.py --check', '```', '',
              'The exact input hashes and basis permutations are recorded in [the audit data](../data/simple_multiplicity_one_through_rank11.json). As elsewhere in this project, the completeness statement uses the current census and categorification decisions; independent human verification remains pending.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = audit()
    outputs = {ROOT / 'data/simple_multiplicity_one_through_rank11.json': json.dumps(result, indent=2) + '\n', ROOT / 'docs/SIMPLE_MULTIPLICITY_ONE.md': markdown(result)}
    for path, text in outputs.items():
        if args.write:
            path.write_text(text)
        if args.check:
            require(path.read_text() == text, 'Audit output is stale: ' + str(path))
    print(f"Checked {result['checked_models']} multiplicity-one model tensors: 15 simple rings; no unresolved multiplicity-one candidate remains.")
    if not args.check:
        print(markdown(result))
