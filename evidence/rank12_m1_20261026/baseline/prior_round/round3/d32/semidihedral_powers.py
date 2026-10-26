from pathlib import Path
import json,itertools,sys
HERE=Path(__file__).resolve().parent;BASE=HERE.parents[1]/'rank12-m1-offline-20261025'
sys.path.insert(0,str(BASE/'sources/work/rank11'));import common,bimodule
r=json.loads((HERE/'semidihedral_lift_results.json').read_text())['models'][0];labs=[(a,tuple(g))for a,g in r['source_labels']];E=list(itertools.product(range(8),range(2)));ind={g:j for j,g in enumerate(E)};T=r['source_omega'];R=r['source_tensor'];D=json.loads((BASE/'tensors.json').read_text());out=[]
for power in [3,5,7]:
 def F(a,b,c,k):
  aa,bb,cc,kk=[labs[x][0]for x in(a,b,c,k)];g,h,j=[ind[labs[x][1]]for x in(a,b,c)];v=power*T[g][h][j]
  if aa==cc==2 and bb!=2:v+=8*bb*kk
  if aa!=2 and bb==2 and cc!=2:v+=8*aa*cc
  return v%16
 c=labs.index((0,(0,1)));M,info=bimodule.construct(R,F,c,q=16);hits=[]
 for rid,U in D.items():
  if common.coarse(U)!=common.coarse(M):continue
  p=common.based_iso(U,M)
  if p is not None:hits.append(rid)
 out.append(dict(power=power,matches=hits));print(out[-1],flush=True)
(HERE/'semidihedral_powers_results.json').write_text(json.dumps(out,indent=2))
