import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import galois_pseudo_reduction as G
C={x['id']:x['N'] for x in json.load(open(P/'data/census.json'))}
def stop(*a):raise TimeoutError('explicit 800 second reduction budget')
signal.signal(signal.SIGALRM,stop)
for rid in ('R6_8_311','R6_8_1660'):
 st=time.monotonic();signal.alarm(800)
 try:
  c=G.certificate(C[rid],timeout=120);o={'outcome':'proved_reduction' if c else 'no_reduction','certificate':c}
  if c:o['verification']=G.verify(C[rid],c)
 except TimeoutError as e:o={'outcome':'budget_incomplete','reason':str(e)}
 finally:signal.alarm(0)
 o['id']=rid;o['seconds']=time.monotonic()-st
 (P/f'research/round4/m8/{rid}_reduction.json').write_text(json.dumps(o,separators=(',',':'))+'\n');print({k:v for k,v in o.items() if k!='certificate'},flush=True)
