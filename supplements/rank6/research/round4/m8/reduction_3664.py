import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import galois_pseudo_reduction as G
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_8_3664')
st=time.monotonic()
def stop(*a):raise TimeoutError('explicit 800 second reduction budget')
signal.signal(signal.SIGALRM,stop);signal.alarm(800)
try:
 c=G.certificate(R,timeout=120);o={'outcome':'proved_reduction' if c else 'no_reduction','certificate':c}
 if c:o['verification']=G.verify(R,c)
except TimeoutError as e:o={'outcome':'budget_incomplete','reason':str(e)}
o['seconds']=time.monotonic()-st
(P/'research/round4/m8/3664_reduction.json').write_text(json.dumps(o,separators=(',',':'))+'\n');print({k:v for k,v in o.items() if k!='certificate'},flush=True)
