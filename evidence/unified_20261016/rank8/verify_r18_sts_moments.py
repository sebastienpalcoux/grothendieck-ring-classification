#!/usr/bin/env python3
"""R8_1_18: exact source, character, full Galois-orbit and STS moment obstruction.
Standard library only; no optimizer or floating arithmetic.
"""
import argparse,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
SHA='cdd3aa4477861e8521c75ac63cb0f9e4e5d0a021073d1619aae358a0850704f2'
INV=[0,1,2,7];NON=[3,4,5,6];MAP=[0,1,7,2,3,6,5,4]
P=[0,2,1,6,5,4,3,7];DU=[0,2,1,4,3,6,5,7]
PAIRS=list(itertools.combinations_with_replacement(range(1,8),2));ZERO=(0,0,0,0)
def req(x,msg):
 if not x:raise RuntimeError(msg)
def flat(N):return tuple(x for M in N for v in M for x in v)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(n,a):return tuple(n*x for x in a)
def power(n):
 n%=8;v=[0]*4;v[n%4]=(-1 if n>=4 else 1);return tuple(v)
def mul(a,b):
 v=[0]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):v[(i+j)%4]+=x*y*(-1 if i+j>=4 else 1)
 return tuple(v)
def conj(a):return tuple(sum(a[j]*power(-j)[i]for j in range(4))for i in range(4))
def sigma3(a):return tuple(sum(a[j]*power(3*j)[i]for j in range(4))for i in range(4))
def qmul(a,b):return(a[0]*b[0]+a[1]*b[1],a[0]*b[1]+a[1]*b[0]+4*a[1]*b[1])
def summ(vs):
 out=ZERO
 for v in vs:out=add(out,v)
 return out
def dim(v):return(sum(v[i]for i in INV),sum(v[i]for i in NON))
def sub(R,v):return[[R[i][j]-v[i]*v[j]for j in range(8)]for i in range(8)]
def psd(R):
 M=[[F(x)for x in row]for row in R]
 for k in range(len(M)):
  p=M[k][k]
  if p<0:return False
  if not p:
   if any(M[k][j]for j in range(k+1,len(M))):return False
   continue
  for i in range(k+1,len(M)):
   for j in range(i,len(M)):M[j][i]=M[i][j]=M[i][j]-M[i][k]*M[k][j]/p
 return True
def good(R):return all(x>=0 for row in R for x in row)and psd(R)
def integral(a,b):
 n=a*a+4*a*b-b*b
 if not n:return False
 x=F(8*a+16*b,n);y=F(16*a-8*b,n)
 return(2*x+4*y).denominator==1 and(x*x+4*x*y-y*y).denominator==1
