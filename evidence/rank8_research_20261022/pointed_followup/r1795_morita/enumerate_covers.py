"""Complete central-C2 based-ring covers of the R1795 pair quotient.

Exploratory necessary ring calculation. No categorical realization claim.
Native enumeration is replayed by exact Python identities for every result.
"""
from pathlib import Path
import hashlib
import itertools as it
import json
import subprocess
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def need(ok, msg):
    if not ok:
        raise AssertionError(msg)


def main():
    srcpath = ROOT / 'evidence/rank8_m3_20261021/pipeline/census_m3.json'
    census = {r['id']: r for r in json.loads(srcpath.read_text())}
    src = census['R8_3_1795']['tensor']
    canonical = 'feddd2934d44be4872c82ed6c5650bf9d8aac2bc87b72778d88b375726f4cd1f'
    need(hashlib.sha256(json.dumps(src, separators=(',', ':')).encode()).hexdigest() ==
         census['R8_3_1795']['tensor_sha256'] == canonical, 'canonical source tensor identity')
    need(all(src[i][j] == src[j][i] for i,j in it.product(range(8), repeat=2)), 'source commutativity')
    need(all(src[i][j][0] == int(i == j) for i,j in it.product(range(8), repeat=2)), 'source selfduality')
    pairs = [[0, 1], [2, 7], [3, 6], [4, 5]]
    need(all(src[1][i][j] == int({i,j} in [set(p) for p in pairs])
             for i,j in it.product(range(8), repeat=2)), 'source free involution orbits')
    Q = [[[sum(src[pairs[i][0]][pairs[j][0]][k] for k in pairs[l])
           for l in range(4)] for j in range(4)] for i in range(4)]
    triples = list(it.combinations_with_replacement(range(1, 4), 3))
    # Odd T122, T223, T233 transform by independent signs of bases 1,3,2.
    positive = {(1, 2, 2), (2, 2, 3), (2, 3, 3)}
    domains = [list(range(-Q[i][j][k], Q[i][j][k] + 1, 2))
               for i, j, k in triples]
    for z, t in enumerate(triples):
        if t in positive:
            domains[z] = [a for a in domains[z] if a > 0]
    # Small domains first, then shared variables for early exact pruning.
    order = sorted(range(len(triples)), key=lambda j: (len(domains[j]), triples[j]))
    triples = [triples[j] for j in order]
    domains = [domains[j] for j in order]
    xs = s.symbols('x:10')
    index = {t: j for j, t in enumerate(triples)}

    def val(i, j, k):
        if 0 in (i, j, k):
            return int((i == 0 and j == k) or (j == 0 and i == k) or (k == 0 and i == j))
        return xs[index[tuple(sorted((i, j, k)))]]

    equations = set()
    for i, j, k, l in it.product(range(4), repeat=4):
        expr = s.expand(sum(val(i, j, a) * val(a, k, l) - val(j, k, a) * val(i, a, l)
                            for a in range(4)))
        if expr == 0:
            continue
        p = s.Poly(expr, *xs)
        if p.LC() < 0:
            expr = -expr
        equations.add(expr)
    checks = [[] for _ in xs]
    for eq in sorted(equations, key=str):
        last = max(xs.index(a) for a in eq.free_symbols)
        checks[last].append(s.ccode(eq, user_functions={}))
    code = '#include <iostream>\nusing namespace std;\nint main(){\nlong long count=0;\n'
    for i, domain in enumerate(domains):
        code += 'for(long long x%d : {%s}) {\n' % (i, ','.join(str(v) + 'LL' for v in domain))
        for eq in checks[i]:
            # All variables degree at most two; explicit multiplication avoids float pow.
            for j in range(10):
                eq = eq.replace('pow(x%d, 2)' % j, '(x%d*x%d)' % (j, j))
            need('pow(' not in eq, 'native equations integral polynomial')
            code += 'if ((%s)!=0) continue;\n' % eq
    code += '++count; cout << ' + ' << "," << '.join('x%d' % j for j in range(10)) + ' << "\\n";\n'
    code += '}\n' * 10 + 'cerr << count << " solutions\\n"; return 0;\n}\n'
    cpp = HERE / 'covers_native.cpp'
    binary = HERE / 'covers_native'
    cpp.write_text(code)
    subprocess.run(['g++', '-O3', '-std=c++17', str(cpp), '-o', str(binary)], check=True)
    out = subprocess.run([str(binary)], capture_output=True, text=True, check=True)
    values = [list(map(int, line.split(','))) for line in out.stdout.splitlines()]
    records = []
    z = s.Symbol('z')
    for coeffs in values:
        T = [[[int(val(i, j, k).subs(dict(zip(xs, coeffs)))) if hasattr(val(i, j, k), 'subs') else val(i, j, k)
               for k in range(4)] for j in range(4)] for i in range(4)]
        need(all(sum(T[i][j][a] * T[a][k][l] for a in range(4)) ==
                 sum(T[j][k][a] * T[i][a][l] for a in range(4))
                 for i, j, k, l in it.product(range(4), repeat=4)), 'ordered signed associativity')
        R = [[[(Q[i // 2][j // 2][k // 2] + (-1) ** ((i+j+k) % 2) * T[i // 2][j // 2][k // 2]) // 2
               for k in range(8)] for j in range(8)] for i in range(8)]
        need(all(R[i][j][k] >= 0 for i,j,k in it.product(range(8), repeat=3)), 'nonnegative cover')
        need(all(sum(R[i][j][a] * R[a][k][l] for a in range(8)) ==
                 sum(R[j][k][a] * R[i][a][l] for a in range(8))
                 for i, j, k, l in it.product(range(8), repeat=4)), 'ordered cover associativity')
        cas = sum((s.Matrix(T[i])**2 for i in range(4)), s.zeros(4)) * 2
        fs = s.factor_list(cas.charpoly(z).as_expr())[1]
        bad = []
        for f, mult in fs:
            p = s.Poly(f, z)
            # delta has degree2 and norm3600. For every codegree f, require
            # deg(f)*v_p(3600) >= 2*v_p(norm(f)) in a common field.
            n = abs(int(p.TC()))
            if not n:
                bad.append({'polynomial': str(f), 'reason': 'zero_codegree'})
            else:
                for prime, exponent in s.factorint(n).items():
                    if p.degree() * s.factorint(3600).get(prime, 0) < 2 * exponent:
                        bad.append({'polynomial': str(f), 'prime': int(prime), 'norm_valuation': int(exponent)})
        records.append({'coefficients': coeffs, 'tensor': R, 'signed_casimir_factors':
                        [[str(f), int(m)] for f,m in fs], 'norm_obstructions': bad,
                        'multiplicity': max(v for a in R for b in a for v in b)})

    # These classifications apply only after the complete enumeration above.
    matches = []
    for recid, rec in enumerate(records):
        if rec['norm_obstructions']:
            rec['outcome'] = 'formal_codegree_norm_obstruction'
            continue
        R = rec['tensor']
        map_to_source = None
        for swap in (False, True):
            target_pairs = [pairs[0], pairs[1], pairs[3] if swap else pairs[2], pairs[2] if swap else pairs[3]]
            for mask in range(8):
                perm = [0, 1]
                for i in range(1, 4):
                    p = target_pairs[i]
                    perm.extend(p[::-1] if mask & (1 << (i-1)) else p)
                if all(R[i][j][k] == src[perm[i]][perm[j]][perm[k]] for i,j,k in it.product(range(8), repeat=3)):
                    map_to_source = perm
                    break
            if map_to_source is not None:
                break
        if map_to_source is not None:
            rec.update(outcome='source_tensor_match', permutation_to_R1795=map_to_source)
            matches.append(recid)
        elif any(f == 'z**2 - 120*z + 720' for f,m in rec['signed_casimir_factors']):
            # Every possible forgotten center object has radical coordinate in 3Z.
            dims = [(1,0),(1,0),(6,3),(6,3),(7,3),(7,3),(7,3),(7,3)]
            need(all(b % 3 == 0 for a,b in dims), 'source radical dimension lattice')
            need((60*5+5*24*2,60*2+24*5)==(540,240), 'exact D/f=(5,2) identity')
            need(2 % 3 != 0, 'central dimension not in source lattice')
            rec.update(outcome='center_dimension_lattice_obstruction',
                       formal_codegree=[60,24], forced_center_dimension=[5,2],
                       dimension_basis='1,sqrt(5)', source_radical_coefficient_divisor=3)
        else:
            sub = [0,2,4,6]
            need(all(R[i][j][k] == 0 for i,j in it.product(sub, repeat=2) for k in range(8) if k not in sub),
                 'closed rank-four subring')
            need([[[R[i][j][k] for k in sub] for j in sub] for i in sub] == Q,
                 'rank-four tensor is Q')
            need(270 > 24+12*2 and 3 < 2**2, 'rank-four FP dimension exceeds accepted bound')
            rec.update(outcome='accepted_general_rank_four_bound_obstruction',
                       subring=sub, subring_FPdim=[270,120],
                       accepted_bound='24+12sqrt(3)')
    need(len(records)==45 and len(matches)==1, 'complete cover outcome counts')
    # All possible pair dual swaps are eliminated by these odd quotient entries.
    odd_witnesses = [[1,2,Q[2][2][1]],[2,3,Q[3][3][2]],[3,2,Q[2][2][3]]]
    need(all(q % 2 == 1 for i,j,q in odd_witnesses), 'all pair dualities forced selfdual')
    dependencies = [srcpath,
        ROOT/'evidence/rank8_research_20261022/pointed_followup/R1795_pointed_associator_obstruction.json',
        ROOT/'evidence/rank8_research_20261022/pivotality/general_spherical_gates.json',
        ROOT/'manuscripts/rank4/papers/companion_sections/14_finite_certification.tex']
    pointed = json.loads(dependencies[1].read_text())
    need(pointed['id'] == 'R8_3_1795' and pointed['tensor_sha256'] == canonical,
         'pointed obstruction canonical tensor binding')
    need(pointed['record']['status'] == 'all_indicator_branches_exact_infeasible' and
         len(pointed['record']['branches']) == 8 and
         all(b['indicators'][0] == -1 for b in pointed['record']['branches']),
         'complete nontrivial pointed-associator obstruction dependency')
    gates = json.loads(dependencies[2].read_text())
    gate = next(r for r in gates if r['id'] == 'R8_3_1795')
    need(gate['tensor_sha256'] == canonical and 'pseudo-unitary Galois conjugate' in gate['conclusion'],
         'general spherical/PU-Galois gate dependency')
    outcome_counts = {name:sum(r['outcome']==name for r in records)
                      for name in sorted({r['outcome'] for r in records})}
    need(outcome_counts == {'accepted_general_rank_four_bound_obstruction':1,
                           'center_dimension_lattice_obstruction':2,
                           'formal_codegree_norm_obstruction':41,
                           'source_tensor_match':1}, 'complete expected cover outcomes')
    result = {'schema': 'r1795-forced-c2-dual-cover-enumeration/v1',
              'status': 'conditional_Grothendieck_ring_self_duality',
              'scope': 'Every hypothetical R1795 category, under the cited pointed-associator obstruction, has subgroup-algebra Morita dual with the same fusion ring. No category or categorical self-equivalence constructed.',
              'source_tensor_sha256': census['R8_3_1795']['tensor_sha256'],
              'quotient': Q, 'triples': triples, 'domains': domains,
              'normalization': 'T122,T223,T233 positive, independent three basis signs',
              'box_size': int(s.prod(len(d) for d in domains)), 'ordered_associativity_polynomials': len(equations),
              'solutions': len(records), 'norm_survivors': sum(not r['norm_obstructions'] for r in records),
              'selfdual_parity_witnesses_i_j_Qjji': odd_witnesses,
              'remaining_source_match_indices': matches,
              'outcome_counts': outcome_counts,
              'dependency_sha256': {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dependencies},
              'records': records, 'native_source_sha256': hashlib.sha256(code.encode()).hexdigest()}
    (HERE / 'covers.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','quotient','domains')}))


if __name__ == '__main__':
    main()
