from zest_models import *
def central_extension_tensor(R,d,h,p,q,r):
 a=len(R);n=2*a;act=[M[h].index(1)for M in R]
 T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,j,k in itertools.product(range(n),repeat=3):
  x,e=divmod(i,2);y,f=divmod(j,2);z,t=divmod(k,2)
  shift=(p*d[x]*d[y]+q*e*f+r*e*d[y])%2
  T[i][j][k]=R[x][y][act[z]if shift else z]*int(t==(e^f))
 return T

def central_group(p,q,r):
 # (central bit,u bit,v bit), multiply normal forms z^c u^a v^e.
 labs=list(itertools.product(range(2),repeat=3));ix={a:i for i,a in enumerate(labs)}
 return [[ix[((c+d+p*a*b+q*e*f+r*e*b)%2,a^b,e^f)]for d,b,f in labs]for c,a,e in labs]

def run():
 source=OUT/'known_models_group.json'
 if not source.exists():source=OUT/'known_models_zested.json'
 known=json.load(open(source));lookup={x['id']:x for x in known};by=collections.defaultdict(list)
 for n in[9,10]:
  for i,R in enumerate(read(n),1):by[(n,coarse(R))].append((f'R{n}_1_{i}',R))
 new=[];bases=[('SU(2)_4',su2(4),[0,1,0,1,0],4)]
 # Other rank5 braided groups have no nontrivial grading; central extensions reduce to ordinary zests.
 for name,R,d,h in bases:
  for p,q,r in itertools.product(range(2),repeat=3):
   T=central_extension_tensor(R,d,h,p,q,r);G=central_group(p,q,r)
   assert all(G[G[a][b]][c]==G[a][G[b][c]]for a,b,c in itertools.product(range(8),repeat=3))
   for rid,S in by[(len(T),coarse(T))]:
    bm=based_iso(S,T)
    if bm is None:continue
    if rid not in lookup:lookup[rid]={'id':rid,'tensor_sha256':tensor_hash(S),'status':'unitarily_realized','models':[]};new.append(rid)
    rec={'model':f'Central-extension quotient of {name}, parameters({p},{q},{r})','constructor':'central_extension_quotient','parameters':{'base_name':name,'base_tensor':R,'grading':d,'central_boson':h,'p':p,'q':q,'r':r,'central_extension_group_table':G},'reference':'Full matching-grading subcategory of C x Vec(E), then modules for diagonal central boson1+(h,z); z central order2; coefficient formula from freeorbits','basis_map_source_to_model':bm,'model_tensor':T}
    lookup[rid]['models'].append(rec);print(rid,(p,q,r),flush=True)
 known=sorted(lookup.values(),key=lambda x:tuple(map(int,x['id'].replace('R','').split('_'))))
 (OUT/'known_models_central.json').write_text(json.dumps(known,indent=2)+'\n');print('NEW',new)
if __name__=='__main__':run()
