"""Exhaustive based involutions and exact Cuntz-equivariantization tensor replay.
Standard library only. Categorical completeness is proved in NG_ACTIONS.tex.
"""
from pathlib import Path
from itertools import permutations,product
import json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent

def require(ok,msg):
 if not ok:raise ValueError(msg)

def group(e):
 # r^a s^b, r^4=1, s r=r^-1 s, s²=r^(2e).
 return [[((a+(-1)**b*c+2*e*b*d)%4)+4*((b+d)%2)for c,d in [(j%4,j//4)for j in range(8)]]for a,b in [(i%4,i//4)for i in range(8)]]

def automorphisms(G):
 ans=[]
 for tail in permutations(range(1,8)):
  f=(0,)+tail
  if all(f[G[a][b]]==G[f[a]][f[b]]for a,b in product(range(8),repeat=2)):ans.append(f)
 return ans

# Gaussian integer matrices; W=A/sqrt(2), so no floating arithmetic is used.
def zadd(x,y):return (x[0]+y[0],x[1]+y[1])
def zmul(x,y):return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def zconj(x):return (x[0],-x[1])
def mat(a):return [[(x,0)if isinstance(x,int)else x for x in row]for row in a]
def madd(A,B):return [[zadd(A[i][j],B[i][j])for j in range(2)]for i in range(2)]
def mmul(A,B):return [[zadd(zmul(A[i][0],B[0][j]),zmul(A[i][1],B[1][j]))for j in range(2)]for i in range(2)]
def mstar(A):return [[zconj(A[j][i])for j in range(2)]for i in range(2)]
def mconj(A):return [[zconj(x)for x in row]for row in A]
def representations(e):
 I=mat([[1,0],[0,1]]);r=mat([[0,-1],[1,0]])if e==0 else mat([[(0,1),0],[0,(0,-1)]])
 ss=mat([[1,0],[0,-1]])if e==0 else mat([[0,1],[-1,0]])
 P=[]
 for g in range(8):
  A=I
  for _ in range(g%4):A=mmul(A,r)
  if g//4:A=mmul(A,ss)
  P.append(A)
 return P,I if e==0 else ss

def check_intertwiner(G,f,e):
 P,J=representations(e);I=mat([[1,0],[0,1]])
 require(all(mmul(P[a],P[b])==P[G[a][b]]for a,b in product(range(8),repeat=2)),'faithful irrep')
 if e==0:
  H=mat([[1,1],[1,-1]]);candidates=[mmul(P[g],H)for g in range(8)]
 else:candidates=[madd(P[g],P[h])for g,h in product(range(8),repeat=2)if G[g][h]!=G[h][g]]
 for A in candidates:
  if not all(mmul(A,P[g])==mmul(P[f[g]],A)for g in range(8)):continue
  require(mmul(A,mstar(A))==mat([[2,0],[0,2]]),'unitary W')
  require(mmul(A,A)==mat([[2*(-1)**e,0],[0,2*(-1)**e]]),'square W')
  require(mmul(A,J)==mmul(J,mconj(A)),'antiunitary compatibility')
  require(zadd(A[0][0],A[1][1])==(0,0),'zero fusion-space trace')
  return A
 raise ValueError('missing exact intertwiner')

def tensor(G,f,e):
 fixed=[g for g in range(8)if f[g]==g];seen=set(fixed);orbits=[]
 for g in range(8):
  if g not in seen:orb=sorted({g,f[g]});seen.update(orb);orbits.append(orb)
 require(len(fixed)==2 and len(orbits)==3,'orbit profile')
 labels=[('f',g,t)for g in fixed for t in (1,-1)]+[('p',*orb)for orb in orbits]+[('r',1),('r',-1)]
 n=len(labels);N=[[[0]*n for _ in range(n)]for _ in range(n)]
 support=lambda x:[x[1]]if x[0]=='f'else list(x[1:])
 for a,A in enumerate(labels):
  for b,B in enumerate(labels):
   if A[0]!='r'and B[0]!='r':
    aa=support(A);bb=support(B)
    for c,C in enumerate(labels[:7]):
     pairs=[(g,h)for g in aa for h in bb if G[g][h]==C[1]]
     if C[0]=='p':N[a][b][c]=len(pairs)
     else:
      tr=sum((A[2]if A[0]=='f'else 0)*(B[2]if B[0]=='f'else 0)for g,h in pairs if f[g]==g and f[h]==h)
      val=len(pairs)+C[2]*tr;require(val%2==0,'character parity');N[a][b][c]=val//2
   elif A[0]=='r'and B[0]=='r':
    for c,C in enumerate(labels[:7]):
     N[a][b][c]=int(C[2]==((-1)**e)*A[1]*B[1])if C[0]=='f'else 1
    N[a][b][7]=N[a][b][8]=1 # trace W=0 on Hom(rho,rho²)
   else:
    X,Y=(A,B)if A[0]=='r'else(B,A)
    if Y[0]=='f':N[a][b][7 if X[1]*Y[2]==1 else 8]=1
    else:N[a][b][7]=N[a][b][8]=1
 return labels,N

def check(N):
 n=len(N);require(all(N[0][i][j]==int(i==j)==N[i][0][j]for i,j in product(range(n),repeat=2)),'unit')
 du=[]
 for i in range(n):
  ds=[j for j in range(n)if N[i][j][0]];require(len(ds)==1,'duality');du.append(ds[0])
 require(all(sum(N[i][j][x]*N[x][k][l]for x in range(n))==sum(N[j][k][x]*N[i][x][l]for x in range(n))for i,j,k,l in product(range(n),repeat=4)),'associativity')
 return du

def match(N,R):
 n=len(N);d=[1]*4+[2]*3+[4]*2
 def sig(X,i):return tuple(sorted(tuple(sorted(X[i][j]))for j in range(n)))
 domains=[[j for j in range(n)if sig(N,i)==sig(R,j)]for i in range(n)];p=[0]+[-1]*(n-1)
 def go(i,used):
  if i==n:return p[:]
  for j in domains[i]:
   if j in used:continue
   p[i]=j
   if all(N[a][b][c]==R[p[a]][p[b]][p[c]]for a,b,c in product(range(i+1),repeat=3)):
    out=go(i+1,used|{j})
    if out is not None:return out
  p[i]=-1
 return go(1,{0})

def main():
 T=json.loads((ROOT/'work/input_audit/tensors.json').read_text());out=[]
 for e,name in [(0,'D8'),(1,'Q8')]:
  G=group(e);auts=automorphisms(G);inv=[f for f in auts if all(f[f[i]]==i for i in range(8))and sum(f[i]==i for i in range(8))==2];records=[]
  for f in inv:
   A=check_intertwiner(G,f,e);labs,N=tensor(G,f,e);du=check(N);maps={str(k):m for k in [12,62,87,108]if(m:=match(N,T[f'R9_1_{k}']))is not None}
   require(set(maps)==({'12'}if e==0 else{'108'}),'unique matching target')
   records.append(dict(automorphism=list(f),intertwiner_numerator=A,intertwiner_denominator="sqrt(2)",labels=labs,dual=du,matches_model_to_input=maps,tensor=N))
  require(len(auts)==(8 if e==0 else 24),'complete group automorphism count')
  require(len(inv)==(2 if e==0 else 6),'required involution count')
  rr=dict(group=name,automorphisms=len(auts),required_involutions=len(inv),coherence_on_rho=(-1)**e,rho_lifts_self_dual=(e==0),actions=records);out.append(rr)
  print(name,'PASS',len(inv),'involutions, all match',12 if e==0 else 108,flush=True)
 (HERE/'ng_actions.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
