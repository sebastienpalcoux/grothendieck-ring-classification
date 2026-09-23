#!/usr/bin/env python3
"""Check that a released rank-six tensor list is the source census through 7."""
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
    live=[]
    for line in rows(a.repository_tables):
        m=max(map(int,line.replace('{','').replace('}','').split(',')))
        if m<=7:live.append(line)
    assert len(old)==len(live)==9613
    assert len(set(old))==9613
    assert old==live, 'Tensors or source ordering differ'
    summary={'result':'9,613 identical full tensor lines in identical order',
             'scope':'rank 6, multiplicity <= 7',
             'release_tables_gz_sha256':sha(a.release_tables),
             'repository_tables_gz_sha256':sha(a.repository_tables),
             'records':len(old)}
    if a.report:a.report.write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
