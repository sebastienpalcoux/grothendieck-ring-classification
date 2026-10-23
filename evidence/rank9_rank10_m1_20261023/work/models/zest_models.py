from extra_models import *
def gradings(R):
 n=len(R)
 for bits in itertools.product(range(2),repeat=n-1):
  g=(0,)+bits
  if any(g) and all(g[k]==(g[i]^g[j])for i,j,k in itertools.product(range(n),repeat=3)if R[i][j][k]):yield list(g)
def zest(R,g,h):
 n=len(R);act=[]
 for i in range(n):
  assert sum(R[h][i])==1;act.append(R[h][i].index(1))
 assert act[0]==h and act[h]==0 and all(R[h][i]==R[i][h]for i in range(n)) and g[h]==0
 T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,j,k in itertools.product(range(n),repeat=3):T[i][j][act[k]if g[i]*g[j]else k]=R[i][j][k]
 return T

def braided_models():
 for name,R,kind,pars,ref in models():
  if kind=='ty' and any(a!=2 for a in pars['orders']):continue
  if kind=='deligne_product_registry' and pars['right_name'] in ['TY(C4)','LPR-12','LPR-24']:continue
  yield name,R,kind,pars,ref
 for N in [11,13]:yield f'SO({N})_2',metaplectic(N),'odd_metaplectic',{'N':N},'Unitary standard odd metaplectic category'
 for name,R in [('Ising',ty((2,))),('Rep(S3)',rep_dihedral(3))]:yield f'({name} x {name})^C2_swap',permutation_equivariant(R),'permutation_equivariant',{'base_name':name,'base_tensor':R},'Braided C2-equivariantization by canonical swap'

def run():
 data=json.load(open(OUT/'known_models_extended.json'));lookup={x['id']:x for x in data};by=collections.defaultdict(list)
 for n in [9,10]:
  for i,R in enumerate(read(n),1):by[(n,coarse(R))].append((f'R{n}_1_{i}',R))
 new=[]
 for name,R,kind,pars,ref in braided_models():
  variants=[(R,{'kind':kind,'parameters':pars},name)]
  n=len(R)
  for g in gradings(R):
   for h in range(1,n):
    if g[h] or R[h][h][0]!=1 or sum(R[h][h])!=1:continue
    T=zest(R,g,h)
    variants.append((T,{'kind':'associative_C2_zest','base_constructor':kind,'base_parameters':pars,'base_name':name,'base_tensor':R,'grading':g,'central_invertible':h},f'C2-zest({name}; h={h}, degree={g})'))
  for T,p,model in variants:
   for rid,S in by[(n,coarse(T))]:
    bm=based_iso(S,T)
    if bm is None:continue
    if rid not in lookup:
     lookup[rid]={'id':rid,'tensor_sha256':tensor_hash(S),'status':'unitarily_realized','models':[]};new.append(rid)
    rec={'model':model,'constructor':p['kind'],'parameters':p,'reference':ref+'; associative zesting DGP Definition3.2/Proposition3.4, lambda(a,b)=h^{ab}, tau=1 for boson and i^{abc} for fermion','basis_map_source_to_model':bm,'model_tensor':T}
    if not any(c['constructor']==rec['constructor']for c in lookup[rid]['models']):lookup[rid]['models'].append(rec)
    print(rid,model,flush=True)
 data=sorted(lookup.values(),key=lambda x:tuple(map(int,x['id'].replace('R','').split('_'))))
 (OUT/'known_models_zested.json').write_text(json.dumps(data,indent=2)+'\n')
 print('NEW',new,'TOTAL',collections.Counter(x['id'].split('_')[0]for x in data))
if __name__=='__main__':run()
