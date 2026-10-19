#!/usr/bin/env python3
"""Export known categorifiable rings, preserving unresolved and unassessed bands.

The source is the checked classification-status ledger. Never infer a zero
Grothendieck-ring count from the fusion-ring census alone.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / 'data/classification_status.json').read_text())
rows = []
for s in source['rows']:
    count = sum(s[k] for k in ('realized_unitary',
                              'realized_other_or_unspecified',
                              'realized_spherical_nonpseudounitary'))
    if s['classification_coverage'] == 'census_only':
        relation = 'unknown'
    elif s['unresolved_general'] or s['unassessed']:
        relation = 'lower_bound'
    else:
        relation = 'exact'
    rows.append(dict(rank=s['rank'], multiplicity=s['multiplicity'],
                     known_realized=count, unresolved_general=s['unresolved_general'],
                     unassessed=s['unassessed'], count_relation=relation))
assert len({(r['rank'], r['multiplicity']) for r in rows}) == len(rows)
payload = dict(schema='grothendieck-ring-classification/realized-counts/v1',
               semantics='Known based-isomorphism classes of complex fusion-category Grothendieck rings; lower_bound indicates unresolved general cases, unknown indicates a band without categorification analysis.',
               rows=rows)
(ROOT / 'data/grothendieck_counts.json').write_text(
    json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + '\n')
with (ROOT / 'data/grothendieck_counts.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print(f'Exported {len(rows)} Grothendieck-ring count bands.')
