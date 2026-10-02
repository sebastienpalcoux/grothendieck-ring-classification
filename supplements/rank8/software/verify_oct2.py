"""Replay the finite October 2 update; preserve every earlier unaffected record."""
from pathlib import Path
from itertools import product
import collections,json,gzip,hashlib
from oct2_extensions import require,model_tensor,verify_certificate
ROOT=Path(__file__).resolve().parents[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def fp(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def main():
    raw=gzip.open(ROOT/'data/rank8_tables.txt.gz','rb').read()
    require(hashlib.sha256(raw).hexdigest()=='97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600')
    rings=[json.loads(l.replace('{','[').replace('}',']')) for l in raw.decode().splitlines() if l.strip()]
    source={fp(R):R for R in rings};require(len(source)==973)
    ds=json.loads((ROOT/'data/decisions.json').read_text());by={d['id']:d for d in ds}
    models=json.loads((ROOT/'data/realized_models.json').read_text());mb={d['id']:d for d in models}
    baseline=json.loads((ROOT/'data/oct2_baseline_fingerprints.json').read_text())
    for rid,h in baseline['unchanged_record_sha256'].items():require(digest(by[rid])==h,rid+' old record changed')
    for rid,h in baseline['previous_positive_record_sha256'].items():require(digest(mb[rid])==h,rid+' old model changed')
    positives=json.loads((ROOT/'data/oct2_models.json').read_text());negatives=json.loads((ROOT/'data/oct2_exclusions.json').read_text())
    require(len(positives)==22 and len(negatives)==8)
    require(len(mb)==len(models), 'duplicate realized-model IDs')
    require(set(mb)==set(baseline['previous_positive_record_sha256'])|{x['id'] for x in positives}, 'realized-model inventory mismatch')
    require(len(by)==len(ds)==973, 'ledger ID inventory is not unique and complete')
    require(set(by)==set(baseline['unchanged_record_sha256'])|{x['id'] for x in positives+negatives}, 'ledger inventory mismatch')
    require(set(baseline['changed_ids'])=={x['id'] for x in positives+negatives})
    for x in positives:
        rid=x['id'];R=source[x['tensor_sha256']];require(x['tensor']==R and mb[rid]==x)
        require(len(x['constructors'])==1, rid+' must have exactly one independently replayed new constructor')
        T=model_tensor(rid);require(T==x['constructors'][0]['tensor'])
        q=x['constructors'][0]['basis_map_source_to_model'];require(q[0]==0 and sorted(q)==list(range(8)))
        require(all(R[i][j][k]==T[q[i]][q[j]][q[k]] for i,j,k in product(range(8),repeat=3)))
        require(all(T[0][i][j]==T[i][0][j]==int(i==j) for i,j in product(range(8),repeat=2)))
        require(all(sum(T[i][j][p]*T[p][k][l] for p in range(8))==sum(T[j][k][p]*T[i][p][l] for p in range(8)) for i,j,k,l in product(range(8),repeat=4)))
        require(by[rid]['status']=='unitarily_realized' and by[rid]['models']==[x['constructors'][0]['model']])
    for x in negatives:
        rid=x['id'];d=by[rid];R=source[d['tensor_sha256']];require(R==x['tensor'])
        require(d['status']=='excluded' and d['certificate']==x['certificate']);verify_certificate(R,x['certificate'])
    from verify_r8_1_7_zesting import verify as verify_central_square_root
    central_lift_report=verify_central_square_root()
    require(central_lift_report['status']=='PASS')
    from verify_pseudo_psu_swap import verify as verify_flip
    flip_report=json.loads(json.dumps(verify_flip(),default=str))
    require(flip_report['status']=='PASS')
    from verify_r8_1_53_orbifold import verify as verify_orbifold
    orbifold_report=verify_orbifold()
    require(orbifold_report['status']=='PASS')
    from verify_r8_1_12_orbifold import verify as verify_cyclic_orbifold
    cyclic_orbifold_report=verify_cyclic_orbifold()
    require(cyclic_orbifold_report['status']=='PASS')
    from verify_r8_1_83_triality import verify as verify_triality
    triality_report=verify_triality()
    require(triality_report['status']=='PASS')
    counts=[]
    for m in (1,2):
        co=collections.Counter(d['status'] for d in ds if d['multiplicity']==m)
        counts.append(dict(multiplicity=m,fusion_rings=sum(co.values()),excluded=co['excluded'],realized=co['unitarily_realized'],unresolved=co['unresolved']))
    require(counts==json.loads((ROOT/'data/classification_counts.json').read_text()))
    report=dict(status='PASS',new_unitary_models=[x['id'] for x in positives],new_general_exclusions=[x['id'] for x in negatives],
        full_tensor_coefficients_per_positive=512,central_lift_replay=central_lift_report,flip_action_replay=flip_report,orbifold_replay=orbifold_report,cyclic_orbifold_replay=cyclic_orbifold_report,triality_replay=triality_report,previous_unaffected_ledger_records_preserved=len(baseline['unchanged_record_sha256']),
        previous_positive_records_preserved=len(baseline['previous_positive_record_sha256']),counts=counts,
        scope='Twenty-two explicit categorical constructions and eight general exclusions; earlier proofs retained unchanged.')
    (ROOT/'verification/oct2_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
