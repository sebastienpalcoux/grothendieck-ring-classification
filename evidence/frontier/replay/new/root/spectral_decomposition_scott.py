"""Necessary constituent tests for matrix triples with product identity.
A passing leaf is only a necessary-test survivor, never a constructed matrix.
"""
from pathlib import Path
import json,itertools,functools,collections,time
P=Path(__file__).parent
src=json.load(open(P/'pure_braid_peeling_receipt.json'))
def canon(rows):return tuple(sorted(tuple(sorted((int(e),int(m)) for e,m in row if m)) for row in rows))
def necessary(key):
 n=sum(m for e,m in key[0])
 if sum(e*m for row in key for e,m in row)%24:return False
 if n==1:return True
 # Scott centralizer dimension and rank inequalities, for an irreducible triple.
 if sum(m*m for row in key for e,m in row)>n*n+2:return False
 mx=[max(m for e,m in row) for row in key]
 if any(mx[i]+mx[j]>n for i,j in [(0,1),(0,2),(1,2)]):return False
 return True
@functools.lru_cache(None)
def selections(row,k):
 out=[]
 for mm in itertools.product(*(range(min(m,k)+1) for e,m in row)):
  if sum(mm)==k:
   a=tuple((e,m) for (e,_),m in zip(row,mm) if m)
   b=tuple((e,m-v) for (e,m),v in zip(row,mm) if m-v)
   out.append((a,b,sum(e*m for e,m in a)%24))
 return out
nodes=0
@functools.lru_cache(None)
def solve(key):
 global nodes
 nodes+=1
 if nodes>150000:raise RuntimeError('short-search budget reached; no exclusion licensed')
 n=sum(m for e,m in key[0]); assert all(sum(m for e,m in row)==n for row in key)
 if necessary(key):return [key]
 if n<=1:return None
 for k in range(1,n//2+1):
  rows=[selections(row,k) for row in key]
  thirds=collections.defaultdict(list)
  for q in rows[2]:thirds[q[2]].append(q)
  for a,b in itertools.product(rows[0],rows[1]):
   for c in thirds[(-a[2]-b[2])%24]:
    first=solve(canon((a[0],b[0],c[0])))
    if first is None:continue
    second=solve(canon((a[1],b[1],c[1])))
    if second is not None:return first+second
 return None
out=[];start=time.time()
for p in src['remaining_Scott_reducible_profiles']:
 key=canon(p['spectrum']); ans=solve(key)
 out.append({'case':p['case'],'dimension':p['n'],'necessary_block_partition':ans,'excluded_by_test':ans is None})
receipt={'scope':'necessary irreducible-constituent tests, passing leaves not proved realizable','profiles':out,'failures':[p for p in out if p['excluded_by_test']],'memo_nodes':nodes,'elapsed_seconds':time.time()-start}
(P/'spectral_decomposition_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='profiles'},indent=2))
