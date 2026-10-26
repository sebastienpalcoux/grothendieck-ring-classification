"""Actual graph-subgroup group-theoretical candidates at dimension 120."""
from signed_mod4 import *
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE/'sources/work/rank11/arithmetic/legacy'))
import group_models as gt
sys.path.insert(0,str(BASE/'sources'))
import group_theoretical as old

def candidate():
 vals,A=old.permutation_group(5,True)
 r=vals.index((1,2,3,4,0));s=vals.index((0,4,3,2,1));D=gt.subgroup(A,[r,s]);C=gt.subgroup(A,[r])
 G=gt.group_product(A,[[0,1],[1,0]])
 H=sorted(2*g+int(g not in C)for g in D)
 common.require(len(G)==120 and len(H)==10 and H==gt.subgroup(G,H),'actual graph subgroup')
 return G,H

if __name__=='__main__':
 start=time.monotonic();G,H=candidate();R,info=gt.fusion(G,H);print(info,flush=True);out=[]
 if R is not None:
  T=json.loads((BASE/'tensors.json').read_text())
  for rid,S in T.items():
   if common.coarse(S)!=common.coarse(R):continue
   p=common.based_iso(S,R)
   if p is not None:
    common.require(all(S[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in itertools.product(range(12),repeat=3)),'all 1728 coefficients')
    out.append(dict(id=rid,status='unitarily_realized',tensor_sha256=common.sha(S),name='C(A5 x C2, graph(D10 reflection sign))',constructor='group_theoretical',parameters=dict(group_table=G,subgroup=H,cocycle='trivial',subgroup_cochain='trivial'),model_tensor=R,basis_map_source_to_model=p))
 print('matches',[r['id']for r in out],'seconds',time.monotonic()-start,flush=True)
 (Path(__file__).resolve().parent/'group_graph_models.json').write_text(json.dumps(dict(candidate_info=info,models=out),indent=2)+'\n')
