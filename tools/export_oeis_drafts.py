#!/usr/bin/env python3
"""Generate provisional b-files from fully classified multiplicity bands only."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'data/classification_status.json').read_text())['rows']
byrank={r:[x for x in rows if x['rank']==r] for r in (4,5)}
for rank, cells in byrank.items():
    complete=[]
    for x in cells:
        if x['classification_coverage']!='complete_classification':break
        complete.append(x)
    assert len(complete)=={4:128,5:20}[rank]
    target=ROOT/f'oeis/draft_rank{rank}_realized.txt'
    target.parent.mkdir(exist_ok=True)
    target.write_text(''.join(f"{x['multiplicity']} {x['realized_unitary']+x['realized_other_or_unspecified']+x['realized_spherical_nonpseudounitary']}\n" for x in complete))
    print(f'{target.name}: {len(complete)} fully classified bands in this release')
