"""Exhaustive group law test after all Morita right-action matrices are enumerated."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import json,collections,numpy as np,sympy as s,sys
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'supplements/rank6/software'));sys.path.insert(0,str(Path(__file__).resolve().parent))
from full_morita_gram import full_gram
from r4982_module import all_modules
report=json.load(open(Path(__file__).with_name('r4982_fullgram_actions.json')));V=[tuple(z) for z in report['invertible_actions']];n=len(V);r=13;index={v:i for i,v in enumerate(V)};ms=[np.array(z).reshape(r,r) for z in V];e=index[tuple(np.eye(r,dtype=int).flat)];table=[[index[tuple((A@B).flat)] for B in ms] for A in ms]
G=np.array(full_gram(all_modules()[0]),dtype=int)
for z in report['noninvertible_actions']:G-=np.outer(z,z)
subgroups={frozenset([e])};queue=[frozenset([e])]
def generated(H,g):
 S=set(H);todo=list(H)
 while todo:
  h=todo.pop()
  for j in list(S)+[g]:
   for k in [table[h][j],table[j][h]]:
    if k not in S:
     S.add(k);todo.append(k)
     if len(S)>12:return None
 return frozenset(S)
for H in queue:
 for g in range(n):
  if g in H:continue
  K=generated(H,g)
  if K is not None and 12%len(K)==0 and K not in subgroups:subgroups.add(K);queue.append(K)
print('subgroups',len(subgroups),'orders',collections.Counter(map(len,subgroups)),flush=True)
passing=[]
for H in subgroups:
 k=12//len(H);K=sum((np.outer(V[j],V[j]) for j in H),np.zeros_like(G))*k
 if np.array_equal(K,G):passing.append(sorted(H))
print('passing',len(passing),passing,flush=True)
result={'permutation_group_order':n,'subgroup_counts':dict(collections.Counter(map(len,subgroups))),'passing_subgroups':passing,'identity':e,'multiplication_table':table}
Path(__file__).with_name('r4982_invertible_group_result.json').write_text(json.dumps(result)+'\n')
