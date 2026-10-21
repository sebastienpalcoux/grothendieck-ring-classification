"""Exact finite integer Gram factorization for connected algebra targets."""
from pathlib import Path
import itertools,json,math,time
import sympy as s
from gram_discovery import rows,require,HERE,REPO,OLD,TARGETS

def bounded_solutions(A,b,bounds):
 n=len(bounds)
 if n==0:return ([[]]if all(v==0 for v in b)else[]),{'rank':0,'nodes':1,'free':[],'complete':True}
 rr,piv=A.row_join(s.Matrix(b)).rref()
 if n in piv:return [],{'inconsistent_rational_system':True,'nodes':0,'complete':True}
 free=[j for j in range(n)if j not in piv]
 free.sort(key=lambda j:max(abs(rr[i,j])for i in range(len(piv)))*bounds[j],reverse=True)
 co=[];lo=[];hi=[]
 for i,p in enumerate(piv):
  den=int(s.ilcm(1,*[rr[i,j].q for j in free+[n]]));r=[int(rr[i,j]*den)for j in free];upper=int(rr[i,n]*den)
  co.append(r);hi.append(upper);lo.append(upper-bounds[p]*den)
 k=len(free);r=len(piv);mn=[[0]*(k+1)for _ in piv];mx=[[0]*(k+1)for _ in piv]
 for i,row in enumerate(co):
  for at in range(k-1,-1,-1):
   v=row[at]*bounds[free[at]];mn[i][at]=mn[i][at+1]+min(0,v);mx[i][at]=mx[i][at+1]+max(0,v)
 partial=[0]*r;values=[0]*n;results=[];nodes=0
 def dfs(at):
  nonlocal nodes
  nodes+=1
  if at==k:
   v=list(values)
   for i,p in enumerate(piv):
    q=rr[i,n]-sum(rr[i,j]*v[j]for j in free)
    if q.q!=1 or not 0<=q<=bounds[p]:return
    v[p]=int(q)
   results.append(v);return
  lower=0;upper=bounds[free[at]]
  for i,row in enumerate(co):
   c=row[at];a=lo[i]-partial[i]-mx[i][at+1];b=hi[i]-partial[i]-mn[i][at+1]
   if c>0:lower=max(lower,-((-a)//c));upper=min(upper,b//c)
   elif c<0:lower=max(lower,-((-b)//c));upper=min(upper,a//c)
   elif not a<=0<=b:return
  for v in range(lower,upper+1):
   values[free[at]]=v
   for i in range(r):partial[i]+=co[i][at]*v
   dfs(at+1)
   for i in range(r):partial[i]-=co[i][at]*v
 dfs(0)
 for v in results:
  require(A*s.Matrix(v)==s.Matrix(b),'original equations')
  require(all(0<=x<=u for x,u in zip(v,bounds)),'bounds')
 require(len({tuple(x)for x in results})==len(results),'duplicate')
 return sorted(results),{'rank':len(piv),'nodes':nodes,'free':free,'unpruned_free_box':math.prod(bounds[j]+1 for j in free),'complete':True}

def run():
 data=json.loads((HERE/'gram_discovery.json').read_text());out=[]
 for rec in data:
  t=time.monotonic();G=s.Matrix(rec['gram']);V,meta=rows(G);require(V==[tuple(v)for v in rec['vectors']],'row enumeration')
  pairs=list(itertools.combinations_with_replacement(range(8),2));A=s.Matrix([[v[i]*v[j]for v in V]for i,j in pairs]);b=[G[i,j]for i,j in pairs]
  sol,em=bounded_solutions(A,b,rec['bounds']);rr={**rec,'status':'exact_complete_Gram_factors'if sol else'exact_integer_Gram_obstruction','all_multiplicities':sol,'integer_enumeration':em};rr.pop('multiplicities')
  out.append(rr);print(rec['id'],rec['candidate_index'],len(V),len(sol),em['nodes'],round(time.monotonic()-t,3),flush=True)
  (HERE/'integral_gram.json').write_text(json.dumps(out,default=int,separators=(',',':'))+'\n')
 return out
if __name__=='__main__':run()
