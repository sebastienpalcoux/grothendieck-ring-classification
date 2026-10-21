#!/usr/bin/env python3
"""Import the accepted M3 census band and model catalogue additively."""
import argparse
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path
from rank8_publication import HISTORICAL_MODELS, MODELS, LEDGER, TABLES, historical_sources
ROOT=Path(__file__).resolve().parents[1]
SOURCE='https://github.com/sebastienpalcoux/fusion-ring-census'

def models():
    old=json.loads((ROOT/HISTORICAL_MODELS).read_text())
    new=json.loads((ROOT/'evidence/rank8_m3_20261021/models/consolidated_models.json').read_text())
    if isinstance(new,dict):new=new['models']
    if len(old)!=77 or any(r['multiplicity']!=3 for r in new):raise ValueError('Model band mismatch')
    rows=old+new
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate model ID')
    path=ROOT/MODELS;path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    historical_sources(ROOT)
    return len(new)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('census',nargs='?',type=Path);p.add_argument('--commit');p.add_argument('--models-only',action='store_true')
    a=p.parse_args();new_models=models()
    if a.models_only:
        print(f'Preserved 77 old models; imported {new_models} new exact-M3 models.');return
    if not (ROOT/LEDGER).is_file():raise ValueError('Accepted M3 publication ledger required')
    if not a.census or not re.fullmatch('[0-9a-f]{40}',a.commit or ''):raise ValueError('Producer manifest and full census commit required')
    manifest=json.loads(a.census.read_text());entry=manifest['ranks']['8']
    if (entry['bound'],entry['classes'],entry['counts'])!=(3,4500,{'1':96,'2':877,'3':3527}):raise ValueError('Unexpected census partition')
    raw=(ROOT/TABLES).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=entry['tables_gz_sha256'] or hashlib.sha256(gzip.decompress(raw)).hexdigest()!=entry['tables_uncompressed_sha256']:
        raise ValueError('Census and classification tensor sources differ')
    target=ROOT/'data/counts.json';result=json.loads(target.read_text())
    old={r['multiplicity']:r['rings'] for r in result['rows'] if r['rank']==8}
    if any(old[m]!=entry['counts'][str(m)] for m in (1,2)):raise ValueError('Earlier bands changed')
    newrow=dict(rank=8,multiplicity=3,rings=3527,source=f'{SOURCE}/blob/{a.commit}/results/rank8/counts.csv',verification=f'{SOURCE}/blob/{a.commit}/verification/rank8/audit.json')
    result['rows']=sorted([r for r in result['rows'] if (r['rank'],r['multiplicity'])!=(8,3)]+[newrow],key=lambda r:(r['multiplicity'],r['rank']))
    next(r for r in result['rank_summary'] if r['rank']==8).update(census_through=3,recorded_through=3,classes_at_recorded_bound=4500,method='pinned_repository',census_commit=a.commit)
    result.setdefault('census_extensions',{})['rank8_m3']={
        'date':'2026-10-21','census_commit':a.commit,'manifest_sha256':hashlib.sha256(a.census.read_bytes()).hexdigest(),
        'tables_gz_sha256':entry['tables_gz_sha256'],'tables_uncompressed_sha256':entry['tables_uncompressed_sha256'],
        'enumeration_source_available':entry.get('enumeration_source_available',False),'completeness_basis':entry.get('completeness_basis'),
        'independent_enumeration_rerun':entry.get('independent_enumeration_rerun',False),'independent_verification_scope':entry.get('independent_verification_scope')}
    prior=result['census_extensions'].get('rank7_m5');rank7=manifest['ranks'].get('7',{})
    if prior and 'completeness_basis' in rank7:
        prior.update(completeness_basis=rank7['completeness_basis'],optimized_source_verified_in_commit=a.commit,enumeration_source_available=rank7.get('enumeration_source_available',False))
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    with (ROOT/'data/counts.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['rank','multiplicity','rings','source','verification'],lineterminator='\n');w.writeheader();w.writerows(result['rows'])
    print(f'Imported 3,527 new rings, 4,500 cumulative; {new_models} new models.')

if __name__=='__main__':main()
