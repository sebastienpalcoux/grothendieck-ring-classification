#!/usr/bin/env python3
"""Validate every committed count and classification partition without downloads."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
counts=json.loads((ROOT/'data/counts.json').read_text())
status=json.loads((ROOT/'data/classification_status.json').read_text())
assert counts['census_commit']=='b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726'
rows=counts['rows']
cells={(x['rank'],x['multiplicity']):x['rings'] for x in rows}
assert len(cells)==len(rows)==2162
assert all(x['rings']>=0 for x in rows)
assert all(cells[(2,m)]==(2 if m==1 else 1) for m in range(1,1001))
for entry in counts['rank_summary']:
    rank=entry['rank'];b=entry['recorded_through']
    assert set(k[1] for k in cells if k[0]==rank)==set(range(1,b+1))
    assert sum(cells[(rank,m)] for m in range(1,b+1))==entry['classes_at_recorded_bound']
with (ROOT/'data/counts.csv').open(newline='') as f:
    csvrows=list(csv.DictReader(f))
assert [(int(x['rank']),int(x['multiplicity']),int(x['rings'])) for x in csvrows]==[(x['rank'],x['multiplicity'],x['rings']) for x in rows]

statusrows=status['rows']
assert len(statusrows)==2162
assert {(x['rank'],x['multiplicity']) for x in statusrows}==set((r,m) for r,b in [(2,1000),(3,1000),(4,128),(5,20),(6,8),(7,4),(8,2)] for m in range(1,b+1))
byrank=defaultdict(lambda:defaultdict(int))
for x in statusrows:
    r,m=x['rank'],x['multiplicity']
    assert x['rings']==cells[(r,m)]
    columns=['excluded_general','realized_unitary','realized_other_or_unspecified',
             'realized_spherical_nonpseudounitary','unresolved_general','unassessed']
    assert all(type(x[c]) is int and x[c]>=0 for c in columns)
    assert sum(x[c] for c in columns)==x['rings']
    expected=('census_only' if x['unassessed'] else
              'partial_classification' if x['unresolved_general'] else
              'complete_classification')
    assert x['classification_coverage']==expected
    for c in columns:byrank[r][c]+=x[c]
assert byrank[4]['excluded_general']==889515 and byrank[4]['realized_other_or_unspecified']==15
assert byrank[5]['excluded_general']==40982 and byrank[5]['realized_other_or_unspecified']==17 and byrank[5]['unresolved_general']==0
assert byrank[2]['realized_other_or_unspecified']==2 and byrank[2]['excluded_general']==999
assert byrank[3]['realized_other_or_unspecified']==5 and byrank[3]['excluded_general']==460348
assert byrank[6]['excluded_general']==16536 and byrank[6]['realized_unitary']==53 and byrank[6]['realized_spherical_nonpseudounitary']==1 and byrank[6]['unresolved_general']==22
assert (byrank[7]['excluded_general'],byrank[7]['realized_unitary'],byrank[7]['unresolved_general'])==(4107,16,78)
assert (byrank[8]['excluded_general'],byrank[8]['realized_unitary'],byrank[8]['unresolved_general'])==(824,33,116)
rank6_expected=[(39,18,21,0,0),(154,132,21,1,0),(384,381,3,0,0),
                (872,863,2,0,7),(1582,1579,1,0,2),(2768,2762,3,0,3),
                (3814,3810,2,0,2),(6999,6991,0,0,8)]
for m,expected in enumerate(rank6_expected,1):
    row=next(x for x in statusrows if x['rank']==6 and x['multiplicity']==m)
    assert tuple(row[k] for k in ('rings','excluded_general','realized_unitary',
                                  'realized_spherical_nonpseudounitary','unresolved_general'))==expected
rank6_root=ROOT/'supplements/rank6'
rank6_raw=(rank6_root/'data/decisions.json').read_bytes()
assert hashlib.sha256(rank6_raw).hexdigest()==status['inputs']['rank6']['sha256']=='c8ad5ac40750125259e14b01a70f174abd1d76e97cbc596473a1481b6717adab'
rank6_ledger=json.loads(rank6_raw)
assert len(rank6_ledger)==len({x['id'] for x in rank6_ledger})==16612
for m,expected in enumerate(rank6_expected,1):
    band=[x for x in rank6_ledger if x['m']==m]
    assert (len(band),*(sum(x['status']==s for x in band) for s in
            ('excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved')))==expected
rank6_summary=json.loads((rank6_root/'verification/release_summary.json').read_text())
assert (rank6_summary['excluded'],rank6_summary['positive'],rank6_summary['unresolved'])==(16536,54,22)
assert rank6_summary['general_multiplicity_three_complete'] is True
assert rank6_summary['complete_through_multiplicity']==status['inputs']['rank6']['general_complete_through']==3
assert rank6_summary['first_unresolved']=='R6_4_6'
assert (rank6_summary['first_continuation_excluded'],rank6_summary['second_continuation_excluded'])==(7,18)
assert len(json.loads((rank6_root/'data/model_catalog.json').read_text()))==54
assert next(x for x in rank6_ledger if x['id']=='R6_3_215')['status']=='excluded'
assert sum(x['rings'] for x in statusrows if x['rank']==6 and x['multiplicity']<=3)==577
assert sum(x['excluded_general'] for x in statusrows if x['rank']==6 and x['multiplicity']<=3)==531
rank6_bundle=next(x for x in status['bundles'] if x['name']==status['inputs']['rank6']['current_bundle'])
assert rank6_bundle=={'name':'Rank6_Categorification_M8_Revised_2026-09-29_v2.zip',
                      'sha256':'c9508a49228f199e8f4bf476edddb72a0eddcce45b6e249a11b9f49105de2467'}
assert next(x for x in statusrows if x['rank']==5 and x['multiplicity']==18)['excluded_general']==5080
assert all(next(x for x in statusrows if x['rank']==5 and x['multiplicity']==m)['excluded_general']==cells[(5,m)] for m in (19,20))
assert all(x['unassessed']==0 for x in statusrows)
assert status['inputs']['rank5']['sha256']=='9261917451d469ece9929a1756f505924cf84adf34e79a0d2e6f68fed43f55cf'
for rank, expected, ledger in ((7,4201,'supplements/rank7/output/rank7_ledger.json'),
                               (8,973,'supplements/rank8/data/decisions.json')):
    raw=(ROOT/ledger).read_bytes()
    assert status['inputs'][f'rank{rank}']['sha256']==hashlib.sha256(raw).hexdigest()
    records=json.loads(raw)
    assert len(records)==expected
    assert sum(x['status']=='unitarily_realized' for x in records)==len(json.loads((ROOT/f'supplements/rank{rank}/data/model_catalog.json').read_text()))
    assert all(next(x for x in statusrows if x['rank']==rank and x['multiplicity']==m)['rings']==sum(x['multiplicity']==m for x in records)
               for m in set(x['multiplicity'] for x in records))
for name in ('pinned_full_verification','optimized_inert_full_verification',
             'extension19_20_verification','extension19_20_optimized_verification'):
    report=json.loads((ROOT/f'supplements/rank5/verification/{name}.json').read_text())
    assert report['status']=='PASS'
    assert report['general_exclusions']==(12506 if 'extension' in name else 28476)
with (ROOT/'data/classification_status.csv').open(newline='') as f:
    csvstatus=list(csv.DictReader(f))
assert len(csvstatus)==len(statusrows)
for a,b in zip(csvstatus,statusrows):
    assert all(a[k]==str(v) for k,v in b.items())
realized=json.loads((ROOT/'data/grothendieck_counts.json').read_text())['rows']
assert len(realized)==len(statusrows)
with (ROOT/'data/grothendieck_counts.csv').open(newline='') as f:
    csvrealized=list(csv.DictReader(f))
assert len(csvrealized)==len(realized)
for a,b,s in zip(csvrealized,realized,statusrows):
    assert all(a[k]==str(v) for k,v in b.items())
    assert (b['rank'],b['multiplicity'])==(s['rank'],s['multiplicity'])
    assert b['known_realized']==sum(s[c] for c in ('realized_unitary',
        'realized_other_or_unspecified','realized_spherical_nonpseudounitary'))
    assert b['unresolved_general']==s['unresolved_general']
    assert b['count_relation']==('unknown' if s['unassessed'] else
          'lower_bound' if s['unresolved_general'] else 'exact')
assert all(x['missing_in_repository']==x['additional_in_repository']==0
           for x in json.loads((ROOT/'data/rank5_crosswalk.json').read_text())['bands'])
assert json.loads((ROOT/'data/rank6_crosswalk.json').read_text())['records']==16612
for rank,bound in ((4,128),(5,20)):
    lines=(ROOT/f'oeis/draft_rank{rank}_realized.txt').read_text().splitlines()
    assert len(lines)==bound
    for m,line in enumerate(lines,1):
        x=next(x for x in statusrows if x['rank']==rank and x['multiplicity']==m)
        assert x['classification_coverage']=='complete_classification'
        assert line==f"{m} {x['realized_unitary']+x['realized_other_or_unspecified']+x['realized_spherical_nonpseudounitary']}"
print('Verified 2,162 census cells and 2,162 categorification bands; no unassessed band interpreted as zero.')
