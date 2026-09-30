import sys,json,itertools
from collections import Counter,defaultdict
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'));from round5_629 import *
here=Path(__file__).parent;R,d,cols,lab,src=source_data();C=d['C'];twists=json.load(open(here/'decoded_twists.json'));conjugate=[]
for rank in (35,38):
 cases=[c for c in twists if c['rank']==rank];require(len(cases)==2,'twist branch count')
 def multiset(case,sign=1):
  out=Counter()
  for o in case['orbits']:
   require(o['orbit_degree']==1 and o['root_order'] in (1,3,5,15),'twists not explicitly in conductor15')
   out[tuple(o['column']),sign*(15//o['root_order']*o['root_power'])%15]+=o['copies']
  return out
 require(multiset(cases[0],-1)==multiset(cases[1]),'twist branches not conjugate');conjugate.append(rank)
case=next(c for c in twists if c['rank']==35 and c['solution']==0);groups=defaultdict(list);ix=6
for o in case['orbits']:
 key=(tuple(o['column']),15//o['root_order']*o['root_power']%15)
 for _ in range(o['copies']):groups[key].append(ix);ix+=1
pairs=[v for v in groups.values() if len(v)>1];require(len(pairs)==2 and all(len(p)==2 for p in pairs),'wrong duality ambiguity')
branches=json.load(open(here/'rank35_modular_completions.json'))['branches'];good=[b for b in branches if b['obstruction'] is None];require(len(good)==4,'wrong modular completion count');ref=good[0];answer=[]
for b in good:
 found=[]
 for swaps in itertools.product((False,True),repeat=2):
  perm=list(range(35))
  for swap,(i,j) in zip(swaps,pairs):
   if swap:perm[i],perm[j]=perm[j],perm[i]
  if all(b['S'][i][j]==ref['S'][perm[i]][perm[j]] for i in range(35) for j in range(35)):found.append(perm)
 require(found,'admissible matrices not related by twin swaps');answer.append({'signs':b['signs'],'permutation':found[0]})
rec={'passed':True,'complex_conjugate_twist_pairs':conjugate,'maximum_negative_duality_eigenvalues':2,'finite_rep_other_branch_negative_duality_eigenvalues':4,'admissible_rank35_completions':4,'one_class_under_twins':True,'twin_pairs':pairs,'equivalences':answer};(here/'equivalences.json').write_text(json.dumps(rec,indent=2));print({k:v for k,v in rec.items() if k!='equivalences'},flush=True)
