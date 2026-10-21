"""Necessary tensor action of the unique central lift of source g.

The exact core finite-domain proof forces mass(g)=1. The complete low
frame contains only one central simple restricting to source1, so G^2=1.
For the surviving indicator branches nu2(g)=-1, hence theta_G=+/-i and G
acts freely on central simples. Low translates give forced high masses;
other high masses are invariant under g; fixed restriction types have even
mass. These constraints concern actual integral multiplicities only.
"""
from pathlib import Path
from collections import Counter
import json,hashlib,sys
HERE=Path(__file__).resolve().parent

def main(fi=2,dual_parity=False):
 d=json.loads((HERE/f'frame{fi}_system.json').read_text());domain=json.loads((HERE/f'frame{fi}_domains.json').read_text())
 ROOT=HERE.parents[2];profiles=json.loads((ROOT/'evidence/rank8_frontier_20261021/commutative_integer/R8_3_982_profile.json').read_text());P=profiles['records'][fi]
 vectors={r['index']:(0,)+tuple(r['vector'])for r in P['high_vectors']};orbits=[tuple(vectors[i]for i in o['indices'])for o in P['duality_orbits']]
 lookup={v:j for j,o in enumerate(orbits)for v in o}
 perm=(6,2,1,4,3,7,0,5);act=lambda v:tuple(v[perm[i]]for i in range(8))
 low=Counter(map(tuple,P['low_columns']));unit=(1,0,0,0,0,0,0,0);g=act(unit)
 if low[unit]!=1:raise AssertionError('forgetful kernel not verified trivial in low frame')
 lower=d['source_lower'];upper=d['source_upper'];keep=d['metadata']['source_metadata']['retained_indices'];pos={j:k for k,j in enumerate(keep)}
 gi=lookup[g];gdomain=[lower[gi]+v for v in domain['domains'][pos[gi]]]if gi in pos else[lower[gi]]
 if gdomain!=[1]:raise AssertionError('unique central lift of g not forced')
 rows=[];receipts=[];seen=set();parities=[]
 def add(terms,rhs,reason):
  row=[0]*len(keep)
  for j,a in terms.items():
   rhs-=a*lower[j]
   if j in pos:row[pos[j]]+=a
   elif lower[j]!=upper[j]:raise AssertionError('nonretained nonfixed mass')
  if not any(row):
   if rhs:raise AssertionError('central-action scalar contradiction '+str(reason))
   return
  key=tuple(row)+(rhs,)
  if key not in seen:seen.add(key);rows.append(row+[rhs]);receipts.append(reason)
 for j,orbit in enumerate(orbits):
  for v in orbit:
   if v[6]:add({j:1},low[act(v)],('low_translate_mass',j,v,act(v)))
   else:
    w=act(v)
    if w not in lookup:add({j:1},0,('missing_high_translate',j,v,w))
    else:
     k=lookup[w]
     if k!=j:add({j:1,k:-1},0,('high_translate_equality',j,k))
    du=(0,2,1,4,3,5,6,7)
    if w==v or (dual_parity and w==tuple(v[k]for k in du)):
     if j in pos:parities.append((pos[j],(-lower[j])%2,j))
     elif lower[j]%2:raise AssertionError('fixed central g-invariant restriction has odd multiplicity')
 base=[[a for a in row]+[b]for row,b in zip(zip(*d['columns']),d['rhs'])]
 combined=base+rows;columns=list(map(list,zip(*(row[:-1]for row in combined))))
 out={**d,'columns':columns,'rhs':[row[-1]for row in combined],'central_action_rows':receipts,'dual_semion_parity':dual_parity,'central_action_parities':sorted(set(parities)),'central_action_source':{'profile_sha256':hashlib.sha256(json.dumps(P,sort_keys=True).encode()).hexdigest(),'core_domain_certificate_sha256':hashlib.sha256((HERE/f'frame{fi}_domains.json').read_bytes()).hexdigest(),'central_g_original_index':gi,'central_g_reduced_index':pos.get(gi),'central_g_domain':gdomain,'source_g_index':6,'requires_indicator_g':-1,'unique_low_source_unit':True}}
 (HERE/f'central{"_dual"if dual_parity else""}_frame{fi}_system.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
 print('central action',fi,'new equalities',len(rows),'even high masses',len(set(parities)),flush=True)
if __name__=='__main__':main(int(sys.argv[1]),'--dual'in sys.argv)
