"""Exact independent check of the published +TY relaxation witness.

No optimizer; arithmetic in Q(d), d^2=8d+2. This rejects one witness,
not the fusion ring or the necessary-system feasible region.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'r137'/'prior'/'forced_export.json'
x=json.loads(P.read_text())
def add(z,w):return (z[0]+w[0],z[1]+w[1])
def mul(z,w):return (z[0]*w[0]+2*z[1]*w[1],z[0]*w[1]+z[1]*w[0]+8*z[1]*w[1])
def inv(z):
    q=z[0]*z[0]+8*z[0]*z[1]-2*z[1]*z[1]
    assert q
    return ((z[0]+8*z[1])/q,-z[1]/q)
def scale(a,z):return (a*z[0],a*z[1])
ZERO=(F(0),F(0));D=(F(16),F(32));D2=mul(D,D)
w={int(j):F(c) for j,c in x['witness']}
assert len(w)==len(x['witness'])==102
assert all(c>=0 for c in w.values())
assert not set(w).intersection(x['removed_columns'])
for row,rhs in zip(x['A'],x['b']):
    assert sum(F(row[j])*c for j,c in w.items())==F(rhs)
mapping={int(j):v for j,v,*_ in x['physical_mapping']}
gram_pairs=[(i,j) for i in range(9) for j in range(i,9)]
for j,v in mapping.items():
    assert all(x['A'][k][j]==v[i]*v[l] for k,(i,l) in enumerate(gram_pairs))
sumval=ZERO;dimweights={}
for j,c in w.items():
    if j not in mapping:continue
    v=mapping[j]
    a=F(v[0]+v[1]+v[2]+v[7]+2*v[8]);b=F(sum(v[3:7]))
    delta=(a,b);eta=(a,4*a-b)
    term=mul(mul(mul(eta,eta),eta),inv(mul(D2,delta)))
    sumval=add(sumval,scale(c,term))
    dimweights[(str(a),str(b))]=dimweights.get((str(a),str(b)),F(0))+c
assert sumval==(F(5,6),F(0)),sumval
labels=json.loads((P.parent.parent/'verlinde_witness.json').read_text())
def from_sqrt(v):return (F(v[0])-F(4,3)*F(v[1]),F(v[1])/3)
chars=[[from_sqrt(v) for v in chi] for chi in labels['chars']]
ff=[from_sqrt(v) for v in labels['codegrees']]
spec=importlib.util.spec_from_file_location('tensor_data',P.parents[2]/'current_remaining_cases.py')
tm=importlib.util.module_from_spec(spec);spec.loader.exec_module(tm)
N=tm.TENSORS['R9_2_137']
for chi,f in zip(chars,ff):
    assert chi[0]==(1,0)
    for i in range(9):
        for j in range(9):
            total=ZERO
            for k in range(9):total=add(total,scale(N[i][j][k],chi[k]))
            assert total==mul(chi[i],chi[j])
    total=ZERO
    for z in chi:total=add(total,mul(z,z))
    assert total==f
vals=[ZERO]*9
for j,c in w.items():
    if j not in mapping:continue
    v=mapping[j];a=F(v[0]+v[1]+v[2]+v[7]+2*v[8]);b=F(sum(v[3:7]))
    delta=(a,b);eta=(a,4*a-b)
    factor=mul(mul(eta,eta),inv(mul(D,delta)))
    for e,(chi,f) in enumerate(zip(chars,ff)):
        charval=ZERO
        for i in range(9):charval=add(charval,scale(v[i],chi[i]))
        vals[e]=add(vals[e],scale(c,mul(factor,mul(charval,inv(f)))))
assert vals==[from_sqrt(v) for v in labels['witness_NBB']]
result={'source_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'old_relaxation_equations_verified':len(x['b']),'support':len(w),'nonnegative':True,'removed_columns_used':0,'physical_columns_with_unweighted_Gram_verified':len(mapping),'complete_nine_character_table_multiplicativity':'PASS','all_nine_distinguished_Verlinde_coefficients_independently_replayed':'PASS','N_BB_to_B':{'rational':'5/6','d_coefficient':'0'},'verdict':'The published +TY rational relaxation witness cannot extend to modular fusion data because forced Verlinde coefficients are nonintegral, some even irrational.','scope':'One witness rejection only. No exclusion of R9_2_137 or all feasible solutions. No optimizer used.'}
(Path(__file__).parent/'audit_r137_verlinde.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
