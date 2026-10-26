from extra_groups import *
from twisted_h4_matrix import construct
import hashlib

def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def main():
 rows=json.loads((OUT/'adapted_transfer_models.json').read_text());seen=set();out=[];D=json.loads((BASE/'tensors.json').read_text())
 for r in rows:
  if r['id']in seen or any(r['cup_bits'])or r['subgroup_class']:continue
  G,H,W=r['group'],r['subgroup'],np.array(r['relative_transfer'],dtype=int)
  N,info=construct(G,H,lambda a,b,c:int(W[a,b,c]))
  common.require(N==r['tensor'],'frozen model replay')
  ob=dict(id=r['id'],name=r['name'],group_table=G,subgroup=H,modulus=8,omega=W.tolist(),psi=[[0]*len(H)for _ in H],objects=info['objects'],model_tensor=N,source_tensor=D[r['id']],source_to_model=r['source_to_model'],source_tensor_sha256=sha(D[r['id']]),model_tensor_sha256=sha(N),omega_sha256=sha(W.tolist()),transfer_bits=r['bits'],construction='H-bimodules in Vec_G^omega')
  out.append(ob);seen.add(r['id']);print(r['id'],ob['source_tensor_sha256'],ob['model_tensor_sha256'],flush=True)
 (OUT/'positive_witnesses.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
if __name__=='__main__':main()
