"""Bounded continuous checks of the two remaining R982 integer frames.

The previous MILP infeasibility reports are not certificates.  Here any
negative result is accepted only with a checked integer bounded-Farkas
covector.  Numerical proposals are confined to explicit --write discovery.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import r982 as old
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'quadratic_atomic_integer'))
from unit_pair_constraints import append_unit_pair_constraints
from fp_fusion_bounds import tighten_fusion_bounds
import linear


def pins():
    paths = [HERE / name for name in ('r982.py', 'r982_remaining_linear.py',
        'features.py', 'bounds.py', 'equations.py', 'linear.py')]
    paths += [HERE.parent / 'quadratic_atomic_integer/unit_pair_constraints.py',
              HERE.parent / 'quadratic/fp_fusion_bounds.py',
              HERE.parent / 'quadratic/atomic_galois_balance.py']
    return {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--write', action='store_true')
    args = ap.parse_args(); source = old.st.load_ring('R8_3_982')
    C = old.cg.cone(source['tensor'], 4, 'sts_frame')
    T = old.character_table(source['tensor'], C.a)
    old.require(len(C.frames) == 4, 'complete low-frame count changed')
    path = HERE / 'R8_3_982_remaining_linear.json'
    saved = None if args.write else json.loads(path.read_text())
    records = []
    for fi in (0, 1):
        D, profile = old.filtered(C, fi)
        S = old.f.build(D, T, frame_index=fi)
        S = old.append_galois_balance(S, D, T)
        S = tighten_fusion_bounds(S, D, T)
        previous = json.loads((HERE / f'R8_3_982_frame{fi}.json').read_text())
        old.require(previous['tensor_sha256'] == source['tensor_sha256'] and
                    previous['metadata'] == S.metadata and previous['profile'] == profile,
                    'original fixed-frame integer domain differs')
        S = append_unit_pair_constraints(S, D, T)
        propagation = old.box.propagate(S)
        record = {'frame_index': fi, 'source_integer_receipt_sha256': old.st.digest(previous),
                  'metadata': S.metadata, 'box': propagation}
        if propagation['outcome'] == 'integer_box_obstruction':
            record['status'] = 'exact_source_unit_box_obstruction'
        else:
            compact = old.equations.compact(old.box.reduced(S, propagation))
            record['compact_metadata'] = compact.metadata
            print('R982 remaining bounded LP', fi, len(compact.rhs), len(compact.columns), flush=True)
            if args.write:
                result = linear.discover(compact)
            else:
                result = saved['records'][fi]['linear']
                if result['conclusion'] == 'exact_bounded_linear_obstruction':
                    linear.verify(compact, result['certificate'])
                else:
                    old.require(result['conclusion'] == 'no_exact_bounded_separator',
                                'unrecognized noncertifying numerical outcome')
            record['linear'] = result
            record['status'] = result['conclusion']
        records.append(record)
        print('PASS R982 remaining continuous check', fi, record['status'], flush=True)
    out = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
           'kind': 'fixed_frame_bounded_linear_source_unit_strengthening',
           'scope': 'pseudo_unitary_necessary_system_only',
           'numerical_infeasibility_is_not_a_certificate': True,
           'source_sha256': pins(), 'records': records}
    if args.write:
        path.write_text(json.dumps(out, separators=(',', ':')) + '\n')
    else:
        old.require(out == saved, 'remaining-frame continuous receipt differs')


if __name__ == '__main__':
    main()
