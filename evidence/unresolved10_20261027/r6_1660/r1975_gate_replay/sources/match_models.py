from pathlib import Path
import json,gzip,itertools,hashlib,collections
import numpy as np
BASE=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
REPO=BASE/'repositories/classification-sparse'
def read(n):
 return [json.loads(x.replace('{','[').replace('}',']')) for x in gzip.open(BASE/f'inputs/rank{n}_M1_verified/FusionRingMultiplicationTables.txt.gz','rt') if x.strip()]
def tensor_hash(R):return hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
def signature(R):
 n=len(R);du=[next(j for j in range(n) if R[i][j][0]) for i in range(n)]
 return [(i==0,du[i]==i,tuple(sorted(sum(r) for r in R[i])),tuple(sorted(sum(R[j][i]) for j in range(n))),tuple(sorted(R[i][du[i]])),sum(R[i][j][j] for j in range(n))) for i in range(n)]
def coarse(R):return tuple(sorted(signature(R)))
def based_iso(A,B):
 n=len(A)
 if len(B)!=n:return None
 sa,sb=signature(A),signature(B)
 if sorted(sa)!=sorted(sb):return None
 ca=[{j for j in range(n) if sa[i]==sb[j]} for i in range(n)]
 p={0:0};used={0};duA=[next(j for j in range(n) if A[i][j][0]) for i in range(n)];duB=[next(j for j in range(n) if B[i][j][0]) for i in range(n)]
 def okay(i,j):
  if A[i][i][i]!=B[j][j][j]:return False
  if duA[i] in p and duB[j]!=p[duA[i]]:return False
  for a,b in p.items():
   if (A[i][i][a],A[i][a][i],A[a][i][i])!=(B[j][j][b],B[j][b][j],B[b][j][j]):return False
   for c,d in p.items():
    if (A[i][a][c],A[a][i][c],A[a][c][i])!=(B[j][b][d],B[b][j][d],B[b][d][j]):return False
  return True
 def dfs():
  if len(p)==n:return [p[i] for i in range(n)]
  best=None;choices=None
  for i in range(n):
   if i in p:continue
   cs=[j for j in ca[i]-used if okay(i,j)]
   if not cs:return None
   if choices is None or len(cs)<len(choices):best,choices=i,cs
  for j in choices:
   p[best]=j;used.add(j)
   z=dfs()
   if z is not None:return z
   del p[best];used.remove(j)
  return None
 result=dfs()
 if result is not None:
  assert all(A[i][j][k]==B[result[i]][result[j]][result[k]] for i,j,k in itertools.product(range(n),repeat=3))
 return result

def group(orders):
 els=list(itertools.product(*(range(a) for a in orders)));ix={a:i for i,a in enumerate(els)};n=len(els)
 return [[[int(ix[tuple((a+b)%m for a,b,m in zip(els[i],els[j],orders))]==k) for k in range(n)] for j in range(n)] for i in range(n)]
def pointed_dihedral(m):
 els=list(itertools.product(range(2),range(m)));ix={a:i for i,a in enumerate(els)};n=2*m
 return [[[int(ix[((a+c)%2,(b+(-1)**a*d)%m)]==k) for k in range(n)] for c,d in els] for a,b in els]
def ty(orders):
 G=group(orders);g=len(G);n=g+1;R=[[[0]*n for _ in range(n)]for _ in range(n)]
 for i,j,k in itertools.product(range(g),repeat=3):R[i][j][k]=G[i][j][k]
 for i in range(g):R[i][g][g]=R[g][i][g]=R[g][g][i]=1
 return R

