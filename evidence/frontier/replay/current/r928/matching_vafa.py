"""Finite NC3 matching and three-C3 Vafa check; all phases inherited candidates."""
import json
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path

BASE=Path(__file__).resolve().parent
N=1728
p=next(p for p in json.load(open(BASE/'prior/spectral_reduction.json'))['patterns'] if p['pattern']==186)
n=p['rank'];dims=p['dimensions']
B=[[Q(a)+Q(b) for a,b in zip(row1,row2)] for row1,row2 in zip(p['baseline_M'],p['fixed_Q0'])]
assert all(z.denominator==1 for row in B for z in row)
B=[[int(z) for z in row] for row in B]
u=B[3];M=p['N_c_squared'][3]
groups={}
for i in range(5,n):groups.setdefault(tuple(dims[i]),[]).append(i)
def matchings(indices,k):
 if k==0:
  yield [];return
 if len(indices)<2*k:return
 a=indices[0]
 yield from matchings(indices[1:],k)
 for j,b in enumerate(indices[1:]):
  rem=indices[1:j+1]+indices[j+2:]
  for tail in matchings(rem,k-1):yield [(a,b)]+tail
allmatch=[]
gs=[g for g in groups.values() if len(g)>1]
for counts in product(*(range(len(g)//2+1) for g in gs)):
 if sum(counts)!=3:continue
 for tup in product(*(list(matchings(g,k)) for g,k in zip(gs,counts))):allmatch.append(sum(tup,[]))
assert len(allmatch)==354,len(allmatch)
records=[]
for cand in json.load(open(BASE/'vafa_probe.json'))['survivors']:
 t,k,A,bt,h=cand
 phase=[0]*4+[N//4,t*12]+A+[v*12 for v in bt]+h+[k,t*12]
 assert len(phase)==n
 base=[(M[j]*phase[j]-3*sum(u[r]*B[r][j]*phase[r] for r in range(n)))%N for j in range(n)]
 survive=[]
 for pairs in allmatch:
  z=base[:]
  for a,b in pairs:
   assert u[a]==u[b]
   q=3*u[a]*(phase[b]-phase[a])
   z[a]=(z[a]+q)%N;z[b]=(z[b]-q)%N
  if not any(z):survive.append(pairs)
 records.append({'phase':cand,'matchings':survive})
print('candidate phases',len(records),'phases surviving',sum(bool(x['matchings']) for x in records),'matching totals',sum(len(x['matchings']) for x in records))
(BASE/'matching_vafa.json').write_text(json.dumps({'matching_count':len(allmatch),'results':records},indent=2)+'\n')
