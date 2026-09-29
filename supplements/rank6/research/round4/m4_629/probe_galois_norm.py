import json,sys,time,collections,math
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as m
from spectral_induction import Spectrum
from exact import evaluate,key
here=Path(__file__).parent;R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');src=json.load(open(here/'filtered_profiles.json'));data=m.data_for(R,3,15);tab=data['tab'];C=data['C'];cols=data['lows'][3];V=list(map(tuple,src['vectors']));sp=Spectrum(tab,cols,[(v,None) for v in V]);vectors=sp.vectors;signatures=[(tab.dims[v]**2/tab.D**2,)+tt for v,tt in zip(vectors,sp.types)];ix={sig:i for i,sig in enumerate(signatures)};autos=[a for a in range(15) if math.gcd(a,15)==1];trans={a:[tuple(evaluate(z.to_list(),C.unit**a,C) for z in sig) for sig in signatures] for a in autos};out=[]
for pi,c in zip(src['surviving_indices'],src['counts']):
 counts=[1]*6+c;base=collections.Counter()
 for sig,cc in zip(signatures,counts):base[sig]+=cc
 rec={'profile':pi,'rank':sum(counts),'passed':True}
 for a in autos:
  moved=collections.Counter()
  for sig,cc in zip(trans[a],counts):moved[sig]+=cc
  if moved!=base:
   bad=next(sig for sig in moved if moved[sig]!=base[sig]);rec.update(passed=False,automorphism=a,source_count=base[bad],conjugate_count=moved[bad],signature=[key(x) for x in bad]);break
 out.append(rec);print({k:v for k,v in rec.items() if k!='signature'},flush=True)
(here/'galois_norm_profiles.json').write_text(json.dumps(out))
