"""Replay all 2026-10-02 rank-seven changes and preservation of prior decisions.

Categorical existence/nonexistence theorems are cited mathematical inputs.
This finite replay checks complete model tensors and all obstruction hypotheses.
"""
from pathlib import Path
import sys,json,hashlib,collections,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'software'))
from exact import require
from residual_update_20261002 import model_records,verify_f210,verify_support40
from half_partition_tannakian import verify as verify_half_partition
from half_partition_tannakian import verify_odd120
from oriented_signed import validate_general
from ty_equivariant_models import verify_targets as verify_ty
from quaternion_equivariant_model import verify_target as verify_quaternion
from verify_r7_4_2019_chern import verify_record as verify_chern
from dimension52_equivariantization import verify as verify_dimension52
from dimension52_equivariantization import verify_record as verify_dimension52_record
from verify_d96_premises import verify as verify_dimension96
from verify_d96_premises import verify_record as verify_dimension96_record
from order16_orbit_obstruction import verify_orbit_obstruction

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
    rows=json.loads((ROOT/'output/rank7_ledger.json').read_text());by={r['id']:r for r in rows}
    require((ROOT/'data/model_catalog.json').read_bytes()==(ROOT/'output/rank7_model_catalog.json').read_bytes(),
            'published model catalogue alias differs')
    from analyze import read_source
    source=read_source(4)
    require(len(rows)==len(source),'source length')
    require(all(r['id']==s['id'] and r['source_line']==s['source_line'] and r['tensor']==s['tensor']
                for r,s in zip(rows,source)),'source census binding')
    models=model_records(rows);stored=json.loads((ROOT/'data/residual_20261002_models.json').read_text())
    require(models==stored,'new model catalogue differs from reconstruction')
    require({m['id']for m in models}=={'R7_3_602','R7_2_218','R7_2_313','R7_2_1','R7_2_195','R7_4_2','R7_4_2019'},'model coverage')
    ty=verify_ty(rows);quaternion=verify_quaternion(rows)
    require(ty==json.loads((ROOT/'output/ty_equivariant_models_verification.json').read_text()),'TY receipt')
    require(quaternion==json.loads((ROOT/'output/quaternion_equivariant_model_verification.json').read_text()),'quaternion receipt')
    chern_record=json.loads((ROOT/'data/r7_4_2019_chern_certificate.json').read_text())
    require(chern_record['tensor']==by['R7_4_2019']['tensor'],'Chern model source binding')
    chern=verify_chern(chern_record)
    require(chern==json.loads((ROOT/'output/r7_4_2019_chern_verification.json').read_text()),'Chern model receipt')
    dimension52_record=json.loads((ROOT/'data/r7_2_75_certificate.json').read_text())
    dimension52=verify_dimension52_record(dimension52_record,by['R7_2_75']['tensor'])
    require(dimension52==json.loads((ROOT/'output/r7_2_75_verification.json').read_text()),'dimension-52 receipt')
    dimension96_records=json.loads((ROOT/'data/d96_premise_certificates.json').read_text())
    dimension96=[verify_dimension96_record(r,by[r['id']]['tensor'])for r in dimension96_records]
    require(dimension96==json.loads((ROOT/'output/d96_premise_verification.json').read_text())['records'],
            'dimension-96 source-premise receipt')
    orbit=json.loads(json.dumps(verify_orbit_obstruction()))
    require(orbit==json.loads((ROOT/'output/order16_orbit_verification.json').read_text()),'order-16 orbit receipt')
    for m in models:
        validate_general(m['tensor']);r=by[m['id']]
        require(r['status']=='unitarily_realized' and r['model_names']==[m['name']],'new model status')
    exclusions=json.loads((ROOT/'data/residual_20261002_exclusions.json').read_text())
    require(set(exclusions)=={'R7_2_185','R7_3_635','R7_3_900','R7_3_905','R7_3_991','R7_4_2727','R7_2_75','R7_2_252','R7_2_315'},'exclusion coverage')
    for rid,c in exclusions.items():
        r=by[rid];validate_general(r['tensor'])
        {'localized_TPE_F210':verify_f210,'solvable_minkowski_support':verify_support40,
         'half_partition_tannakian':verify_half_partition,
         'odd_pointed_tannakian_120':verify_odd120,
         'solvable_double_equivariantization_orbit_obstruction':verify_dimension52,
         'D96_solvable_order16_orbit_obstruction':verify_dimension96}[c['kind']](r['tensor'],c)
        require(r['status']=='excluded' and r['certificate']==c and r['criterion']==c['kind'],'exclusion record')
    p=json.loads((ROOT/'data/residual_20261002_preservation.json').read_text());changed=set(exclusions)|{m['id']for m in models}
    require(digest([r for r in rows if r['id']not in changed])==p['unchanged_records_sha256'],'prior record changed')
    require(digest([r for r in rows if r['status']=='excluded' and r['id']not in changed])==p['prior_negative_records_sha256'],'prior exclusion changed')
    summary=json.loads((ROOT/'output/rank7_summary.json').read_text())
    counts={str(m):dict(collections.Counter(r['status']for r in rows if r['multiplicity']==m))for m in range(1,5)}
    require(summary['status_counts']==counts,'status counts')
    require(set(p['changed_ids'])==changed and len(changed)==16,'preservation coverage')
    require(sum(r['status']=='unitarily_realized'for r in rows)==26,'model total')
    require(sum(r['status']=='excluded'for r in rows)==4116,'exclusion total')
    require(sum(r['status']=='unresolved'for r in rows)==59,'unresolved total')
    report={'passed':True,'new_models':7,'new_general_exclusions':9,'unchanged_records':len(rows)-len(changed),
            'old_negative_records_preserved':4107,'status_counts':counts,'optimized_python':not __debug__,
            'TY_action_coherence_and_orbit_fusion':ty,'quaternion_action_and_fusion':quaternion,
            'quaternion_Chern_class_model':chern,'dimension52_general_exclusion':dimension52,
            'dimension96_general_exclusions':dimension96,'order16_orbit_corroboration':orbit,
            'scope':'Exact model constructions including coherent equivariantizations and a global characteristic-class group-theoretical model, source theorem/local-template hypotheses, rational support inequalities, double-equivariantization orbit obstruction, and preservation hashes; no new large associator or center search, no rerun of published TPE Groebner basis.'}
    (ROOT/'output/residual_20261002_verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
