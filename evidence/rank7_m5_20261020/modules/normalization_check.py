"""Exact normalization and first-row/column multiplicity checks for R4982."""
if not __debug__:
 raise RuntimeError("This exact certificate requires Python assertions; disable optimization.")
import sys,json,itertools,numpy as np,sympy as s
from pathlib import Path
B=Path(__file__).parent;P=B.parents[2]
sys.path.insert(0,str(P/'supplements/rank6/software'))
from r4982_module import all_modules
from full_morita_gram import full_gram
M=all_modules()[0];G=full_gram(M);V=s.Matrix.hstack(*G.columnspace())
assert G.extract(range(0,169,13),range(0,169,13))==3*s.eye(13)
assert M[3][:4,:4]==s.ones(4)-s.eye(4) and M[3][4:,4:]==3*s.eye(9)
checks=[]
for a,b in itertools.product([4,7,10],repeat=2):
 inds=list(range(0,169,13))+list(range(1,13))+[i*13+j for i in range(1,4) for j in range(1,4)]
 vals=[int(i==a) for i in range(13)]+[int(i==b) for i in range(1,13)]+[0]*9
 A=V.extract(inds,range(V.cols));rhs=s.Matrix(vals)
 ra=A.rank();rab=A.row_join(rhs).rank();assert (ra==rab)==(a==b)
 checks.append({'column_anchor':a,'row_anchor':b,'rank':ra,'augmented_rank':rab})
rep=json.load(open(B/'r4982_fullgram_actions.json'));ps=[np.array(z).reshape(13,13) for z in rep['invertible_actions']];stab=[Q for Q in ps if Q[0,0]]
assert len(ps)==72 and len(stab)==18
orbits={str(a):sorted({int(np.argmax(Q[:,a])) for Q in stab}) for a in [4,7,10]}
assert list(orbits.values())==[list(range(a,a+3)) for a in [4,7,10]]
Bs=[np.array(z).reshape(13,13) for z in rep['noninvertible_actions']];counts={}
for X in Bs:
 assert sum(X[:,0])==sum(X[0,:])==1
 a=int(np.argmax(X[:,0]));b=int(np.argmax(X[0,:]));counts[a,b]=counts.get((a,b),0)+1
for a,b in itertools.product(range(4,13),repeat=2):
 expected=int((a-4)//3==(b-4)//3)
 assert int(G[13*a,b])==counts.get((a,b),0)==expected
params=json.load(open(B/'rightaction_parameters.json'))
assert all(all(z['bounds'][i]<z['den'] for i in z['solved']) for z in params)
out={'cross_anchor_affine_checks':checks,'stabilizer_order':len(stab),'stabilizer_big_orbits':orbits,'possible_noninvertible_action_count':len(Bs),'cross_gram_multiplicities':[[int(G[13*a,b]) for b in range(4,13)] for a in range(4,13)],'solved_variable_bounds_below_denominator':True}
(B/'r4982_normalization_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
