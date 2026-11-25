"""Dyadic certificate at valuation nine. Requires NumPy, SymPy and quadratic40.py."""

from functools import lru_cache
from itertools import product

import numpy as np
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form

from quadratic40 import binary, conjugate, epsilon, field_one, mul4, multiply, normfield, red

ZERO = (0,) * 6
BINARY_POINTS = np.array(binary, dtype=np.int64)


def add_mod_two(x, y):
    return tuple(a ^ b for a, b in zip(x, y))


def span(basis):
    space = {ZERO}
    for generator in basis:
        space |= {add_mod_two(x, generator) for x in space}
    return space


def bilinear(x, y, kind):
    z = multiply(x, y, kind)
    return (z[1] + z[3] + z[5] + (z[4] if kind == "R" else 0)) % 2


def middle_spaces(kind, basis):
    characteristic = (0, 0, 1, 0, 1, int(kind == "R"))
    initial = [*basis, characteristic]
    space = span(initial)
    if len(space) == 8:
        yield space
        return
    seen = set()
    for v in binary:
        if any(bilinear(v, w, kind) for w in [v, *initial]):
            continue
        enlarged = frozenset(space | {add_mod_two(v, w) for w in space})
        if len(enlarged) == 8 and enlarged not in seen:
            seen.add(enlarged)
            yield enlarged


def coset_representatives(space):
    seen, representatives = set(), []
    for x in binary:
        if x not in seen:
            seen.update(add_mod_two(x, v) for v in space)
            representatives.append(x)
    return representatives


def complement_basis(small, large):
    space, basis = set(small), []
    for v in sorted(large):
        if v not in space:
            basis.append(v)
            space |= {add_mod_two(v, x) for x in space}
    return basis


def integral_basis(generators, kind):
    exact_basis = hermite_normal_form(Matrix(np.array(generators, dtype=int).T))
    if abs(exact_basis.det()) != 512:
        return None
    exact_inverse = 8 * exact_basis.inv()
    assert all(x.is_Integer for x in exact_inverse)
    basis = np.array(exact_basis, dtype=np.int64)
    inverse = np.array(exact_inverse, dtype=np.int64)
    assert np.array_equal(inverse @ basis, 8 * np.eye(6, dtype=np.int64))
    raw_products = np.array([[multiply(x, y, kind) for x in basis.T] for y in basis.T])
    table = raw_products @ inverse.T
    if (table % 8).any():
        return None
    return basis, inverse, table // 8, raw_products


def lattices(kind):
    one = (1, 0, 0, 0, 1, int(kind == "R"))
    e = (0, 0, 1, 0, 0, 0)
    ambient = np.eye(6, dtype=np.int64)
    found = {}
    for low_basis in ([one], [one, e]):
        low = span(low_basis)
        high = {v for v in binary if all(not bilinear(v, x, kind) for x in low_basis)}
        high_reps = coset_representatives(high)
        high_gens = [4 * np.array(v) for v in complement_basis({ZERO}, high)]
        for middle in middle_spaces(kind, low_basis):
            middle_basis = complement_basis(low, middle)
            if e in low:
                e_lifts = [np.array(e) + 2 * np.array(t) + 4 * np.array(s)
                           for t, s in product(coset_representatives(middle), high_reps)]
            else:
                e_lifts = [None]
            for shifts in product(high_reps, repeat=len(middle_basis)):
                mid_gens = [2 * np.array(v) + 4 * np.array(s)
                            for v, s in zip(middle_basis, shifts)]
                gens = [*list(8 * ambient), one, *high_gens, *mid_gens]
                for lift in e_lifts:
                    candidate = integral_basis(gens if lift is None else [*gens, lift], kind)
                    if candidate is not None:
                        found[tuple(candidate[0].ravel())] = candidate
    assert len(found) == 28
    return found.values()


def unit_powers(y):
    powers = [field_one]
    while True:
        x = red(mul4(powers[-1], y), 32)
        if x == field_one:
            return powers
        powers.append(x)
        assert len(powers) <= 96


def scale(x, h):
    return tuple(h * a % 32 for a in x)


