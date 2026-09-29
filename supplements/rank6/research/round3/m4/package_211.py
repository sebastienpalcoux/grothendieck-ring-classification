import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import galois_pseudo_reduction as G
R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_211');st=time.monotonic()
c=G.certificate(R,timeout=120)
if c is None:raise RuntimeError('unrestricted reduction did not complete')
meta=G.verify(R,c);p=Path(__file__).with_name('R6_4_211_general.json')
pseudo=json.load(open(Path(__file__).with_name('R6_4_211_ambient_h3.json')))
z={'kind':'general_ambient_full_character_rotation','version':1,'scope':'general','reduction':c,'pseudo':pseudo}
p.write_text(json.dumps({'id':'R6_4_211','certificate':z,'reduction_verification':meta,'seconds':time.monotonic()-st},separators=(',',':'))+'\n');print(meta,time.monotonic()-st,flush=True)
