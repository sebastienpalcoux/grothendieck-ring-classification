import sys,json,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from spectral_induction import reciprocity_data
from modular_character_induction import certificate,verify
R=next(r['N'] for r in json.load(open(P/'data/unresolved_tensors.json')) if r['id']=='R6_8_6525')
t=time.monotonic();d,tab=reciprocity_data(R)
print('DATA',time.monotonic()-t,'q',d['q'],'columncounts',[len(c) for c in d['columns']],'lows',len(d['lows']),'fielddegree',tab.K.mod.degree(),flush=True)
(P/'research/round3/arithmetic/R6_8_6525_lows.json').write_text(json.dumps({'lows':d['lows'],'column_counts':[len(c) for c in d['columns']]},indent=2))
c=certificate(R,6,progress=lambda *x:print('PROGRESS',time.monotonic()-t,x,flush=True))
print('CERTIFICATE',bool(c),'seconds',time.monotonic()-t,flush=True)
if c:
 (P/'research/round3/arithmetic/R6_8_6525_pseudo.json').write_text(json.dumps(c,indent=2))
 verify(R,c);print('VERIFIED',flush=True)
