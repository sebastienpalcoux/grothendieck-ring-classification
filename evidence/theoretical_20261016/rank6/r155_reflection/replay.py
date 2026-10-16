"""Replay all 226 necessary reflection partitions without running a search.

Standard library only. No braid representation or categorification is claimed.
"""
import hashlib
import json
from pathlib import Path
import r155_braid_reflections as extension
import r155_braid_scott as base
from reflection_test import reflection_test

HERE = Path(__file__).resolve().parent
source = (HERE / 'r155_data.json').read_bytes()
base.require(hashlib.sha256(source).hexdigest() == base.DATA_SHA256,
             'inherited modular input hash mismatch')
data = base.Input(json.loads(source))
profiles = json.loads((HERE / 'partitions.json').read_text())
base.require(len(profiles) == 80, 'expected 80 normalized profiles')
used = set()
blocks = []
for a in range(data.n):
    for b in range(data.n):
        dimension = data.dimension(a, b)
        if dimension <= 4:
            continue
        profile = base.canonical(data.spectra(a, b))
        key = base.digest(profile)
        base.require(key in profiles, 'missing exact normalized profile')
        row = profiles[key]
        stored = tuple(tuple(tuple(x) for x in leg) for leg in row['spectra_mod144'])
        base.require(profile == stored, 'stored spectra disagree with modular input')
        base.Search(profile, 0, 0).verify_witness(row['partition'])
        used.add(key)
        blocks.append([a, b, dimension, key])
base.require(len(blocks) == 226 and len(used) == 80, 'incomplete block coverage')

# This is a local irreducibility restriction, not a categorical exclusion.
profile = base.canonical(data.spectra(16, 3))
exponents = tuple(tuple(e for e, m in leg) for leg in profile)
counts = tuple(tuple(m for e, m in leg) for leg in profile)
base.require(extension.scott_admissible(exponents, counts), 'expected Scott pass')
allowed, trace, reason = reflection_test(exponents, counts)
base.require(not allowed, 'expected full dimension-ten irreducibility obstruction')

files = ['r155_data.json', 'su2_4_control.json', 'r155_braid_scott.py',
         'reflection_test.py', 'r155_braid_reflections.py', 'partitions.json', 'replay.py']
receipt = {
    'status': 'PASS',
    'scope': 'Necessary spectral partitions only; R6_4_155 remains unresolved in every categorification scope.',
    'algorithm': 'Scott inequalities plus multiplicative-preprojective reflection necessary conditions',
    'recorded_blocks': 226, 'distinct_normalized_profiles': 80,
    'dimension_range': [min(v[2] for v in blocks), max(v[2] for v in blocks)],
    'verdicts': {'PASS_NECESSARY': 226}, 'unknown': 0,
    'blocks_sha256': base.digest(blocks),
    'files_sha256': {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in files},
    'controls': base.self_test(),
    'local_restriction': {'block': [16, 3], 'dimension': 10,
                          'Scott_full_block': 'PASS_NECESSARY',
                          'reflection_full_block': 'CANNOT_BE_IRREDUCIBLE',
                          'reflection_trace': trace, 'reason': reason,
                          'passing_partition_dimensions': [sum(p[0]) for p in profiles[base.digest(profile)]['partition']]},
    'theoretical_source': 'Crawley-Boevey--Shaw, arXiv:math/0404186v2, Theorem 1.7, Lemmas 5.1 and 8.3',
}
(HERE / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: receipt[k] for k in ['status', 'recorded_blocks',
      'distinct_normalized_profiles', 'dimension_range', 'verdicts', 'unknown']}, indent=2))
