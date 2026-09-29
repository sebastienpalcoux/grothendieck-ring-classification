import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));import galois_pseudo_reduction as G
R=next(r['N']for r in json.load(open(P/'data/census.json'))if r['id']=='R6_6_1035');st=time.monotonic()
def stop(*a):raise TimeoutError('840-second reduction budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(840);c=G.certificate(R,timeout=120);signal.alarm(0)
if c is None:raise RuntimeError('general reduction not completed')
p=Path(__file__).with_name('R6_6_1035_reduction.json');p.write_text(json.dumps(c,separators=(',',':'))+'\n');print('seconds',time.monotonic()-st,'values',len(c['all_values']),'orbits',len(c['branches']),flush=True)
