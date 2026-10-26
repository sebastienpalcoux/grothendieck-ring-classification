from pathlib import Path
import itertools,json,math
import ring_checks as common
HERE=Path(__file__).resolve().parent

def group(orders):
 E=list(itertools.product(*(range(n)for n in orders)));idx={x:i for i,x in enumerate(E)};G=[[idx[tuple((a+b)%n for a,b,n in zip(x,y,orders))]for y in E]for x in E];return E,G

def forms(orders,E):
 q=math.lcm(*orders);positions=list(itertools.product(range(len(orders)),repeat=2));ranges=[range(math.gcd(orders[i],orders[j]))for i,j in positions]
 for vals in itertools.product(*ranges):
  coeff={pos:v*(q//math.gcd(orders[pos[0]],orders[pos[1]]))for pos,v in zip(positions,vals)}
  B=[[sum(x[i]*y[j]*coeff[i,j]for i,j in positions)%q for y in E]for x in E]
  if len(set(map(tuple,B)))==len(E):yield B

def auts(orders,E):
 for images in itertools.product(E,repeat=len(orders)):
  if any(any((orders[i]*v)%n for v,n in zip(images[i],orders))for i in range(len(orders))):continue
  p=[E.index(tuple(sum(x[i]*images[i][j]for i in range(len(orders)))%n for j,n in enumerate(orders)))for x in E]
  if len(set(p))==len(E):yield p

def main():
 out=[]
 # H4: every compatible pair has a central common isotropic involution.
 for orders in [(4,),(2,2)]:
  E,G=group(orders);q=math.lcm(*orders);Bs=list(forms(orders,E));Ps=[p for p in auts(orders,E)if all(p[p[i]]==i for i in range(len(E)))];count=0
  for B,P,dual_swap in itertools.product(Bs,Ps,[False,True]):
   B1=[[B[P[i]][j]for j in range(len(E))]for i in range(len(E))]
   if dual_swap:
    if B1!=list(map(list,zip(*B))):continue
   elif B!=list(map(list,zip(*B)))or B1!=list(map(list,zip(*B1))):continue
   hs=[i for i in range(1,len(E))if G[i][i]==0 and P[i]==i and B[i][i]==B1[i][i]==0]
   common.require(hs,'H4 common central isotropic involution');count+=1
  out.append(dict(lemma='H4 common isotropic involution',orders=orders,nondegenerate_bicharacters=len(Bs),involutions=len(Ps),compatible_cases=count))
 # H8: cosquare-involution is trivial; no moved order2 vector has both odd diagonal signs negative.
 for orders in [(8,),(4,2),(2,2,2)]:
  E,G=group(orders);q=math.lcm(*orders);Bs=list(forms(orders,E));Ps=[p for p in auts(orders,E)if all(p[p[i]]==i for i in range(len(E)))];cosq=0;orth=0;moved=0
  for B,P in itertools.product(Bs,Ps):
   BP=[[B[P[i]][j]for j in range(8)]for i in range(8)]
   if BP==list(map(list,zip(*B))):
    common.require(P==list(range(8)),'H8 no nontrivial involutive cosquare');cosq+=1
   if B!=list(map(list,zip(*B)))or any(B[P[i]][P[j]]!=B[i][j]for i,j in itertools.product(range(8),repeat=2)):continue
   orth+=1
   for c in range(1,8):
    if G[c][c]or P[c]==c:continue
    common.require(not(B[c][c]==q//2 and BP[c][c]==q//2),'H8 fixed-odd inverse-algebra obstruction');moved+=1
  out.append(dict(lemma='H8 cosquare and fixed-odd branch',orders=orders,nondegenerate_bicharacters=len(Bs),involutions=len(Ps),compatible_cosquares=cosq,orthogonal_pairs=orth,moved_involutions=moved))
 (HERE/'finite_bicharacter_lemmas.json').write_text(json.dumps(dict(status='pass',records=out),indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
