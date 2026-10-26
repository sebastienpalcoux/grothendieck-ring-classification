from extra_groups import *
import sympy as s

def fusion(row):
 G,H=row['table'],row['subgroup'];n=len(G);hs=set(H);inv=[next(j for j in range(n)if G[i][j]==0)for i in range(n)];hi={a:i for i,a in enumerate(H)}
 psi=lambda a,b:row['psi'][hi[a]][hi[b]]
 K=s.QQ.cyclotomic_field(96);zeta=K.unit
 objects=[]
 for ob in row['objects']:
  z=ob['z'];orbit={G[G[u][z]][inv[v]]:(u,v)for u in H for v in H};chi={a:sum((K(c)*zeta**j for j,c in enumerate(cs)if c),K.zero)for a,cs in zip(ob['stab'],ob['char'])}
  objects.append((z,ob['stab'],chi,orbit))
 cosets=[];covered=set()
 for x in range(n):
  if x not in covered:cosets.append(x);covered|={G[x][h]for h in H}
 cache={}
 def val(i,x,a,b):
  key=i,x,a,b
  if key in cache:return cache[key]
  z,stab,chi,orb=objects[i]
  if x not in orb or G[a][x]!=G[x][b]:v=K.zero
  else:
   u,v0=orb[x];h=G[G[inv[u]][a]][u];k=G[G[inv[v0]][b]][v0]
   phase=(psi(a,u)-psi(b,v0)-psi(u,h)+psi(v0,k))%2
   v=chi[h]*((-1)**phase)
  cache[key]=v;return v
 rank=len(objects);R=[[[0]*rank for _ in range(rank)]for _ in range(rank)]
 for k,(z,stab,chi,orb)in enumerate(objects):
  for i,j in itertools.product(range(rank),repeat=2):
   result=K.zero
   for a in stab:
    b=G[G[inv[z]][a]][z];tr=K.zero
    for x in cosets:
     h=G[G[inv[x]][a]][x]
     if h in hs:tr+=val(i,x,a,h)*val(j,G[inv[x]][z],h,b)
    conj=sum((K(t)*zeta**(-e)for e,t in enumerate(row['objects'][k]['char'][stab.index(a)])if t),K.zero)
    result+=conj*tr
   result/=K(len(stab));co=result.to_list();common.require(len(co)<=1 and(not co or co[0].denominator==1 and co[0]>=0),'exact nonnegative integer coefficient')
   R[i][j][k]=int(co[0])if co else 0
 units=[i for i in range(rank)if all(R[i][j][k]==R[j][i][k]==int(j==k)for j,k in itertools.product(range(rank),repeat=2))];common.require(len(units)==1,'tensor unit')
 p=[units[0]]+[i for i in range(rank)if i!=units[0]];R=[[[R[a][b][c]for c in p]for b in p]for a in p];common.validate(R)
 return R

def main():
 D=json.loads((BASE/'tensors.json').read_text());ids=[r['id']for r in json.loads((ROOT/'rank12-m1-round2-20261025/unresolved_tensors.json').read_text())if r['exact_dimension_character']['family']=='D48'];out=[];attempt=[]
 for row in json.loads((OUT/'subgroup_twist_candidates.json').read_text()):
  R=fusion(row);mult=max(c for a in R for b in a for c in b);hits=[]
  if mult==1:
   for rid in ids:
    p=common.based_iso(D[rid],R)
    if p is not None:hits.append(rid);out.append(dict(id=rid,parameters=row,tensor=R,source_to_model=p))
  attempt.append(dict(smallgroup=row['smallgroup'],subgroup=row['subgroup'],multiplicity=mult,matches=hits,tensor=R));print(row['smallgroup'],row['subgroup'],mult,hits,flush=True)
  (OUT/'subgroup_twist_models.json').write_text(json.dumps(out,indent=2)+'\n');(OUT/'subgroup_twist_attempts.json').write_text(json.dumps(attempt,indent=2)+'\n')
if __name__=='__main__':main()
