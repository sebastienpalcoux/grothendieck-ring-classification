"""Exact necessary-condition audit of the 44 source-stage residual tensors.

Passing the FP index condition is not a categorification certificate.
Requires Python 3 and SymPy. No floating-point arithmetic is used.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
args = parser.parse_args()
repo = args.repo.resolve()
evidence = repo / 'evidence/theoretical_20261016/rank8'
source = repo / 'supplements/rank8/data/rank8_tables.txt.gz'
residual_source = repo / 'evidence/upper_residual_20261002c/remaining_ids.json'
expected = json.loads(residual_source.read_text())['8']
characters = json.loads((evidence / 'fp_characters.json').read_text())
ledger = {r['id']: r for r in json.loads((repo / 'supplements/rank8/data/decisions.json').read_text())}
flat = lambda R: tuple(x for a in R for b in a for x in b)
rows = [json.loads(line.replace('{', '[').replace('}', ']')) for line in gzip.open(source, 'rt')]
tensors = {}
for m in (1, 2):
    selected = sorted((R for R in rows if max(flat(R)) == m), key=flat)
    tensors.update({f'R8_{m}_{i+1}': R for i, R in enumerate(selected)})

def need(condition, message):
    if not condition:
        raise ValueError(message)

need(len(expected) == len(set(expected)) == 44, 'Original residual set must have 44 distinct cases')
need(set(characters) == set(expected) - {'R8_2_857'}, 'Exact-character coverage')
q = s.Symbol('q')
reports = []
for identifier in expected:
    R = tensors[identifier]
    sha = hashlib.sha256(json.dumps(R, separators=(',', ':')).encode()).hexdigest()
    need(sha == ledger[identifier]['tensor_sha256'], f'{identifier}: tensor hash mismatch')
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    subrings = []
    for size in range(2, 8):
        for tail in itertools.combinations(range(1, 8), size - 1):
            S = (0,) + tail
            if any(dual[i] not in S for i in S):
                continue
            if any(R[i][j][k] for i in S for j in S for k in range(8) if k not in S):
                continue
            subrings.append(S)
    report = {'id': identifier, 'tensor_sha256': sha,
              'proper_nontrivial_fusion_subring_count': len(subrings)}
    if identifier == 'R8_2_857':
        need(not subrings, 'R857 has an unhandled proper fusion subring')
        report.update({'index_condition': 'VACUOUS', 'exact_FP_character_checked': False,
                       'reason': 'Exact enumeration finds no proper nontrivial fusion subring; no FP character is needed.'})
        reports.append(report)
        continue
    ds = [s.sympify(x, locals={'sqrt': s.sqrt}) for x in characters[identifier]]
    need(len(ds) == 8 and ds[0] == 1, f'{identifier}: unital character')
    need(all(x.is_positive is True for x in ds), f'{identifier}: exact positivity')
    for i, j in itertools.product(range(8), repeat=2):
        need(s.simplify(ds[i] * ds[j] - sum(R[i][j][k] * ds[k] for k in range(8))) == 0,
             f'{identifier}: dimension character product {i},{j}')
    D = s.simplify(sum(x*x for x in ds))
    indices = []
    for S in subrings:
        E = s.simplify(sum(ds[i]**2 for i in S))
        ratio = s.simplify(D/E)
        mp = s.Poly(s.minpoly(ratio, q), q).monic()
        integral = all(c.q == 1 for c in mp.all_coeffs())
        indices.append({'labels': list(S), 'subcategory_FP_dimension': str(E),
                        'index': str(ratio),
                        'monic_minimal_polynomial_coefficients': list(map(str, mp.all_coeffs())),
                        'algebraic_integer': integral})
    outcome = 'FAIL' if any(not x['algebraic_integer'] for x in indices) else ('PASS' if indices else 'VACUOUS')
    report.update({'index_condition': outcome, 'exact_FP_character_checked': True,
                   'FP_dimensions': list(map(str, ds)), 'global_FP_dimension': str(D), 'indices': indices})
    reports.append(report)
need([r['id'] for r in reports if r['index_condition'] == 'FAIL'] == ['R8_2_209'],
     'Expected unique source-stage subcategory-index exclusion')
print(json.dumps({'audit_status': 'PASS',
                  'meaning': 'All 44 source tensors bound and all proper nontrivial fusion-subring indices audited; PASS is only a necessary condition.',
                  'census_gzip_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                  'residual_list_sha256': hashlib.sha256(residual_source.read_bytes()).hexdigest(),
                  'character_file_sha256': hashlib.sha256((evidence/'fp_characters.json').read_bytes()).hexdigest(),
                  'case_count': len(reports),
                  'summary': {k: sum(r['index_condition'] == k for r in reports) for k in ('PASS', 'FAIL', 'VACUOUS')},
                  'cases': reports}, indent=2))
