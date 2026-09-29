from galois_probe import *
from modular_cyclotomic_trace import rational_rows
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
import numpy as np

def verlinde(R,data,tab,cols,lab,A,b,labels,restriction=True):
 C=data['C'];n=len(R);sp=Spectrum(tab,cols,[(v,None) for v in dict.fromkeys(v for v,ti in labels)]);forbidden=set(map(tuple,sp.forbidden));labels=[(v,ti) for v,ti in labels if v not in forbidden];nv=len(A[0]);nh=len(labels);tuples=dict(zip(sp.vectors,sp.types));triple={};base=nv
 lowstar=[]
 for a in range(n):
  row=tab.rows[lab[a]];crow=tuple(evaluate(x.to_list(),C.unit**(data['F']-1),C) for x in row)
  lowstar.append(lab.index(tab.rows.index(crow)))
 for a,bb,c in itertools.combinations_with_replacement(range(1,n),3):
  ha,hb,hc=[lab[x] for x in (a,bb,c)]
  weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)}
  rhs=-sum((weights[v] for v in sp.low),C.zero)
  co=[weights[(0,)+tuple(v)] for v,ti in labels]+[C.zero]*(nv-nh)+[-C.one]
  for row in A:row.append(0)
  triple[(a,bb,c)]=nv;nv+=1
  for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
 if restriction:
  allowed=[v for v in sp.high if list(v[1:]) not in sp.forbidden]
  for a,bb in itertools.combinations_with_replacement(range(1,n),2):
   ca,cb=cols[a],cols[bb];fp=[sum(ca[i]*cb[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
   qvars={}
   for v in allowed:
    bound=min(fp[k]//v[k] for k in range(n) if v[k])
    if bound:qvars[v]=(nv,bound);nv+=1
   for row in A:row.extend([0]*(nv-len(row)))
   for k in range(n):
    row=[0]*nv
    for c in range(1,n):row[triple[tuple(sorted((a,bb,lowstar[c])))]]+=cols[c][k]
    for v,(j,B) in qvars.items():row[j]=v[k]
    A.append(row);b.append(fp[k]-int(a==lowstar[bb] and k==0))
   for v,(j,B) in qvars.items():
    row=[0]*(nv+1);row[j]=1;row[nv]=1
    for k,(w,ti) in enumerate(labels):
     if tuple(w)==v[1:]:row[k]-=B
    for rr in A:rr.append(0)
    A.append(row);b.append(0);nv+=1
 return A,b,labels,base

if __name__=='__main__':
 rings={r['id']:r['N'] for r in json.load(open(ROOT/'data/census.json'))};out=[]
 for rid in sys.argv[1:] or ['R6_4_22','R6_4_91']:
  R=rings[rid];m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,1,1,1) if rid.endswith('_22') else (0,0,-1,1,1);mod=forced_module_data(R)
  for lab in tab.assignments(cols):
   A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
   keep=list(range(len(A[0])))
   if rid.endswith('_91'):
    C=data['C'];allowed={j for j,t in enumerate(data['phases']) if t in {tuple(C.unit**(a*k%16) for k in range(1,4)) for a in range(1,16,2)}};keep=[j for j in range(len(A[0])) if j>=len(labels) or not labels[j][0][2] or labels[j][1] in allowed];A=[[row[j] for j in keep] for row in A]
   print('startlp',rid,lab,len(A),len(A[0]),flush=True)
   aa=np.array(A,dtype=float);bb=np.array(b,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(A[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':120},method='highs');print('lp',sol.status,sol.message,flush=True)
   y=None
   if sol.status==2:
    y=farkas(A,b)
    if y is not None:check_farkas(A,b,y)
   elif sol.status==0:
    integ=np.array([int(j<len(labels) or j>=base) for j in keep]);mi=milp(np.zeros(len(A[0])),integrality=integ,bounds=Bounds(0,np.inf),constraints=LinearConstraint(aa/scale[:,None],bb/scale,bb/scale),options={'time_limit':120});print('milp',mi.status,mi.message,flush=True)
    if mi.status==0:
     vals=[str(__import__('fractions').Fraction(float(x)).limit_denominator(1000000)) for x in mi.x]
     exact=[__import__('fractions').Fraction(x) for x in vals]
     ok=all(sum(x*y for x,y in zip(row,exact))==rhs for row,rhs in zip(A,b))
     witness={'id':rid,'lab':lab,'variables':vals,'keep':keep,'labels':labels,'exact':ok,'base':base}
     wp=Path(__file__).with_name(rid+'_witness_'+str(lab[-1])+'.json');wp.write_text(json.dumps(witness,indent=2))
     print('exactwitness',ok,'high_count',sum(exact[k] for k,j in enumerate(keep) if j<len(labels)),flush=True)
   out.append(dict(id=rid,lab=lab,status=sol.status,ray=y));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
