"""Exact oriented sign associativity and dual-compatible gauge normalization.

No commutativity or FS-indicator normalization is imposed. Variable orbits
use cyclic trace symmetry and dual reversal only. All multiplication terms
retain their order. Exact binomial/triangle-equality deductions precede
finite enumeration of every remaining normalized assignment.
"""
import collections,itertools,json,hashlib,time,sys
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
sys.path.insert(0,str(ROOT/'work/obstructions'))
from arithmetic import read,comm

def require(v,msg):
 if not v:raise ValueError(msg)
def parity(x):return x.bit_count()%2

def build(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 require(all(R[i][j][k] in (0,1) for i,j,k in itertools.product(range(n),repeat=3)),'multiplicity one')
 def orbit(t):
  a,b,c=t;v=(du[c],du[b],du[a]);return {t,(b,c,a),(c,a,b),v,(v[1],v[2],v[0]),(v[2],v[0],v[1])}
 unseen=set(itertools.product(range(1,n),repeat=3));variables=[];mapping={}
 while unseen:
  tri=min(unseen);orb=orbit(tri);unseen.difference_update(orb)
  a,b,c=tri;val=R[a][b][du[c]]
  require(all(R[i][j][du[k]]==val for i,j,k in orb),'oriented reciprocity')
  if not val:continue
  ix=len(variables);variables.append(sorted(orb))
  for i,j,k in orb:mapping[i,j,du[k]]=ix
 def mono(i,j,k):
  if not R[i][j][k]:return None
  if 0 in (i,j,k):return 0
  return 1<<mapping[i,j,k]
 eqs=[]
 for i,j,k,l in itertools.product(range(n),repeat=4):
  p=collections.Counter()
  for h in range(n):
   a,b=mono(i,j,h),mono(h,k,l)
   if a is not None and b is not None:p[a^b]+=1
   a,b=mono(j,k,h),mono(i,h,l)
   if a is not None and b is not None:p[a^b]-=1
  p={m:c for m,c in p.items() if c}
  if p:eqs.append(((i,j,k,l),p))
 require(all(sum(p.values())==0 for _,p in eqs),'original associativity')
 duorbits=[];seen={0}
 for i in range(1,n):
  if i not in seen:duorbits.append(sorted({i,du[i]}));seen|={i,du[i]}
 gauge=[]
 for orb in duorbits:
  S=set(orb);gauge.append(sum((sum(i in S for i in vs[0])%2)<<j for j,vs in enumerate(variables)))
 return du,variables,mapping,eqs,duorbits,gauge

def linear_analysis(R):
 du,variables,mapping,eqs,duorbits,gauge=build(R);v=len(variables);basis={};deductions=[]
 def reduce(m):
  for p in sorted(basis,reverse=True):
   if m>>p&1:m^=basis[p]
  return m
 def rp(p):
  q=collections.Counter()
  for m,c in p.items():q[reduce(m)]+=c
  return {m:c for m,c in q.items() if c}
 def add(m):
  m=reduce(m)
  if m:basis[m.bit_length()-1]=m
  return m
 def saturate(stage):
  passes=0
  while True:
   before=len(basis);passes+=1
   for source,p in eqs:
    q=rp(p)
    if not q:continue
    total=sum(abs(c) for c in q.values())
    a=next((m for m,c in q.items() if 2*abs(c)==total),None)
    if a is None:continue
    rows=[]
    for b in q:
     m=add(a^b)
     if m:rows.append(m)
    if rows:deductions.append({'stage':stage,'source':list(source),'terms':sorted(q.items()),'relations':rows})
   if len(basis)==before:break
  return passes
 passes=saturate('unfixed_gauge');linear_rank=len(basis)
 require(all(parity(g&b)==0 for g in gauge for b in basis.values()),'gauge preserves equations')
 # Select independent gauge coordinate rows; their signs can simultaneously
 # be made positive, and they remove exactly the gauge action's rank.
 piv={};coords=[]
 for j in range(v):
  mask=sum(((g>>j)&1)<<i for i,g in enumerate(gauge))
  for p in sorted(piv,reverse=True):
   if mask>>p&1:mask^=piv[p]
  if mask:piv[mask.bit_length()-1]=mask;coords.append(j)
 for j in coords:require(add(1<<j),'gauge normalization independent')
 passes+=saturate('normalized_gauge')
 residuals=[];seen=set()
 for source,p in eqs:
  q=rp(p)
  if q:
   tq=tuple(sorted(q.items()))
   if tq not in seen:seen.add(tq);residuals.append((source,q))
 free=[i for i in range(v) if i not in basis]
 return dict(du=du,variables=variables,mapping=mapping,equations=eqs,gauge_orbits=duorbits,gauge=gauge,gauge_coordinates=coords,gauge_rank=len(coords),basis=basis,deductions=deductions,linear_rank=linear_rank,free=free,reduced_variables=[reduce(1<<i) for i in range(v)],residuals=residuals,passes=passes)

def serial_analysis(r,a):
 return dict(id=r['id'],tensor_sha256=r['tensor_sha256'],rank=r['rank'],source_commutative=comm(r['tensor']),variables=len(a['variables']),oriented_orbits=a['variables'],equations=len(a['equations']),linear_rank_before_gauge=a['linear_rank'],gauge_rank=a['gauge_rank'],gauge_coordinates=a['gauge_coordinates'],gauge_dual_orbits=a['gauge_orbits'],gauge_vectors=a['gauge'],normalized_free_variables=a['free'],normalized_variable_exponents=a['reduced_variables'],normalized_residuals=[{'source':list(x),'terms':sorted(p.items())} for x,p in a['residuals']],deductions=a['deductions'])

def targets():
 ids={x['id'] for x in json.load(open(ROOT/'work/obstructions/survivors.json'))}
 for p in ['work/models/known_models_zested.json','work/root_models/models.json']:
  ids-={x['id'] for x in json.load(open(ROOT/p))}
 g=json.load(open(ROOT/'work/literature/gty_liptrap_certificates.json'));ids-={i for i,v in g.items() if v.get('found')}
 out=[]
 for r in read():
  if r['id'] not in ids:continue
  R=r['tensor'];n=len(R)
  if all(R[i][j][0]==int(i==j) for i in range(n) for j in range(n)):continue
  out.append(r)
 return out

if __name__=='__main__':
 rows=targets();out=[];start=time.monotonic()
 for r in rows:
  a=linear_analysis(r['tensor']);v=serial_analysis(r,a);out.append(v)
  (P/'profile.json').write_text(json.dumps(out,indent=2)+'\n')
  print(r['id'],'vars',v['variables'],'linear',v['linear_rank_before_gauge'],'gauge',v['gauge_rank'],'free',len(v['normalized_free_variables']),'residual',len(v['normalized_residuals']),'seconds',round(time.monotonic()-start,2),flush=True)
 print('DONE',len(out),'seconds',time.monotonic()-start,flush=True)
