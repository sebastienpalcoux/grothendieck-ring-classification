#!/usr/bin/env python3
"""Check exact equality of the released and pinned rank-six source exports."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()


def rows(path):
    with gzip.open(path,'rt') as f:
        for line in f:yield line.rstrip('\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('release_tables',type=Path)
    p.add_argument('repository_tables',type=Path)
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    old=list(rows(a.release_tables))
    live=list(rows(a.repository_tables))
    if not old or len(old)!=len(live) or len(set(old))!=len(old):
        raise ValueError('Source tensor cardinality or literal uniqueness mismatch')
    if old!=live:
        raise ValueError('Tensors or source ordering differ')
    bound=max(max(v for layer in json.loads(line.replace('{','[').replace('}',']'))
                  for row in layer for v in row) for line in old)
    summary={'result':f'{len(old):,} identical full tensor lines in identical order',
             'scope':f'rank 6, multiplicity <= {bound}',
             'release_tables_gz_sha256':sha(a.release_tables),
             'repository_tables_gz_sha256':sha(a.repository_tables),
             'records':len(old)}
    if a.report:a.report.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
