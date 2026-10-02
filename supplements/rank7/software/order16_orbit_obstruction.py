"""Exact finite corroboration of the pure theoretical order16 orbit obstruction.
Standard library only; the categorical reduction is proved separately.
"""
import itertools,json
from pathlib import Path

def mm(a,b,m):
 n=len(a);return tuple(tuple(sum(a[i][k]*b[k][j]for k in range(n))%m for j in range(n))for i in range(n))
def mv(a,v,m):return tuple(sum(x*y for x,y in zip(row,v))%m for row in a)
def orbit_type(R,S,m):
 A=set(itertools.product(range(m),repeat=len(R)));ans=[]
 while A:
  O={min(A)};Q=list(O)
  for v in Q:
   for T in(R,S):
    w=mv(T,v,m)
    if w not in O:O.add(w);Q.append(w)
  A-=O;ans.append(len(O))
 return sorted(ans)

def c4():
 m=4;I=((1,0),(0,1));zero=(0,0)
 G=[((a,b),(c,d))for a,b,c,d in itertools.product(range(4),repeat=4)if(a*d-b*c)%2]
 Rlist=[R for R in G if mm(mm(R,R,4),R,4)==I and R!=I and
        [v for v in itertools.product(range(4),repeat=2)if mv(R,v,4)==v]==[zero]]
 records=[]
 for R in Rlist:
  R2=mm(R,R,4)
  for S in G:
   if S==I or mm(S,S,4)!=I or mm(mm(S,R,4),S,4)!=R2:continue
   fixed=sum(mv(S,v,4)==v for v in itertools.product(range(4),repeat=2))
   records.append((fixed,orbit_type(R,S,4)))
 return dict(group='C4xC4',GL_order=len(G),fixed_point_free_C3_matrices=len(Rlist),
             S3_action_pairs=len(records),fixed_counts=sorted(set(x[0]for x in records)),
             orbit_types=[list(x)for x in sorted(set(tuple(x[1])for x in records))])

def c2four():
 I=tuple(tuple(int(i==j)for j in range(4))for i in range(4))
 R=((0,1,0,0),(1,1,0,0),(0,0,0,1),(0,0,1,1));R2=mm(R,R,2)
 # All fixed-point-freeC3actions are the sumoftwo irreducibleF2[C3]modules.
 records=[]
 for bits in itertools.product(range(2),repeat=16):
  S=tuple(tuple(bits[4*i+j]for j in range(4))for i in range(4))
  if mm(S,S,2)!=I or mm(mm(S,R,2),S,2)!=R2:continue
  fixed=sum(mv(S,v,2)==v for v in itertools.product(range(2),repeat=4))
  records.append((fixed,orbit_type(R,S,2)))
 return dict(group='C2^4',chosen_C3_matrix=R,S3_reflection_lifts=len(records),
             fixed_counts=sorted(set(x[0]for x in records)),
             orbit_types=[list(x)for x in sorted(set(tuple(x[1])for x in records))])

def require(condition, message):
 if not condition:raise ValueError(message)

def verify_orbit_obstruction():
 a=c4();b=c2four()
 require(a['GL_order']==96, 'GL2(Z4) completeness')
 require(a['fixed_point_free_C3_matrices']==8, 'C4^2 order-three actions')
 require(a['S3_action_pairs']==48, 'C4^2 reversing involutions')
 require(b['S3_reflection_lifts']==30, 'C2^4 reversing involutions')
 require(a['fixed_counts']==b['fixed_counts']==[4], 'reflection fixed points')
 require(a['orbit_types']==b['orbit_types']==[[1,3,3,3,6]], 'actual orbit types')
 require([1,3,6,6] not in a['orbit_types']+b['orbit_types'], 'required orbit type absent')
 # Stronger check: every involution on C4^2 fixes at least four points.
 I=((1,0),(0,1));counts={}
 for aa,bb,cc,dd in itertools.product(range(4),repeat=4):
  if (aa*dd-bb*cc)%2==0:continue
  S=((aa,bb),(cc,dd))
  if mm(S,S,4)!=I:continue
  fixed=sum(mv(S,v,4)==v for v in itertools.product(range(4),repeat=2))
  require(fixed>=4, 'C4^2 involution has too few fixed points')
  counts[fixed]=counts.get(fixed,0)+1
 require(counts=={4:18,8:9,16:1}, 'all involutions on C4^2')
 return dict(status='PASS',scope='finite corroboration of the accompanying general exclusion proof',
             required_orbit_type=[1,3,6,6],required_reflection_fixed_points=2,
             C4xC4=a,C2four=b,all_C4xC4_involution_fixed_point_counts=counts)

if __name__=='__main__':
 print(json.dumps(verify_orbit_obstruction(),indent=2))
