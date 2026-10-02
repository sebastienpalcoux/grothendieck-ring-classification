"""Independent exact replay: Python integer contractions, no NumPy/SciPy/repository imports."""
import json,hashlib,itertools
from pathlib import Path
from fractions import Fraction
import sympy as sy
HERE=Path(__file__).resolve().parent
t=sy.Symbol('t')
def check(x,msg):
 if not x:raise RuntimeError(msg)
def sign(co,f,interval):
 co=[Fraction(str(x)) for x in co];lo,hi=map(Fraction,interval)
 for _ in range(100):
  a=b=Fraction(0)
  for c in co:
   vals=[a*lo,a*hi,b*lo,b*hi];a,b=min(vals)+c,max(vals)+c
  if a>0:return 1
  if b<0:return -1
  if not any(co):return 0
  check(lo!=hi,'zero algebraic sign')
  x,y=f.refine_root(sy.Rational(lo.numerator,lo.denominator),sy.Rational(hi.numerator,hi.denominator),steps=4);lo,hi=Fraction(str(x)),Fraction(str(y))
 raise RuntimeError('sign interval did not separate')
def contract(M,v,n):
 def at(a,b,c):return (a*n+b)*n+c
 w=[0]*(n**3)
 for a,b,c in itertools.product(range(n),repeat=3):w[at(a,b,c)]=sum(M[c][z]*v[at(a,b,z)] for z in range(n))
 u=[0]*(n**3)
 for a,b,c in itertools.product(range(n),repeat=3):u[at(a,b,c)]=sum(M[b][z]*w[at(a,z,c)] for z in range(n))
 total=0
 for a,b,c in itertools.product(range(n),repeat=3):total+=v[at(a,b,c)]*sum(M[a][z]*u[at(z,b,c)] for z in range(n))
 return total

CERTIFICATES_PATH=HERE/'unitary_obstruction_certificates.json'
def hashN(N):return hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
def get_certificate(ring_id):
 return next(r for r in json.loads(CERTIFICATES_PATH.read_text()) if r['id']==ring_id)
