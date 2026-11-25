#!/usr/bin/env python3
"""Verify descent in the maximal real subfield of the thirteenth cyclotomic field.

The trace and Fourier bounds are tested with integer or rational arithmetic.
NumPy batches integer calculations, with overflow bounds checked before each step.
SymPy performs exact root isolation and rational linear algebra."""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import isqrt, lcm
import numpy as np
import sympy as s


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


def h_vectors(A):
    return np.array([[1, a, b, c, d, A-1-a-b-c-d]
                     for a in range(1, A-4)
                     for b in range(1, A-3-a)
                     for c in range(1, A-2-a-b)
                     for d in range(1, A-1-a-b-c)], dtype=np.int64)


def check_full_span(c, C, M, H):
    A = sum(c)
    inverse = C.inv()
    denominator = lcm(*(int(x.q) for x in inverse))
    numerator = inverse*denominator
    N = np.array(numerator, dtype=np.int64)
    # Bound every dot product and every sum of six squares before int64 use.
    bound = 3*A*max(sum(abs(int(x)) for x in row) for row in N)
    assert 6*bound*bound <= INT64_MAX
    assert 29*denominator**2 <= INT64_MAX
    Z = (H+2*A)@N.T
    keep = np.sum(Z*Z, axis=1) <= 29*denominator**2
    HQ, ZQ = H[keep], Z[keep]
    stats = [len(H), len(HQ), 0, 0]
    for h, z in zip(HQ, ZQ):
        # Python/SymPy integers make the next products independent of word size.
        zv = s.Matrix(list(map(int, z)))
        wv = M*zv
        if sum(x*x for x in wv) > 29*denominator**2:
            continue
        stats[2] += 1
        v, w = zv/(13*denominator), wv/(13*denominator)
        assert sum(v) == sum(w) == 1
        assert 13*C*v == s.Matrix([int(x)+2*A for x in h])
        norm_q = multiplication(v).det()
        # E=1/q is an algebraic integer and totally positive, so N(q)=1/n.
        if norm_q.p != 1:
            continue
        stats[3] += 1
        assert any([w[index(g*j)] for j in range(1, 7)] == list(v)
                   for g in GALOIS), (c, list(h), list(v), list(w))
    return stats


def check_cubic_span(c, C, M):
    A = sum(c)
    assert A % 2 == 0
    C3 = C[:3, :]
    assert C3.rank() == 3 and C[3:, :] == C3
    right = C3.T*(C3*C3.T).inv()/13
    checked = 0
    for h1 in range(1, A//2-1):
        h = [1, h1, A//2-1-h1]
        v = right*s.Matrix([x+2*A for x in h])
        w = M*v
        assert sum(v) == sum(w) == 1
        # Projection to the cubic subfield has square trace at most 5/26;
        # equivalently, 338*sum(v_j^2)<=57, for both q and p=alpha*q.
        assert (338*sum(x*x for x in v) > 57 or
                338*sum(x*x for x in w) > 57), (c, h)
        checked += 1
    return checked


def main():
    check_trace_bound()
    candidates = alpha_candidates()
    assert len(candidates) == 222
    square_norm = []
    for c in candidates:
        M = multiplication(c)
        norm = int(M.det())
        if norm > 0 and isqrt(norm)**2 == norm:
            square_norm.append((c, M))
    assert len(square_norm) == 37
    eligible = [(c, M) for c, M in square_norm if is_d_number(M)]
    assert len(eligible) == 18
    ranks = Counter()
    cache = {}
    stats = [0, 0, 0, 0]
    cubic_count = 0
    for c, M in eligible:
        C = trace_matrix(c)
        rank = C.rank()
        ranks[rank] += 1
        if rank == 6:
            A = sum(c)
            if A not in cache:
                cache[A] = h_vectors(A)
            branch = check_full_span(c, C, M, cache[A])
            stats = [a+b for a, b in zip(stats, branch)]
        elif rank == 3:
            cubic_count += check_cubic_span(c, C, M)
        else:
            raise AssertionError((c, rank))
    assert ranks == {6: 15, 3: 3}
    assert stats == [86131, 382, 30, 5]
    assert cubic_count == 30
    print("Exact conductor-13 descent certificate passed.")
    print("Ratio trace bound: 30.")
    print("Alpha candidates: 222; square norm: 37; d-number: 18.")
    print("Orbit-span ranks:", dict(sorted(ranks.items())))
    print("Full-span trace vectors / signed moment / both moments / norm-integral:", *stats)
    print("Cubic trace vectors excluded:", cubic_count)
    print("All five surviving pairs p,q are exactly Galois conjugate.")


if __name__ == "__main__":
    main()
