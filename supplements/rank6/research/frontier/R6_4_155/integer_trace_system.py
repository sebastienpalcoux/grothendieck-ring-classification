"""Exact necessary trace-count system for the inherited R155 center frontier.
No optimizer is called. Every original variable counts actual simples or
rotation eigenvalues; certificate slack variables are only nonnegative.
"""
from pathlib import Path
import json,sys
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round3_m4 as M
from spectral_induction import Spectrum
from round5_155 import verify_labelling_quotient

class System:
 def __init__(self,height=6,F=24):
  if height!=6 or F!=24:raise ValueError("Expected height6 and ambient conductor24")
  self.height=height
  R=next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id']=='R6_4_155');self.R=R
  self.cert=json.load(open(P/'research/round5/m4_155/frontier_certificate.json'))
  self.rem=json.load(open(P/'research/round5/m4_155/packet_frontier.json'))['remaining_profiles']
  d=M.data_for(R,height,F);self.d=d;C=d['C'];self.V=list(map(tuple,self.cert['high_columns']));cols=d['lows'][6];self.cols=cols
  expected_cols=((1,0,0,0,0,0),(1,2,2,0,0,0),(1,2,2,1,0,0),(1,2,2,1,0,0),(1,1,1,0,0,0),(1,1,1,0,0,0))
  if tuple(map(tuple,cols))!=expected_cols:raise ValueError('Inherited low frame changed')
  if self.rem!=[275,277,279,296,298,306]:raise ValueError('Inherited six-profile domain changed')
  labs=d['tab'].assignments(cols);self.labelling_permutations=verify_labelling_quotient(cols,labs)
  if len(labs)!=4:raise ValueError('Inherited character assignment domain changed')
  lab=labs[0]
  union=[i for i in range(len(self.V)) if any(self.cert['profiles'][pi][i] for pi in self.rem)]
  allowed=[self.V[i] for i in union];self.allowed=allowed
  G,_=M.high_vectors(d,cols);sp=Spectrum(d['tab'],cols,[(v,None) for v in allowed]);d['_branch_cache']={tuple(map(tuple,cols)):(G,allowed,sp)}
  self.A,self.b,self.meta=M.system(R,d,cols,[0,0,1,-1,-1],lab)
  if self.meta['vectors']!=len(allowed):raise ValueError('Spectrum pruned allowed columns')
  if self.meta['variables']!=len(self.A[0]):raise ValueError('System variable metadata mismatch')
  self.nt=len(d['phases']);self.nh=len(allowed)*self.nt;self.vix={v:i for i,v in enumerate(self.V)}
  invs=[(3,1),(4,-1),(5,-1)];self.pointed_phases={}
  for g,ep in invs:
   roots=[C.one,-C.one] if ep==1 else [C.unit**(F//4),-C.unit**(F//4)]
   self.pointed_phases[g]={d['phases'].index(tuple(z**k for k in range(1,height+1))) for z in roots}
 def profile(self,pi):
  if pi not in self.rem:raise ValueError("Profile outside inherited frontier")
  counts=self.cert['profiles'][pi];nt=self.nt;nh=self.nh
  keep=[j for i,v in enumerate(self.allowed) if counts[self.vix[v]] for j in range(i*nt,(i+1)*nt) if all(not v[g-1] or j%nt in ids for g,ids in self.pointed_phases.items())]+list(range(nh,len(self.A[0])))
  A=[[r[j] for j in keep] for r in self.A];b=self.b[:]
  for vi,v in enumerate(self.allowed):
   n=counts[self.vix[v]]
   if n:A.append([int(j<nh and j//nt==vi) for j in keep]);b.append(n)
  labs=[(self.vix[self.allowed[j//nt]],j%nt) if j<nh else ('rotation',j-nh) for j in keep]
  nz=[i for i,r in enumerate(A) if any(r) or b[i]]
  return [A[i] for i in nz],[b[i] for i in nz],labs
