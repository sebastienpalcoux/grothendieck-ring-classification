"""Wall-clock bounded exploratory scan; timeouts are never exclusions."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    multiplicity = int(sys.argv[1])
    seconds = int(sys.argv[2]) if len(sys.argv)>2 else 12
    selected = set(map(int,sys.argv[3:])) if len(sys.argv)>3 else None
    rows = json.loads((ROOT/'data/decisions.json').read_text())
    if multiplicity == 2 and selected is None:
        prelim = json.loads((HERE/'screen_m2.json').read_text())
        selected = {int(x['id'].split('_')[-1]) for x in prelim
                    if x['status']=='complete_spherical_obstruction'}
    targets = [d for d in rows if d['multiplicity']==multiplicity and
               d['commutative'] and d['status']=='unresolved' and
               (selected is None or d['index'] in selected)]
    print('targets',len(targets),'wall budget',seconds,'workers',4,flush=True)
    def run(d):
        begin=time.monotonic()
        try:
            requested = str(d['index']) if multiplicity == 1 else f'2_{d["index"]}'
            p=subprocess.run([sys.executable,str(HERE/'try_rank8.py'),requested,
                str(min(10,seconds))],capture_output=True,text=True,timeout=seconds)
            status=('checked_exclusion' if 'exact_verification_complete' in p.stdout
                    and p.returncode==0 else 'incomplete' if p.returncode==0 else 'error')
            out=p.stdout[-1200:];err=p.stderr[-1200:]
        except subprocess.TimeoutExpired as exc:
            status='timeout';out=(exc.stdout or b'').decode(errors='replace')[-500:];err=''
        return {'id':d['id'],'status':status,'seconds':round(time.monotonic()-begin,2),
                'stdout':out,'stderr':err}
    results=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for f in as_completed([pool.submit(run,d) for d in targets]):
            r=f.result();results.append(r)
            print(r['id'],r['status'],r['seconds'],r['stdout'][-200:],r['stderr'][-150:],flush=True)
    report={'rank':8,'multiplicity':multiplicity,'seconds_per_ring':seconds,
            'results':sorted(results,key=lambda r:int(r['id'].split('_')[-1]))}
    (HERE/('scan_m1.json' if multiplicity==1 else 'scan_m2_full.json')).write_text(json.dumps(report,indent=2)+'\n')
    print('complete',len(results),flush=True)


if __name__=='__main__':main()
