import json,itertools,sys,sympy as s
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(Path(__file__).resolve().parent))
from cyclic3_spectral import choices,norm,conjugate,trace,matmul
R=next(r['tensor'] for r in json.load(open(P/'supplements/rank7/output/m5/survivors.json')) if r['id']=='R7_5_4982');M=list(map(s.Matrix,R));x=s.Symbol('x');F=[4,5,6];B=M[4].extract(F,F)
print('B',B);print('minors',[((12*s.eye(3)-B)[:i,:i]).det() for i in range(1,4)])
q=s.Poly(x*(x-12)*(x**3+x**2-12*x+11),x);V=sum((c*M[4]**k for (k,),c in q.terms()),s.zeros(7));print('ringq',list(V[0,:]))
ds=[[v[0] for v in choices(int(B[i,i])) if v[1]==0] for i in range(3)];eds=list(itertools.combinations(range(3),2));cs=[choices(int(B[i,j])) for i,j in eds];good=[];count=0;trs=set()
for d in itertools.product(*ds):
 if sum(d)!=-1:continue
 for vs in itertools.product(*cs):
  if sum(v*v for v in d)+2*sum(map(norm,vs))!=25:continue
  A=[[(0,0) for i in range(3)] for j in range(3)]
  for i,v in enumerate(d):A[i][i]=(v,0)
  for (i,j),v in zip(eds,vs):A[i][j]=v;A[j][i]=conjugate(v)
  tr=trace(matmul(matmul(A,A),A));assert tr[1]==0;count+=1;trs.add(tr[0])
  if tr[0]==-70:good.append(A)
print('count',count,'traces',sorted(trs),'good',len(good));Path(__file__).with_name('4982_matrix_candidates.json').write_text(json.dumps(good))
# Polynomial action on the cubic spectral ideal.
c=s.Poly(x**3+x**2-12*x+11,x);h=s.Poly(x*(x-12),x);u,v,d=s.gcdex(h,c);e=s.rem(u*h,c*h);E=sum((co*M[4]**k for (k,),co in e.terms()),s.zeros(7))
print('E projector',E*E==E,E.rank())
V=s.Matrix.hstack(*(s.Matrix(list(E*M[4]**k)) for k in range(3)))
polys=[list(V.gauss_jordan_solve(s.Matrix(list(E*M[i])))[0]) for i in range(7)]
print('polys',polys)
def madd(A,B):return [[(A[i][j][0]+B[i][j][0],A[i][j][1]+B[i][j][1]) for j in range(3)] for i in range(3)]
def smul(c,A):return [[(c*v[0],c*v[1]) for v in row] for row in A]
I=[[(int(i==j),0) for j in range(3)] for i in range(3)];surv=[]
for T in good:
 ps=[I,T,matmul(T,T)];TT=[]
 for i,p in enumerate(polys):
  A=[[(0,0) for j in range(3)] for i in range(3)]
  for k,co in enumerate(p):A=madd(A,smul(co,ps[k]))
  if any(A[a][b] not in choices(R[i][F[a]][F[b]]) for a in range(3) for b in range(3)):break
  TT.append(A)
 if len(TT)==7:surv.append(TT)
print('fullcompatible',len(surv));Path(__file__).with_name('4982_full_representations.json').write_text(json.dumps(surv,default=str))
