#!/usr/bin/env python3
"""Exact necessary obstruction: R8_1_9 cannot have pointed C4 class2."""
import argparse,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
P=list(itertools.combinations_with_replacement(range(1,8),2));NON=[3,4,5,6];INV=[0,1,2,7];MAP=[0,1,7,2,5,3,6,4]
BASE=[((4,0),(4,0)),((-4,0),(4,0)),((0,0),(-4,0)),((-3,1),(1,-1)),((1,-1),(-3,1)),((3,-1),(1,-1)),((-1,1),(-3,1)),((0,0),(3,-1)),((0,0),(-1,1))]
VERTICES=[tuple(tuple(2*x for x in p)for p in v)for v in BASE]+[tuple(tuple(-x for x in p)for p in BASE[k])for k in[0,1,3,4,5,6,7,8]]
def req(x,m):
 if not x:raise RuntimeError(m)
def flat(N):return tuple(x for M in N for row in M for x in row)
def mul(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qmul(x,y):return(x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0]+4*x[1]*y[1])
def dim(v):return(sum(v[i]for i in INV),sum(v[i]for i in NON))
def sub(R,v):return[[R[i][j]-v[i]*v[j]for j in range(8)]for i in range(8)]
def psd(M):
 C=[[F(x)for x in row]for row in M]
 for k in range(len(C)):
  p=C[k][k]
  if p<0:return False
  if not p:
   if any(C[k][j]for j in range(k+1,len(C))):return False
   continue
  for i in range(k+1,len(C)):
   for j in range(i,len(C)):C[j][i]=C[i][j]=C[i][j]-C[i][k]*C[k][j]/p
 return True
def good(R):
 if any(x<0 for row in R for x in row):return False
 if any(R[i][i]*R[j][j]<R[i][j]**2 for i,j in P):return False
 return psd(R)
