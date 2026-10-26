from setup import *
import importlib.util
from twisted_h4_matrix import construct as construct_old

def groupcheck(G,H):
 A=np.array(G,dtype=int);n=len(G);ii=np.arange(n)
 common.require(np.array_equal(A[0],ii)and np.array_equal(A[:,0],ii),'actual unit')
 common.require(all(np.array_equal(A[A[a,:],:],A[a,A])for a in range(n)),'actual group associativity')
 common.require(all(any(G[a][b]==G[b][a]==0 for b in range(n))for a in range(n)),'group inverses')
 common.require(0 in H and len(set(H))==len(H)and all(G[a][b]in H for a,b in itertools.product(H,repeat=2)),'actual subgroup')
def bind(rid,M,p):
 common.require(sorted(p)==list(range(12))and p[0]==0,'based bijection')
 common.require(all(DATA[rid][a][b][c]==M[p[a]][p[b]][p[c]]for a,b,c in itertools.product(range(12),repeat=3)),'all1728inputentries')
def main():
 out=[]
 ordinary=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/root/group_graph_models.json').read_text())['models']
 ordinary += [dict(id=r['id'],**r['model'])for r in json.loads((OLD/'order48_models.json').read_text())]
 for r in ordinary:
  G=r['parameters']['group_table'];H=r['parameters']['subgroup'];groupcheck(G,H)
  common.require(r['parameters']['cocycle']=='trivial'and r['parameters']['subgroup_cochain']=='trivial','ordinary associator and subgroupcochain')
  M,info=gm.fusion(G,H);common.require(M is not None,'ordinary fullgroup model')
  common.require(common.based_iso(M,r['model_tensor'])is not None,'recomputed modeltensor')
  bind(r['id'],r['model_tensor'],r['basis_map_source_to_model']);out.append(dict(id=r['id'],status='PASS',group_order=len(G),subgroup_order=len(H),actual_categorical_premise='bimodules of ordinary separable subgroup algebra in unitary Vec_G',source_hash=digest(DATA[r['id']])))
 spec=importlib.util.spec_from_file_location('prior_relative_models',ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/d24_pointed_extensions/models.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 rows=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-round2-20261025/d24_pointed_extensions/models.json').read_text())['models'];E,G,h=old.setup()
 for r in rows:
  m=r['model'];pa=m['parameters'];common.require(pa['group_table']==G and pa['subgroup_generator']==h and pa['normal_coordinates']==[list(v)for v in E],'group sourcebinding');w=old.cocycle(E,pa['relative_cocycle_coefficients'],modulus=8);old.verify_group_cocycle(G,[0,h],w,8)
  M,info=construct_old(G,[0,h],w);common.require(M is not None and common.based_iso(M,m['model_tensor'])is not None,'independent scalarbimodule replay');bind(r['id'],m['model_tensor'],m['basis_map_source_to_model']);out.append(dict(id=r['id'],status='PASS',group_order=24,subgroup_order=2,all_cocycle_equations=24**4,subgroup_cochain='trivial',actual_categorical_premise='normalized actual unitary cocycle, trivial exact Hrestriction, connected separable subgroupalgebra',source_hash=digest(DATA[r['id']])))
 (OUT/'earlier_model_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
