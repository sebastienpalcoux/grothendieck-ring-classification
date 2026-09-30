"""Exact 24th-root equations for the remaining 277 spin-centralizer."""
def require(ok,msg):
 if not ok:raise ValueError(msg)
from itertools import product
from collections import Counter
# Z[t]/(t^8-t^4+1), t=zeta24. All coefficient arithmetic integral.
def add(*vs):return tuple(sum(v[i]for v in vs)for i in range(8))
def scale(v,n):return tuple(n*x for x in v)
def mul(a,b):
 c=[0]*15
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 for k in range(14,7,-1):c[k-4]+=c[k];c[k-8]-=c[k]
 return tuple(c[:8])
one=(1,0,0,0,0,0,0,0);z=(0,1,0,0,0,0,0,0);r=[one]
for k in range(1,24):r.append(mul(r[-1],z))
zero=(0,)*8
require(mul(r[-1],z)==one,'24th root relation')
pair={}
for b in range(24):
 for c in range(b,24):
  sm=add(r[b],r[c]);cb=add(r[3*b%24],r[3*c%24])
  if sm in pair:require(pair[sm][0]==cb,'pair cubic sum not determined')
  pair[sm]=(cb,(b,c))
sol=[]
for a,d,e in product(range(24),repeat=3):
 target=add(scale(r[21],-6),scale(r[a],-1),scale(r[d],-2),scale(r[e],-4))
 if target not in pair:continue
 cb,(b,c)=pair[target]
 cube=add(r[3*a%24],cb,scale(r[3*d%24],2),scale(r[3*e%24],4))
 sol.append(dict(alpha=a,beta=b,gamma=c,delta=d,epsilon=e,cubic_sum=list(cube),cubic_zero=cube==zero))
require(sol and not any(q['cubic_zero']for q in sol),'unexpected cubic-zero solution')
import json,argparse
from pathlib import Path
out=dict(modulus='t^8-t^4+1',roots=24,gauss_solutions=len(sol),cubic_zero_solutions=0,solutions=sol)
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verify',action='store_true',help='verify without writing a receipt')
parser.add_argument('--output',type=Path)
args=parser.parse_args()
target=args.output or (None if args.verify else Path(__file__).with_suffix('.json'))
if target:target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items()if k!='solutions'},indent=2))
