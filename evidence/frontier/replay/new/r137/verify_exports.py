"""Standard-library arithmetic replay of both frozen strengthened systems.
Checks inherited rows, exact witnesses, the residual-Gram cuts, and all12 new
rows from exported exact column metadata. Character/phase applicability is
proved in REPORT and source metadata reconstruction is in the builder.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,gzip,hashlib,itertools,math
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[1]/'prior/evidence/unresolved7_20261027/audit_parity'
G=[[9,1,3,8,8,8,8,3,0],[1,9,3,8,8,8,8,3,0],[3,3,9,8,8,8,8,1,0],[8,8,8,76,64,64,68,8,16],[8,8,8,64,76,68,64,8,16],[8,8,8,64,68,76,64,8,16],[8,8,8,68,64,64,76,8,16],[3,3,1,8,8,8,8,9,0],[0,0,0,16,16,16,16,0,16]]
vB=[1,0,0,1,1,1,1,0,0]
H=[[Q(G[i][j]-int(i==j==0)-vB[i]*vB[j])for j in range(9)]for i in range(9)]
def inverse(M):
 a=[row[:]+[Q(i==j)for j in range(len(M))]for i,row in enumerate(M)];n=len(M)
 for i in range(n):
  k=next(k for k in range(i,n)if a[k][i]);a[i],a[k]=a[k],a[i]
  c=a[i][i];a[i]=[x/c for x in a[i]]
  for k in range(n):
   if k!=i:
    c=a[k][i];a[k]=[x-c*y for x,y in zip(a[k],a[i])]
 return [row[n:]for row in a]
J=inverse(H)
pairs=list(itertools.combinations_with_replacement(range(9),2))
for sign in ['plus','minus']:
 oldbytes=(PRIOR/f'R137_tau_{sign}_positive_fs2_system.json.gz').read_bytes();old=json.loads(gzip.decompress(oldbytes))
 x=json.loads(gzip.decompress((HERE/f'R137_tau_{sign}_forced_galois_replay.json.gz').read_bytes()));A=x['A'];b=x['b'];n=len(old['A'][0]);m=len(old['A'])
 assert hashlib.sha256(oldbytes).hexdigest()==x['source_sha256']
 assert len(A)==m+12 and all(row[:n]==p for row,p in zip(A[:m],old['A']))
 assert b[:m]==old['b'] and all(not any(row[n:])for row in A[:m])
 rows=[[Q(0)]*n for _ in range(4)];removed=[];covered=set()
 for j,v,k,norm,tt in x['physical_mapping']:
  assert j not in covered;covered.add(j)
  assert all(Q(old['A'][r][j]*G[i][h],old['b'][r])==v[i]*v[h] for r,(i,h)in enumerate(pairs)if old['b'][r])
  assert Q(norm)==sum(v[i]*J[i][h]*v[h]for i,h in itertools.product(range(9),repeat=2))
  z=(sum(v[i]for i in [0,1,2,7])+2*v[8]+4*sum(v[i]for i in [3,4,5,6]),3*sum(v[i]for i in [3,4,5,6]))
  t=tuple(map(Q,tt[3]));val=z[0]*t[1]+z[1]*t[0]
  for r,i in enumerate([3,4,5,6]):rows[r][j]=v[i]*val
  if not v[0] and k*Q(norm)>1:removed.append(j)
  if v[0] and z==(17,12) and v!=vB:removed.append(j)
 assert covered=={j for j in range(n)if any(old['A'][r][j]for r in range(45))}
 assert removed==x['removed_columns']
 for r,row in enumerate(rows):
  for h,sg in enumerate([1,-1]):
   actual=A[m+2*r+h];target=[4*sg*v for v in row]+[Q(i==2*r+h)for i in range(8)]
   assert actual==target and b[m+2*r+h]==1536
  assert A[m+8+r]==[int(j==n+2*r)for j in range(n+8)] and b[m+8+r]==768
 witness={int(j):Q(v)for j,v in x['witness']}
 assert len(witness)==len(x['witness']) and all(v>=0 for v in witness.values())
 assert not(set(witness)&set(removed))
 assert all(sum(row[j]*v for j,v in witness.items())==rhs for row,rhs in zip(A,b))
 print(json.dumps({'TY_sign':sign,'status':'EXACT_PASS','inherited_equations':m,'new_equations':12,'removed_columns':len(removed),'exact_witness_support':len(witness)}))
