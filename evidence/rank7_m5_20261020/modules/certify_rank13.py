"""Check reconstructed based rings and extract the forbidden rank-thirteen subrings."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import json,hashlib,numpy as np
from pathlib import Path
B=Path(__file__).parent;P=B.parents[2]
rows=json.load(open(B/'r4982_dual_fusion_options.json'));out=[]
assert len(rows)==2
for row in rows:
 assert row['product_option_counts']=={'1':729}
 assert row['incompatible_products']==[] and row['ambiguous_products']=={} and row['associativity_failures']==[]
 n=39;N=np.array([[row['unique_products'][f'{i},{j}'] for j in range(n)] for i in range(n)],dtype=np.int64);du=row['duality'];d=np.array([1]*12+[4]*27,dtype=np.int64)
 assert np.min(N)>=0 and np.array_equal(N[0],np.eye(n,dtype=np.int64)) and np.array_equal(N[:,0,:],np.eye(n,dtype=np.int64))
 assert np.array_equal(N[:,:,0],np.array([[int(j==du[i]) for j in range(n)] for i in range(n)]))
 assert all(du[du[i]]==i for i in range(n))
 for i in range(n):
  for j in range(n):
   assert N[i,j]@d==d[i]*d[j]
   assert all(N[i,j,k]==N[du[i],k,j]==N[k,du[j],i] for k in range(n))
   assert np.array_equal(N[i]@N[j],sum((int(N[j,i,k])*N[k] for k in range(n)),np.zeros((n,n),dtype=np.int64)))
 S={0,14};prev=None
 while prev!=S:
  prev=set(S);S.update(du[i] for i in prev)
  for i in prev:
   for j in prev:S.update(int(k) for k in np.nonzero(N[i,j])[0])
 S=sorted(S);assert S==[0,1,4,9,14,15,18,23,25,27,30,33,38]
 inv=[i for i in S if d[i]==1];assert inv==[0,1,4,9]
 assert all(N[g,g,0]==1 for g in inv)
 sub=N[np.ix_(S,S,S)].tolist();sd=[int(d[i]) for i in S]
 assert sum(a*a for a in sd)==148 and sorted(sd)==[1]*4+[4]*9
 out.append({'dual_rank':n,'dual_dimensions':[1]*12+[4]*27,'generator':14,'closed_subset':S,'subring_rank':len(S),'subring_dimension':148,'subring_dimensions':sd,'invertible_indices_in_dual':inv,'invertible_group':'C2 x C2','tensor':sub})
R=next(r['tensor'] for r in json.load(open(P/'supplements/rank7/output/m5/census.json')) if r['id']=='R7_5_4982')
cert={'id':'R7_5_4982','kind':'cyclic3_full_morita_rank13_descent','scope':'general','input_tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'fourier_sectors':18,'module_isomorphism_classes':1,'possible_dual_based_rings':2,'branches':out,'contradiction':'An integral category of dimension 4p, p>3 prime, with dimensions (1^4,4^((p-1)/4)) must have cyclic C4 invertibles; both forced rank13 subcategories instead have C2 x C2.'}
(B/'r4982_exclusion_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print('Both rank39 based rings and forbidden V4 rank13 subrings verified; dimension 148 = 4*37.',flush=True)
