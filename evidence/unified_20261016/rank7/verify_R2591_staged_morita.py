#!/usr/bin/env python3
"""Exact source/group certificate for the general R7_4_2591 exclusion."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def need(value, message):
    if not value:
        raise RuntimeError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def group_table(kind):
    if kind == 'C8':
        return [[(a+b) % 8 for b in range(8)] for a in range(8)]
    if kind == 'C2^3':
        return [[a ^ b for b in range(8)] for a in range(8)]
    pairs = list(itertools.product(range(4), range(2)))
    index = {g: i for i, g in enumerate(pairs)}
    out = []
    for a, b in pairs:
        row = []
        for c, d in pairs:
            sign = (-1)**b if kind in ('D8', 'Q8') else 1
            correction = 2*b*d if kind == 'Q8' else 0
            row.append(index[((a+sign*c+correction) % 4, (b+d) % 2)])
        out.append(row)
    return out


def group_data(table):
    inv = [next(j for j in range(8) if table[i][j] == 0) for i in range(8)]
    need(all(table[0][i] == table[i][0] == i for i in range(8)), 'group unit')
    need(all(table[table[i][j]][k] == table[i][table[j][k]]
             for i, j, k in itertools.product(range(8), repeat=3)), 'group associativity')
    aut = []
    for tail in itertools.permutations(range(1, 8)):
        p = (0,)+tail
        if all(p[table[i][j]] == table[p[i]][p[j]]
               for i, j in itertools.product(range(8), repeat=2)):
            aut.append(p)
    klein = []
    for tail in itertools.combinations(range(1, 8), 3):
        L = (0,)+tail
        if all(table[i][i] == 0 for i in L) and all(table[i][j] in L for i in L for j in L):
            klein.append(L)
    return inv, aut, klein


def double_orbits(table, left, right):
    unseen = set(range(8))
    result = []
    while unseen:
        g = min(unseen)
        orbit = {table[table[l][g]][r] for l in left for r in right}
        stabilizer = sum(table[table[l][g]][r] == g for l in left for r in right)
        result.append((sorted(orbit), stabilizer))
        unseen -= orbit
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    here = Path(__file__).resolve().parent
    dependency = here / 'verify_R2591_twisted_v4.py'
    with tempfile.TemporaryDirectory(prefix='r2591_staged_') as tmp:
        receipt = Path(tmp)/'initial_reduction.json'
        command = [sys.executable]
        if sys.flags.optimize:
            command.append('-O')
        command += [str(dependency), '--repo', str(args.repo), '--output', str(receipt)]
        replay = subprocess.run(command, check=True, text=True, capture_output=True)
        initial = json.loads(receipt.read_text())
    need(initial['status'] == 'PASS' and initial['case'] == 'R7_4_2591', 'initial twisted reduction replay')
    source_path = args.repo/'supplements/rank7/data/rank7_tables.txt.gz'
    counts = collections.Counter()
    source = None
    for line in gzip.open(source_path, 'rt'):
        if not line.strip():
            continue
        tensor = json.loads(line.replace('{', '[').replace('}', ']'))
        m = max(v for aa in tensor for bb in aa for v in bb)
        counts[m] += 1
        if (m, counts[m]) == (4, 2591):
            source = tensor
            break
    need(source is not None and digest(source) == initial['tensor_sha256'], 'source tensor binding')
    G, X, Y, Z = [0, 3, 4, 5], 6, 1, 2
    need(source[Y][Z][0] == source[Z][Y][0] == 1, 'source irrational dual pair')
    need(source[X][X] == [int(i in G) for i in range(7)], 'source integral TY sector')
    for g in G:
        for w in (X, Y, Z):
            expected = [int(i == w) for i in range(7)]
            need(source[g][w] == source[w][g] == expected, 'individual fixedness on both sides')

    # Every nontrivial subgroup of V4 has a nontrivial character restriction.
    vectors = list(itertools.product(range(2), repeat=2))
    character_restrictions = []
    for v in vectors[1:]:
        values = [sum(a*b for a, b in zip(c, v)) % 2 for c in vectors]
        need(sorted(values) == [0, 0, 1, 1], 'surjective character restriction to C2')
        character_restrictions.append({'generator': v, 'character_exponents': values})

    rows = []
    stored = {}
    for kind in ('C8', 'C4xC2', 'C2^3', 'D8', 'Q8'):
        table = group_table(kind)
        inv, aut, klein = group_data(table)
        stored[kind] = (table, inv, aut, klein)
        nonnormal_involutions = []
        for h in range(1, 8):
            if table[h][h] != 0:
                continue
            if any(table[table[g][h]][inv[g]] != h for g in range(8)):
                nonnormal_involutions.append(h)
            else:
                orbits = double_orbits(table, [0, h], [0, h])
                need(len(orbits) == 4 and all(len(o) == 2 and st == 2 for o, st in orbits),
                     'normal involution gives eight pointed bimodules')
        need(bool(nonnormal_involutions) == (kind == 'D8'), 'only D8 has nonnormal involutions')
        if kind in ('C8', 'Q8'):
            need(not klein, 'no inverse V4 subgroup')
        count = 0
        fixed_rows = []
        for L in klein:
            need(all(table[table[g][l]][inv[g]] in L for g in range(8) for l in L), 'L normal')
            for phi in aut:
                if {phi[l] for l in L} != set(L):
                    continue
                for a in set(range(8))-set(L):
                    square = [table[table[a][g]][inv[a]] for g in range(8)]
                    if phi[a] != a or any(phi[phi[g]] != square[g] for g in range(8)):
                        continue
                    count += 1
                    need(kind != 'D8', 'D8 restriction-square obstruction')
                    fixed = [d for d in L if d and phi[d] == d]
                    need(fixed, 'fixed nontrivial inverse-subgroup involution')
                    d = fixed[0]
                    need(all(table[d][g] == table[g][d] for g in range(8)), 'delta central')
                    pointed = double_orbits(table, [0, d], [0, d])
                    irrational = double_orbits(table, [0, d], [0, phi[d]])
                    need(len(pointed) == len(irrational) == 4, 'four support orbits of each type')
                    need(all(len(o) == 2 and st == 2 for o, st in pointed+irrational),
                         'all staged stabilizers C2')
                    fixed_rows.append({'L': L, 'phi': phi, 'a': a, 'delta': d})
        rows.append({'group': kind, 'multiplication_sha256': digest(table), 'automorphisms': len(aut),
                     'V4_subgroups': klein, 'nonnormal_involutions': nonnormal_involutions,
                     'compatible_inverse_systems': count, 'fixed_involution_witnesses': fixed_rows})
    need(next(r for r in rows if r['group'] == 'D8')['compatible_inverse_systems'] == 0,
         'nonabelian inverse group eliminated')

    table, inv, aut, klein = stored['D8']
    central = [z for z in range(1, 8) if all(table[z][g] == table[g][z] for g in range(8))]
    need(len(central) == 1, 'unique central dihedral involution')
    z = central[0]
    configurations = []
    for h in range(1, 8):
        if table[h][h] != 0 or h == z:
            continue
        conjugates = {table[table[g][h]][inv[g]] for g in range(8)}
        pointed = double_orbits(table, [0, h], [0, h])
        need(sorted((len(o), st) for o, st in pointed) == [(2, 2), (2, 2), (4, 1)],
             'reflection inverse pointed type four invertibles plus one dimension two')
        for psi in aut:
            irrational = double_orbits(table, [0, h], [0, psi[h]])
            if psi[h] in conjugates:
                need(any(st == 2 for o, st in irrational), 'conjugate reflections create forbidden dimension t')
                continue
            need(len(irrational) == 2 and all(len(o) == 4 and st == 1 for o, st in irrational),
                 'opposite classes give exactly two dimension-2t objects')
            need({table[z][g] for g in irrational[0][0]} == set(irrational[1][0]),
                 'central rotation swaps irrational supports')
            need({0, h} != {z, table[z][h]}, 'central rotation pointed support distinct from unit')
            configurations.append({'h': h, 'psi': psi, 'orbits': irrational,
                                   'swapping_invertible_support': sorted([z, table[z][h]])})
    need(len(configurations) == 16, 'all sixteen opposite-reflection configurations')
    output = {
        'status': 'PASS', 'case': 'R7_4_2591',
        'criterion': 'twisted_v4_staged_morita_obstruction',
        'conclusion': 'no complex fusion-category categorification',
        'classification_status': 'excluded',
        'source_compressed_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'source_tensor_sha256': digest(source),
        'initial_reduction_verifier_sha256': hashlib.sha256(dependency.read_bytes()).hexdigest(),
        'initial_reduction_replay': initial,
        'character_restrictions': character_restrictions,
        'group_checks': rows,
        'dihedral_inverse_configurations': configurations,
        'categorical_scope': 'relative algebra and Morita steps proved in companion theorem; no pivotality assumption',
        'optimizer_used': False,
    }
    args.output.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'case': 'R7_4_2591', 'classification_status': 'excluded',
                      'inverse_group_systems': {r['group']: r['compatible_inverse_systems'] for r in rows},
                      'dihedral_configurations': len(configurations)}))


if __name__ == '__main__':
    main()
