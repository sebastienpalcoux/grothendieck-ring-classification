"""Short experiment: full-column square-Galois orbit PSD filter.
No numerical result is an exclusion; accepted outputs require exact certificates.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,sys,json,gzip,math,collections,inspect,time
import sympy as s
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[1]/'prior'
WORK=PRIOR/'evidence/unresolved_retry_20261024/proofs'
sys.path[:0]=[str(WORK/'rank9_m2_research/phase3/quadratic_s_symmetry'),str(WORK/'rank9_m2_research/sources')]
import quadratic_s_symmetry as qs
qc=qs.qc
spec=importlib.util.spec_from_file_location('inputs',PRIOR/'data/current_remaining_cases.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
R=mod.TENSORS['R9_2_137']; n=9; ch=qc.Characters(R); G=ch.C
old=json.loads(gzip.decompress((PRIOR/'evidence/unresolved7_20261027/audit_parity/R137_tau_plus_prior_system.json.gz').read_bytes()))
pairs=list(__import__('itertools').combinations_with_replacement(range(n),2));diags={i:pairs.index((i,i)) for i in range(n)}
cols=set()
for j in range(len(old['A'][0])):
 v=[]
 for i in range(n):
  ri=diags[i]; v2=Q(old['A'][ri][j]*int(G[i,i]),old['b'][ri]);z=math.isqrt(v2.numerator)
  assert v2.denominator==1 and z*z==v2.numerator
  v.append(z)
 if any(v):cols.add(tuple(v))
D=(Q(144),Q(96));dims=[(Q(1),Q(0))]*n
for i in [3,4,5,6]:dims[i]=(Q(4),Q(3))
dims[8]=(Q(2),Q(0))
chars=qs.characters(ch,2,D);assert len(chars)==9
counts=collections.Counter(c['dimension'] for c in chars)
ratio=qc.div(D,(D[0],-D[1]),2)
def conj(z):
 out=qc.mul(ratio,(z[0],-z[1]),2)
 return out if qc.sign(out,2)>0 else qc.scale(out,-1)
cols=sorted((v,tuple(sum(v[i]*dims[i][c] for i in range(n)) for c in range(2)))for v in cols)
available={z for v,z in cols};gps=sorted({tuple(sorted((z,conj(z))))for z in available if z!=conj(z)})
data={'ch':ch,'q':2,'dims':dims,'D':D,'counts':counts,'cols':cols,'galois_pairs':gps,'primes':[2,3], 'raw_columns':len(cols),'pre_modular_columns':len(cols),'pre_galois_dimensions':len(available),'post_galois_dimensions':len(available)}
source=inspect.getsource(qs.build).replace('return AA,bb,meta','return AA,bb,meta,keys')
namespace=dict(vars(qs));exec(source,namespace)
qc.base=lambda _:data
A,b,meta,keys=namespace['build'](R,4,False)
types,bound=qc.trace_types(2,[2,3],4)
# Calculate every height-four trace with first nonzero order in box; all others vanish.
def trace(order,sign):
 out=[]
 for k in range(1,5):
  g=math.gcd(order,k);nn=order//g;phi=int(s.totient(nn));a=Q(int(s.mobius(nn)),phi);bb=Q(0)
  if nn%8==0:
   z=nn//8
   if math.gcd(z,8)==1:bb=Q(sign*int(s.mobius(z))*int(s.kronecker_symbol(8,z))*int(s.kronecker_symbol(8,k//g))*2,phi)
  out.append((a,bb))
 return tuple(out)
def orbit(order):
 N=math.lcm(order,8)
 return len({a*a%order for a in range(N) if math.gcd(a,N)==1 and s.kronecker_symbol(8,a)==1})
minorbit={typ:10**9 for typ in types};orders={typ:[] for typ in types}
for o in s.divisors(64*27):
 for sign in [-1,1]:
  typ=trace(int(o),sign)
  if typ not in minorbit:continue
  k=orbit(int(o));minorbit[typ]=min(minorbit[typ],k);orders[typ].append((int(o),sign,k))
assert all(x<10**9 for x in minorbit.values())
# Outside 2^5*3^2 box, traces are zero. Minimum orbit size is >=4 (2-adic) or >=9 (3-adic).
zero=tuple([(Q(0),Q(0))]*4);assert minorbit[zero]==3
Ginv=G.inv();norm={v:Q((s.Matrix(v).T*Ginv*s.Matrix(v))[0]) for v,z in cols}
col_dims=dict(cols)
# Use exact existing system columns, matched by all inherited base rows.
# Reordering the recovered set of restriction columns is harmless; this match
# proves each filtered old variable has the asserted exact (v, trace) identity.
siginfo={}
for j,(kind,v,ti) in enumerate(keys):
 if kind not in ('high','label','anonymous'):continue
 signature=tuple(row[j] for row in A)
 k=minorbit[types[ti]] if kind=='high' else 1
 value=(v,k,norm[v],types[ti] if kind=='high' else tuple([(Q(1),Q(0))]*4))
 if signature in siginfo:assert siginfo[signature][:3]==value[:3]
 siginfo[signature]=value
for tau in [1,-1]:
 sign='plus' if tau==1 else 'minus'
 p=PRIOR/f'evidence/unresolved7_20261027/audit_parity/R137_tau_{sign}_positive_fs2_system.json.gz'
 x=json.loads(gzip.decompress(p.read_bytes()));AA=x['A'];bb=x['b'];removed=[];matched=0; fourth=[[]for _ in range(4)]
 for j in range(len(AA[0])):
  physical=any(AA[r][j] for r in range(45))
  if not physical:
   for row in fourth:row.append(Q(0))
   continue
  sig=tuple(AA[r][j] for r in range(len(A)))
  if sig not in siginfo:raise ValueError(('unmatched',j,len(A)))
  v,k,nn,tt=siginfo[sig];matched+=1
  for row,i in zip(fourth,[3,4,5,6]):row.append(v[i]*qc.mul(col_dims[v],tt[3],2)[1])
  if k*nn>1:removed.append(j)
 for row in fourth:
  for sg in [1,-1]:
   den=math.lcm(*(v.denominator for v in row));
   for rr in AA:rr.append(0)
   AA.append([int(sg*v*den)for v in row]+[0]*(len(AA[0])-len(row)-1)+[1]);bb.append(384*den)
 remset=set(removed);keep2=[j for j in range(len(AA[0])) if j not in remset]
 aa=np.asarray(AA,dtype=float)[:,keep2];rhs=np.asarray(bb,dtype=float);scale=np.maximum(1,np.maximum(abs(rhs),np.max(abs(aa),axis=1)))
 res=linprog(np.zeros(len(keep2)),A_eq=aa/scale[:,None],b_eq=rhs/scale,bounds=(0,None),method='highs',options={'time_limit':20})
 out={'fourth_indicator_bounds':[-4,4],'tau':tau,'columns_before':len(AA[0]),'columns_matched':matched,'columns_removed':len(removed),'status':int(res.status),'message':res.message,'new_filter_passes_numerically':bool(res.success),'accepted_exclusion':False,'minimum_orbits':{str(t):k for t,k in minorbit.items()}}
 if res.success:
  import flint
  support=[keep2[j] for j,v in enumerate(res.x) if v>1e-7]
  mat,rank=flint.fmpq_mat([[row[j]for j in support]+[y]for row,y in zip(AA,bb)]).rref()
  vals=[Q(0)]*len(support)
  for i in range(rank):
   pivot=next(j for j in range(len(support)+1)if mat[i,j]);assert pivot<len(support);vals[pivot]=Q(str(mat[i,len(support)]))
  assert all(v>=0 for v in vals)
  assert all(sum(row[j]*v for j,v in zip(support,vals))==y for row,y in zip(AA,bb))
  out['exact_witness']=[[j,str(v)]for j,v in zip(support,vals)if v]
  out['exact_witness_support']=len(out['exact_witness'])
 out['removed_columns']=removed
 (HERE/f'orbit_quartic_screen_tau{tau}.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['minimum_orbits','exact_witness','removed_columns']},flush=True)
