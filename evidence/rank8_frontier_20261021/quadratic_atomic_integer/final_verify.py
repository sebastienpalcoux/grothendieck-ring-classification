"""Final joint-spectrum and source-unit product campaign for R1768 and R1795.

With no arguments this is an exact, read-only replay of both final domains.
Numerical proposals occur only under --write and never certify a negative
conclusion unless their integer separator is checked on every exact column.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, math, sys, time

HERE = Path(__file__).resolve().parent
FRONTIER = HERE.parent
for name in ('global_induction', 'commutative_integer', 'quadratic'):
    sys.path.insert(0, str(FRONTIER / name))
import streaming as st
from atomic_real_sts import AtomicRealSTS
from partial_s import RealTable
import features as f
import bounds as box
import equations
import lattice
import linear
from atomic_galois_balance import append_galois_balance
from galois_support_filter import filter_support as individual_support
from joint_galois_balance import append_joint_balance, filter_support as joint_support
from fp_fusion_bounds import tighten_fusion_bounds
from integral_center import filter_integral
from unit_pair_constraints import append_unit_pair_constraints
from proposal import propose_bounded


def sources(number):
    paths = [HERE / name for name in ('final_verify.py', 'integral_center.py', 'proposal.py', 'unit_pair_constraints.py')]
    paths += [FRONTIER / 'commutative_integer' / name for name in
              ('features.py', 'bounds.py', 'equations.py', 'lattice.py', 'linear.py')]
    paths += [FRONTIER / 'quadratic' / name for name in
              ('atomic_galois_balance.py', 'galois_support_filter.py',
               'joint_galois_balance.py', 'fp_fusion_bounds.py')]
    paths += [FRONTIER / 'global_induction' / name for name in
              ('atomic_real_sts.py', 'partial_s.py', 'streaming.py')]
    paths += [FRONTIER / 'global_induction' / 'complete_results' /
              f'R8_3_{number}_atomic_real_sts_h4.json']
    return {str(p.relative_to(FRONTIER)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def construct(number):
    source = st.load_ring(f'R8_3_{number}')
    C = AtomicRealSTS(source['tensor'], 4)
    old = json.loads((FRONTIER / 'global_induction' / 'complete_results' /
                      f'R8_3_{number}_atomic_real_sts_h4.json').read_text())
    f.require(old['tensor_sha256'] == source['tensor_sha256'] and C.meta == old['metadata'],
              'complete original atomic domain changed')
    T = RealTable(source['tensor'], C.a)
    C, integral = filter_integral(C, T)
    C, individual = individual_support(C, T)
    f.require(individual['outcome'] == 'necessary_support_survives',
              'individual support obstruction needs separate result handling')
    C, joint = joint_support(C, T)
    reports = {'integral_center': integral, 'individual_support': individual,
               'joint_support': joint}
    print('joint support', number, joint['outcome'], joint['retained_low'],
          joint['retained_high_orbits'], flush=True)
    if joint['outcome'] != 'joint_support_survives':
        return source, None, reports
    S = f.build(C, T)
    S = append_galois_balance(S, C, T)
    S = append_joint_balance(S, C, T)
    S = tighten_fusion_bounds(S, C, T)
    S = append_unit_pair_constraints(S, C, T)
    print('joint integer system', number, len(S.rhs), len(S.columns), flush=True)
    return source, S, reports


def lift_bounded(original, compact, certificate):
    values = [Q(0)] * len(original.rhs)
    for y, (row, scale) in zip(certificate['covector'], compact.metadata['representatives']):
        values[row] += Q(y, scale)
    denominator = math.lcm(*(value.denominator for value in values))
    y = [int(value * denominator) for value in values]
    products = [sum(a * b for a, b in zip(y, col)) for col in original.columns]
    result = {'kind': 'exact_bounded_linear_separator', 'covector': y,
              'rhs_value': sum(a * b for a, b in zip(y, original.rhs)),
              'box_upper': sum(max(0, value) * bound for value, bound in zip(products, original.bounds))}
    linear.verify(original, result)
    return result


def run(number, write=False, seconds=180):
    started = time.monotonic()
    path = HERE / f'R8_3_{number}_final.json'
    source, S, reports = construct(number)
    if write:
        out = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
               'kind': 'final_joint_spectral_integer_Gram_S_cubic_source_unit_campaign',
               'scope': 'pseudo_unitary_necessary_system', 'source_sha256': sources(number),
               'reports': reports, 'status': 'joint_support_obstruction' if S is None else 'in_progress'}
        def save():
            path.write_text(json.dumps(out, separators=(',', ':')) + '\n')
        save()
        if S is not None:
            out['metadata'] = S.metadata
            out['box'] = box.propagate(S)
            print('joint bounds', number, out['box']['outcome'], out['box']['fixed_variables'], flush=True)
            if out['box']['outcome'] == 'integer_box_obstruction':
                out['status'] = 'exact_integer_box_obstruction'
            else:
                reduced = box.reduced(S, out['box'])
                compact = equations.compact(reduced)
                out['compression'] = compact.metadata
                print('joint reduced', number, len(compact.rhs), len(compact.columns), flush=True)
                out['linear'] = linear.discover(compact)
                if out['linear']['conclusion'] == 'exact_bounded_linear_obstruction':
                    out['full_reduced_linear_separator'] = lift_bounded(reduced, compact, out['linear']['certificate'])
                    out['status'] = 'exact_bounded_linear_obstruction'
                else:
                    out['modular'] = []
                    for prime in (2, 3):
                        test = lattice.modular(compact, prime)
                        out['modular'].append(test)
                        print('joint modular', number, prime, test['outcome'], test['rank'], flush=True)
                        if test['outcome'] == 'modular_obstruction':
                            out['status'] = 'exact_modular_obstruction'
                            break
                    save()
                    if out['status'] == 'in_progress':
                        out['Hermite_batch_size'] = 512 if number == 1795 else 64
                        out['Hermite'] = lattice.hermite(compact, batch=out['Hermite_batch_size'], progress=lambda done, rank:
                            print('joint HNF', number, done, rank, flush=True)
                            if done % 512 == 0 or done == len(compact.columns) else None)
                        if out['Hermite']['outcome'] == 'integer_lattice_obstruction':
                            out['status'] = 'exact_integer_lattice_obstruction'
                        else:
                            out['status'] = 'integer_lattice_member_no_bounded_witness'
                            save()
                            if seconds > 0:
                                out['proposal'] = propose_bounded(compact, seconds,
                                    lambda _, values: f.check_integer(reduced, values))
                                if out['proposal']['conclusion'] == 'exact_integer_feasible_relaxation':
                                    original = box.lift(S, out['box'], out['proposal']['integer_values'])
                                    f.check_integer(S, original)
                                    out['integer_witness'] = original
                                    out['status'] = 'exact_bounded_integer_feasible_relaxation'
            save()
    else:
        out = json.loads(path.read_text())
        f.require(out['id'] == source['id'] and out['tensor_sha256'] == source['tensor_sha256'],
                  'source identity changed')
        f.require(out['source_sha256'] == sources(number), 'joint campaign source inventory changed')
        f.require(out['reports'] == reports, 'complete support reports differ')
        if S is None:
            f.require(out['status'] == 'joint_support_obstruction', 'support conclusion differs')
        else:
            f.require(out['metadata'] == S.metadata, 'joint integer matrix changed')
            box.verify(S, out['box'])
            if out['box']['outcome'] == 'integer_box_obstruction':
                f.require(out['status'] == 'exact_integer_box_obstruction', 'box conclusion differs')
            else:
                reduced = box.reduced(S, out['box'])
                compact = equations.compact(reduced)
                f.require(out['compression'] == compact.metadata, 'joint compression changed')
                if out['linear']['conclusion'] == 'exact_bounded_linear_obstruction':
                    linear.verify(compact, out['linear']['certificate'])
                    linear.verify(reduced, out['full_reduced_linear_separator'])
                    f.require(out['status'] == 'exact_bounded_linear_obstruction', 'linear conclusion differs')
                else:
                    f.require(out['linear']['conclusion'] == 'no_exact_bounded_separator',
                              'unrecognized numerical linear outcome')
                    for test in out['modular']:
                        lattice.verify_result(compact, test)
                    if any(test['outcome'] == 'modular_obstruction' for test in out['modular']):
                        f.require(out['status'] == 'exact_modular_obstruction', 'modular conclusion differs')
                    else:
                        f.require([test['prime'] for test in out['modular']] == [2, 3],
                                  'planned modular tests incomplete')
                        if out['Hermite']['outcome'] == 'integer_lattice_obstruction':
                            lattice.verify_separator(compact, out['Hermite']['certificate'])
                        else:
                            batch = 512 if number == 1795 else 64
                            f.require(out.get('Hermite_batch_size', 64) == batch,
                                      'Hermite batch policy differs')
                            f.require(lattice.hermite(compact, batch=batch) == out['Hermite'],
                                      'exact final Hermite reconstruction differs')
                        if out['Hermite']['outcome'] == 'integer_lattice_obstruction':
                            f.require(out['status'] == 'exact_integer_lattice_obstruction', 'lattice conclusion differs')
                        elif 'integer_witness' in out:
                            f.check_integer(reduced, out['proposal']['integer_values'])
                            f.require(box.lift(S, out['box'], out['proposal']['integer_values']) == out['integer_witness'],
                                      'integer witness lift changed')
                            f.check_integer(S, out['integer_witness'])
                            f.require(out['status'] == 'exact_bounded_integer_feasible_relaxation', 'witness status differs')
                        else:
                            f.require(out['status'] == 'integer_lattice_member_no_bounded_witness',
                                      'lattice membership is not a bounded solution')
                        if 'proposal' in out:
                            f.require(out['proposal']['numerical_infeasibility_is_not_a_certificate'] is True,
                                      'numerical status is not an exclusion')
                            f.require((out['proposal']['conclusion'] == 'exact_integer_feasible_relaxation') ==
                                      ('integer_witness' in out), 'proposal and exact witness differ')
    print('PASS joint campaign', source['id'], out['status'],
          round(time.monotonic() - started, 3), flush=True)
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ring', type=int, choices=(1768, 1795))
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--seconds', type=int, default=180)
    args = parser.parse_args()
    for number in ([args.ring] if args.ring else (1768, 1795)):
        run(number, args.write, args.seconds)
