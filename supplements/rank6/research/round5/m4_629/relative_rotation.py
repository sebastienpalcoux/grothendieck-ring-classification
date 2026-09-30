import sys,json,itertools,time,math
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
from exact import vector
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];D=d['DD'];f=json.load(open(here/'rank35_fusion_data.json'));N=f['fusion_tensor'];br=next(x for x in json.load(open(here/'rank35_modular_completions.json'))['branches'] if x['signs']==f['signs']);S=[[C([s.Rational(z) for z in v]) for v in row] for row in br['S']];rank=35;dims=[z/S[0][0] for z in S[0]]
case=next(x for x in json.load(open(here/'decoded_twists.json')) if x['rank']==35 and x['solution']==0);ts=[0]*6;vs=list(cols)
for o in case['orbits']:ts.extend([15//o['root_order']*o['root_power']%15]*o['copies']);vs.extend([(0,)+tuple(o['column'])]*o['copies'])
def spectrum(z,h,p):
 Z=C.unit**(15//p);B=s.Matrix.hstack(*(vector(Z**i,8) for i in range(p-1)));piv=(B.T).rref()[1];L=B.extract(piv,range(p-1)).inv();v=vector(z,8);c=L*v.extract(piv,[0]);require(B*c==v,'trace outside prime field');base=(s.Integer(h)-sum(c))/p;mult=[base+x for x in c]+[base];return list(map(str,mult)),all(x.is_Integer and x>=0 for x in mult)
out=[]
for p in (3,5):
 original=[sum((C(vs[j][i])*dims[j]*C.unit**(p*ts[j]) for j in range(rank)),C.zero)/D for i in range(6)];fail=[]
 for a in range(rank):
  center=sum((C(N[j][k][a])*dims[j]*dims[k]*C.unit**(p*(ts[j]-ts[k])) for j in range(rank) for k in range(rank)),C.zero)/D**2
  hc=[1]+[0]*(rank-1);hf=[1]+[0]*5
  for _ in range(p):hc=[sum(hc[j]*N[j][a][k] for j in range(rank)) for k in range(rank)];hf=[sum(hf[i]*vs[a][j]*R[i][j][k] for i in range(6) for j in range(6)) for k in range(6)]
  tr=sum((C(vs[a][i])*original[i] for i in range(6)),C.zero)-center;mu,ok=spectrum(tr,hf[0]-hc[0],p)
  if not ok:fail.append({'object':a,'multiplicities':mu,'dimension':hf[0]-hc[0],'trace':list(map(str,tr.to_list()))})
 rec={'power':p,'failures':fail};out.append(rec);print(rec,flush=True)
(here/'relative_rotation.json').write_text(json.dumps(out,indent=2))
