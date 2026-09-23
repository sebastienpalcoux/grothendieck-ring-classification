#!/usr/bin/env python3
"""Apply the same tensor criteria to a census selection or an external tensor.

Discovery is not verification: a candidate ray or decision is emitted only
when the exact checker accepts it. A timeout or unavailable criterion yields
UNRESOLVED, never an exclusion. No existing decision ledger is consulted.
"""
import os
for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[v]='1'
import argparse,json,signal,time,traceback,subprocess
from pathlib import Path
import unified
P=Path(__file__).resolve().parents[1]

class SearchTimeout(Exception):pass
def _alarm(*args):raise SearchTimeout('total per-tensor search limit reached')

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--multiplicity',type=int)
    a.add_argument('--index',type=int,help='local archival ordinal within exact multiplicity')
    a.add_argument('--tensor',type=Path,help='JSON fusion tensor; no census label needed')
    a.add_argument('--census',type=Path,default=P/'data/classification_tensors.json')
    a.add_argument('--height',type=int,default=6)
    a.add_argument('--seconds',type=int,default=120,help='total limit; signed subprocess receives half this allowance')
    a.add_argument('--output',type=Path,default=P/'verification/new_discovery.jsonl')
    x=a.parse_args();unified.require(x.height>=3 and x.seconds>=2,'height >=3, seconds >=2 required')
    if x.tensor:
        obj=json.load(open(x.tensor));R=obj.get('N',obj.get('tensor')) if isinstance(obj,dict) else obj
        rows=[{'N':R}]
    else:
        rows=[r for r in json.load(open(x.census)) if (x.multiplicity is None or r['m']==x.multiplicity) and (x.index is None or r['local_index']==x.index)]
    unified.require(bool(rows),'empty census selection')
    registry=unified.build_model_registry();x.output.parent.mkdir(parents=True,exist_ok=True)
    signal.signal(signal.SIGALRM,_alarm)
    with x.output.open('w') as out:
        for row in rows:
            R=row['N'];unified.validate(R);st=time.monotonic();record={k:row[k] for k in ('m','j','local_index') if k in row}
            record['fingerprint']=unified.fingerprint(R)
            try:
                signal.alarm(x.seconds)
                model=unified.match_model(R,registry)
                if model:record.update(status='realized',model=model)
                else:
                    cert=unified.certificate(R,height=x.height,timeout=max(1,x.seconds//2))
                    if cert:
                        unified.verify(R,cert);record.update(status='excluded',certificate=cert)
                    else:record.update(status='unresolved',diagnostic='No certificate returned by the implemented criteria.')
            except (SearchTimeout,TimeoutError,subprocess.TimeoutExpired) as e:
                record.update(status='unresolved',diagnostic=str(e))
            except Exception:
                record.update(status='unresolved',diagnostic='Search or exact checking failed; this is not an exclusion.',error=traceback.format_exc())
            finally:signal.alarm(0)
            record['seconds']=round(time.monotonic()-st,6)
            out.write(json.dumps(record,separators=(',',':'))+'\n');out.flush()
            print({k:v for k,v in record.items() if k not in ('certificate','error')},flush=True)
if __name__=='__main__':main()
