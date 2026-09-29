import sys,json,time,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
from higher_traces import trace_types,farkas,check_farkas
from fractions import Fraction as Q
R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']=='R6_4_6');data,tab=H.I.reciprocity_data(R);height=6
out=[]
for ix,cols in enumerate(data['lows']):
 why=H.I.low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
 if why:out.append(dict(frame=ix,ordinary=why));continue
 for ep in H.I.indicator_choices(R):
  if ep[4]!=1:continue
  A,b,meta=H.trace_system(R,data,tab,cols,ep,height,None,None,[3,4]);L=H.I.s.Matrix.hstack(*map(H.I.s.Matrix,cols));_,_,rot=H.I.system_rotation(R,data,L,ep,height);labels=rot['labels'];ts,_=trace_types(data['q'],data['primes'],height)
  keep=[j for j in range(len(A[0])) if j>=len(labels) or not(labels[j][0][0] or labels[j][0][1]) or ts[labels[j][1]][3]==(Q(-1),Q(0))]
  A=[[row[j] for j in keep] for row in A];ray=farkas(A,b);print(ix,ep,len(keep),'excluded',ray is not None,flush=True)
  if ray is not None:check_farkas(A,b,ray)
  out.append(dict(frame=ix,ep=list(ep),excluded=ray is not None,ray=ray,rows=len(A),cols=len(keep)))
Path(__file__).with_name('probe_twist.json').write_text(json.dumps(out))
