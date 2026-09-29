"""Exact necessary rank-six modules for the actual GI cyclic-eight quotient.

Assumes the hypothetical canonical central algebra has the six twist-one
summands recorded by cyclic8_center_tensor.json. This is conditional Morita
class analysis, not a general exclusion of R6_3_215.
"""
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def require(condition):
    if not condition:raise RuntimeError("Exact cyclic8 module check failed")

def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def plus(*As):return [[sum(a) for a in zip(*rows)] for rows in zip(*As)]
def scale(c,A):return [[c*a for a in row] for row in A]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def trace(A):return sum(A[i][i] for i in range(len(A)))
def pm(p):return [[int(j==p[i]) for j in range(len(p))] for i in range(len(p))]
def transpose(A):return list(map(list,zip(*A)))
I=ident(6);A=pm([1,2,3,0,5,4]);Ap=[I,A]
Ap += [mm(Ap[-1],A)];Ap += [mm(Ap[-1],A)]
source=json.load(open(ROOT/'research/center_continuation/cyclic8_canonical_restriction.json'))
center=json.load(open(ROOT/'research/center_continuation/cyclic8_center_tensor.json'))
require(source['inner_product']==6)
require(source['cross_gram'][1][0]==0 and source['cross_gram'][2][0]==2)
require(all(source['cross_gram'][i][0]==8 for i in range(4,8)))
require(source['cross_gram'][0][1]==2)
# All permutations of simples preserving dimensions and twists preserve the
# proposed unit-induction vector and its g-coefficient. Dimension is encoded
# in Q(d), d^2=8d+1, by the known R215 basis dimensions.
dims=[(1,0),(1,0),(0,1),(0,1),(-1,1),(1,1)]
groups={}
for z,(F,t) in enumerate(zip(center['F'],center['twists_as_136th_root_exponents'])):
    dim=tuple(sum(F[i]*dims[i][k] for i in range(6)) for k in range(2))
    groups.setdefault((dim,t),[]).append(z)
for zs in groups.values():
    require(len({source['induction_unit_R'][z] for z in zs})==1)
    require(len({center['F'][z][1] for z in zs})==1)
# alpha is a permutation of order dividing4. Trace0 and trace(alpha^2)=2
# force one4cycle and one2cycle. A simultaneous relabeling fixes A above.
cycle_types=[]
for n1 in range(7):
 for n2 in range(4):
  for n4 in range(2):
   if n1+2*n2+4*n4==6 and n1==0 and n1+2*n2==2:
    cycle_types.append([n1,n2,n4])
require(cycle_types==[[0,1,1]])
# All symmetric B with BA=A^{-1}B have the following8-parameter form.
# Trace(B)=Tr(AB)=8 fixes u,v. Tr(B^2)=70 bounds r_i<=4,e,f<=2.
solutions=[];tested=0
for r in itertools.product(range(5),repeat=4):
 u=4-r[0]-r[2];v=4-r[1]-r[3]
 if u<0 or v<0:continue
 for e,f in itertools.product(range(3),repeat=2):
  tested+=1
  B=[[0]*6 for _ in range(6)]
  for i in range(4):
   for j in range(4):B[i][j]=r[(i+j)%4]
   B[i][4]=B[4][i]=e if i%2==0 else f
   B[i][5]=B[5][i]=f if i%2==0 else e
  B[4][4]=B[5][5]=u;B[4][5]=B[5][4]=v
  require(B==transpose(B) and mm(B,A)==mm(Ap[3],B))
  require(trace(B)==trace(mm(A,B))==8)
  if trace(mm(B,B))!=70:continue
  if mm(B,B)!=plus(I,scale(2,mm(plus(*Ap),B))):continue
  s=sum(r)
  require(e==f==1 and s in (1,7))
  # Normalized module dimensions squared: four x, two y.
  # These exact pairs mean a+b*d. Verify d*m0=s*m0+2*m4,
  # normalization4*x+2*y=8+32*d, and y/x=(d-s)^2/4.
  x,y=((1,1),(2,14)) if s==1 else ((1,7),(2,2))
  def mul(p,q):
   a,b=p;c,d=q
   return (a*c+b*d,a*d+b*c+8*b*d)
  require((4*x[0]+2*y[0],4*x[1]+2*y[1])==(8,32))
  require(mul(x,mul((-s,1),(-s,1)))==(4*y[0],4*y[1]))
  solutions.append({'r':list(r),'e':e,'f':f,'u':u,'v':v,'s':s,
                    'rho_action':B,'four_cycle_squared_dimension':list(x),
                    'two_cycle_squared_dimension':list(y)})
# Right g: permutation, involution, trace2, commuting with left alpha.
# This uniquely fixes the action as alpha^2, hence it fixes both2cycle objects.
g_candidates=[]
for p in itertools.permutations(range(6)):
 G=pm(p)
 if trace(G)==2 and mm(G,G)==I and mm(G,A)==mm(A,G):g_candidates.append(list(p))
require(g_candidates==[[2,3,0,1,4,5]])
require(all(mm(pm(g_candidates[0]),t['rho_action'])==mm(t['rho_action'],pm(g_candidates[0])) for t in solutions))
counts={str(s):sum(t['s']==s for t in solutions) for s in (1,7)}
require(counts=={'1':4,'7':4})
# g-fixed objects in s7 have squared dimension2+2d. Splitting over1+g
# divides squared dimensions by2, giving1+d in the new Morita module.
for t in solutions:
 if t['s']==7:require(t['two_cycle_squared_dimension']==[2,2])
output={'status':'conditional necessary module enumeration; no general categorification conclusion',
 'input_scope':'GI cyclic-eight quotient center with proposed six-summand canonical algebra',
 'center_relabeling_invariance_verified':True,'alpha_cycle_type':cycle_types[0],
 'finite_parameter_assignments_tested':tested,'solutions_by_upper_row_sum':counts,
 'right_g_permutation':g_candidates[0],'solutions':solutions,
 's7_condensation_fixed_simple_squared_dimensions':[1,1],
 's1_simple_internal_end':'1+alpha^h rho',
 's7_after_involution_condensation_simple_internal_end':'1+alpha^h rho'}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({k:v for k,v in output.items() if k!='solutions'}))
