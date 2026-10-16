"""Discovery only: full T1-support, torus and compressed-S constraints."""
from pathlib import Path
import os,sys,json,time,signal,pickle
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
BASE=Path(__file__).resolve().parents[3]
P=BASE/'repo/supplements/rank6'
sys.path.insert(0,str(P/'research/round5/m8_actual48'))
sys.path.insert(0,str(P/'research/round5/m8_modrep'))
import actual48 as Q
import ising_complement as IC
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('bounded discovery')))
signal.alarm(360)
start=time.time()
R=next(x['N'] for x in json.loads((P/'data/census.json').read_text()) if x['id']=='R6_8_1660')
d=Q.prepare(R)
old=json.loads((P/'research/round5/m8_actual48/certificate.json').read_text())
torus=json.loads((Path(__file__).parent/'torus_spectra.json').read_text())
compression=json.loads((Path(__file__).parent.parent/'modrep_audit/compressed_spectra.json').read_text())
results=[]
for branch in old['branches']:
 if branch['outcome']!='profile_frontier':continue
 A,b,meta=Q.build(R,d,branch['low'],branch['labelling'],branch['indicators'])
 oldnv=len(A[0]);nh=len(meta['high_labels'])
 branchc=next(r for r in compression['branches'] if r['low']==branch['low'] and r['labelling']==branch['labelling'])
 eligible={tuple(p) for p in branchc['eligible_irrep_pairs']}
 reps=[r for r in torus['irreps'] if r['allowed'] and (r['T0']==0 or tuple(r['factors']) in eligible)]
 nv=oldnv+len(reps)+48
 A=[row+[0]*(len(reps)+48) for row in A]
 for k in range(48):
  row=[0]*nv
  for j,(v,a) in enumerate(meta['high_labels']):
   if a==k:row[j]=1
  for j,r in enumerate(reps):row[oldnv+j]=-r['spectrum'][k]
  A.append(row);b.append(-6 if k==0 else 0)
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=r['central_sign']*r['spectrum'][k]
  row[oldnv+len(reps)+k]=-1
  A.append(row);b.append(6 if k==0 else 0)
 for h,target in enumerate(torus['target_weights']):
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=r['torus_weights'][h]
  A.append(row);b.append(target)
 assert len(branchc['decompositions'])==1
 decomposition=branchc['decompositions'][0]
 for h,spectype in enumerate(branchc['eligible_spectrum_types']):
  row=[0]*nv
  for j,r in enumerate(reps):row[oldnv+j]=int(r['factors'] in spectype['pairs'])
  A.append(row);b.append(decomposition.count(h))
 bounds=[(0,None)]*nv
 # The forced Ising-center subrepresentation decomposes as 1+2+6.
 for pair in ([3,2],[9,2],[57,2]):
  j=next(j for j,r in enumerate(reps) if r['factors']==pair)
  bounds[oldnv+j]=(1,None)
 forbidden=[j for j,(v,a) in enumerate(meta['high_labels']) if a==0]
 for j in forbidden:bounds[j]=(0,0)
 cache=Path(__file__).parent/f"compressed_{branch['low']}_{branch['labelling'][-2]}.pickle"
 with cache.open('wb') as file:pickle.dump((A,b,meta,reps,bounds),file)
 AA=np.asarray(A,dtype=float);bb=np.asarray(b,dtype=float)
 scale=np.maximum(np.max(np.abs(AA),axis=1),np.abs(bb));scale[scale==0]=1
 AA=csr_matrix(AA/scale[:,None]);bb=bb/scale
 print(json.dumps({'phase':'built','low':branch['low'],'labelling':branch['labelling'],'shape':AA.shape,'forbidden_high_T1':len(forbidden),'seconds':time.time()-start}),flush=True)
 res=linprog(np.zeros(nv),A_eq=AA,b_eq=bb,bounds=bounds,method='highs',options={'time_limit':30})
 row={'low':branch['low'],'labelling':branch['labelling'],'status':int(res.status),'message':res.message,'forbidden_high_T1':len(forbidden)}
 if res.success:
  row['max_equality_residual']=float(np.max(np.abs(AA@res.x-bb)))
  row['solution_support']=[[int(j),float(v)] for j,v in enumerate(res.x) if abs(v)>1e-8]
 results.append(row)
 (Path(__file__).parent/'compressed_discovery.json').write_text(json.dumps({'scope':'discovery_only_no_exclusion_or_feasibility_claim','results':results},indent=2)+'\n')
 print(json.dumps({k:v for k,v in row.items() if k!='solution_support'}),flush=True)
print('Finished',time.time()-start,flush=True)
