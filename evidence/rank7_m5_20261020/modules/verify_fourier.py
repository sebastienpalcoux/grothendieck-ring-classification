"""Regenerate the exhaustive eighteen Fourier sectors from the raw R4982 tensor."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import itertools,json,sys,sympy as s
from pathlib import Path
B=Path(__file__).parent;P=B.parents[2]
sys.path.insert(0,str(P/'evidence/rank7_m5_20261019/theory'))
from cyclic3_spectral import choices,norm,conjugate,trace,matmul
R=next(r['tensor'] for r in json.load(open(P/'supplements/rank7/output/m5/census.json')) if r['id']=='R7_5_4982')
M=list(map(s.Matrix,R));x=s.Symbol('x');F=[4,5,6];BB=M[4].extract(F,F)
assert all(R[1][a][b]==int(b==a) for a in range(3,7) for b in range(7))
assert all(any(R[i][a][a]%3 for i in range(3,7)) for a in range(3,7))
assert M[3].extract(range(3,7),range(3,7))==s.diag(2,3,3,3)
assert M[3]**2==M[0]+M[1]+M[2]+2*M[3]
assert all(M[3]*M[i]==3*M[i] for i in [4,5,6])
assert [sorted({u for u,v in choices(n) if v==0}&{-1,3}) for n in [2,3,3,3]]==[[-1],[3],[3],[3]]
assert BB==s.Matrix([[2,4,5],[4,5,3],[5,3,4]])
mins=[int(((12*s.eye(3)-BB)[:i,:i]).det()) for i in range(1,4)];assert mins==[10,54,47]
c=s.Poly(x**3+x**2-12*x+11,x);h=s.Poly(x*(x-12),x);q=c*h
assert c.is_irreducible and int(s.trace(BB))%3==2
assert sum((co*M[4]**k for (k,),co in q.terms()),s.zeros(7))==s.zeros(7)
ds=[[v[0] for v in choices(int(BB[i,i])) if v[1]==0] for i in range(3)];eds=list(itertools.combinations(range(3),2));cs=[choices(int(BB[i,j])) for i,j in eds];good=[];count=0
for diag in itertools.product(*ds):
 if sum(diag)!=-1:continue
 for vs in itertools.product(*cs):
  if sum(v*v for v in diag)+2*sum(map(norm,vs))!=25:continue
  A=[[(0,0) for i in range(3)] for j in range(3)]
  for i,v in enumerate(diag):A[i][i]=(v,0)
  for (i,j),v in zip(eds,vs):A[i][j]=v;A[j][i]=conjugate(v)
  tr=trace(matmul(matmul(A,A),A));assert tr[1]==0;count+=1
  if tr[0]==-70:good.append(A)
assert count==639 and len(good)==18
u,v,d=s.gcdex(h,c);e=s.rem(u*h,c*h);E=sum((co*M[4]**k for (k,),co in e.terms()),s.zeros(7));assert E*E==E and E.rank()==3
V=s.Matrix.hstack(*(s.Matrix(list(E*M[4]**k)) for k in range(3)))
polys=[[int(z) for z in V.gauss_jordan_solve(s.Matrix(list(E*M[i])))[0]] for i in range(7)]
assert polys==[[1,0,0],[1,0,0],[1,0,0],[3,0,0],[0,1,0],[7,-3,-1],[-8,2,1]]
def madd(A,B):return [[(A[i][j][0]+B[i][j][0],A[i][j][1]+B[i][j][1]) for j in range(3)] for i in range(3)]
def smul(c,A):return [[(c*v[0],c*v[1]) for v in row] for row in A]
I=[[(int(i==j),0) for j in range(3)] for i in range(3)];surv=[]
for T in good:
 ps=[I,T,matmul(T,T)];TT=[]
 for i,p in enumerate(polys):
  A=[[(0,0) for j in range(3)] for i in range(3)]
  for k,co in enumerate(p):A=madd(A,smul(co,ps[k]))
  assert all(A[a][b] in choices(R[i][F[a]][F[b]]) for a in range(3) for b in range(3))
  TT.append(A)
 surv.append(TT)
(B/'r4982_fourier_certificate.json').write_text(json.dumps({'matrix_majorant':BB.tolist(),'positive_definite_principal_minors':mins,'first_two_moments_count':count,'third_moment_count':len(good),'cubic_action_polynomials':polys,'full_representations':surv},default=int)+'\n')
print('Fourier prerequisite identities and exhaustive 639 -> 18 enumeration verified.',flush=True)
