"""Small meet-in-the-middle: singleton square-Galois orbits, total mass <=9."""
from itertools import combinations_with_replacement
from collections import defaultdict,Counter
import json
from pathlib import Path
def root(k):
 k%=24;p=[0]*24;p[k]=1
 for i in range(23,7,-1):
  a=p[i];p[i]=0;p[i-4]+=a;p[i-8]-=a
 return tuple(p[:8])
rt=[root(k) for k in range(24)]
def add(*xs):return tuple(map(sum,zip(*xs))) if xs else (0,)*8
def sc(c,x):return tuple(c*a for a in x)
def root_sum(tup):return add(*(rt[k] for k in tup))
targets={t:add(sc(-1,rt[0]),sc(-2,rt[t//6]),sc(-2,rt[5]),sc(-2,rt[1])) for t in [60,84,96]}
# sqrt3*xi=(zeta24^2+zeta24^-2)*zeta24^3=zeta24^5+zeta24.
left=defaultdict(list)
for n in range(5):
 for tup in combinations_with_replacement(range(24),n):left[root_sum(tup)].append(tup)
out={t:set() for t in targets}
for n in range(6):
 for tup in combinations_with_replacement(range(24),n):
  z=root_sum(tup)
  for t,v in targets.items():
   for other in left.get(add(v,sc(-1,z)),[]):
    out[t].add(tuple(sorted(tup+other)))
print({t:dict(Counter(map(len,vs))) for t,vs in out.items()})
Path(__file__).resolve().with_suffix('.json').write_text(json.dumps({str(t):[list(v) for v in sorted(vs,key=lambda a:(len(a),a))] for t,vs in out.items()},indent=2)+'\n')
