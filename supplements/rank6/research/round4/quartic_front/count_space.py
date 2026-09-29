import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
import sympy as s
from fractions import Fraction
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];mod=forced_module_data(R);ep=(0,0,-1,1,1) if rid.endswith('_91') else (0,0,1,1,1)
A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);vectors=list(dict.fromkeys(v for v,ti in labels));sp=Spectrum(tab,cols,[(v,None) for v in vectors]);vectors=[v for v in vectors if v not in map(tuple,sp.forbidden)];L=s.Matrix.hstack(*map(s.Matrix,cols));G=(data['ch'].C-L*L.T).extract(range(1,6),range(1,6));aa=[];bb=[]
for i in range(5):
 for j in range(i,5):aa.append([v[i]*v[j] for v in vectors]);bb.append(G[i,j])
rr,rb=sp.balance([(v,None) for v in vectors],len(vectors));aa+=rr;bb+=rb
M=s.Matrix([row+[val] for row,val in zip(aa,bb)]);rref,piv=M.rref();print(rid,'vectors',len(vectors),'rank',len(piv),'free',len(vectors)-len(piv),'G',list(G),flush=True)
print('vectors',vectors,flush=True);free=[i for i in range(len(vectors)) if i not in piv];print('free',[(i,vectors[i]) for i in free],flush=True)
for i,j in enumerate(piv):print('piv',j,vectors[j],str(rref[i,-1]-sum(rref[i,k]*s.Symbol('m'+str(k)) for k in free)),flush=True)
Path(__file__).with_name(rid+'_count_space.json').write_text(json.dumps(dict(id=rid,vectors=vectors,A=aa,b=list(map(int,bb)),rank=len(piv),free=free),indent=2)+'\n')
