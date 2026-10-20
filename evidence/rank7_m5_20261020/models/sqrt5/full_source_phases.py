#!/usr/bin/env python3
"""Exact relative two-moment phases over two multiquadratic fields.

phase_records('L4') returns 22 records: 21 nonzero pairs obtained in Q(zeta_80)
and the zero pair for higher 2/5-primary orders. Coordinates are scaled by 8
in the ordered basis (1,sqrt(5),sqrt(-2),sqrt(-10)), first moment then second.
The fixed-row multiplicity restrictions require the categorical Galois
action described in FULL_SOURCE_PHASES_PROOF.md.

phase_records('F8') uses Q(sqrt(5),sqrt(2),i), returns 37 records, and uses
basis (1,sqrt(5),sqrt(2),sqrt(10),i,i*sqrt(5),i*sqrt(2),i*sqrt(10)).
The default L4 is retained for compatibility; F8 is the stronger unified set.
"""
from functools import lru_cache
import argparse
import json
import math
from pathlib import Path

import sympy as s

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def chi_minus8(value):
    require(value % 2 == 1, "odd input for the conductor-eight character")
    return 1 if value % 8 in (1, 3) else -1


@lru_cache(maxsize=2)
def phase_records(field="L4"):
    """Return exact integer phase tuples and their order/multiplicity provenance."""
    x = s.Symbol("x")
    modulus = s.Poly(s.cyclotomic_poly(80, x), x, domain=s.QQ)
    require(modulus.degree() == 32, "cyclotomic degree")
    def reduce(value):
        return s.Poly(value, x, domain=s.QQ).rem(modulus)
    unit = reduce(1)
    sqrt5 = reduce(1 + 2*(x**16 + x**64))
    sqrt_minus2 = reduce(x**10 + x**30)
    sqrt_minus10 = reduce(sqrt5.as_expr() * sqrt_minus2.as_expr())
    if field == "L4":
        basis = [unit, sqrt5, sqrt_minus2, sqrt_minus10]
        subgroup = [1, 9, 11, 19, 41, 49, 51, 59]
        expected_count = 21
    elif field == "F8":
        sqrt2 = reduce(x**10 + x**70)
        imaginary_unit = reduce(x**20)
        require(reduce(sqrt2.as_expr()**2).as_expr() == 2, "sqrt-two embedding")
        require(reduce(imaginary_unit.as_expr()**2).as_expr() == -1, "imaginary-unit embedding")
        real_basis = [unit, sqrt5, sqrt2, reduce(sqrt5.as_expr()*sqrt2.as_expr())]
        basis = real_basis + [reduce(imaginary_unit.as_expr()*value.as_expr()) for value in real_basis]
        subgroup = [1, 9, 41, 49]
        expected_count = 36
    else:
        raise ValueError("field must be L4 or F8")
    require(reduce(sqrt5.as_expr()**2).as_expr() == 5, "sqrt-five embedding")
    require(reduce(sqrt_minus2.as_expr()**2).as_expr() == -2, "sqrt-minus-two embedding")
    vectors = s.Matrix([[value.nth(j) for value in basis] for j in range(32)])
    require(vectors.rank() == len(basis), "multiquadratic basis independence")
    source_fixing_subgroup = [u for u in range(80) if math.gcd(u, 80) == 1
                and u % 5 in (1, 4) and chi_minus8(u) == 1]
    require(source_fixing_subgroup == [1, 9, 11, 19, 41, 49, 51, 59], "source-fixing Galois subgroup")
    require(len(subgroup)*len(basis) == 32, "relative subgroup index")
    for u in subgroup:
        for value in basis:
            require(reduce(value.as_expr().subs(x, x**u)) == value, "fixed field basis")
    @lru_cache(maxsize=None)
    def relative_trace(exponent):
        value = reduce(sum(x**((exponent*u) % 80) for u in subgroup) / len(subgroup))
        coefficients = vectors.gauss_jordan_solve(s.Matrix([value.nth(j) for j in range(32)]))[0]
        require(all(coefficient.is_Rational for coefficient in coefficients), "rational phase coordinates")
        return tuple(coefficients)
    grouped = {}
    for k in range(80):
        raw = relative_trace(k) + relative_trace(2*k)
        scaled = tuple(8*value for value in raw)
        require(all(value.is_Integer for value in scaled), "scale-eight integrality")
        scaled = tuple(map(int, scaled))
        grouped.setdefault(scaled, []).append(k)
    require(len(grouped) == expected_count and (0,)*(2*len(basis)) not in grouped,
            "complete nonzero finite phase list")
    if field == "F8":
        def coordinates(value):
            polynomial = reduce(value)
            answer = vectors.gauss_jordan_solve(s.Matrix([polynomial.nth(j) for j in range(32)]))[0]
            require(all((8*z).is_Integer for z in answer), "closed-form phase scale")
            return tuple(int(8*z) for z in answer)
        xi = x**10
        cases = [(1, 1)] + [((-1+delta*sqrt5.as_expr())/4,
                            (-1-delta*sqrt5.as_expr())/4) for delta in (-1, 1)]
        closed_form = {coordinates(xi**j*c1) + coordinates(xi**(2*j)*c2)
                       for j in range(8) for c1, c2 in cases}
        closed_form.update((0,)*8 + coordinates(xi**j*c1)
                           for j in (1, 3, 5, 7) for c1, c2 in cases)
        require(len(closed_form) == 36 and closed_form == set(grouped),
                "24 plus 12 closed-form phase description")
    records = []
    for scaled, exponents in sorted(grouped.items()):
        orders = sorted({80 // math.gcd(80, k) for k in exponents})
        require(len(orders) == 1, "unique order provenance of finite phase")
        order = orders[0]
        multiple = 2 if order in (16, 80) else 1
        # Automorphisms fixing the entire source field act by squares on twists.
        for k in exponents:
            orbit = {(k*u*u) % 80 for u in source_fixing_subgroup}
            require(len(orbit) == multiple, "fixed-row square-action orbit size")
            require(all(relative_trace(j) + relative_trace(2*j)
                        == tuple(s.Rational(v, 8) for v in scaled) for j in orbit),
                    "relative phase invariant under square action")
        records.append({"scaled8": scaled, "orders": orders, "exponents80": exponents,
                        "fixed_row_multiple": multiple, "zero_semigroup": None})
    records.append({"scaled8": (0,)*(2*len(basis)), "orders": [], "exponents80": [],
                    "fixed_row_multiple": 1, "zero_semigroup": [4, 5],
                    "order_condition": "2^a*5^b with a>=5 or b>=2"})
    return records


def phases_scaled8(field="L4"):
    """Return the phase tuples, with the genuine zero phase last."""
    return [record["scaled8"] for record in phase_records(field)]


def receipt(field="L4"):
    bases = {"L4": ["1", "sqrt(5)", "sqrt(-2)", "sqrt(-10)"],
             "F8": ["1", "sqrt(5)", "sqrt(2)", "sqrt(10)", "i", "i*sqrt(5)", "i*sqrt(2)", "i*sqrt(10)"]}
    return {
        "schema": "relative-full-source-field-two-moments-v1",
        "field": "Q(sqrt(5),sqrt(-2))" if field == "L4" else "Q(sqrt(5),sqrt(2),i)", "basis": bases[field],
        "scale": 8, "cyclotomic_modulus": 80, "cyclotomic_degree": 32,
        "relative_subgroup": [1, 9, 11, 19, 41, 49, 51, 59] if field == "L4" else [1, 9, 41, 49],
        "nonzero_phase_count": len(phase_records(field))-1, "total_phase_count": len(phase_records(field)),
        "phases": phase_records(field),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-receipt", action="store_true")
    parser.add_argument("--field", choices=("L4", "F8"), default="L4")
    args = parser.parse_args()
    result = json.loads(json.dumps(receipt(args.field)))
    path = HERE / ("full_source_phases_certificate.json" if args.field == "L4" else "maximal_multiquadratic_phases_certificate.json")
    if args.write_receipt:
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        require(json.loads(path.read_text()) == result, "relative phase receipt mismatch")
    print(f"PASS: all 80 roots, {result['nonzero_phase_count']} nonzero {args.field} phase pairs, square-action row multiplicities, plus higher-order zero")


if __name__ == "__main__":
    main()
