#!/usr/bin/env python3
"""Independent direct tensor/gauge audit of the four new sphericality receipts.

Does not import the producer or its tensor reconstruction/enumeration routines.
The separate optimized replay supplies exhaustive enumeration and character
arithmetic; this checker verifies the finite outputs and orbit accounting.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRODUCER = ROOT / 'evidence/rank8_research_20261022/pivotality'


def need(ok, text):
    if not ok:
        raise ValueError(text)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def reconstruct(original, dual, orbits, values):
    n = len(original)
    out = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        out[0][i][i] = out[i][0][i] = 1
        out[i][dual[i]][0] = 1
    for orbit, value in zip(orbits, values):
        for i, j, k in orbit:
            out[i][j][dual[k]] = value
    return out


def validate(tensor, original, dual):
    n = len(tensor)
    for i, j, k in itertools.product(range(n), repeat=3):
        a, b = tensor[i][j][k], original[i][j][k]
        need(abs(a) <= b and (a-b) % 2 == 0, 'full parity domain')
        need(a == tensor[dual[i]][k][j] == tensor[k][dual[j]][i]
             == tensor[dual[j]][dual[i]][dual[k]], 'duality and Frobenius reciprocity')
    for i, j, k, l in itertools.product(range(n), repeat=4):
        need(sum(tensor[i][j][a] * tensor[a][k][l] for a in range(n)) ==
             sum(tensor[j][k][a] * tensor[i][a][l] for a in range(n)),
             'ordered integer associativity')
    # This is checked as a RESULT, never used to reduce the enumeration.
    return all(tensor[i][j] == tensor[j][i] for i in range(n) for j in range(n))


def run():
    census_path = ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    gate_path = PRODUCER / 'general_spherical_gates.json'
    census = {r['id']: r for r in json.loads(census_path.read_text())}
    gates = json.loads(gate_path.read_text())
    rows = []
    for gate in gates:
        original = census[gate['id']]['tensor']
        n = len(original)
        need(digest(original) == gate['tensor_sha256'], 'canonical tensor hash')
        dual = [next(j for j in range(n) if original[i][j][0] == 1) for i in range(n)]
        orbits = gate['active_trace_orbits']
        values = [tuple(v) for v in gate['signed_values']]
        need(len(values) == len(set(values)) == gate['normalized_signed_count'], 'solution multiplicity')
        signs = [(1,) + tail for tail in itertools.product((-1, 1), repeat=n-1)
                 if all(((1,) + tail)[i] == ((1,) + tail)[dual[i]] for i in range(n))]
        masks = [tuple(g[o[0][0]] * g[o[0][1]] * g[o[0][2]] for o in orbits) for g in signs]
        fixed = gate['gauge_fixed_variables']
        groups = {}
        all_commutative = True
        fs = gate['normalization'] == 'positive_second_indicator_lifts'
        for v in values:
            tensor = reconstruct(original, dual, orbits, v)
            all_commutative &= validate(tensor, original, dual)
            if fs:
                need(not fixed, 'additional gauge in FS-normalized search')
                need(all(dual[i] == i for i in range(n)), 'selfduality assumption')
                need(all((original[j][dual[j]][i] - tensor[j][dual[j]][i]) % 4 == 0
                         for i in range(n) for j in range(n)), 'FS modulo-four condition')
                representative = v
                need(tensor == original, 'FS-normalized tensor must be original')
            else:
                need(all(v[i] > 0 and v[i] % 2 for i in fixed), 'odd positive gauge')
                representative = min(tuple(x*y for x, y in zip(v, m)) for m in masks)
            groups.setdefault(representative, []).append(v)
        if not fs:
            need({tuple(m[i] for i in fixed) for m in masks} ==
                 set(itertools.product((-1, 1), repeat=len(fixed))), 'gauge surjectivity')
            expanded = sorted({tuple(x*y for x, y in zip(v, m)) for v in values for m in masks})
            need(len(expanded) == len(values) * 2**len(fixed) == gate['complete_unrestricted_count'],
                 'complete sign orbit count')
            need(digest(expanded) == gate['complete_unrestricted_values_sha256'], 'expanded tensor hash')
        recorded = {tuple(r['representative']): r for r in gate['gauge_classes']}
        need(set(recorded) == set(groups), 'complete gauge class list')
        counts = {'spherical_section': 0, 'nongauge_excluded': 0}
        obstructions = {}
        for rep, members in groups.items():
            report = recorded[rep]
            need(report['normalized_members'] == len(members), 'class member counts')
            counts[report['kind']] += 1
            tensor = reconstruct(original, dual, orbits, rep)
            if report['kind'] == 'spherical_section':
                g = report['gauge_signs']
                need(g[0] == 1 and all(x in (-1, 1) for x in g), 'gauge signs')
                need(all(g[i] == g[dual[i]] for i in range(n)), 'dual-compatible gauge')
                need(all(tensor[i][j][k] == g[i]*g[j]*g[k]*original[i][j][k]
                         for i, j, k in itertools.product(range(n), repeat=3)), 'full section identity')
            else:
                chars = report['characters']
                need(sum(len(c['factor'])-1 for c in chars) == n, 'all scalar embeddings counted')
                for c in chars:
                    kind = c['obstruction']['kind']
                    need(kind in ('zero', 'duality', 'norm'), 'unreviewed character criterion')
                    obstructions[kind] = obstructions.get(kind, 0) + 1
        need(all_commutative and counts['spherical_section'] == 1, 'scalar commutative accounting')
        need([c['factor'] for c in gate['ordinary_characters'] if c['obstruction'] is None] ==
             [gate['fp_character_factor']], 'unique ordinary FP component')
        rows.append({'id': gate['id'], 'normalized_tensors_directly_checked': len(values),
                     'ordered_associativity_identities_checked': len(values)*n**4,
                     'all_returned_tensors_commutative': all_commutative,
                     'unrestricted_tensor_count': gate['complete_unrestricted_count'],
                     'gauge_rank': len(fixed), 'class_counts': counts,
                     'nongauge_character_obstruction_counts': obstructions})
    return {'kind': 'independent_integer_tensor_and_gauge_audit', 'cases': rows,
            'scope': 'exact finite-output verification; exhaustive search and scalar arithmetic independently rerun using producer',
            'dependencies_sha256': {str(p.relative_to(ROOT)): sha(p) for p in
                                    (census_path, gate_path, PRODUCER / 'verify_general_spherical_gates.py',
                                     Path(__file__).resolve())}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = run()
    target = HERE / 'pivotality_independent_review.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(target.read_text()), 'review receipt changed')
    print('PASS: direct integer tensor identities and complete gauge accounting for four pivotality gates.')
