#!/usr/bin/env python3
"""Refresh rank-seven/eight publication rows from their frozen decision ledgers.

The existing lower-rank status rows and input identities are preserved exactly.
"""
import collections,csv,hashlib,json
from pathlib import Path
from publication_stages import load_stages
ROOT=Path(__file__).resolve().parents[1]
def main():
    target=ROOT/'data/classification_status.json';x=json.loads(target.read_text())
    latest=load_stages(ROOT)['latest']
    old_lower=[r.copy() for r in x['rows'] if r['rank']<7]
    sources={7:('supplements/rank7/output/rank7_ledger.json','supplements/rank7/release/rank7-certified-through-m4.zip'),
             8:('supplements/rank8/data/decisions.json','supplements/rank8/rank8-verified-supplement.zip')}
    for rank,(ledger,archive) in sources.items():
        raw=(ROOT/ledger).read_bytes();rows=json.loads(raw);counts=collections.Counter(r['status'] for r in rows)
        x['inputs'][f'rank{rank}'].update(file=ledger,sha256=hashlib.sha256(raw).hexdigest(),status_totals=dict(counts),
            residual_update='evidence/'+latest+'/README.md')
        for row in x['rows']:
            if row['rank']!=rank:continue
            band=[d for d in rows if d['multiplicity']==row['multiplicity']]
            if not band:raise ValueError('Missing census band')
            co=collections.Counter(d['status'] for d in band)
            if co.keys()-{'excluded','unitarily_realized','unresolved'}:raise ValueError('Unknown status')
            row.update(rings=len(band),excluded_general=co['excluded'],realized_unitary=co['unitarily_realized'],
                realized_other_or_unspecified=0,realized_spherical_nonpseudounitary=0,unresolved_general=co['unresolved'],
                unassessed=0,classification_coverage='partial_classification' if co['unresolved'] else 'complete_classification')
        a=ROOT/archive
        b=next(z for z in x['bundles'] if z['name']==a.name);b['sha256']=hashlib.sha256(a.read_bytes()).hexdigest()
    if old_lower!=[r for r in x['rows'] if r['rank']<7]:raise ValueError('Lower-rank status changed')
    target.write_text(json.dumps(x,indent=2)+'\n')
    with (ROOT/'data/classification_status.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(x['rows'][0]));w.writeheader();w.writerows(x['rows'])
    print({r:x['inputs'][f'rank{r}']['status_totals'] for r in (7,8)})
if __name__=='__main__':main()
