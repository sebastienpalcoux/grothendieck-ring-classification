#!/usr/bin/env python3
"""Compare this release with a checked-out fusion-ring-census tensor export.

A based-ring isomorphism fixes the unit and simultaneously permutes the
remaining basis elements. The program compares complete canonical tensors,
never row labels or raw labeled-tensor fingerprints.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def canonical(tensor, maps):
    flat = tuple(x for matrix in tensor for row in matrix for x in row)
    return min(tuple(flat[index] for index in order) for order in maps)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository-tables', type=Path,
                        default=ROOT / 'data/pinned_repository/rank5/tables.txt.gz',
                        help='pinned repository tables, bundled here by default')
    parser.add_argument('--local', type=Path, default=ROOT / 'data/classification_tensors.json')
    parser.add_argument('--through', type=int, default=18)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.through < 1:
        parser.error('--through must be positive')
    maps = [tuple(25*p[i] + 5*p[j] + p[k]
                  for i in range(5) for j in range(5) for k in range(5))
            for p in ((0,) + q for q in itertools.permutations(range(1, 5)))]
    local_sets, remote_sets = defaultdict(set), defaultdict(set)
    local_count = remote_count = 0
    for record in json.loads(args.local.read_text()):
        m = record['m']
        if m <= args.through:
            local_count += 1
            local_sets[m].add(canonical(record['N'], maps))
    with gzip.open(args.repository_tables, 'rt') as data:
        for line in data:
            N = json.loads(line.replace('{', '[').replace('}', ']'))
            m = max(x for matrix in N for row in matrix for x in row)
            if m <= args.through:
                remote_count += 1
                remote_sets[m].add(canonical(N, maps))
    rows = []
    for m in range(1, args.through + 1):
        old, new = local_sets[m], remote_sets[m]
        rows.append({'multiplicity': m, 'local': len(old), 'repository': len(new),
                     'missing_in_repository': len(old - new),
                     'additional_in_repository': len(new - old)})
    success = (local_count == sum(len(v) for v in local_sets.values())
               and remote_count == sum(len(v) for v in remote_sets.values())
               and local_count == remote_count
               and all(r['missing_in_repository'] == r['additional_in_repository'] == 0
                       for r in rows))
    result = {'status': 'PASS' if success else 'FAIL',
              'repository_path': str(args.repository_tables),
              'repository_sha256': digest(args.repository_tables),
              'local_sha256': digest(args.local),
              'through': args.through, 'classes': local_count,
              'repository_rows': remote_count, 'basis_permutations': len(maps),
              'counts': rows}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if not success:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
