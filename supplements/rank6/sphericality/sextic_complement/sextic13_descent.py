#!/usr/bin/env python3
"""Verify descent in the maximal real subfield of the thirteenth cyclotomic field.

The trace and Fourier bounds are tested with integer or rational arithmetic.
NumPy batches integer calculations, with overflow bounds checked before each step.
SymPy performs exact root isolation and rational linear algebra."""

from collections import Counter
from itertools import product
from math import isqrt
import numpy as np
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form


X = s.Symbol("X")
POLYNOMIAL = s.Poly(X**6+X**5-5*X**4-4*X**3+6*X**2+3*X-1, X)
SCALE = 10**12
GALOIS = (1, 2, 4, 5, 3, 6)  # powers of 2 modulo multiplication by -1 mod 13
# The trace rows below list the inverse Galois conjugates, still in cyclic order.
INT64_MAX = 2**63-1


def index(k):
    r = k % 13
    assert r
    return min(r, 13-r)-1


def b_vector(k):
    if k % 13 == 0:
        return [-2]*6  # b_0=2=-2*(b_1+...+b_6)
    return [int(i == index(k)) for i in range(6)]


BASIS_MATRICES = [s.Matrix(6, 6, lambda i, j:
                  b_vector(k+j+2)[i]+b_vector(k-j)[i]) for k in range(6)]


def multiplication(coefficients):
    """Multiplication by -sum c_j b_j, in the basis b_1,...,b_6."""
    return -sum((s.Rational(c)*B for c, B in zip(coefficients, BASIS_MATRICES)),
                s.zeros(6))


def root_bounds():
    intervals = s.polys.polytools.intervals(POLYNOMIAL,
                                           eps=s.Rational(1, 10*SCALE))
    assert len(intervals) == 6 and all(m == 1 for _, m in intervals)
    lower, upper = [], []
    for ((lo, hi), _) in reversed(intervals):
        a, b = int(s.floor(lo*SCALE)), int(s.ceiling(hi*SCALE))
        assert a < b
        assert POLYNOMIAL.eval(s.Rational(a, SCALE))*POLYNOMIAL.eval(s.Rational(b, SCALE)) < 0
        lower.append(a)
        upper.append(b)
    assert all(lower[i] > upper[i+1] for i in range(5))
    return np.array(lower, dtype=np.int64), np.array(upper, dtype=np.int64)


def check_trace_bound():
    # Pair Fourier estimates give q_1,q_5>1/25, q_2,q_4>1/36,
    # q_3>1/14 when q_0 is minimal.  These integer comparisons prove
    # the corresponding radical inequalities without numerical approximations.
    assert 13*25 > 18**2
    assert 13*4 > 7**2
    assert 2193 > 0 and 1250**2*3 < 2193**2
    # The weights (0,25,36,14,36,25) have Fourier coefficients
    # (136,-25,-47,8,-47,-25); their nontrivial absolute sum is 152.
    assert 2*25+2*36+14 == 136
    assert 25-36-14 == -25 and -25-36+14 == -47
    assert -2*25+2*36-14 == 8
    assert 2*25+2*47+8 == 152
    # Tr(alpha)<(71+76/sqrt(13))/3<31, so its integer trace is <=30.
    assert 76**2 < 22**2*13


def alpha_candidates():
    lo, hi = root_bounds()
    ML = np.array([[lo[index(i*j)] for j in range(1, 7)] for i in range(1, 7)], dtype=np.int64)
    MU = np.array([[hi[index(i*j)] for j in range(1, 7)] for i in range(1, 7)], dtype=np.int64)
    assert 30*max(abs(int(t)) for T in (ML, MU) for t in T.flat) < INT64_MAX
    triples = np.array(list(product(range(1, 10), repeat=3)), dtype=np.int64)
    sums, maxima = triples.sum(axis=1), triples.max(axis=1)
    out = []
    for prefix in triples:
        traces = sums+sum(prefix)
        mask = (traces <= 30) & (13*np.maximum(maxima, max(prefix)) < 4*traces)
        C = np.column_stack((np.tile(prefix, (int(sum(mask)), 1)), triples[mask]))
        if not len(C):
            continue
        # All c_j>0, so multiplication reverses the interval endpoints.
        AL, AU = -C@MU.T, -C@ML.T
        keep = ((AU.min(axis=1) > 0) & (AL[:, 0] <= SCALE)
                & (AL[:, 0] <= AU.min(axis=1)))
        for c in C[keep]:
            if max(c) != min(c):  # rational alpha was handled in the proof
                out.append(tuple(map(int, c)))
    return out


def is_d_number(M):
    factors = s.factor_list(M.charpoly(X).as_poly())[1]
    assert len(factors) == 1  # multiplication by one element of a number field
    f = factors[0][0]
    a = list(map(int, f.all_coeffs()[1:]))
    n = len(a)
    return all(v**n % abs(a[-1])**i == 0 for i, v in enumerate(a, 1))


def trace_matrix(c):
    return s.Matrix([[c[index(g*j)] for j in range(1, 7)] for g in GALOIS])


def verify_order_and_trace(c, matrix, norm):
    """Show that Z[Gx] contains x O, then test the nonunit obstruction."""
    conjugates = trace_matrix(c)
    # Signs do not affect the generated lattices in the period basis.
    lattice = hermite_normal_form(s.Matrix.hstack(s.ones(6, 1), conjugates.T))
    multipliers = [multiplication(row) for row in conjugates.tolist()]
    for _ in range(2):
        enlarged = hermite_normal_form(s.Matrix.hstack(
            lattice, *(operator*lattice for operator in multipliers)))
        if enlarged == lattice:
            break
        lattice = enlarged

    # The columns of matrix generate x O.  All columns of lattice are
    # products of integral translates of x, or sums of such products.
    assert all(entry.q == 1 for entry in lattice.inv()*matrix)
    if norm == 1:
        return
    # Coordinates of (2-b_1)/13 in the basis (-b_1,...,-b_6).
    p = s.Matrix([3, 2, 2, 2, 2, 2])/13
    trace = sum(matrix.inv()*p)
    assert trace == {64: s.Rational(1, 2), 169: s.Rational(7, 13)}[norm]


def main():
    check_trace_bound()
    candidates = alpha_candidates()
    assert len(candidates) == 222
    norms = Counter()
    cubic = 0
    for c in candidates:
        matrix = multiplication(c)
        norm = int(matrix.det())
        if norm <= 0 or isqrt(norm)**2 != norm or not is_d_number(matrix):
            continue
        if len(set(tuple(row) for row in trace_matrix(c).tolist())) < 6:
            cubic += 1
            continue
        verify_order_and_trace(c, matrix, norm)
        norms[norm] += 1

    assert cubic == 3
    assert norms == {1: 11, 64: 2, 169: 2}
    print("Conductor 13: 15 primitive ratios of trace at most 30.")
    print("All translated-ratio orders contain x O. The four nonunit traces are 1/2 or 7/13.")


if __name__ == "__main__":
    main()
