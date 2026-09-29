"""Exact inputs for excluding R6_3_215 from the actual cyclic-eight Morita class.

No hypothetical restriction F is assumed. The canonical-induction support
is forced by formal codegrees and the six twist-one simples of the actual
Grossman--Izumi center. This is not uniqueness of that modular category.
"""
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / 'research/center_continuation'
z = json.loads((P/'cyclic8_center_tensor.json').read_text())
can = json.loads((P/'cyclic8_canonical_restriction.json').read_text())

def need(condition, message):
    if not condition:
        raise ArithmeticError(message)

def add(x,y): return (x[0]+y[0],x[1]+y[1])
def mul(x,y):
    a,b=x;c,e=y
    return (a*c+b*e,a*e+b*c+8*b*e)

# d=4+sqrt17, Delta=8+32d. Formal codegrees are
# Delta, its conjugate, 4,4,8,8. These can also be read directly from
# the exact original-character certificate of the first continuation.
delta=(8,32); conjugate_delta=(264,-32)
dimensions=[(1,0),(1,8),(2,8),(2,8),(1,4),(1,4)]
codegrees=[delta,conjugate_delta,(4,0),(4,0),(8,0),(8,0)]
need(all(mul(x,f)==delta for x,f in zip(dimensions,codegrees)),
     'canonical dimensions do not match the formal codegrees')

# Use the actual source restriction, not the proposed target restriction,
# to compute every center-simple dimension.
source_dimensions=[(1,0)]*4+[(0,1)]*4
center_dimensions=[tuple(sum(row[i]*source_dimensions[i][j] for i in range(8))
                         for j in range(2)) for row in can['F_D']]
twists=z['twists_as_136th_root_exponents']
twist_one=[i for i,t in enumerate(twists) if t%136==0]
need(len(twist_one)==6,'wrong number of twist-one simples')
need(Counter(center_dimensions[i] for i in twist_one)==Counter(dimensions),
     'twist-one simple dimensions do not force the proposed support')
a=[int(i in twist_one) for i in range(22)]
need(a==can['induction_unit_R'],'old candidate differs from forced vector')
rank=sum(x*y for x,y in zip(a,can['induction_unit_D']))
need(rank==6,'wrong Morita-module rank')
traces=[sum(a[z]*can['F_D'][z][i] for z in range(22)) for i in range(8)]
need(traces==[6,0,2,0,8,8,8,8],'wrong left-action traces')

# The forced algebra 1+g has a dual with based ring R215 (separate exact
# full-Morita certificate). Thus it has the same forced central support,
# and the condensed module again has rank 6. A C2 permutation action
# with f fixed objects has (6-f)/2 free-orbit modules and 2f fixed modules.
possible_fixed=[f for f in range(7) if (6-f)%2==0 and (6-f)//2+2*f==6]
need(possible_fixed==[2],'right g fixed-point count is not forced')

out={'scope':'actual Grossman--Izumi cyclic-eight quotient Morita class',
     'hypothetical_target_restriction_assumed':False,
     'twist_one_indices':twist_one,
     'forced_induction_unit':a,
     'forced_dimensions_in_basis_1_d':dimensions,
     'module_rank':rank,'left_action_traces':traces,
     'condensed_module_rank':6,'right_g_fixed_points':2,
     'conclusion':'These are precisely the hypotheses of the existing complete module and second-algebra obstruction; no R215 category is weakly Morita equivalent to this actual source category.',
     'not_proved':['uniqueness of a modular category from S and T',
                   'general noncategorifiability of R6_3_215']}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
