"""Couple exact finite integer domains with whole-pattern phase inequalities."""
from pathlib import Path
import json,math,sys,time
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix,hstack,vstack,eye
from domain_probe import rows_for,propagate
HERE=Path(__file__).resolve().parent

def dual_or_point(rows,inequalities,domains):
 n=len(domains);m=len(rows);q=len(inequalities)
 scales=[max(1,max(map(abs,row)))for row in rows]
 cs=[max(1,max(map(abs,row)))for row in inequalities]
 A=csc_matrix(np.array([[a/scales[i]for a in row[:-1]]for i,row in enumerate(rows)]))
 C=csc_matrix(np.array([[a/cs[i]for a in row[:-1]]for i,row in enumerate(inequalities)]))
 b=np.array([row[-1]/s for row,s in zip(rows,scales)]);d=np.array([row[-1]/s for row,s in zip(inequalities,cs)])
 eq=hstack((A,eye(m,format='csc'),-eye(m,format='csc'),csc_matrix((m,q))),format='csc')
 ub=hstack((C,csc_matrix((q,2*m)),-eye(q,format='csc')),format='csc')
 bounds=[(min(v),max(v))for v in domains]+[(0,None)]*(2*m+q)
 r=linprog(np.r_[np.zeros(n),np.ones(2*m+q)],A_eq=eq,b_eq=b,A_ub=ub,b_ub=d,bounds=bounds,method='highs')
 if not r.success:return {'status':'numerical_unresolved','message':str(r.message)}
 if r.fun<1e-9:return {'status':'fractional_proposal','values':list(map(float,r.x[:n]))}
 raw=[v/s for v,s in zip(r.eqlin.marginals,scales)]+[min(0,v/s)for v,s in zip(r.ineqlin.marginals,cs)];norm=max(map(abs,raw))
 for k in range(3,19):
  vector=[round(v/norm*10**k)for v in raw];g=math.gcd(*vector);vector=[v//g for v in vector];y,z=vector[:m],vector[m:]
  coeff=[sum(t*row[j]for t,row in zip(y,rows))+sum(t*row[j]for t,row in zip(z,inequalities))for j in range(n)]
  target=sum(t*row[-1]for t,row in zip(y,rows))+sum(t*row[-1]for t,row in zip(z,inequalities))
  upper=sum(max(c*min(v),c*max(v))for c,v in zip(coeff,domains))
  if target>upper:return {'status':'exact_bounded_linear_obstruction','equality_covector':y,'inequality_covector':z,'rhs_value':target,'box_upper':upper}
 return {'status':'numerical_unresolved','objective':float(r.fun)}

def prune(rows,ineq,domains):
 domains=[set(x)for x in domains];stages=[]
 while True:
  changes=[];seeds=set()
  for i,row in enumerate(ineq):
   minimum=sum(min(a*v for v in domains[j])for j,a in enumerate(row[:-1])if a)
   if minimum>row[-1]:return {'status':'exact_inequality_domain_obstruction','stages':stages,'inequality':i,'minimum':minimum,'rhs':row[-1],'domains':[sorted(v)for v in domains]}
   for j,a in enumerate(row[:-1]):
    if not a or len(domains[j])==1:continue
    other=minimum-min(a*v for v in domains[j]);removed=sorted(v for v in domains[j]if a*v+other>row[-1])
    if removed:
     changes.append((i,j,removed));domains[j].difference_update(removed);seeds.add(j)
     if not domains[j]:raise AssertionError('inequality deleted entire domain without detecting total minimum')
  if not changes:break
  base=propagate(rows,domains,seedvars=sorted(seeds),record_steps=True);stages.append({'inequality_steps':changes,'equality_result':base})
  if base['outcome']=='exact_domain_obstruction':return {'status':'exact_equality_domain_obstruction','stages':stages,'domains':base['domains']}
  domains=[set(x)for x in base['domains']]
 return {'status':'consistent','stages':stages,'domains':[sorted(v)for v in domains]}

def main(fi):
 name=f'frame{fi}';d,rows,rank=rows_for(name);rr=rows[len(d['rhs']):len(d['rhs'])+rank]
 domainfile=json.loads((HERE/(name+'_domains.json')).read_text());source=json.loads((HERE/f'phasecut_frame{fi}.json').read_text())
 keep=d['metadata']['source_metadata']['retained_indices'];lower=d['source_lower']
 out={'frame':fi,'scope':'pseudo_unitary_necessary_all_integer_patterns','branches':[]}
 for bi,branch in enumerate(source['branches']):
  inequalities=[]
  for coeff,b in zip(source['rounded_coefficients'],branch['rounded_rhs']):
   inequalities.append([coeff[j]for j in keep]+[b-sum(c*v for c,v in zip(coeff,lower))])
  result=prune(rows,inequalities,domainfile['domains']);rec={'branch':bi,'indicators':branch['indicators'],'inequalities':inequalities,'domain_propagation':result}
  if result['status']=='consistent':
   trial=dual_or_point(rr,inequalities,result['domains']);rec['linear']=trial
   print('branch',bi,trial['status'],len(result['stages']),'fixed',sum(len(x)==1 for x in result['domains']),flush=True)
  else:print('branch',bi,result['status'],len(result['stages']),flush=True)
  out['branches'].append(rec);(HERE/f'hybrid_frame{fi}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
if __name__=='__main__':main(int(sys.argv[1]))
