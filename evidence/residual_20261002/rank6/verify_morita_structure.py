"""Small exact checks for newly derived Morita structural corollaries."""
from pathlib import Path
import json,hashlib,argparse
from fractions import Fraction
P=Path(__file__).parent
R=next((q/'supplements/rank6' for q in P.parents if (q/'supplements/rank6/data/census.json').is_file()),None)
if R is None:raise FileNotFoundError('Place this verifier inside the classification repository')
source=R/'research/frontier/new_research/r1660_categorical/dual_actions_receipt.json'
def require(ok,message):
 if not ok:raise RuntimeError(message)
data=json.loads(source.read_text());rows=[]
for branch in data:
 for index,sol in enumerate(branch['solutions']):
  N=sol['fusion_tensor'];n=len(N);dual=sol['dual']
  require(all(N[i][dual[i]][0]==1 for i in range(n)), 'duality convention')
  S={0}
  for i in range(n):S.update(k for k in range(n) if N[i][dual[i]][k])
  changed=True
  while changed:
   old=set(S)
   S.update(dual[i] for i in tuple(S))
   for i in old:
    for j in old:S.update(k for k in range(n) if N[i][j][k])
   changed=S!=old
  require(len(S)==n, 'proper adjoint subring')
  comm=all(N[i][j]==N[j][i] for i in range(n) for j in range(n))
  row=dict(type=branch['type'],index=index,rank=n,commutative=comm,adjoint_labels=sorted(S))
  if n==8:require(not comm, 'commutative rank-eight candidate')
  rows.append(row)
# Integer arithmetic norms: positive dimensions D155=72+48 sqrt2;
# D1660 has monic minimal polynomial with constant147456.
n155=72**2-2*48**2
# Norm over Q(sqrt3) after pairing sqrt2 sign.
# D1660=(144+80sqrt3)+(96+56sqrt3)sqrt2.
a=144**2+3*80**2-2*(96**2+3*56**2)
b=2*144*80-4*96*56
n1660=a*a-3*b*b
require(n155==2**6*3**2 and n1660==2**14*3**2, 'dimension norms')
# Norm of would-be de-equivariantized S: (1+sqrt3)/2.
require(Fraction(1-3,4)==-Fraction(1,2), 'half-dimension norm')
out=dict(status='exact_arithmetic_and_adjoint_support_checks_only',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),dimension_norms={'R6_4_155':n155,'R6_8_1660':n1660},e6_half_dimension_norm='-1/2',all_dual_solutions_adjoint=rows)
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
receipt=P/'morita_structure_receipt.json'
if args.write:receipt.write_text(json.dumps(out,indent=2)+'\n')
else:require(out==json.loads(receipt.read_text()),'structural receipt or source binding mismatch')
print(json.dumps(dict(passed=True,dimension_norms=out['dimension_norms'],dual_rings_checked=len(rows),all_adjoint_full=True,category_status='both_unresolved')))
