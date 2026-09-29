import json,sys,time,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import cyclotomic_stabilizer_trace as C
from higher_traces import indicator_choices,farkas,check_farkas
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_4_91');data=C.data_for(R,3);K=data['C'];dims=data['dims'];D=data['DD'];out=[]
for ix,cols in enumerate(data['lows']):
 why=C.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
 if why:out.append(dict(frame=ix,ordinary=why));continue
 for ep in indicator_choices(R):
  A,b,meta,labels=C.system(R,data,cols,ep,[5],return_state=True);nv=len(A[0])
  for target in [-2,1]:
   B=[r[:] for r in A];bb=b[:]
   for obj,value in [(1,1),(2,1),(5,target)]:
    rhs=K(value)*D-sum((K(v[obj])*sum((K(v[j])*dims[j] for j in range(6)),K.zero) for v in cols),K.zero)
    coeff=[K(v[obj-1])*sum((K(v[j])*dims[j+1] for j in range(5)),K.zero)*data['phases'][ti][2] for v,ti in labels]+[K.zero]*(nv-len(labels))
    for row,rr in C.rational_rows(coeff,rhs,K):B.append(row);bb.append(rr)
   ray=farkas(B,bb)
   if ray is not None:check_farkas(B,bb,ray)
   print(ix,ep,target,ray is not None,flush=True)
   out.append(dict(frame=ix,ep=list(ep),third=target,excluded=ray is not None,ray=ray,rows=len(B),variables=len(B[0])))
Path(__file__).with_name('R6_4_91_probe.json').write_text(json.dumps(out)+'\n')
