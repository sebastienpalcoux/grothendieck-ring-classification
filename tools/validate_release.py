#!/usr/bin/env python3
"""Validate every committed count and classification partition without downloads."""
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
counts=json.loads((ROOT/'data/counts.json').read_text())
status=json.loads((ROOT/'data/classification_status.json').read_text())
assert counts['census_commit']=='b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726'
rows=counts['rows']
cells={(x['rank'],x['multiplicity']):x['rings'] for x in rows}
assert len(cells)==len(rows)==2156
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
assert len(statusrows)==2156
assert {(x['rank'],x['multiplicity']) for x in statusrows}==set((r,m) for r,b in [(2,1000),(3,1000),(4,128),(5,20),(6,8)] for m in range(1,b+1))
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
assert byrank[5]['excluded_general']==40980 and byrank[5]['realized_other_or_unspecified']==17 and byrank[5]['unresolved_general']==2
assert byrank[2]['realized_other_or_unspecified']==2 and byrank[2]['excluded_general']==999
assert byrank[3]['realized_other_or_unspecified']==5 and byrank[3]['excluded_general']==460348
assert byrank[6]['excluded_general']==16511 and byrank[6]['realized_unitary']==53 and byrank[6]['realized_spherical_nonpseudounitary']==1 and byrank[6]['unresolved_general']==47
assert next(x for x in statusrows if x['rank']==6 and x['multiplicity']==8)['excluded_general']==6980
assert next(x for x in statusrows if x['rank']==5 and x['multiplicity']==18)['unresolved_general']==2
assert all(next(x for x in statusrows if x['rank']==5 and x['multiplicity']==m)['excluded_general']==cells[(5,m)] for m in (19,20))
assert all(x['unassessed']==0 for x in statusrows)
assert status['inputs']['rank5']['sha256']=='4ca1313570668d55b4d9203de4d5e613d381d32e7db7155bbacfff30ce8757b2'
for name in ('pinned_full_verification','optimized_pinned_verification',
             'extension19_20_verification','optimized_extension19_20_verification'):
    report=json.loads((ROOT/f'supplements/rank5/verification/{name}.json').read_text())
    assert report['status']=='PASS'
    assert report['general_exclusions']==(12506 if 'extension' in name else 28474)
with (ROOT/'data/classification_status.csv').open(newline='') as f:
    csvstatus=list(csv.DictReader(f))
assert len(csvstatus)==len(statusrows)
for a,b in zip(csvstatus,statusrows):
    assert all(a[k]==str(v) for k,v in b.items())
assert all(x['missing_in_repository']==x['additional_in_repository']==0
           for x in json.loads((ROOT/'data/rank5_crosswalk.json').read_text())['bands'])
assert json.loads((ROOT/'data/rank6_crosswalk.json').read_text())['records']==16612
for rank,bound in ((4,128),(5,17)):
    lines=(ROOT/f'oeis/draft_rank{rank}_realized.txt').read_text().splitlines()
    assert len(lines)==bound
    for m,line in enumerate(lines,1):
        x=next(x for x in statusrows if x['rank']==rank and x['multiplicity']==m)
        assert x['classification_coverage']=='complete_classification'
        assert line==f"{m} {x['realized_unitary']+x['realized_other_or_unspecified']+x['realized_spherical_nonpseudounitary']}"
print('Verified 2,156 census cells and 2,156 categorification bands; no unassessed band interpreted as zero.')
