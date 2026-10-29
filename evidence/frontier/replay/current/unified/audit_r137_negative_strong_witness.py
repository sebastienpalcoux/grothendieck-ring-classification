"""Independent exact replay of the surviving -TY rational relaxation witness.

No optimizer or rref, and no claim of category existence.
"""
from fractions import Fraction as F
from collections import defaultdict
from itertools import combinations_with_replacement
from pathlib import Path
import json,hashlib

P=Path(__file__).resolve().parents[1]/'r137'
source=P/'prior/forced_export_minus.json';x=json.loads(source.read_text())
wf=P/'negative_strong_exact_witness.json';wit=json.loads(wf.read_text())
assert wit['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
w={int(j):F(z) for j,z in wit['witness']}
assert len(w)==len(wit['witness'])==124 and all(c>0 for c in w.values())
drop={244,245,246,247,260,261,262,263}
assert sorted(drop)==wit['removed_test_rows']
rows=0
for i,(row,rhs) in enumerate(zip(x['A'],x['b'])):
    if i in drop:continue
    assert sum(F(row[j])*z for j,z in w.items())==F(rhs),(i,rhs)
    rows+=1
assert rows==256
assert not set(w).intersection(x['removed_columns'])
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0]+8*a[1]*b[1]
def scale(c,a):return c*a[0],c*a[1]
def inv(a):
    norm=a[0]*a[0]+8*a[0]*a[1]-2*a[1]*a[1]
    return (a[0]+8*a[1])/norm,-a[1]/norm
def from_sqrt(z):return F(z[0])-F(4,3)*F(z[1]),F(z[1])/3
cf=json.loads((P/'verlinde_witness.json').read_text())
chars=[[from_sqrt(z) for z in chi] for chi in cf['chars']];ff=[from_sqrt(z) for z in cf['codegrees']]
mp={j:(tuple(v),tuple(tuple(F(z) for z in t) for t in typ)) for j,v,_,_,typ in x['physical_mapping']}
groups=defaultdict(list)
for j,key in mp.items():groups[key].append(j)
def av(v):return v[0]+v[1]+v[2]+v[7]+2*v[8]
def partner(v):
    a=av(v)
    return tuple(a-v[i] if a and 3<=i<=6 else v[i] for i in range(9))
def charvals(v):
    out=[]
    for chi,f in zip(chars,ff):
        z=(F(0),F(0))
        for k in range(9):z=add(z,scale(v[k],chi[k]))
        out.append(mul(z,inv(f)))
    return out
ZERO=(F(0),F(0));D=(F(16),F(32));pairs=list(combinations_with_replacement(range(9),2));fusion=[ZERO]*45;ind={3:[ZERO]*4,4:[ZERO]*4};mass_checks=0
assert [list(p) for p in pairs]==wit['labelpairs']
for j,c in w.items():
    if j not in mp:continue
    v,typ=mp[j];pv=partner(v);assert min(pv)>=0 and (pv,typ) in groups
    lhs=sum(w.get(k,F(0)) for k in groups[v,typ]);rhs=sum(w.get(k,F(0)) for k in groups[pv,typ]);assert lhs==rhs
    cc=charvals(v);mass=ZERO
    for z in cc:mass=add(mass,mul(z,z))
    assert mass[1]==0
    if not v[0]:assert mass[0]<F(3,4);mass_checks+=1
    a=F(av(v));b=F(sum(v[3:7]));delta=(a,b);eta=(a,4*a-b);fac=mul(eta,inv(delta))
    for q,(e,f) in enumerate(pairs):fusion[q]=add(fusion[q],scale(c,mul(fac,mul(cc[e],cc[f]))))
    for m in [3,4]:
        term=mul(mul(delta,inv(D)),from_sqrt(typ[m-1]))
        for q in range(4):ind[m][q]=add(ind[m][q],scale(c*v[q+3],term))
for z,target in zip(fusion,wit['fusionblock']):assert z==(F(target),F(0)) and target>=0 and isinstance(target,int)
assert ind[3]==[(F(1,2),F(0))]*4
assert ind[4]==[(F(2),F(0))]*4
out={'status':'PASS','support':len(w),'general_inherited_equations_verified':rows,'dropped_test_only_rows':sorted(drop),'complement_pairing_of_all_supported_types':'PASS','strict_bosonic_mass_supported_columns_verified':mass_checks,'distinguished_fusion_block_entries':45,'all_fusion_entries_nonnegative_integers':True,'all_fusion_radical_parts_zero':True,'projected_nu3':['1/2']*4,'projected_nu4':[2]*4,'witness_sha256':hashlib.sha256(wf.read_bytes()).hexdigest(),'scope':'An exact rational witness for a necessary relaxation, not integral central multiplicities, complete modular data, associators, or a categorification.'}
(Path(__file__).parent/'audit_r137_negative_strong_witness.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
