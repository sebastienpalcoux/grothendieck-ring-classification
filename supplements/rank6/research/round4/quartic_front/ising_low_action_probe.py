import sys,json,time,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from galois_probe import *
import sympy as s
from fractions import Fraction
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_array
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];C=data['C'];lab=tab.assignments(cols)[0];wi=json.load(open(ROOT/f'research/round3/quartic/{rid}_witness_{lab[-1]}.json'));counts=Counter()
for j,val in zip(wi['keep'],map(Fraction,wi['variables'])):
 if j<len(wi['labels']) and val:counts[(0,)+tuple(wi['labels'][j][0])]+=int(val)
B=list(map(tuple,cols))+[v for v,ct in counts.items() for _ in range(ct)];r=len(B);sp=Spectrum(tab,cols,[(v[1:],None) for v in counts]);tt=dict(zip(sp.vectors,sp.types));conj=lambda x:evaluate(x.to_list(),C.unit**(data['F']-1),C)
lowstar=[lab.index(tab.rows.index(tuple(conj(x) for x in tab.rows[lab[a]]))) for a in range(6)];triples=list(itertools.combinations_with_replacement(range(1,6),3));nt={abc:Fraction(wi['variables'][wi['keep'].index(wi['base']+k)]) for k,abc in enumerate(triples)}
S=[[sum(x*y for x,y in zip(v,w))-int(i==j) for j,w in enumerate(B)] for i,v in enumerate(B)];variables={};fixed={};lb=[];ub=[]
def can(a,y,z):
 if lowstar[a]<a:return can(lowstar[a],z,y)
 if lowstar[a]==a and z<y:return (a,z,y)
 return (a,y,z)
def lowval(a,y,z):
 if not y:return int(a==z)
 if not z:return int(a==lowstar[y])
 return int(nt[tuple(sorted((a,y,lowstar[z])))])
for a in range(1,6):
 for y in range(r):
  for z in range(r):
   key=can(a,y,z)
   if key in variables or key in fixed:continue
   if y<6 and z<6:fixed[key]=lowval(a,y,z)
   elif not S[y][z]:fixed[key]=0
   else:variables[key]=len(variables);lb.append(0);ub.append(S[y][z])
rows=[];rhs=[]
def add(terms,target):
 row={}
 for a,y,z,k in terms:
  key=can(a,y,z)
  if key in fixed:target-=k*fixed[key]
  else:j=variables[key];row[j]=row.get(j,0)+k
 row={j:k for j,k in row.items() if k}
 if row or target:rows.append(row);rhs.append(target)
for y in range(r):
 for z in range(y,r):add([(a,y,z,1) for a in range(1,6)],S[y][z])
for a in range(1,6):
 for y in range(r):
  for i in range(6):
   target=sum(cols[a][j]*B[y][k]*R[j][k][i] for j in range(6) for k in range(6))
   add([(a,y,z,B[z][i]) for z in range(r) if B[z][i]],target)
 trace=sum((tt[v][lab[a]] for v in B),C.zero);require(len(trace.to_list())<=1 and (not trace or trace.to_list()[0].denominator==1),'trace is not integral');add([(a,y,y,1) for y in range(r)],int(trace.to_list()[0] if trace else 0))
# In this fixed profile, the unique pure Ising object gives disjoint A3 actions.
sigma=3;g=4
sigmap=lambda v:tuple(sum(v[j]*R[sigma][j][k] for j in range(6)) for k in range(6))
gmap=lambda v:tuple(sum(v[j]*R[g][j][k] for j in range(6)) for k in range(6))
Cdata=data['C'];zz=__import__('cmath').exp(2j*__import__('math').pi/data['F'])
approx=lambda v:sum(float(co)*zz**i for i,co in enumerate(reversed(sum((Cdata(v[j])*data['dims'][j] for j in range(6)),Cdata.zero).to_list()))).real
remaining=set(range(r));sigma_action=np.zeros((r,r),dtype='int64');orbits=[]
while remaining:
 i=min(remaining,key=lambda j:(approx(B[j]),j));v=B[i];remaining.remove(i)
 choices=[j for j in remaining if B[j]==gmap(v)];require(choices,'missing g partner');j=min(choices);remaining.remove(j)
 choices=[k for k in remaining if B[k]==sigmap(v)];require(choices,'missing sigma partner');k=min(choices);remaining.remove(k)
 for x,y in [(i,k),(j,k),(k,i),(k,j)]:sigma_action[x,y]=1
 orbits.append((i,j,k))
g_action=sigma_action@sigma_action-np.eye(r,dtype='int64');sigma_index=B.index(tuple(int(j==sigma) for j in range(6)));g_index=B.index(tuple(int(j==g) for j in range(6)))
for a in range(1,6):
 for z in range(r):
  add([(a,sigma_index,z,1)],int(sigma_action[a,z]));add([(a,g_index,z,1)],int(g_action[a,z]))
 for y in range(r):
  for z in range(r):
   terms=[(a,y,k,int(sigma_action[k,z])) for k in range(r) if sigma_action[k,z]]+[(a,k,z,-int(sigma_action[y,k])) for k in range(r) if sigma_action[y,k]]
   add(terms,0)
print('system',rid,'rank',r,'variables',len(variables),'equations',len(rows),flush=True)
rr=[];cc=[];vv=[]
for i,row in enumerate(rows):
 for j,v in row.items():rr.append(i);cc.append(j);vv.append(float(v))
A=coo_array((vv,(np.array(rr,dtype=np.int32),np.array(cc,dtype=np.int32))),shape=(len(rows),len(variables))).tocsc();sol=milp(np.zeros(len(variables)),integrality=np.ones(len(variables)),bounds=Bounds(lb,ub),constraints=LinearConstraint(A,rhs,rhs),options={'time_limit':600});print('milp',sol.status,sol.message,flush=True);rec=dict(id=rid,rank=r,lab=lab,variables=len(variables),rows=len(rows),status=int(sol.status))
if sol.status==0:
 vals=[round(x) for x in sol.x];require(all(sum(k*vals[j] for j,k in row.items())==b for row,b in zip(rows,rhs)),'rounded witness failed');rec['exact']=True;rec['N']=[[[int(y==z) for z in range(r)] for y in range(r)]]+[[[fixed[can(a,y,z)] if can(a,y,z) in fixed else vals[variables[can(a,y,z)]] for z in range(r)] for y in range(r)] for a in range(1,6)];rec['columns']=B
 mats=[np.array(M,dtype='int64') for M in rec['N']];rec['commute']=all(np.array_equal(x@y,y@x) for x in mats for y in mats);print('exact',True,'commute',rec['commute'],flush=True)
Path(__file__).with_name(rid+'_ising_low_action_probe.json').write_text(json.dumps(rec,indent=2)+'\n')
