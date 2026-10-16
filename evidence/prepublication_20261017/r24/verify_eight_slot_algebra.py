#!/usr/bin/env python3
"""Finite audit of the proposed R24 repair; no categorical/classification claim."""
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def ga(a, b):
    return (a[0] + b[0], a[1] + b[1])


def gm(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])


def const(a, b=0):
    return {(): (a, b)} if (a, b) != (0, 0) else {}


def var(name):
    return {(name,): (1, 0)}


def add(*polys):
    out = {}
    for p in polys:
        for m, c in p.items():
            out[m] = ga(out.get(m, (0, 0)), c)
    return {m: c for m, c in out.items() if c != (0, 0)}


def mul(a, b):
    out = {}
    for m, c in a.items():
        for n, d in b.items():
            mn = tuple(sorted(m+n))
            out[mn] = ga(out.get(mn, (0, 0)), gm(c, d))
    return {m: c for m, c in out.items() if c != (0, 0)}


def neg(a):
    return mul(const(-1), a)


def coeff(matrix, v):
    i, j, k, l = v
    return matrix[2*i+j][2*k+l]


def p(v):
    i, j, k, l = v
    return k, 1-j, i, 1-l


def c(v):
    i, j, k, l = v
    return j, 1-k, 1-i, l


def c2(v):
    return c(c(v))


def field_add(a, b):
    return a[0]+b[0], a[1]+b[1]


def field_mul(a, b):
    return a[0]*b[0]+5*a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def field_scale(a, k):
    return a[0]*k, a[1]*k


def display(poly):
    return {"*".join(m) or "1": list(k) for m, k in sorted(poly.items())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    zero = {}
    r = var("r0")
    A = [[r,zero,zero,var("aU")], [zero,r,r,zero],
         [zero,r,r,zero], [var("aL"),zero,zero,r]]
    D = [[var("x"),zero,zero,var("Z")],
         [zero,var("X"),var("y"),zero],
         [zero,var("Y"),var("W"),zero],
         [var("z"),zero,zero,var("w")]]
    slots = list(itertools.product(range(2), repeat=4))
    for v in slots:
        need(p(p(v)) == v, "odd slot involution")
        need(c(c(c(v))) == v, "ordinary-face rotation has order three")
        if sum(v) % 2:
            need(coeff(A,v) == coeff(D,v) == {}, "parity zero")
        need(coeff(A,v) == coeff(A,c(v)), "ordinary A symmetry")

    def b(l):
        return const(0, -1 if l == 0 else 1)

    def binv(l):
        return const(0, 1 if l == 0 else -1)

    for l in range(2):
        need(mul(b(l),binv(l)) == const(1), "reciprocal loop factor")

    def AA(v): return coeff(A,v)
    def AV(v): return coeff(A,p(v))
    def DD(v): return coeff(D,v)
    def DV(v): return coeff(D,p(v))
    def BB(v): return mul(b(v[3]),DD(c(v)))
    def BV(v): return mul(binv(v[3]),DV(c(v)))
    def CC(v): return mul(b(v[3]),DD(c2(v)))
    def CV(v): return mul(binv(v[3]),DV(c2(v)))

    def contract(fun, dual, k, l):
        return add(*(mul(fun((i,j,k,l)),dual((i,j,k,l)))
                     for i,j in itertools.product(range(2), repeat=2)))

    xx = mul(var("x"),var("X"))
    ww = mul(var("W"),var("w"))
    yy = mul(var("y"),var("Y"))
    zz = mul(var("z"),var("Z"))
    rr2 = mul(const(2),mul(r,r))
    need(contract(AA,AV,0,1) == rr2, "F0 column01 A")
    need(contract(BB,BV,0,1) == add(xx,ww), "F0 column01 B")
    need(contract(CC,CV,0,0) == add(ww,zz), "F1 column00 C")
    need(contract(DD,DV,0,0) == add(xx,zz), "F1 column00 D")
    need(contract(CC,CV,0,1) == add(ww,yy), "F1 column01 C")
    need(contract(DD,DV,0,1) == add(xx,yy), "F1 column01 D")

    # The odd map is deliberately not commuted with the even transport.
    pc_differs = [v for v in slots if p(c(p(v))) != c(v)]
    need(pc_differs, "test detects danger of silently commuting p and c")

    invd = (Q(-2), Q(1))
    branches = []
    for tau in (1,-1):
        rv = (Q(2+tau,4),Q(-1,4))
        nonzero = field_add(field_mul(rv,rv),field_scale(invd,Q(1,2)))
        expected = (Q(-1,8),Q(1,8)) if tau == 1 else (Q(-5,8),Q(3,8))
        need(nonzero == expected and nonzero != (0,0), "two nonzero branches")
        corner = field_add(field_scale(rv,Q(4)),(Q(-2),Q(1)))
        need(field_mul(corner,corner) == (Q(1),Q(0)), "corner polynomial")
        branches.append({"tau":tau,"r0":[str(v) for v in rv],
                         "yY_equals_zZ":[str(v) for v in nonzero]})

    receipt = {
        "status":"PASS_CONDITIONAL_FINITE_ALGEBRA",
        "classification_decisions":0,
        "categorical_transport_certified":False,
        "D_even_slots":8,
        "D_decorated_even_flips_used":0,
        "decorated_cubic_phases_used":0,
        "independent_opposite_transport_definitions":True,
        "p_c_p_differs_from_c_on_slots":len(pc_differs),
        "F0_col01_A":display(contract(AA,AV,0,1)),
        "F0_col01_B":display(contract(BB,BV,0,1)),
        "F1_col00_total":display(add(contract(CC,CV,0,0),contract(DD,DV,0,0))),
        "F1_col01_total":display(add(contract(CC,CV,0,1),contract(DD,DV,0,1))),
        "scalar_branches":branches,
        "scope":"Checks consequences of separately stated paired categorical transport; does not prove that transport."
    }
    out = json.dumps(receipt,indent=2)+"\n"
    if args.output:
        args.output.write_text(out)
    print(out,end="")


if __name__ == "__main__":
    main()
