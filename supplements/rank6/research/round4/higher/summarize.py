"""Collate frozen higher-multiplicity proof and control receipts, without solving."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from frozen_inputs import rows

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(name):
    return json.loads((HERE / name).read_text())


selected = rows(ROOT)
ids = [r['id'] for r in selected]
positive = {r['id'] for r in selected if r['status'] != 'unresolved'}
coverage = read('coverage.json')
c3 = read('c3_controls.json')
e6 = read('e6_controls.json')
for records in (coverage['records'], c3, e6):
    require([r['id'] for r in records] == ids, 'wrong frozen 64-input coverage')
    for r in records:
        outcome = r.get('outcome', r.get('mass_outcome'))
        require(outcome != 'error', 'control error')
        require(not (r['id'] in positive and outcome.endswith('excluded')),
                'false positive exclusion')
retry = read('e6_positive_retry.json')
require(retry['id'] == 'R6_2_127' and
        retry['outcome'] == 'necessary_system_survives', 'incomplete eligible control')

certified = []
for rid in ('R6_6_49', 'R6_6_1035'):
    name = rid + '_general.json'
    certificate = read(name)
    digest = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
    replays = []
    for suffix, optimized in (('_replay.json', False), ('_replay_optimized.json', True)):
        receipt = read(rid + suffix)
        require(receipt['passed'] and receipt['optimizer_used'] is False,
                'failed exact replay')
        require(receipt['python_optimized'] is optimized and
                receipt['certificate_sha256'] == digest, 'mismatched replay')
        replays.append({'path': rid + suffix, **receipt})
    require(certificate['scope'] == 'general', 'incorrect categorical scope')
    certified.append({'id': rid, 'outcome': 'excluded', 'scope': 'general',
                      'certificate': name, 'certificate_sha256': digest,
                      'kind': certificate['kind'], 'replays': replays})

audit_paths = ['../models/c3_independent_audit.json',
               '../models/half_e6_independent_audit.json']
for path in audit_paths:
    require(read(path)['passed'], 'independent audit failure')
probe = read('probe_1204_verlinde.json')
require(probe['outcome'] == 'no_exact_obstruction', 'unexpected open-target outcome')
surviving = [b for b in probe['branches'] if b['ray'] is None]
summary = {
    'kind': 'fourth_continuation_higher_summary', 'version': 1,
    'certified': certified,
    'unresolved': [{'id': 'R6_5_1204', 'low_frames': probe['metadata']['lows'],
                    'outcome': 'necessary_system_survives',
                    'receipt': 'probe_1204_verlinde.json',
                    'surviving_tested_systems': surviving}],
    'controls': {
        'frozen_inputs': 64, 'inherited_frontier': 10, 'realized': len(positive),
        'recognition_and_weak_mass': dict(Counter(r['mass_outcome'] for r in coverage['records'])),
        'cyclic_three': dict(Counter(r['outcome'] for r in c3)),
        'half_e6_original_pass': dict(Counter(r['outcome'] for r in e6)),
        'half_e6_completed_followup': retry,
        'false_positive_exclusions': 0,
        'source_cyclic_three_checks': coverage['cyclic_pointed_source_checks'],
        'input_selector': 'frozen_inputs.py',
    },
    'independent_audits': audit_paths,
    'exploratory_scope': 'Earlier timeouts, surviving relaxations, MILP statuses and '
                         'unsuccessful congruence searches make no categorical claims. '
                         'The final half-E6 exclusion uses the conductor-60 certificate, '
                         'not the secondary degree-eight discovery or real-field MILP.',
}
(HERE / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({'certified': [r['id'] for r in certified],
                  'unresolved': ['R6_5_1204'], 'controls': 64,
                  'replays_passed': 4, 'false_positive_exclusions': 0}))