def prod(A,B):
 a,b=len(A),len(B);n=a*b
 return [[[A[i//b][j//b][k//b]*B[i%b][j%b][k%b] for k in range(n)]for j in range(n)]for i in range(n)]
def su2(k,even=False):
 labs=list(range(0,k+1,2 if even else 1))
 return [[[int(abs(a-b)<=c<=min(a+b,2*k-a-b) and (a+b+c)%2==0) for c in labs]for b in labs]for a in labs]
def rep_dihedral(m,dic=False):
 # D_{2m}, order2m; Dic_{m/2}, order2m if m even.
 assert not dic or m%2==0
 l=4 if m%2==0 else 2;q=m//2-1 if l==4 else (m-1)//2;n=l+q
 R=[[[0]*n for _ in range(n)]for _ in range(n)]
 cyclic=bool(dic and (m//2)%2)
 for x,y in itertools.product(range(l),repeat=2):R[x][y][(x+y)%4 if cyclic else x^y]=1
 for x in range(l):
  flip=x%2 if cyclic else x//2
  for k in range(1,q+1):
   kk=m//2-k if flip else k
   R[x][l+k-1][l+kk-1]=R[l+k-1][x][l+kk-1]=1
 for k,j in itertools.product(range(1,q+1),repeat=2):
  for a in (k+j,abs(k-j)):
   if a==0:
    R[l+k-1][l+j-1][0]+=1;R[l+k-1][l+j-1][2 if cyclic else 1]+=1
   elif l==4 and a==m//2:
    R[l+k-1][l+j-1][1 if cyclic else 2]+=1;R[l+k-1][l+j-1][3]+=1
   else:R[l+k-1][l+j-1][l+min(a,m-a)-1]+=1
 return R

def models():
 for orders in [(9,),(3,3),(10,)]:yield ('Vec('+ 'x'.join('C'+str(x)for x in orders)+')',group(orders),'pointed',{'orders':orders},'EGNO, Tensor Categories, pointed categories')
 yield ('Vec(D10)',pointed_dihedral(5),'pointed_dihedral',{'m':5},'Pointed fusion category for the dihedral group of order10')
 for orders in [(8,),(4,2),(2,2,2),(9,),(3,3)]:yield('TY('+ 'x'.join('C'+str(x)for x in orders)+')',ty(orders),'ty',{'orders':orders},'Tambara--Yamagami, J Algebra209(1998), Theorem1; a nondegenerate symmetric bicharacter and positive tau give a unitary category')
 for k,even in [(8,False),(16,True),(17,True),(9,False),(18,True),(19,True)]:yield (('PSU'if even else 'SU')+f'(2)_{k}',su2(k,even),'su2',{'level':k,'even':even},'Standard unitary SU(2) level k category and its even subcategory')
 for m in [12,15,14,17]:
  yield(f'Rep(D{2*m})',rep_dihedral(m),'rep_dihedral',{'m':m},'Character ring of the dihedral group of order '+str(2*m))
  if m%2==0:yield(f'Rep(Dic{m//2})',rep_dihedral(m,True),'rep_dicyclic',{'m':m},'Character ring of the dicyclic group of order '+str(2*m))
 rank3=[('Vec(C3)',group((3,)),{'kind':'pointed','orders':[3]}),('Ising',ty((2,)),{'kind':'ty','orders':[2]}),('Rep(S3)',rep_dihedral(3),{'kind':'rep_dihedral','m':3}),('PSU(2)_5',su2(5,True),{'kind':'su2','level':5,'even':True})]
 for i,(a,A,pa) in enumerate(rank3):
  for b,B,pb in rank3[i:]:yield(a+' x '+b,prod(A,B),'deligne_product',{'left':pa,'right':pb},'Deligne product of the indicated standard unitary rank3 models')
 rank5=json.load(open(REPO/'supplements/rank8/data/lower_rank_positive_models.json'))
 for rec in rank5:
  B=rec['tensor']
  if len(B)!=5 or max(v for M in B for row in M for v in row)>1:continue
  for a,A in [('Vec(C2)',group((2,))),('Fib',[[[1,0],[0,1]],[[0,1],[1,1]]])]:
   yield(a+' x '+rec['name'],prod(A,B),'deligne_product_registry',{'left':a,'right_name':rec['name'],'right_tensor':B,'registry_sha256':tensor_hash(B)},'Deligne product; '+rec['reference'])

def run():
 ms=list(models());out=[];remaining=[]
 by=collections.defaultdict(list)
 for name,R,kind,pars,ref in ms:
  if len(R) not in [9,10]:raise ValueError(name)
  by[(len(R),coarse(R))].append((name,R,kind,pars,ref))
 for n in [9,10]:
  for idx,R in enumerate(read(n),1):
   rid=f'R{n}_1_{idx}';matches=[]
   for name,M,kind,pars,ref in by[(n,coarse(R))]:
    p=based_iso(R,M)
    if p is not None:matches.append({'model':name,'constructor':kind,'parameters':pars,'reference':ref,'basis_map_source_to_model':p,'model_tensor':M})
   if matches:out.append({'id':rid,'tensor_sha256':tensor_hash(R),'status':'unitarily_realized','models':matches});print(rid,[x['model'] for x in matches],flush=True)
   else:remaining.append(rid)
 (OUT/'known_models.json').write_text(json.dumps(out,indent=2)+'\n');(OUT/'unmatched.json').write_text(json.dumps(remaining,indent=2)+'\n')
 print('TOTAL',collections.Counter(x['id'].split('_')[0]for x in out),'UNMATCHED',len(remaining))
 return out
if __name__=='__main__':run()
