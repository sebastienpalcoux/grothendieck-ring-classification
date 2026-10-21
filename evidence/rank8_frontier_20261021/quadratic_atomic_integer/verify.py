"""Exact atomic integer screens for R1768 and R1795.

Default mode reconstructs all source-derived domains and replays exact
certificates. Numerical search is an optional proposal source in --write
mode; its failure never supplies an exclusion.
"""
from pathlib import Path
import argparse, hashlib, json, sys, time

HERE = Path(__file__).resolve().parent
FRONTIER = HERE.parent
for relative in ('global_induction', 'commutative_integer', 'quadratic'):
    sys.path.insert(0, str(FRONTIER / relative))
import streaming as st
from atomic_real_sts import AtomicRealSTS
from partial_s import RealTable
import features as f
import bounds as box
import lattice
import equations
from atomic_galois_balance import append_galois_balance
from galois_support_filter import filter_support
from fp_fusion_bounds import tighten_fusion_bounds
from proposal import propose_bounded


def digest_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources(number):
    paths = [HERE / 'verify.py', HERE / 'proposal.py']
    paths += [FRONTIER / 'commutative_integer' / name
              for name in ('features.py', 'bounds.py', 'lattice.py', 'equations.py')]
    paths += [FRONTIER / 'quadratic' / 'atomic_galois_balance.py',
              FRONTIER / 'quadratic' / 'galois_support_filter.py',
              FRONTIER / 'quadratic' / 'fp_fusion_bounds.py',
              FRONTIER / 'global_induction' / 'atomic_real_sts.py',
              FRONTIER / 'global_induction' / 'partial_s.py',
              FRONTIER / 'global_induction' / 'streaming.py',
              FRONTIER / 'global_induction' / 'complete_results' /
              f'R8_3_{number}_atomic_real_sts_h4.json']
    return {str(p.relative_to(FRONTIER)): digest_file(p) for p in paths}


def construct(number):
    source = st.load_ring(f'R8_3_{number}')
    C = AtomicRealSTS(source['tensor'], 4)
    previous = json.loads((FRONTIER / 'global_induction' / 'complete_results' /
                           f'R8_3_{number}_atomic_real_sts_h4.json').read_text())
    f.require(source['tensor_sha256'] == previous['tensor_sha256'],
              'source tensor differs from complete atomic receipt')
    f.require(C.meta == previous['metadata'], 'complete atomic domain changed')
    T = RealTable(source['tensor'], C.a)
    support = None
    if number == 1795:
        C, support = filter_support(C, T)
        print('support', number, support['outcome'], support['retained_low_columns'],
              support['retained_high_orbits'], flush=True)
        f.require(support['outcome'] == 'necessary_support_survives',
                  'support obstruction requires separate certificate packaging')
    S = f.build(C, T)
    print('integer features', number, len(S.rhs), len(S.columns), flush=True)
    S = append_galois_balance(S, C, T)
    print('Galois features', number, len(S.rhs), len(S.columns), flush=True)
    initial = S
    S = tighten_fusion_bounds(S, C, T)
    print('FP fusion bounds', number, S.metadata['FP_fusion_bounds']['tightened_variables'], flush=True)
    return source, S, support, initial


def replay_initial(number, initial):
    path = HERE / f'R8_3_{number}_initial.json'
    if not path.exists():
        return None
    result = json.loads(path.read_text())
    f.require(result['metadata'] == initial.metadata, 'initial exact system changed')
    box.verify(initial, result['box'])
    reduced = box.reduced(initial, result['box'])
    for test in result['modular']:
        lattice.verify_result(reduced, test)
    lattice.verify_hermite(reduced, result['Hermite'])
    f.require(result['proposal']['conclusion'] == 'no_exact_integer_witness_found' and
              result['proposal']['numerical_infeasibility_is_not_a_certificate'] is True,
              'initial interrupted numerical search is not a proof')
    return {'path': path.name, 'sha256': digest_file(path),
            'modular_outcomes': [x['outcome'] for x in result['modular']],
            'Hermite_outcome': result['Hermite']['outcome'],
            'proposal_conclusion': result['proposal']['conclusion']}


