"""Peel forced common characters from finite semisimple local spectra."""
import runpy,json,time,collections,itertools
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent; ns=runpy.run_path(str(P/'pure_braid_eigenspaces.py'))
N,t,M,r=map(ns.get,['N','t','M','r']); profiles={}
def canonical(A,B,C,k):
 # Spectra channel exponents satisfy product z^k. Shift third spectrum by -k.
 rows=[tuple(sorted((int(e),int(v)) for e,v in enumerate(A) if v)),
       tuple(sorted((int(e),int(v)) for e,v in enumerate(B) if v)),
       tuple(sorted(((int(e)-int(k))%24,int(v)) for e,v in enumerate(C) if v))]
 return tuple(sorted(rows))
for a,b,c in itertools.combinations_with_replacement(range(r),3):
 for d in range(r):
  if M[a,b,c,d].sum():
   key=canonical(M[a,b,c,d],M[b,c,a,d],M[a,c,b,d],t[a]+t[b]+t[c]+t[d])
   profiles.setdefault(key,[a,b,c,d])
def peel(key):
 rows=[dict(row) for row in key]; removed=[]
 while True:
  n=sum(rows[0].values()); assert all(sum(row.values())==n for row in rows)
  forced=collections.defaultdict(int)
  for i,j in [(0,1),(0,2),(1,2)]:
   k=3-i-j
   for e,u in rows[i].items():
    for f,v in rows[j].items():
     need=u+v-n
     if need>0:
      ch=[None]*3;ch[i]=e;ch[j]=f;ch[k]=(-e-f)%24;ch=tuple(ch)
      forced[ch]=max(forced[ch],need)
  if not forced: return rows,removed,None
  for ch,m in forced.items():
   for i,e in enumerate(ch):rows[i][e]=rows[i].get(e,0)-m
   removed.append([ch,m])
  if any(v<0 for row in rows for v in row.values()):return rows,removed,'forced character multiplicities exceed spectrum'
  rows=[{e:v for e,v in row.items() if v} for row in rows]
  if not rows[0]:return rows,removed,None
start=time.time();fails=[]; leftovers=collections.Counter(); scott=[];peeled=0
for key,case in profiles.items():
 rows,removed,err=peel(key);peeled+=bool(removed)
 if err:fails.append({'case':case,'error':err,'spectrum':key,'removed':removed});continue
 n=sum(rows[0].values());leftovers[n]+=1
 if n>0 and sum(v*v for row in rows for v in row.values())>n*n+2:
  scott.append({'case':case,'n':n,'spectrum':[sorted(row.items()) for row in rows]})
out={'scope':'necessary spectral tests only','unique_profiles':len(profiles),'profiles_with_forced_characters':peeled,'violations':fails,'remaining_dimensions':dict(sorted(leftovers.items())),'remaining_Scott_reducible_profiles':scott,'elapsed':time.time()-start}
(P/'pure_braid_peeling_receipt.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps({k:v for k,v in out.items() if k not in ('remaining_dimensions','remaining_Scott_reducible_profiles')},indent=2));print('Scott reducible',len(scott))
