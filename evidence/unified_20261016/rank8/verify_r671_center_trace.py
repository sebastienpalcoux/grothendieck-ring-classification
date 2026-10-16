#!/usr/bin/env python3
"""Complete source-bound R671 center trace exclusion; exact standard library only."""
import argparse,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
P=list(itertools.combinations_with_replacement(range(1,8),2))
A=[1,1,3,4,4,3,2,2];B=[0,0,1,1,1,1,1,1]
FS=[4,6,6,12,12,12]
RAW=[[1,-1,1,0,0,-1,0,0],[1,-1,-1,1,-1,1,0,0],[1,1,1,-1,-1,1,0,0],[1,-1,-1,-2,2,1,0,0],[1,1,-1,0,0,-1,1,1],[1,1,-1,0,0,-1,1,1]]
CH=[[(x,0) for x in row] for row in RAW]
CH[4][6]=(1,1);CH[4][7]=(1,-1);CH[5][6]=(1,-1);CH[5][7]=(1,1)
UNRESTRICTED=[((8,0),(8,0)),((-8,0),(8,0)),((4,0),(-4,0)),((-4,0),(-4,0)),((0,0),(-8,0)),((0,1),(0,0)),((0,-1),(0,0)),((0,0),(0,1)),((0,0),(0,-1))]
RESTRICTED=[((-8,0),(8,0)),((0,0),(-8,0)),((-2,0),(-2,0)),((0,0),(0,0)),((2,0),(-2,0)),((0,0),(2,0)),((0,-1),(0,0))]
def req(x,m):
 if not x:raise RuntimeError(m)
