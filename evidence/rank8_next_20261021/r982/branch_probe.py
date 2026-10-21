"""Exact finite-domain split certificates, using floating LP only as proposal."""
from pathlib import Path
import json,math,sys,time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix,hstack,eye
from domain_probe import rows_for,propagate
HERE=Path(__file__).resolve().parent

def phase(rows,domains):
 b=[row[-1]for row in rows];n=len(domains);m=len(b)
 lo=[min(d)for d in domains];hi=[max(d)for d in domains]
 scales=[max(1,abs(row[-1]),max(map(abs,row[:-1])))for row in rows]
 A=csc_matrix(np.array([[a/scales[i]for a in row[:-1]]for i,row in enumerate(rows)]))
 B=np.array([x/s for x,s in zip(b,scales)])
 E=hstack((A,eye(m,format='csc'),-eye(m,format='csc')),format='csc')
 r=linprog(np.r_[np.zeros(n),np.ones(2*m)],A_eq=E,b_eq=B,bounds=list(zip(lo,hi))+[(0,None)]*(2*m),method='highs')
 if not r.success:return {'status':'unresolved_numerical','message':str(r.message)}
 if r.fun>1e-9:
  raw=[v/s for v,s in zip(r.eqlin.marginals,scales)];norm=max(map(abs,raw))
  for power in range(3,19):
   y=[int(round(v/norm*10**power))for v in raw];g=math.gcd(*y);y=[v//g for v in y]
   c=[sum(y[i]*rows[i][j]for i in range(m))for j in range(n)]
   target=sum(y[i]*b[i]for i in range(m));upper=sum(max(c[j]*lo[j],c[j]*hi[j])for j in range(n))
   if target>upper:return {'status':'exact_bounded_linear_obstruction','covector':y,'rhs_value':target,'box_upper':upper,'floating_objective':float(r.fun)}
  return {'status':'unresolved_numerical','floating_objective':float(r.fun)}
 return {'status':'fractional_proposal','values':list(map(float,r.x[:n]))}

def run(name,limit):
 start=time.monotonic();d,allrows,rank=rows_for(name)
 # The first source rows plus rationally equivalent derived rows propagate;
 # rref rows alone suffice for LP proposal and exact dual leaves.
 m=len(d['rhs']);rr=allrows[m:m+rank]
 rootdomains=json.loads((HERE/(name+'_domains.json')).read_text())['domains']
 out={'source':name,'scope':'bounded_integer_necessary_system_only','node_limit':limit,'nodes':0,'status':'running','tree':{}}
 def save(): (HERE/(name+'_branch.json')).write_text(json.dumps(out,separators=(',',':'))+'\n')
 def visit(node,domains,seed=None,depth=0):
  out['nodes']+=1
  if out['nodes']>limit:node['status']='node_limit';return False
  pr=propagate(allrows,domains,seedvars=seed)
  node['propagation']={k:v for k,v in pr.items()if k!='domains'}
  if pr['outcome']=='exact_domain_obstruction':node['status']='exact_domain_obstruction';return True
  dom=pr['domains'];res=phase(rr,dom)
  if res['status']!='fractional_proposal':node.update(res);return res['status']=='exact_bounded_linear_obstruction'
  x=res['values'];candidate=[round(v)for v in x]
  if all(candidate[j]in dom[j]for j in range(len(dom))) and all(sum(a*v for a,v in zip(row[:-1],candidate))==row[-1]for row in rr):
   node.update(status='exact_integer_survivor',values=candidate);return False
  fractions=[(min(v-math.floor(v),math.ceil(v)-v),-len(dom[j]),j)for j,v in enumerate(x)if len(dom[j])>1 and abs(v-round(v))>1e-7]
  if not fractions:node.update(status='unresolved_numerical_rounding');return False
  _,_,j=max(fractions);k=math.floor(x[j]);left=[v for v in dom[j]if v<=k];right=[v for v in dom[j]if v>k]
  if not left or not right:node.update(status='unresolved_invalid_split');return False
  node.update(status='split',variable=j,cut=k,children=[{},{}])
  if out['nodes']%10==1:print('node',out['nodes'],'depth',depth,'split',j,k,'elapsed',round(time.monotonic()-start,2),flush=True);save()
  a=[list(v)for v in dom];a[j]=left
  if not visit(node['children'][0],a,[j],depth+1):return False
  a=[list(v)for v in dom];a[j]=right
  return visit(node['children'][1],a,[j],depth+1)
 complete=visit(out['tree'],rootdomains)
 out['status']='exact_bounded_integer_obstruction'if complete else'incomplete_or_survivor';out['seconds']=time.monotonic()-start;save()
 print(out['status'],'nodes',out['nodes'],'seconds',out['seconds'],flush=True)
if __name__=='__main__':run(sys.argv[1],int(sys.argv[2])if len(sys.argv)>2 else 1000)
