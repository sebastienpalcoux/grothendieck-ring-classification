"""Independent audit of the new R65 pointed-phase cone restriction.

This does not import PointedPhaseCone or use its allowed-column/oracle code.
It imports the previously accepted unrestricted AtomicCMRealSTS cone, builds
the new allowed domain independently, and checks explicit columns exactly.
The 13 all-order relative-trace types are independently reconstructed as
cyclotomic polynomial averages, without the original Gauss-sum formula.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import itertools
import json
import math
import sys
import sympy as s

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
FRONTIER = ROOT / 'evidence/rank8_frontier_20261021'
sys.path[:0] = [str(FRONTIER / 'global_induction'), str(FRONTIER / 'quadratic')]
import streaming as st
from atomic_cm_real_sts import AtomicCMRealSTS


def need(test, message):
    if not test:
        raise AssertionError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cyclotomic_traces(order, powers=(1, 2, 3, 4)):
    """Average every primitive root over Gal(Q(zeta_lcm(5,n))/Q(sqrt5))."""
    x = s.Symbol('x')
    conductor = math.lcm(5, order)
    mod = s.Poly(s.cyclotomic_poly(conductor, x), x, domain=s.QQ)
    group = [a for a in range(conductor)
             if math.gcd(a, conductor) == 1 and a % 5 in (1, 4)]
    need(len(group) * 2 == int(s.totient(conductor)), 'quadratic fixed-field subgroup')
    sqrt5 = s.Poly(1 + 2 * x ** (conductor // 5) + 2 * x ** (4 * conductor // 5), x, domain=s.QQ).rem(mod)
    need((sqrt5 * sqrt5 - s.Poly(5, x)).rem(mod).is_zero, 'cyclotomic sqrt5 realization')
    probe = next(i for i in range(1, mod.degree()) if sqrt5.nth(i))
    rows = set()
    for primitive in range(1, order + 1):
        if math.gcd(primitive, order) != 1:
            continue
        row = []
        for power in powers:
            exponents = [(conductor // order * primitive * power * a) % conductor for a in group]
            numerator = s.Poly.from_dict({(e,): exponents.count(e) for e in set(exponents)}, x, domain=s.QQ)
            average = numerator.rem(mod).mul_ground(s.Rational(1, len(group)))
            b = average.nth(probe) / sqrt5.nth(probe)
            a = average.nth(0) - b * sqrt5.nth(0)
            need((average - sqrt5.mul_ground(b) - s.Poly(a, x)).is_zero, 'relative trace lies in Q(sqrt5)')
            row.append((Q(str(a)), Q(str(b))))
        rows.add(tuple(row))
    return rows


def independent_allowed(C, k, fourier):
    odd = k == 1
    generator_values = {0: [(1, 1, 1, 1), (-1, 1, -1, 1), (0, -1, 0, 1)],
                        1: [(0, 0, 0, 0)], 2: [(0, 0, 0, -1)]}[k]
    generator_traces = {tuple((Q(v), Q(0)) for v in values) for values in generator_values}
    square_traces = {tuple((Q(v), Q(0)) for v in values) for values in
                     ([(0, -1, 0, 1)] if odd else [(1, 1, 1, 1), (-1, 1, -1, 1)])}
    permitted = list(range(C.offset)) + list(range(C.high_end, C.nvars))
    for orbit_index, orbit in enumerate(C.orbits):
        for trace_index, trace in enumerate(C.types):
            keep = True
            for restriction_index in orbit:
                v = (0,) + tuple(C.a['high'][restriction_index][0])
                need(sum(v[i] != 0 for i in (1, 2, 7)) <= 1, 'pointed-support disjointness')
                if v[1] or v[2]:
                    keep &= tuple(trace) in generator_traces
                    if fourier:
                        keep &= v[1] + v[2] == 1 and sum(v[i] for i in (3, 4, 5, 6)) <= 11
                if v[7]:
                    keep &= tuple(trace) in square_traces
            if keep:
                permitted.append(C.offset + orbit_index * C.nt + trace_index)
    return sorted(permitted)


def main():
    source = st.load_ring('R8_3_65')
    need(st.digest(source['tensor']) == source['tensor_sha256'] ==
         'fb2d70fa36311b2092190eb1ecd5e3e82fd4ab7ff646b11aa7c7e518d261a1c4', 'canonical tensor hash')
    C = AtomicCMRealSTS(source['tensor'], 4)
    need(C.nrows == 283 and C.nvars == 6521, 'accepted parent cone dimensions')
    need(C.a['q'] == 5 and C.a['primes'] == [2, 5] and C.bound == 40, 'all-order trace inputs')
    need(C.D == (250, 110) and C.D[0] ** 2 - 5 * C.D[1] ** 2 == 2000,
         'global dimension norm and Cauchy prime support')
    # All orders 2^a 5^b outside the box a<=3,b<=1 give zero at powers<=4:
    # a>=4 leaves a 2-power >=4 in each reduced root order; b>=2 leaves
    # a 5-power >=25. Both rational Ramanujan and quadratic Gauss traces vanish.
    direct = {tuple((Q(0), Q(0)) for _ in range(4))}
    per_order = {}
    for order in (1, 2, 4, 5, 8, 10, 20, 40):
        values = cyclotomic_traces(order)
        direct |= values
        per_order[str(order)] = len(values)
    need(direct == {tuple(row) for row in C.types} and len(direct) == 13,
         'independent complete cyclotomic trace inventory differs')
    boundary = {}
    for order in (16, 25, 80, 200):
        values = cyclotomic_traces(order)
        need(values == {tuple((Q(0), Q(0)) for _ in range(4))}, 'outside-box zero trace control')
        boundary[str(order)] = 'zero tuple only'
    need(cyclotomic_traces(16) == {tuple((Q(0), Q(0)) for _ in range(4))}, 'odd-class generator phases')
    need(cyclotomic_traces(8) == {tuple((Q(v), Q(0)) for v in (0, 0, 0, -1))}, 'class-two generator phases')
    need(cyclotomic_traces(4) == {tuple((Q(v), Q(0)) for v in (0, -1, 0, 1))}, 'odd-class square phases')

    # Recheck pointed support and ν2 branch choices straight from the tensor.
    R = source['tensor']
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    choices = []
    for i in range(1, 8):
        choices.append([0] if dual[i] != i else
                       [1] if any(R[j][dual[j]][i] % 2 for j in range(8)) else [-1, 1])
    all_indicators = list(itertools.product(*choices))
    need(all_indicators == [(0, 0, 0, 0, 1, e, f) for e in (-1, 1) for f in (-1, 1)],
         'exhaustive inherited second-indicator branches')
    need(all(C.a['B'][i, j] == (8 if i == j else 0) for i in (0, 1, 2, 7) for j in (0, 1, 2, 7)),
         'pointed induction Gram block')
    need(all(not any(v[i] for i in (1, 2, 7)) for _, v, _ in C.low), 'all low columns retained legitimately')

    folder = ROOT / 'evidence/rank8_research_20261022/r65'
    receipts = []
    inputs = []
    for name, k, fourier, count in [('pointed_phase_k0_fourier.json', 0, True, 2413),
                                  ('pointed_phase_k1_fourier.json', 1, True, 1992),
                                  ('pointed_phase_k2.json', 2, False, 2222)]:
        odd = k == 1
        path = folder / name
        inputs.append(path)
        data = json.loads(path.read_text())
        need(data['tensor_sha256'] == source['tensor_sha256'], 'separator tensor binding')
        need(all(data['metadata'][key] == value for key, value in st.encode(C.meta).items()),
             'entire accepted parent cone metadata agrees')
        allowed = independent_allowed(C, k, fourier)
        need(len(allowed) == count == data['metadata']['allowed_columns'], 'allowed domain cardinality')
        need(st.digest(allowed) == data['metadata']['pointed_phase_domain_sha256'], 'allowed domain exact match')
        expected = [list(e) for e in all_indicators if e[-1] == (-1 if odd else 1)]
        need([b['indicators'] for b in data['branches']] == expected, 'complete branch coverage')
        branches = []
        columns = [C.column(i) for i in allowed]
        need(all(type(v) is int for col in columns for v in col.values()), 'all matrix entries integral')
        for branch in data['branches']:
            need(branch['status'] == 'exact_infeasible', 'branch has exclusion certificate')
            y = branch['certificate']['y']
            need(len(y) == C.nrows and all(type(v) is int for v in y), 'integral full-length separator')
            values = [sum(y[row] * v for row, v in col.items()) for col in columns]
            rhs = C.rhs_for(branch['indicators'])
            value = sum(a * b for a, b in zip(y, rhs))
            need(min(values) >= 0 and value < 0, 'independent explicit Farkas inequalities')
            need(value == branch['certificate']['bTy'], 'reported right-hand-side pairing')
            branches.append({'indicators': branch['indicators'], 'columns_checked': len(columns),
                             'minimum_column_pairing': min(values), 'zero_column_pairings': values.count(0),
                             'right_hand_side_pairing': value,
                             'separator_sha256': st.digest(y)})
        receipts.append({'certificate': path.relative_to(ROOT).as_posix(), 'allowed_columns': count,
                         'domain_sha256': st.digest(allowed), 'branches': branches})
    inputs += [folder / 'pointed_phase_cone.py', folder / 'PROOF.md',
               FRONTIER / 'quadratic/atomic_cm_real_sts.py', FRONTIER / 'global_induction/atomic_spectrum.py',
               FRONTIER / 'global_induction/streaming.py', ROOT / 'supplements/rank8/experimental_signed/higher_traces.py']
    print(json.dumps({'schema': 'independent-r65-pointed-phase-arithmetic-audit/v1', 'status': 'PASS',
        'scope': 'Independent new-domain construction, cyclotomic all-order trace inventory and exact separator replay; imports the accepted parent cone and relies on its previously proved categorical necessity.',
        'tensor_sha256': source['tensor_sha256'], 'parent_rows': C.nrows, 'parent_columns': C.nvars,
        'trace_type_count': len(direct), 'finite_representative_order_divisor_bound': 40,
        'finite_order_trace_type_counts': per_order, 'outside_box_trace_controls': boundary,
        'all_order_completeness': 'Cauchy prime support is {2,5}. At powers 1..4, orders 2^a*5^b with a>=4 or b>=2 have vanishing rational and quadratic relative trace components; the zero tuple is included.',
        'receipts': receipts,
        'source_sha256': {p.relative_to(ROOT).as_posix(): sha(p) for p in inputs},
        'verifier_sha256': sha(Path(__file__))}, indent=2))


if __name__ == '__main__':
    main()
