"""Finite replay for REPORT.md; no optimization or long computation.

The arbitrary-complex-cochain argument is the commutator lemma in the report.
The explicit eighth-root witness is a consistency witness, not a category.
"""
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
G = list(product(range(2), repeat=3))
L = list(product(range(2), repeat=4))
ONE = (0, 0, 0)
UNIT = ONE + (0,)
P0, S0, Z0 = (1, 0, 0), (0, 0, 1), (1, 1, 0)
P, S, Z, E = P0 + (0,), S0 + (0,), Z0 + (0,), ONE + (1,)


def mul(a, b):
    x, y, n = a
    u, v, m = b
    if m:
        x, y = y, x
    return x ^ u, y ^ v, n ^ m


INV = {a: next(b for b in G if mul(a, b) == ONE) for a in G}


def lm(a, b):
    return mul(a[:3], b[:3]) + (a[3] ^ b[3],)


def second(a):
    x, y, n, e = a
    return x ^ e, y ^ e, n


def swap(a):
    return second(a) + (a[3],)


def w(a, b, c, sign=1):
    x, y, n = a
    u, v, m = b
    ell = c[2]
    xp, yp = (y, x) if m else (x, y)
    return (ell * (3*m*(x ^ y) + xp*u + yp*v + 2*yp*u)
            + 2*sign*n*m*ell) % 4


def beta(a, b):
    x, y, n, e = a
    u, v, m, f = b
    return (2*n*f + 2*n*m + 2*y*f + 3*y*m + 2*y*m*f
            + 2*y*u + y*e*m + x*m + 2*x*m*f + 2*x*u
            + 3*x*e*m + 2*x*y*m) % 4


def conj(q, a):
    return mul(mul(q, a), INV[q])


def transport(q, a):
    g, k = conj(q, a[:3]), second(a)
    assert g[2] == k[2] and (g[0] ^ k[0]) == (g[1] ^ k[1])
    return g + (g[0] ^ k[0],)


def kappa(q, a, b, sign=1):
    return (w(q, a, b, sign) + w(conj(q, a), conj(q, b), q, sign)
            - w(conj(q, a), q, b, sign)) % 4


def obstruction(q, a, b, cochain=beta, sign=1):
    return (cochain(transport(q, a), transport(q, b))
            + kappa(q, a[:3], b[:3], sign)
            + cochain(swap(a), swap(b))) % 4


def comm(c, a, b):
    assert lm(a, b) == lm(b, a)
    return (c(a, b) - c(b, a)) % 4


def coboundary_witness(c, modulus=8):
    # Only used to FIND a positive witness, never to prove nonexistence.
    gens = [P, S, E]
    for values in product(range(modulus), repeat=3):
        result, stack, good = {UNIT: 0}, [UNIT], True
        while stack and good:
            a = stack.pop()
            for g, value in zip(gens, values):
                ag = lm(a, g)
                proposed = (result[a] + value - c(a, g)) % modulus
                if ag in result and result[ag] != proposed:
                    good = False
                    break
                if ag not in result:
                    result[ag] = proposed
                    stack.append(ag)
        if good and all((result[a] + result[b] - result[lm(a, b)]
                         - c(a, b)) % modulus == 0
                        for a, b in product(L, repeat=2)):
            return result
    return None


# A representative of the Schur class from D16 -> D8.
R0 = mul(P0, S0)
COORD, r = {}, ONE
for k in range(4):
    for e in range(2):
        COORD[mul(r, S0) if e else r] = (k, e)
    r = mul(r, R0)


def schur(a, b):
    k, e = COORD[a[:3]]
    ell, _ = COORD[b[:3]]
    total = k + (-1)**e * ell
    return ((total - (total % 4)) // 4) % 2


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: this finite replay intentionally uses assertions")
    for a, b, c in product(G, repeat=3):
        assert mul(mul(a, b), c) == mul(a, mul(b, c))
    assert mul(mul(P0, S0), mul(P0, S0)) == Z0
    assert all(mul(Z0, g) == mul(g, Z0) for g in G)
    assert all(swap(lm(a, b)) == lm(swap(a), swap(b))
               for a, b in product(L, repeat=2))
    receipt = {"status": "PASS", "this_test_alone": "branch exclusion",
               "new_branch_exclusion": "reflection duality shift",
               "branch_passing_this_test": "rotation duality shift; excluded separately by Galois-unit parity",
               "finite_checks": {}, "duality_witnesses": {}}
    for sign in (0, 1):
        for a, b, c, d in product(G, repeat=4):
            assert (w(b, c, d, sign) - w(mul(a, b), c, d, sign)
                    + w(a, mul(b, c), d, sign)
                    - w(a, b, mul(c, d), sign) + w(a, b, c, sign)) % 4 == 0
        for a, b, c in product(L, repeat=3):
            assert (beta(b, c) - beta(lm(a, b), c)
                    + beta(a, lm(b, c)) - beta(a, b)
                    - w(a[:3], b[:3], c[:3], sign)
                    + w(second(a), second(b), second(c), sign)) % 4 == 0
        for q in G:
            for a, b, c in product(G, repeat=3):
                assert (kappa(q, b, c, sign) - kappa(q, mul(a, b), c, sign)
                        + kappa(q, a, mul(b, c), sign) - kappa(q, a, b, sign)
                        - w(a, b, c, sign)
                        + w(conj(q, a), conj(q, b), conj(q, c), sign)) % 4 == 0
            cq = lambda a, b: obstruction(q, a, b, sign=sign)
            assert (comm(cq, P, E) + comm(cq, S, E)) % 4 == 2*(sum(q) % 2)
        receipt["finite_checks"][str((-1)**sign)] = {
            "pointed_cocycle_equations": 8**4,
            "stabilizer_cochain_equations": 16**3,
            "normalizer_equations": 8**4,
            "commutator_invariants": 8,
        }
    for a, b, c in product(L, repeat=3):
        assert (schur(b, c) - schur(lm(a, b), c)
                + schur(a, lm(b, c)) - schur(a, b)) % 2 == 0
    for label, q, cochain in [
        ("rotation", R0, beta),
        ("zero", ONE, lambda a, b: (beta(a, b) + 2*schur(a, b)) % 4),
    ]:
        c = lambda a, b: 2*obstruction(q, a, b, cochain=cochain)
        witness = coboundary_witness(c)
        assert witness is not None
        for a, b in product(L, repeat=2):
            assert (witness[a] + witness[b] - witness[lm(a, b)] - c(a, b)) % 8 == 0
        receipt["duality_witnesses"][label] = {
            "shift_lift": q,
            "modulus": 8,
            "cochain_in_lexicographic_L_order": [witness[a] for a in L],
            "equations_checked": 256,
        }
    receipt["scope"] = (
        "The report proves independence from every complex 2-cocycle. "
        "Finite witnesses establish only compatibility with this duality test; "
        "they do not construct fusion categories."
    )
    (HERE / "duality_obstruction_receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
