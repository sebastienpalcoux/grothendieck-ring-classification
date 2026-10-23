"""Replay the explicit nonsplit group-theoretical model of R11_1_104.

The full group, associator, algebra, and basis map are certificate inputs.
The cocycle search is not needed for this verification.
"""
from pathlib import Path
import sys,json,itertools,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent))
sys.path.insert(0,str(HERE.parent/'integral'))
from common import read,sha,validate,require
from gt32 import fusion

def main():
 d=json.loads((HERE/'jordan_gt_model.json').read_text())
 G=d['group_table'];w=np.array(d['omega'],dtype=np.int64);H=d['subgroup'];n=32
 require(d['modulus']==8 and w.shape==(n,n,n),'cocycle dimensions')
 require(all(0<=int(x)<8 for x in w.flat),'cocycle exponents')
 def sigma(a):
  a0,a1,a2=[(a>>i)&1 for i in range(3)]
  return(a0^a1)+2*(a1^a2)+4*a2
 pp=[list(range(8))]
 for _ in range(3):pp.append([sigma(a)for a in pp[-1]])
 require(G==[[4*(a^pp[e][b]^(1 if e+f>=4 else 0))+(e+f)%4 for b in range(8)for f in range(4)]for a in range(8)for e in range(4)],'specified nonsplit group')
 require(all(G[0][a]==G[a][0]==a and 0 in G[a]for a in range(n)),'identity and inverses')
 require(all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(n),repeat=3)),'group associativity')
 require(H==[0,8,16,24]and all(G[a][b]in H for a,b in itertools.product(H,repeat=2)),'specified subgroup')
 require(d['psi']==[[0]*4 for _ in range(4)],'specified trivial algebra cochain')
 require(not np.any(w[0,:,:])and not np.any(w[:,0,:])and not np.any(w[:,:,0]),'normalized associator')
 gg=np.array(G);ii=np.arange(n)
 for a in range(n):
  delta=w-w[gg[a],:,:]+w[a,gg[:,:,None],ii[None,None,:]]-w[a,ii[:,None,None],gg[None,:,:]]+w[a,:,:,None]
  require(not np.any(delta%8),'full cocycle equation at first coordinate '+str(a))
 require(all(w[a,b,c]==0 for a,b,c in itertools.product(H,repeat=3)),'trivial algebra associator')
 for a,b,c in itertools.product(range(8),repeat=3):
  a0=a&1;b0,b1,b2=[(b>>i)&1 for i in range(3)];c0,c1,c2=[(c>>i)&1 for i in range(3)]
  require(w[4*a,4*b,4*c]==4*((a0*(b0*c0+b1*c1+b2*c2+b1*c2))%2),'specified restriction to A')
 psi={(a,b):0 for a,b in itertools.product(H,repeat=2)}
 T,labs=fusion(G,H,2*w,psi)
 require(T==d['model_tensor'],'reconstructed GT tensor')
 dimensions=[4*sum(v['character_polynomial'][0].values())//len(v['stabilizer'])for v in labs]
 require(sorted(dimensions)==[1]*4+[2]*7 and sum(x*x for x in dimensions)==32,'simple dimensions')
 require(labs==[{**v,'scalar_projective':{int(k):e for k,e in v['scalar_projective'].items()},'character_polynomial':{int(k):{int(e):c for e,c in ch.items()}for k,ch in v['character_polynomial'].items()}}for v in d['labels']],'reconstructed projective labels')
 validate(T);R=read()['R11_1_104'];q=d['basis_map_source_to_model']
 require(sha(R)==d['tensor_sha256'],'source tensor hash')
 require(q[0]==0 and sorted(q)==list(range(11)),'unital basis permutation')
 require(all(R[a][b][c]==T[q[a]][q[b]][q[c]]for a,b,c in itertools.product(range(11),repeat=3)),'all source fusion coefficients')
 report={'status':'PASS','id':'R11_1_104','model':'C(G32_nonsplit_Jordan, omega, V4, 1)','modulus':8,'group_associativity_checks':32**3,'cocycle_checks':32**4,'algebra_checks':4**3,'fusion_coefficients':11**3,'basis_map_source_to_model':q,'certificate_sha256':hashlib.sha256((HERE/'jordan_gt_model.json').read_bytes()).hexdigest(),'scope':'Full categorical input and primary GT tensor replay; independent tensor implementation is in nonintegral/audit104.'}
 (HERE/'jordan_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 return report
if __name__=='__main__':main()
