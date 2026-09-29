import sys,json,time,signal
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import galois_pseudo_reduction as G
R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']=='R6_4_155')
st=time.monotonic();c=G.certificate(R,timeout=120);out={'id':'R6_4_155','certificate':c,'seconds':time.monotonic()-st}
if c is not None:out['replay']=G.verify(R,c)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print(out['seconds'],out.get('replay'))
