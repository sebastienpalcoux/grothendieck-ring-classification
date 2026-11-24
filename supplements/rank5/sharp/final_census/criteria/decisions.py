"""Exact necessary conditions for pseudo-unitary categorifiability.

Theorem A of the manuscript makes this sufficient for excluding complex
rank-five categorifications. No signed-table enumeration is used here.
"""
from exact import *
from rings import *
from induction import check_pseudo
import higher_traces


def multiplication_matrix(a, K, f):
    u = K(s.Poly(t, t).rem(f).all_coeffs())
    return s.Matrix.hstack(*(vector(a*u**i, f.degree()) for i in range(f.degree())))


def check_subring(R, certificate):
    J = certificate['subset']
    require(all(type(i) is int and 0 <= i < len(R) for i in J),
            'subring basis indices must be integers in range')
    require(0 in J and 2 <= len(J) < len(R) and len(set(J)) == len(J), 'invalid subring')
    a = Characters(R)
    f, K, ds, D, pD, emb = a.fp()
    require(all(a.du[i] in J for i in J), 'subring not dual closed')
    require(not any(R[i][j][k] for i in J for j in J for k in range(len(R)) if k not in J),
            'subring not closed')
    dimension = sum((ds[i]*ds[a.du[i]] for i in J), K.zero)
    polynomial = multiplication_matrix(D/dimension, K, f).charpoly(t).as_poly()
    require(pc(polynomial) == certificate['quotient_polynomial']
            and any(v.q != 1 for v in polynomial.all_coeffs()),
            'quotient integrality not excluded')


def verify(R, certificate):
    kind = certificate['kind']
    if kind == 'dnumber':
        check_dnumber(R, certificate)
    elif kind == 'subring':
        check_subring(R, certificate)
    elif kind in ('fp_norm', 'fp_dimension_field'):
        a = Characters(R, certificate['generator'])
        f, K, ds, D, pD, emb = a.fp()
        require(pc(f) == certificate['factor'], 'wrong FP character factor')
        if kind == 'fp_norm':
            check_norm(pD, a.cf, certificate['obstruction'])
        else:
            check_field(f, a.cf, certificate['obstruction'])
    elif kind == 'finite_indicator_traces':
        higher_traces.verify(R, certificate)
    else:
        require(kind == 'induction', 'unknown certificate kind')
        check_pseudo(R, certificate)
