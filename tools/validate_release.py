#!/usr/bin/env python3
"""Validate every committed count and classification partition without downloads."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from rank6_publication import validate_identity,completion_files,require,FRONTIER

ROOT=Path(__file__).resolve().parents[1]
counts=json.loads((ROOT/'data/counts.json').read_text())
status=json.loads((ROOT/'data/classification_status.json').read_text())
rank6_identity=json.loads((ROOT/'data/rank6_release_identity.json').read_text())
validate_identity(rank6_identity)
assert counts['census_commit']==rank6_identity['census_commit']
rows=counts['rows']
cells={(x['rank'],x['multiplicity']):x['rings'] for x in rows}
assert len(cells)==len(rows)==sum(x['recorded_through'] for x in counts['rank_summary'])
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
assert len(statusrows)==len(rows)
assert {(x['rank'],x['multiplicity']) for x in statusrows}==set(cells)
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
assert byrank[6]['excluded_general']==rank6_identity['summary']['excluded'] and byrank[6]['realized_unitary']==56 and byrank[6]['realized_spherical_nonpseudounitary']==1 and byrank[6]['unresolved_general']==rank6_identity['summary']['unresolved']
assert (byrank[7]['excluded_general'],byrank[7]['realized_unitary'],byrank[7]['unresolved_general'])==(4132, 27, 42)
assert (byrank[8]['excluded_general'],byrank[8]['realized_unitary'],byrank[8]['unresolved_general'])==(846, 72, 55)
rank6_expected=[tuple(row) for row in rank6_identity['counts']]
for m,expected in enumerate(rank6_expected,1):
    row=next(x for x in statusrows if x['rank']==6 and x['multiplicity']==m)
    assert tuple(row[k] for k in ('rings','excluded_general','realized_unitary',
                                  'realized_spherical_nonpseudounitary','unresolved_general'))==expected
rank6_root=ROOT/'supplements/rank6'
require(set(completion_files(rank6_root))==set(rank6_identity['completion_files_sha256']),
        'Completion proof inventory differs from the release identity')
for relative,digest in rank6_identity['completion_files_sha256'].items():
    require(hashlib.sha256((rank6_root/relative).read_bytes()).hexdigest()==digest,
            'Completion evidence changed: '+relative)
paper_files={f.relative_to(rank6_root/'papers').as_posix()
             for f in (rank6_root/'papers').rglob('*') if f.is_file()}
require(paper_files==set(rank6_identity['documents']),'Publication document inventory changed')
for name,document in rank6_identity['documents'].items():
    for path in (rank6_root/document['path'],ROOT/'manuscripts/rank6/papers'/name):
        raw=path.read_bytes()
        require(len(raw)==document['bytes'] and hashlib.sha256(raw).hexdigest()==document['sha256'],
                'Publication document changed: '+str(path.relative_to(ROOT)))
rank6_raw=(rank6_root/'data/decisions.json').read_bytes()
require(hashlib.sha256(rank6_raw).hexdigest()==status['inputs']['rank6']['sha256']==rank6_identity['ledger_sha256'],
        'Rank-six ledger hash differs from the release identity')
rank6_ledger=json.loads(rank6_raw)
require({x['id'] for x in rank6_ledger if x['status']=='unresolved'}==FRONTIER,
        'The completed release must retain exactly the two earlier frontier cases')
assert len(rank6_ledger)==len({x['id'] for x in rank6_ledger})==sum(row[0] for row in rank6_expected)
for m,expected in enumerate(rank6_expected,1):
    band=[x for x in rank6_ledger if x['m']==m]
    require((len(band),*(sum(x['status']==s for x in band) for s in
            ('excluded','unitarily_realized','spherically_realized_nonpseudounitary','unresolved')))==expected,
            'Rank-six ledger band differs from the release identity: '+str(m))
rank6_summary=json.loads((rank6_root/'verification/release_summary.json').read_text())
assert (rank6_summary['excluded'],rank6_summary['positive'],rank6_summary['unresolved'])==tuple(rank6_identity['summary'][k] for k in ('excluded','positive','unresolved'))
assert rank6_summary['general_multiplicity_three_complete'] is True
assert rank6_summary['complete_through_multiplicity']==status['inputs']['rank6']['general_complete_through']==3
assert rank6_summary['first_unresolved']==rank6_identity['summary']['first_unresolved']
assert (rank6_summary['first_continuation_excluded'],rank6_summary['second_continuation_excluded'])==(7,18)
assert rank6_summary['third_continuation_excluded']==rank6_identity['summary']['third_continuation_excluded']
assert hashlib.sha256((rank6_root/'certificates/continuation_round3.jsonl').read_bytes()).hexdigest()==rank6_identity['third_certificate_sha256']
assert rank6_summary['fourth_continuation_excluded']==rank6_identity['summary']['fourth_continuation_excluded']
assert hashlib.sha256((rank6_root/'certificates/continuation_round4.jsonl').read_bytes()).hexdigest()==rank6_identity['fourth_certificate_sha256']
for relative, digest in rank6_identity['research_files_sha256'].items():
    if hashlib.sha256((rank6_root/relative).read_bytes()).hexdigest()!=digest:
        raise ValueError('Current research provenance changed: '+relative)
frontier=json.loads((rank6_root/'data/frontier_research_progress.json').read_text())
if {x['id'] for x in frontier['cases']}!={x['id'] for x in rank6_identity['research_progress']}:
    raise ValueError('Publication omits a current frontier case')
require([{'id':x['id'],'result':x['public_summary']} for x in frontier['cases']]==rank6_identity['research_progress'],
        'Publication current summaries differ from the audited overlay')
new_models=json.loads((rank6_root/'data/conformal_positive_models.json').read_text())
if {x['id'] for x in new_models}!=set(rank6_identity['conformal_models']):
    raise ValueError('Conformal constructors do not match the release identity')
assert len(json.loads((rank6_root/'data/model_catalog.json').read_text()))==57
assert next(x for x in rank6_ledger if x['id']=='R6_3_215')['status']=='excluded'
assert next(x for x in rank6_ledger if x['id']=='R6_5_1204')['status']=='excluded'
assert {x['id'] for x in rank6_ledger if x['status']=='unresolved'}=={x['id'] for x in rank6_identity['research_progress']}
assert sum(x['rings'] for x in statusrows if x['rank']==6 and x['multiplicity']<=3)==577
assert sum(x['excluded_general'] for x in statusrows if x['rank']==6 and x['multiplicity']<=3)==531
rank6_bundle=next(x for x in status['bundles'] if x['name']==status['inputs']['rank6']['current_bundle'])
assert rank6_bundle=={k:rank6_identity['archive'][k] for k in ('name','sha256')}
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
    for m in set(x['multiplicity']for x in records):
        band=next(x for x in statusrows if x['rank']==rank and x['multiplicity']==m)
        for col,status_name in [('excluded_general','excluded'),('realized_unitary','unitarily_realized'),('unresolved_general','unresolved')]:
            assert band[col]==sum(x['multiplicity']==m and x['status']==status_name for x in records)
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
assert json.loads((ROOT/'data/rank6_crosswalk.json').read_text())['records']==len(rank6_ledger)
for rank,bound in ((4,128),(5,20)):
    lines=(ROOT/f'oeis/draft_rank{rank}_realized.txt').read_text().splitlines()
    assert len(lines)==bound
    for m,line in enumerate(lines,1):
        x=next(x for x in statusrows if x['rank']==rank and x['multiplicity']==m)
        assert x['classification_coverage']=='complete_classification'
        assert line==f"{m} {x['realized_unitary']+x['realized_other_or_unspecified']+x['realized_spherical_nonpseudounitary']}"
print(f'Verified {len(rows):,} census cells and {len(statusrows):,} categorification bands; no unassessed band interpreted as zero.')
