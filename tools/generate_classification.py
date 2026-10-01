#!/usr/bin/env python3
"""Summarize the attached rank 4–8 classification ledgers, preserving gaps.

Run with the source paths shown by ``--help``, or use ``--refresh-rank6`` to
replace only the rank-six partition in an existing export. This script never assigns a
categorifiability decision to a census ring absent from the relevant ledger.
"""
import argparse
import csv
import gzip
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def records(rank, path):
    if rank == 4:
        with gzip.open(path, 'rt') as inp:
            for line in inp:
                row = json.loads(line)
                if 'multiplicity' in row:
                    yield row['multiplicity'], row['status']
    else:
        for row in json.loads(path.read_text()):
            yield row['multiplicity'] if rank >= 7 else row['m'], row['general'] if rank == 5 else row['status']


def write_export(out, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir/'classification_status.json').write_text(json.dumps(out, indent=2)+'\n')
    with (output_dir/'classification_status.csv').open('w', newline='') as stream:
        writer=csv.DictWriter(stream, fieldnames=list(out['rows'][0]))
        writer.writeheader()
        writer.writerows(out['rows'])


def refresh_rank6(args):
    """Refresh one ledger without requiring or regenerating other rank releases."""
    out=json.loads((args.output_dir/'classification_status.json').read_text())
    summary=defaultdict(Counter)
    allowed={'excluded', 'unitarily_realized',
             'spherically_realized_nonpseudounitary', 'unresolved'}
    ledger=json.loads(args.rank6.read_text())
    census=json.loads((args.output_dir/'counts.json').read_text())
    expected={x['multiplicity']:x['rings'] for x in census['rows'] if x['rank']==6}
    if len(ledger)!=sum(expected.values()) or len({x['id'] for x in ledger})!=len(ledger):
        raise ValueError('Rank-six ledger must cover the pinned census exactly')
    for row in ledger:
        if type(row['m']) is not int or row['status'] not in allowed:
            raise ValueError('Unknown rank-six multiplicity or status')
        summary[row['m']][row['status']]+=1
    bound=max(expected)
    if set(summary)!=set(expected) or set(expected)!=set(range(1,bound+1)):
        raise ValueError('Rank-six ledger has an unexpected multiplicity domain')
    current=[]
    for m in sorted(expected):
        row={'rank':6,'multiplicity':m,'rings':expected[m]}
        totals=summary[row['multiplicity']]
        if sum(totals.values())!=row['rings']:
            raise ValueError('The new ledger changes the pinned census partition')
        row.update(excluded_general=totals['excluded'],
                   realized_unitary=totals['unitarily_realized'],
                   realized_other_or_unspecified=0,
                   realized_spherical_nonpseudounitary=totals['spherically_realized_nonpseudounitary'],
                   unresolved_general=totals['unresolved'], unassessed=0,
                   classification_coverage=('partial_classification' if totals['unresolved']
                                            else 'complete_classification'))
        current.append(row)
    out['rows']=sorted([x for x in out['rows'] if x['rank']!=6]+current,
                       key=lambda x:(x['rank'],x['multiplicity']))
    complete=0
    for m in range(1,bound+1):
        if summary[m]['unresolved']:break
        complete=m
    out['inputs']['rank6']={
        'file':args.rank6.name, 'sha256':digest(args.rank6),
        'classified_through':bound, 'general_complete_through':complete,
        'status_totals':dict(sum(summary.values(),Counter())),
        'current_bundle':args.rank6_bundle.name}
    bundle={'name':args.rank6_bundle.name,'sha256':digest(args.rank6_bundle)}
    out['bundles']=[x for x in out['bundles'] if not x['name'].startswith('Rank6_Categorification_M')]+[bundle]
    write_export(out,args.output_dir)
    print('Refreshed rank-six partition; all other rank rows and inputs preserved.')


