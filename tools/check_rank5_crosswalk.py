#!/usr/bin/env python3
"""Compare every rank-5 tensor in the release archive to the pinned repository.

Based-ring isomorphisms fix the tensor unit and simultaneously permute the
four nonunit basis elements in all three tensor indices.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path

perms = ((0,) + p for p in itertools.permutations(range(1, 5)))
index_maps = [tuple(25*p[i] + 5*p[j] + p[k] for i in range(5) for j in range(5) for k in range(5)) for p in perms]

def canonical(N):
    flat = tuple(x for plane in N for row in plane for x in row)
    return min(tuple(flat[i] for i in index_map) for index_map in index_maps)

def summarize_source(release):
    grouped = {}
    for x in release:
        m = x['m']
        grouped.setdefault(m, set()).add(canonical(x['N']))
    return grouped

def summarize_remote(tables):
    grouped = {}
    count = 0
    with gzip.open(tables, 'rt') as inp:
        for row in inp:
            N = json.loads(row.replace('{','[').replace('}',']'))
            m = max(x for plane in N for vec in plane for x in vec)
            if m > 18: continue
            count += 1
            grouped.setdefault(m, set()).add(canonical(N))
    return grouped, count

def file_digest(path):
    h=hashlib.sha256()
    with path.open('rb') as inp:
        for chunk in iter(lambda:inp.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def set_digest(tuples):
    h=hashlib.sha256()
    for t in sorted(tuples):
        h.update(','.join(map(str,t)).encode('ascii'))
        h.update(b'\n')
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('release_json',type=Path,help='rank-five release data/census_independent.json')
    p.add_argument('repository_tables',type=Path,help='pinned fusion-ring-census results/rank5/tables.txt.gz')
    p.add_argument('--report',type=Path,help='optional JSON report path')
    args=p.parse_args()
    release=json.loads(args.release_json.read_text())
    old=summarize_source(release)
    new,raw_count=summarize_remote(args.repository_tables)
    bands=[]
    print('m,release_count,repository_count,missing_in_repository,additional_in_repository')
    for m in range(1,19):
        a,b=old.get(m,set()),new.get(m,set())
        bands.append({'multiplicity':m,'release_count':len(a),'repository_count':len(b),
                      'missing_in_repository':len(a-b),'additional_in_repository':len(b-a),
                      'canonical_set_sha256':set_digest(a) if a==b else None})
        print(f'{m},{len(a)},{len(b)},{len(a-b)},{len(b-a)}')
    print('raw_repository_prefix_count',raw_count)
    assert sum(map(len,old.values())) == sum(map(len,new.values())) == len(release) == raw_count == 28493
    assert all(old.get(m,set()) == new.get(m,set()) for m in range(1,19))
    if args.report:
        report={'method':'lexicographic minimum of tensor flattening over all 24 simultaneous unit-fixing basis permutations',
                'release_sha256':file_digest(args.release_json),
                'repository_tables_gz_sha256':file_digest(args.repository_tables),
                'verified_records':raw_count,'bands':bands}
        args.report.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
