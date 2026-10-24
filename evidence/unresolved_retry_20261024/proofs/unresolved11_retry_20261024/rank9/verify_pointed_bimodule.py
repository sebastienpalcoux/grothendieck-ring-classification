"""Exact finite replay for the new D8 bimodule pairing theorem.

The categorical inference is proved in POINTED_BIMODULE.md. This script
checks the cocycle, its cyclic restrictions, an explicit stabilizer
trivialization, and its nondegenerate stabilizer pairing. No optimization.
"""
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
G = list(product(range(2), repeat=3))
L = list(product(range(2), repeat=4))
ONE = (0, 0, 0)


def mul(a, b):
    x, y, n = a
    u, v, m = b
    if m:
        x, y = y, x
    return x ^ u, y ^ v, n ^ m


def lm(a, b):
    return mul(a[:3], b[:3]) + (a[3] ^ b[3],)


def p2(a):
    x, y, n, e = a
    return x ^ e, y ^ e, n


def w(a, b, c, sign):
    x, y, n = a
    u, v, m = b
    _, _, ell = c
    xp, yp = (y, x) if m else (x, y)
    return (ell * (3*m*(x ^ y) + xp*u + yp*v + 2*yp*u)
            + 2*sign*n*m*ell) % 4


def beta(a, b):
    x, y, n, e = a
    u, v, m, f = b
    return (2*n*f + 2*n*m + 2*y*f + 3*y*m + 2*y*m*f
            + 2*y*u + y*e*m + x*m + 2*x*m*f + 2*x*u
            + 3*x*e*m + 2*x*y*m) % 4


def order_and_indicator(g, sign):
    t, exponent, order = ONE, 0, 0
    while True:
        exponent = (exponent + w(g, t, g, sign)) % 4
        t = mul(t, g)
        order += 1
        if t == ONE:
            return order, exponent


def main():
    for a, b, c in product(G, repeat=3):
        assert mul(mul(a, b), c) == mul(a, mul(b, c))
    z = (1, 1, 0)
    assert all(mul(z, a) == mul(a, z) for a in G)
    # z is a commutator: the two involutions below have product of order 4.
    p, s = (1, 0, 0), (0, 0, 1)
    assert mul(mul(mul(p, s), p), s) == z
    receipt = {"signs": {}, "classification_change": False}
    for sign in (0, 1):
        for a, b, c, d in product(G, repeat=4):
            assert (w(b, c, d, sign) - w(mul(a, b), c, d, sign)
                    + w(a, mul(b, c), d, sign)
                    - w(a, b, mul(c, d), sign) + w(a, b, c, sign)) % 4 == 0
        for a, b, c in product(L, repeat=3):
            assert (beta(b, c) - beta(lm(a, b), c)
                    + beta(a, lm(b, c)) - beta(a, b)
                    - w(a[:3], b[:3], c[:3], sign)
                    + w(p2(a), p2(b), p2(c), sign)) % 4 == 0
        cyc = []
        for g in G:
            order, exponent = order_and_indicator(g, sign)
            assert exponent == (2 if order == 4 else 2*sign*g[2])
            cyc.append({"element": g, "order": order,
                        "indicator_exponent_mod4": exponent})
        receipt["signs"][str((-1)**sign)] = {
            "cocycle_identities_checked": len(G)**4,
            "cochain_identities_checked": len(L)**3,
            "cyclic_restrictions": cyc,
        }
    left, right = (1, 1, 0, 1), (0, 0, 0, 1)
    assert lm(left, right) == z + (0,)
    assert beta(left, right) - beta(right, left) == 2
    receipt["stabilizer_pairing"] = -1
    receipt["projected_third_indicator_each_dual_large_simple"] = [-1, "1/2"]
    receipt["projected_sum_source_large_third_indicators"] = [
        -4, "-5/2", -1, "1/2", 2]
    receipt["scope"] = (
        "All surviving identity-quotient-action D8 Morita candidates, both TY signs. "
        "Pairing and invertibility are general complex; indicator conclusions require "
        "a spherical realization (apply to a pseudo-unitary Galois conjugate). "
        "The finite checks do not construct any fusion category."
    )
    (HERE / "pointed_bimodule_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"checked": True, "stabilizer_pairing": -1,
                      "classification_change": False}))


if __name__ == "__main__":
    main()
