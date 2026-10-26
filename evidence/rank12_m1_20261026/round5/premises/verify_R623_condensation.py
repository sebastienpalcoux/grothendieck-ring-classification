"""Independent exact checks of the cyclic-near-group condensation data.
This is not an existence verifier for the analytic TPE precursor. Existence is
Theorems2.10/5.4 and Corollary6.6 of He et al.; the mixed reconstruction bridge
is proved separately. No numerical algebra or optimization is used.
"""
import json
from pathlib import Path
from fractions import Fraction
OUT=Path(__file__).resolve().parent

def require(v,msg):
    if not v: raise RuntimeError(msg)

n=36
# All phases are powers of zeta_72. TPE chi=exp(2*pi*i*g*h/36),
# a(g)=exp(pi*i*g*(36-g)/36).
def chi(g,h): return (2*g*h) %72
def a(g): return (g*(36-g)) %72
H=list(range(0,36,6))
count=0
for g in range(n):
    require(a(-g%n)==a(g),'a even')
    require((2*a(g)+chi(g,g))%72==0,'quadratic diagonal')
    for h in range(n):
        require((a(g)+a(h)-a((g+h)%n)-chi(g,h))%72==0,'quadratic refinement')
        require(chi(g,h)==chi(h,g),'symmetry')
        # pi_x shift g; pi_y shift -g with phase a(h)-a(h-g);
        # pi_z diagonal chi(g,h). Product pi_x*pi_y*pi_z scalar a(g)^-1.
        require((chi(g,h)+a(h)-a((h-g)%n)+a(g))%72==0,'three insertion scalar')
        for k in range(n):
            require((chi(g,(h+k)%n)-chi(g,h)-chi(g,k))%72==0,'bicharacter')
            count+=1
require([g for g in range(n) if all(chi(g,h)==0 for h in H)]==H,'H Lagrangian')
require(all(chi(h,k)==0 for h in H for k in H),'H isotropic')
require([a(h) for h in H]==[0,36,0,36,0,36],'restriction a')
# Izumi dictionary inverts chi and a. a|H is its own inverse.
ga=[g for g in range(n) if all((-chi(h,g)-a(h))%72==0 for h in H)]
require(ga==[3,9,15,21,27,33],'pointed square coset')

N=[[[0]*12 for _ in range(12)] for _ in range(12)]
for i in range(12):
 for j in range(12):
  x,y=i%6,j%6
  if i<6 and j<6: N[i][j][(x+y)%6]=1
  elif i<6: N[i][j][6+(x+y)%6]=1
  elif j<6: N[i][j][6+(x-y)%6]=1
  else:
   N[i][j][(x-y+3)%6]=1
   for k in range(6,12):N[i][j][k]=1

T=json.loads((OUT/'R623_tensor.json').read_text())
G=[i for i in range(12) if all(sum(T[i][j])==1 for j in range(12))]
def mul(i,j):
 s=[k for k,v in enumerate(T[i][j]) if v]
 require(len(s)==1 and T[i][j][s[0]]==1,'single product')
 return s[0]
units=[i for i in range(12) if all(T[i][j][j]==1 and sum(T[i][j])==1 for j in range(12))]
require(len(units)==1,'unit')
u=units[0]
maps=[]
for g in G:
 powers=[u]
 for _ in range(1,6):powers.append(mul(g,powers[-1]))
 if len(set(powers))!=6 or mul(g,powers[-1])!=u:continue
 for r in range(12):
  if r in G:continue
  p=powers+[mul(x,r) for x in powers]
  if len(set(p))!=12:continue
  if all(N[i][j][k]==T[p[i]][p[j]][p[k]] for i in range(12) for j in range(12) for k in range(12)):maps.append(p)
require(maps,'full tensor isomorphism')
# Associativity, rigidity, and duality independent of source tensor.
for i in range(12):
 for j in range(12):
  for k in range(12):
   for l in range(12):
    require(sum(N[i][j][m]*N[m][k][l] for m in range(12))==sum(N[j][k][m]*N[i][m][l] for m in range(12)),'associativity')
star=[(-i)%6 if i<6 else 6+((i-6+3)%6) for i in range(12)]
for i in range(12):
 require(N[i][star[i]][0]==1,'duality')
 for j in range(12):
  for k in range(12):require(N[i][j][k]==N[star[j]][star[i]][star[k]],'star anti-involution')
result={'status':'PASS','source':'He-Liu-Lu-Palcoux-Ren arXiv:2610.11652v1, TPE precursor C36+36',
 'H':H,'H_perp':H,'a_on_H_exponents_mod72':[a(h) for h in H],
 'ga_coset':ga,'quotient_group':'C6','mixed_action':'inversion','square_pointed_term':3,
 'bicharacter_identity_checks':count,'basis_map':maps[0],'all_basis_maps':maps,'tensor_entries_checked':1728,
 'new_claim':'Ring binding and finite mixed scalar identities only; categorical model needs separate written bridge.',
 'unitarity_claimed':False}
(OUT/'R623_condensation_independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
