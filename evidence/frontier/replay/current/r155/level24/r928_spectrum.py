#!/usr/bin/env python3
"""Small spectrum decomposition using previously verified level-8/3 tables."""
from pathlib import Path
import json,time,hashlib
HERE=Path(__file__).resolve().parent
tables=[json.loads((HERE/f'sl2_{q}.json').read_text()) for q in [8,3]]
allreps=[]
for i,A in enumerate(tables[0]['irreps']):
 for j,B in enumerate(tables[1]['irreps']):
  T=[0]*24
  for k,x in enumerate(A['T_multiplicities']):
   for l,y in enumerate(B['T_multiplicities']):T[(3*k+8*l)%24]+=x*y
  allreps.append(dict(indices=[i,j],degree=A['degree']*B['degree'],central_sign=A['central_sign']*B['central_sign'],T=T))
results=[]
for pattern,m in [(186,1),(40,4)]:
 target={23:2,15:2,3:2,11:1,20:1,9:2,17:1,12:m}
 tar=[target.get(i,0) for i in range(24)]
 reps=[r for r in allreps if all(a<=b for a,b in zip(r['T'],tar))]
 support=[sum(bool(r['T'][k]) for r in reps) for k in range(24)]
 reps.sort(key=lambda r:(min(support[k] for k,v in enumerate(r['T']) if v),-r['degree']))
 n=len(reps);suffix=[set() for _ in range(n+1)]
 for k in reversed(range(n)):suffix[k]=suffix[k+1]|{e for e,v in enumerate(reps[k]['T']) if v}
 sols=[];mult=[0]*n;nodes=0
 def rec(k,rem):
  global nodes
  nodes+=1
  if not any(rem):
   sols.append([dict(multiplicity=mult[j],**reps[j]) for j in range(k) if mult[j]])
   return
  if k==n or any(v and e not in suffix[k] for e,v in enumerate(rem)):return
  r=reps[k]['T'];bd=min(rem[e]//v for e,v in enumerate(r) if v)
  for a in range(bd+1):
   mult[k]=a;rec(k+1,[v-a*w for v,w in zip(rem,r)])
 rec(0,tar)
 results.append(dict(pattern=pattern,rank=sum(tar),target=target,compatible_irreps=len(reps),solutions=sols,nodes=nodes))
 print(pattern,'rank',sum(tar),'irreps',len(reps),'solutions',len(sols),'nodes',nodes)
 print([[([*r['indices']],r['multiplicity'],r['degree'],r['central_sign']) for r in z] for z in sols][:30])
out=dict(scope='Conditional level-24 complementary representations; not modular data or categories.',inputs={str(q):hashlib.sha256((HERE/f'sl2_{q}.json').read_bytes()).hexdigest() for q in [8,3]},results=results)
(HERE/'r928_spectrum.json').write_text(json.dumps(out,indent=2)+'\n')
