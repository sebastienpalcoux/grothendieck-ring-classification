"""Unitary C3 equivariantization of Izumi's Q8 near-group category."""
from pathlib import Path
import sys,json,itertools,time
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
sys.path[:0]=[str(ROOT/'work/resolve_rank9_neargroup'),str(ROOT/'work/rank11')]
from verify_ng_actions import group,representations,mat,madd,mmul,mstar,mconj,zadd,check,require
from common import read,sha,based_iso,validate

def neg(A):return [[(-x,-y)for x,y in row]for row in A]

def construct():
 G=group(1);rep,J=representations(1);I=mat([[1,0],[0,1]])
 A=neg(madd(madd(I,rep[1]),madd(rep[4],rep[5])))
 require(mmul(A,mstar(A))==mat([[4,0],[0,4]]),'W=A/2 unitary')
 require(mmul(mmul(A,A),A)==mat([[8,0],[0,8]]),'W cube identity')
 require(mmul(A,J)==mmul(J,mconj(A)),'W commutes quaternionic antiunitary')
 require(zadd(A[0][0],A[1][1])==(-2,0),'trace W=-1')
 phi=[next(h for h in range(8)if mmul(A,rep[g])==mmul(rep[h],A))for g in range(8)]
 require(all(phi[phi[phi[g]]]==g for g in range(8)),'C3 action')
 require(all(phi[G[g][h]]==G[phi[g]][phi[h]]for g,h in itertools.product(range(8),repeat=2)),'group automorphism')
 fixed=[g for g in range(8)if phi[g]==g];seen=set(fixed);orbits=[]
 for g in range(8):
  if g not in seen:o=sorted({g,phi[g],phi[phi[g]]});orbits.append(o);seen.update(o)
 require(fixed==[0,2]and len(orbits)==2 and all(len(o)==3 for o in orbits),'fixed/free orbit profile')
 labels=[('fixed',g,t)for g in fixed for t in range(3)]+[('orbit',*o)for o in orbits]+[('rho',t)for t in range(3)]
 n=len(labels);N=[[[0]*n for j in range(n)]for i in range(n)]
 supp=lambda a:[a[1]]if a[0]=='fixed'else list(a[1:])
 for i,L in enumerate(labels):
  for j,M in enumerate(labels):
   if L[0]!='rho'and M[0]!='rho':
    for k,U in enumerate(labels[:8]):
     pairs=[(g,h)for g in supp(L)for h in supp(M)if G[g][h]==U[1]]
     if U[0]=='orbit':N[i][j][k]=len(pairs)
     elif L[0]==M[0]=='fixed':N[i][j][k]=len(pairs)*int(U[2]==(L[2]+M[2])%3)
     else:require(len(pairs)%3==0,'free fibre C3 orbit');N[i][j][k]=len(pairs)//3
   elif L[0]==M[0]=='rho':
    for k,U in enumerate(labels[:8]):N[i][j][k]=1 if U[0]=='orbit'else int(U[2]==(L[1]+M[1])%3)
    for k,U in enumerate(labels[8:],8):N[i][j][k]=int((U[1]-L[1]-M[1])%3 in(1,2))
   else:
    X,Y=(L,M)if L[0]=='rho'else(M,L)
    for k,U in enumerate(labels[8:],8):N[i][j][k]=1 if Y[0]=='orbit'else int(U[1]==(X[1]+Y[2])%3)
 validate(N);du=check(N);R=read()['R11_1_179'];p=based_iso(N,R);require(p is not None,'all1331coefficients matchR179')
 dims=[1]*6+[3]*2+[4]*3
 require(all(dims[i]*dims[j]==sum(N[i][j][k]*dims[k]for k in range(n))for i,j in itertools.product(range(n),repeat=2)),'exact dimensions')
 return dict(id='R11_1_179',status='unitarily_realized',tensor_sha256=sha(R),model='C3-equivariantization of an Izumi Q8 near-group category of type (1^8,4)',group_table=G,automorphism=phi,intertwiner_numerator=A,intertwiner_denominator=2,intertwiner_trace=-1,intertwiner_cube='identity',labels=labels,dimensions=dims,dual=du,model_tensor=N,model_to_input=p,input_to_model=[p.index(i)for i in range(n)],categorical_existence='Izumi arXiv:1512.04288v2 Theorem6.1 and normalized functor construction in prior NG_ACTIONS.tex; W^3=1 supplies strict action',coherence='identity compositor; C3 generator actsS_g→S_phi(g),T(v)→T(Wv)',parameters='Any of the three cube-root associator parameters gives this tensor')
if __name__=='__main__':
 start=time.monotonic();r=construct();(P/'model.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status='PASS',id=r['id'],model_to_input=r['model_to_input'],seconds=time.monotonic()-start),indent=2),flush=True)
