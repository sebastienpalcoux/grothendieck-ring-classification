"""Independent receipt replay for oriented GF(2) sign completeness.

The discovery reduction routine is not called. Each recorded sign relation
is derived again from its full associativity polynomial and triangle equality;
gauge normalization and the final complete finite domain are checked afresh.
"""
import collections,itertools,json,hashlib,sys
from pathlib import Path
from branches import signed_tensor,validate,dimension_test
from oriented import read,require,parity,P

def reducer(basis):
 def reduce(m):
  for p in sorted(basis,reverse=True):
   if m>>p&1:m^=basis[p]
  return m
 return reduce

def rank(rows):
 b={};reduce=reducer(b)
 for r in rows:
  r=reduce(r)
  if r:b[r.bit_length()-1]=r
 return len(b)

def verify_record(R,rec):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 mapping={};orbits=rec['oriented_orbits']
 for j,orb in enumerate(orbits):
  a,b,c=orb[0];v=(du[c],du[b],du[a]);expected={(a,b,c),(b,c,a),(c,a,b),v,(v[1],v[2],v[0]),(v[2],v[0],v[1])}
  require(set(map(tuple,orb))==expected,'exact oriented orbit')
  for i,k,l in orb:
   require(i and k and l and R[i][k][du[l]]==1,'orbit support')
   require((i,k,du[l]) not in mapping,'disjoint orbits');mapping[i,k,du[l]]=j
 require(len(mapping)==sum(R[i][j][k] for i,j,k in itertools.product(range(1,n),repeat=3)),'complete oriented support')
 def mono(i,j,k):
  if not R[i][j][k]:return None
  return 0 if 0 in (i,j,k) else 1<<mapping[i,j,k]
 def raw(source):
  i,j,k,l=source;p=collections.Counter()
  for h in range(n):
   a,b=mono(i,j,h),mono(h,k,l)
   if a is not None and b is not None:p[a^b]+=1
   a,b=mono(j,k,h),mono(i,h,l)
   if a is not None and b is not None:p[a^b]-=1
  return {m:c for m,c in p.items() if c}
 dual_orbits=[];seen={0}
 for i in range(1,n):
  if i not in seen:dual_orbits.append(sorted({i,du[i]}));seen|={i,du[i]}
 require(dual_orbits==rec['gauge_dual_orbits'],'dual gauge orbits')
 gs=[]
 for D in dual_orbits:
  gs.append(sum((sum(i in D for i in orb[0])%2)<<j for j,orb in enumerate(orbits)))
 require(gs==rec['gauge_vectors'],'gauge vectors')
 coords=rec['gauge_coordinates'];require(len(coords)==rank(gs)==rec['gauge_rank'],'full gauge rank')
 restricted=[sum(((g>>j)&1)<<h for h,j in enumerate(coords)) for g in gs]
 require(rank(restricted)==len(coords),'gauge normalization surjective')
 basis={};reduce=reducer(basis);normalized=False
 def add(r):
  r=reduce(r)
  require(r!=0,'independent relation');basis[r.bit_length()-1]=r
 def gauge_fix():
  require(len(basis)==rec['linear_rank_before_gauge'],'pre-gauge rank')
  require(all(parity(g&b)==0 for g in gs for b in basis.values()),'gauge preserves pre-normalization equations')
  for j in coords:add(1<<j)
 for d in rec['deductions']:
  if d['stage']=='normalized_gauge' and not normalized:gauge_fix();normalized=True
  require(d['stage']==('normalized_gauge' if normalized else 'unfixed_gauge'),'deduction order')
  q=collections.Counter()
  for m,c in raw(d['source']).items():q[reduce(m)]+=c
  q={m:c for m,c in q.items() if c}
  require(sorted(q.items())==[tuple(x) for x in d['terms']],'recomputed reduced polynomial')
  total=sum(abs(c) for c in q.values());anchors=[m for m,c in q.items() if 2*abs(c)==total]
  require(anchors and sum(q.values())==0,'exact saturating triangle equality')
  allowed=[anchors[0]^m for m in q];allowed_basis=dict(basis);ared=reducer(allowed_basis)
  for m in allowed:
   m=ared(m)
   if m:allowed_basis[m.bit_length()-1]=m
  for rel in d['relations']:
   require(ared(rel)==0 and reduce(rel)==rel,'claimed relation is implied and reduced');add(rel)
 if not normalized:gauge_fix()
 free=[j for j in range(len(orbits)) if j not in basis]
 exp=[reduce(1<<j) for j in range(len(orbits))]
 require(free==rec['normalized_free_variables'] and exp==rec['normalized_variable_exponents'],'complete final linear domain')
 require(len(rec['branches'])==1<<len(free),'all normalized assignments enumerated')
 a={'mapping':mapping}
 for z,b in enumerate(rec['branches']):
  require(z==b['free_bits'],'branch order');zf=sum(((z>>j)&1)<<i for j,i in enumerate(free));values=sum(parity(m&zf)<<i for i,m in enumerate(exp))
  require(values==b['sign_assignment'],'sign reconstruction')
  T=signed_tensor(R,a,values)
  if b['outcome']=='not_associative':
   source=b['associativity_failure']['source'];p=raw(source);diff=sum(c*(-1 if parity(m&values) else 1) for m,c in p.items())
   require(diff!=0 and diff==b['associativity_failure']['difference'],'exact associativity failure')
  else:
   validate(T,du)
   require(hashlib.sha256(json.dumps(T,separators=(',',':')).encode()).hexdigest()==b['signed_tensor_sha256'],'signed tensor identity')
   if b['outcome']=='gauge_original':require(values==0 and T==R,'original branch')
   else:
    result=dimension_test(R,T,du);require(result==b['dimension_test'],'dimension character receipt')
    require(b['outcome']==('excluded_dimension_characters' if result['all_dimension_characters_excluded'] else 'signed_branch_survives'),'branch classification')
 require(rec['all_categorical_signed_tables_are_gauge_original']==all(b['outcome']!='signed_branch_survives' for b in rec['branches']),'categorical sign conclusion')
 return True

if __name__=='__main__':
 rows={r['id']:r for r in read()};ledger=json.loads((P/'ledger.json').read_text())
 for i,rec in enumerate(ledger,1):
  r=rows[rec['id']];require(r['tensor_sha256']==rec['tensor_sha256'],'source identity');verify_record(r['tensor'],rec)
  if i%10==0:print('PASS',i,flush=True)
 print('PASS complete independent oriented sign replay',len(ledger),flush=True)
