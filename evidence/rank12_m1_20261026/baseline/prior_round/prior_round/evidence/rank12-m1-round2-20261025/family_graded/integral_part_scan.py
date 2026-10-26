from pathlib import Path
import json,itertools,sys
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));from twisted_c2_models import construct,common
from feudal40 import rings
D=json.loads((BASE/'tensors.json').read_text());P={r['id']:r for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']=='D40'}
models=[]
for name in ['F20','D10xC2']:
 R=next(R for p,R in rings()if p['group']==name);G=[[R[a][b].index(1)for b in range(20)]for a in range(20)];c=10 if name=='F20'else 5
 parameters=([dict(cyclic_class=k)for k in[0,2]]if name=='F20'else[dict(trilinear_coefficients=[0,b,c])for b,c in itertools.product(range(2),repeat=2)])
 for par in parameters:
  if name=='F20':w=lambda a,b,c:par['cyclic_class']*(a//5)*(((b//5)+(c//5))//4)%4
  else:
   terms=[(0,0,0),(1,1,1),(0,1,1)];bits=par['trilinear_coefficients'];coords=lambda a:((a//5)&1,(a//5)>>1)
   w=lambda a,b,c:2*(sum(v*coords(a)[i]*coords(b)[j]*coords(c)[k]for v,(i,j,k)in zip(bits,terms))%2)
  T,info=construct(G,c,w,expected_rank=8);hits=[]
  for rid in P:
   RR=D[rid];inds=[a for a,v in enumerate(P[rid]['dimensions_in_field'])if len(v)==1];B=[[[RR[a][b][d]for d in inds]for b in inds]for a in inds]
   bm=common.based_iso(B,T)
   if bm is not None:hits.append(rid)
  models.append(dict(group=name,parameters=par,model_tensor=T,matches=hits));print(name,par,hits,flush=True)
(OUT/'integral_part_results.json').write_text(json.dumps(models,indent=2)+'\n')