def transport(v):
 a,b=dim(v)
 if b%2:return None
 w=tuple(v[i]+(a-b//2 if i in NON else 0)for i in range(8))
 if min(w)<0:w=tuple(-x for x in w)
 return w if min(w)>=0 else None
def full_orbit(v):
 todo=[v];seen=set()
 while todo:
  x=todo.pop()
  if x in seen:continue
  seen.add(x);t=transport(x)
  if t is None:return None
  todo.extend([t,tuple(x[P[i]]for i in range(8)),tuple(x[DU[i]]for i in range(8))])
 return tuple(sorted(seen))
def source(repo):
 tensors=[]
 for line in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
  N=json.loads(line.replace('{','[').replace('}',']'))
  if max(flat(N))==1:tensors.append(N)
 tensors.sort(key=flat);N=tensors[17]
 req(hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()==SHA,'source hash')
 for i,j in itertools.product(range(8),repeat=2):
  out=[0]*8
  if i<4 and j<4:out[MAP[(i+j)%4]]=1
  elif i<4 or j<4:out[MAP[4+(i+j)%4]]=1
  else:
   out[MAP[(i+j+1)%4]]=1
   for a in NON:out[a]=1
  req(N[MAP[i]][MAP[j]]==out,'all source model coefficients')
 req([next(j for j in range(8)if N[i][j][0])for i in range(8)]==DU,'duality')
 dims=[(1,0)if i in INV else(0,1)for i in range(8)]
 for i,j in itertools.product(range(8),repeat=2):req(qmul(dims[i],dims[j])==tuple(sum(N[i][j][k]*dims[k][h]for k in range(8))for h in range(2)),'FP character')
 req(tuple(sum(qmul(d,d)[k]for d in dims)for k in range(2))==(8,16),'global dimension')
 req(40*40-5*16*16==320 and 320==2**6*5,'Cauchy rational prime support')
 chars=[]
 for k in[1,2,3]:
  for sign in[1,-1]:
   row=[None]*8
   for j in range(4):row[MAP[j]]=power(2*k*j);row[MAP[4+j]]=scale(sign,power(k+2*k*j))
   chars.append(row)
 for c in chars:
  for i,j in itertools.product(range(8),repeat=2):req(mul(c[i],c[j])==summ(scale(N[i][j][k],c[k])for k in range(8)),'source character identity')
  req(summ(mul(c[i],c[DU[i]])for i in range(8))==(8,0,0,0),'formal codegree8')
  req(summ(c[i]for i in NON)==ZERO,'quadratic Galois transport on f8 characters')
  req(all(c[P[i]]==sigma3(c[i])for i in range(8)),'full extra Galois permutation')
 req(len({tuple(c)for c in chars})==6,'distinct f8 characters')
 C=[[sum(N[k][i][l]*N[k][j][l]for k in range(8)for l in range(8))for j in range(8)]for i in range(8)]
 req(C[0]==[8,0,0,4,4,4,4,0],'unit induction row')
 req(all(C[i][j]==8*int(i==j)for i in INV for j in INV),'pointed Gram and Fourier multiplicity bound')
 return N,C,chars

def low_frames(C,chars):
 profiles=[v for v in itertools.product(range(3),repeat=4)if sum(v)==2]
 values=[[summ(scale(n,c[MAP[4+j]])for j,n in enumerate(v))for v in profiles]for c in chars]
 dual=[5,4,3,2,1,0];star=lambda v:tuple(v[(-1-j)%4]for j in range(4));sol=[]
 def rec(chosen,sums):
  i=len(chosen)
  if i==6:
   if sums==[3]*4:sol.append(chosen)
   return
  for a,v in enumerate(profiles):
   if any(sums[j]+v[j]>3 for j in range(4)):continue
   if any(values[j][a]!=values[i][chosen[j]]for j in range(i)):continue
   if any(i==dual[j]and v!=star(profiles[chosen[j]])for j in range(i)):continue
   rec(chosen+[a],[sums[j]+v[j]for j in range(4)])
 rec([],[0]*4);req(len(sol)==8,'exhaustive eight low assignments');out=[]
 averaged=[[(1,0)if i in INV else(0,1)for i in range(8)],[(1,0)if i in INV else(4,-1)for i in range(8)]]+ [[(c[i][0],0)for i in range(8)]for c in chars]
 for ids in sol:
  low=[(1,0,0,0,0,0,0,0),(1,0,0,1,1,1,1,0)]
  for a in ids:
   v=[1]+[0]*7
   for j,n in enumerate(profiles[a]):v[MAP[4+j]]=n
   low.append(tuple(v))
  R=C
  for v in low:R=sub(R,v)
  req(good(R),'low residual Gram')
  for i,j in itertools.product(range(1,8),repeat=2):
   actual=tuple(sum(low[a][i]*averaged[a][j][h]for a in range(8))for h in range(2));req(actual==((4,-1)if i in NON and j in NON else(0,0)),'full relative STS target')
  out.append(low)
 return out

def mobius(n):
 p=2;ans=1
 while p*p<=n:
  if n%p==0:
   n//=p;ans=-ans
   if n%p==0:return 0
  while n%p==0:n//=p
  p+=1
 return-ans if n>1 else ans
def relative_root(N,k,m):
 g=math.gcd(k*m,N);M=N//g;l=k*m//g;a=b=0;n=M
 while n>1 and n%2==0:a+=1;n//=2
 while n>1 and n%5==0:b+=1;n//=5
 req(n==1,'root prime support')
 if b==0:return(F(mobius(M),sum(math.gcd(j,M)==1 for j in range(M))if M>1 else 1),F(0))
 if b>=2 or a>=2:return(F(0),F(0))
 e=l*pow(2**a,-1,5)%5;u=(F(-3,4),F(1,4))if e in[1,4]else(F(1,4),F(-1,4));return tuple((-1 if a==1 else 1)*x for x in u)
def phases():
 out={tuple(tuple(8*x for x in relative_root(40,k,m))for m in[1,2,4])for k in range(40)};out.add(((F(0),F(0)),)*3)
 req(len(out)==13,'complete thirteen prime-supported relative phase vectors')
 return sorted(out)
def high_system(low,C,k):
 R=C
 for v in low:R=sub(R,v)
 bounds=[math.isqrt(R[i][i])for i in range(8)];bounds[1]=bounds[2]=1;orbits=[]
 for tail in itertools.product(*(range(bounds[i]+1)for i in range(1,8))):
  v=(0,)+tail
  if not any(v)or not integral(*dim(v)):continue
  orb=full_orbit(v)
  if orb is None or v!=min(orb):continue
  RR=R
  for x in orb:RR=sub(RR,x)
  if not good(RR)or any(not integral(*dim(x))for x in orb):continue
  orbits.append(orb)
 cols=[]
 for orb in orbits:
  ds=[dim(x)for x in orb];pv=phases()
  if any(x[1]or x[2]for x in orb):pv=[((8,0),(8,0),(8,0)),((-8,0),(8,0),(8,0)),((0,0),(-8,0),(8,0))]if k==0 else[((0,0),(0,0),(-8,0))]if k==2 else[((0,0),)*3]
  if any(x[7]for x in orb):pv=[((8,0),(8,0),(8,0)),((-8,0),(8,0),(8,0))]if k%2==0 else[((0,0),(-8,0),(8,0))]
  gram=[sum(x[i]*x[j]for x in orb)for i,j in PAIRS]
  for v in pv:
   col=gram[:]
   for xx,yy in v[:2]:
    for i in range(1,8):col.extend([sum(x[i]*(a*xx+b*yy)for x,(a,b)in zip(orb,ds)),sum(x[i]*(a*yy+b*xx+4*b*yy)for x,(a,b)in zip(orb,ds))])
   xx,yy=v[2]
   for i in range(1,8):col.append(sum(x[i]*(2*(a*xx+b*yy)-(a*yy+b*xx+4*b*yy))for x,(a,b)in zip(orb,ds)))
   for i,j in PAIRS:
    a=sum(x[i]*x[j]for x in orb);col.extend([a*v[0][0],a*v[0][1]])
   req(all(F(x).denominator==1 for x in col),'integral column');cols.append(tuple(map(int,col)))
 rhs=[R[i][j]for i,j in PAIRS];ld=[dim(v)for v in low]
 for m in[1,2]:
  for i in range(1,8):
   nu=(1 if k%2==0 else-1)if i==7 else 0
   rhs.extend([8*(-sum(x[i]*d[0]for x,d in zip(low,ld))+(8*nu if m==2 else 0)),8*(-sum(x[i]*d[1]for x,d in zip(low,ld))+(16*nu if m==2 else 0))])
 for i in range(1,8):rhs.append(-8*sum(x[i]*(2*d[0]-d[1])for x,d in zip(low,ld)))
 for i,j in PAIRS:
  known=sum(v[i]*v[j]for v in low);target=(4-known,-1)if i in NON and j in NON else(-known,0);rhs.extend([8*x for x in target])
 req(len(rhs)==119,'119-row source-derived moment system')
 return cols,rhs,len(orbits)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('r18_sts_moment_certificate.json'));ap.add_argument('--output',type=Path);args=ap.parse_args();N,C,chars=source(args.repo);lows=low_frames(C,chars);cert=json.loads(args.certificate.read_text());branches=[]
 for k in[0,1,2]:
  y=cert['separators'][str(k)];req(len(y)==119 and all(type(x)==int for x in y),'integer covector')
  for f,low in enumerate(lows):
   cols,rhs,n=high_system(low,C,k);mn=min(sum(x*z for x,z in zip(y,c))for c in cols);b=sum(x*z for x,z in zip(y,rhs));req(mn>=0 and b<0,'exact separating inequality')
   branches.append({'pointed_class':k,'frame':f,'row_orbits':n,'moment_columns':len(cols),'minimum_column_pairing':mn,'rhs_pairing':b})
 result={'status':'PASS','id':'R8_1_18','criterion':'cyclic_induction_STS_fourth_moment','scope':'general_complex_after_two_dimension_Galois_pseudo_unitarity','tensor_sha256':SHA,'low_assignments':len(lows),'phase_vectors':len(phases()),'odd_classes_combined':[1,3],'branches':branches,'optimizer_used':False,'floating_arithmetic_used':False};txt=json.dumps(result,indent=2)+'\n'
 if args.output:args.output.write_text(txt)
 print(txt)
if __name__=='__main__':main()
