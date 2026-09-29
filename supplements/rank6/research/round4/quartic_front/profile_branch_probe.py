import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT/'software'),str(ROOT/'research/round3/quartic')]
from verlinde_probe import *
from fractions import Fraction
from scipy.optimize import linprog
import numpy as np
rid=sys.argv[1] if len(sys.argv)>1 else 'R6_4_91'
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);m.R=R;data=data_for(R,3);tab=table_for(R,data);cols=data['lows'][1];ep=(0,0,-1,1,1) if rid.endswith('_91') else (0,0,1,1,1);mod=forced_module_data(R);out=[]
for lab in tab.assignments(cols):
 A,b,meta,labels=system(R,data,cols,ep,mod['objects'],True);A,b,meta=stronger_system(data,tab,cols,lab,A,b,labels);A,b,n=coupled(data,tab,cols,A,b,labels);A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
 C=data['C'];one=tuple(C.one for _ in range(3));minus=tuple(C((-1)**k) for k in range(1,4));
 if rid.endswith('_91'):
  sigma_types={tuple(C.unit**(a*k%16) for k in range(1,4)) for a in [3,5,11,13]}
  def permitted(v,ti):return (not v[2] or data['phases'][ti] in sigma_types) and (not v[3] or data['phases'][ti]==minus)
 else:
  def permitted(v,ti):return not v[2] or data['phases'][ti] in (one,minus)
 keep=[j for j in range(len(A[0])) if j>=len(labels) or permitted(*labels[j])];A=[[row[j] for j in keep] for row in A]
 profiles=json.load(open(Path(__file__).with_name(rid+'_filtered_profiles.json')));selected=next(x['accepted'] for x in profiles if x['lab']==list(lab));V=json.load(open(Path(__file__).with_name(rid+'_count_space.json')))['vectors']
 for profile in [p for p in selected if p['profile_index']==64]:
  counts=dict(zip(map(tuple,V),profile['counts']));kk=[k for k,j in enumerate(keep) if j>=len(labels) or counts[tuple(labels[j][0])]];AK=[[row[k] for k in kk] for row in A];bk=list(b)
  for v,count in counts.items():
   if count:AK.append([int(keep[k]<len(labels) and tuple(labels[keep[k]][0])==v) for k in kk]);bk.append(count)
  print('start',rid,lab,'profile',profile['profile_index'],'rank',profile['rank'],len(AK),len(AK[0]),flush=True);aa=np.array(AK,dtype=float);bb=np.array(bk,dtype=float);scale=np.maximum(1,np.maximum(abs(aa).max(axis=1),abs(bb)));sol=linprog(np.zeros(len(AK[0])),A_eq=aa/scale[:,None],b_eq=bb/scale,bounds=(0,None),options={'time_limit':45},method='highs');print('LP',sol.status,flush=True)
  rec=dict(id=rid,lab=lab,profile_index=profile['profile_index'],rank=profile['rank'],status=sol.status,rows=len(AK),columns=len(AK[0]))
  if sol.status==2:
   y=farkas(AK,bk)
   if y is not None:check_farkas(AK,bk,y);rec['ray']=y
  elif sol.status==0:
   from integer_branch import discover,verify
   integer=[k for k,jj in enumerate(kk) if keep[jj]<len(labels) or keep[jj]>=base]
   branch=discover(AK,bk,integer);verify(AK,bk,integer,branch);rec['branch_certificate']=branch
  out.append(rec);Path(__file__).with_name(rid+'_profile_branch_probe.json').write_text(json.dumps(out,indent=2)+'\n')
