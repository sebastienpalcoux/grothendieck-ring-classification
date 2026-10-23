"""Standard-library replay of a two-character central-restriction obstruction.

No character discovery, column enumeration, floating point or solver is used.
General-complex scope requires the separately replayed signed/Galois bridge.
"""
from pathlib import Path
from fractions import Fraction as Q
import gzip,json,hashlib,itertools,time
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
DATA={
 'R11_1_3':([4,5,6,7],[1,1,1,0,'-q','q','q','-q',0,1,-2]),
 'R11_1_52':([4,5,7,8],[1,1,1,0,'-q','q',-2,'q','-q',0,1]),
 'R11_1_142':([1,2,3,4],[1,'q','q','-q','-q',-2,1,0,1,1,0]),
 'R11_1_149':([3,4,5,6],[1,1,1,'q','q','-q','-q',0,-2,0,1]),
}
def need(v,msg):
 if not v:raise ValueError(msg)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def mul(a,b):return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def total(v):
 z=(Q(0),Q(0))
 for x in v:z=add(z,x)
 return z
def scalar(x):return (Q(x),Q(0))
def conj(x):return(x[0],-x[1])
def check_character(R,row):
 n=len(R);du=[next(j for j in range(n)if R[i][j][0])for i in range(n)]
 need(row[0]==scalar(1),'unit character')
 for i,j in itertools.product(range(n),repeat=2):need(mul(row[i],row[j])==total(row[k]for k in range(n)if R[i][j][k]),'all product identities')
 return total(mul(row[i],row[du[i]])for i in range(n))

def verify():
 out=[]
 for line_no,line in enumerate(gzip.open(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz','rt'),1):
  id=f'R11_1_{line_no}'
  if id not in DATA:continue
  R=json.loads(line.replace('{','[').replace('}',']'));n=len(R);need(n==11 and all(x in(0,1) for A in R for row in A for x in row),'rank11 M1')
  X,raw=DATA[id];du=[next(j for j in range(n)if R[i][j][0])for i in range(n)];G=[i for i in range(n)if sum(R[i][du[i]])==1];Y=[i for i in range(n)if i not in G+X]
  need(len(G)==4 and len(X)==4 and len(Y)==3 and 0 in G and not set(G)&set(X),'dimension classes')
  dims=[scalar(1) if i in G else scalar(2) if i in Y else(Q(2),Q(2)) for i in range(n)]
  D=check_character(R,dims);need(D==(64,32),'FP global dimension')
  chi=[conj(x)for x in dims];fchi=check_character(R,chi);need(fchi==(64,-32),'conjugate formal codegree')
  phi=[(Q(0),Q(1)) if x=='q' else(Q(0),Q(-1)) if x=='-q' else scalar(x)for x in raw]
  fphi=check_character(R,phi);need(fphi==scalar(16),'second formal codegree')
  betachi=(Q(3),Q(2));betaphi=(Q(4),Q(2))
  need(mul(betachi,fchi)==D and mul(betaphi,fphi)==D,'central dimensions')
  need(all(phi[i]!=(0,0) for i in X),'nonzero second character on all possible X')
  # Coefficient of sqrt2 forces exactly one X in each restriction.
  # Unit multiplicity one leaves zero rational weight for beta_chi and
  # rational weight one for beta_phi: exactly one other invertible g.
  for x in X:
   need(add(scalar(1),dims[x])==betachi,'all first restrictions')
   for g,y in itertools.product([g for g in G if g!=0],X):
    need(total([scalar(1),dims[g],dims[y]])==betaphi,'all second restrictions')
    c=total([scalar(1),chi[g],chi[y]])
    need(c==(4,-2),'constant conjugate evaluation')
    need(mul(betachi,c)==betaphi,'left reciprocity equals beta_phi')
    need(mul(betaphi,add(scalar(1),phi[x]))!=betaphi,'right reciprocity contradicts nonzero phi(X)')
  out.append(dict(id=id,tensor_sha256=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),scope='general_complex_after_separately_verified_signed_Galois_reduction',criterion='two_character_central_restriction',invertibles=G,two_dimensional=Y,dimension_2_plus_2_sqrt2=X,character_phi=raw,formal_codegrees=['64-32*sqrt(2)','16'],central_dimensions=['3+2*sqrt(2)','4+2*sqrt(2)'],possible_first_restrictions=4,possible_second_restrictions=12,reciprocity_contradictions=48))
 need(len(out)==4,'all four inputs')
 return out
if __name__=='__main__':
 start=time.monotonic();out=verify();(P/'two_character_certificates.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',count=len(out),seconds=time.monotonic()-start,ids=[r['id']for r in out]),indent=2),flush=True)
