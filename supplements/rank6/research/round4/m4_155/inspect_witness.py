import sys,json
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as M
from fractions import Fraction
rid='R6_4_155';R=next(r['N'] for r in json.load(open(P/'data/census.json')) if r['id']==rid)
a=Path(sys.argv[1]);c=json.load(open(a));F=24 if 'F24' in a.name else 8;d=M.data_for(R,c['height'],F);cs=d['lows'][c['low']];lab=c['labelling'];ep=c['indicators'];A,b,meta=M.system(R,d,cs,ep,lab);G,vs,sp=d['_branch_cache'][tuple(map(tuple,cs))];bad=set(map(tuple,sp.forbidden));labs=[(v,ti) for v in vs if v not in bad for ti in range(len(d['phases']))]
for row in cs:print('low',row)
C=d['C'];terms={}
for j,(v,t) in enumerate(labs):
 k=int(Fraction(c['values'][j]));
 if not k:continue
 terms[v]=terms.get(v,0)+k
 ts=d['phases'][t];root=next((a for a in range(F) if tuple(C.unit**(a*r) for r in range(1,c['height']+1))==ts),None)
 print(k,'high',v,'theta',f'zeta_{F}^{root}' if root is not None else str(ts))
print('collapsed',terms)
