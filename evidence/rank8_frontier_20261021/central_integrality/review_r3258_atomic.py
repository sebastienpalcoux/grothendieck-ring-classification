"""Independent quadratic coefficients and full-domain R3258 ray audit.

The complete original restriction/phase domains and reconstructed characters
are imported from the reviewed producer. Every field operation thereafter,
partial-S filter, labeled low domain, operator column, RHS and ray pairing is
recomputed here. No producer column or factorized oracle supplies a coefficient;
column equality is checked only after the independent reconstruction.
The canonical producer replay separately verifies the general signed lift.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
import argparse
import hashlib
import itertools
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'global_induction'))
import atomic_generation as driver
from atomic_real_sts import AtomicRealSTS
from partial_s import RealTable
st = driver.cg.st
ZERO = (Q(0), Q(0))
ONE = (Q(1), Q(0))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def scale(x, n):
    return x[0] * n, x[1] * n


def mul(x, y):
    return x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def divide(x, y):
    norm = y[0] ** 2 - 5 * y[1] ** 2
    need(norm != 0, 'Nonzero quadratic denominator')
    return scale(mul(x, (y[0], -y[1])), 1 / norm)


def total(xs):
    out = ZERO
    for x in xs:
        out = add(out, x)
    return out


def integral(x):
    return (2 * x[0]).denominator == 1 and (x[0] ** 2 - 5 * x[1] ** 2).denominator == 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    source = st.load_ring('R8_3_3258')
    path = st.HERE / 'atomic_results/R8_3_3258_h4.json'
    saved = json.loads(path.read_text())
    need(saved['tensor_sha256'] == source['tensor_sha256'] == st.digest(source['tensor']), 'Tensor identity')
    need(saved['status'] == 'excluded' and saved['scope'] == 'general_complex_fusion_category', 'General target')
    pseudo = saved['certificate']['general']['sphere']['pseudo']
    need(pseudo == saved['pseudo_certificate'], 'Pseudo certificate is the actual general-lift premise')
    R = source['tensor']
    a = st.old.setup(R)
    need(a['width'] == 2 and a['q'] == 5, 'Exact quadratic adapter scope')
    T = RealTable(R, a)
    C = AtomicRealSTS(R, 4)
    need(C.meta == pseudo['metadata'] == saved['metadata'], 'Complete domain identity')
    chars = [tuple(T.coordinates(x) for x in row) for row in T.characters]
    ds = tuple(tuple(map(Q, d)) for d in a['dimensions'])
    D = total(mul(d, d) for d in ds)
    need(len(set(chars)) == 8 and ds in chars, 'Complete distinct dimension characters')
    du = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    need(du == list(range(8)), 'Self-dual source')
    for ch in chars:
        need(ch[0] == ONE, 'Unital character')
        for i, j in itertools.product(range(8), repeat=2):
            need(mul(ch[i], ch[j]) == total(scale(ch[k], R[i][j][k]) for k in range(8)), 'Independent character multiplication')
    fs = [total(mul(ch[i], ch[du[i]]) for i in range(8)) for ch in chars]
    for E, F in itertools.product(range(8), repeat=2):
        need(total(mul(chars[E][i], chars[F][du[i]]) for i in range(8)) == (fs[E] if E == F else ZERO), 'Independent orthogonality')
    beta = [divide(D, f) for f in fs]
    fp = chars.index(ds)
    labels = [E for E in range(8) if E != fp]
    need(labels == C.meta['low_character_labels'], 'Complete low character labels')

    @lru_cache(None)
    def evaluate(v):
        return tuple(total(scale(x, n) for x, n in zip(ch, v)) for ch in chars)

    def dimension(v):
        return total(scale(x, n) for x, n in zip(ds, v))

    def allowed(v):
        dim = dimension(v)
        return all(integral(divide(mul(be, value), dim)) for be, value in zip(beta, evaluate(v)))

    original_low = sorted(set(tuple(v) for cs in a['columns'] for v in cs))
    need(all(allowed(v) for v in original_low), 'No rejected low column')
    kept_high = [(v, z) for v, z in a['high'] if allowed((0,) + tuple(v))]
    need(kept_high == C.a['high'], 'Independent full high integrality filter')
    low = [(g, v, dimension(v)) for g, E in enumerate(labels)
           for v in original_low if dimension(v) == beta[E]]
    need(low == C.low, 'Every allowed labeled low atom, with exact order')
    # Independent Casimir matrix and tensor powers, using only the source tensor.
    B = [[sum(R[k][i][p] * R[du[k]][p][j] for k in range(8) for p in range(8))
          for j in range(8)] for i in range(8)]
    need(B == a['B'].tolist(), 'Induction Gram is the source Casimir')
    powers = {}
    for obj in range(1, 8):
        pp = [[int(i == 0) for i in range(8)]]
        for order in range(1, 5):
            pp.append([sum(pp[-1][i] * R[i][obj][j] for i in range(8)) for j in range(8)])
        powers[obj] = pp
    auxiliary = []
    for obj in range(1, 8):
        for order in (3, 4):
            divisors = [r for r in range(1, order) if order % r == 0]
            for tt in a['rotations'](order, divisors):
                auxiliary.append((obj, order, dict(zip(divisors, tt))))
    need(C.nvars == len(low) + len(C.orbits) * len(C.types) + len(auxiliary), 'Complete column partition')
    # Odd multiplicity in X_j X_j^* forces positive second indicator.
    witnesses = [next(j for j in range(8) if R[j][du[j]][i] % 2) for i in range(1, 8)]
    need([case['indicators'] for case in pseudo['cases']] == [[1] * 7], 'Complete forced-indicator coverage')
    ray = pseudo['cases'][0]['y']
    need(len(ray) == len(C.rows) and all(type(v) is int for v in ray), 'Complete integral ray')

    def rhs(label):
        kind = label[0]
        if kind == 'simplex':
            return Q(1)
        if kind == 'gram':
            i, j = label[1:]
            return Q(B[i][j] - int(i == j == 0))
        if kind == 'moment':
            power, i, k = label[1:]
            return D[k] if power == 2 else Q(0)
        if kind == 'rotation_sum':
            obj, order = label[1:]
            return Q(powers[obj][order][0])
        if kind == 'rotation':
            obj, order, r, k = label[1:]
            return Q(powers[obj][r][0] if k == 0 else 0)
        if kind == 'atomic_S_symmetry':
            return Q(0)
        if kind == 'atomic_STS':
            E, F, k = label[1:]
            return add(fs[F] if F == fp else ZERO, (-Q(1), Q(0)))[k]
        raise ValueError('Unrecognized row')

    b = []
    for label, factor in zip(C.rows, C.scales):
        v = rhs(label) * factor
        need(v.denominator == 1, 'Integral independently reconstructed RHS')
        b.append(int(v))
    need(b == C.rhs_for([1] * 7), 'Every RHS coefficient agrees')

    def column(index):
        is_low = index < len(low)
        is_high = len(low) <= index < C.high_end
        if is_low:
            group, v, z = low[index]
            G = labels[group]
            vectors = [v]
            cv = evaluate(v)
        elif is_high:
            oi, ti = divmod(index - len(low), len(C.types))
            vectors = [(0,) + tuple(kept_high[j][0]) for j in C.orbits[oi]]
            z = dimension(vectors[0])
            need(all(dimension(v) == z for v in vectors), 'Equal dual dimensions')
            vv = [evaluate(v) for v in vectors]
            traces = C.types[ti]
        else:
            obj0, order0, tt = auxiliary[index - C.high_end]
        out = {}
        for row, (label, factor) in enumerate(zip(C.rows, C.scales)):
            kind = label[0]
            co = Q(0)
            if kind == 'simplex':
                if is_low:
                    co = Q(group == label[1])
            elif kind == 'gram' and (is_low or is_high):
                i, j = label[1:]
                co = Q(sum(v[i] * v[j] for v in vectors))
            elif kind == 'moment' and (is_low or is_high):
                power, i, k = label[1:]
                co = sum(v[i] for v in vectors) * (z if is_low else mul(z, traces[power - 1]))[k]
            elif kind == 'rotation_sum' and not (is_low or is_high):
                co = Q((obj0, order0) == label[1:])
            elif kind == 'rotation':
                obj, order, r, k = label[1:]
                if is_low or is_high:
                    count = sum(powers[obj][r][i] * v[i] for v in vectors for i in range(8))
                    co = -count * (z if is_low else mul(z, traces[order // r - 1]))[k]
                elif (obj, order) == (obj0, order0):
                    co = mul(D, tt[r])[k]
            elif kind == 'atomic_S_symmetry' and is_low:
                E, F, k = label[1:]
                co = add(mul(beta[E], cv[E]) if G == F else ZERO,
                         scale(mul(beta[F], cv[F]), -1) if G == E else ZERO)[k]
            elif kind == 'atomic_STS':
                E, F, k = label[1:]
                if is_low:
                    co = add(mul(cv[E], cv[F]), scale(mul(fs[F], cv[E]), -1) if G == F else ZERO)[k]
                elif is_high:
                    co = mul(total(mul(ch[E], ch[F]) for ch in vv), traces[0])[k]
            co *= factor
            need(co.denominator == 1, 'Integral independent operator coefficient')
            if co:
                out[row] = int(co)
        return out

    pairings = []
    for index in range(C.nvars):
        col = column(index)
        need(col == C.column(index), 'Independent full coefficient reconstruction differs at ' + str(index))
        value = sum(ray[row] * coefficient for row, coefficient in col.items())
        need(value >= 0, 'Independent column violates exact separator')
        pairings.append(value)
    bty = sum(v * y for v, y in zip(b, ray))
    need(bty == pseudo['cases'][0]['bTy'] < 0, 'Independent strict RHS separation')
    result = {'id': source['id'], 'tensor_sha256': source['tensor_sha256'],
              'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'status': 'PASS', 'scope': 'Independent quadratic arithmetic, filtering, labeled domain, full operator and ray audit',
              'character_count': 8, 'low_counts': [sum(g == j for g, v, z in low) for j in range(7)],
              'original_high_columns': len(a['high']), 'retained_high_columns': len(kept_high),
              'rejected_high_columns': len(a['high']) - len(kept_high),
              'positive_indicator_witnesses': witnesses, 'rows': len(C.rows), 'columns_checked': C.nvars,
              'minimum_column_pairing': min(pairings), 'column_pairings_sha256': st.digest(pairings),
              'rhs_pairing': bty, 'general_scope': 'Canonical verify_accepted_atomic_sts.py separately replays the full oriented signed lift.'}
    target = HERE / 'review_r3258_atomic.json'
    if args.write:
        target.write_text(json.dumps(result, indent=2) + '\n')
    else:
        need(result == json.loads(target.read_text()), 'Recorded independent audit differs')
    print('PASS R3258 independent full operator/ray audit:', C.nvars, 'columns;', len(C.rows), 'rows')


if __name__ == '__main__':
    main()
