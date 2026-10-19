"""Exact C3 Fourier-module obstruction for the integral dimension-390 tensor.

General complex categorification scope; no pivotality assumption. The proof
that any categorification supplies the matrices is in cyclic3_spectral.tex.
"""
import itertools,json,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(P/'supplements/rank7/software'))
from exact import require

def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def conjugate(a):return (a[0]-a[1],-a[1])
def norm(a):return a[0]**2-a[0]*a[1]+a[1]**2

def choices(n):
 return sorted({(a-c,b-c) for a in range(n+1) for b in range(n-a+1) if (c:=n-a-b)>=0})
def matmul(A,B):
 return [[tuple(map(sum,zip(*(mul(A[i][k],B[k][j]) for k in range(len(A)))))) for j in range(len(A))] for i in range(len(A))]
def trace(A):return tuple(map(sum,zip(*(A[i][i] for i in range(len(A))))))

def certificate(R,g=1,gen=3):
 n=len(R);require(n==7,'rank');require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)),'commutativity')
 mats=list(map(s.Matrix,R));x=s.Symbol('x');identity=s.eye(n)
 require(mats[g]**3==identity and mats[g]!=identity,'order three')
 fixed=[i for i in range(n) if R[g][i][i]];require(len(fixed)==4,'four fixed objects')
 require(all(R[i][i][0]==1 for i in fixed),'fixed objects self-dual')
 require(R[gen][gen][0]==1,'generator self-dual')
 witnesses=[]
 for i in fixed:
  a,j=next((a,j) for a in fixed for j in fixed if R[a][i][j]%3)
  witnesses.append([i,a,j,R[a][i][j]])
 # These witnesses force the left-g action to be identity on the Fourier sector.
 q=s.Poly((x-9)*(x+1)*(x**3-x**2-4*x-1),x)
 value=sum((c*mats[gen]**k for (k,),c in q.terms()),s.zeros(n))
 coeff=list(value[0,:]);G=[0,g,next(i for i in range(n) if R[g][g][i])]
 require(all(coeff[i]==0 for i in range(n) if i not in G) and sum(coeff[i] for i in G)==0,'annihilator does not vanish at g=1')
 require(value==sum((coeff[i]*mats[i] for i in range(n)),s.zeros(n)),'polynomial multiplication identity')
 B=mats[gen].extract(fixed,fixed);L=9*s.eye(4)-B
 minors=[int(L[:i,:i].det()) for i in range(1,5)]
 require(all(v>0 for v in minors),'Perron bound')
 target=s.Poly((x+1)*(x**3-x**2-4*x-1),x)
 require(target.is_sqf and s.Poly(x**3-x**2-4*x-1,x).is_irreducible,'factor irreducibility')
 # Hermitian Q(zeta_3)-matrices have rational, hence integral, characteristic polynomial.
 # Degree four and the annihilator leave (x+1)^4 or the target.
 require(int(s.trace(B))%3 != (-4)%3,'alternative spectrum not eliminated modulo three')
 trace1=-int(target.all_coeffs()[1]);trace2=trace1**2-2*int(target.all_coeffs()[2]);trace3=trace1**3-3*trace1*int(target.all_coeffs()[2])-3*int(target.all_coeffs()[3])
 diagchoices=[[v[0] for v in choices(int(B[i,i])) if v[1]==0] for i in range(4)]
 edges=list(itertools.combinations(range(4),2));edgechoices=[choices(int(B[i,j])) for i,j in edges]
 minimum=[min(map(norm,cs)) for cs in edgechoices]
 diagonals=[d for d in itertools.product(*diagchoices) if sum(d)==trace1 and sum(v*v for v in d)+2*sum(minimum)<=trace2]
 require(len(diagonals)==1,'unique norm-compatible diagonal')
 d=diagonals[0];require(sum(v*v for v in d)+2*sum(minimum)==trace2,'norm bound must saturate')
 minimalchoices=[[v for v in cs if norm(v)==m] for cs,m in zip(edgechoices,minimum)]
 traces=set();count=0
 for es in itertools.product(*minimalchoices):
  A=[[(0,0) for j in range(4)] for i in range(4)]
  for i,v in enumerate(d):A[i][i]=(v,0)
  for (i,j),v in zip(edges,es):A[i][j]=v;A[j][i]=conjugate(v)
  require(trace(A)==(trace1,0) and trace(matmul(A,A))==(trace2,0),'trace audit')
  cube=trace(matmul(matmul(A,A),A));require(cube[1]==0,'nonreal Hermitian trace');traces.add(cube[0]);count+=1
 require(trace3 not in traces,'cubic moment remains feasible')
 return {'kind':'cyclic3_spectral_module','scope':'general_complex','g':g,'generator':gen,'fixed':fixed,'forced_identity_witnesses':witnesses,'annihilator':list(map(int,q.all_coeffs())),'annihilator_ring_coefficients':list(map(int,coeff)),'perron_minor_witnesses':minors,'required_characteristic_polynomial':list(map(int,target.all_coeffs())),'required_moments':[trace1,trace2,trace3],'diagonal':list(d),'edge_minimal_norms':minimum,'matrices_checked':count,'possible_cubic_traces':sorted(traces)}
def verify(R,c):require(c==certificate(R,c['g'],c['generator']),'C3 spectral certificate mismatch')
if __name__=='__main__':
 rows=json.load(open(P/'supplements/rank7/output/m5/survivors.json'));r=next(a for a in rows if a['id']=='R7_5_5007');c=certificate(r['tensor']);verify(r['tensor'],c)
 out={'id':r['id'],'certificate':c,'replayed':True};Path(__file__).with_name('cyclic3_spectral_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
