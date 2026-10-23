import json,pathlib,itertools
P=pathlib.Path(__file__).resolve().parents[1]/'quadratic_obstructions'
def flat(a):return tuple(x for r in a for x in r)
def tr(a):return [list(r) for r in zip(*a)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
def summ(*a):return [[sum(x[i][j] for x in a) for j in range(8)] for i in range(8)]
for q in [21,114,115,152,153,179]:
 p=P/f'R10_1_{q}_dual_action_candidates.json'
 if not p.exists():continue
 c=json.load(open(p))['candidates'];M=[x['matrix'] for x in c];lookup={flat(a):i for i,a in enumerate(M)}
 mod=json.load(open(P/f'R10_1_{q}_module.json')); original=next(a for a in json.load(open(P.parents[1]/'catalogue.json'))['cases'] if a['id']==f'R10_1_{q}'); invsrc=original['invariants']['invertible_indices']; invmods=[i for i,orb in enumerate(mod['free_orbits']) if orb[0] in invsrc]; inv=[i for i,x in enumerate(c) if x['module_index'] in invmods];small=[i for i,x in enumerate(c) if x['module_index']>=4];large=[i for i in range(16) if i not in inv+small]
 unit=lookup[tuple(int(i==j) for i in range(8) for j in range(8))];du=[lookup.get(flat(tr(a))) for a in M];print(q,'unit',unit,'dual',du,flush=True)
 out={'id':f'R10_1_{q}','unit':unit,'dual':du,'small_products':{},'adjoint_closure':{}}
 products={}
 for i,j in itertools.product(inv+small,repeat=2):
  a=flat(mul(M[i],M[j]));choices=[]
  if i in inv or j in inv: choices=[(lookup[a],)] if a in lookup else[]
  else:
   if a in lookup:choices=[(lookup[a],)]
   for g in inv:
    for y,z in itertools.combinations_with_replacement(small,2):
     if flat(summ(M[g],M[y],M[z]))==a:choices.append((g,y,z))
  products[i,j]=choices
  out['small_products'][str((i,j))]=choices
 for i in small:
  ss={unit};old=None
  for choice in products[i,du[i]]:ss.update(choice)
  while ss!=old and not ss.intersection(large):
   old=set(ss)
   for a,b in itertools.product(old,repeat=2):
    for choice in products.get((a,b),[]):ss.update(choice)
  out['adjoint_closure'][i]=sorted(ss)
  print(' ',i,'adj',products[i,du[i]],'closure',sorted(ss),flush=True)
 pathlib.Path(__file__).with_name(f'R10_1_{q}_small_actions.json').write_text(json.dumps(out,indent=2))
