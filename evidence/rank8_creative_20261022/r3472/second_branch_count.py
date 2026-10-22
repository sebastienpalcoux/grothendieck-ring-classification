"""Exact multiset count for the second R3472 rank-two Morita branch.

This dependency was omitted from the published creative-stage source inventory.
The implementation is reconstructed from PROOF.md, rather than recovered from
the historical run. Its mathematical counts agree with the historical receipt;
its cache-state statistics need not agree with an unavailable implementation.

For h invertible objects, count nonnegative integer multiplicities n_(u,t) with
u >= 0, t >= 1 and
    sum n*u*u = 35-h, sum n*u*t = 70, sum n*t*t = 175.
Every type and multiplicity has a finite bound from these equations. No
floating-point arithmetic, solver, timeout, or search cutoff is used.
"""
from functools import lru_cache
from math import isqrt


def count(h):
    if h not in (1, 2, 5, 7):
        raise ValueError("The documented second branch has h in {1,2,5,7}")
    U0, V0, W0 = 35-h, 70, 175
    types = [(u*u, u*t, t*t)
             for u in range(1, isqrt(U0)+1)
             for t in range(1, isqrt(W0)+1) if u*t <= V0]

    # Coefficients of product_(t>=1) (1-z^(t*t))^(-1), through degree W0.
    # They count exactly the u=0 types after all positive-u types are fixed.
    squares = [0]*(W0+1)
    squares[0] = 1
    for t in range(1, isqrt(W0)+1):
        for w in range(t*t, W0+1):
            squares[w] += squares[w-t*t]

    @lru_cache(None)
    def visit(index, U, V, W):
        if min(U, V, W) < 0 or V*V > U*W:
            return 0
        if U == 0:
            return squares[W] if V == 0 else 0
        if index == len(types):
            return 0
        a, b, c = types[index]
        return sum(visit(index+1, U-n*a, V-n*b, W-n*c)
                   for n in range(min(U//a, V//b, W//c)+1))

    result = visit(0, U0, V0, W0)
    return {"integral_global_dimension": h,
            "nonintegral_multisets": result,
            "states": visit.cache_info().currsize}


if __name__ == "__main__":
    import json
    print(json.dumps([count(h) for h in (1, 2, 5, 7)], indent=2))
