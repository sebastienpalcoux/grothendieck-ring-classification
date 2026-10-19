#!/usr/bin/env python3
"""Import the rank-seven M5 census without changing lower-rank release pins."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/sebastienpalcoux/fusion-ring-census'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('census', type=Path)
    p.add_argument('--commit', required=True)
    a = p.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', a.commit):
        raise ValueError('A full published census commit is required')
    manifest = json.loads(a.census.read_text())
    entry = manifest['ranks']['7']
    if (entry['bound'], entry['classes'], entry['counts']) != (5, 10006, {'1':43,'2':319,'3':1059,'4':2780,'5':5805}):
        raise ValueError('Unexpected rank-seven M5 census partition')
    target = ROOT/'data/counts.json'
    result = json.loads(target.read_text())
    old = {r['multiplicity']:r['rings'] for r in result['rows'] if r['rank']==7}
    if any(old[m] != entry['counts'][str(m)] for m in range(1,5)):
        raise ValueError('Extension changes an earlier census band')
    imported = [dict(rank=7,multiplicity=m,rings=entry['counts'][str(m)],
                     source=f'{SOURCE}/blob/{a.commit}/results/rank7/counts.csv',
                     verification=f'{SOURCE}/blob/{a.commit}/verification/rank7/audit.json')
                for m in range(1,6)]
    result['rows'] = sorted([r for r in result['rows'] if r['rank']!=7]+imported,
                            key=lambda r:(r['multiplicity'],r['rank']))
    summary = next(r for r in result['rank_summary'] if r['rank']==7)
    summary.update(census_through=5,recorded_through=5,classes_at_recorded_bound=10006,
                   method='pinned_repository',census_commit=a.commit)
    result.setdefault('census_extensions', {})['rank7_m5'] = {
        'date':'2026-10-19', 'census_commit':a.commit,
        'manifest_sha256':hashlib.sha256(a.census.read_bytes()).hexdigest(),
        'tables_gz_sha256':entry['tables_gz_sha256'],
        'completeness_basis':entry.get('completeness_basis'),
        'independent_enumeration_rerun':entry.get('independent_enumeration_rerun',False),
        'independent_verification_scope':entry.get('independent_verification_scope')}
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    with (ROOT/'data/counts.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['rank','multiplicity','rings','source','verification'],lineterminator='\n')
        w.writeheader();w.writerows(result['rows'])
    print('Imported rank seven through M5: 10,006 rings; earlier release pins preserved.')

if __name__=='__main__':main()
