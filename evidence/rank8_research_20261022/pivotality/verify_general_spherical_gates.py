#!/usr/bin/env python3
"""Replay four complete general-to-spherical/Galois-PU reductions.

R982/R1768/R1795: full parity domains modulo a proved basis-sign gauge.
R3472: positive-second-indicator lifts, with NO additional sign gauge.
See PROOF.md for the categorical justification of both normalizations.
Requires Python 3, SymPy, and g++; no Sage, numerical solver, or network.
"""
from pathlib import Path
import argparse, hashlib, itertools, json, re, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'evidence/rank8_m3_20261021/noncommutative'))
import scalar_sieve as exact
from oriented_signed import problem

IDS = ('R8_3_982', 'R8_3_1768', 'R8_3_1795', 'R8_3_3472')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def gauge_data(R, p):
    n = len(R)
    du = exact.dual(R)
    signs = [(1,) + tail for tail in itertools.product((-1, 1), repeat=n-1)
             if all(((1,) + tail)[i] == ((1,) + tail)[du[i]] for i in range(n))]
    masks = [tuple(g[a] * g[b] * g[c] for orb in p['active'] for a, b, c in [orb[0]])
             for g in signs]
    return signs, masks


def enumerate_complete(R, indicator_normalized):
    p = problem(R)
    du = exact.dual(R)
    full_domains = [list(range(-R[a][b][du[c]], R[a][b][du[c]] + 1, 2))
                    for orb in p['active'] for a, b, c in [orb[0]]]
    signs, masks = gauge_data(R, p)
    fixed = []
    if indicator_normalized:
        need(all(i == du[i] for i in range(len(R))), 'FS normalization used on nonselfdual ring')
        # Reconstruct the entire mod-four restriction independently.
        domains = [list(d) for d in full_domains]
        for i in range(1, len(R)):
            for j in range(1, len(R)):
                b = R[j][du[j]][i]
                if b:
                    v = p['mapping'][j, du[j], i]
                    domains[v] = [x for x in domains[v] if (b-x) % 4 == 0]
        need(domains == p['domains'], 'FS-positive domains differ')
    else:
        # Erase EVERY indicator restriction before imposing a pure sign gauge.
        domains = [list(d) for d in full_domains]
        pairs = sorted({min(i, du[i]) for i in range(1, len(R))})
        coordinate = {i: pairs.index(min(i, du[i])) for i in range(1, len(R))}
        vectors = []
        for orb in p['active']:
            vector = 0
            for i in orb[0]:
                vector ^= 1 << coordinate[i]
            vectors.append(vector)
        basis = {}
        for var in p['order']:
            if domains[var][0] % 2 == 0:
                continue
            vector = vectors[var]
            while vector:
                pivot = vector.bit_length()-1
                if pivot in basis:
                    vector ^= basis[pivot]
                else:
                    basis[pivot] = vector
                    fixed.append(var)
                    break
        # Explicitly certify simultaneous gauge accessibility of all sign patterns.
        patterns = {tuple(mask[i] for i in fixed) for mask in masks}
        need(patterns == set(itertools.product((-1, 1), repeat=len(fixed))),
             'selected sign coordinates are not independent')
        need(all(0 not in domains[i] for i in fixed), 'zero variable used to fix sign')
        for var in fixed:
            domains[var] = [x for x in domains[var] if x > 0]

    # Retain all ordered associativity equations; replace domains only.
    pattern = r'case (\d+):for\(int x:vector<int>\{([^}]*)\}\)\{v\[(\d+)\]=x;'
    def replacement(match):
        level, var = int(match[1]), int(match[3])
        need(p['order'][level] == var, 'native variable order')
        need([int(x) for x in match[2].split(',') if x] == p['domains'][var],
             'native original domains mismatch')
        need(max(map(abs, domains[var])) <= max(map(abs, p['domains'][var])),
             'native arithmetic bound expanded')
        return ('case ' + str(level) + ':for(int x:vector<int>{' +
                ','.join(map(str, domains[var])) + '}){v[' + str(var) + ']=x;')
    cpp, count = re.subn(pattern, replacement, p['source'])
    need(count == len(domains), 'not every native domain replaced')
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / 'enum.cpp'
        executable = Path(directory) / 'enum'
        source.write_text(cpp)
        subprocess.run(['g++', '-O3', '-std=c++17', str(source), '-o', str(executable)],
                       check=True, capture_output=True)
        result = subprocess.run([str(executable)], check=True, capture_output=True,
                                text=True, timeout=600)
    values = sorted(tuple(map(int, line.split())) for line in result.stdout.splitlines())
    need(len(values) == len(set(values)), 'duplicate signed solution')
    need(all(len(v) == len(domains) and all(x in d for x, d in zip(v, domains))
             for v in values), 'signed solution outside domains')
    p['domains'] = domains
    return values, p, masks, fixed, result.stderr.strip()


