import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from round5_629 import fixed_profile_certificate
here=Path(__file__).parent;rank=int(sys.argv[1]);height=int(sys.argv[2]) if len(sys.argv)>2 else 10;st=time.monotonic()
c=fixed_profile_certificate(height,rank,progress=lambda *x:print(x,flush=True))
(here/f'exact_rank{rank}_h{height}.json').write_text(json.dumps(c));print('completed',rank,'solutions',len(c['solutions']),'seconds',time.monotonic()-st,'stats',{k:v for k,v in c['enumeration'].items() if k!='permutation'},flush=True)
