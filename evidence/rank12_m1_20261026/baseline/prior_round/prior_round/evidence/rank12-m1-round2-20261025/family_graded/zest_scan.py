from pathlib import Path
import json,sys,itertools,collections,time
BASE=Path(__file__).resolve().parents[2]/'rank12-m1-offline-20261025';OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(BASE/'sources/work/models'),str(BASE/'sources/work/rank11')]
import common
from match_models import prod,group,rep_dihedral
from extra_models import metaplectic
D=json.loads((BASE/'tensors.json').read_text());F={r['id']:r['family']for r in json.loads((BASE/'unresolved_families.json').read_text())['records']if r['family']in ['D24','D40','D32']}

def cocycles(K):
 n=len(K);vars=[(a,b)for a in range(1,n)for b in range(1,n)];ix={ab:i for i,ab in enumerate(vars)};rows=[]
 def bit(a,b):return 1<<ix[a,b]if a and b else 0
 for a,b,c in itertools.product(range(n),repeat=3):rows.append(bit(a,b)^bit(K[a][b],c)^bit(b,c)^bit(a,K[b][c]))
 piv={}
 for row in rows:
  while row:
   p=row.bit_length()-1
   if p in piv:row^=piv[p]
   else:piv[p]=row;break
 free=[i for i in range(len(vars))if i not in piv]
 for val in range(1<<len(free)):
  x=sum(((val>>j)&1)<<a for j,a in enumerate(free))
  for p,row in sorted(piv.items()):
   if (row&x).bit_count()%2:x^=1<<p
  M=[[0]*n for _ in range(n)]
  for (a,b),i in ix.items():M[a][b]=(x>>i)&1
  assert all((M[a][b]+M[K[a][b]][c]-M[b][c]-M[a][K[b][c]])%2==0 for a,b,c in itertools.product(range(n),repeat=3))
  yield M

def zest(R,deg,h,lam):
 n=len(R);act=[row.index(1)for row in R[h]];T=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,j,k in itertools.product(range(n),repeat=3):T[i][j][act[k]if lam[deg[i]][deg[j]]else k]=R[i][j][k]
 return T

def main():
 buckets=collections.defaultdict(list)
 for rid in F:buckets[common.coarse(D[rid])].append(rid)
 candidates=[]
 for orders in [(4,),(2,2)]:
  P=group(orders);K=[[row.index(1)for row in A]for A in P];R=prod(rep_dihedral(3),P);candidates.append(('Rep(S3) x Vec'+str(orders),R,[i%4 for i in range(12)],4,K,dict(base='Rep(S3) x Vec',orders=list(orders),central_boson=4)))
 R=prod(metaplectic(5),group((2,)));K=[[a^b for b in range(4)]for a in range(4)];deg=[2*int(i//2 in [2,3])+i%2 for i in range(12)];candidates.append(('SO(5)_2 x Vec(C2)',R,deg,2,K,dict(base='SO(5)_2 x Vec(C2)',central_boson=2)))
 sys.path.insert(0,str(BASE));import additional_models as add
 for name,R,kind,par,h in add.candidates():
  if kind!='metaplectic_character_crossed_product':continue
  deg=[2*int(par['labels'][i%6][0]==[5])+i//6 for i in range(12)]
  candidates.append((name,R,deg,h,K,dict(base=kind,base_parameters=par,central_boson=h)))
 sys.path.insert(0,str(BASE/'sources/work/rank11/known_models'));from standard import cyclic_equivariant
 from match_models import ty
 for parity in [0,1]:
  pp=[0]*5+[parity];R,labs=cyclic_equivariant(ty((5,)),[0,4,3,2,1,5],4,pp)
  # The canonical order-two character of C4 is central and has trivial self-braiding.
  # Ring is C2xC2 graded by TY parity and parity of the C4 character.
  # First retain the unmodified C4 equivariantization; further gradings below.
  for rid in F:
   p=common.based_iso(D[rid],R)
   if p is not None:print('CYCLIC DIRECT HIT',rid,parity,flush=True)
  K0=([[a^b for b in range(4)]for a in range(4)]if parity==0 else[[(a+b)%4 for b in range(4)]for a in range(4)])
  deg0=([2*int(O==[5])+(j%2)for O,j in labs]if parity==0 else[(2*j+int(O==[5]))%4 for O,j in labs])
  common.require(all(deg0[k]==K0[deg0[i]][deg0[j]]for i,j,k in itertools.product(range(12),repeat=3)if R[i][j][k]),'C4 equivariantization grading')
  candidates.append(('TY(C5)^C4, parity='+str(parity),R,deg0,2,K0,dict(base='TY_C5_C4_equivariant',parity=parity,labels=labs,central_boson=2)))
 out={};attempts=[];seen=set()
 for name,R,deg,h,K,par in candidates:
  for lam in cocycles(K):
   M=zest(R,deg,h,lam);sha=common.sha(M)
   if sha in seen:continue
   seen.add(sha);common.validate(M);hits=[]
   for rid in buckets[common.coarse(M)]:
    p=common.based_iso(D[rid],M)
    if p is None:continue
    hits.append(rid)
    out.setdefault(rid,[]).append(dict(name='Bosonic group-graded zest of '+name,constructor='central_boson_group_zest',parameters=dict(**par,base_tensor=R,grading_group_table=K,grading=deg,cocycle=lam),model_tensor=M,basis_map_source_to_model=p))
   attempts.append(dict(base=name,sha=sha,matches=hits))
 (OUT/'zest_results.json').write_text(json.dumps([dict(id=rid,family=F[rid],models=ms)for rid,ms in out.items()],indent=2)+'\n');(OUT/'zest_attempts.json').write_text(json.dumps(attempts,indent=2)+'\n');print('HITS',len(out),list(out), 'candidates',len(attempts),flush=True)
if __name__=='__main__':main()