def character_report(R, required):
    # SymPy Poly equality includes its coefficient domain; use QQ uniformly
    # when comparing a stored norm polynomial with a freshly factored one.
    required = [(exact.s.Poly(f, exact.t, domain=exact.s.QQ), m) for f, m in required]
    a = exact.ScalarCharacters(R)
    concise = exact.character_obstructions(R, required)
    reports = []
    for (f, multiplicity), record in zip(a.components, concise):
        need(multiplicity == 1, 'nonseparable scalar component')
        K, ds, D, pD = a.component(f)
        need(exact.pc(f) == record['factor'], 'scalar component order')
        obstruction = record['obstruction']
        if obstruction and obstruction['kind'] == 'norm':
            exact.proofs.check_norm(pD, required, obstruction)
        reports.append(dict(record, global_dimension_polynomial=exact.pc(pD),
                            dimension_coordinates=[exact.ec(d) for d in ds]))
    return reports


def compute(source):
    rid = source['id']
    R = source['tensor']
    need(digest(R) == source['tensor_sha256'], rid + ': source tensor hash')
    exact.validate_general(R, nonnegative=True)
    indicator = rid == 'R8_3_3472'
    values, p, masks, fixed, statistics = enumerate_complete(R, indicator)
    print(rid, statistics, flush=True)
    original = exact.ScalarCharacters(R)
    need(original.scalar_rank == len(R), 'original ring not commutative semisimple')
    ordinary = character_report(R, original.cf)
    fp_factor = exact.pc(original.fp()[0])
    need([c['factor'] for c in ordinary if c['obstruction'] is None] == [fp_factor],
         rid + ': FP Galois orbit not unique ordinary survivor')

    groups = {}
    for v in values:
        exact.validate_general(exact.from_values(R, p, v))
        representative = v if indicator else min(tuple(x*y for x, y in zip(v, mask)) for mask in masks)
        groups.setdefault(representative, []).append(v)
    reports = []
    for representative, members in sorted(groups.items()):
        T = exact.from_values(R, p, representative)
        exact.validate_general(T)
        gauge = exact.proofs.gauge_original(T, R)
        if gauge is not None:
            need(all(T[i][j][k] == gauge[i]*gauge[j]*gauge[k]*R[i][j][k]
                     for i in range(8) for j in range(8) for k in range(8)), 'full gauge identity')
            report = {'kind': 'spherical_section', 'gauge_signs': gauge}
        else:
            signed = exact.ScalarCharacters(T)
            need(signed.scalar_rank == len(R), 'signed sector not commutative semisimple')
            characters = character_report(T, original.cf + signed.cf)
            need(all(c['obstruction'] and c['obstruction']['kind'] in ('zero', 'duality', 'norm')
                     for c in characters), rid + ': nongauge scalar survivor')
            report = {'kind': 'nongauge_excluded', 'characters': characters,
                      'signed_formal_codegree_factors': [exact.pc(f) for f, m in signed.cf]}
        reports.append({'representative': list(representative), 'normalized_members': len(members), **report})
    need(sum(r['kind'] == 'spherical_section' for r in reports) == 1,
         'unique original sign class not verified')
    if indicator:
        need(len(values) == 1 and exact.from_values(R, p, values[0]) == R,
             'FS-normalized result not exactly original tensor')
        expanded = None
    else:
        expanded = sorted({tuple(x*y for x, y in zip(v, mask)) for v in values for mask in masks})
        need(len(expanded) == len(values)*2**len(fixed), 'gauge transversal count')
    return {'id': rid, 'tensor_sha256': source['tensor_sha256'],
            'normalization': 'positive_second_indicator_lifts' if indicator else 'full_parity_modulo_basis_signs',
            'commutativity_assumed_for_signed_enumeration': False,
            'signed_variables': len(p['active']), 'active_trace_orbits': p['active'],
            'domains': p['domains'], 'gauge_fixed_variables': fixed,
            'normalized_signed_count': len(values), 'native_statistics': statistics,
            'signed_values': values,
            'complete_unrestricted_count': None if expanded is None else len(expanded),
            'complete_unrestricted_values_sha256': None if expanded is None else digest(expanded),
            'gauge_classes': reports,
            'original_formal_codegree_factors': [exact.pc(f) for f, m in original.cf],
            'ordinary_characters': ordinary, 'fp_character_factor': fp_factor,
            'conclusion': 'every categorification is spherical and has a pseudo-unitary Galois conjugate; no existence or general unbraided exclusion asserted'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--ring', choices=IDS)
    args = parser.parse_args()
    census = {r['id']: r for r in json.loads((ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
    ids = (args.ring,) if args.ring else IDS
    output = [compute(census[rid]) for rid in ids]
    # Round-trip tuples before exact comparison with the portable receipt.
    output = json.loads(json.dumps(output))
    path = HERE / 'general_spherical_gates.json'
    if args.write:
        need(args.ring is None, '--write requires the complete four-case record')
        path.write_text(json.dumps(output, indent=2) + '\n')
    else:
        recorded = {r['id']: r for r in json.loads(path.read_text())}
        need(output == [recorded[rid] for rid in ids], 'regenerated complete gate record differs')
    print('PASS: complete general-to-spherical and Galois-PU gates:', ', '.join(ids))
