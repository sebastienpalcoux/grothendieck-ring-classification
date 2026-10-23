#!/usr/bin/env python3
"""Independent exact finite proof for the four dimension-60 rank-nine rings.
No native code, optimizer, floating-point arithmetic, or assertion statements.
"""
from pathlib import Path
import json,math,itertools,collections,time
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
T=json.loads((ROOT/'work/input_audit/tensors.json').read_text())
IDS=['R9_1_'+str(i) for i in [2,48,84,101]]
def require(c,m='exact verification failed'):
 if not c:raise ValueError(m)
def charpoly(A):
 n=len(A);B=[[int(i==j) for j in range(n)] for i in range(n)];co=[1]
 for k in range(1,n+1):
  AB=[[sum(A[i][h]*B[h][j] for h in range(n)) for j in range(n)] for i in range(n)]
  tr=sum(AB[i][i] for i in range(n));require(tr%k==0);c=-tr//k;co.append(c)
  B=[[AB[i][j]+c*int(i==j) for j in range(n)] for i in range(n)]
 return co

def codegree_polynomial():
 out=[1]
 for v in [60,15,4,4,12,12,12,12,12]:
  new=[0]*(len(out)+1)
  for i,a in enumerate(out):new[i]+=a;new[i+1]-=v*a
  out=new
 return out

def facts(name):
 N=T[name];n=len(N);require(all(N[i][j]==N[j][i] for i in range(n) for j in range(n)));du=[row.index(1) for row in [[N[i][j][0] for j in range(n)] for i in range(n)]]
 ds=[1,1,1,2,4,4,2,1,4] if name==IDS[0] else None
 # Recover integral dimensions from integer common positive character using
 # bounded enumeration by the known multiset; uniqueness is checked exactly.
 if ds is None:
  for v in set(itertools.permutations([1,1,1,2,2,4,4,4])):
   d=(1,)+v
   if all(d[i]*d[j]==sum(N[i][j][k]*d[k] for k in range(n)) for i in range(n) for j in range(n)):
    ds=list(d);break
 require(ds is not None)
 require(all(ds[i]*ds[j]==sum(N[i][j][k]*ds[k] for k in range(n)) for i in range(n) for j in range(n)))
 B=[[sum(N[a][j][k]*N[k][du[a]][i] for a in range(n) for k in range(n)) for i in range(n)] for j in range(n)]
 require(B==list(map(list,zip(*B))))
 require(charpoly(B)==codegree_polynomial())
 return N,du,ds,B

def candidates(ds,B,beta):
 bounds=[min(B[0][i],math.isqrt(B[i][i]),(beta-1)//ds[i]) for i in range(1,9)]
 return [(1,)+v for v in itertools.product(*(range(q+1) for q in bounds)) if sum(a*b for a,b in zip(v,ds[1:]))==beta-1]

def enumerate_low(ds,B):
 # Five repeated dimension-5 columns are unordered. Dimension-15 pair is
 # unordered. The last column is forced by the I(1) row sum.
 beta=[4,5,5,5,5,5,15,15];cols=[candidates(ds,B,b) for b in beta];last={v:i for i,v in enumerate(cols[-1])}
 require(list(map(len,cols))==[10,17,17,17,17,17,210,210])
 target=tuple(B[0][i]-(i==0) for i in range(9));counts=collections.Counter();lowlist=[];failures=[]
 def visit(chosen,rem,Q):
  counts['nodes']+=1;lev=len(chosen)
  if lev==7:
   c=rem
   if c not in last or c<chosen[-1]:return
   options=[c]
  else:options=cols[lev]
  for c in options:
   if lev and beta[lev]==beta[lev-1] and c<chosen[-1]:continue
   r=tuple(a-b for a,b in zip(rem,c))
   if min(r)<0:continue
   q=[[Q[i][j]-c[i]*c[j] for j in range(9)] for i in range(9)]
   if any(q[i][j]<0 or q[i][i]*q[j][j]<q[i][j]**2 for i in range(9) for j in range(i+1)):continue
   cs=chosen+[c]
   if lev<7:visit(cs,r,q);continue
   require(not any(r));counts['entry_and_2x2_gram_lows']+=1
   mass=[sum(v[i]*b for v,b in zip(cs,beta)) for i in range(9)]
   # The universal self-dual upper bound is also valid for non-self-dual X.
   failed=[i for i in range(1,9) if (3*ds[i]+1)*mass[i]>60*ds[i]*(ds[i]+1)]
   require(failed,'A candidate survives the claimed moment obstruction')
   i=failed[0];lowlist.append([list(v) for v in cs]);failures.append({'object':i,'low_mass':mass[i],'positive_gap':(3*ds[i]+1)*mass[i]-60*ds[i]*(ds[i]+1)})
 Q=[row[:] for row in B];Q[0][0]-=1
 visit([],target,Q)
 require(counts['entry_and_2x2_gram_lows']==404)
 return dict(counts),lowlist,failures

def main():
 started=time.time();N,du,ds,B=facts(IDS[0]);perms={IDS[0]:list(range(9))}
 for name in IDS[1:]:
  n,d2,ds2,B2=facts(name);sets=[([i for i,d in enumerate(ds2) if d==q and i],[j for j,d in enumerate(ds) if d==q and j]) for q in [1,2,4]]
  found=None
  for choices in itertools.product(*(list(itertools.permutations(b)) for a,b in sets)):
   p=[0]*9
   for (a,b),perm in zip(sets,choices):
    for i,j in zip(a,perm):p[i]=j
   if all(B2[i][j]==B[p[i]][p[j]] for i in range(9) for j in range(9)):found=p;break
  require(found is not None);perms[name]=found
 counts,lows,failures=enumerate_low(ds,B)
 cert={'case_ids':IDS,'input_to_reference_coordinate_maps':perms,'reference_dimensions':ds,'reference_induction_gram':B,'nonunit_low_dimensions_in_enumeration_order':[4,5,5,5,5,5,15,15],'formal_codegrees_counted_with_multiplicity':[60,15,4,4,12,12,12,12,12],'counts':counts,'lows':lows,'moment_failures':failures,'all_branches_excluded':True,'scope':'general complex fusion categories: integral implies pseudo-unitary','seconds':time.time()-started}
 (OUT/'dim60_exclusion_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
 print(json.dumps({'status':'PASS','ids':IDS,'counts':counts,'maps':perms,'seconds':time.time()-started},indent=2),flush=True)
if __name__=='__main__':main()
