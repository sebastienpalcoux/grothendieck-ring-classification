import sys,json,itertools,time,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round2_literature/quartic')]
import modular_cyclotomic_trace as m
from cyclotomic_stabilizer_trace import data_for,forced_module_data,system
from modular_cyclotomic_trace import table_for,stronger_system
from spectral_induction import Spectrum
from exact import evaluate,require
from higher_traces import farkas,check_farkas
from collections import Counter

def coupled(data,tab,cols,A,b,labels):
 C=data['C'];high=[(v,None) for v in dict.fromkeys(v for v,ti in labels)];sp=Spectrum(tab,cols,high)
 forbidden=set(map(tuple,sp.forbidden));keep=[j for j in range(len(labels)) if labels[j][0] not in forbidden]
 labs=[labels[j] for j in keep];types=data['phases'];idx=dict(zip(sp.vectors,sp.types));one=types.index(tuple(C.one for _ in types[0]));zero=types.index(tuple(C.zero for _ in types[0]));low=Counter((idx[tuple(c)],one) for c in cols)
 allpairs=set((idx[(0,)+tuple(v)],ti) for v,ti in labs)|set(low)
 nv=len(A[0]);seen=set();count=0
 from collections import defaultdict
 positions=defaultdict(list)
 for j,(v,ti) in enumerate(labs):positions[idx[(0,)+tuple(v)],ti].append(j)
 for a in range(data['F']):
  if math.gcd(a,data['F'])>1:continue
  z=C.unit**a;zz=C.unit**(a*a%data['F']);pmap={j:types.index(tuple(evaluate(x.to_list(),zz,C) for x in ty)) for j,ty in enumerate(types)}
  for t,ti in sorted(allpairs,key=str):
   tt=tuple(evaluate(x.to_list(),z,C) for x in t);tj=pmap[ti]
   if (t,ti)==(tt,tj):continue
   pair=tuple(sorted(((str(t),ti),(str(tt),tj))))
   if pair in seen:continue
   seen.add(pair)
   row=[0]*nv
   for j in positions[t,ti]:row[j]+=1
   for j in positions[tt,tj]:row[j]-=1
   rhs=low[tt,tj]-low[t,ti]
   if any(row) or rhs:A.append(row);b.append(rhs);count+=1
 return A,b,count

if __name__=='__main__':
 rings={r['id']:r['N'] for r in json.load(open(ROOT/'data/census.json'))};out=[]
 for rid in sys.argv[1:] or ['R6_4_22','R6_4_91']:
  R=rings[rid];m.R=R;data=data_for(R,3);tab=table_for(R,data);mod=forced_module_data(R);cols=data['lows'][1];ep=(0,0,1,1,1) if rid.endswith('_22') else (0,0,-1,1,1)
  for lab in tab.assignments(cols):
   A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True)
   A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels)
   print(rid,lab,len(A),len(A[0]),'coupled',n,flush=True);y=farkas(A,b)
   if y is not None:check_farkas(A,b,y)
   rec=dict(id=rid,lab=lab,ep=ep,rows=len(A),variables=len(A[0]),excluded=y is not None,ray=y);out.append(rec)
   print({k:v for k,v in rec.items() if k!='ray'},flush=True)
   (Path(__file__).with_suffix('.json')).write_text(json.dumps(out,indent=2)+'\n')
