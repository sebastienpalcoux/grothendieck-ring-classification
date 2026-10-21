"""Independent count of all R1154 fourth-moment histogram fibers.

Uses raw integer-scaled residuals, all seven restriction equations, and a
weighted transfer count. Does not import the discovery enumerator.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[3]

def check(value, message):
    if not value:
        raise ValueError(message)

def read(rel):
    return json.loads((ROOT / rel).read_text())

def count_fiber(counts, columns, group, h):
    scale = 205
    alpha = Q(group['alpha'])
    norm = int(alpha * scale**2)
    types = []
    for n, col, row, bounds in zip(counts, columns,
            group['minimum_norm_rows_by_high_type'], group['integer_pair11_ranges']):
        if not n:
            continue
        qrow = list(map(Q, row))
        options = []
        for x in range(bounds[0], bounds[1] + 1):
            t = Q(x) - qrow[0]
            if t*t > alpha:
                continue
            pair = [q+t*v for q,v in zip(qrow,h)]
            check(all(z.denominator == 1 and z >= 0 for z in pair),
                  'Discovery domain must imply full pair-product integrality')
            options.append(int(scale*t))
        check(options, 'Nonempty coordinate domain on incoming survivor')
        aggregate = Counter()
        for values in combinations_with_replacement(options, n):
            square = sum(v*v for v in values)
            if square <= norm:
                total = sum(values)
                aggregate[(tuple(total*c for c in col), square)] += 1
        if not aggregate:
            return 0, 0
        types.append(aggregate)
    # This count keeps multiplicities when distinct histograms have identical
    # linear and norm contributions; hence it counts histograms, not states.
    types.sort(key=len)
    ntypes = len(types)
    lower = [[0]*8 for _ in range(ntypes+1)]
    upper = [[0]*8 for _ in range(ntypes+1)]
    for i in range(ntypes-1, -1, -1):
        vectors = [linear+(cost,) for linear,cost in types[i]]
        for j in range(8):
            lower[i][j] = lower[i+1][j]+min(v[j] for v in vectors)
            upper[i][j] = upper[i+1][j]+max(v[j] for v in vectors)
    @lru_cache(None)
    def transfer(i, target):
        if any(v < a or v > b for v,a,b in zip(target,lower[i],upper[i])):
            return 0
        if i == ntypes:
            return int(not any(target))
        return sum(m * transfer(i+1, tuple(a-b for a,b in zip(target,linear+(cost,))))
                   for (linear,cost),m in types[i].items())
    answer = transfer(0, (0,)*7+(norm,))
    return answer, transfer.cache_info().currsize

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args=parser.parse_args()
    paths = {
        'base':'evidence/rank8_center_followup_20261021/r1154_quartic_necessary_filters.json',
        'incoming':'evidence/rank8_center_followup_20261021/r1154_quartic_coordinate_propagation.json',
        'gram':'evidence/rank8_frontier_20261021/central_integrality/integer_gram_1154.json',
        'discovery':'evidence/rank8_next_20261021/r1154/joint_quartic_fibers.json'}
    base,incoming,gram,discovery=[read(paths[k]) for k in ('base','incoming','gram','discovery')]
    check(discovery['all_histogram_solutions_enumerated'] and discovery['complete'], 'complete discovery')
    ids=incoming['survivor_indices']
    check(len(ids)==292 and [r['index'] for r in discovery['results']]==ids, 'identical incoming domain')
    groups={i:g for g in base['groups'] for i in g['indices']}
    h=list(map(Q,base['h']))
    results=[]
    for record in discovery['results']:
        ix=record['index']; group=groups[ix]
        count,nodes=count_fiber(gram['completions'][ix], gram['high_columns'],group,h)
        solutions=record.get('pair11_histogram_solutions_by_high_type',[])
        # Independently check all saved witnesses, including all ten pair
        # products, and reject duplicate canonical histograms.
        keys=set()
        for solution in solutions:
            key=tuple(tuple((x,m) for x,m in hist if m) for hist in solution)
            check(key not in keys, 'duplicate saved histogram');keys.add(key)
            lin=[Q(0)]*7;square=Q(0)
            for n,col,row,hist in zip(gram['completions'][ix],gram['high_columns'],
                    group['minimum_norm_rows_by_high_type'],solution):
                check(sum(m for x,m in hist)==n, 'multiplicity')
                for x,m in hist:
                    check(isinstance(x,int) and isinstance(m,int) and m>=0,'histogram integers')
                    if not m:continue
                    t=Q(x)-Q(row[0]); square+=m*t*t
                    for j in range(7):lin[j]+=m*col[j]*t
                    check(all((Q(v)+t*hh).denominator==1 and Q(v)+t*hh>=0
                              for v,hh in zip(row,h)), 'ten pair products')
            check(not any(lin) and square==Q(group['alpha']), 'full joint equations')
        check(count==len(solutions), f'independent exact count mismatch at {ix}')
        results.append({'index':ix,'histograms':count,'transfer_states':nodes})
    out={'schema':'r1154-joint-quartic-independent-review/v1','passed':True,
         'patterns':len(results),'empty':sum(r['histograms']==0 for r in results),
         'nonempty':sum(r['histograms']>0 for r in results),
         'total_histograms':sum(r['histograms'] for r in results),'results':results,
         'scope':'Complete necessary joint pair-product fibers; no ring categorifiability decision',
         'source_sha256':{p:sha256((ROOT/p).read_bytes()).hexdigest() for p in paths.values()},
         'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(out,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
