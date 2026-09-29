import sys,json,time,math
from pathlib import Path
from fractions import Fraction
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize as op
def disabled(*a,**k):raise RuntimeError('numerical optimizers disabled')
op.linprog=op.milp=disabled
from round4_629_orbits import *
from exact import require
here=Path(__file__).parent;st=time.monotonic();R=next(x['N'] for x in json.load(open(P/'data/unresolved_tensors.json')) if x['id']=='R6_4_629');src=json.load(open(here/'filtered_profiles.json'));data=ambient.data_for(R,6,15);cols=data['lows'][3];vs=list(map(tuple,src['vectors']));G,V=ambient.high_vectors(data,cols);sp=Spectrum(data['tab'],cols,[(v,None) for v in V]);V=[v for v in V if list(v) not in sp.forbidden];require(V==vs,'incorrect high-column universe');labels=[(v,ti) for v in vs for ti in range(len(data['phases']))];nh=len(labels);reports=[]
for fn in ['fixed_twist_h6.json','fixed_twist_h6_lab1.json']:
 r=json.load(open(here/fn));require(r['source_profiles']==src['surviving_indices'],'omitted profile');require(tuple(r['lab']) in data['tab'].assignments(cols),'invalid low labelling');A,b,meta=ambient.system(R,data,cols,r['ep'],r['lab']);labreport={'file':fn,'lab':r['lab'],'profiles':[]}
 for br,counts in zip(r['branches'],src['counts']):
  require(br['profile']==src['surviving_indices'][len(labreport['profiles'])],'profile order changed');domains={B:orbit_domain(data,B) for B in set(counts) if B};ct=dict(zip(vs,counts));keep=[]
  for j in range(len(A[0])):
   if j>=nh:keep.append((j,1))
   else:
    v,ti=labels[j]
    if ct[v]:keep.extend((j,e) for e in domains[ct[v]].get(ti,[]))
  require(list(map(list,keep))==br['columns'],'wrong exhaustive orbit-size domain');AA=[[row[j]*e for j,e in keep] for row in A];bb=b[:]
  for v,cc in zip(vs,counts):
   if cc:AA.append([int(j<nh and labels[j][0]==v)*e for j,e in keep]);bb.append(cc)
  require(len(AA)==br['rows'] and len(keep)==br['variables'],'incorrect system size');rr={'profile':br['profile'],'rank':br['rank'],'rows':len(AA),'variables':len(keep),'outcome':br['outcome']}
  if br['outcome']=='exact_linear_obstruction':
   y=br['ray'];require(len(y)==len(bb) and all(type(z) is int for z in y),'invalid ray');sy=[(i,z) for i,z in enumerate(y) if z];require(sum(bb[i]*z for i,z in sy)<0 and all(sum(AA[i][j]*z for i,z in sy)>=0 for j in range(len(keep))),'exact Farkas inequality failed');rr['passed']=True
  elif br['outcome']=='exact_necessary_witness':
   x=br['primal'];require(len(x)==len(keep) and all(type(z) is int and z>=0 for z in x),'invalid integer primal');sx=[(i,z) for i,z in enumerate(x) if z];require(all(sum(row[i]*z for i,z in sx)==rhs for row,rhs in zip(AA,bb)),'exact primal equation failed');rr['passed']=True
  else:rr['passed']=None;rr['scope']='no exact conclusion'
  labreport['profiles'].append(rr);print(rr,flush=True)
 reports.append(labreport)
out={'passed':True,'optimizer_used':False,'optimized_python':not __debug__,'reports':reports,'seconds':time.monotonic()-st};(here/'fixed_twist_exact_replay_O.json' if not __debug__ else here/'fixed_twist_exact_replay.json').write_text(json.dumps(out));print('completed',out['seconds'],flush=True)
