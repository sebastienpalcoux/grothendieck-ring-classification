#!/usr/bin/env python3
"""Independent pair-closure subgroup enumeration for the three neutral groups."""
import itertools,json

def require(x,msg):
 if not x:raise ValueError(msg)
def lattice(G,mul,unit,expected,orders):
 def close(H):
  H=set(H)
  while True:
   K=H|{mul(a,b)for a in H for b in H}
   if K==H:return frozenset(H)
   H=K
 seen={frozenset([unit])};todo=list(seen)
 while todo:
  H=todo.pop()
  for x in G:
   if x in H:continue
   K=close(H|{x})
   if K not in seen:seen.add(K);todo.append(K)
 inv={x:next(y for y in G if mul(x,y)==mul(y,x)==unit)for x in G}
 ab=[]
 for H in seen:
  require(close(H)==H,'not a subgroup')
  if all(mul(x,y)==mul(y,x)for x in H for y in H) and all(mul(mul(g,x),inv[g])in H for g in G for x in H):ab.append(len(H))
 require(len(seen)==expected and sorted(ab)==orders,'group kernel classification')
 return dict(group_order=len(G),subgroups=len(seen),normal_abelian_orders=sorted(ab))
def main():
 G=list(itertools.product(range(3),range(3),range(4)))
 def m36(x,y):
  a,b=y[:2]
  for _ in range(x[2]):a,b=(-b)%3,a
  return ((x[0]+a)%3,(x[1]+b)%3,(x[2]+y[2])%4)
 a=lattice(G,m36,(0,0,0),38,[1,9])
 G=list(itertools.product(range(2),range(2),range(3)))
 def m12(x,y):
  a,b=y[:2]
  for _ in range(x[2]):a,b=b,(a+b)%2
  return ((x[0]+a)%2,(x[1]+b)%2,(x[2]+y[2])%3)
 b=lattice(G,m12,(0,0,0),10,[1,4])
 G=list(itertools.permutations(range(4)))
 c=lattice(G,lambda x,y:tuple(x[y[i]]for i in range(4)),tuple(range(4)),30,[1,4])
 print(json.dumps(dict(status='PASS',scope='independent_finite_group_premises',groups=[a,b,c]),indent=2))
if __name__=='__main__':main()
