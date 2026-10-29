"""Independent SymPy check of R928's bosonic-row obstruction.

Uses no prior quartic arithmetic implementation or spectral-projector code.
The categorical premises and conclusions are recorded in audit_r928_bosonic_row.md.
"""
import json
from pathlib import Path
import sympy as s

P=Path(__file__).resolve().parents[1]/'r928'/'prior'
data=json.loads((P/'spectral_reduction.json').read_text())
src=next(r for r in json.loads((P/'source.json').read_text())['records'] if r['id']=='R8_3_928')
a,b=s.sqrt(2),s.sqrt(3)
basis=[s.Integer(1),a,b,a*b]
def value(v):return s.expand(sum(s.Rational(x)*q for x,q in zip(v,basis)))
D=144+96*a+80*b+56*a*b
L=s.expand(D*a/2)
H=s.expand(L/2)
signs=[(1,1),(-1,1),(-1,-1),(1,-1)]
def sigma(v,e,f):
    # Work on explicitly saved coefficient vectors, below, for an unambiguous embedding.
    return s.expand(sum(s.Rational(c)*z for c,z in zip(v,[1,e*a,f*b,e*f*a*b])))

assert all(src['low_columns'][j][0]==1 for j in range(4))
assert all(value(src['full_characters'][j][7])==1 for j in range(4))
rows=[]
for pat in data['patterns']:
    ds=[value(v) for v in pat['dimensions']]
    for j,(e,f) in enumerate(signs):
        assert s.expand(ds[j]*sigma([144,96,80,56],e,f)-D)==0
    labels=[i for i,d in enumerate(ds) if s.expand(d-H)==0]
    for h in labels:
        row=[]
        for j,(e,f) in enumerate(signs):
            expect=s.Rational(e,2)
            assert s.expand(ds[j]*sigma(pat['dimensions'][h],e,f)-expect*L)==0
            row.append(str(expect))
        assert sum(s.Rational(x)**2 for x in row)==1
        assert h>=4
        rows.append({'pattern':pat['pattern'],'H_label':h,'known_S_row':row,'norm_used':'1','forced_S_HH':'0','forced_STS_HH':'1','modular_rhs_HH':'0'})
assert {x['pattern'] for x in rows}=={49,191}
result={'arithmetic':'PASS (independent SymPy implementation)','source_scalar_characters_g':'all +1','canonical_unit_multiplicities':'all 1','excluded_patterns':rows,'scope':'Excludes these two complete center patterns under inherited pseudo-unitary and semion-splitting premises; does not exclude R928 while patterns40,186 survive.'}
(Path(__file__).parent/'audit_r928_bosonic_row.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
