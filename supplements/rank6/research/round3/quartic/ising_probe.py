from galois_probe import *
import fourth_modular_probe as fm
from modular_cyclotomic_trace import rational_rows
from scipy.optimize import linprog
import numpy as np
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']=='R6_4_91');m.R=R
started=time.monotonic();data=data_for(R,4);print('data',time.monotonic()-started,flush=True);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,-1,1,1);mod=forced_module_data(R);C=data['C'];fm.current_cols=cols
for lab in tab.assignments(cols):
 A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b=fm.fourth(data,R,ep,A,b,labels)
 low=sum((C(sum(c[3]*c[j] for c in cols))*data['dims'][j] for j in range(6)),C.zero)
 coeff=[C(v[2])*sum((C(v[i])*data['dims'][i+1] for i in range(5)),C.zero)*data['phases'][ti][3] for v,ti in labels]+[C.zero]*(len(A[0])-len(labels))
 for row,rhs in rational_rows(coeff,-low,C):A.append(row);b.append(rhs)
 A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels)
 print('startlp',lab,len(A),len(A[0]),flush=True)
 aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs')
 print('lp',lab,sol.status,sol.message,flush=True)
 if sol.status==2:
  y=farkas(A,b)
  if y is not None:check_farkas(A,b,y)
  Path(__file__).with_suffix('.json').write_text(json.dumps(dict(lab=lab,ray=y),indent=2))
