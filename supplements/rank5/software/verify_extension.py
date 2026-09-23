#!/usr/bin/env python3
"""Recheck the pinned rank-five m=19,20 exclusions against every source tensor."""
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[name] = '1'
import argparse
import collections
import concurrent.futures
import csv
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'software'))
from census_common import TABLES, COUNTS, TABLES_SHA256, canonical, check_axioms
from exact import require
from rings import fingerprint


def check_one(record):
    import unified
    require(record['certificate'] is not None, 'uncertified extension tensor')
    require(record['criterion'] == record['certificate']['kind'], 'criterion mismatch')
    unified.verify(record['N'], record['certificate'])
    return record['criterion']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--input', type=Path,
                        default=ROOT / 'data/extension19_20/full.jsonl')
    parser.add_argument('--output', type=Path,
                        default=ROOT / 'verification/extension19_20_verification.json')
    args = parser.parse_args()
    require(1 <= args.jobs <= 16, 'jobs must lie in 1..16')
    start = time.monotonic()
    require(hashlib.sha256(TABLES.read_bytes()).hexdigest() == TABLES_SHA256,
            'pinned source tensor hash mismatch')
    counts = {}
    with COUNTS.open(newline='') as stream:
        for row in csv.reader(stream):
            if row and row[0].isdigit() and int(row[0]) == 5:
                counts[int(row[1])] = int(row[2])
    require(19 in counts and 20 in counts, 'source count rows missing')
    records = [json.loads(line) for line in args.input.read_text().splitlines()]
    require(len(records) == counts[19] + counts[20], 'extension coverage size mismatch')
    by_m = collections.Counter()
    seen = set()
    with gzip.open(TABLES, 'rt') as source:
        for line in source:
            tensor = json.loads(line.replace('{', '[').replace('}', ']'))
            m = max(x for matrix in tensor for row in matrix for x in row)
            if m not in (19, 20):
                continue
            k = by_m[m]
            index = sum(by_m.values())
            require(index < len(records), 'source has extra tensor')
            record = records[index]
            require(record['m'] == m and record['repository_index'] == k + 1,
                    'pinned repository tensor order mismatch')
            require(record['N'] == tensor, 'extension tensor differs from pinned source')
            require(record['fingerprint'] == fingerprint(tensor),
                    'extension fingerprint mismatch')
            check_axioms(tensor)
            can = canonical(tensor)
            require(can not in seen, 'duplicate extension isomorphism class')
            seen.add(can)
            by_m[m] += 1
    require({m: by_m[m] for m in (19, 20)} == {m: counts[m] for m in (19, 20)},
            'pinned source totals mismatch')
    print(f'PASS pinned-source coverage: {len(records)} m=19,20 tensors, all pairwise nonisomorphic.', flush=True)
    allocation = collections.defaultdict(collections.Counter)
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as workers:
        for index, kind in enumerate(workers.map(check_one, records, chunksize=20), 1):
            allocation[records[index-1]['m']][kind] += 1
            if index % 1000 == 0:
                print(f'{index}/{len(records)} extension exclusion certificates rechecked.', flush=True)
    require(all(sum(allocation[m].values()) == counts[m] for m in (19, 20)),
            'uncertified extension tensor')
    result = {'status': 'PASS', 'pinned_repository_commit':
              'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
              'source_tables_sha256': TABLES_SHA256,
              'checked_tensors': len(records), 'general_exclusions': len(records),
              'counts': {str(m): counts[m] for m in (19, 20)},
              'criterion_allocation': {str(m): dict(sorted(allocation[m].items()))
                                       for m in (19, 20)},
              'seconds': round(time.monotonic() - start, 3)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
