from pathlib import Path
import sys,json
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'repositories/classification-sparse/supplements/rank6/software'))
from group_theoretical import permutation_group,subgroup,fusion
sys.path.insert(0,str(BASE/'work/models'))
from match_models import read,based_iso,tensor_hash

def main():
 G,M=permutation_group(4)
 cases=[('C2',( (1,0,2,3),)),('D8',((1,2,3,0),(0,3,2,1))),('V4',((1,0,2,3),(0,1,3,2))),('S3',((1,0,2,3),(1,2,0,3)))]
 out=[]
 for name,gens in cases:
  H=subgroup(M,[G.index(g)for g in gens]);print('START',name,len(H),flush=True)
  R=fusion(M,H);n=len(R);print('RANK',n,flush=True)
  if n not in [9,10]:continue
  for i,T in enumerate(read(n),1):
   p=based_iso(T,R)
   if p is not None:
    rid=f'R{n}_1_{i}';print('MATCH',name,rid,flush=True)
    out.append({'id':rid,'tensor_sha256':tensor_hash(T),'status':'unitarily_realized','models':[{'model':f'C(S4,1,{name},1)','constructor':'untwisted_group_theoretical','parameters':{'group':'S4','degree':4,'subgroup':name,'subgroup_generators':gens},'reference':'Ostrik, Module categories over the Drinfeld double of a finite group; unitary bimodules over the subgroup algebra in Vec(S4). Fusion computed by equivariant bundle convolution.','basis_map_source_to_model':p,'model_tensor':R}]})
 (Path(__file__).parent/'group_theoretical_models.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
