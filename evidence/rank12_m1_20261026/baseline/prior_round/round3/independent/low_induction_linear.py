"""Fresh exact low-induction linear relaxation; SAT is only a necessary-condition witness."""
from pathlib import Path
import json,sys,time,collections,itertools,math
import sympy as s
import z3
BASE=Path(__file__).resolve().parents[2]
FIRST=BASE/'rank12-m1-offline-20261025';sys.path.insert(0,str(FIRST))
from induction_scan import columns,fp_character,exact,require
ROOT=Path(__file__).resolve().parent
raw=json.loads((BASE/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text())
prof={r['id']:r for r in json.loads((FIRST/'profile.json').read_text())['records']}

def run(row):
 R=row['tensor'];rid=row['id'];p=prof[rid];n=len(R)
 f,K,u,d,D,emb=fp_character(R);B=sum((s.Matrix(A)*s.Matrix(A).T for A in R),s.zeros(n))
 roots=[]
 for q,m in B.charpoly(exact.t).as_poly().factor_list()[1]:
  rr=exact.discover_roots(q,K)
  if rr is None:return dict(result='not_split')
  for root in rr:roots +=[root]*m
 roots.remove(D);groups={}
 for root in roots:
  key=tuple(exact.ec(D/root))
  if key not in groups:
   cs,nodes=columns(d,D/root,K,B,cap=1000000)
   if cs is None:return dict(result='column_budget')
   groups[key]={'columns':cs,'multiplicity':0}
  groups[key]['multiplicity']+=1
 solver=z3.Solver();solver.set(timeout=10000);variables=[];vs=[];blocks=[]
 for gi,(key,g)in enumerate(groups.items()):
  cc=[z3.Int(f'c_{gi}_{j}')for j in range(len(g['columns']))]
  for c in cc:solver.add(c>=0,c<=g['multiplicity'])
  solver.add(z3.Sum(cc)==g['multiplicity']);variables+=cc;vs+=g['columns'];blocks.append({'dimension':list(key),'multiplicity':g['multiplicity'],'columns':g['columns']})
 LL=[[int(i==j==0)+z3.Sum([c*v[i]*v[j]for c,v in zip(variables,vs)if v[i]*v[j]])for j in range(n)]for i in range(n)]
 for i in range(n):
  solver.add(LL[0][i]==int(B[0,i]))
  for j in range(i+1):solver.add(LL[i][j]<=int(B[i,j]))
 # Sound rational weakening of the exact moment inequalities. Use 1e-6 floors,
 # independently validate each proposed linear coefficient bound in K.
 scale=10**6
 for i in range(1,n):
  factor=K(3) if p['dual'][i]!=i else K(3)*d[i]+K.one
  rhs=D*d[i]if p['dual'][i]!=i else D*d[i]*(d[i]+K.one)
  value=float(emb.midpoint(rhs)) if hasattr(emb,'midpoint') else None
  # Exact bounds by binary search for floor in the distinguished embedding.
  def floorval(a):
   lo,hi=-1000000000000,1000000000000
   while lo+1<hi:
    mid=(lo+hi)//2
    if emb.sign(a-K(mid))>=0:lo=mid
    else:hi=mid
   return lo
  b=floorval(K(scale)*rhs)+1; aa=[]
  for v in vs:
   c=factor*sum((K(v[i]*v[j])*d[j]for j in range(n)),K.zero)
   aa.append(floorval(K(scale)*c))
  solver.add(z3.Sum([c*a for c,a in zip(variables,aa)])<=b)
 (ROOT/(rid+'.smt2')).write_text(solver.to_smt2())
 t=time.monotonic();status=solver.check();result={'result':str(status),'seconds':time.monotonic()-t,'columns':sum(len(g['columns'])for g in groups.values()),'blocks':len(groups)}
 if status==z3.sat:
  sol=solver.model();counts=[sol[c].as_long()for c in variables];chosen=[list(v)for c,v in zip(counts,vs)for _ in range(c)]
  L=s.zeros(n);L[0,0]=1
  for v in chosen:L+=s.Matrix(v)*s.Matrix(v).T
  Q=B-L
  require(all(Q[i,j]>=0 for i,j in itertools.product(range(n),repeat=2)),'Gram entries')
  require(all(Q[0,i]==0 for i in range(n)),'first row')
  moments=[]
  for i in range(1,n):
   lo=sum((K(L[i,j])*d[j]for j in range(n)),K.zero)
   gap=K(3)*lo-D*d[i]if p['dual'][i]!=i else(K(3)*d[i]+K.one)*lo-D*d[i]*(d[i]+K.one)
   moments.append(emb.sign(gap))
  minors=all(Q[i,i]*Q[j,j]>=Q[i,j]**2 for i in range(n)for j in range(i))
  result.update(chosen_columns=chosen,exact_moment_pass=max(moments)<=0,two_by_two_minor_pass=minors,residual_gram=[list(map(int,Q.row(i)))for i in range(n)])
 return result

rows=[]
for row in raw:
 if row['id']not in ['R12_1_180','R12_1_181','R12_1_262','R12_1_361','R12_1_362','R12_1_453','R12_1_561','R12_1_628']:continue
 t=time.monotonic()
 try:r=run(row)
 except Exception as e:r={'result':'error','message':str(e)}
 rows.append(dict(id=row['id'],tensor_sha256=row['tensor_sha256'],**r));print(row['id'],{k:v for k,v in r.items()if k not in ['chosen_columns','residual_gram']},time.monotonic()-t,flush=True)
 (ROOT/'low_induction_results.json').write_text(json.dumps(rows,indent=2)+'\n')
