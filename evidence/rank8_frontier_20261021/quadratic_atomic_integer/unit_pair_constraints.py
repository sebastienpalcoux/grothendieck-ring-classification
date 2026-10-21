"""Exact source-unit multiplicity constraints for distinguished products.

Call after spectral adapters: new slack columns are integer inequalities,
not additional central restriction types.
"""
from dataclasses import replace
from pathlib import Path
import argparse, hashlib, itertools, json, sys
HERE = Path(__file__).resolve().parent
for directory in ('commutative_integer', 'global_induction', 'quadratic'):
    sys.path.insert(0, str(HERE.parent / directory))
from features import require, st, build, check_integer


def append_unit_pair_constraints(system, C, T):
    require(all(C.R[i][j] == C.R[j][i] for i in range(8) for j in range(8)),
            'unit pair adapter requires a commutative source ring')
    fp = T.characters.index(tuple(T.ds))
    labels = [E for E in range(8) if E != fp]
    du = [next(j for j in range(8) if C.R[i][j][0]) for i in range(8)]
    dual = [T.characters.index(tuple(ch[j] for j in du)) for ch in T.characters]
    require(dual == system.metadata['dual_characters'], 'dual character labels changed')
    require(all(v[0] == 0 for label in system.column_labels if label[0] == 'high_orbit'
                for v in label[2]), 'high restriction has positive source-unit multiplicity')
    frame = system.metadata['frame_index']
    norms = {E: [] for E in labels}
    fixed = {}
    if frame is None:
        for label in system.column_labels:
            if label[0] == 'low':
                E, v = label[1], label[2]
                require(v[0] == 1, 'distinguished restriction unit multiplicity is not one')
                norms[E].append(sum(n * n for n in v))
    else:
        chars = C.meta['frame_character_labels'][frame]
        vectors = [(1,) + (0,) * 7] + [C.low[j][1] for j in C.frames[frame]]
        require(chars[0] == fp, 'fixed frame unit character differs')
        for E, v in zip(chars[1:], vectors[1:]):
            require(v[0] == 1, 'fixed distinguished restriction unit multiplicity is not one')
            fixed[E] = sum(n * n for n in v)
            norms[E] = [fixed[E]]
    require(all(norms[E] for E in labels), 'missing distinguished restriction group')
    maximum = {E: max(norms[E]) for E in labels}
    lookup = {tuple(label[1:]): j for j, label in enumerate(system.column_labels)
              if label[0] == 'fusion_coefficient'}
    require(len(lookup) == 196, 'complete distinguished cubic variables required')
    rows, rhs, row_labels, slacks = [], [], [], []

    def product_row(E, F, coefficient):
        pair = tuple(sorted((E, F)))
        row = [0] * len(system.columns)
        for G in labels:
            row[lookup[pair + (G,)]] = coefficient
        return row

    for E in labels:
        row = product_row(E, dual[E], 1)
        if frame is None:
            for j, label in enumerate(system.column_labels):
                if label[0] == 'low' and label[1] == E:
                    row[j] -= sum(n * n for n in label[2])
        rows.append(row)
        rhs.append(fixed[E] - 1 if frame is not None else -1)
        row_labels.append(('distinguished_product_unit_norm', E))
    for E, F in itertools.combinations_with_replacement(labels, 2):
        if F == dual[E]:
            continue
        row = product_row(E, F, 2)
        if frame is None:
            for j, label in enumerate(system.column_labels):
                if label[0] == 'low':
                    row[j] -= (int(label[1] == E) + int(label[1] == F)) * sum(n * n for n in label[2])
        position = len(rows)
        rows.append(row)
        rhs.append(fixed[E] + fixed[F] if frame is not None else 0)
        row_labels.append(('distinguished_product_unit_AMGM', E, F))
        slacks.append((position, E, F, maximum[E] + maximum[F]))
    original_rows = len(system.rhs)
    columns = [tuple(col) + tuple(row[j] for row in rows)
               for j, col in enumerate(system.columns)]
    column_labels = list(system.column_labels)
    bounds = list(system.bounds)
    for position, E, F, upper in slacks:
        col = [0] * (original_rows + len(rows))
        col[original_rows + position] = 1
        columns.append(tuple(col))
        column_labels.append(('unit_pair_AMGM_slack', E, F))
        bounds.append(upper)
    b = tuple(system.rhs) + tuple(rhs)
    all_rows = tuple(system.row_labels) + tuple(row_labels)
    h = hashlib.sha256()
    for col in columns:
        h.update((repr(col) + '\n').encode())
    report = {'norm_equalities': len(labels), 'AMGM_inequalities': len(slacks),
              'new_integer_slacks': len(slacks), 'source_unit_multiplicity': 1,
              'high_unit_multiplicity': 0, 'maximum_low_squared_norms': maximum,
              'norm_rows_sha256': st.digest(rows[:len(labels)]),
              'all_new_rows_sha256': st.digest(rows), 'all_new_rhs_sha256': st.digest(rhs),
              'slack_records': [list(record) for record in slacks]}
    metadata = {**system.metadata, 'kind': 'integer_center_with_source_unit_product_constraints',
                'pre_unit_pair_metadata': system.metadata, 'unit_pair_constraints': st.encode(report),
                'rows': len(b), 'variables': len(columns), 'columns_sha256': h.hexdigest(),
                'rhs_sha256': st.digest(b), 'bounds_sha256': st.digest(bounds),
                'row_labels_sha256': st.digest(all_rows), 'column_labels_sha256': st.digest(column_labels)}
    return replace(system, columns=tuple(columns), rhs=b, bounds=tuple(bounds),
                   row_labels=all_rows, column_labels=tuple(column_labels), metadata=metadata)


def lift_witness(original, strengthened, values):
    check_integer(original, values)
    require(len(values) == len(original.columns), 'original witness size differs')
    result = list(values)
    offset = len(original.rhs)
    for position, E, F, upper in strengthened.metadata['unit_pair_constraints']['slack_records']:
        row = offset + position
        slack = strengthened.rhs[row] - sum(value * strengthened.columns[j][row]
                                           for j, value in enumerate(values))
        result.append(slack)
    check_integer(strengthened, result)
    return result


def control():
    from atomic_spectrum import AtomicSpectrum, table_for
    from review_cm_real_sts import fib_group
    R = fib_group(True)
    C = AtomicSpectrum(R, 4)
    T = table_for(R, C.a)
    S = build(C, T)
    actual = json.loads((HERE.parent / 'commutative_integer' / 'control.json').read_text())
    require(S.metadata == actual['metadata'], 'actual center base system changed')
    strengthened = append_unit_pair_constraints(S, C, T)
    witness = lift_witness(S, strengthened, actual['integer_witness'])
    return {'model': 'Fibonacci tensor Vec(C4)', 'actual_center_rank': 64,
            'complete_original_integer_center_retained': True,
            'metadata': strengthened.metadata, 'integer_witness': witness,
            'source_tensor_sha256': st.digest(R)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    out = st.encode(control())
    path = HERE / 'unit_pair_control.json'
    if args.write:
        path.write_text(json.dumps(out, indent=2) + '\n')
    else:
        require(out == json.loads(path.read_text()), 'unit pair control changed')
    print('PASS source-unit norm and AMGM constraints on actual64-simple center', flush=True)
