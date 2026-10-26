#!/usr/bin/env python3
"""Bounded higher-indicator probe. A feasible LP is not a category model."""
import sys,json,itertools,math,time
from pathlib import Path
from fractions import Fraction as Q
from types import SimpleNamespace
import sympy as s
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'grothendieck-revision/supplements/rank6/software'))
import higher_traces as ht
R=json.loads((ROOT/'rank12-m1-offline-20261025/tensors.json').read_text())['R12_1_350'];du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)];G=[0,1,2,5,8,10]
B=s.Matrix(12,12,lambda j,i:sum(R[a][j][k]*R[k][du[a]][i] for a in range(12) for k in range(12)))
D=(Q(120),Q(36));ds=[(Q(1),Q(0)) if i in G else (Q(3),Q(1)) for i in range(12)]
data={'ch':SimpleNamespace(n=12,C=B,du=du),'q':10,'conductor':40,'dimensions':ds,'global_dimension':D,'primes':[2,3,5]}
classes=[[1,2],[5,8,10],[3,4],[6,7,9],[11]]
def high_columns(data,L):
 Qm=(B-L*L.T).extract(range(1,12),range(1,12));rank=Qm.rank();ix=next(ii for ii in itertools.combinations(range(11),rank) if Qm.extract(ii,ii).det()!=0);sub=Qm.extract(ix,ix);inv=sub.inv();null=Qm.nullspace();cols=[]
 bounds=[math.isqrt(int(Qm[cl[0]-1,cl[0]-1])) for cl in classes]
 for v5 in itertools.product(*(range(x+1) for x in bounds)):
  if not any(v5):continue
  v=[0]*11
  for cl,k in zip(classes,v5):
   for j in cl:v[j-1]=k
  if any(v[i]*v[j]>Qm[i,j] for i in range(11) for j in range(i,11)):continue
  if any(sum(v[i]*w[i] for i in range(11)) for w in null):continue
  vi=s.Matrix([v[i] for i in ix])
  if (vi.T*inv*vi)[0]>1:continue
  z=tuple(sum((v[i]*ds[i+1][k] for i in range(11)),Q(0)) for k in range(2));norm=z[0]**2-10*z[1]**2
  if not norm:continue
  quotient=((D[0]*z[0]-10*D[1]*z[1])/norm,(D[1]*z[0]-D[0]*z[1])/norm)
  if not ht.integer_pair(quotient,10):continue
  if z[1] and ((2*z[0])**2/norm).denominator!=1:continue
  cols.append((tuple(v),z))
 return Qm,cols
ht.high_columns=high_columns
recs=json.loads((OUT/'R350_induction_low_exact.json').read_text())['branches'];survivors=[r for r in recs if r['psd']]
def vec(a,u):
 v=[0]*12;v[0]=u
 for cl,k in zip(classes[2:],a):
  for j in cl:v[j]=k
 return s.Matrix(v)
out=[]
for bi,rec in enumerate(survivors):
 a,b,c,e,f=rec['column_class_coefficients'];L=s.Matrix.hstack(s.eye(12)[:,0],vec(a,1),vec(b,1),vec(c,1),vec(e,2),vec(f,2))
 for ep in ht.indicator_choices(R):
  started=time.monotonic();A,rhs,meta=ht.build_system(R,data,L,ep,6);y=ht.farkas(A,rhs)
  item={'branch':bi,'indicators':ep,'column_count':meta['column_count'],'trace_types':meta['trace_types'],'rows':meta['rows'],'separated':y is not None,'seconds':time.monotonic()-started}
  if y is not None:
   ht.check_farkas(A,rhs,y);item['farkas']=y;item['bTy']=sum(a*b for a,b in zip(rhs,y))
  out.append(item);print({k:v for k,v in item.items() if k!='farkas'},flush=True)
  (OUT/'R350_higher_probe.json').write_text(json.dumps(out,indent=2)+'\n')
  if y is None:break
