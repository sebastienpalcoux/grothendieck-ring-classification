#!/usr/bin/env python3
"""Apply exact rank-five categorical certificates to the pinned m=19,20 tensors.

The basic phase accepts only arithmetic certificates rechecked from each
entire tensor. A second phase may apply the costlier general engine to the
remaining tensors. Counts and statuses are separate from census counts.
"""
import argparse
import collections
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'software'))
from census_common import TABLES, canonical, check_axioms
from rings import fingerprint
import unified


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'data/extension19_20/basic.jsonl')
    parser.add_argument('--height',type=int,default=6)
    parser.add_argument('--seconds',type=int,default=45)
    parser.add_argument('--full',action='store_true',help='run the generic engine on non-arithmetic survivors')
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    seen=set();index=collections.Counter();kinds=collections.defaultdict(collections.Counter)
    start=time.monotonic()
    with gzip.open(TABLES,'rt') as inp,args.output.open('w') as output:
        for line in inp:
            N=json.loads(line.replace('{','[').replace('}',']'))
            m=max(x for mat in N for row in mat for x in row)
            if m not in (19,20):continue
            check_axioms(N);can=canonical(N)
            if can in seen:raise RuntimeError('duplicate pinned tensor')
            seen.add(can);index[m]+=1
            c=unified.certificate(N,height=args.height,timeout=args.seconds) if args.full else unified.basic_certificate(N)
            if c is not None:unified.verify(N,c)
            kind=c['kind'] if c is not None else 'not_yet_excluded'
            kinds[m][kind]+=1
            record={'m':m,'repository_index':index[m], 'fingerprint':fingerprint(N),'N':N,'criterion':kind,'certificate':c}
            output.write(json.dumps(record,separators=(',',':'))+'\n')
            if (index[19]+index[20])%500==0:
                output.flush()
                print('processed',dict(index),'status',{m:dict(kinds[m]) for m in (19,20)},'seconds',round(time.monotonic()-start,1),flush=True)
    report={'status':'PASS','source':'pinned repository commit b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
            'phase':'full' if args.full else 'basic','counts':dict(index),
            'criteria':{m:dict(kinds[m]) for m in (19,20)},'seconds':round(time.monotonic()-start,3)}
    args.output.with_suffix('.summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':main()
