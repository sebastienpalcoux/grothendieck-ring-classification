from galois_probe import *
from scipy.optimize import linprog
import numpy as np
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_4_91');m.R=R
started=time.monotonic();data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,-1,1,1);mod=forced_module_data(R);C=data['C'];out=[]
allowed={j for j,t in enumerate(data['phases']) if t in {tuple(C.unit**(a*k%16) for k in range(1,4)) for a in range(1,16,2)}}
print('allowed',allowed,flush=True)
for lab in tab.assignments(cols):
 A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True)
 A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels)
 sp=Spectrum(tab,cols,[(v,None) for v in dict.fromkeys(v for v,ti in labels)]);forbidden=set(map(tuple,sp.forbidden));labels=[(v,ti) for v,ti in labels if v not in forbidden]
 keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][2] or labels[j][1] in allowed]
 A=[[row[j] for j in keep] for row in A]
 print('startlp',lab,len(A),len(A[0]),flush=True)
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs')
 print('lp',lab,sol.status,sol.message,flush=True)
 y=None
 if sol.status==2:
  y=farkas(A,b)
  if y is not None:check_farkas(A,b,y)
 out.append(dict(lab=lab,status=sol.status,ray=y));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
