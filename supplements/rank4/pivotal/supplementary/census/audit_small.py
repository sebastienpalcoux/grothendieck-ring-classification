#!/usr/bin/env python3
"""Independent small-bound check by exhaustive parameter boxes (default M=2).
No elimination equations or minimal-coordinate reductions are used.
"""
import argparse
import itertools
import json
from pathlib import Path
import tempfile
import time
from generate import generate
from rank4 import tensor,canonical,casimir,leading_minors,require

def commute(A,B):
    # Inspect genuine matrix products, without the enumerator's equations.
    for i in range(4):
        for j in range(4):
            if sum(A[i][k]*B[k][j]-B[i][k]*A[k][j] for k in range(4)):
                return False
    return True

def run(M):
    require(1<=M<=2,'exhaustive test allows only M=1 or 2')
    start=time.monotonic();keys=set();boxes=0
    for tag,length in [('S',10),('N',6)]:
        for p in itertools.product(range(M+1),repeat=length):
            boxes+=1;R=tensor(tag,p)
            if not all(commute(R[i],R[j])for i,j in [(1,2),(1,3),(2,3)]):continue
            minors=leading_minors(casimir(R))
            if len(minors)==4 and min(minors)>0:keys.add(canonical(R))
    with tempfile.TemporaryDirectory(prefix='rank4-box-audit-')as tmp:
        output=Path(tmp);generate(output,M)
        observed={canonical(json.loads(line)['tensor'])for line in (output/'rings.jsonl').read_text().splitlines()}
    require(observed==keys,'exhaustive box mismatch')
    report={'maximum_multiplicity':M,'parameter_assignments':boxes,
            'rings':len(keys),'exact_set_equality':True,
            'elapsed_seconds':round(time.monotonic()-start,3)}
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-multiplicity',type=int,default=2)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();report=run(args.max_multiplicity)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
