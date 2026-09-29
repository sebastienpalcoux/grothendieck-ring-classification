"""Discovery of rank-twelve commutative cyclic two-orbit ring obstructions."""
import itertools,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(P/'software'))
from rings import codegree_factors,dnumber
from exact import poly,norm_failure,pc

def compositions(total,n):
 if n==1:
  yield (total,)
  return
 for k in range(total+1):
  for tail in compositions(total-k,n-1):yield (k,)+tail

def tensor(u,a):
 R=[[[0]*12 for _ in range(12)] for _ in range(12)]
 for i,j in itertools.product(range(12),repeat=2):
  k=(i%6+j%6)%6
  if i<6 and j<6:R[i][j][k]=1
  elif i<6 or j<6:R[i][j][6+k]=1
  else:
   R[i][j][(k+u)%6]=1
   for h,c in enumerate(a):R[i][j][6+(k+h)%6]=c
 return R

def run():
 pD=poly([1,-120,720]);out=[]
 for u,a in itertools.product(range(6),compositions(4,6)):
  if any(a[k]!=a[(u-k)%6] for k in range(6)):continue
  R=tensor(u,a);cf=codegree_factors(R)
  reason=dnumber(R) or norm_failure(pD,cf)
  row={'u':u,'a':a,'codegree_factors':[[pc(q),m] for q,m in cf],'obstruction':reason}
  out.append(row)
 print('total',len(out),'excluded',sum(r['obstruction'] is not None for r in out))
 print('survivors',[(r['u'],r['a']) for r in out if r['obstruction'] is None])
 (Path(__file__).with_suffix('.json')).write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run()
