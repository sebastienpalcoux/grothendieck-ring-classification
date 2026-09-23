#!/usr/bin/env python3
"""Export exact-multiplicity based-ring counts from a pinned census manifest.

Usage: python tools/generate_counts.py PATH/TO/fusion-ring-census/results/census.json
"""
import csv
import json
import sys
from pathlib import Path

PINNED_COMMIT = 'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726'
ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/sebastienpalcoux/fusion-ring-census'

def export(path, output_dir=None):
    manifest = json.loads(path.read_text())
    output_dir = Path(output_dir) if output_dir else ROOT/'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = [dict(rank=2, multiplicity=m, rings=2 if m == 1 else 1,
                 source='Rank-two fusion-ring normal form X²=1+nX (n≥0)',
                 verification='Symbolic count; n=0 and n=1 both have multiplicity 1')
            for m in range(1,1001)]
    summary = [dict(rank=2, census_through='all', recorded_through=1000,
                    classes_at_recorded_bound=1001, method='symbolic')]
    for rank in range(3,9):
        entry = manifest['ranks'][str(rank)]
        assert entry['complete'] and entry['verified']
        bound = entry['bound']
        counts = entry['counts']
        assert set(counts) == {str(m) for m in range(1,bound+1)}
        assert sum(counts.values()) == entry['classes']
        for m in range(1,bound+1):
            rows.append(dict(rank=rank, multiplicity=m, rings=counts[str(m)],
                             source=f'{SOURCE}/blob/{PINNED_COMMIT}/results/rank{rank}/counts.csv',
                             verification=f'{SOURCE}/blob/{PINNED_COMMIT}/verification/rank{rank}/audit.json'))
        summary.append(dict(rank=rank, census_through=bound, recorded_through=bound,
                            classes_at_recorded_bound=entry['classes'], method='pinned_repository'))
    rows.sort(key=lambda row:(row['multiplicity'],row['rank']))
    result = dict(schema='grothendieck-ring-classification/counts/v1',
                  scope='Based fusion rings up to based-ring isomorphism; all duality types; categorifiability is a separate problem.',
                  multiplicity='Exact maximum structure constant; multiplicity 1 includes every ring with all coefficients at most 1.',
                  census_repository=SOURCE,census_commit=PINNED_COMMIT,
                  rank_summary=summary, rows=rows)
    (output_dir/'counts.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    with (output_dir/'counts.csv').open('w',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=['rank','multiplicity','rings','source','verification'])
        writer.writeheader();writer.writerows(rows)
    print(f'Wrote {len(rows)} exact-multiplicity cells; repository bounds: '+', '.join(f'r{a["rank"]}: {a["census_through"]}' for a in summary))

if __name__ == '__main__':
    if len(sys.argv)!=2: raise SystemExit(__doc__)
    export(Path(sys.argv[1]))
