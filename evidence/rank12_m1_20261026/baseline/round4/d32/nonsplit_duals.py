from pathlib import Path
import json,sys,itertools
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path[:0]=[str(ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/family_graded'),str(ROOT/'prior_round/round3/d32')]
from feudal_dual import reconstruct
import ring_checks as common,bimodule
DATA=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json').read_text());out=[]
for u in [7,3]:
 src=json.loads((HERE/('nonsplit_ising_'+str(u)+'.json')).read_text());R=src['tensor'];labs=src['labels'];F0,mul,du=reconstruct(R,src['certificate']);degree=[(2*x[1],x[2])if x[0]=='g'else(x[1],x[2])for x in labs];c=labs.index(['g',0,1,0]);q=16;fix=F0(c,c,c,c);common.require(fix in(0,8),'C2 associator class')
 F=lambda a,b,d,k:(F0(a,b,d,k)+fix*degree[a][1]*degree[b][1]*degree[d][1])%q
 M,info=bimodule.construct(R,F,c,q=q);hits=[]
 for rid,T in DATA.items():
  if M is None or common.coarse(T)!=common.coarse(M):continue
  p=common.based_iso(T,M)
  if p is not None:hits.append(rid);out.append(dict(id=rid,u=u,source_tensor=R,source_labels=labs,liptrap_certificate=src['certificate'],subgroup_generator=c,subgroup_correction=fix,source_degrees=degree,model_tensor=M,basis_map=p,bimodules=info['objects']))
 print('NEW SOURCE',u,'rank',info['rank'],'max',max(x for a in M for b in a for x in b),'hits',hits,flush=True)
(HERE/'nonsplit_dual_results.json').write_text(json.dumps(out,indent=2)+'\n')