def export(args):
    census = json.loads(args.census.read_text())
    by_rank = {}
    for rank in (4, 5, 6, 7, 8):
        path = getattr(args, f'rank{rank}')
        summary = defaultdict(Counter)
        for m, status in records(rank, path):
            assert isinstance(m, int) and m > 0
            summary[m][status] += 1
        by_rank[rank] = summary
        assert set(summary) == set(range(1, max(summary) + 1))
        assert all(sum(summary[m].values()) == census['ranks'][str(rank)]['counts'][str(m)]
                   for m in summary)
        expected = (census['ranks'][str(rank)]['bound'], census['ranks'][str(rank)]['classes'])
        assert (max(summary), sum(map(sum, (x.values() for x in summary.values())))) == expected

    data = []
    for rank in (2, 3, 4, 5, 6, 7, 8):
        census_counts = census['ranks'][str(rank)]['counts'] if rank>=3 else {
            str(m):(2 if m==1 else 1) for m in range(1,1001)}
        for m in sorted(map(int, census_counts)):
            if rank==2:
                statuses=Counter({'realized':2}) if m==1 else Counter({'excluded':1})
            elif rank==3:
                positive=4 if m==1 else 1 if m==2 else 0
                statuses=Counter({'realized':positive,'excluded':census_counts[str(m)]-positive})
            else:
                statuses = by_rank[rank].get(m, Counter())
            excluded = statuses.get('excluded', 0)
            realized_unitary = statuses.get('unitarily_realized', 0)
            realized_unspecified = statuses.get('realized', 0)
            realized_spherical_nonpseudo = statuses.get('spherically_realized_nonpseudounitary', 0)
            unresolved = statuses.get('unresolved', 0)
            assessed = sum(statuses.values())
            rings = census_counts[str(m)]
            assert assessed in (0, rings)
            if assessed == 0:
                coverage = 'census_only'
            elif unresolved:
                coverage = 'partial_classification'
            else:
                coverage = 'complete_classification'
            data.append(dict(rank=rank, multiplicity=m, rings=rings,
                             excluded_general=excluded,
                             realized_unitary=realized_unitary,
                             realized_other_or_unspecified=realized_unspecified,
                             realized_spherical_nonpseudounitary=realized_spherical_nonpseudo,
                             unresolved_general=unresolved, unassessed=rings-assessed,
                             classification_coverage=coverage))

    inputs = {f'rank{rank}': {'file': getattr(args, f'rank{rank}').name,
                              'sha256': digest(getattr(args, f'rank{rank}')),
                              'classified_through': max(by_rank[rank]),
                              'status_totals': dict(sum(by_rank[rank].values(), Counter()))}
              for rank in (4, 5, 6, 7, 8)}
    complete=0
    for m in sorted(by_rank[6]):
        if by_rank[6][m]['unresolved']:break
        complete=m
    inputs['rank6']['general_complete_through']=complete
    if args.rank6_bundle:inputs['rank6']['current_bundle']=args.rank6_bundle.name
    inputs['rank2']={'basis':'X²=1+nX, n>=0; complex realizations exactly n=0,1',
                     'classified_through':'all'}
    inputs['rank3']={'basis':'Five unrestricted categorical Grothendieck rings: four of multiplicity 1 and one of multiplicity 2; see the standalone sphericality and ring-classification manuscript',
                     'classified_through':'all',
                     'proof_status':'Independent ring-level necessity proof and sphericality argument in manuscripts/rank3.tex; source includes an exact arithmetic checker.'}
    bundles=[{'name':args.bundle.name,'sha256':digest(args.bundle)}]
    for rank in (5,6,7,8):
        bundle=getattr(args,f'rank{rank}_bundle')
        if bundle:bundles.append({'name':bundle.name,'sha256':digest(bundle)})
    out = dict(schema='grothendieck-ring-classification/status/v1',
               semantics='Rows count based-isomorphism classes. Unresolved means a general categorification decision remains open in the attached release; unassessed means no classification ledger for this census band. Realized means at least one realization, not every categorification has the given structure.',
               bundles=bundles,
               inputs=inputs, rows=data)
    write_export(out,args.output_dir)
    print('Wrote status for', len(data), 'rank/multiplicity bands:',
          [(r,max(by_rank[r]),sum(map(sum,(x.values() for x in by_rank[r].values()))))
           for r in (4,5,6,7,8)])


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--refresh-rank6',action='store_true',
                   help='Replace only rank-six rows/metadata in the existing status export')
    p.add_argument('--bundle', type=Path)
    for r in (5,6,7,8):p.add_argument(f'--rank{r}-bundle',type=Path)
    p.add_argument('--output-dir',type=Path,default=ROOT/'data')
    p.add_argument('--census', type=Path)
    for r in (4,5,6):p.add_argument(f'--rank{r}', type=Path)
    p.add_argument('--rank7',type=Path,default=ROOT/'supplements/rank7/output/rank7_ledger.json')
    p.add_argument('--rank8',type=Path,default=ROOT/'supplements/rank8/data/decisions.json')
    args=p.parse_args()
    required=('rank6','rank6_bundle') if args.refresh_rank6 else ('bundle','census','rank4','rank5','rank6')
    for name in required:
        if getattr(args,name) is None:p.error('--'+name.replace('_','-')+' is required')
    (refresh_rank6 if args.refresh_rank6 else export)(args)
