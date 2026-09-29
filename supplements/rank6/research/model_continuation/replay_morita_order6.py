"""Replay the order-six Morita proof, including rejection of corrupt witnesses.

Run from any directory with Python or Python -O. All guard checks use
VerificationError, so optimization cannot remove mathematical checks.
"""
import copy
import json
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(P / 'software'))
from exact import VerificationError, require
from rings import permute
from new_morita_order6 import verify, finite_dual_classification


def replay():
    rows = json.loads((P / 'research/model_continuation/morita_order6_certificates.json').read_text())
    finite = finite_dual_classification()
    require(finite == rows['finite_dual_classification'], 'recorded finite classification differs')
    census = {r['id']: r['N'] for r in json.loads((P / 'data/census.json').read_text())}
    checks = []
    for row in rows['exclusions']:
        rid = row['id']
        R, c = census[rid], row['certificate']
        verify(R, c, False)
        mutations = [
            ('involution', lambda x: x.__setitem__('involution', 0)),
            ('missing_branch', lambda x: x.__setitem__('branches', [])),
            ('search_size', lambda x: x.__setitem__('generator_tuples', x['generator_tuples'] + 1)),
            ('branch_matrix', lambda x: x['branches'][0]['T'][0].__setitem__(0, 2)),
            ('dimension_count', lambda x: x['branches'][0]['dual_dimensions'][0].__setitem__(1, 5)),
        ]
        for name, mutate in mutations:
            bad = copy.deepcopy(c)
            mutate(bad)
            try:
                verify(R, bad, False)
            except VerificationError:
                checks.append([rid, name, 'rejected'])
            else:
                raise VerificationError('mutation accepted: ' + name)
        p = list(range(6))
        g = c['involution']
        h = next(k for k in range(1, 6) if k != g)
        p[g], p[h] = p[h], p[g]
        try:
            verify(permute(R, p), c, False)
        except VerificationError:
            checks.append([rid, 'relabelled_input_with_stale_certificate', 'rejected'])
        else:
            raise VerificationError('stale certificate accepted')
    require(len(rows['exclusions']) == 2, 'unexpected application domain')
    return {'optimized': bool(sys.flags.optimize), 'finite_domain_matches_record': True,
            'valid_certificates': len(rows['exclusions']), 'mutation_checks': checks}


if __name__ == '__main__':
    print(json.dumps(replay(), indent=2))
