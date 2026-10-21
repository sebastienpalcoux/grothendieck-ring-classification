"""Exact R439/R567 rotation tests forbidding nonunit integral center simples.

This isolated calculation retains its explicit categorical prerequisite. All
indicator branches are checked, with complete full-S low-frame coverage.
No frozen earlier proof files or receipts are modified.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'noncommutative'))
sys.path.insert(0, str(HERE.parent / 'noncommutative_followup'))
import full_rotation as full
import certified_lp as lp
import additional_central_constraints as central
c = full.c


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def setup(source):
    full.base.install()
    R = source['tensor']
    frames = central.compute(source)
    good = [r['low_index'] for r in frames['frames'] if r['complete_symmetric_S_assignments']]
    c.require(good == [2], 'Complete full-S domain must have exactly frame two')
    a = c.w.data(R)
    cols = a['lows'][2]
    L = c.s.Matrix.hstack(*map(c.s.Matrix, cols))
    high = full.base.grams.high_columns(a, L)[1]
    integral = [i for i, (v, z) in enumerate(high) if z[1] == 0]
    c.require(all(high[i][1][0].denominator == 1 and high[i][1][0] > 1 for i in integral),
              'Forbidden high dimensions must be nonunit positive integers')
    for col in cols[1:]:
        c.require(sum(col[i] * a['dimensions'][i][1] for i in range(8)) != 0,
                  'A distinguished nonunit integral central object would already exclude this frame')
    meta = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
            'height': 6, 'low_index': 2, 'full_S_domain_sha256': digest(frames),
            'high_columns': [list(v) for v, z in high],
            'forbidden_integral_indices': integral,
            'forbidden_integral_dimensions': [str(high[i][1][0]) for i in integral],
            'scope': 'conditional_on_no_nonunit_integral_dimensional_center_simple'}
    return R, a, L, meta


def system(R, a, L, indicators, meta):
    A, b, oldmeta = full.system(R, a, L, indicators, 6)
    nt = oldmeta['trace_types']
    for i in meta['forbidden_integral_indices']:
        row = [0] * len(A[0])
        row[i * nt:(i + 1) * nt] = [1] * nt
        A.append(row)
        b.append(0)
    return A, b, dict(oldmeta, no_integral_center_rows=len(meta['forbidden_integral_indices']),
                      augmented_matrix_sha256=digest(A), augmented_rhs_sha256=digest(b))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--ring', type=int, choices=(439, 567))
    args = parser.parse_args()
    rows = {r['id']: r for r in json.loads((c.OLD.parent / 'pipeline/census_m3.json').read_text())}
    prior = {r['id']: r for r in json.loads((HERE.parent / 'noncommutative_followup/additional_joint_rotation_h6.json').read_text())}
    for number in ((args.ring,) if args.ring else (439, 567)):
        ident = 'R8_3_' + str(number)
        source = rows[ident]
        R, a, L, meta = setup(source)
        path = HERE / (ident + '_h6.json')
        saved = None if args.write else json.loads(path.read_text())
        choices = list(full.h.indicator_choices(R))
        c.require([case['indicators'] for case in prior[ident]['cases']] == list(map(list, choices)),
                  'Complete earlier indicator domain')
        if saved is not None:
            c.require(saved['metadata'] == meta and [x['indicators'] for x in saved['cases']] == list(map(list, choices)),
                      'Complete source-bound current indicator domain')
        cases = []
        for index, indicators in enumerate(choices):
            A, b, system_meta = system(R, a, L, indicators, meta)
            old = prior[ident]['cases'][index]['decision']
            if args.write:
                if old['status'] == 'exact_infeasible_relaxation':
                    decision = dict(old, ray=old['ray'] + [0] * len(meta['forbidden_integral_indices']))
                else:
                    decision = lp.decide(A, b)
            else:
                c.require(saved['cases'][index]['system'] == system_meta, 'Augmented operator binding')
                decision = saved['cases'][index]['decision']
            lp.verify(A, b, decision)
            cases.append({'indicators': list(indicators), 'system': system_meta, 'decision': decision})
            print(ident, indicators, decision['status'], flush=True)
        out = {'metadata': meta, 'cases': cases,
               'conditional_exclusion': all(case['decision']['status'] == 'exact_infeasible_relaxation' for case in cases)}
        if args.write:
            path.write_text(json.dumps(out, indent=2) + '\n')
        else:
            c.require(saved == out, 'Exact complete replay differs')
        print('PASS', ident, 'conditional_exclusion', out['conditional_exclusion'], flush=True)


if __name__ == '__main__':
    main()
