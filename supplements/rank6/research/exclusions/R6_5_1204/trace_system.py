from pathlib import Path
import json,sys
import numpy as np
PROOF=Path(__file__).resolve().parent
P=PROOF.parents[2]
sys.path.insert(0,str(P/'software'))
import round3_m4 as M
from spectral_induction import Spectrum
from dimension_block_support import restriction_order_bounds
class System:
 def __init__(self,height=6,R=None):
  self.height=height
  if R is None:R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_5_1204')
  self.r=json.load(open(P/'research/round5/m5_1204/remaining_profiles.json'))
  self.rem=set(json.load(open(Path(__file__).with_name('forced_W.json')))['remaining_profiles'])
  self.cases={x['profile_index']:x for x in self.r['profiles']}
  inherited=json.load(open(P/'research/round5/m5_1204/profile_certificate.json'))
  if [x['profile_index'] for x in self.r['profiles']]!=inherited['remaining_profile_indices']:raise ValueError('Inherited frontier identifier mismatch')
  d=M.data_for(R,height,24);self.d=d;C=d['C'];self.V=list(map(tuple,self.r['high_columns']));cols=d['lows'][21]
  if list(map(list,cols))!=self.r['low_columns']:raise ValueError('Inherited low frame mismatch')
  assignments=d['tab'].assignments(cols);lab=assignments[0]
  if M.indicator_choices(R)!=[(1,1,1,1,1)]:raise ValueError('Uncovered indicator branch')
  # Every labelling is obtained by permuting equal restriction columns.
  # All moment equations use every unordered pair of nonunit low simples.
  for alternative in assignments:
   permutation=[lab.index(character) for character in alternative]
   if permutation[0]!=0 or any(cols[i]!=cols[j] for i,j in enumerate(permutation)):raise ValueError('Inequivalent low character assignment')
  union=set(i for x in self.r['profiles'] if x['profile_index'] in self.rem for i,n in x['multiplicities'])
  allowed=[self.V[i] for i in sorted(union)];self.allowed=allowed
  G,_=M.high_vectors(d,cols);sp=Spectrum(d['tab'],cols,[(v,None) for v in allowed]);d['_branch_cache']={tuple(map(tuple,cols)):(G,allowed,sp)}
  self.A,self.b,self.meta=M.system(R,d,cols,[1]*5,lab)
  if self.meta['vectors']!=len(allowed):raise ValueError('Spectrum unexpectedly pruned allowed columns')
  if self.meta['variables']!=len(self.A[0]):raise ValueError('System variable metadata mismatch')
  self.nt=len(d['phases']);self.nh=len(allowed)*self.nt
  support=restriction_order_bounds(d,[[0]+list(v) for v in allowed]);self.restricted=[x['order_bound']==12 for x in support['columns']]
  roots=[tuple(C.unit**((2*k*h)%24) for h in range(1,height+1)) for k in range(12)]
  self.phaseids=[d['phases'].index(t) for t in roots];self.vix={v:i for i,v in enumerate(self.V)}
 def profile(self,pi):
  counts=dict(self.cases[pi]['multiplicities']);nt=self.nt;nh=self.nh
  keep=[j for i,v in enumerate(self.allowed) if counts.get(self.vix[v],0) for j in range(i*nt,(i+1)*nt) if not self.restricted[i] or j%nt in self.phaseids]+list(range(nh,len(self.A[0])))
  A=[[r[j] for j in keep] for r in self.A];b=self.b[:]
  for vi,v in enumerate(self.allowed):
   n=counts.get(self.vix[v],0)
   if n:A.append([int(j<nh and j//nt==vi) for j in keep]);b.append(n)
  labs=[(self.vix[self.allowed[j//nt]],j%nt) if j<nh else ('rotation',j-nh) for j in keep]
  nz=[i for i,r in enumerate(A) if any(r) or b[i]]
  return [A[i] for i in nz],[b[i] for i in nz],labs
