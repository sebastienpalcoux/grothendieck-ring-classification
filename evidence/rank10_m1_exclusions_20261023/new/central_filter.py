import sys,json,pathlib,importlib.util
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parents[1]/'prior/rank9_rank10_m1_20261023'
spec=importlib.util.spec_from_file_location('old',P/'work/audit_new_models/verify_rank10_reciprocity.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
records={a['id']:a for a in json.load(open(P.parents[1]/'catalogue.json'))['cases']}
def sub(x,y):return old.add(x,old.scale(-1,y))
def inv(x):
 a,b,c,d=x; y=(a,b,-c,-d);z=old.mul(x,y);t=(z[0],-z[1],0,0);num=old.mul(y,t);den=old.mul(z,t);assert den[1:]==(0,0,0) and den[0];return old.scale(1/den[0],num)
def mv(T,v):return [sum(t*x for t,x in zip(row,v)) for row in T]
def psd(A):
 a=[[F(x) for x in r] for r in A];n=len(a)
 for i in range(n):
  if a[i][i]<0:return False
  if not a[i][i]:
   if any(a[i][j] for j in range(i+1,n)):return False
   continue
  for j in range(i+1,n):
   for k in range(j,n):a[j][k]=a[k][j]=a[j][k]-a[j][i]*a[k][i]/a[i][i]
 return True

def main():
 for q in [114,115,152,153,179]:
  id=f'R10_1_{q}';rec=records[id];N=rec['fusion_tensor'];dual=rec['invariants']['dual_indices'];a=json.load(open(P/f'work/resolve_rank10_quadratic/{id}_reciprocal.json'))
  chars=[[old.decode(x) for x in row] for row in a['characters']]
  dualchars=[chars.index([r[i] for i in dual]) for r in chars]
  sqchars=[chars.index([(x[0],-x[1],x[2],-x[3]) for x in r]) for r in chars]
  fs=[old.decode(x) for x in a['formal_codegrees']]
  B=[[sum(N[k][j][l]*N[l][dual[k]][i] for k in range(10) for l in range(10)) for j in range(10)] for i in range(10)]
  T=[[old.total(old.mul(chars[h][dual[i]],old.mul(chars[sqchars[h]][j],inv(fs[sqchars[h]]))) for h in range(10)) for j in range(10)] for i in range(10)]
  assert all(x[1:]==(0,0,0) for r in T for x in r)
  T=[[x[0] for x in row] for row in T]
  print(id,'T=',T,flush=True)
  good=[];counts=[0,0,0]
  for sol in a['solutions']:
   V=[a['column_sets'][h][j] for h,j in enumerate(sol)]
   if any(V[dualchars[h]] != [V[h][i] for i in dual] for h in range(10)):continue
   counts[0]+=1
   if any(mv(T,V[h]) != V[sqchars[h]] for h in range(10)):continue
   counts[1]+=1
   Q=[[B[i][j]-sum(v[i]*v[j] for v in V) for j in range(10)] for i in range(10)]
   if not psd(Q):continue
   counts[2]+=1;good.append(sol)
  print(id,'old',len(a['solutions']),'after',counts,flush=True)
  out=dict(id=id,T=[[str(x) for x in row] for row in T],dualchars=dualchars,sqchars=sqchars,solutions=good,B=B)
  pathlib.Path(__file__).with_name(id+'_central.json').write_text(json.dumps(out,indent=2))
if __name__=='__main__':main()
