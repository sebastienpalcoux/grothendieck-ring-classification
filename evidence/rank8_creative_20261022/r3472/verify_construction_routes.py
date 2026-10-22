#!/usr/bin/env python3
"""Exact arithmetic receipt for the scoped cyclic-parent obstruction.

The categorical lemma is proved in CONSTRUCTION_ROUTES.md; this script
checks its two specializations and deliberately makes no target exclusion.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def mul(x, y, field):
    a, b = x
    c, d = y
    return (a*c + field*b*d, a*d + b*c)


def scale(x, k):
    return tuple(k*v for v in x)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def pair(x):
    return [str(v) for v in x]


def receipt():
    rows = []
    for rid, g, field, radical_coefficient, target in [
        ('R8_3_1768', 6, 37, 1, (444, 72)),
        ('R8_3_3472', 7, 2, 5, (700, 490)),
    ]:
        delta = (Q(g), Q(radical_coefficient))
        d2 = mul(delta, delta, field)
        need(d2 == add((Q(1), Q(0)), scale(delta, 2*g)), 'GNG dimension relation')
        n, h = 4*g*g, 4*g
        rho = scale(delta, 2*g)
        rho2 = mul(rho, rho, field)
        need(rho2 == add((Q(n), Q(0)), scale(rho, n)), 'Near-group dimension relation')
        target_d = scale(add((Q(1), Q(0)), d2), g)
        need(target_d == target, 'Target global dimension')
        parent_d = add((Q(n), Q(0)), rho2)
        need(parent_d == scale(target_d, h), 'Parent quotient scalar match')
        forced = scale(rho, Q(1, h))
        norm = forced[0]*forced[0] - field*forced[1]*forced[1]
        trace = 2*forced[0]
        need(norm == Q(-1, 4) and trace == g, 'Exact nonintegrality certificate')
        need(norm.denominator != 1, 'Nonintegral norm')
        need(mul(forced, forced, field) == add(scale(forced, g), (Q(1, 4), Q(0))),
             'Quadratic polynomial identity')
        # A character-group image of order h is the unique subgroup of C_n.
        generator = n//h
        need(n % h == 0 and generator == g, 'Cyclic subgroup generator')
        rows.append({
            'id': rid,
            'quadratic_field_radicand': field,
            'g': g,
            'delta_coefficients': pair(delta),
            'target_global_dimension_coefficients': pair(target_d),
            'near_group_parent_group_order_and_multiplicity': n,
            'parent_noninvertible_dimension_coefficients': pair(rho),
            'parent_global_dimension_coefficients': pair(parent_d),
            'required_deequivariantization_order': h,
            'pointed_subgroup_generator': generator,
            'forced_descendant_dimension_coefficients': pair(forced),
            'forced_descendant_trace': str(trace),
            'forced_descendant_norm': str(norm),
            'forced_descendant_monic_minimal_polynomial': f'x^2 - {g}*x - 1/4',
            'outcome': 'direct_ordinary_cyclic_near_group_parent_route_excluded',
            'general_categorification_status': 'unresolved',
            'new_target_model': False,
        })
    return {
        'schema': 'rank8-creative-cyclic-parent-route/v1',
        'status': 'PASS',
        'arithmetic': 'exact rational pairs; no floating point',
        'scope': 'direct ordinary de-equivariantization from cyclic NG(C_(4g^2),4g^2)',
        'categorical_proof': 'evidence/rank8_creative_20261022/r3472/CONSTRUCTION_ROUTES.md',
        'excluded_target_fusion_rings': [],
        'constructed_target_fusion_categories': [],
        'noncyclic_parent_routes_excluded': False,
        'arbitrary_morita_routes_excluded': False,
        'records': rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = receipt()
    path = Path(__file__).with_name('construction_routes.json')
    raw = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.write:
        path.write_text(raw)
    else:
        need(path.read_text() == raw, 'Saved construction-route receipt differs')
    print(raw, end='')


if __name__ == '__main__':
    main()
