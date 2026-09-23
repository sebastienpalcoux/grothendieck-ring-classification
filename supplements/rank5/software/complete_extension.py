#!/usr/bin/env python3
"""Apply full categorical criteria to the arithmetic survivors at m=19,20."""
import argparse
import collections
import concurrent.futures
import json
import os
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path

for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'software'))
import unified

class Limit(Exception):pass

def alarm_handler(*args):raise Limit('per-tensor search/check limit reached')

def check(record,height,seconds):
    st=time.monotonic()
    signal.signal(signal.SIGALRM,alarm_handler)
    signal.alarm(seconds*3+30)
    try:
        R=record['N']
        cert=unified.certificate(R,height=height,timeout=seconds)
        if cert:
            unified.verify(R,cert)
            record['criterion']=cert['kind'];record['certificate']=cert
        else:
            record['criterion']='general_residual';record['certificate']=None
            record['diagnostic']='No exact general certificate found by current criteria.'
    except (Limit,TimeoutError,subprocess.TimeoutExpired) as exc:
        record['criterion']='general_residual';record['certificate']=None
        record['diagnostic']=str(exc)
    except Exception:
        record['criterion']='general_residual';record['certificate']=None
        record['diagnostic']='Search/check raised; no exclusion accepted.'
        record['error']=traceback.format_exc()
    finally:
        signal.alarm(0)
    record['seconds']=round(time.monotonic()-st,3)
    return record


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,default=ROOT/'data/extension19_20/basic.jsonl')
    ap.add_argument('--output',type=Path,default=ROOT/'data/extension19_20/full.jsonl')
    ap.add_argument('--jobs',type=int,default=3)
    ap.add_argument('--height',type=int,default=6)
    ap.add_argument('--seconds',type=int,default=40)
    args=ap.parse_args()
    rows=[json.loads(line) for line in args.input.read_text().splitlines()]
    todo=[r for r in rows if r['criterion']=='not_yet_excluded']
    start=time.monotonic();done={};print('categorical survivors to check',len(todo),flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures={pool.submit(check,r,args.height,args.seconds):r for r in todo}
        for f in concurrent.futures.as_completed(futures):
            r=f.result();done[r['fingerprint']]=r
            print('completed',len(done),'/',len(todo),'m',r['m'],'index',r['repository_index'],
                  'criterion',r['criterion'],'seconds',r['seconds'],flush=True)
    output=[done.get(r['fingerprint'],r) for r in rows]
    counts=collections.defaultdict(collections.Counter)
    for r in output:counts[r['m']][r['criterion']]+=1
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w') as stream:
        for r in output:stream.write(json.dumps(r,separators=(',',':'))+'\n')
    summary={'status':'PASS','source':'pinned repository commit b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
             'checked_tensors':len(output),'categorical_survivors_processed':len(todo),
             'by_multiplicity':{str(m):dict(v) for m,v in sorted(counts.items())},
             'seconds':round(time.monotonic()-start,3)}
    args.output.with_suffix('.summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
