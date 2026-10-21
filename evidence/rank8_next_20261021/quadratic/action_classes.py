"""Identify the fully determined based-module actions up to module-basis permutation."""
import json,itertools,collections
from gram_discovery import HERE,require
from morita_closure import DATA,dim,mul,div,enc

def run():
 recs=json.loads((HERE/'profile_closure.json').read_text());out={}
 for rid,r in recs.items():
  n,ds=DATA[rid];classes={}
  for f in r['surviving_factors']:
   if f['full_rank_action']is None:continue
   U=f['full_rank_action'];B=f['B'];ad=dim(B[0],ds);dims=[div(mul(dim(v,ds),dim(v,ds),n),ad,n)for v in B];blocks=[[i for i,t in enumerate(dims)if t==d]for d in sorted(set(dims))];best=None;order=None
   for pp in itertools.product(*(itertools.permutations(b)for b in blocks)):
    p=[j for block in pp for j in block];key=tuple(U[i][j][k]for i in range(8)for j in p for k in p)
    if best is None or key<best:best=key;order=p
   if best not in classes:classes[best]={'module_rank':len(B),'canonical_internal_end_dimension_profile':[enc(dims[j])for j in order],'actions':[[[U[i][j][k]for k in order]for j in order]for i in range(8)],'induction_roots':[]}
   classes[best]['induction_roots'].append({'candidate_index':f['candidate_index'],'factor_index':f['factor_index']})
  if rid=='R8_3_65':
   families=[]
   for c in classes.values():
    g=c['actions'][1];rho=c['actions'][5];m=len(g);per=[next(i for i in range(m)if g[i][j])for j in range(m)];orbits=[];seen=set()
    require(all(sum(g[i][j]for i in range(m))==1 for j in range(m)),'invertible permutation')
    for j in range(m):
     if j in seen:continue
     orbit=[];k=j
     while k not in orbit:orbit.append(k);seen.add(k);k=per[k]
     orbits.append(orbit)
    require(len(orbits)==2 and len(orbits[0])==len(orbits[1])in(1,2,4),'two equal C4 orbits')
    Q=[[sum(rho[u][v]for v in b)for b in orbits]for u in [a[0]for a in orbits]]
    require(all([sum(rho[u][v]for v in b)for b in orbits]==Q[i]for i,a in enumerate(orbits)for u in a),'orbit quotient well defined')
    require(Q in ([[0,1],[1,11]],[[3,5],[5,8]]),'two quotient families')
    c['C4_orbits']=orbits;c['noninvertible_orbit_quotient']=Q;families.append((len(orbits[0]),tuple(map(tuple,Q))))
   require(len(set(families))==6,'one lift per size and quotient')
  out[rid]={'complete_action_classes':list(classes.values()),'complete_class_count':len(classes)}
  print(rid,'complete action classes',len(classes),'ranks',sorted(x['module_rank']for x in classes.values()),flush=True)
 (HERE/'action_classes.json').write_text(json.dumps(out,separators=(',',':'))+'\n');return out
if __name__=='__main__':run()
