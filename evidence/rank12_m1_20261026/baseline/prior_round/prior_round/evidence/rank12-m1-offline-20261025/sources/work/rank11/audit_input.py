#!/usr/bin/env python3
"""Independent exact fusion-axiom and pairwise based-isomorphism audit.
Tensor convention: N[i,j,k] is coefficient of b_k in b_i b_j.
"""
from pathlib import Path
import gzip,json,hashlib,collections,itertools,math,time
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import common
OUT=Path(__file__).resolve().parent

def require(condition,message="Exact verification failed"):
 if not condition:raise ValueError(message)

def refinement(N):
 n=len(N); dual=np.argmax(N[:,:,0],axis=1)
 cols=[(int(i==0),int(dual[i]==i),int(N[i,i,i]),int(np.trace(N[i])),int(N[i].sum()),int(N[:,i,:].sum())) for i in range(n)]
 for t in range(n):
  palette={s:i for i,s in enumerate(sorted(set(cols)))}
  cs=[palette[s] for s in cols]
  sig=[]
  for i in range(n):
   c=collections.Counter((cs[j],cs[k],int(N[i,j,k]),int(N[j,i,k]),int(N[j,k,i])) for j in range(n) for k in range(n))
   sig.append((cs[i],cs[dual[i]],tuple(sorted(c.items()))))
  if len(set(sig))==len(set(cols)):
   return (tuple(sorted(sig)),sig)
  cols=sig
 raise AssertionError('refinement did not stabilize')

def graph(N,sigs):
 n=len(N); G=nx.MultiDiGraph()
 for i in range(n): G.add_node(('b',i),color=('basis',sigs[i]))
 for i in range(n):
  for j in range(n):
   p=('p',i,j); G.add_node(p,color=('product',))
   G.add_edge(('b',i),p,role='left'); G.add_edge(('b',j),p,role='right')
   for k in range(n):
    if N[i,j,k]: G.add_edge(p,('b',k),role='output')
 return G

def subrings(N,dual):
 n=len(N); supp=[[sum(1<<k for k in np.flatnonzero(N[i,j])) for j in range(n)] for i in range(n)]
 def closure(mask):
  while True:
   old=mask; a=[i for i in range(n) if mask>>i&1]
   for i in a:
    mask|=1<<int(dual[i])
    for j in a: mask|=supp[i][j]
   if mask==old:return mask
 seen={1}; todo=[1]
 while todo:
  S=todo.pop()
  for i in range(1,n):
   if not S>>i&1:
    T=closure(S|1<<i)
    if T not in seen:seen.add(T);todo.append(T)
 return [[i for i in range(n) if S>>i&1] for S in sorted(seen,key=lambda x:(x.bit_count(),x))]

def radical(q):
 a=1;b=q
 for x in range(2,math.isqrt(q)+1):
  while b%(x*x)==0:a*=x;b//=x*x
 return a,b

def radical_dimension_certificate(N,d):
 sq=np.rint(d*d).astype(int)
 if max(abs(d*d-sq))>1e-7:return None
 n=len(N)
 for i in range(n):
  for j in range(n):
   a,b=radical(int(sq[i]*sq[j])); R=collections.Counter({b:a})
   for k in range(n):
    if N[i,j,k]:
     a,b=radical(int(sq[k])); R[b]-=int(N[i,j,k])*a
   if any(R.values()):return None
 return sq.tolist()

