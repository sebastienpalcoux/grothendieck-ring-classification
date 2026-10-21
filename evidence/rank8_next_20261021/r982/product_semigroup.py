"""Exact selected-pattern high-remainder product decompositions.

Only integer vectors which pass every source coefficient are retained.
This is not a fusion associator or a complete center fusion table.
"""
from pathlib import Path
import json,itertools
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
P=json.loads((ROOT/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json').read_text())['records'][2];S=json.loads((HERE/'frame2_system.json').read_text());W=json.loads((HERE/'joint_integer_result.json').read_text())['integer_core_values'];original=S['source_lower'][:]
for j,v in zip(S['metadata']['source_metadata']['retained_indices'],W):original[j]+=v
vectors={r['index']:(0,)+tuple(r['vector'])for r in P['high_vectors']};types=[vectors[i]for j,o in enumerate(P['duality_orbits'])if original[j] for i in o['indices']]
T=json.loads((ROOT/'evidence/rank8_frontier_20261021/global_induction/complete_results/R8_3_982_sts_frame_h4.json').read_text())['metadata']['character_table'];charge=[int(ch[6][0])for ch in T['characters']];perm=(6,2,1,4,3,7,0,5);low=dict(zip(P['character_labels'],map(tuple,P['low_columns'])));translated={tuple(v[i]for i in perm):-charge[E]for E,v in low.items()};g=(0,0,0,0,0,0,1,0)
products=json.loads((HERE/'forgetful_product_probe.json').read_text())['pairs'];results=[]
for case in products:
 E,F=case['pair'];target=case['residual_high_restriction'];bounds=[]
 for v in types:
  ub=min(target[i]//a for i,a in enumerate(v)if a)
  if v==g or (v in translated and translated[v]!=charge[E]*charge[F]):ub=0
  bounds.append(ub)
 A=np.array(types,dtype=float).T;ans=milp(np.zeros(len(types)),integrality=np.ones(len(types)),bounds=Bounds(np.zeros(len(types)),bounds),constraints=LinearConstraint(A,target,target),options={'time_limit':15})
 rec={'pair':[E,F],'status':'no_exact_conclusion','numerical_status':int(ans.status)}
 if ans.x is not None:
  vals=[int(round(x))for x in ans.x]
  if all(0<=x<=u for x,u in zip(vals,bounds)) and [sum(x*v[i]for x,v in zip(vals,types))for i in range(8)]==target:rec.update(status='exact_nonnegative_integer_high_remainder',coefficients=vals)
 results.append(rec)
out={'scope':'individual_low_pair_remainders_on_selected_joint_witness_only','high_restriction_types':types,'known_translated_low_charge_constraints':True,'central_g_forbidden_in_low_low_product':True,'pairs':results,'all28_exact':all(r['status']=='exact_nonnegative_integer_high_remainder'for r in results)}
(HERE/'product_semigroup.json').write_text(json.dumps(out,separators=(',',':'))+'\n');print('all28 exact charged-compatible high-remainder decompositions',out['all28_exact'],'types',len(types),'failures',[r['pair']for r in results if r['status']!='exact_nonnegative_integer_high_remainder'])