def verify_record(r,expected_tensor=None):
 counts={};general=[]
 N=r['tensor'];n=len(N);I=range(n);check(expected_tensor is None or N==expected_tensor,'census mismatch');check(hashN(N)==r['tensor_sha256'],'tensor hash');check(r['scope']=='unitary_only','unexpected base scope')
 check(all(type(v)==int and v>=0 for M in N for row in M for v in row),'not nonnegative integers')
 check(all(N[0][i][j]==N[i][0][j]==int(i==j) for i,j in itertools.product(I,repeat=2)),'unit')
 dual=[next(j for j in I if N[i][j][0]) for i in I];check(all(dual[dual[i]]==i for i in I),'dual involution');check(all(N[dual[i]][j][k]==N[i][k][j] for i,j,k in itertools.product(I,repeat=3)),'transpose duality');check(all(N[i][j][0]==int(dual[i]==j) for i,j in itertools.product(I,repeat=2)),'duals')
 check(all(sum(N[a][b][x]*N[x][c][d] for x in I)==sum(N[b][c][x]*N[a][x][d] for x in I) for a,b,c,d in itertools.product(I,repeat=4)),'associativity')
 f=sy.Poly.from_list([sy.Rational(x) for x in r['field_polynomial']],t);check(f.is_irreducible,'field polynomial reducible')
 lo,hi=map(sy.Rational,r['root_interval']);check((lo==hi and f.eval(lo)==0) or (lo<hi and f.count_roots(lo,hi)==1),'root interval')
 K=sy.QQ.alg_field_from_poly(f);ds=[K([sy.Rational(x) for x in a]) for a in r['dimensions']]
 check(ds[0]==K.one and all(sign(a,f,r['root_interval'])==1 for a in r['dimensions']),'positive dimensions')
 check(all(ds[i]*ds[j]==sum((K(N[i][j][k])*ds[k] for k in I),K.zero) for i,j in itertools.product(I,repeat=2)),'dimension character')
 for c in r['certificates']:
  if c['kind']=='primary_3':
   v=c['integer_vector'];check(len(v)==n**3 and all(type(x)==int for x in v),'integer test vector');cs=[contract(M,v,n) for M in N];check(cs==c['coefficients'],'contraction')
   z=sum((K(x)/d for x,d in zip(cs,ds)),K.zero);check([str(x) for x in z.to_list()]==c['negative_value'],'negative value');check(sign(z.to_list(),f,r['root_interval'])==-1,'primary sign')
  elif c['kind']=='minkowski_support_limit':
   i,j,k=c['ijk'];l=c['l'];S=c['subset'];check(N[i][j][l]>0,'missing left support');T=[m for m in I if N[j][k][m]>0 and any(N[i][m][x]>0 for x in S)];check(T==c['right_support'],'right support')
   a=sum((K(N[l][k][x])*ds[x] for x in S),K.zero)/ds[l];b=sum((K(N[j][k][x])*ds[x] for x in T),K.zero)/ds[j]
   check([str(x) for x in (a-b).to_list()]==c['positive_gap'],'support gap');check(sign((a-b).to_list(),f,r['root_interval'])==1,'support sign')
  else:raise RuntimeError('unknown certificate')
  counts[c['kind']]=counts.get(c['kind'],0)+1
 D=sum((a*a for a in ds),K.zero).to_list()
 if len(D)==1 and D[0].denominator==1 and len(sy.factorint(int(D[0])))<=2:
  general.append(dict(id=r['id'],FPdim=int(D[0]),prime_factorization={str(k):v for k,v in sy.factorint(int(D[0])).items()},theorems=['ENO0809.3031 Theorem1.6','GHR1105.5048 Theorem5.20']))
 braided={'id':r['id'],'FPdim':int(D[0]),'theorems':['Dong2103.04553 Corollary3.5','GHR1105.5048 Theorem5.20']} if len(D)==1 and D[0].denominator==1 and 0<int(D[0])<1800 else None
 return {'id':r['id'],'certificate_counts':counts,'general_upgrade':general[0] if general else None,'braided_upgrade':braided}

def main():
 records=json.loads(CERTIFICATES_PATH.read_text());results=[verify_record(r) for r in records]
 counts={}
 for r in results:
  for k,v in r['certificate_counts'].items():counts[k]=counts.get(k,0)+v
 general=[r['general_upgrade'] for r in results if r['general_upgrade']]
 check(len(records)==28 and len({r['id'] for r in records})==28,'certificate inventory')
 check(counts=={'minkowski_support_limit':9,'primary_3':22},'criterion inventory')
 check({r['id'] for r in general}=={'R7_3_900','R7_3_991'},'general upgrade inventory')
 expected=json.loads((HERE/'general_upgrades.json').read_text())
 check(expected['general_exclusions']==general,'general metadata')
 braided=[r['braided_upgrade'] for r in results if r['braided_upgrade']]
 check(json.loads((HERE/'braided_upgrades.json').read_text())['braided_exclusions']==braided,'braided metadata')
 check(len(braided)==10,'braided upgrade inventory')
 max_bound=max((max(abs(v) for v in c['integer_vector'])**2)*max(sum(sum(row) for row in M)**3 for M in r['tensor']) for r in records for c in r['certificates'] if c['kind']=='primary_3')
 check(max_bound<2**63,'historical NumPy int64 bound')
 report={'status':'PASS','checked_rings':len(records),'certificate_counts':counts,'general_exclusions':general,'braided_exclusions':braided,'base_obstructions_scope':'unitary','max_discovery_integer_contraction_bound':max_bound,'replay_arithmetic':'Python arbitrary-size integers and exact number fields with rational root isolation'}
 print(json.dumps(report,indent=2))
 return report
if __name__=='__main__':main()
