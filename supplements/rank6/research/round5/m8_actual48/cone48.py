"""Complete level48 signed T-spectrum cone with exact integer capacity bounds."""
import sys,math,json,hashlib
import actual48 as Q
from exact import require,evaluate
sys.path.insert(0,str(Q.P/'research/round5/m8_modrep'))
import representation_cone as K

def append_rows(R,d,cols,labels,nv,profile_vectors):
 C=d['C'];require(d['F']==48 and len(cols)==6,'level48 rank6 center required');require(all(evaluate(z.to_list(),C.unit**47,C)==z for row in d['tab'].rows for z in row),'lowcharacters not all real');allowed={a for v,a in labels}|{0};primitive={a for a in allowed if math.gcd(a,48)==3};require(len(d['ising_labels'])==1,'unique Ising pair required');g,ss=d['ising_labels'][0]
 for v,a in labels:
  if a in primitive:
   dv=sum((C(v[i])*d['dims'][i+1]for i in range(len(v))),C.zero);require(v[ss-1]==1 and dv==d['DD']*d['dims'][ss]/C(8),'primitive16 capacity2 not proved')
 source=K.records();allcone=source['cone'];kept=[i for i,r in enumerate(allcone)if all(not z or k in allowed for k,z in enumerate(r['spectrum']))and all(r['spectrum'][k]<=2 for k in primitive)];cone=[allcone[i]for i in kept];total=nv+len(cone)*2+48;rows=[];rhs=[]
 for k in range(48):
  row={j:1 for j,(v,a)in enumerate(labels)if a==k}
  for j,r in enumerate(cone):
   if r['spectrum'][k]:row[nv+j]=-r['spectrum'][k]
  rows.append(row);rhs.append(-6 if k==0 else 0);row={nv+j:r['central_sign']*r['spectrum'][k]for j,r in enumerate(cone)if r['spectrum'][k]};row[nv+len(cone)+k]=-1;rows.append(row);rhs.append(6 if k==0 else 0)
 for j,r in enumerate(cone):rows.append({nv+j:1,nv+len(cone)+48+j:1})
 supports={tuple(v):{a for w,a in labels if tuple(w)==tuple(v)}for v in profile_vectors}
 def bounds(profile):
  rank=6+sum(profile);cap=[6]+[0]*47
  for v,m in zip(profile_vectors,profile):
   for a in supports[tuple(v)]:cap[a]+=m
  for a in primitive:cap[a]=2
  return [min(rank//r['degree'],min(cap[a]//z for a,z in enumerate(r['spectrum'])if z))for r in cone]
 return rows,rhs,total,bounds,dict(kind='complete_SL2Z48_signed_spectrum_integer_capacity',irreducible_count=source['irreducible_count'],all_spectrum_types=len(allcone),retained_spectrum_types=len(cone),kept_spectrum_indices=kept,primitive16_roots=sorted(primitive),primitive16_capacity=2,variables_added=total-nv,equations_added=len(rows),bounds='min(floor(center_rank/degree),floor(root_capacity/root_multiplicity))')