def main():
 all_summary={}; raw={}; graphs={}; start=time.time()
 for rank,count in [(11,182)]:
  path=common.SOURCE
  data=gzip.open(path,'rt').read(); rows=data.splitlines(); require(len(rows)==count)
  rings=[]; buckets=collections.defaultdict(list); exact_tests=0
  for index,line in enumerate(rows,1):
   N=np.array(json.loads(line.replace('{','[').replace('}',']')),dtype=np.int64); n=len(N)
   require(N.shape==(rank,rank,rank))
   require(set(N.ravel())<={0,1})
   require(np.array_equal(N[0],np.eye(n,dtype=int)) and np.array_equal(N[:,0,:],np.eye(n,dtype=int)))
   require(np.all(N[:,:,0].sum(0)==1) and np.all(N[:,:,0].sum(1)==1))
   dual=np.argmax(N[:,:,0],axis=1)
   require(all(dual[dual[i]]==i for i in range(n)))
   # Associativity and the two Frobenius reciprocity identities, all integral.
   require(np.array_equal(np.einsum('ijx,xkl->ijkl',N,N),np.einsum('jkx,ixl->ijkl',N,N)))
   for i,j,k in itertools.product(range(n),repeat=3):
    require(N[i,j,k]==N[dual[i],k,j]==N[k,dual[j],i])
    require(N[i,j,k]==N[dual[j],dual[i],dual[k]])
   A=N.sum(0); require(np.array_equal(A,A.T))
   w,V=np.linalg.eigh(A); d=V[:,-1]/V[0,-1]; require(min(d)>0)
   require(max(np.max(np.abs(N[i]@d-d[i]*d)) for i in range(n))<1e-8)
   inv=[i for i in range(n) if N[i,dual[i]].sum()==1]
   subs=subrings(N,dual)
   key,sigs=refinement(N)
   for old in buckets[key]:
    G=graphs.setdefault((rank,index),graph(N,sigs)); H=graphs[(rank,old)]
    match=nx.algorithms.isomorphism.MultiDiGraphMatcher(G,H,node_match=nx.algorithms.isomorphism.categorical_node_match('color',None),edge_match=nx.algorithms.isomorphism.categorical_multiedge_match('role',None))
    exact_tests+=1
    require(not match.is_isomorphic(),f'Duplicate rank {rank}: {old}, {index}')
   if (rank,index) not in graphs: graphs[(rank,index)]=graph(N,sigs)
   buckets[key].append(index)
   entry={'id':f'R{rank}_1_{index}','line':index,'dual':dual.tolist(),'commutative':bool(np.array_equal(N,N.swapaxes(0,1))),'invertible_indices':inv,'invertible_rank':len(inv),'fp_dimensions_approx':d.tolist(),'fp_dimension_approx':float(d@d),'squared_fp_dimensions_exact':radical_dimension_certificate(N,d),'fusion_subrings':subs,'simple':len(subs)==2,'tensor_sha256_uint8_flattened':hashlib.sha256(N.astype('uint8').tobytes()).hexdigest(),'tensor_sha256_compact_json':common.sha(N.tolist())}
   rings.append(entry);raw[entry['id']]=N.tolist()
  summary={'rank':rank,'count':count,'all_fusion_axioms_pass':True,'exact_pairwise_nonisomorphic':True,'distinct_refinement_classes':len(buckets),'exact_graph_isomorphism_tests':exact_tests,'commutative':sum(x['commutative'] for x in rings),'noncommutative':sum(not x['commutative'] for x in rings),'pointed':sum(x['invertible_rank']==rank for x in rings),'simple':sum(x['simple'] for x in rings),'invertible_rank_distribution':dict(sorted(collections.Counter(x['invertible_rank'] for x in rings).items())),'weakly_integral_exact_certificates':sum(x['squared_fp_dimensions_exact'] is not None for x in rings),'table_uncompressed_sha256':hashlib.sha256(data.encode()).hexdigest(),'rings':rings}
  all_summary[str(rank)]=summary
  print(json.dumps({k:v for k,v in summary.items() if k!='rings'}),flush=True)
 (OUT/'profile.json').write_text(json.dumps(all_summary,indent=2)+'\n')
 (OUT/'tensors.json').write_text(json.dumps(raw,separators=(',',':'))+'\n')
 print('Elapsed',time.time()-start,flush=True)
if __name__=='__main__':main()
