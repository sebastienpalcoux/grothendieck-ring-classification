"""Independent Hamilton-coordinate and exact U(2) replay; read-only. Requires SymPy."""
from pathlib import Path
import json,itertools,hashlib,sys,gzip
p=Path(__file__).resolve().parents[1]
# Order: (1,triv),(1,sign),(1,std),(z,triv-projective),(z,sign-projective),(z,std-projective),X.
ch=[(1,1,1),(1,-1,1),(2,0,-1)];weights=(1,3,2)
T=[[[0]*7 for _ in range(7)]for _ in range(7)]
def require(x,m):
 if not x:raise ValueError(m)
for i,j in itertools.product(range(7),repeat=2):
 if i<6 and j<6:
  a,r=divmod(i,3);b,s=divmod(j,3)
  for t in range(3):
   z=sum(weights[k]*ch[r][k]*ch[s][k]*ch[t][k]*(ch[1][k]if a==b==1 else 1)for k in range(3))
   require(z>=0 and z%6==0,'character product');T[i][j][3*(a^b)+t]=z//6
 elif i==j==6:T[i][j]=[1,1,2,1,1,2,4]
 else:T[i][j][6]=ch[(j if i==6 else i)%3][0]
require(all(sum(T[i][j][s]*T[s][k][l]for s in range(7))==sum(T[j][k][s]*T[i][s][l]for s in range(7))for i,j,k,l in itertools.product(range(7),repeat=4)),'associativity')
d=next(x for x in json.loads((p/'output/rank7_ledger.json').read_text())if x['id']=='R7_4_2019');R=d['tensor']
q=next(((0,)+tail for tail in itertools.permutations(range(1,7)) if all(T[i][j][k]==R[((0,)+tail)[i]][((0,)+tail)[j]][((0,)+tail)[k]] for i,j,k in itertools.product(range(7),repeat=3))),None)
require(q is not None,'census tensor differs')
q=list(q)
require(all(T[i][j][k]==R[q[i]][q[j]][q[k]]for i,j,k in itertools.product(range(7),repeat=3)),'full343coefficientmatch')
# Hamilton quaternion coordinates give an independent free-orbit/fiber check.
Q=[tuple(s*int(j==i)for j in range(4))for s in(1,-1)for i in range(4)]
def mul(a,b):
 w,x,y,z=a;v,i,j,k=b;return(w*v-x*i-y*j-z*k,w*i+x*v+y*k-z*j,w*j-x*k+y*v+z*i,w*k+x*j-y*i+z*v)
def parity(q):return sum(q[i]>q[j]for i in range(3)for j in range(i+1,3))%2
def act(q,a):
 out=[a[0],0,0,0]
 for i in range(3):out[1+q[i]]=(-1)**parity(q)*a[1+i]
 return tuple(out)
S3=list(itertools.permutations(range(3)));noncentral=[a for a in Q if a[0]==0]
for target in Q:
 fibre={(a,b)for a,b in itertools.product(noncentral,repeat=2)if mul(a,b)==target}
 if target[0]:
  require(len(fibre)==6,'centralfiberlength')
  ab=next(iter(fibre));require({(act(q,ab[0]),act(q,ab[1]))for q in S3}==fibre,'centralfiberregularS3set')
 else:require(len(fibre)==4,'noncentralcoefficient')
raw=gzip.open(p/'data/rank7_tables.txt.gz','rb').read()
rings=[json.loads(l.replace('{','[').replace('}',']'))for l in raw.decode().splitlines()if l.strip()]
require(rings.count(R)==1,'raw census source absent or duplicated')
report={'raw_source_sha256':hashlib.sha256(raw).hexdigest(),'status':'PASS','id':d['id'],'model_to_census':q,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'coefficients':343,'central_fibers':'regularS3 at both1,z','noncentral_fiber_cardinality':4,'model_tensor':T}
require(report==json.loads((p/'data/r7_4_2019_independent_audit.json').read_text()),'independent audit receipt mismatch')
print({k:v for k,v in report.items()if k!='model_tensor'})

# Independent exact U(2) representation check.
import sympy as sp
I=sp.eye(2);qi=sp.diag(sp.I,-sp.I);qj=sp.Matrix([[0,1],[-1,0]]);qk=qi*qj
r=-(I+qi+qj+qk)/2;s=sp.I*(qi-qj)/sp.sqrt(2)
zero=lambda M:all(sp.simplify(x)==0 for x in M)
require(zero(r**3-I) and zero(s**2-I) and zero(s*r*s-r**2),'S3 presentation')
require(zero(r*qi*r.inv()-qj) and zero(r*qj*r.inv()-qk),'cycle conjugation')
require(zero(s*qi*s.inv()+qj) and zero(s*qj*s.inv()+qi) and zero(s*qk*s.inv()+qk),'signed transposition')
require(sp.simplify(r.det())==1 and sp.simplify(s.det())==-1,'determinants')
print('Exact U2 embedding and standard S3 restriction: PASS')
