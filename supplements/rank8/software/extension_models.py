"""Explicit orbit and crossed-product tensors for the October2 models."""
from itertools import product
import itertools

def require(x,message='exact construction failed'):
    if not x:raise ValueError(message)

def psu_flip(pseudo, twist):
    B=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for a,b in product(range(2),repeat=2):
        B[a][b][(a+b)%2]=1
        B[a][2+b][2+(a+b)%2]=B[2+a][b][2+(a+b)%2]=1
        B[2+a][2+b][(a+b+int(pseudo))%2]=1
        B[2+a][2+b][2]=B[2+a][2+b][3]=1
    T=[[[0]*8 for _ in range(8)] for _ in range(8)]
    act=[1,0,3,2];tau=[0,1,3,2]
    for g,h,a,b,c in product(range(2),range(2),range(4),range(4),range(4)):
        target=act[c] if twist*g*h else c
        T[4*g+a][4*h+b][4*((g+h)%2)+target]=B[a][tau[b] if g else b][c]
    return T

def q8_equivariant():
    def mul(a,b):
        s,x=a;t,y=b
        if x==0:return(s^t,y)
        if y==0:return(s^t,x)
        if x==y:return(s^t^1,0)
        return(s^t^(0 if(x,y)in[(1,2),(2,3),(3,1)]else 1),6-x-y)
    def sigma(a):return(a[0],0 if a[1]==0 else a[1]%3+1)
    Q=list(product(range(2),range(4)))
    require(all(mul(mul(a,b),c)==mul(a,mul(b,c)) for a,b,c in product(Q,repeat=3)))
    require(all(sigma(mul(a,b))==mul(sigma(a),sigma(b))for a,b in product(Q,repeat=2)))
    labels=[([(s,0)],e)for s in range(2)for e in range(3)]+[([(s,a)for a in(1,2,3)],None)for s in range(2)]
    T=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,(A,e) in enumerate(labels):
        for j,(B,f) in enumerate(labels):
            for k,(C,h) in enumerate(labels):
                n=sum(mul(a,b)==C[0]for a in A for b in B)
                if len(C)>1:T[i][j][k]=n
                elif len(A)==len(B)==1:T[i][j][k]=n*int((e+f)%3==h)
                else:
                    require(n%3==0)
                    T[i][j][k]=n//3
    return T