def flat(N):return tuple(x for m in N for r in m for x in r)
def mul(z,w,r):return(z[0]*w[0]+r*z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def dim(v):return(sum(x*y for x,y in zip(v,A)),sum(v[2:]))
def evaluate(c,v):return tuple(sum(x*y[j] for x,y in zip(v,c)) for j in range(2))
def sub(R,v):return [[R[i][j]-v[i]*v[j] for j in range(8)] for i in range(8)]
def psd(M):
 C=[[F(x) for x in row] for row in M]
 for k in range(len(C)):
  p=C[k][k]
  if p<0:return False
  if not p:
   if any(C[k][j] for j in range(k+1,len(C))):return False
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
 if b%3:return None
 return tuple(v[i]+B[i]*(a-10*b//3) for i in range(8))
def arithmetic(a,b):
 n=a*a-10*b*b
 return bool(n) and (120*a-360*b)%n==0 and (36*a-120*b)%n==0
def source(repo):
 rows=[]
 for l in gzip.open(repo/'supplements/rank8/data/rank8_tables.txt.gz','rt'):
  if l.strip():
   N=json.loads(l.replace('{','[').replace('}',']'))
   if max(flat(N))==2:rows.append(N)
 rows.sort(key=flat);N=rows[670]
 req(hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()=='299ed4d94e5e3e54de5c4699704f5a335012b06efa9cc259c1f732b40f5c595d','immutable source tensor hash')
 du=[next(j for j in range(8) if N[i][j][0]) for i in range(8)]
 req(du==list(range(8)),'all source objects selfdual')
 req(all(N[0][i]==N[i][0]==[int(i==j) for j in range(8)] for i in range(8)),'unit')
 req(all(N[i][j][k]==N[j][i][k]==N[i][k][j] for i in range(8) for j in range(8) for k in range(8)),'symmetric tensor')
 for i,j,k,l in itertools.product(range(8),repeat=4):req(sum(N[i][j][t]*N[t][k][l] for t in range(8))==sum(N[j][k][t]*N[i][t][l] for t in range(8)),'associativity')
 dims=list(zip(A,B))
 for i,j in itertools.product(range(8),repeat=2):req(mul(dims[i],dims[j],10)==tuple(sum(N[i][j][k]*dims[k][t] for k in range(8)) for t in range(2)),'dimension character')
 req(len(set(tuple(c) for c in CH))==6,'six distinct remaining characters')
 req(all(any(x==(0,0) for x in c) for c in CH),'remaining characters have zero values')
 req(all(a*a-10*b*b for a,b in dims) and any(b for a,b in dims),'FP and Galois characters are distinct and nowhere zero; eight characters complete')
 for i in range(8):
  ell=F(A[i])-F(10*B[i],3)
  req((A[i]+18*ell,B[i]+6*ell)==mul((19,6),(A[i],-B[i]),10),'exact dimension transport')
 req(sum(A[i]*B[i] for i in range(8))-F(10*sum(x*x for x in B),3)==-2,'transport involution')
 for c,f in zip(CH,FS):
  for i,j in itertools.product(range(8),repeat=2):req(mul(c[i],c[j],3)==tuple(sum(N[i][j][k]*c[k][t] for k in range(8)) for t in range(2)),'ordinary character')
  req(tuple(sum(mul(x,x,3)[j] for x in c) for j in range(2))==(f,0),'formal codegree')
  req(evaluate(c,B)==(0,0),'transport annihilates other characters')
 req(tuple(sum(mul(x,x,10)[j] for x in dims) for j in range(2))==(120,36),'global dimension')
 req(120*120-10*36*36==1440 and 2*36*20==1440,'norm and exact conductor40 saturation')
 req(59**2%40==1 and 59%12==11 and 59%40==19,'coherent Galois exponent CRT')
 # The graph of all forced pivotal sign equalities is connected to the unit.
 edges=[]
 for x,y in itertools.product(range(8),repeat=2):
  for z in range(8):
   if sum(N[x][y][t]*N[t][x][z] for t in range(8))%2:edges.append((y,z))
 for x,z in itertools.product(range(8),repeat=2):
  if sum(N[x][x][t]*N[t][x][z] for t in range(8))%2:edges.append((x,z))
 reached={0}
 while True:
  new=reached|{v for u,v in edges if u in reached}|{u for u,v in edges if v in reached}
  if new==reached:break
  reached=new
 req(len(reached)==8,'all second indicators positive')
 req(N[1][1]==[1]+[0]*7,'pointed involution')
 omega=[sum(N[k][k][j] for k in range(8)) for j in range(8)];req(omega==[8,2,4,6,8,6,6,6],'FI1')
 C=[[sum(N[k][i][l]*N[k][j][l] for k in range(8) for l in range(8)) for j in range(8)] for i in range(8)]
 return N,omega,C

def low_frames(omega,C):
 base=[(1,0,0,0,0,0,0,0),(1,0,1,1,1,1,1,1)]
 req(transport(base[0])==base[1] and transport(base[1])==base[0],'forced Galois unit rows')
 R0=sub(sub(C,base[0]),base[1]);target=tuple(omega[i]-sum(v[i] for v in base) for i in range(8));dom=[]
 for f in FS:
  DD=[];aa,bb=120//f,36//f
  for tail in itertools.product(*(range(min(target[i],bb)+1) for i in range(2,8))):
   if sum(tail)!=bb:continue
   inv=aa-1-sum(A[i]*tail[i-2] for i in range(2,8))
   if not 0<=inv<=target[1]:continue
   v=(1,inv)+tail
   if good(sub(R0,v)):DD.append(v)
  dom.append(DD)
 ev=[[ [evaluate(CH[i],v) for v in dom[j]] for j in range(6)] for i in range(6)]
 compat={}
 for i,j in itertools.permutations(range(6),2):
  buckets={}
  for k,v in enumerate(ev[i][j]):buckets.setdefault(tuple(FS[j]*x for x in v),set()).add(k)
  compat[i,j]=[buckets.get(tuple(FS[i]*x for x in v),set()) for v in ev[j][i]]
 out=[];nodes=[0]*7
 def rec(chosen,avail,sums,R):
  nodes[len(chosen)]+=1
  if len(chosen)==6:
   if sums==target:out.append(base+[dom[j][chosen[j]] for j in range(6)])
   return
  j=min(avail,key=lambda j:(len(avail[j]),j))
  for k in sorted(avail[j]):
   v=dom[j][k];ss=tuple(sums[i]+v[i] for i in range(8))
   if any(ss[i]>target[i] for i in range(8)):continue
   RR=sub(R,v)
   if not good(RR):continue
   new={i:avail[i]&compat[j,i][k] for i in avail if i!=j}
   if any(not ks for ks in new.values()):continue
   if any(ss[c]+sum(min(dom[i][k][c] for k in ks) for i,ks in new.items())>target[c] or ss[c]+sum(max(dom[i][k][c] for k in ks) for i,ks in new.items())<target[c] for c in range(8)):continue
   rec({**chosen,j:k},new,ss,RR)
 rec({}, {j:set(range(len(dom[j]))) for j in range(6)},(0,)*8,R0)
 return out,[len(d) for d in dom],nodes

def high_columns(low,C):
 R=C
 for v in low:R=sub(R,v)
 bounds=[math.isqrt(R[i][i]) for i in range(8)];orbits=[]
 for tail in itertools.product(*(range(bounds[i]+1) for i in range(1,8))):
  v=(0,)+tail;aa,bb=dim(v)
  if not any(v) or bb%3 or not arithmetic(aa,bb):continue
  w=transport(v)
  if min(w)<0:w=tuple(-x for x in w)
  if min(w)<0 or v>w:continue
  orbit=[v] if v==w else[v,w]
  RR=R
  for x in orbit:RR=sub(RR,x)
  if not good(RR):continue
  ds=[dim(x) for x in orbit]
  if any(not arithmetic(*d) for d in ds):continue
  rat=3*aa==10*bb
  vertices=([UNRESTRICTED[0],UNRESTRICTED[1]] if rat else[UNRESTRICTED[1]]) if v[1] else (UNRESTRICTED if rat else RESTRICTED)
  orbits.append((orbit,ds,vertices))
 cols=[]
 for orbit,ds,vertices in orbits:
  gram=[sum(v[i]*v[j] for v in orbit) for i,j in P]
  for vertex in vertices:
   col=gram[:]
   for x,y in vertex:
    for i in range(1,8):col.extend([sum(v[i]*(aa*x+10*bb*y) for v,(aa,bb) in zip(orbit,ds)),sum(v[i]*(aa*y+bb*x) for v,(aa,bb) in zip(orbit,ds))])
   cols.append(col)
 rhs=[R[i][j] for i,j in P];ds=[dim(v) for v in low]
 for moment in[1,2]:
  for i in range(1,8):
   ll=[sum(v[i]*d[j] for v,d in zip(low,ds)) for j in range(2)]
   rhs.extend([8*(-ll[0]+(120 if moment==2 else 0)),8*(-ll[1]+(36 if moment==2 else 0))])
 return cols,rhs,len(orbits)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('r671_center_trace_certificate.json'));ap.add_argument('--output',type=Path);args=ap.parse_args()
 N,omega,C=source(args.repo);frames,domains,nodes=low_frames(omega,C);req(len(frames)==6,'complete six low frames');cert=json.loads(args.certificate.read_text());reports=[]
 for k,low in enumerate(frames):
  cols,rhs,n=high_columns(low,C);found=None
  for j,Y in enumerate(cert['separators']):
   req(len(Y)==len(rhs)==56,'separator dimension');mins=min(sum(x*y for x,y in zip(Y,c)) for c in cols);value=sum(x*y for x,y in zip(Y,rhs))
   if mins>=0 and value<0:found={'frame':k,'orbits':n,'moment_columns':len(cols),'separator':j,'minimum_column_pairing':mins,'rhs_pairing':value};break
  req(found is not None,'every frame separated');reports.append(found)
 result={'status':'PASS','id':'R8_2_671','criterion':'quadratic_conductor40_center_trace','scope':'general_complex_given_HI6_PAIR_GALOIS_PU','tensor_sha256':hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest(),'low_domain_counts':domains,'low_search_nodes':nodes,'complete_low_frames':len(frames),'frames':reports,'optimizer_used':False,'floating_arithmetic_used':False}
 text=json.dumps(result,indent=2)+'\n'
 if args.output:args.output.write_text(text)
 print(text)
if __name__=='__main__':main()
