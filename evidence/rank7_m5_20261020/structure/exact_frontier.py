"""Exact structural grouping of the initial fifteen-ring M5 frontier.

This is an invariant report, not a categorical existence/nonexistence test.
"""
import itertools
import json
import sys
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'supplements/rank7/software'))
from rings import Characters, dual, fingerprint, permute
from exact import ec, evaluate, pc, require, t


def analyze(row):
    R = row['tensor']
    n = len(R)
    du = dual(R)
    inv = [i for i in range(n) if sum(R[i][du[i]]) == 1]
    chars = Characters(R)
    f, K, ds, D, pD, emb = chars.fp()
    dp = []
    for d, N in zip(ds, chars.N):
        ff = [g for g, _ in N.charpoly(t).as_poly().factor_list()[1]
              if not evaluate(g.all_coeffs(), d, K)]
        require(len(ff) == 1, 'dimension minimal polynomial ambiguity')
        dp.append(pc(ff[0]))
    actions = {str(g): [next(k for k, v in enumerate(R[g][i]) if v)
                        for i in range(n)] for g in inv}
    subs = []
    for bits in range(1, 2 ** (n - 1) - 1):
        I = [0] + [j for j in range(1, n) if bits >> (j - 1) & 1]
        S = set(I)
        if all(du[i] in S for i in I) and all(
                k in S for i in I for j in I for k, v in enumerate(R[i][j]) if v):
            subs.append(I)
    autos = []
    for tail in itertools.permutations(range(1, n)):
        p = (0,) + tail
        if all(du[p[i]] == p[du[i]] and dp[p[i]] == dp[i] for i in range(n)):
            if permute(R, p) == R:
                autos.append(list(p))
    return {'id': row['id'], 'tensor_sha256': fingerprint(R),
            'duality': du, 'invertibles': inv, 'invertible_actions': actions,
            'proper_nontrivial_subrings': subs, 'automorphisms': autos,
            'automorphism_count': len(autos),
            'fp_field_generator_polynomial': pc(f),
            'fp_generator_isolating_interval': [str(emb.lo), str(emb.hi)],
            'fp_dimensions_in_generator': [ec(d) for d in ds],
            'fp_dimension_minimal_polynomials': dp,
            'global_fp_dimension_in_generator': ec(D),
            'global_fp_dimension_minimal_polynomial': pc(pD),
            'formal_codegree_factors': [{'polynomial': pc(g), 'multiplicity': m}
                                        for g, m in chars.cf]}


def main():
    source = HERE.parent / 'computation/source_frontier.json'
    rows = json.loads(source.read_text())
    require(len(rows) == 15, 'initial frontier must have fifteen records')
    report = [analyze(row) for row in rows]
    groups = {}
    for row in report:
        key = ','.join(row['global_fp_dimension_minimal_polynomial'])
        groups.setdefault(key, []).append(row['id'])
    result = {'scope': 'Exact structural invariants only; no classification status changed.',
              'source': str(source.relative_to(ROOT)), 'records': report,
              'equal_global_dimension_groups': list(groups.values())}
    (HERE / 'exact_frontier.json').write_text(json.dumps(result, indent=2) + '\n')
    for row in report:
        print(row['id'], 'invertibles', row['invertibles'],
              'subrings', row['proper_nontrivial_subrings'],
              'aut', row['automorphism_count'],
              'global', row['global_fp_dimension_minimal_polynomial'], flush=True)


if __name__ == '__main__':
    main()