def weight_tuples(kind):
    xi = unit_powers((1, 0, 1, 0))
    phi = unit_powers((0, 1, 0, 0))
    theta = unit_powers((3, 0, -1, 2))
    sqrt_five = (-1, 2, 0, 0)
    quartic_units = set()
    for i, j, l in product(range(len(xi)), range(0, len(phi), 3), range(len(theta))):
        if (i + l) % 2 != 1:
            continue
        d = (j + l) % 2
        seed = sqrt_five if d else field_one
        v = mul4(mul4(xi[i], phi[j]), mul4(theta[l], seed))
        inv = mul4(mul4(xi[-i], phi[-j]), mul4(theta[-l], seed))
        for h in range(1, 32, 2):
            quartic_units.add((scale(v, h), scale(inv, pow(5**d * h, -1, 32))))
    quadratic_units = set()
    for j, k in product(range(3, len(phi), 6), range(1, 32, 2)):
        v = mul4(phi[j], sqrt_five)
        inv = mul4(phi[-j], sqrt_five)
        quadratic_units.add((scale(v, k), scale(inv, pow(5 * k, -1, 32))))

    data = set()
    for v, inv in quartic_units:
        assert red(mul4(v, inv), 32) == field_one
        c = scale(mul4(epsilon, inv), 2)
        units = [scale(mul4(conjugate(v, j, l), inv), (-1)**l)
                 for j, l in ((1, 0), (0, 1), (1, 1))]
        weights = normfield(*v)
        if kind == "R":
            if (weights[0] + 2) % 32 == 8:
                data.add((red(weights + (1, 1), 32), (c + (2, 2), *(u + (1, 1) for u in units))))
        else:
            for w, winv in quadratic_units:
                assert red(mul4(w, winv), 32) == field_one
                a, b = w[:2]
                if (weights[0] + 2*a + b) % 32 != 8:
                    continue
                conjugate_unit = red(mul4(conjugate(w, 1, 0), winv), 32)[:2]
                marks = (c + scale(winv[:2], 2), units[0] + conjugate_unit,
                         units[1] + (1, 0), units[2] + conjugate_unit)
                data.add((red(weights + (2*a+b, a+3*b), 32), marks))
    assert len(data) == (4096 if kind == "R" else 262144)
    return data


def models(kind):
    data = list(weight_tuples(kind))
    weights = np.array([w for w, _ in data], dtype=np.int64)
    marks = np.array([m for _, m in data], dtype=np.int64)
    del data
    for basis, inverse, table, raw_products in lattices(kind):
        # Vectorized integer products are exact: weights and marks have entries at
        # most 31. The assertions below bound every product by less than 2^40.
        assert max(abs(basis).max(), abs(inverse).max(), abs(raw_products).max()) < 10000
        valid = np.all((weights @ basis) % 8 == 0, axis=1)
        coordinate_num = marks[valid] @ inverse.T
        integral = np.all(coordinate_num % 8 == 0, axis=(1, 2))
        if not integral.any():
            continue
        coordinates = coordinate_num[integral] // 8 % 4
        gram = weights[valid][integral] @ raw_products.reshape(36, 6).T
        assert not (gram % 8).any()
        records = np.c_[gram // 8 % 4, coordinates.reshape(-1, 24)]
        yield inverse, table, np.unique(records, axis=0)


def signatures(kind):
    result = set()
    one = np.array([1, 0, 0, 0, 1, int(kind == "R")], dtype=np.int64)
    for inverse, table, data in models(kind):
        unit_numerator = inverse @ one
        assert not (unit_numerator % 8).any()
        unit = unit_numerator // 8
        squares = np.einsum("ni,nj,ijk->nk", BINARY_POINTS, BINARY_POINTS, table) % 4
        for row in data:
            gram = row[:36].reshape(6, 6)
            c, j, l, m = row[36:].reshape(4, 6)
            norm = int(c @ gram @ c) % 4
            if kind == "R":
                assert norm == 3
            if norm != 3:
                continue
            c_squares = np.einsum("ni,j,ijk->nk", squares, c, table) % 4
            def count(points, target):
                return int(np.all((points - target) % 4 == 0, axis=1).sum())
            result.add((count(squares, c-l), count(squares, -unit-c), count(c_squares, 2*j+2*m-c)))
    return result


if __name__ == "__main__":
    ordinary, signed = signatures("R"), signatures("T")
    print("ordinary", sorted(ordinary))
    print("signed", sorted(signed))
    assert ordinary == {(0,0,8), (1,0,8), (1,0,16), (1,1,0)}
    assert signed == {(0,0,0), (0,0,16), (0,1,8)}
    assert not ordinary & signed
