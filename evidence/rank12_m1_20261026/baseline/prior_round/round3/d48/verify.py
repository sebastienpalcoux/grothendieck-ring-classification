#!/usr/bin/env python3
"""Standalone exact replay of the two D48 positive witnesses; requires NumPy.

No catalogue, GAP runtime, parent checkout, network, or floating arithmetic is
used. All categorical data are frozen in positive_witnesses.json. Failures
raise explicit ValueError exceptions, including when Python runs with -O.
"""
from pathlib import Path
import hashlib,itertools,json,sys
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'verification_modules'))
from twisted_h4_matrix import construct

def require(c,m):
 if not c:raise ValueError(m)
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def verify(r):
 G=np.array(r['group_table'],dtype=np.int64);W=np.array(r['omega'],dtype=np.int64);H=r['subgroup'];n=len(G);m=r['modulus'];I=np.arange(n)
 require(n==48 and G.shape==(n,n),'group table shape');require(((G>=0)&(G<n)).all(),'group entries')
 require(np.array_equal(G[0],I)and np.array_equal(G[:,0],I),'identity zero')
 require(all(any(G[a,b]==G[b,a]==0 for b in range(n))for a in range(n)),'two-sided inverses')
 require(all(G[G[a,b],c]==G[a,G[b,c]]for a,b,c in itertools.product(range(n),repeat=3)),'all group associativity equations')
 require(len(set(H))==4 and 0 in H and all(G[a,b]in H for a,b in itertools.product(H,repeat=2)),'order-four subgroup')
 require(W.shape==(n,n,n)and ((W>=0)&(W<m)).all(),'cocycle shape and entries')
 require(not W[0,:,:].any()and not W[:,0,:].any()and not W[:,:,0].any(),'normalized cocycle')
 bs=I[:,None,None];cs=I[None,:,None];ds=I[None,None,:]
 for a in range(n):
  delta=W+W[a,G[:,:,None],ds]+W[a,:,:,None]-W[G[a,:,None,None],cs,ds]-W[a,bs,G[None,:,:]]
  require(not np.mod(delta,m).any(),'all group 3-cocycle equations, first variable '+str(a))
 require(all(W[a,b,c]==0 for a,b,c in itertools.product(H,repeat=3)),'trivial subgroup restriction')
 require(all(not any(row)for row in r['psi']),'trivial subgroup 2-cochain')
 require(sha(W.tolist())==r['omega_sha256'],'cocycle SHA256')
 require(sha(r['source_tensor'])==r['source_tensor_sha256'],'source tensor SHA256')
 require(sha(r['model_tensor'])==r['model_tensor_sha256'],'model tensor SHA256')
 N,info=construct(G.tolist(),H,lambda a,b,c:int(W[a,b,c]))
 require(N==r['model_tensor'],'all exact model tensor entries')
 require(info['objects']==r['objects'],'all regenerated simple bimodule actions')
 p=r['source_to_model'];require(sorted(p)==list(range(12))and p[0]==0,'unit preserving basis bijection')
 require(all(r['source_tensor'][a][b][c]==N[p[a]][p[b]][p[c]]for a,b,c in itertools.product(range(12),repeat=3)),'all 1728 source-to-model coefficients')
 dims=[len(o['support'])*o['fiber_dimension']//4 for o in info['objects']]
 require(sorted(dims)==[1]*8+[2]*2+[4]*2,'simple dimensions')
 require(all(sum(N[a][b][c]*dims[c]for c in range(12))==dims[a]*dims[b]for a,b in itertools.product(range(12),repeat=2)),'FP dimension character')
 return dict(id=r['id'],status='verified_unitary_model',all_group_cocycle_equations=48**4,all_source_to_model_coefficients=12**3,source_sha256=r['source_tensor_sha256'],model_sha256=r['model_tensor_sha256'])

def main():
 data=json.loads((HERE/'positive_witnesses.json').read_text());require({r['id']for r in data}=={'R12_1_414','R12_1_531'},'exact positive witness set')
 receipt=[verify(r)for r in data]
 (HERE/'verification_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
