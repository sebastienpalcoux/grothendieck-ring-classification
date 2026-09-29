import sys,json,itertools,time,math
from pathlib import Path
from fractions import Fraction
import sympy as s
root=Path(__file__).resolve().parent;rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91';d=json.load(open(root/(rid+'_count_space.json')));V=d['vectors'];M=s.Matrix([r+[b] for r,b in zip(d['A'],d['b'])]);rr,piv=M.rref();free=d['free'];G=d['b'][:15];diag=[G[j] for j in [0,5,9,12,14]];ub=[min(diag[k]//(v[k]*v[k]) for k in range(5) if v[k]) for v in V];n=len(free);co=[[int(i==j) for j in free] for i in range(len(V))];const=[0]*len(V)
for row,i in enumerate(piv):
 require=lambda p,msg: None if p else (_ for _ in ()).throw(ValueError(msg))
 require(all(x.q==1 for x in rr[row,:]),'noninteger rref');const[i]=int(rr[row,-1]);co[i]=[-int(rr[row,j]) for j in free]
order=sorted(range(n),key=lambda j:(ub[free[j]],-sum(abs(c[j]) for c in co)));co=[[c[j] for j in order] for c in co];bounds=[ub[free[j]] for j in order];smin=[[0]*len(V) for _ in range(n+1)];smax=[[0]*len(V) for _ in range(n+1)]
for level in range(n-1,-1,-1):
 for i in range(len(V)):
  z=co[i][level]*bounds[level];smin[level][i]=smin[level+1][i]+min(0,z);smax[level][i]=smax[level+1][i]+max(0,z)
out=[];nodes=0;st=time.monotonic()
def dfs(level,partial):
 global nodes
 nodes+=1
 if nodes%100000==0 and time.monotonic()-st>750:raise TimeoutError('explicit enumeration limit')
 if any(p+smax[level][i]<0 or p+smin[level][i]>ub[i] for i,p in enumerate(partial)):return
 if level==n:out.append(partial);return
 for x in range(bounds[level]+1):dfs(level+1,[p+co[i][level]*x for i,p in enumerate(partial)])
dfs(0,const);out.sort();rec=dict(id=rid,complete=True,nodes=nodes,seconds=time.monotonic()-st,profiles=len(out),free_bounds=bounds,rank_distribution={str(k):sum(sum(x)+6==k for x in out) for k in sorted(set(sum(x)+6 for x in out))},zero_sigma=sum(x[V.index([0,0,1,0,0])]==0 for x in out),zero_g=sum(x[V.index([0,0,0,1,0])]==0 for x in out),counts=out);(root/(rid+'_count_profiles.json')).write_text(json.dumps(rec,indent=2)+'\n');print({k:v for k,v in rec.items() if k!='counts'})
