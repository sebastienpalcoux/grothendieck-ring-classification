"""Discover exact integral induction Gram factors; no negative numerical claim."""
from pathlib import Path
import itertools,json,math,time
import sympy as s
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
OLD=REPO/'evidence/rank8_frontier_20261021'
TARGETS={'R8_3_65','R8_3_1768','R8_3_1795','R8_3_3472'}

def require(ok,msg):
 if not ok:raise ValueError(msg)

def rows(G):
 G=s.Matrix(G); piv=list(G.rref()[1]);rank=len(piv)
 if not rank:return [],{'rank':0,'box':1}
 H=G.extract(piv,piv).inv();L=H*G.extract(piv,range(G.cols))
 den=int(s.ilcm(*[v.q for v in L]));Li=[[int(v*den)for v in L.row(i)]for i in range(rank)]
 dh=int(s.ilcm(1,*[v.q for v in H]));Hi=[[int(H[i,j]*dh)for j in range(rank)]for i in range(rank)]
 lim=[math.isqrt(int(G[j,j]))for j in piv];alllim=[math.isqrt(int(G[j,j]))for j in range(G.cols)]
 found=[]
 for p in itertools.product(*(range(v+1)for v in lim)):
  if not any(p):continue
  norm=sum(p[i]*Hi[i][j]*p[j]for i in range(rank)for j in range(rank))
  if norm>dh:continue
  v=[sum(p[i]*Li[i][j]for i in range(rank))for j in range(G.cols)]
  if any(x%den or x<0 or x>den*bound for x,bound in zip(v,alllim)):continue
  found.append(tuple(x//den for x in v))
 return sorted(found),{'rank':rank,'pivot_columns':piv,'box':math.prod(x+1 for x in lim)}

def run():
 import numpy as np
 from scipy.optimize import milp, Bounds, LinearConstraint
 source={r['id']:r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
 candidates=json.loads((OLD/'quadratic/connected_algebra_candidates_results.json').read_text())['records']+json.loads((OLD/'structural_models/algebra_candidates.json').read_text())['records']
 results=json.loads((HERE/'gram_discovery.json').read_text())if (HERE/'gram_discovery.json').exists()else[]
 completed={(x['id'],x['candidate_index'])for x in results}
 for row in candidates:
  rid=row['id']
  if rid not in TARGETS:continue
  R=source[rid]['tensor'];total=len(row['necessary_survivor_vectors'])
  for ai,a in enumerate(row['necessary_survivor_vectors']):
   if (rid,ai) in completed:continue
   start=time.monotonic();G=s.Matrix(8,8,lambda i,j:sum(a[k]*R[i][k][j]for k in range(8))-a[i]*a[j]);V,meta=rows(G)
   pairs=list(itertools.combinations_with_replacement(range(8),2));E=np.array([[v[i]*v[j]for v in V]for i,j in pairs],dtype=float);b=np.array([int(G[i,j])for i,j in pairs],dtype=float)
   bounds=[min(int(G[i,i])//(v[i]**2)for i in range(8)if v[i])for v in V]
   record={'id':rid,'candidate_index':ai,'algebra_object':a,'gram':G.tolist(),'vectors':V,'bounds':bounds,'enumeration':meta}
   if not V:
    require(not any(G),'empty vector domain butnonzeroGram');x=[];record['status']='exact_integer_factor'
   else:
    ans=milp(np.ones(len(V)),integrality=np.ones(len(V)),bounds=Bounds(np.zeros(len(V)),bounds),constraints=LinearConstraint(E,b,b),options={'time_limit':5})
    x=[int(round(z))for z in ans.x]if ans.x is not None else None
    if x is not None and all(0<=n<=lim for n,lim in zip(x,bounds))and all(sum(n*v[i]*v[j]for n,v in zip(x,V))==G[i,j]for i,j in pairs):record['status']='exact_integer_factor'
    else:record['status']='integer_feasibility_unresolved';x=None
   record['multiplicities']=x;results.append(record)
   print(rid,ai+1,total,meta['rank'],len(V),record['status'],round(time.monotonic()-start,3),flush=True)
   (HERE/'gram_discovery.json').write_text(json.dumps(results,default=int,separators=(',',':'))+'\n')
 return results
if __name__=='__main__':run()
