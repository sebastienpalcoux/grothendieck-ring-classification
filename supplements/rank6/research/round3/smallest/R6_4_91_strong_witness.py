import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from verlinde_probe import *
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_4_91');m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,-1,1,1);mod=forced_module_data(R);C=data['C'];D=data['DD'];dims=data['dims'];out=[]
for lab in tab.assignments(cols):
 A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
 nv=len(A[0]);allowed={j for j,t in enumerate(data['phases']) if t in {tuple(C.unit**(a*k%16) for k in range(1,4)) for a in range(1,16,2)}}
 for obj,value in [(1,1),(2,1),(5,1)]:
  rhs=C(value)*D-sum((C(v[obj])*sum((C(v[j])*dims[j] for j in range(6)),C.zero) for v in cols),C.zero)
  coeff=[C(v[obj-1])*sum((C(v[j])*dims[j+1] for j in range(5)),C.zero)*data['phases'][ti][2] for v,ti in labels]+[C.zero]*(nv-len(labels))
  for row,rr in rational_rows(coeff,rhs,C):A.append(row);b.append(rr)
 keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][2] or labels[j][1] in allowed];A=[[row[j] for j in keep] for row in A]
 print('start',lab,len(A),len(A[0]),flush=True)
 from fractions import Fraction
 witness_path=ROOT/'research/round3/quartic'/('R6_4_91_witness_'+str(lab[-1])+'.json')
 witness=json.load(open(witness_path));require(witness['keep']==keep and witness['lab']==list(lab),'changed witness variable domain')
 values=[Fraction(x) for x in witness['variables']]
 require(len(values)==len(A[0]) and all(x>=0 for x in values),'bad positive witness')
 require(all(sum(x*y for x,y in zip(row,values))==rhs for row,rhs in zip(A,b)),'strong scalar-indicator witness equation failed')
 require(all(values[k].denominator==1 for k,j in enumerate(keep) if j<len(labels) or j>=base),'nonintegral high/triple multiplicity')
 print('exact stronger witness verified',lab,flush=True);out.append(dict(lab=lab,necessary_relaxation_survives=True,rows=len(A),columns=len(A[0]),source=str(witness_path.relative_to(ROOT)),third_indicators={'1':1,'2':1,'5':1},high_count=str(sum(values[k] for k,j in enumerate(keep) if j<len(labels)))))
 Path(__file__).with_suffix('.json').write_text(json.dumps(out)+'\n')
