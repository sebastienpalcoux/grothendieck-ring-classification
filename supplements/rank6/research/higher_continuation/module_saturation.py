"""Frozen-frontier exploratory exact module refinements, with explicit timeouts.

Integral Gram and simultaneous dual-action tests are necessary conditions only.
Surviving actions do not establish existence. This script allocates no decisions.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys
import time

P = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(P / 'software'))
import sympy as s
from exact import require, ec, pc
from module_dual_gram import anti_representations, module_matrices, dual_dimensions, system
from involution_module import invs
from rings import Characters, permute


def integral_system(A, b, meta):
    ng = len(meta['counts']); nr = len(b) - ng
    columns = list(zip(*A)); groups = []
    for g, count in enumerate(meta['counts']):
        choices = [c[:nr] for c in columns if c[nr + g]]
        options = set()
        for selected in itertools.combinations_with_replacement(choices, count):
            v = tuple(sum(x) for x in zip(*selected))
            if all(x <= y for x, y in zip(v, b)):
                options.add(v)
        groups.append(tuple(sorted(options)))
    groups.sort(key=len)
    visits = 0
    @lru_cache(None)
    def solve(k, left):
        nonlocal visits
        visits += 1
        if visits > 2000000:
            raise TimeoutError('integral Gram node budget')
        if k == len(groups):
            return not any(left)
        return any(all(x <= y for x, y in zip(v, left)) and
                   solve(k + 1, tuple(y-x for x, y in zip(v, left)))
                   for v in groups[k])
    answer = solve(0, tuple(b[:nr]))
    return {'feasible': answer, 'nodes': visits,
            'class_options': [len(g) for g in groups], 'columns': len(columns)}


def action_candidates(Ms, seeds, u, v):
    r = Ms[0].rows
    G = [sum((int(Ms[i][m, m])*Ms[i] for i in range(len(Ms))), s.zeros(r))
         for m in range(r)]
    bounds = [math.isqrt(int(G[j][i, i] - (i == j)))
              for i in range(r) for j in range(r)]
    C = s.Matrix.vstack(*[s.kronecker_product(s.eye(r), Ms[i].T) -
                          s.kronecker_product(Ms[i], s.eye(r)) for i in seeds])
    rhs = [0]*C.rows
    for i in range(r):
        row = [0]*r*r; row[i*r+u] = 1
        C = C.col_join(s.Matrix([row])); rhs.append(v[i])
    try:
        sol, params = C.gauss_jordan_solve(s.Matrix(rhs))
    except ValueError:
        return []
    params = list(params)
    free = [next(k for k, e in enumerate(sol) if e == p) for p in params]
    choices = []
    for values in itertools.product(*(range(bounds[k]+1) for k in free)):
        z = sol.subs(dict(zip(params, values)))
        if any(t.q != 1 or t < 0 or t > bounds[k] for k, t in enumerate(z)):
            continue
        X = s.Matrix(r, r, list(z))
        if all(X[i,m]*X[j,m] <= G[m][i,j] - (i == m and j == m)
               for m in range(r) for i in range(r) for j in range(r)):
            choices.append(X)
    return choices


def actions(R, Ms, seeds, g, labels):
    r = Ms[0].rows; u = labels.index((0, 0)); cols = []; done = set()
    for i in range(r):
        if i in done: continue
        j = next(j for j in range(r) if Ms[g][i,j])
        v = [0]*r; v[i] = 1
        if j == i: cols.extend([v[:], v[:]])
        else: v[j] = 1; cols.append(v)
        done.update((i,j))
    cols.remove([int(i == u) for i in range(r)])
    domains = []; counts = []
    for v, count in sorted(Counter(tuple(v) for v in cols).items()):
        candidates = action_candidates(Ms, seeds, u, v)
        counts.append({'column': list(v), 'multiplicity': count,
                       'matrix_candidates': len(candidates)})
        domains.append(list(itertools.combinations_with_replacement(candidates, count)))
    Gs = [sum((int(Ms[i][m,m])*Ms[i] for i in range(len(Ms))), s.zeros(r))
          for m in range(r)]
    survivors = []
    for choice in itertools.product(*domains):
        Xs = [s.eye(r)] + [X for group in choice for X in group]
        if any(sum((X[:,m]*X[:,m].T for X in Xs), s.zeros(r)) != Gs[m]
               for m in range(r)):
            continue
        V = s.Matrix.hstack(*(s.Matrix(list(X)) for X in Xs))
        record = {'action_rank': V.rank(), 'dual_rank': len(Xs)}
        if V.rank() == len(Xs):
            S = []; valid = True
            for X in Xs:
                row = []
                for Y in Xs:
                    try: z, params = V.gauss_jordan_solve(s.Matrix(list(X*Y)))
                    except ValueError: valid = False; break
                    if params or any(t.q != 1 or t < 0 for t in z):
                        valid = False; break
                    row.append([int(t) for t in z])
                if not valid: break
                S.append(row)
            record['based_multiplication'] = valid
            if valid:
                record['dual_tensor'] = S
                record['isomorphisms_to_input'] = [list((0,)+p)
                    for p in itertools.permutations(range(1,len(R)))
                    if len(S) == len(R) and permute(S,(0,)+p) == R]
        survivors.append(record)
    return {'column_domains': counts, 'gram_actions': len(survivors), 'actions': survivors}


def one(rid, stage):
    rows = json.load(open(P/'data/census.json'))
    R = next(row['N'] for row in rows if row['id'] == rid)
    report = {'id': rid, 'stage': stage, 'status': 'not_applicable', 'involutions': []}
    if any(R[i][j] != R[j][i] for i in range(len(R)) for j in range(len(R))):
        return report
    for g in invs(R):
        info = anti_representations(R,g)
        if info is None: continue
        fixed,seeds,nodes,reps = info
        report['status'] = 'completed'
        branch = {'involution': g, 'fixed': fixed, 'anti_representations': len(reps),
                  'branches': []}
        arithmetic = Characters(R).fp()
        branch['primitive_polynomial'] = pc(arithmetic[0])
        for T in reps:
            labels, Ms = module_matrices(R,g,fixed,T)
            _,K,ds,_,_,_ = arithmetic
            dims, profile = dual_dimensions(labels,Ms,g,K,ds)
            profile[tuple(ec(K.one))] += 1
            result = {'dual_dimension_classes': [[list(z),c] for z,c in sorted(profile.items())]}
            if stage == 'integral':
                result['module_simples'] = []
                for m in range(1,len(labels)):
                    ab,meta = system(R,g,fixed,T,m,arithmetic)
                    answer = ({'feasible': False, 'reason': meta['reason']} if ab is None
                              else integral_system(*ab,meta))
                    result['module_simples'].append({'module_simple': m, **answer})
                    if not answer['feasible']: break
            elif stage == 'actions':
                result.update(actions(R,Ms,seeds,g,labels))
            branch['branches'].append(result)
        report['involutions'].append(branch)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--one'); ap.add_argument('--stage', choices=['profile','integral','actions'])
    ap.add_argument('--profiles', action='store_true')
    ap.add_argument('--seconds', type=int, default=12)
    args = ap.parse_args()
    if args.one:
        print(json.dumps(one(args.one,args.stage))); return
    ids = json.load(open(P/'verification/continuation/campaign_manifest.json'))['input_ids']
    if args.profiles:
        records = [one(rid, 'profile') for rid in ids]
        report = {'frozen_input_ids': ids, 'input_count': len(ids),
                  'applicable': sum(r['status'] == 'completed' for r in records),
                  'higher_multiplicity_applicable': sum(r['status'] == 'completed' and
                      int(r['id'].split('_')[1]) >= 4 for r in records), 'records': records}
        Path(__file__).with_name('involution_profiles.json').write_text(
            json.dumps(report, indent=2) + '\n')
        print(report['applicable'], report['higher_multiplicity_applicable'])
        return
    ids = [rid for rid in ids if 4 <= int(rid.split('_')[1]) <= 8]
    start = time.monotonic()
    def job(task):
        rid,stage = task; begun = time.monotonic()
        try:
            result = subprocess.run([sys.executable,__file__,'--one',rid,'--stage',stage],
                                    text=True,capture_output=True,timeout=args.seconds)
            if result.returncode:
                record = {'id':rid,'stage':stage,'status':'error','detail':result.stderr[-1500:]}
            else: record = json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            record = {'id':rid,'stage':stage,'status':'timeout','coverage':'incomplete; no conclusion'}
        record['seconds'] = round(time.monotonic()-begun,3)
        return record
    tasks = [(rid,stage) for rid in ids for stage in ['integral','actions']]
    with ThreadPoolExecutor(max_workers=4) as pool: records = list(pool.map(job,tasks))
    summary = {stage: dict(Counter(r['status'] for r in records if r['stage']==stage))
               for stage in ['integral','actions']}
    report = {'frozen_input_ids':ids,'input_count':len(ids),'per_stage_seconds':args.seconds,
              'wall_seconds':round(time.monotonic()-start,3),'summary':summary,'records':records,
              'allocation_policy':'Research audit only; no decisions changed.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__': main()
