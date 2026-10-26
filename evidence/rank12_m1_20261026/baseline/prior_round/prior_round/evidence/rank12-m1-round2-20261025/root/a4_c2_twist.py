"""Positive-only eighth-root subgroup-bimodule retry."""
from signed_mod4 import *
sys.path.insert(0,str(BASE));import group_models as gm
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'family_integral'))
from twisted_h4_matrix import construct
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'family_graded'))
from twisted_h4_scan import coordinates,psi_solutions

if __name__=='__main__':
 start=time.monotonic();els,G,H,w4=coordinates();D=json.loads((BASE/'tensors.json').read_text());models=[];attempts=[]
 for typ in (0,1):
  w0=lambda a,b,c:typ*w4(a,b,c);P0=psi_solutions(G,H,w0)
  for schur in (0,1):
   w=lambda a,b,c:2*w0(a,b,c)
   psi=lambda a,b:(2*P0[a,b]+4*schur*els[a][1]*els[b][2])%8
   try:R,info=construct(G,H,w,psi)
   except ValueError as e:
    attempts.append(dict(type=typ,schur=schur,result='unsupported',reason=str(e)));print(attempts[-1],flush=True);continue
   hits=[]
   if R is not None:
    common.validate(R)
    for rid,S in D.items():
     if common.coarse(S)!=common.coarse(R):continue
     p=common.based_iso(S,R)
     if p is None:continue
     common.require(all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 coefficients')
     hits.append(rid);models.append(dict(id=rid,name=f'C(A4 x C2, mixed cocycle{typ}, HgraphV4, psi{schur})',constructor='twisted_group_theoretical_h4',parameters=dict(group_table=G,subgroup=H,cocycle_exponents=[[[w(a,b,c)for c in range(24)]for b in range(24)]for a in range(24)],phase_modulus=8,subgroup_cochain=[[a,b,psi(a,b)]for a,b in itertools.product(H,repeat=2)],coordinates=els,cocycle_type=typ,schur_class=schur),model_tensor=R,basis_map_source_to_model=p,bimodule_witness=info))
   attempts.append(dict(type=typ,schur=schur,info={k:v for k,v in info.items()if k!='objects'},matches=hits));print(attempts[-1],flush=True)
 (Path(__file__).resolve().parent/'a4_c2_twist_models.json').write_text(json.dumps(dict(models=models,attempts=attempts,elapsed_seconds=time.monotonic()-start),indent=2)+'\n')
