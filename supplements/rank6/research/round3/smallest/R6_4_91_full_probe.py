import json,sys,time,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round3_m4 as C
from higher_traces import indicator_choices,farkas,check_farkas
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_4_91');data=C.data_for(R,3,16);K=data['C'];dims=data['dims'];D=data['DD'];tab=data['tab'];out=[]
for ix,cols in enumerate(data['lows']):
 for lab in tab.assignments(cols):
  for ep in indicator_choices(R):
   A,b,meta=C.system(R,data,cols,ep,lab)
   if A is None:out.append(dict(frame=ix,lab=lab,ep=ep,excluded=True,spectrum=meta));continue
   G,vectors=C.high_vectors(data,cols);sp=C.Spectrum(tab,cols,[(v,None) for v in vectors]);bad=set(map(tuple,sp.forbidden));vectors=[v for v in vectors if v not in bad];labels=[(v,ti) for v in vectors for ti in range(len(data['phases']))];nv=len(A[0])
   for target in [-2,1]:
    B=[r[:] for r in A];bb=b[:]
    for obj,value in [(1,1),(2,1),(5,target)]:
     rhs=K(value)*D-sum((K(v[obj])*sum((K(v[j])*dims[j] for j in range(6)),K.zero) for v in cols),K.zero)
     coeff=[K(v[obj-1])*sum((K(v[j])*dims[j+1] for j in range(5)),K.zero)*data['phases'][ti][2] for v,ti in labels]+[K.zero]*(nv-len(labels))
     for row,rr in C.rational_rows(coeff,rhs,K):B.append(row);bb.append(rr)
    ray=farkas(B,bb)
    if ray is not None:check_farkas(B,bb,ray)
    print(ix,lab,ep,target,ray is not None,flush=True)
    out.append(dict(frame=ix,lab=lab,ep=list(ep),third=target,excluded=ray is not None,ray=ray,rows=len(B),variables=len(B[0])))
    Path(__file__).with_suffix('.json').write_text(json.dumps(out)+'\n')
