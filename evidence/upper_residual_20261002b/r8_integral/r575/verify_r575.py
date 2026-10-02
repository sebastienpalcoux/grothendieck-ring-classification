#!/usr/bin/env python3
"""Exact independent reconstruction of the R8_2_575 fusion model.

Standard library only. No floating point and no assertions are used. The
checker constructs the Hopf algebra and the DR input directly from the displayed
formulae, then computes irreducible-character products using its coproduct.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import sys


class Q16:
    """Q[z]/(z**8+1), with z a primitive sixteenth root of unity."""
    __slots__ = ("v",)

    def __init__(self, value=0):
        if isinstance(value, Q16):
            self.v = value.v
        elif isinstance(value, (tuple, list)):
            if len(value) != 8:
                raise ValueError("eight rational coefficients required")
            self.v = tuple(Fraction(x) for x in value)
        else:
            self.v = (Fraction(value),) + (Fraction(0),) * 7

    def __add__(self, other):
        b = Q16(other)
        return Q16(tuple(x + y for x, y in zip(self.v, b.v)))

    __radd__ = __add__

    def __neg__(self):
        return Q16(tuple(-x for x in self.v))

    def __sub__(self, other):
        return self + (-Q16(other))

    def __mul__(self, other):
        b = Q16(other)
        a_nonzero = [(i, x) for i, x in enumerate(self.v) if x]
        b_nonzero = [(i, x) for i, x in enumerate(b.v) if x]
        out = [Fraction(0)] * 8
        for i, x in a_nonzero:
            for j, y in b_nonzero:
                k = i + j
                out[k % 8] += x * y * (-1 if k >= 8 else 1)
        return Q16(out)

    __rmul__ = __mul__

    def __eq__(self, other):
        try:
            return self.v == Q16(other).v
        except (ValueError, TypeError):
            return False

    def __bool__(self):
        return any(self.v)

    def rational(self):
        if any(self.v[1:]):
            raise ValueError("not rational")
        return self.v[0]

    def integer(self):
        r = self.rational()
        if r.denominator != 1:
            raise ValueError("not integral")
        return int(r)

    def encoded(self):
        return [[x.numerator, x.denominator] for x in self.v]

    def __repr__(self):
        return str(self.v)


ZERO, ONE = Q16(0), Q16(1)


def zeta(n):
    n %= 16
    row = [0] * 8
    row[n % 8] = -1 if n >= 8 else 1
    return Q16(row)


Z = [zeta(n) for n in range(16)]


def require(condition, label):
    if not condition:
        raise ValueError("verification failed: " + label)


BASIS = list(product(range(4), range(2), range(2)))
INDEX = {h: i for i, h in enumerate(BASIS)}


def gmul(a, b):
    p, q = a
    r, s = b
    return ((p + (-1 if q else 1) * r) % 4, (q + s) % 2)


def ginv(a):
    p, q = a
    return ((p if q else -p) % 4, q)


def tau(a):
    p, q = a
    return ((-p + q) % 4, q)


def multiplication(a, b):
    p, q, j = a
    r, s, k = b
    right = tau((r, s)) if j else (r, s)
    if (p, q) != right:
        return {}
    return {(p, q, (j + k) % 2): Z[(2 * q * j * k) % 16]}


def coproduct(h):
    p, q, j = h
    result = {}
    for a in product(range(4), range(2)):
        b = gmul(ginv(a), (p, q))
        result[(a + (j,), b + (j,))] = Z[(-4 * a[1] * b[0] * j) % 16]
    return result


def antipode(h):
    p, q, j = h
    out = ginv((p, q))
    if j:
        out = tau(out)
    return {out + (j,): Z[((4 * p - 2) * q * j) % 16]}


def epsilon(h):
    return ONE if h[:2] == (0, 0) else ZERO


UNIT = {(p, q, 0): ONE for p, q in product(range(4), range(2))}
MULT = {(a, b): multiplication(a, b) for a in BASIS for b in BASIS}
DELTA = {a: coproduct(a) for a in BASIS}
ANTIPODE = {a: antipode(a) for a in BASIS}


def add_term(out, key, value):
    if not value:
        return
    value = out.get(key, ZERO) + value
    if value:
        out[key] = value
    elif key in out:
        del out[key]


def apply_linear(vector, operation):
    out = {}
    for key, coefficient in vector.items():
        for target, scalar in operation[key].items():
            add_term(out, target, coefficient * scalar)
    return out


def multiply_vectors(a, b):
    out = {}
    for x, cx in a.items():
        for y, cy in b.items():
            for z, c in MULT[x, y].items():
                add_term(out, z, cx * cy * c)
    return out


def tensor_multiply(a, b):
    out = {}
    for (x1, x2), cx in a.items():
        for (y1, y2), cy in b.items():
            for z1, c1 in MULT[x1, y1].items():
                for z2, c2 in MULT[x2, y2].items():
                    add_term(out, (z1, z2), cx * cy * c1 * c2)
    return out


def scalar_sum(values):
    return sum(values, ZERO)


def check_hopf():
    checks = {}
    for a, b, c in product(BASIS, repeat=3):
        require(multiply_vectors(MULT[a, b], {c: ONE}) ==
                multiply_vectors({a: ONE}, MULT[b, c]), "associativity")
    checks["algebra_associativity"] = 4096
    for a in BASIS:
        singleton = {a: ONE}
        require(multiply_vectors(UNIT, singleton) == singleton, "left unit")
        require(multiply_vectors(singleton, UNIT) == singleton, "right unit")
        left, right = {}, {}
        for (b, c), coefficient in DELTA[a].items():
            for (d, e), scalar in DELTA[b].items():
                add_term(left, (d, e, c), coefficient * scalar)
            for (d, e), scalar in DELTA[c].items():
                add_term(right, (b, d, e), coefficient * scalar)
        require(left == right, "coassociativity")
        for side in (0, 1):
            out = {}
            for (b, c), coefficient in DELTA[a].items():
                x, y = (b, c) if side == 0 else (c, b)
                add_term(out, y, coefficient * epsilon(x))
            require(out == singleton, "counit")
        for side in (0, 1):
            out = {}
            for (b, c), coefficient in DELTA[a].items():
                result = multiply_vectors(ANTIPODE[b], {c: ONE}) if side == 0 else \
                    multiply_vectors({b: ONE}, ANTIPODE[c])
                for x, scalar in result.items():
                    add_term(out, x, coefficient * scalar)
            require(out == {x: v * epsilon(a) for x, v in UNIT.items() if epsilon(a)},
                    "antipode identity")
        require(apply_linear(ANTIPODE[a], ANTIPODE) == singleton, "S squared")
    for a, b in product(BASIS, repeat=2):
        require(apply_linear(MULT[a, b], DELTA) == tensor_multiply(DELTA[a], DELTA[b]),
                "bialgebra compatibility")
        require(scalar_sum(c * epsilon(x) for x, c in MULT[a, b].items()) ==
                epsilon(a) * epsilon(b), "counit algebra map")
    require(apply_linear(UNIT, DELTA) == {(x, y): cx * cy for x, cx in UNIT.items()
                                         for y, cy in UNIT.items()}, "coproduct unit")
    checks.update(coalgebra_coassociativity=16, bialgebra_products=256,
                  unit_counit_antipode="PASS", involutivity="PASS")
    return checks


def pairing(a, b):
    p, q, j = a
    r, s, k = b
    if s != j or k != q:
        return ZERO
    return Z[(-12 * r * p + j * q) % 16] * Fraction(1, 4)


P = [[pairing(a, b) for b in BASIS] for a in BASIS]
PINV = [[Z[(-4 * a[0] * b[0] - a[1] * a[2]) % 16]
         if b[1] == a[2] and b[2] == a[1] else ZERO for b in BASIS] for a in BASIS]


def check_pairing_and_dr():
    for a, b, c in product(BASIS, repeat=3):
        lhs = scalar_sum(v * pairing(x, c) for x, v in MULT[a, b].items())
        rhs = scalar_sum(v * pairing(a, x) * pairing(b, y)
                         for (x, y), v in DELTA[c].items())
        require(lhs == rhs, "pairing multiplication in first variable")
        lhs = scalar_sum(v * pairing(a, x) for x, v in MULT[b, c].items())
        rhs = scalar_sum(v * pairing(x, b) * pairing(y, c)
                         for (x, y), v in DELTA[a].items())
        require(lhs == rhs, "pairing multiplication in second variable")
    for a, b in product(BASIS, repeat=2):
        require(pairing(a, b) == pairing(b, a), "symmetric pairing")
    for a in BASIS:
        require(scalar_sum(v * pairing(x, a) for x, v in UNIT.items()) == epsilon(a),
                "pairing first unit")
        require(scalar_sum(v * pairing(a, x) for x, v in UNIT.items()) == epsilon(a),
                "pairing second unit")
    for i, j in product(range(16), repeat=2):
        require(scalar_sum(P[i][k] * PINV[k][j] for k in range(16)) == (ONE if i == j else ZERO),
                "pairing right inverse")
        require(scalar_sum(PINV[i][k] * P[k][j] for k in range(16)) == (ONE if i == j else ZERO),
                "pairing left inverse")
    # H-vee has opposite product and coproduct relative to the standard dual.
    # P^-1 is a standard-dual Hopf isomorphism; the antipode converts conventions.
    gamma = [[ZERO] * 16 for _ in range(16)]
    for i, a in enumerate(BASIS):
        for target, scalar in ANTIPODE[a].items():
            for j in range(16):
                gamma[INDEX[target]][j] += scalar * PINV[i][j]
    for i, j in product(range(16), repeat=2):
        require(gamma[i][j] == gamma[j][i], "DR Gamma symmetry")
    # Independently check Gamma against the actual op/cop dual structure, rather
    # than relying solely on the preceding pairing argument.
    gamma_map = {a: {b: gamma[INDEX[b]][INDEX[a]] for b in BASIS
                     if gamma[INDEX[b]][INDEX[a]]} for a in BASIS}
    for a, b in product(BASIS, repeat=2):
        dual_product = {h: DELTA[h][b, a] for h in BASIS if (b, a) in DELTA[h]}
        require(apply_linear(dual_product, gamma_map) ==
                multiply_vectors(gamma_map[a], gamma_map[b]), "Gamma dual algebra map")
    for a in BASIS:
        right = {}
        for b, c in product(BASIS, repeat=2):
            scalar = MULT[c, b].get(a, ZERO)
            if scalar:
                for x, cx in gamma_map[b].items():
                    for y, cy in gamma_map[c].items():
                        add_term(right, (x, y), scalar * cx * cy)
        require(apply_linear(gamma_map[a], DELTA) == right, "Gamma dual coalgebra map")
        require(scalar_sum(c * epsilon(x) for x, c in gamma_map[a].items()) ==
                (ONE if a[2] == 0 else ZERO), "Gamma dual counit")
        dual_antipode = {h: ANTIPODE[h][a] for h in BASIS if a in ANTIPODE[h]}
        require(apply_linear(dual_antipode, gamma_map) ==
                apply_linear(gamma_map[a], ANTIPODE), "Gamma antipode intertwining")
    require(apply_linear({a: epsilon(a) for a in BASIS if epsilon(a)}, gamma_map) == UNIT,
            "Gamma dual unit")
    lam = [Q16(Fraction(1, 2)) if a[2] == 0 else ZERO for a in BASIS]
    for a in BASIS:
        for side in (0, 1):
            out = {}
            for (b, c), coefficient in DELTA[a].items():
                x, y = (b, c) if side == 0 else (c, b)
                add_term(out, x, coefficient * lam[INDEX[y]])
            require(out == {x: v * lam[INDEX[a]] for x, v in UNIT.items() if lam[INDEX[a]]},
                    "two-sided cointegral")
    integral = {(0, 0, 0): Q16(Fraction(1, 2)), (0, 0, 1): Q16(Fraction(1, 2))}
    for a in BASIS:
        target = {x: v * epsilon(a) for x, v in integral.items() if epsilon(a)}
        require(multiply_vectors({a: ONE}, integral) == target, "left normalized integral")
        require(multiply_vectors(integral, {a: ONE}) == target, "right normalized integral")
    gamma_lam = [scalar_sum(gamma[i][j] * lam[j] for j in range(16)) for i in range(16)]
    require({a: gamma_lam[i] for i, a in enumerate(BASIS) if gamma_lam[i]} ==
            {a: 4 * c for a, c in integral.items()}, "Gamma(lambda)=4 Lambda")
    require(scalar_sum(lam[i] * gamma_lam[i] for i in range(16)) == ONE,
            "DR normalization lambda Gamma lambda")
    return {"hopf_pairing_identities": 8192, "symmetric_nondegenerate_pairing": "PASS",
            "explicit_fourier_inverse": "PASS", "dr_dual_convention": "standard_dual_op_cop",
            "gamma": "S composed with P inverse", "gamma_symmetric": "PASS",
            "gamma_actual_op_cop_dual_products": 256, "gamma_actual_op_cop_dual_coproducts": 16,
            "two_sided_cointegral": "PASS", "distinguished_grouplike": 1,
            "gamma_lambda": "4 Lambda", "lambda_gamma_lambda": 1,
            "dr_theorem_2_5_conditions": "PASS"}


def characters():
    """Orbit representations of Fun(D8) crossed by the involution tau.

    The two fixed points (0,0),(2,0) each give two one-dimensional
    representations. Three free two-element orbits give three matrix blocks.
    The ordering yields the conventional Rep(D16) based ring ordering.
    """
    chars = []
    for p, sign in ((0, 1), (0, -1), (2, 1), (2, -1)):
        chars.append([Q16(sign ** j) if (r, q) == (p, 0) else ZERO
                      for r, q, j in BASIS])
    for orbit in (((0, 1), (1, 1)), ((1, 0), (3, 0)), ((2, 1), (3, 1))):
        chars.append([ONE if j == 0 and (p, q) in orbit else ZERO for p, q, j in BASIS])
    return chars


def model_tensor():
    chars = characters()
    neutral = [[[0] * 7 for _ in range(7)] for _ in range(7)]
    for i, j in product(range(7), repeat=2):
        char = [scalar_sum(v * chars[i][INDEX[a]] * chars[j][INDEX[b]]
                           for (a, b), v in DELTA[h].items()) for h in BASIS]
        coefficients = []
        for p, sign in ((0, 1), (0, -1), (2, 1), (2, -1)):
            coefficients.append(((char[INDEX[(p, 0, 0)]] + sign * char[INDEX[(p, 0, 1)]]) *
                                 Fraction(1, 2)).integer())
        for rep in ((0, 1, 0), (1, 0, 0), (2, 1, 0)):
            coefficients.append(char[INDEX[rep]].integer())
        require(all(x >= 0 for x in coefficients), "character multiplicities nonnegative")
        require(all(char[k] == scalar_sum(coefficients[l] * chars[l][k] for l in range(7))
                    for k in range(16)), "all neutral character values")
        neutral[i][j] = coefficients
    # Compare to an independently constructed ordinary character ring of D16.
    # The group elements r^p s^q have p modulo 8 and q modulo 2.
    group = list(product(range(8), range(2)))
    dihedral = []
    for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        dihedral.append([Q16((-1) ** (a * p + b * q)) for p, q in group])
    for k in (1, 2, 3):
        dihedral.append([ZERO if q else Z[(2 * k * p) % 16] + Z[(-2 * k * p) % 16]
                         for p, q in group])
    for i, j in product(range(7), repeat=2):
        inner = scalar_sum(dihedral[i][g] * dihedral[j][g] for g in range(16)) * Fraction(1, 16)
        require(inner == int(i == j), "D16 character orthogonality")
        for k in range(7):
            coeff = scalar_sum(dihedral[i][g] * dihedral[j][g] * dihedral[k][g]
                               for g in range(16)) * Fraction(1, 16)
            require(coeff.integer() == neutral[i][j][k], "independent Rep(D16) ring")
    dims = [1, 1, 1, 1, 2, 2, 2, 4]
    tensor = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i, j in product(range(7), repeat=2):
        tensor[i][j][:7] = neutral[i][j]
    for i in range(7):
        tensor[i][7][7] = tensor[7][i][7] = dims[i]
        tensor[7][7][i] = dims[i]
    return tensor


def tensor_checks(tensor):
    dims = [1, 1, 1, 1, 2, 2, 2, 4]
    for i, j in product(range(8), repeat=2):
        require(sum(tensor[i][j][k] * dims[k] for k in range(8)) == dims[i] * dims[j],
                "fusion dimensions")
        require(tensor[i][j][0] == int(i == j), "self-duality")
    for i, j, k, l in product(range(8), repeat=4):
        require(sum(tensor[i][j][a] * tensor[a][k][l] for a in range(8)) ==
                sum(tensor[j][k][a] * tensor[i][a][l] for a in range(8)), "fusion associativity")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path,
                        default=next(p for p in Path(__file__).resolve().parents if (p / "evidence").is_dir()))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = {"id": "R8_2_575", "status": "PASS", "arithmetic": "Q[z]/(z^8+1)",
               "assertions_used": False, "scope": "unitary", "model_to_census": [0, 5, 1, 2, 3, 7, 4, 6]}
    receipt["hopf"] = check_hopf()
    receipt["davydov_runkel"] = check_pairing_and_dr()
    tensor = model_tensor()
    tensor_checks(tensor)
    raw = gzip.decompress((args.repository / "supplements/rank8/data/rank8_tables.txt.gz").read_bytes())
    raw_digest = hashlib.sha256(raw).hexdigest()
    require(raw_digest == "97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600",
            "raw rank-eight census digest")
    rows = [json.loads(line.replace("{", "[").replace("}", "]"))
            for line in raw.decode().splitlines() if line.strip()]
    flat = lambda t: tuple(v for matrix in t for row in matrix for v in row)
    band = [row for row in rows if max(flat(row)) == 2]
    require(len(band) == 877 and len(rows) == 973, "source census counts")
    band.sort(key=flat)
    source = band[574]
    mapping = receipt["model_to_census"]
    mapped = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i, j, k in product(range(8), repeat=3):
        mapped[mapping[i]][mapping[j]][mapping[k]] = tensor[i][j][k]
    require(mapped == source, "all 512 source coefficients")
    digest = hashlib.sha256(json.dumps(mapped, separators=(",", ":")).encode()).hexdigest()
    require(digest == "b69b81c82fee86626ed0d7c132227bee7a67fbf8f4c54a84f31d62a3a51858cf", "source tensor digest")
    receipt["census_tensor_sha256"] = digest
    receipt["raw_census_sha256"] = raw_digest
    receipt["fusion"] = {"neutral_character_values_checked": 784, "full_tensor_coefficients": 512,
                         "independent_dihedral_character_products": 343,
                         "fusion_associativity": 4096, "dimensions": [1, 1, 1, 1, 2, 2, 2, 4],
                         "global_dimension": 32, "full_source_match": True}
    receipt["source_file_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    encoded = json.dumps(receipt, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded)
    sys.stdout.write(encoded)


if __name__ == "__main__":
    main()
