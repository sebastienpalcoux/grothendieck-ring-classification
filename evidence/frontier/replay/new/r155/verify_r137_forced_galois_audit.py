"""Independent standard-library replay of R137's frozen new restrictions/witnesses."""
from pathlib import Path
from fractions import Fraction as Q
from math import gcd,lcm,isqrt
from itertools import combinations_with_replacement
import gzip,json,hashlib,runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1];PRIOR=ROOT/'prior';NEW=ROOT/'new/r137'
def ck(x,msg):
 if not x:raise ValueError(msg)
T=runpy.run_path(str(PRIOR/'data/current_remaining_cases.py'))['TENSORS']['R9_2_137'];n=len(T)
dual=[next(j for j in range(n)if T[i][j][0])for i in range(n)]
G=[[sum(T[a][j][k]*T[k][dual[a]][i]for a in range(n)for k in range(n))for j in range(n)]for i in range(n)]
bcol=[1,0,0,1,1,1,1,0,0]
H=[[G[i][j]-int(i==j==0)-bcol[i]*bcol[j]for j in range(n)]for i in range(n)]
B=[[Q(t)for t in row]+[Q(i==j)for j in range(n)]for i,row in enumerate(H)]
for i in range(n):
 k=next(k for k in range(i,n)if B[k][i]);B[k],B[i]=B[i],B[k]
 t=B[i][i];ck(t>0,'residual Gram positive pivot');B[i]=[x/t for x in B[i]]
 for k in range(n):
  if k!=i:
   t=B[k][i];B[k]=[x-t*y for x,y in zip(B[k],B[i])]
Gi=[r[n:]for r in B]
def norm(v):return sum(v[i]*Gi[i][j]*v[j]for i in range(n)for j in range(n))
def phi(n):
 r=n;p=2
 while p*p<=n:
  if n%p==0:
   r=r//p*(p-1)
   while n%p==0:n//=p
  p+=1
 if n>1:r=r//n*(n-1)
 return r
def mu(n):
 sg=1;p=2
 while p*p<=n:
  if n%p==0:
   n//=p;sg=-sg
   if n%p==0:return 0
  p+=1
 return -sg if n>1 else sg
