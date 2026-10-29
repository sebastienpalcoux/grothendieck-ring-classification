"""Independent exact audit of the full-character Galois complement rule."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json

P=Path(__file__).resolve().parents[1]/'r137'
x=json.loads((P/'prior'/'forced_export.json').read_text())
labels=json.loads((P/'verlinde_witness.json').read_text())
def add(z,w):return z[0]+w[0],z[1]+w[1]
def mul(z,w):return z[0]*w[0]+2*z[1]*w[1],z[0]*w[1]+z[1]*w[0]+8*z[1]*w[1]
def inv(z):
    q=z[0]*z[0]+8*z[0]*z[1]-2*z[1]*z[1]
    assert q
    return ((z[0]+8*z[1])/q,-z[1]/q)
def sig(z):return z[0]+8*z[1],-z[1]
def scale(c,z):return c*z[0],c*z[1]
def from_sqrt(z):return F(z[0])-F(4,3)*F(z[1]),F(z[1])/3
chars=[[from_sqrt(z) for z in chi] for chi in labels['chars']]
ff=[from_sqrt(z) for z in labels['codegrees']]
def av(v):return v[0]+v[1]+v[2]+v[7]+2*v[8]
def T(v):
    a=av(v)
    return tuple(a-v[i] if 3<=i<=6 else v[i] for i in range(9))
def chi(v,c):
    z=(F(0),F(0))
    for n,k in zip(v,c):z=add(z,scale(n,k))
    return z
for j in range(9):
    v=tuple(int(i==j) for i in range(9))
    assert T(T(v))==v
    for c,f in zip(chars,ff):
        assert chi(T(v),c)==mul(mul(f,inv(sig(f))),sig(chi(v,c)))
old=set(x['removed_columns']); bad=set(); groups=defaultdict(list)
for j,v,_,_,typ in x['physical_mapping']:
    groups[tuple(v),tuple(tuple(F(z) for z in t) for t in typ)].append(j)
    if av(v)>0 and min(T(v))<0:bad.add(j)
    if av(v)==0:
        assert tuple(-z for z in T(v))==tuple(v)
seen=set();eq=[];missing=[]
for key,js in groups.items():
    v,typ=key
    partner=(T(v) if av(v)>0 else v,typ)
    if min(partner[0])<0:continue
    if partner not in groups:
        missing+=js
        continue
    if partner==key or key in seen:continue
    eq.append((sorted(js),sorted(groups[partner])))
    seen.add(key);seen.add(partner)
assert len(bad-old)==8752
case_metadata=json.loads((P/'complement_metadata.json').read_text())
assert set(case_metadata['removed'])==old|bad|set(missing)
canon=lambda pairs:{tuple(sorted((tuple(a),tuple(b)))) for a,b in pairs}
assert canon(eq)==canon(case_metadata['equalities'])
w={j:F(z) for j,z in x['witness']}
violations=sum(sum(w.get(j,F(0)) for j in a)!=sum(w.get(j,F(0)) for j in b) for a,b in eq)
result={'transform_identity_on_all_nine_basis_vectors_and_characters':'PASS','T_squared':'identity','positive_integral_part_sign':'+','pure_large_sign':'-','forbidden_physical_columns_by_negative_complement':len(bad),'newly_forbidden_by_negative_complement':len(bad-old),'additional_newly_forbidden_missing_partner_types':len(set(missing)-old-bad),'total_newly_forbidden':len((bad|set(missing))-old),'total_forbidden_with_previous_filter':len(old|bad|set(missing)),'complete_grouped_trace_pairing_equalities':len(eq),'missing_partner_type_variables':len(missing),'old_witness_positive_forbidden_variables':sum(j in (bad|set(missing)) and z>0 for j,z in w.items()),'old_witness_failed_pairing_equalities':violations,'researcher_filter_and_pairings_independently_matched':True,'scope':'Necessary Galois criterion only; missing-partner deletions require inherited complete column-domain premise; no ring exclusion established by this audit.'}
(Path(__file__).parent/'audit_r137_galois_complement.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