def transport(v):
 a,b=dim(v)
 if b%2:return None
 return tuple(v[i]+(a-b//2 if i in NON else 0)for i in range(8))
def arithmetic(a,b):
 n=a*a+4*a*b-b*b
 if not n:return False
 x=F(8*a+16*b,n);y=F(16*a-8*b,n)
 return(2*x+4*y).denominator==1 and(x*x+4*x*y-y*y).denominator==1
def chars():
 out=[]
 for a in[(-1,0),(0,1),(0,-1)]:
  for sign in[1,-1]:
   p=(1,0);gp=[];np=[]
   for j in range(4):gp.append(p);np.append((sign*p[0],sign*p[1]));p=mul(p,a)
   c=gp+np;out.append([c[MAP.index(i)]for i in range(8)])
 return out
def source(repo):
 rr=[]
 for line in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
  N=json.loads(line.replace('{','[').replace('}',']'))
  if max(flat(N))==1:rr.append(N)
 rr.sort(key=flat);N=rr[8]
 req(hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()=='1718ab13b6969ed751b621f7303b9e2bb29bb8280f692315499b130a420538f6','immutable source hash')
 du=[next(j for j in range(8)if N[i][j][0])for i in range(8)]
 req(du==[0,2,1,4,3,5,6,7],'duality')
 req(all(N[0][i]==N[i][0]==[int(i==j)for j in range(8)]for i in range(8)),'unit')
 req(all(N[i][j][k]==N[j][i][k]==N[du[i]][k][j]for i,j,k in itertools.product(range(8),repeat=3)),'commutativity and Frobenius')
 for i,j,k,l in itertools.product(range(8),repeat=4):req(sum(N[i][j][t]*N[t][k][l]for t in range(8))==sum(N[j][k][t]*N[i][t][l]for t in range(8)),'associativity')
 dims=[(1,0)if i in INV else(0,1)for i in range(8)]
 for i,j in itertools.product(range(8),repeat=2):req(qmul(dims[i],dims[j])==tuple(sum(N[i][j][k]*dims[k][a]for k in range(8))for a in range(2)),'FP character')
 CH=chars();req(len(set(tuple(c)for c in CH))==6,'six distinct remaining characters')
 for c in CH:
  for i,j in itertools.product(range(8),repeat=2):req(mul(c[i],c[j])==tuple(sum(N[i][j][k]*c[k][a]for k in range(8))for a in range(2)),'ordinary character')
  req(tuple(sum(mul(c[i],c[du[i]])[a]for i in range(8))for a in range(2))==(8,0),'formal codegree8')
  req(tuple(sum(c[i][a]for i in NON)for a in range(2))==(0,0),'transport annihilates other characters')
 req(all(N[MAP[i]][MAP[j]]==[int(k==MAP[(i+j)%4])for k in range(8)]for i,j in itertools.product(range(4),repeat=2)),'pointed C4 labels')
 for x in[5,6]:
  cube=[sum(N[x][x][j]*N[j][x][k]for j in range(8))for k in range(8)]
  req(all(cube[i]%2 for i in INV),'odd cube forces positive selfdual source and involution indicators')
 C=[[sum(N[k][i][l]*N[k][j][l]for k in range(8)for l in range(8))for j in range(8)]for i in range(8)]
 req(C[0]==[8,0,0,4,4,4,4,0],'FI1')
 return N,C,CH

def low_frames(C,CH):
 dom=[v for v in itertools.product(range(3),repeat=4)if sum(v)==2];real=[v for v in dom if v[1]==v[3]];star=lambda v:(v[0],v[3],v[2],v[1]);out=[];counts=[0,0,0,0]
 for aa,bb,cc,dd in itertools.product(real,real,dom,dom):
  counts[0]+=1;profiles=[aa,bb,cc,dd,star(cc),star(dd)]
  if any(sum(v[j]for v in profiles)!=3 for j in range(4)):continue
  counts[1]+=1;low=[(1,0,0,0,0,0,0,0),(1,0,0,1,1,1,1,0)]
  for row in profiles:
   vv=[1]+[0]*7
   for j,x in enumerate(row):vv[MAP[4+j]]=x
   low.append(tuple(vv))
  ev=[[tuple(sum(c[i][a]*v[i]for i in range(8))for a in range(2))for v in low[2:]]for c in CH]
  if any(ev[i][j]!=ev[j][i]for i,j in itertools.product(range(6),repeat=2)):continue
  counts[2]+=1;R=C
  for v in low:R=sub(R,v)
  if not good(R):continue
  counts[3]+=1;out.append(low)
 return out,counts

def high_columns(low,C):
 R=C
 for v in low:R=sub(R,v)
 bounds=[math.isqrt(R[i][i])for i in range(8)];orbits=[]
 for tail in itertools.product(*(range(bounds[i]+1)for i in range(1,8))):
  v=(0,)+tail;a,b=dim(v)
  if not any(v)or b%2 or not arithmetic(a,b):continue
  w=transport(v)
  if min(w)<0:w=tuple(-x for x in w)
  if min(w)<0 or v>w:continue
  orbit=[v]if v==w else[v,w];RR=R
  for x in orbit:RR=sub(RR,x)
  if not good(RR):continue
  ds=[dim(x)for x in orbit]
  if any(not arithmetic(*d)for d in ds):continue
  vertices=VERTICES
  if v[1]or v[2]:vertices=[((0,0),(0,0))] # theta^4=-1: primitive eighth roots
  if v[7]:vertices=VERTICES[:2] # theta²=+1
  orbits.append((orbit,ds,vertices))
 cols=[]
 for orbit,ds,vertices in orbits:
  gram=[sum(v[i]*v[j]for v in orbit)for i,j in P]
  for vertex in vertices:
   col=gram[:]
   for x,y in vertex:
    for i in range(1,8):col.extend([sum(v[i]*(a*x+b*y)for v,(a,b)in zip(orbit,ds)),sum(v[i]*(a*y+b*x+4*b*y)for v,(a,b)in zip(orbit,ds))])
   cols.append(col)
 rhs=[R[i][j]for i,j in P];ds=[dim(v)for v in low];nu=[1,0,0,0,0,1,1,1]
 for moment in[1,2]:
  for i in range(1,8):rhs.extend([8*(-sum(v[i]*d[0]for v,d in zip(low,ds))+(8*nu[i]if moment==2 else 0)),8*(-sum(v[i]*d[1]for v,d in zip(low,ds))+(16*nu[i]if moment==2 else 0))])
 return cols,rhs,len(orbits)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('r9_pointed_class2_certificate.json'));ap.add_argument('--output',type=Path);a=ap.parse_args();N,C,CH=source(a.repo);frames,counts=low_frames(C,CH);req(len(frames)==8,'eight exhaustive low frames');Y=json.loads(a.certificate.read_text())['separator'];out=[]
 for j,low in enumerate(frames):
  cols,rhs,n=high_columns(low,C);req(len(Y)==len(rhs)==56,'separator dimension');mn=min(sum(x*y for x,y in zip(Y,c))for c in cols);value=sum(x*y for x,y in zip(Y,rhs));req(mn>=0 and value<0,'exact separator')
  out.append({'frame':j,'row_orbits':n,'moment_columns':len(cols),'minimum_column_pairing':mn,'rhs_pairing':value})
 result={'status':'PASS','id':'R8_1_9','scope':'excludes pointed C4 associator class2 only; class0 remains open','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'low_counts':counts,'frames':out,'optimizer_used':False,'floating_arithmetic_used':False};txt=json.dumps(result,indent=2)+'\n'
 if a.output:a.output.write_text(txt)
 print(txt)
if __name__=='__main__':main()