def kr8(a):return 0 if a%2==0 else(1 if a%8 in(1,7)else-1)
def trace(o,sg):
 ts=[]
 for k in range(1,5):
  g=gcd(o,k);nn=o//g;a=Q(mu(nn),phi(nn));b=Q(0)
  if nn%8==0 and gcd(nn//8,8)==1:b=Q(sg*mu(nn//8)*kr8(nn//8)*kr8(k//g)*2,phi(nn))
  ts.append((a,b))
 return tuple(ts)
def orbit(o):
 N=lcm(o,8)
 return len({a*a%o for a in range(N)if gcd(a,N)==1 and kr8(a)==1})
minimum={}
for a in range(7):
 for b in range(4):
  o=2**a*3**b;k=orbit(o)
  for sg in(-1,1):
   t=trace(o,sg);minimum[t]=min(k,minimum.get(t,10**6))
zero=tuple([(Q(0),Q(0))]*4)
ck(minimum[zero]==3,'zero trace minimum orbit')
ck(orbit(64)==4 and orbit(27)==9,'outside-box orbit lower-bound bases')
pairs=list(combinations_with_replacement(range(n),2));diags=[pairs.index((i,i))for i in range(n)]
results=[]
for tau,sg in((1,'plus'),(-1,'minus')):
 oldpath=PRIOR/f'evidence/unresolved7_20261027/audit_parity/R137_tau_{sg}_positive_fs2_system.json.gz'
 oldbytes=oldpath.read_bytes();old=json.loads(gzip.decompress(oldbytes))
 newpath=NEW/f'R137_tau_{sg}_forced_galois_replay.json.gz';new=json.loads(gzip.decompress(newpath.read_bytes()))
 ck(new['source_sha256']==hashlib.sha256(oldbytes).hexdigest(),'frozen old system hash')
 A,b=new['A'],new['b'];Ao,bo=old['A'],old['b'];no=len(Ao[0]);nr=len(Ao)
 ck(len(A)==nr+12 and len(A[0])==no+8,'new system size')
 ck(A[:nr]==[r+[0]*8 for r in Ao]and b[:nr]==bo,'all old equations unchanged')
 mapping=new['physical_mapping'];indices=[x[0]for x in mapping];ck(len(indices)==len(set(indices)),'distinct mapping labels')
 physical={j for j in range(no)if any(Ao[r][j]for r in range(45))}
 ck(set(indices)==physical,'complete physical variable map')
 removed=[];fourth=[[Q(0)]*no for _ in range(4)];nc={}
 for j,v,k,ns,tts in mapping:
  v=tuple(v);tt=tuple(tuple(Q(x)for x in z)for z in tts)
  ck(len(v)==n and all(isinstance(x,int)and x>=0 for x in v),'restriction vector')
  for i,r in enumerate(diags):ck(Ao[r][j]*G[i][i]==bo[r]*v[i]**2,'full vector matches old Gram diagonals')
  for r,(i,ii)in enumerate(pairs):
   if G[i][ii]:ck(Ao[r][j]*G[i][ii]==bo[r]*v[i]*v[ii],'old Gram offdiagonals')
   else:ck(v[i]*v[ii]==0,'zero Gram position')
  if v not in nc:nc[v]=norm(v)
  ck(Q(ns)==nc[v],'exact whole-vector Gram norm')
  ck(k==minimum[tt],'minimum square-Galois orbit')
  if k*nc[v]>1 and v[0]==0:removed.append(j)
  if v[0] and (sum(v[i]*(4 if i in(3,4,5,6)else(2 if i==8 else 1))for i in range(n)),3*sum(v[i]for i in(3,4,5,6)))==(17,12) and v!=tuple(bcol):removed.append(j)
  z=(sum(v[i]*(4 if i in(3,4,5,6)else(2 if i==8 else 1))for i in range(n)),3*sum(v[i]for i in(3,4,5,6)))
  rad=z[0]*tt[3][1]+z[1]*tt[3][0]
  for row,i in zip(fourth,(3,4,5,6)):row[j]=v[i]*rad
 ck(sorted(removed)==sorted(new['removed_columns']),'complete exact removal list')
 for ri,row in enumerate(fourth):
  den=lcm(*(x.denominator for x in row));ck(den==4,'discrete projected branch scale')
  for si,sign in enumerate((1,-1)):
   rownum=nr+2*ri+si;expected=[int(sign*x*den)for x in row]+[0]*8;expected[no+2*ri+si]=1
   ck(A[rownum]==expected and b[rownum]==384*den,'fresh quartic bound row')
  expected=[0]*(no+8);expected[no+2*ri]=1
  ck(A[nr+8+ri]==expected and b[nr+8+ri]==768,'fresh projected indicator branch row')
 witness={j:Q(x)for j,x in new['witness']};ck(all(x>=0 for x in witness.values()),'nonnegative exact witness')
 ck(all(not witness.get(j,0)for j in removed),'no deleted column used')
 ck(all(sum(r[j]*x for j,x in witness.items())==y for r,y in zip(A,b)),'every equation exactly satisfied')
 for row in fourth:ck(sum(row[j]*x for j,x in witness.items()if j<no)==192,'projected fourth indicator exactly2')
 results.append({'TY_sign':tau,'physical_variables_checked':len(mapping),'removed':len(removed),'exact_witness_support':len(witness),'all_equations':len(A),'replay_sha256':hashlib.sha256(newpath.read_bytes()).hexdigest()})
receipt={'result':'PASS','scope':'Whole-vector Galois filter, quartic projected constraints, complete frozen rational witnesses; not categorification','systems':results}
(HERE/'r137_forced_galois_audit_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
