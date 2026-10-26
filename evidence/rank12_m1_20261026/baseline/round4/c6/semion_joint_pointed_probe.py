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
R=json.loads((ROOT/'prior_round/prior_round/evidence/rank12-m1-offline-20261025/tensors.json').read_text())['R12_1_623'];du=[next(j for j in range(12) if R[i][j][0]) for i in range(12)];G=[i for i in range(12) if sum(R[i][du[i]])==1]
B=s.Matrix(12,12,lambda j,i:sum(R[a][j][k]*R[k][du[a]][i] for a in range(12) for k in range(12)))
D=(Q(120),Q(36));ds=[(Q(1),Q(0)) if i in G else (Q(3),Q(1)) for i in range(12)]
data={'ch':SimpleNamespace(n=12,C=B,du=du),'q':10,'conductor':40,'dimensions':ds,'global_dimension':D,'primes':[2,3,5]}
low_data=json.loads((OUT/'R623_induction_low_exact.json').read_text());classes=low_data['pointed_classes']+low_data['nonpointed_classes']
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
recs=low_data['branches'];survivors=[r for r in recs if r['psd']]
def vec(a,u):
 v=[0]*12;v[0]=u
 for cl,k in zip(classes[2:],a):
  for j in cl:v[j]=k
 return s.Matrix(v)

def add_indicator_equalities(A,rhs,meta,L,ct,ng):
 types,_=ht.trace_types(10,[2,3,5],6);_,hc=high_columns(data,L);lookup={v:z for v,z in hc};LL=L*L.T
 low=[tuple(sum((Q(int(LL[i,j]))*ds[j][k] for j in range(12)),Q(0)) for k in range(2)) for i in range(12)]
 coords=[0,1,10,11,9,2];targets=[]
 for a,i in enumerate(coords):
  if a==0:continue
  for k in range(3,7):
   if k*a%6:av=Q(0)
   else:
    order=36//math.gcd(36,ct*k*a*a);av=Q(int(s.mobius(order)),int(s.totient(order)))
   targets.append((i,k,av))
 targets += [(i,3,ng) for i in range(12) if i not in G]
 for i,k,av in targets:
  row=[]
  for v,ti in meta['labels']:
   z=lookup[tuple(v)];row.append(v[i-1]*ht.mul(z,types[ti][k-1],10)[0])
  row += [Q(0)]*(len(A[0])-len(row));bb=D[0]*av-low[i][0]
  den=math.lcm(bb.denominator,*(x.denominator for x in row));rr=[int(x*den) for x in row];bb=int(bb*den);g=math.gcd(bb,*rr) or 1
  A.append([x//g for x in rr]);rhs.append(bb//g)
 return A,rhs
def dual_pair_columns(A,rhs,meta):
 labels=meta['labels'];pos={(tuple(v),ti):i for i,(v,ti) in enumerate(labels)};orbits=[];seen=set()
 for j,(v,ti) in enumerate(labels):
  if j in seen:continue
  vd=tuple(v[du[i]-1] for i in range(1,12));j2=pos[(vd,ti)];orb=sorted({j,j2});seen.update(orb);orbits.append(orb)
 orbits += [[j] for j in range(len(labels),len(A[0]))]
 return [[sum(row[j] for j in orb) for orb in orbits] for row in A],rhs,len(orbits)
out=[]
for bi,rec in enumerate(survivors):
 L=s.Matrix(rec['columns']).T
 if any(L[i,1]!=L[du[i],1] for i in range(12)):continue
 ep=next(ep for ep in ht.indicator_choices(R)if ep[-1]==-1)
 A,rhs,meta=ht.build_system(R,data,L,ep,6)
 ct=int(sys.argv[1]);ng=Q(sys.argv[2]);A,rhs=add_indicator_equalities(A,rhs,meta,L,ct,ng)
 types,box=ht.trace_types(10,[2,3,5],6)
 target=tuple((Q(0),Q(0))if k%2 else(Q((-1)**(k//2)),Q(0))for k in range(1,7))
 ti=types.index(target)
 pos={(tuple(v),t):i for i,(v,t)in enumerate(meta['labels'])}
 def trace_root(n,a):
  g0=math.gcd(n,a);m=n//g0;c=a//g0;ph=int(s.totient(m));r=Q(int(s.mobius(m)),ph);ss=Q(0)
  if m%40==0 and math.gcd(m//40,40)==1:
   z=m//40;ss=Q(int(s.mobius(z))*int(s.kronecker_symbol(40,z))*int(s.kronecker_symbol(40,c))*2,ph)
  return(r,ss)
 from functools import lru_cache
 trace_root=lru_cache(None)(trace_root)
 typepos={tt:i for i,tt in enumerate(types)};pairtypes=set()
 for m0 in s.divisors(box):
  m=int(m0);ell=math.lcm(m,4)
  for a in range(m):
   if math.gcd(m,a)!=1:continue
   ts=tuple(trace_root(m,a*k)for k in range(1,7));tj0=typepos[ts]
   for sg in[-1,1]:
    az=a*(ell//m)+sg*(ell//4);zs=tuple(trace_root(ell,az*k)for k in range(1,7));pairtypes.add((tj0,typepos[zs]))
 zero=typepos[tuple((Q(0),Q(0))for k in range(6))];pairtypes.add((zero,zero))
 print('joint semion trace pairs',len(pairtypes),flush=True)
 perm=[R[11][i].index(1)for i in range(12)]
 constants={}
 for c in range(L.cols):
  v=tuple(int(L[perm[i],c])for i in range(1,12));j=pos[(v,ti)];constants[j]=constants.get(j,0)+1
 rhs=[b-sum(row[j]*m for j,m in constants.items())for row,b in zip(A,rhs)]
 # Pair all remaining central simples by tensoring with the semion.
 # Even twist moments transform by (-1)^(k/2); odd moments are deliberately
 # left unconstrained, a safe overapproximation of possible joint traces.
 labels=meta['labels'];pairs=[];seen=set()
 for j,(v,tt)in enumerate(labels):
  if v[10]:continue
  vz=tuple(v[perm[i]-1]if perm[i]else 0 for i in range(1,12))
  if tuple(v)>vz:continue
  for tj,ttz in enumerate(types):
   if (tt,tj)not in pairtypes:continue
   j2=pos[(vz,tj)]
   if tuple(v)==vz and tt>tj:continue
   pair=(j,j2);pairs.append(pair)
 newcols=[[row[j]+row[k]for row in A]for j,k in pairs]
 for j in range(len(labels),len(A[0])):newcols.append([row[j]for row in A])
 A=[list(row)for row in zip(*newcols)];nvars=len(newcols)
 y=ht.farkas(A,rhs)
 item={'branch':bi,'semion_trace_type':ti,'shifted_low_variables':constants,'separated':y is not None,'variables':nvars}
 if y is not None:ht.check_farkas(A,rhs,y);item.update(farkas=y,bTy=sum(a*b for a,b in zip(rhs,y)))
 print({k:v for k,v in item.items()if k!='farkas'},flush=True);out.append(item)
 (OUT/f"R623_semion_joint_pointed_{ct}_{str(ng).replace('/', '_')}.json").write_text(json.dumps(out,indent=2)+'\n')
