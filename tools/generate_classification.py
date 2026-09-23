#!/usr/bin/env python3
"""Summarize the attached rank 4–6 classification ledgers, preserving gaps.

Run with the four paths shown by ``--help``. This script never assigns a
categorifiability decision to a census ring absent from the relevant ledger.
"""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def records(rank, path):
    if rank == 4:
        with gzip.open(path, 'rt') as inp:
            for line in inp:
                row = json.loads(line)
                if 'multiplicity' in row:
                    yield row['multiplicity'], row['status']
    else:
        for row in json.loads(path.read_text()):
            yield row['m'], row['general'] if rank == 5 else row['status']


def export(args):
    census = json.loads(args.census.read_text())
    by_rank = {}
    for rank in (4, 5, 6):
        path = getattr(args, f'rank{rank}')
        summary = defaultdict(Counter)
        for m, status in records(rank, path):
            assert isinstance(m, int) and m > 0
            summary[m][status] += 1
        by_rank[rank] = summary
        assert set(summary) == set(range(1, max(summary) + 1))
        assert all(sum(summary[m].values()) == census['ranks'][str(rank)]['counts'][str(m)]
                   for m in summary)
        expected = {4: (128, 889530), 5: (18, 28493), 6: (7, 9613)}[rank]
        assert (max(summary), sum(map(sum, (x.values() for x in summary.values())))) == expected

    data = []
    for rank in (4, 5, 6):
        census_counts = census['ranks'][str(rank)]['counts']
        for m in sorted(map(int, census_counts)):
            statuses = by_rank[rank].get(m, Counter())
            excluded = statuses.get('excluded', 0)
            realized_unitary = statuses.get('unitarily_realized', 0)
            realized_unspecified = statuses.get('realized', 0)
            realized_spherical_nonpseudo = statuses.get('spherically_realized_nonpseudounitary', 0)
            unresolved = statuses.get('unresolved', 0)
            assessed = sum(statuses.values())
            rings = census_counts[str(m)]
            assert assessed in (0, rings)
            if assessed == 0:
                coverage = 'census_only'
            elif unresolved:
                coverage = 'partial_classification'
            else:
                coverage = 'complete_classification'
            data.append(dict(rank=rank, multiplicity=m, rings=rings,
                             excluded_general=excluded,
                             realized_unitary=realized_unitary,
                             realized_other_or_unspecified=realized_unspecified,
                             realized_spherical_nonpseudounitary=realized_spherical_nonpseudo,
                             unresolved_general=unresolved, unassessed=rings-assessed,
                             classification_coverage=coverage))

    inputs = {f'rank{rank}': {'file': getattr(args, f'rank{rank}').name,
                              'sha256': digest(getattr(args, f'rank{rank}')),
                              'classified_through': max(by_rank[rank]),
                              'status_totals': dict(sum(by_rank[rank].values(), Counter()))}
              for rank in (4, 5, 6)}
    out = dict(schema='grothendieck-ring-classification/status/v1',
               semantics='Rows count based-isomorphism classes. Unresolved means a general categorification decision remains open in the attached release; unassessed means no classification ledger for this census band. Realized means at least one realization, not every categorification has the given structure.',
               bundle={'name':'FusionFrontier.tar.xz','sha256':digest(args.bundle)},
               inputs=inputs, rows=data)
    target = ROOT/'data/classification_status.json'
    target.write_text(json.dumps(out, indent=2)+'\n')
    with (ROOT/'data/classification_status.csv').open('w', newline='') as stream:
        writer=csv.DictWriter(stream, fieldnames=list(data[0]))
        writer.writeheader();writer.writerows(data)
    print('Wrote status for', len(data), 'rank/multiplicity bands:',
          [(r,max(by_rank[r]),sum(map(sum,(x.values() for x in by_rank[r].values()))))
           for r in (4,5,6)])


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle', required=True, type=Path)
    p.add_argument('--census', required=True, type=Path)
    for r in (4,5,6):p.add_argument(f'--rank{r}', required=True, type=Path)
    export(p.parse_args())
