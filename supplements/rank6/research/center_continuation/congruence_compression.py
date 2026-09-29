import itertools,json
import sympy as s

def mod_group(q):
 def norm(a):return min(a,tuple((-z)%q for z in a))
 def mul(a,b):return norm(((a[0]*b[0]+a[1]*b[2])%q,(a[0]*b[1]+a[1]*b[3])%q,(a[2]*b[0]+a[3]*b[2])%q,(a[2]*b[1]+a[3]*b[3])%q))
 G=sorted({norm((a,b,c,d)) for a,b,c,d in itertools.product(range(q),repeat=4) if (a*d-b*c)%q==1})
 I=norm((1,0,0,1));T=norm((1,1,0,1));S=norm((0,-1%q,1,0));H=[I]
 while mul(H[-1],T)!=I:H.append(mul(H[-1],T))
 # left cosets H g, invariant functions under left H; left S action projected.
 seen=set();cosets=[];lookup={}
 for g in G:
  if g in seen:continue
  C={mul(h,g) for h in H};idx=len(cosets);cosets.append(sorted(C));seen|=C
  for x in C:lookup[x]=idx
 M=s.zeros(len(cosets))
 for j,C in enumerate(cosets):
  for x in C:M[lookup[mul(S,x)],j]+=s.Rational(1,len(H))
 assert M==M.T
 return G,H,M
if __name__=='__main__':
 for q in [4,8]:
  G,H,M=mod_group(q);print(q,len(G),len(H),M.shape,M.charpoly().as_expr().factor(),M.eigenvals())