def run(number, write=False, seconds=180):
    started = time.monotonic()
    path = HERE / f'R8_3_{number}.json'
    source, S, support, initial = construct(number)
    initial_replay = replay_initial(number, initial)
    if write:
        result = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
                  'kind': 'atomic_integer_Gram_S_cubic_Galois_screen',
                  'scope': 'pseudo_unitary_necessary_system',
                  'source_sha256': sources(number), 'metadata': S.metadata,
                  'support': support, 'initial_stage': initial_replay}
        result['box'] = box.propagate(S)
        print('bounds', number, result['box']['outcome'],
              result['box']['fixed_variables'], result['box']['tightenings'], flush=True)
        path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
        if result['box']['outcome'] == 'integer_box_consistent':
            reduced = box.reduced(S, result['box'])
            compact = equations.compact(reduced)
            result['compression'] = compact.metadata
            print('reduced and compressed', number, len(compact.rhs), len(compact.columns), flush=True)
            result['modular'] = []
            for prime in (2, 3):
                test = lattice.modular(compact, prime)
                result['modular'].append(test)
                print('modular', number, prime, test['outcome'], test['rank'], flush=True)
                path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
                if test['outcome'] == 'modular_obstruction':
                    break
            if all(test['outcome'] == 'consistent_mod_prime' for test in result['modular']):
                result['Hermite'] = lattice.hermite(
                    compact, progress=lambda done, rank: print('HNF', number, done, rank, flush=True)
                    if done % 512 == 0 or done == len(compact.columns) else None)
                print('HNF outcome', number, result['Hermite']['outcome'], flush=True)
                path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
                if result['Hermite']['outcome'] == 'integer_lattice_member' and seconds > 0:
                    result['proposal'] = propose_bounded(compact, seconds,
                                                          lambda _, values: f.check_integer(reduced, values))
                    if result['proposal']['conclusion'] == 'exact_integer_feasible_relaxation':
                        original = box.lift(S, result['box'], result['proposal']['integer_values'])
                        f.check_integer(S, original)
                        result['integer_witness'] = original
                    print('proposal', number, result['proposal']['conclusion'], flush=True)
                    path.write_text(json.dumps(result, separators=(',', ':')) + '\n')
    else:
        result = json.loads(path.read_text())
        f.require(result['id'] == source['id'] and result['tensor_sha256'] == source['tensor_sha256'],
                  'source binding changed')
        f.require(result['source_sha256'] == sources(number), 'screen source inventory changed')
        f.require(result.get('support') == support, 'complete support filtering changed')
        f.require(result.get('initial_stage') == initial_replay, 'initial exact stage replay changed')
        f.require(result['metadata'] == S.metadata, 'complete integer system changed')
        box.verify(S, result['box'])
        if result['box']['outcome'] == 'integer_box_consistent':
            reduced = box.reduced(S, result['box'])
            compact = equations.compact(reduced)
            f.require(result['compression'] == compact.metadata, 'exact equation compression differs')
            f.require(len(result.get('modular', [])) > 0, 'modular campaign incomplete')
            for test in result['modular']:
                lattice.verify_result(compact, test)
            if 'Hermite' in result:
                lattice.verify_hermite(compact, result['Hermite'])
            if 'integer_witness' in result:
                f.check_integer(reduced, result['proposal']['integer_values'])
                f.require(box.lift(S, result['box'], result['proposal']['integer_values']) ==
                          result['integer_witness'], 'integer witness lift differs')
                f.check_integer(S, result['integer_witness'])
            if 'proposal' in result:
                proposal = result['proposal']
                f.require(proposal['numerical_infeasibility_is_not_a_certificate'] is True,
                          'numerical infeasibility incorrectly promoted')
                f.require((proposal['conclusion'] == 'exact_integer_feasible_relaxation') ==
                          ('integer_witness' in result), 'numerical outcome and exact witness disagree')
    print('PASS', source['id'], result['box']['outcome'],
          result.get('Hermite', {}).get('outcome'),
          result.get('proposal', {}).get('conclusion'),
          round(time.monotonic() - started, 3), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ring', type=int, choices=(1768, 1795), required=True)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--seconds', type=int, default=180)
    args = parser.parse_args()
    run(args.ring, args.write, args.seconds)
