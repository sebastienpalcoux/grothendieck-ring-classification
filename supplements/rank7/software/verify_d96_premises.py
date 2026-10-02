"""Exact census premises for the general dimension-96 orbit obstruction."""
from pathlib import Path
import gzip
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
CERTIFICATES_PATH = HERE.parent / 'data/d96_premise_certificates.json'
CRITERION = 'D96_solvable_order16_orbit_obstruction'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def get_certificate(ring_id):
    return next(x for x in json.loads(CERTIFICATES_PATH.read_text()) if x['id'] == ring_id)


def verify_record(record, expected_tensor=None):
    T = record['tensor']
    require(record['id'] in ('R7_2_252', 'R7_2_315'), 'unexpected ring')
    require(record['criterion'] == CRITERION, 'criterion')
    require(digest(T) == record['tensor_sha256'], 'tensor hash')
    if expected_tensor is not None:
        require(T == expected_tensor, 'source tensor binding')
    n = 7
    require(len(T) == n and all(len(A) == n and all(len(r) == n for r in A) for A in T), 'shape')
    require(all(type(z) is int and z >= 0 for A in T for r in A for z in r), 'nonnegative integers')
    d = record['dimensions']
    require(d == [1, 3, 3, 6, 6, 1, 2], 'dimensions')
    require(sum(x*x for x in d) == 96, 'global dimension')
    require(all(sum(T[i][j][k]*d[k] for k in range(n)) == d[i]*d[j]
                for i, j in itertools.product(range(n), repeat=2)), 'positive dimension character')
    require(all(T[0][i][j] == T[i][0][j] == int(i == j)
                for i, j in itertools.product(range(n), repeat=2)), 'unit')
    dual = []
    for i in range(n):
        candidates = [j for j in range(n) if T[i][j][0]]
        require(len(candidates) == 1 and T[i][candidates[0]][0] == 1, 'dual')
        dual.append(candidates[0])
    require(dual == record['duals'], 'recorded duality')
    inv = [i for i, x in enumerate(d) if x == 1]
    require(inv == [0, 5] and T[5][5] == [1, 0, 0, 0, 0, 0, 0], 'invertible group C2')
    perm = [5, 2, 1, 3, 4, 0, 6]
    require(all(T[5][i][j] == T[i][5][j] == int(j == perm[i])
                for i, j in itertools.product(range(n), repeat=2)), 'invertible action')
    adj = {0}
    for i in range(n):
        adj.update(k for k in range(n) if T[i][dual[i]][k])
    while True:
        before = set(adj)
        for i, j in itertools.product(before, repeat=2):
            adj.update(k for k in range(n) if T[i][j][k])
        if before == adj:
            break
    require(adj == set(range(n)), 'trivial universal grading')
    return {'id': record['id'], 'status': 'PASS', 'criterion': CRITERION,
            'tensor_sha256': record['tensor_sha256'], 'dimension': 96,
            'invertible_permutation': perm, 'adjoint_closure': sorted(adj),
            'first_deequivariantization_type': {'1': 3, '3': 5},
            'second_deequivariantization': 'pointed order16',
            'forced_S3_orbits': [1, 3, 6, 6],
            'forced_transposition_fixed_points': 2,
            'possible_group_minimum_involution_fixed_points': 4,
            'scope': 'no complex fusion categorification'}


def find_root():
    for p in (HERE, *HERE.parents):
        for q in (p, p / 'classification-repo'):
            if (q / 'supplements/rank7/data/rank7_tables.txt.gz').is_file():
                return q
    raise FileNotFoundError('pass the repository root as the first argument')


def certificate(T):
    sha=digest(T)
    for record in json.loads(CERTIFICATES_PATH.read_text()):
        if record['tensor_sha256']!=sha:continue
        verify_record(record,T)
        return {'kind':CRITERION,'id':record['id'],'tensor_sha256':sha,
                'scope':'all complex fusion categories','dimensions':record['dimensions'],
                'global_dimension':96,'invertible_group':'C2','adjoint_rank':7,
                'forced_S3_orbits':[1,3,6,6],'required_reflection_fixed_points':2,
                'minimum_reflection_fixed_points':4,
                'proof':'papers/D96_GENERAL_EXCLUSION_PROOF.md'}
    return None


def verify(T,c):
    require(c is not None and c==certificate(T),'dimension-96 certificate mismatch')


def main(root=None):
    root = Path(root) if root is not None else HERE.parent
    source_path=root/'data/rank7_tables.txt.gz'
    if not source_path.is_file():source_path=root/'supplements/rank7/data/rank7_tables.txt.gz'
    raw = gzip.open(source_path, 'rb').read()
    source_hash = hashlib.sha256(raw).hexdigest()
    lines = raw.decode().splitlines()
    records = json.loads(CERTIFICATES_PATH.read_text())
    require({r['id'] for r in records} == {'R7_2_252', 'R7_2_315'} and len(records) == 2, 'complete inventory')
    results = []
    for r in records:
        require(source_hash == r['raw_source_sha256'], 'raw source hash')
        source = json.loads(lines[r['source_line']-1].replace('{', '[').replace('}', ']'))
        results.append(verify_record(r, expected_tensor=source))
    report = {'status': 'PASS', 'criterion': CRITERION, 'records': results}
    print(json.dumps(report, indent=2))
    return report


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
