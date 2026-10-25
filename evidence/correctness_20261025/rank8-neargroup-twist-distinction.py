import os
#!/usr/bin/env python3
"""Exact finite inputs to the twist-spectrum distinction proof.
This checks character tables, all symmetric D-column choices, and D-square rules;
it does not import or certify the categorical third-indicator trace formula.
"""

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
import importlib.util, itertools, json
from pathlib import Path
ROOT = Path(os.environ.get('FUSION_CLASSIFICATION_REPO',Path(__file__).resolve().parents[2])).resolve()
OUT = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('ng', ROOT / 'evidence/unified_20261016/rank8/verify_neargroup_centralizer.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
inv = [m.ONE, m.inv_b, m.inv_c, m.inv_c] + [m.inv_a] * 4
cases = []
for which in [820, 869]:
    M = m.matrix(which)
    N = m.model(which)
    for i, j in itertools.product(range(8), repeat=2):
        require(m.total((m.mul(M[i][k], M[k][j]) for k in range(8))) == (m.D if i == j else m.ZERO), 'rank8-neargroup-twist-distinction: required invariant from original line 16')
    for j in range(8):
        chi = [m.mul(M[i][j], inv[j]) for i in range(8)]
        for i, k in itertools.product(range(8), repeat=2):
            require(m.mul(chi[i], chi[k]) == m.total((m.scale(chi[t], N[i][k][t]) for t in range(8))), 'rank8-neargroup-twist-distinction: required invariant from original line 20')
        f = m.total((m.mul(x, x) for x in chi))
        require(f == m.mul(m.D, m.mul(inv[j], inv[j])), 'rank8-neargroup-twist-distinction: required invariant from original line 22')
        require((f == m.scalar(9)) == (j >= 4), 'rank8-neargroup-twist-distinction: required invariant from original line 23')
    symmetric = []
    for p in itertools.permutations(range(4, 8)):
        if any((M[i][p[j - 4]] != M[j][p[i - 4]] for i, j in itertools.product(range(4, 8), repeat=2))):
            continue
        diag = [m.mul(M[i][p[i - 4]], m.inv_a) for i in range(4, 8)]
        if which == 820:
            require(all((r in [m.ONE, m.scalar(-2)] for r in diag)), 'rank8-neargroup-twist-distinction: required invariant from original line 29')
        else:
            require(p[2] == 6, 'rank8-neargroup-twist-distinction: required invariant from original line 31')
            require(diag[2] == m.scalar(-2), 'rank8-neargroup-twist-distinction: required invariant from original line 32')
            for k in [0, 1, 3]:
                r = diag[k]
                require(m.sub(m.sub(m.mul(m.mul(r, r), r), m.scale(r, 3)), m.ONE) == m.ZERO, 'rank8-neargroup-twist-distinction: required invariant from original line 35')
                require(any(r[1:]), 'rank8-neargroup-twist-distinction: required invariant from original line 36')
        symmetric.append({'D_column_permutation': [v - 4 for v in p], 'D_diagonal_over_a': [[str(x) for x in r] for r in diag]})
    missing = []
    for i in range(4, 8):
        require(N[i][i][:4] == [1, 0, 1, 1], 'rank8-neargroup-twist-distinction: required invariant from original line 40')
        require(sorted(N[i][i][4:]) == [0, 1, 1, 1], 'rank8-neargroup-twist-distinction: required invariant from original line 41')
        f = N[i][i][4:].index(0)
        if which == 820:
            require(f == i - 4, 'rank8-neargroup-twist-distinction: required invariant from original line 43')
        missing.append(f)
    cases.append({'id': f'R8_2_{which}', 'all_character_equations': 512, 'formal_codegree9_columns': [4, 5, 6, 7], 'D_square_missing_labels': missing, 'symmetric_D_column_choices': symmetric})
report = {'status': 'PASS', 'cases': cases, 'scope': 'exact algebraic inputs, not the independent categorical indicator premise'}
(OUT / 'rank8-neargroup-twist-distinction.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'symmetric_column_counts': {c['id']: len(c['symmetric_D_column_choices']) for c in cases}}))
