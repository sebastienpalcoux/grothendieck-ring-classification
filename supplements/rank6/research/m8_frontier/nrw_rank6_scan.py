"""Reproducible, scope-limited comparison with NRW's rank-six modular tensors.

Input is the unmodified ancillary file of arXiv:2308.09670v2.  GAP code is
not evaluated: only bracket-balanced literal integer arrays are parsed.
This checks literature-model matches, never arbitrary categorifiability.
"""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import re
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_URL = 'https://arxiv.org/src/2308.09670v2/anc/NsdGOL6.g'
SOURCE_SHA256 = 'eeea55e0ae75982b0afcf7d8e936d7cb7d4adae7a42096e719d13b30974fab0b'


def tensors(path):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('NRW source bytes do not match the reviewed version')
    text = re.sub(r'#[^\n]*', '', raw.decode())
    records = []
    for match in re.finditer(r'NsdGOL\[(\d+)\]\[(\d+)\]\s*:=\s*rec\(\s*Nij_k\s*:=\s*', text):
        start = match.end()
        if text[start] != '[':
            raise ValueError('expected an integer tensor literal')
        depth = 0
        for end in range(start, len(text)):
            depth += (text[end] == '[') - (text[end] == ']')
            if depth == 0:
                break
        tensor = ast.literal_eval(text[start:end + 1])
        if len(tensor) != 6 or any(len(m) != 6 or any(len(row) != 6 for row in m) for m in tensor):
            raise ValueError('unexpected tensor dimensions')
        if any(type(x) is not int or x < 0 for m in tensor for row in m for x in row):
            raise ValueError('nonintegral or negative tensor entry')
        if tensor[0] != [[int(i == j) for j in range(6)] for i in range(6)]:
            raise ValueError('source unit is not object zero')
        records.append({'galois_orbit': int(match[1]), 'record': int(match[2]), 'N': tensor})
    if len(records) != len(re.findall(r'\bNij_k\s*:=', text)):
        raise ValueError('some modular-data records were not parsed')
    return records


def canonical(N):
    """Minimum among all 5! basis permutations fixing the tensor unit."""
    return min(tuple(N[p[i]][p[j]][p[k]] for i in range(6) for j in range(6) for k in range(6))
               for tail in itertools.permutations(range(1, 6)) for p in [(0,) + tail])


def histogram(N):
    return tuple(sorted(Counter(x for matrix in N for row in matrix for x in row).items()))


def main():
    records = tensors(HERE / 'NsdGOL6.g')
    by_key = {}
    for record in records:
        by_key.setdefault(canonical(record['N']), []).append(
            {k: record[k] for k in ('galois_orbit', 'record')})
    residuals = json.loads((ROOT / 'data/unresolved_tensors.json').read_text())
    matches = [{'id': row['id'], 'matches': by_key.get(canonical(row['N']), [])} for row in residuals]
    census = json.loads((ROOT / 'data/census.json').read_text())
    source_histograms = {histogram(record['N']) for record in records}
    census_candidates = [row for row in census if histogram(row['N']) in source_histograms]
    census_matches = []
    for row in census_candidates:
        hit = by_key.get(canonical(row['N']), [])
        if hit:
            census_matches.append({'id': row['id'], 'multiplicity': row['m'], 'matches': hit})
    # The current data source, rather than a filename or fixed row number,
    # selects the least unresolved exact multiplicity.
    frontier = min(residuals, key=lambda r: (r['m'], r['index']))
    out = {
        'source_url': SOURCE_URL, 'source_sha256': SOURCE_SHA256,
        'source_title': 'Classification of modular data up to rank 12',
        'source_version': 'arXiv:2308.09670v2',
        'source_records': len(records),
        'galois_orbits': len({r['galois_orbit'] for r in records}),
        'distinct_based_ring_types': len(by_key),
        'largest_source_fusion_coefficient': max(x for record in records for matrix in record['N'] for row in matrix for x in row),
        'census_tensors_screened': len(census),
        'census_tensors_after_invariant_prefilter': len(census_candidates),
        'census_matches': census_matches,
        'unit_fixed_permutations_per_tensor': 120,
        'residual_count': len(residuals),
        'frontier_id': frontier['id'],
        'frontier_tensor_sha256': hashlib.sha256(json.dumps(frontier['N'], separators=(',', ':')).encode()).hexdigest(),
        'matches': matches,
        'scope': ('No match excludes a modular realization of that fusion ring in the complete rank-six list. '
                  'It is not an exclusion of arbitrary, pivotal, spherical, pseudo-unitary or unitary fusion categorification. '
                  'A match is a literature model lead and still requires the categorical realization reference.'),
    }
    (HERE / 'nrw_rank6_scan.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ('matches', 'census_matches')}, indent=2))
    print('Census matching tensors:', ', '.join(row['id'] for row in census_matches))


if __name__ == '__main__':
    main()
