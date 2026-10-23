"""Exact structural replay from independently reconstructed Morita-dual tensors.
This does not decide categorifiability of the dual tensors.
"""
import json,pathlib,hashlib,itertools
P=pathlib.Path(__file__).resolve().parents[1]/'quadratic_obstructions'
OUT=pathlib.Path(__file__).resolve().parent

def require(x,msg):
 if not x:raise ValueError(msg)
def support(N,i,j):return {k for k,n in enumerate(N[i][j]) if n}
def closure(N,du,seed):
 a=set(seed);old=None
 while a!=old:
  old=set(a);a.update(du[x] for x in old)
  for x,y in itertools.product(old,repeat=2):a.update(support(N,x,y))
 return sorted(a)
rows=[]
for q in [21,114,115,152,153,179]:
 path=P/f'R10_1_{q}_dual_tensor.json';a=json.load(open(path));N=a['fusion_tensor'];du=a['dual'];unit=a['unit']
 require(len(N)==16,'rank16');inv=[i for i in range(16) if support(N,i,du[i])=={unit} and N[i][du[i]][unit]==1]
 # canonical tau is the sign automorphism: all free module simples fixed,
 # each split fixed-object pair swapped.
 mats=json.load(open(P/f'R10_1_{q}_dual_action_candidates.json'))['candidates']
 tau_matrix=[[int((i==j and i<4) or (i>=4 and j==(i^1))) for j in range(8)] for i in range(8)]
 tau=next(i for i,c in enumerate(mats) if c['matrix']==tau_matrix)
 require(tau in inv and support(N,tau,tau)=={unit},'canonical tau involution')
 small=[i for i,c in enumerate(mats) if c['module_index']>=4]
 subcats=sorted({tuple(closure(N,du,support(N,i,du[i]))) for i in small})
 require(len(subcats)==2 and all(len(s)==4 for s in subcats),'two rank4 subcats')
 inter=set(subcats[0])&set(subcats[1]);require(len(inter)==2 and unit in inter,'pointed intersection')
 f=next(i for i in inter if i!=unit);require(f in inv and f!=tau,'shared f distinctfromtau')
 model='PSU(2)_6' if all(du[x]==x for x in subcats[0]) else 'pseudo-PSU(2)_6'
 for sc in subcats:
  xs=[x for x in sc if x not in inv];require(len(xs)==2,'two smalls')
  x,y=xs;require(support(N,f,x)=={y} and support(N,x,f)=={y},'f exchanges')
  require(support(N,x,du[x])=={unit,x,y},'adjointproduct')
  require(support(N,x,x)==({unit,x,y} if du[x]==x else {f,x,y}),'rank4model')
  require(all(n<=1 for i,j in itertools.product(sc,repeat=2) for n in N[i][j]),'rank4mult1')
 conj={i:next(iter(support(N,next(iter(support(N,tau,i))),tau))) for i in range(16)}
 require({conj[i] for i in subcats[0]}==set(subcats[1]),'tau swaps subcats')
 adj=closure(N,du,{k for i in range(16) for k in support(N,i,du[i])})
 require(len(adj)==8 and tau not in adj,'rank8 neutral')
 require(set(adj)==set(closure(N,du,set(subcats[0])|set(subcats[1]))),'subcatsgenerateadjoint')
 require(all(N[i][j]==N[j][i] for i,j in itertools.product(adj,repeat=2)),'neutralcommutative')
 # These exact hypotheses support the relative-factorization proof.
 c,e=map(set,subcats)
 require(all(len(support(N,i,j))==1 and sum(N[i][j])==1 for i,j in itertools.product(c,e)), 'cross products simple')
 require(all(len({next(iter(support(N,i,j))) for j in e})==4 for i in c),'fixed C object acts fully faithfully on E')
 require(all(len({next(iter(support(N,i,j))) for i in c})==4 for j in e),'fixed E object acts fully faithfully on C')
 require(all(next(iter(support(N,f,i)))!=i for i in c),'f acts freely on C')
 y=next(i for i in e if i not in inter)
 complement=set(adj)-c
 require({next(iter(support(N,i,y))) for i in c}==complement,'regular complementary C module')
 require(all(support(N,i,j)<=complement and support(N,j,i)<=complement for i,j in itertools.product(c,complement)),'complement C bimodule')
 fy=next(iter(support(N,f,y)))
 require(support(N,y,y)&complement=={y,fy} and N[y][y][y]==N[y][y][fy]==1,'projected square is Y+fY')
 rows.append(dict(id=a['id'],input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),canonical_tau=tau,shared_invertible=f,subcategories=[list(s) for s in subcats],rank4_models=[model,model],adjoint=adj,tau_swaps_subcategories=True,shared_invertible_is_not_tau=True,relative_factorization_hypotheses_verified=True))
print(json.dumps(rows,indent=2));(OUT/'subcategories_receipt.json').write_text(json.dumps(rows,indent=2)+'\n')
