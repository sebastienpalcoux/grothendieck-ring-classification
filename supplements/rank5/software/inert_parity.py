"""Exact residue-field parity descent for self-dual rank-five rings.

This is a sufficient structural criterion, not a list of special tensors.
The certificate records every character of the fusion ring over F_4 and
recomputes the central-divisibility filter from the input tensor.
"""

import itertools
from functools import reduce

from exact import require
from quadratic_parity import (
    charpoly, connected, matmul, polynomial_quotient,
    rank_mod_two, squarefree, times,
)


def _f4_multiply(x, y):
    """Represent a+b*w by a+2*b, where w*w=w+1 in F_4."""
    a, b, c, d = x & 1, x >> 1, y & 1, y >> 1
    return (a * c ^ b * d) | ((a * d ^ b * c ^ b * d) << 1)


def _f4_characters(R):
    result = []
    for tail in itertools.product(range(4), repeat=4):
        values = (1,) + tail
        if all(
            _f4_multiply(values[i], values[j]) ==
            reduce(
                int.__xor__,
                (values[k] for k in range(5) if R[i][j][k] & 1),
                0,
            )
            for i in range(5) for j in range(5)
        ):
            result.append(list(values))
    return result


def certificate(R):
    if len(R) != 5 or any(len(M) != 5 or any(len(row) != 5 for row in M) for M in R):
        return None
    if any(R[i][j][0] != int(i == j) for i in range(5) for j in range(5)):
        return None
    if any(R[i][j][k] != R[j][i][k] or R[i][j][k] != R[i][k][j]
           for i, j, k in itertools.product(range(5), repeat=3)):
        return None
    M = [[R[j][j][i] for i in range(1, 5)] for j in range(1, 5)]
    if any(sum(row) % 2 for row in M):
        return None
    A = [sum(row) // 2 for row in M]
    raw = 1 + sum(a * a for a in A)
    if raw % 16:
        return None
    q = raw // 16
    if q <= 1 or q % 8 != 5 or not squarefree(q):
        return None
    dimensions = [(1, 0)] + [(a, 2) for a in A]
    if any(times(dimensions[i], dimensions[j], q) !=
           tuple(sum(R[i][j][k] * dimensions[k][b] for k in range(5)) for b in (0, 1))
           for i, j in itertools.product(range(5), repeat=2)):
        return None
    if rank_mod_two(M) != 3 or any(sum(row) % 2 for row in M):
        return None
    irreducibles = [i for i in range(1, 5) if A[i-1] > 0 and connected(R[i])]
    if not irreducibles:
        return None

    squares = [matmul(T, T) for T in R]
    B = [[sum(T[i][j] for T in squares) for j in range(5)] for i in range(5)]
    cp = charpoly(B)
    order_at_zero = next((k for k, c in enumerate(reversed(cp)) if c & 1), len(cp))
    D = tuple(sum(times(d, d, q)[b] for d in dimensions) for b in (0, 1))
    fp_codegree = [1, -2 * D[0], D[0] * D[0] - q * D[1] * D[1]]
    if order_at_zero != 2 or fp_codegree[1] % 2 or fp_codegree[2] % 2:
        return None
    try:
        quotient = polynomial_quotient(cp, fp_codegree)
    except Exception:
        return None
    # 2 is inert since q=5 mod 8, and w=(1+sqrt(q))/2 has w*w=w+1 mod 2.
    # The original FP codegree D is zero in O_K/2; central induction
    # requires δ/D integral and hence δ=1+sum(dim_i^2)=0 in F_4.
    chars = _f4_characters(R)
    allowed = [v for v in chars if reduce(
        int.__xor__, (_f4_multiply(x, x) for x in v), 0) == 0]
    if not allowed or any(any(x not in (0, 1) for x in v) or sum(v[1:]) != 3
                          for v in allowed):
        return None
    return {
        'kind': 'inert_quadratic_parity', 'q': q, 'A': A,
        'M': M, 'parity_rank': 3, 'casimir_polynomial': cp,
        'zero_multiplicity_mod2': order_at_zero,
        'FP_dimension': list(D), 'FP_codegree_polynomial': fp_codegree,
        'remaining_factor': quotient, 'characters_F4': chars,
        'allowed_residue_characters': allowed,
        'irreducible_matrix': irreducibles[0],
    }


def verify(R, recorded):
    require(certificate(R) == recorded, 'inert quadratic parity certificate mismatch')
