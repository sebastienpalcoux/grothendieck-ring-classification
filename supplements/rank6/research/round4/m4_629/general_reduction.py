import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import galois_pseudo_reduction as g
R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');st=time.monotonic()
try:
 c=g.certificate(R,timeout=120);rec={'id':'R6_4_629','outcome':'general_galois_pseudo_reduction' if c else 'no_reduction_certificate','certificate':c}
 if c:rec['replay']=g.verify(R,c)
except Exception as e:rec={'id':'R6_4_629','outcome':'incomplete','reason':repr(e)}
rec['seconds']=time.monotonic()-st;Path(__file__).with_suffix('.json').write_text(json.dumps(rec));print({k:v for k,v in rec.items() if k!='certificate'})