def ty9(group):
    if group=='C9':
        add=lambda a,b:(a+b)%9
        inv=lambda a:(-a)%9
    elif group=='C3xC3':
        add=lambda a,b:3*((a//3+b//3)%3)+(a%3+b%3)%3
        inv=lambda a:3*((-(a//3))%3)+(-(a%3))%3
    else:raise ValueError('unknown group')
    r=10;m=9
    N=[[[0]*r for _ in range(r)] for _ in range(r)]
    for a,b in itertools.product(range(9),repeat=2):N[a][b][add(a,b)]=1
    for a in range(9):N[a][m][m]=N[m][a][m]=N[m][m][a]=1
    sigma=[inv(a) for a in range(9)]+[m]
    labels=[];remaining=set(range(r))
    while remaining:
        a=min(remaining);orbit=sorted({a,sigma[a]});remaining-=set(orbit)
        for sign in ([1,-1] if len(orbit)==1 else [0]):labels.append((orbit,sign))
    require(len(labels)==8)
    T=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j,k in itertools.product(range(8),repeat=3):
        A,sa=labels[i];B,sb=labels[j];C,sc=labels[k];c=C[0]
        dimension=sum(N[a][b][c] for a in A for b in B)
        if len(C)==1:
            # Fixed m has action scalar +/-i, fixed 0 has scalar +/-1.
            # Division by the output scalar cancels i unless both inputs are m.
            trace=sum(N[a][b][c]*sa*sb*(-1 if a==b==m else 1)
                      for a in A for b in B if sigma[a]==a and sigma[b]==b)
            require((dimension+sc*trace)%2==0,'nonintegral projection')
            T[i][j][k]=(dimension+sc*trace)//2
        else:T[i][j][k]=dimension
    require(all(v in (0,1) for M in T for row in M for v in row),'not multiplicity one')
    require(all(sum(T[i][j][s]*T[s][k][l] for s in range(8))==
                sum(T[j][k][s]*T[i][s][l] for s in range(8))
                for i,j,k,l in itertools.product(range(8),repeat=4)),'associativity failed')
    return T


CH=[(1,1,1),(1,-1,1),(2,0,-1)] # S3 classes e,(12),(123)
SG=(1,-1,1)
def req(x,m):
 if not x:raise ValueError(m)
def dot(*vs):return tuple(__import__('math').prod(v[k]for v in vs)for k in range(3))
def decS(v):
 out=[sum(w*a*b for w,a,b in zip((1,3,2),v,c))for c in CH]
 req(all(z%6==0 and z>=0 for z in out),'S3 character');return[z//6 for z in out]
def decC(v):
 req((v[0]+v[1])%2==0 and(v[0]-v[1])%2==0,'C2 character')
 return[(v[0]+v[1])//2,(v[0]-v[1])//2]
def ty_v4_s3(twist):
 # A_1,A_sign,A_std; X_+,X_-; M_1,M_sign,M_std.
 T=[[[0]*8 for _ in range(8)]for _ in range(8)]
 for i,j in itertools.product(range(8),repeat=2):
  a,b=sorted((i,j));v=[0]*8
  if b<3:v[:3]=decS(dot(CH[a],CH[b]))
  elif a<3 and b<5:v[3:5]=decC(dot(CH[a],(1,1 if b==3 else -1,1)))
  elif a<3:v[5:8]=decS(dot(CH[a],CH[b-5]))
  elif b<5:
   v[:3]=decS((3,1 if a==b else -1,0));v[3]=v[4]=1
  elif a<5:v[5:8]=decS(dot((3,1 if a==3 else -1,0),CH[b-5]))
  else:
   z=dot(CH[a-5],CH[b-5],SG if twist else CH[0]);v[:3]=decS(z);v[3:5]=decC(z)
  T[i][j]=v
 dims=[1,1,2,3,3,2,2,4]
 req(all(sum(T[i][j][k]*dims[k]for k in range(8))==dims[i]*dims[j]for i,j in itertools.product(range(8),repeat=2)),'FPdim')
 req(all(sum(T[i][j][s]*T[s][k][l]for s in range(8))==sum(T[j][k][s]*T[i][s][l]for s in range(8))for i,j,k,l in itertools.product(range(8),repeat=4)),'associativity')
 return T

def triality_m0():
 m=0
 T=[[[0]*8 for _ in range(8)]for _ in range(8)]
 def setp(i,j,terms):
  for k,v in terms.items():T[i][j][k]=T[j][i][k]=v
 for i in range(8):setp(0,i,{i:1})
 for i,j in enumerate([1,0,2,4,3,5,6,7]):setp(1,i,{j:1})
 setp(2,2,{0:1,1:1,2:1})
 for i in(3,4):setp(2,i,{3:1,4:1})
 for i in(3,4):setp(i,i,{0:1,2:1,3:1,4:1})
 setp(3,4,{1:1,2:1,3:1,4:1})
 for i in range(3):
  setp(2,5+i,{5+(i+1)%3:1,5+(i+2)%3:1})
  for j in(3,4):setp(j,5+i,{5:1,6:1,7:1})
  setp(5+i,5+i,{0:1,1:1,3:1,4:1,5+(i-1+m)%3:1,5+(i+1+m)%3:1})
 for i,j in itertools.combinations(range(3),2):
  terms={2:1,3:1,4:1};terms[5+i]=T[5+i][5+i][5+j];terms[5+j]=T[5+j][5+j][5+i];terms[5+(3-i-j)]=2-terms[5+i]-terms[5+j]
  setp(5+i,5+j,terms)
 return T
