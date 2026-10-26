from pathlib import Path
import json,sys,itertools,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/family_graded'));from feudal_dual import reconstruct
import ring_checks as common,bimodule
DATA=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json').read_text());SD=json.loads((ROOT/'prior_round/round3/d32/cocycle_SD16_mod16.json').read_text());E=list(itertools.product(range(8),range(2)));ei={g:i for i,g in enumerate(E)};out=[];attempts=[]
for u in [7,3]:
 src=json.loads((HERE/('nonsplit_ising_'+str(u)+'.json')).read_text());R=src['tensor'];labs=src['labels'];F0,mul,du=reconstruct(R,src['certificate']);degree=[(2*x[1],x[2])if x[0]=='g'else(x[1],x[2])for x in labs]
 def omega(g,h,k):
  if u==3:return SD[ei[g]][ei[h]][ei[k]]
  a,b=g;c,d=h;e,f=k;t=c+(-1)**d*e;return(2*a*(-1)**b*((t-t%8)//8))%16
 for rot,mixed,sgn in itertools.product(range(8),range(2)if u==7 else[0],range(2)):
  c=labs.index(['g',0,1,sgn]);fix=F0(c,c,c,c);common.require(fix in(0,8),'C2 associator class')
  def F16(a,b,d,k):
   g,h,j=[degree[x]for x in(a,b,d)];return(F0(a,b,d,k)+fix*g[1]*h[1]*j[1]+rot*omega(g,h,j)+8*mixed*(g[0]%2)*h[1]*j[1])%16
  q=16
  try:M,info=bimodule.construct(R,F16,c,q=q)
  except ValueError as ex:
   if str(ex)!='complete projective stabilizer characters':raise
   q=32;M,info=bimodule.construct(R,lambda a,b,d,k:2*F16(a,b,d,k),c,q=q)
  hits=[]
  for rid,T in DATA.items():
   if common.coarse(T)!=common.coarse(M):continue
   p=common.based_iso(T,M)
   if p is not None:
    hits.append(rid)
    if rid not in[r['id']for r in out]:out.append(dict(id=rid,u=u,rotation_twist=rot,mixed_twist=mixed,subgroup_generator=c,subgroup_correction=fix,phase_modulus=q,source_tensor=R,source_labels=labs,liptrap_certificate=src['certificate'],source_degrees=degree,model_tensor=M,basis_map=p,bimodules=info['objects']))
  attempts.append(dict(u=u,rotation=rot,mixed=mixed,generator=sgn,modulus=q,matches=hits));print(attempts[-1],flush=True)
  (HERE/'nonsplit_twist_results.json').write_text(json.dumps(dict(models=out,attempts=attempts),indent=2)+'\n')
