#!/usr/bin/env python3
"""Refresh rank-seven/eight publication rows from their frozen decision ledgers.

The existing lower-rank status rows and input identities are preserved exactly.
"""
import collections,csv,hashlib,json
from pathlib import Path
from publication_stages import load_stages
from rank7_publication import PUBLICATION_DATE
from rank8_publication import ledger_path as rank8_ledger, archive_path as rank8_archive, extension as rank8_extension
ROOT=Path(__file__).resolve().parents[1]
def main():
    target=ROOT/'data/classification_status.json';x=json.loads(target.read_text())
    latest=load_stages(ROOT)['latest']
    old_lower=[r.copy() for r in x['rows'] if r['rank']<7]
    sources={7:('supplements/rank7/output/rank7_ledger.json','supplements/rank7/release/rank7-certified-through-m5.zip'),
             8:(rank8_ledger(ROOT),rank8_archive(ROOT))}
    for rank,(ledger,archive) in sources.items():
        raw=(ROOT/ledger).read_bytes();rows=json.loads(raw);counts=collections.Counter(r['status'] for r in rows)
        counts.setdefault('unresolved',0)
        x['inputs'][f'rank{rank}'].update(file=ledger,sha256=hashlib.sha256(raw).hexdigest(),status_totals=dict(counts),
            residual_update='evidence/'+latest+'/README.md')
        census=json.loads((ROOT/'data/counts.json').read_text())
        x['rows']=[row for row in x['rows'] if row['rank'] != rank] + [
            dict(rank=rank, multiplicity=row['multiplicity'], rings=row['rings'])
            for row in census['rows'] if row['rank']==rank]
        x['inputs'][f'rank{rank}']['classified_through']=max(r['multiplicity'] for r in rows)
        for row in x['rows']:
            if row['rank']!=rank:continue
            band=[d for d in rows if d['multiplicity']==row['multiplicity']]
            if not band:raise ValueError('Missing census band')
            co=collections.Counter(d['status'] for d in band)
            if co.keys()-{'excluded','unitarily_realized','pseudo_unitarily_realized','unresolved'}:raise ValueError('Unknown status')
            row.update(rings=len(band),excluded_general=co['excluded'],realized_unitary=co['unitarily_realized'],
                realized_other_or_unspecified=co['pseudo_unitarily_realized'],realized_spherical_nonpseudounitary=0,unresolved_general=co['unresolved'],
                unassessed=0,classification_coverage='partial_classification' if co['unresolved'] else 'complete_classification')
        ordered=sorted((r for r in x['rows'] if r['rank']==rank),key=lambda r:r['multiplicity'])
        complete=0
        for row in ordered:
            if row['multiplicity']!=complete+1 or row['classification_coverage']!='complete_classification':break
            complete+=1
        x['inputs'][f'rank{rank}']['general_complete_through']=complete
        a=ROOT/archive
        x['inputs'][f'rank{rank}']['current_bundle']=a.name
        if rank == 7:
            x['inputs']['rank7']['extension'] = {
                'date': PUBLICATION_DATE, 'multiplicity': 5,
                'source': 'supplements/rank7/output/m5/source.json',
                'normal_replay': 'supplements/rank7/output/m5/replay_normal.json',
                'optimized_replay': 'supplements/rank7/output/m5/replay_optimized.json'}
        if rank == 8 and rank8_extension(ROOT):
            x['inputs']['rank8']['extension'] = rank8_extension(ROOT)
        x['bundles']=[z for z in x['bundles'] if not z['name'].startswith(f'rank{rank}-')]
        x['bundles'].append({'name':a.name,'sha256':hashlib.sha256(a.read_bytes()).hexdigest()})
    if old_lower!=[r for r in x['rows'] if r['rank']<7]:raise ValueError('Lower-rank status changed')
    x['rows'].sort(key=lambda row:(row['rank'],row['multiplicity']))
    target.write_text(json.dumps(x,indent=2)+'\n')
    with (ROOT/'data/classification_status.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(x['rows'][0]),lineterminator='\n');w.writeheader();w.writerows(x['rows'])
    print({r:x['inputs'][f'rank{r}']['status_totals'] for r in (7,8)})
if __name__=='__main__':main()
