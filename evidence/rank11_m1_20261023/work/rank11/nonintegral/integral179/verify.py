"""Independent standard-library equivariant Hom-character replay for R179.

Does not import the construction code. Fusion multiplicities are recovered by
C3 character averaging on all underlying near-group fusion spaces, rather than
by the product formulas used in construct.py.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import gzip,json,hashlib,time
P=Path(__file__).resolve().parent;ROOT=P.parents[3]

def need(x,msg):
 if not x:raise ValueError(msg)
def ca(a,b):return(a[0]+b[0],a[1]+b[1])
def cm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cc(a):return(a[0],-a[1])
def ma(A,B):return[[ca(A[i][j],B[i][j])for j in range(2)]for i in range(2)]
def mm(A,B):return[[ca(cm(A[i][0],B[0][j]),cm(A[i][1],B[1][j]))for j in range(2)]for i in range(2)]
def ms(A):return[[cc(A[j][i])for j in range(2)]for i in range(2)]
def mc(A):return[[cc(A[i][j])for j in range(2)]for i in range(2)]
def scale(A,s):return[[(a*s,b*s)for a,b in row]for row in A]
def mat(A):return[[(Q(a),Q(0))if isinstance(a,int)else tuple(map(Q,a))for a in row]for row in A]
def power(A,n):
 O=mat([[1,0],[0,1]])
 for _ in range(n):O=mm(O,A)
 return O
# Cyclotomic pairs a+b*w with w²+w+1=0, used only for C3 characters.
def za(a,b):return(a[0]+b[0],a[1]+b[1])
def zm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]-a[1]*b[1])
def zpow(n):return[(1,0),(0,1),(-1,-1)][n%3]

def verify():
 r=json.load(open(P/'model.json'));G=r['group_table'];phi=r['automorphism'];A=mat(r['intertwiner_numerator']);W=scale(A,Q(1,r['intertwiner_denominator']));I=mat([[1,0],[0,1]]);ii=mat([[(0,1),0],[0,(0,-1)]]);jj=mat([[0,1],[-1,0]]);pi=[mm(power(ii,g%4),power(jj,g//4))for g in range(8)]
 need(all(mm(pi[g],pi[h])==pi[G[g][h]]for g,h in product(range(8),repeat=2)),'faithful quaternion group representation')
 need(mm(W,ms(W))==I and power(W,3)==I,'unitary genuineorder3 intertwiner')
 need(mm(W,jj)==mm(jj,mc(W)),'antiunitary preserved')
 need(all(mm(W,pi[g])==mm(pi[phi[g]],W)for g in range(8)),'exact automorphism intertwining')
 need(ca(W[0][0],W[1][1])==(-1,0),'fusion-space character')
 need(all(phi[phi[phi[g]]]==g for g in range(8)),'pointed C3 action')
 # Underlying near-group tensor and C3 action: all dims finite and exact.
 base=[[[0]*9 for j in range(9)]for i in range(9)]
 for i,j in product(range(8),repeat=2):base[i][j][G[i][j]]=1
 for g in range(8):base[g][8][8]=base[8][g][8]=base[8][8][g]=1
 base[8][8][8]=2
 action=phi+[8];powers=[list(range(9)),action,[action[action[i]]for i in range(9)]]
 labels=r['labels'];support=[];phase=[]
 for l in labels:
  if l[0]=='fixed':need(phi[l[1]]==l[1],'fixed degree');support.append([l[1]]);phase.append(l[2])
  elif l[0]=='orbit':need(set(l[1:])=={l[1],phi[l[1]],phi[phi[l[1]]]},'free orbit');support.append(l[1:]);phase.append(0)
  else:need(l[0]=='rho','rho label');support.append([8]);phase.append(l[1])
 n=len(labels);need(n==11 and len(set(map(tuple,labels)))==11,'all equivariant simples')
 T=[[[0]*n for j in range(n)]for i in range(n)]
 for i,j,k in product(range(n),repeat=3):
  average=(0,0)
  for t in range(3):
   tr=0
   for a,b,c in product(support[i],support[j],support[k]):
    if not all(powers[t][u]==u for u in(a,b,c)):continue
    tr+=-1 if t and a==b==c==8 else base[a][b][c]
   phase_value=zpow(t*(phase[i]+phase[j]-phase[k]));average=za(average,(tr*phase_value[0],tr*phase_value[1]))
  need(average[1]==0 and average[0]>=0 and average[0]%3==0,'integer C3 Hom projection')
  T[i][j][k]=average[0]//3
 need(T==r['model_tensor'],'independent Hom-character reconstruction')
 need(all(T[0][i][j]==T[i][0][j]==int(i==j)for i,j in product(range(n),repeat=2)),'unit')
 du=[next(j for j in range(n)if T[i][j][0])for i in range(n)];need(du==r['dual'],'duality')
 need(all(sum(T[i][j][x]*T[x][k][l]for x in range(n))==sum(T[j][k][x]*T[i][x][l]for x in range(n))for i,j,k,l in product(range(n),repeat=4)),'all14641associativityidentities')
 src=list(gzip.open(ROOT/'repositories/fusion-ring-census/results/rank11/tables.txt.gz','rt'))[178];R=json.loads(src.replace('{','[').replace('}',']'));need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==r['tensor_sha256'],'source identity')
 p=r['model_to_input'];need(sorted(p)==list(range(n))and p[0]==0,'based bijection')
 need(all(T[i][j][k]==R[p[i]][p[j]][p[k]]for i,j,k in product(range(n),repeat=3)),'all1331inputcoefficients')
 return dict(status='PASS',id=r['id'],model=r['model'],tensor_sha256=r['tensor_sha256'],fusion_coefficients=1331,associativity_equations=14641,independent_method='C3 averaging of underlying near-group fusion-space characters',model_to_input=p)
if __name__=='__main__':
 start=time.monotonic();r=verify();r['seconds']=time.monotonic()-start;(P/'replay.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
