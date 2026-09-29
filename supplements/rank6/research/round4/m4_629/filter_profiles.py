import sys,json,math,itertools,time,hashlib
from fractions import Fraction
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as m
from spectral_induction import Spectrum
from exact import require
st=time.monotonic();here=Path(__file__).parent;R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');saved=json.load(open(here/'enumerate_gram.json'));V=saved['vs'];counts=[json.loads(l) for l in open(here/'profiles_counts.jsonl')];require(json.load(open(here/'profiles_summary.json'))['complete'],'incomplete input profiles');require(len(counts)==len({tuple(x) for x in counts}),'duplicate profiles');require(all(all(x>=0 for x in c) and all(sum(a*z for a,z in zip(row,c))==rhs for row,rhs in zip(saved['A'],saved['b'])) for c in counts),'bad input profile')
d=m.data_for(R,3,15);cols=d['lows'][3];tab=d['tab'];C=d['C'];sp=Spectrum(tab,cols,[(tuple(v),None) for v in V]);types=dict(zip(sp.vectors,sp.types));vecs=list(map(tuple,cols))+[(0,)+tuple(v) for v in V];lab=tab.assignments(cols)[0];weights={():[tab.dims[v]**2/tab.D**2 for v in vecs]};indices=list(range(len(counts)));X=np.array(counts,dtype=np.int64);out={'id':'R6_4_629','complete_input_profiles':len(counts),'low_frame':3,'lab':lab,'depths':[]};fail={}
for k in range(1,7):
 for word in itertools.combinations_with_replacement(range(1,6),k):
  w=[z*types[v][lab[word[-1]]] for v,z in zip(vecs,weights[word[:-1]])];weights[word]=w
  if k<3:continue
  const=sum(w[:6],C.zero);ww=[const]+w[6:];cc=[[Fraction(str(a)) for a in reversed(z.to_list())]+[Fraction(0)]*(8-len(z.to_list())) for z in ww]
  for j in range(8):
   co=[r[j] for r in cc];den=math.lcm(*(z.denominator for z in co));nums=[int(z*den) for z in co]
   if not any(nums):continue
   bound=abs(nums[0])+sum(abs(a)*max((c[i] for c in counts),default=0) for i,a in enumerate(nums[1:]));require(bound<2**62,'int64 bound exceeded')
   vals=X@np.array(nums[1:],dtype=np.int64)+nums[0]
   good=(vals>=0)&(vals%den==0) if j==0 else (vals==0)
   for q,g in enumerate(good):
    if not g:fail[indices[q]]={'word':word,'coordinate':j,'numerator':int(vals[q]),'denominator':den}
   indices=[i for i,g in zip(indices,good) if g];X=X[good]
  if not indices:break
 rec={'degree':k,'survivors':len(indices),'rank_distribution':{str(r):sum(6+sum(counts[i])==r for i in indices) for r in sorted({6+sum(counts[i]) for i in indices})}};out['depths'].append(rec);print(rec,flush=True)
 if not indices:break
out.update(surviving_indices=indices,counts=[counts[i] for i in indices],vectors=V,rejected=fail,seconds=time.monotonic()-st,source_sha256=hashlib.sha256((here/'profiles_counts.jsonl').read_bytes()).hexdigest());(here/'filtered_profiles.json').write_text(json.dumps(out));print('seconds',out['seconds'],flush=True)
