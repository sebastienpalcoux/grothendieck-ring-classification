"""Exact bounded rational primals for R982 fixed frames zero and one.

These certify only the continuous relaxation of the integer center system.
The optional floating solver proposes a support; saved replay uses rational
arithmetic only and checks every original equation and finite bound.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, json, sys
import r982 as old
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'quadratic_atomic_integer'))
from unit_pair_constraints import append_unit_pair_constraints
from fp_fusion_bounds import tighten_fusion_bounds


def check(S, values):
    old.require(len(values) == len(S.columns), 'bounded primal length differs')
    x = list(map(Q, values))
    old.require(all(0 <= a <= u for a, u in zip(x, S.bounds)), 'bounded primal violates box')
    total = [Q(0)] * len(S.rhs)
    for a, col in zip(x, S.columns):
        if a:
            for i, c in enumerate(col):
                if c: total[i] += a * c
    old.require(total == list(S.rhs), 'bounded rational primal fails an exact equation')
    return x


def propose(S):
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import csc_matrix
    scales = [max(1, abs(b), max(abs(col[i]) for col in S.columns))
              for i, b in enumerate(S.rhs)]
    A = csc_matrix(np.array([[float(a / scales[i]) for i, a in enumerate(col)]
                            for col in S.columns]).T)
    result = linprog(np.zeros(len(S.columns)), A_eq=A,
        b_eq=np.array([float(b / d) for b, d in zip(S.rhs, scales)]),
        bounds=[(0, u) for u in S.bounds], method='highs')
    old.require(result.success, 'continuous solver did not propose a feasible point')
    for threshold in (1e-7, 1e-9, 1e-11, 0.):
        fixed = {j: (0 if abs(v) <= threshold else u)
                 for j, (v, u) in enumerate(zip(result.x, S.bounds))
                 if abs(v) <= threshold or abs(v - u) <= threshold}
        free = [j for j in range(len(S.columns)) if j not in fixed]
        rhs = [b - sum(S.columns[j][i] * v for j, v in fixed.items())
               for i, b in enumerate(S.rhs)]
        M = old.s.Matrix([[S.columns[j][i] for j in free] for i in range(len(S.rhs))])
        try:
            solution, parameters, free_parameters = M.gauss_jordan_solve(old.s.Matrix(rhs), freevar=True)
        except ValueError:
            continue
        for denominator in (1000, 1000000, 1000000000):
            substitutions = {parameters[k, 0]: old.s.Rational(
                Q(float(result.x[free[j]])).limit_denominator(denominator))
                for k, j in enumerate(free_parameters)}
            values = [Q(0)] * len(S.columns)
            for j, v in fixed.items(): values[j] = Q(v)
            for j, value in zip(free, solution.subs(substitutions)):
                values[j] = Q(int(value.p), int(value.q))
            try:
                check(S, values)
            except Exception:
                continue
            return values
    raise RuntimeError('no exact bounded primal reconstructed; numerical status is not a certificate')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    args = ap.parse_args(); source = old.st.load_ring('R8_3_982')
    C = old.cg.cone(source['tensor'], 4, 'sts_frame')
    T = old.character_table(source['tensor'], C.a)
    reference = json.loads((HERE / 'R8_3_982_remaining_linear.json').read_text())
    old.require(reference['tensor_sha256'] == source['tensor_sha256'], 'continuous reference source differs')
    path = HERE / 'R8_3_982_rational.json'
    saved = None if args.write else json.loads(path.read_text())
    records = []
    for fi in (0, 1):
        D, _ = old.filtered(C, fi)
        S = old.f.build(D, T, frame_index=fi)
        S = old.append_galois_balance(S, D, T)
        S = tighten_fusion_bounds(S, D, T)
        S = append_unit_pair_constraints(S, D, T)
        ref = reference['records'][fi]
        old.require(S.metadata == ref['metadata'], 'strengthened fixed-frame domain differs')
        compact = old.equations.compact(old.box.reduced(S, ref['box']))
        old.require(compact.metadata == ref['compact_metadata'], 'reduced continuous domain differs')
        values = propose(compact) if args.write else list(map(Q, saved['records'][fi]['reduced_values']))
        check(compact, values)
        lower, upper = ref['box']['lower_bounds'], ref['box']['upper_bounds']
        original = list(map(Q, lower)); iterator = iter(values)
        for j, (a, b) in enumerate(zip(lower, upper)):
            if a != b: original[j] += next(iterator)
        old.require(next(iterator, None) is None, 'reduced primal lift has extra coordinates')
        check(S, original)
        records.append({'frame_index': fi, 'metadata': S.metadata,
            'compact_metadata': compact.metadata, 'status': 'exact_bounded_rational_feasible_relaxation',
            'reduced_values': list(map(str, values)), 'original_values': list(map(str, original))})
        print('PASS R982 exact bounded rational primal', fi, len(values), flush=True)
    out = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
           'scope': 'continuous_relaxation_only_not_nonnegative_integer_center_or_model',
           'reference_sha256': old.st.digest(reference),
           'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'records': records}
    if args.write:
        path.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    else:
        old.require(saved == out, 'bounded rational primal receipt differs')


if __name__ == '__main__':
    main()
