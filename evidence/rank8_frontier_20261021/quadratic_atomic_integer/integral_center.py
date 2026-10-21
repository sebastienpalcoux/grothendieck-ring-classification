"""Pointed integral center when I(1) has no other integral simple.

The proof is given in INTEGRAL_CENTER.md. This adapter checks its quadratic
positive-support hypotheses before deleting any complete restriction orbit.
"""
from types import SimpleNamespace
from fractions import Fraction as Q
from features import require, st


def filter_integral(C, T):
    require(T.degree == 2, 'positive quadratic support adapter required')
    ds = [T.coordinates(d) for d in T.ds]
    require(all(b >= 0 for a, b in ds), 'irrational coefficients not all nonnegative')
    pointed = [i for i, (a, b) in enumerate(ds) if b == 0]
    require(all(ds[i] == (Q(1), Q(0)) for i in pointed),
            'integral source support is not pointed')
    for i in pointed:
        inverse = next(j for j in range(len(C.R)) if C.R[i][j][0])
        require(C.R[i][inverse] == [1] + [0] * (len(C.R) - 1),
                'dimension-one source basis element is not invertible')
    fp = T.characters.index(tuple(T.ds))
    betas = [T.coordinates(d) for d in T.beta]
    require([E for E, (a, b) in enumerate(betas) if b == 0] == [fp] and
            T.beta[fp] == T.K.one,
            'I(1) has another integral distinguished dimension')
    keep, removed = [], []
    for orbit in C.orbits:
        bad = []
        for j in orbit:
            v = (0,) + tuple(C.a['high'][j][0])
            integral = all(v[i] == 0 for i in range(len(v)) if i not in pointed)
            if integral and sum(v) != 1:
                bad.append({'high_index': j, 'restriction': v, 'dimension': sum(v)})
        if bad:
            removed.append({'orbit': orbit, 'forbidden_restrictions': bad})
        else:
            keep.append(orbit)
    report = st.encode({'kind': 'pointed_integral_center_from_distinguished_kernel',
                        'tensor_sha256': st.digest(C.R),
                        'source_dimensions': ds, 'distinguished_dimensions': betas,
                        'FP_character': fp, 'pointed_source_indices': pointed,
                        'original_high_orbits': len(C.orbits), 'retained_high_orbits': len(keep),
                        'removed': removed})
    D = SimpleNamespace(R=C.R, a=C.a, low=C.low, orbits=keep,
                        meta={**C.meta, 'integral_center_filter_sha256': st.digest(report)})
    return D, report
