"""Source-bound, exact modular induction-lattice obstruction for R7_3_601.

Uses only Python's standard library. No numerical eigensolver, LP/MILP solver,
or external mathematical software is used by this verifier.
"""
import argparse,gzip,hashlib,itertools,json,math
from collections import Counter
from fractions import Fraction
from functools import reduce
from pathlib import Path

DIGEST='afbed9441f88f4ba296235d0dd6220f41ecbcf97a7424220125e73f255ff489c'
DIMS=[1,5,5,8,8,9,10]
CHARS=[[1,1,1,0,0,1,-2],[1,0,0,1,0,-1,0],
 [1,0,0,-2,3,-1,0],[1,-1,-1,0,0,1,0],
 [1,2,-1,-1,-1,0,1],[1,-1,2,-1,-1,0,1],DIMS]
PAIRS=[(i,j)for i in range(6)for j in range(i+1)]

def need(ok,msg):
 if not ok:raise ValueError(msg)

def psd(A):
 """Exact symmetric Schur elimination, including zero pivots."""
 A=[list(r)for r in A]
 while A:
  if any(A[i][i]<0 for i in range(len(A))):return False
  if A[0][0]==0:
   if any(A[0]):return False
   A=[r[1:]for r in A[1:]];continue
  p=A[0][0]
  B=[[p*A[i][j]-A[i][0]*A[0][j]for j in range(1,len(A))]for i in range(1,len(A))]
  g=reduce(math.gcd,(abs(x)for r in B for x in r),0)
  A=[[x//g for x in r]for r in B]if g>1 else B
 return True

def inverse_scaled(A):
 """Return positive integer h and integer H with H=h A^{-1}."""
 n=len(A);B=[[Fraction(A[i][j])for j in range(n)]+[Fraction(i==j)for j in range(n)]for i in range(n)]
 for k in range(n):
  need(B[k][k]>0,'positive definite residual Schur pivot')
  a=B[k][k];B[k]=[x/a for x in B[k]]
  for i in range(n):
   if i!=k:
    a=B[i][k];B[i]=[x-a*y for x,y in zip(B[i],B[k])]
 Q=[r[n:]for r in B];h=math.lcm(*(x.denominator for r in Q for x in r));H=[[int(h*x)for x in r]for r in Q]
 need(all(sum(A[i][k]*H[k][j]for k in range(n))==h*int(i==j)for i in range(n)for j in range(n)),'inverse identity')
 return h,H

def low_blocks(C,zs):
 domains={}
 for z in set(zs):
  out=[]
  def gen(i,v,left):
   if i==7:
    if left==0:out.append([1]+v)
    return
   for k in range(min(C[0][i],math.isqrt(C[i][i]),left//DIMS[i])+1):gen(i+1,v+[k],left-k*DIMS[i])
  gen(1,[],z-1);domains[z]=out
 sols=[];nodes=[0]*7;target=[C[i][0]-int(i==0)for i in range(7)]
 def rec(k,rem,B,chosen):
  nodes[k]+=1
  if k==6:
   if not any(rem):sols.append(chosen)
   return
  z=zs[k]
  for v in domains[z]:
   if k and zs[k-1]==z and v<chosen[-1]:continue
   if any(x>y for x,y in zip(v,rem)):continue
   BB=[[B[i][j]-v[i]*v[j]for j in range(7)]for i in range(7)]
   if any(x<0 for r in BB for x in r):continue
   if any(BB[i][i]*BB[j][j]<BB[i][j]**2 for i in range(7)for j in range(i)):continue
   if not psd(BB):continue
   rec(k+1,[x-y for x,y in zip(rem,v)],BB,chosen+[v])
 rec(0,target,[[C[i][j]-int(i==j==0)for j in range(7)]for i in range(7)],[])
 return sols,nodes,{str(z):len(v)for z,v in sorted(domains.items())}

def prime_power(n):
 for p in range(2,n+1):
  if n%p:continue
  while n%p==0:n//=p
  return n==1
 return False

def verify(repo):
 with gzip.open(repo/'supplements/rank7/data/rank7_tables.txt.gz','rt')as f:
  for line,s in enumerate(f,1):
   if line==2455:N=json.loads(s.replace('{','[').replace('}',']'));break
 digest=hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest();need(digest==DIGEST,'immutable census source')
 ledger=json.loads((repo/'supplements/rank7/output/rank7_ledger.json').read_text());entry=next(r for r in ledger if r['id']=='R7_3_601');need(entry['tensor']==N and entry['source_line']==2455,'ledger source binding')
 need(all(N[i][j]==N[j][i]for i in range(7)for j in range(7)),'commutative')
 need(all(N[i][j][0]==int(i==j)for i in range(7)for j in range(7)),'self dual')
 need(all(sum(N[i][j][k]*N[k][l][a]for k in range(7))==sum(N[j][l][k]*N[i][k][a]for k in range(7))for i in range(7)for j in range(7)for l in range(7)for a in range(7)),'associativity')
 for t in CHARS:
  need(all(sum(N[i][j][k]*t[k]for k in range(7))==t[i]*t[j]for i in range(7)for j in range(7)),'exact character')
 need(all(sum(x*y for x,y in zip(a,b))==0 for i,a in enumerate(CHARS)for b in CHARS[:i]),'complete orthogonal character table')
 for start in range(1,7):
  S={0,start}
  while True:
   T=S|{k for i in S for j in S for k in range(7)if N[i][j][k]}
   if T==S:break
   S=T
  need(len(S)==7,'based-ring simplicity')
 glob=sum(d*d for d in DIMS);need(glob==360,'dimension')
 schur=sum(Fraction(a*a*b,d)for a,b,d in zip(CHARS[2],CHARS[4],DIMS));need(schur==Fraction(-5,8),'group representation obstruction')
 need(glob%25!=0,'modular divisibility obstruction')
 codegrees=sorted(sum(x*x for x in a)for a in CHARS);need(codegrees==[3,4,8,9,9,15,360],'formal codegrees')
 zs=sorted(glob//f for f in codegrees if f!=glob)
 C=[[sum(N[a][i][k]*N[a][j][k]for a in range(7)for k in range(7))for j in range(7)]for i in range(7)]
 blocks,nodes,domains=low_blocks(C,zs);need(len(blocks)==336,'exact low block coverage')
 cert=json.loads((Path(__file__).with_name('r601_center_lattice_certificate.json')).read_text());need(cert['tensor_sha256']==digest,'certificate tensor binding');need(len(cert['branches'])==len(blocks),'certificate branch coverage')
 allowed=[d for d in range(2,glob+1)if glob%d==0 and not prime_power(d)]
 need(allowed==[6,10,12,15,18,20,24,30,36,40,45,60,72,90,120,180,360],'non-prime-power divisors')
 base=[]
 for v in itertools.product(*(range(math.isqrt(C[i][i])+1)for i in range(1,7))):
  d=sum(x*y for x,y in zip(v,DIMS[1:]))
  if d not in allowed:continue
  q=tuple(v[i]*v[j]for i,j in PAIRS)
  if any(q[k]>C[i+1][j+1]for k,(i,j)in enumerate(PAIRS)):continue
  base.append(q)
 need(len(base)==4700,'exhaustive candidate box')
 counts=Counter();min_count=10**9;max_count=0
 for idx,(cols,branch)in enumerate(zip(blocks,cert['branches'])):
  need(branch['low_rows']==cols,'branch ordering and exact rows')
  R=[[C[i+1][j+1]-sum(v[i+1]*v[j+1]for v in cols)for j in range(6)]for i in range(6)]
  b=[R[i][j]for i,j in PAIRS];h,H=inverse_scaled(R);coeff=[H[i][j]*(1 if i==j else 2)for i,j in PAIRS]
  p=branch['prime'];y=branch['dual'];need(p in(2,3)and len(y)==21,'certificate format')
  need(sum(x*z for x,z in zip(y,b))%p==1,'nonzero residual modular value')
  admissible=0
  for q in base:
   if any(x>z for x,z in zip(q,b)):continue
   if sum(x*z for x,z in zip(coeff,q))>h:continue
   admissible+=1
   need(sum(x*z for x,z in zip(y,q))%p==0,'annihilation of every admissible central column')
  need(admissible==branch['candidate_count'],'candidate count');counts[p]+=1;min_count=min(min_count,admissible);max_count=max(max_count,admissible)
 need(dict(counts)=={2:218,3:118},'all modular certificates')
 return {'status':'PASS','id':'R7_3_601','tensor_sha256':digest,'dimension_vector':DIMS,'FPdim':glob,'formal_codegrees':codegrees,'I1_nonunit_dimensions':zs,'I1_domain_counts':domains,'exact_enumeration_nodes':nodes,'low_blocks':len(blocks),'global_candidate_columns':len(base),'branch_candidate_range':[min_count,max_count],'modular_certificate_counts':dict(counts),'weighted_group_character_sum':str(schur),'scope':'General complex exclusion, using the cited simple-center and prime-power-dimension theorems; all finite coverage and modular contradictions verified exactly.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args();print(json.dumps(verify(a.repo.resolve()),indent=2))
if __name__=='__main__':main()
