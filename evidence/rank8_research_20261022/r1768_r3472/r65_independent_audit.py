#!/usr/bin/env python3
"""Independent finite checks for the R65 pointed-phase exclusion.

The cone class is imported read-only; this audit independently checks its
allowed support, all explicit column pairings, the pointed data and all-order
trace types, for all four associator classes, including k=0.  No optimization.
"""
from fractions import Fraction as Q
from hashlib import sha256
import itertools
import json
from math import gcd
from pathlib import Path
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R65 = HERE.parent / "r65"
sys.path.insert(0, str(R65))
from pointed_phase_cone import PointedPhaseCone


def require(condition, message):
    if not condition:
        raise ValueError(message)


def direct_trace_types():
    """Average all powers of zeta_40 over automorphisms fixing sqrt(5)."""
    x = s.Symbol("x")
    polynomial = s.Poly(s.cyclotomic_poly(40, x), x)
    def reduce(expr):
        return s.rem(s.Poly(expr, x), polynomial).as_expr()
    radical = reduce(1 + 2*(x**8 + x**32))
    require(reduce(radical**2) == 5, "wrong sqrt(5) in cyclotomic field")
    automorphisms = [a for a in range(40) if gcd(a, 40) == 1 and s.kronecker_symbol(5, a) == 1]
    require(len(automorphisms) == 8, "wrong relative trace degree")
    radical_coefficients = s.Poly(radical, x)
    pivot = next(i for i in range(1, 16) if radical_coefficients.nth(i))
    def coordinates(expr):
        p = s.Poly(reduce(expr), x)
        b = p.nth(pivot) / radical_coefficients.nth(pivot)
        a = p.nth(0) - b*radical_coefficients.nth(0)
        require(s.expand(p.as_expr()-a-b*radical) == 0, "trace outside quadratic field")
        return (Q(str(a)), Q(str(b)))
    result = {tuple((Q(0), Q(0)) for _ in range(4))}
    for exponent in range(40):
        result.add(tuple(coordinates(sum(x**((exponent*a*k) % 40) for a in automorphisms)/8)
                         for k in range(1, 5)))
    return result


def main():
    census_path = ROOT / "evidence/rank8_m3_20261021/pipeline/census_m3.json"
    census = {r["id"]: r for r in json.loads(census_path.read_text())}
    source = census["R8_3_65"]
    R = source["tensor"]
    dual = [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    pointed = [i for i in range(8) if all(sum(R[i][j]) == 1 for j in range(8))]
    require(pointed == [0, 1, 2, 7], "wrong pointed support")
    powers = [0]
    for _ in range(4):
        powers.append(R[powers[-1]][1].index(1))
    require(powers == [0, 1, 7, 2, 0], "pointed group not the stated C4")
    # Direct F I(X)=sum_j X_j X X_j* expansion, independent of Casimir helper.
    B = [[sum(R[j][i][a]*R[a][dual[j]][k] for j in range(8) for a in range(8))
          for k in range(8)] for i in range(8)]
    require([[B[i][j] for j in pointed] for i in pointed] ==
            [[8*int(i == j) for j in range(4)] for i in range(4)], "pointed induction Gram")
    # Work in Z[d]/(d^2-11d-1) to verify every source dimension equation.
    dims = [(1, 0) if i in pointed else (0, 1) for i in range(8)]
    def mul(u, v):
        a,b = u; c,d = v
        return (a*c+b*d, a*d+b*c+11*b*d)
    for i,j in itertools.product(range(8), repeat=2):
        require(mul(dims[i], dims[j]) ==
                tuple(sum(R[i][j][k]*dims[k][t] for k in range(8)) for t in (0,1)),
                "source FP dimension character")
    D = tuple(sum(mul(v,v)[t] for v in dims) for t in (0,1))
    require(D == (8,44), "global dimension mismatch")
    # Direct standard cyclic cocycle indicator exponents, modulo four.
    cyclic = []
    for k in range(4):
        exponents = []
        for a,n in ((1,4),(3,4),(2,2)):
            exponents.append(sum(k*a*(((j*a)%4+a)//4) for j in range(n)) % 4)
        require(exponents == [k,k,(2*k)%4], "cyclic indicator class formula")
        cyclic.append(exponents)

    direct = direct_trace_types()
    reports = []
    for filename, k, fourier, count in (("pointed_phase_k0_fourier.json",0,True,2413),
                                       ("pointed_phase_k1_fourier.json",1,True,1992),
                                       ("pointed_phase_k2.json",2,False,2222)):
        path = R65 / filename
        data = json.loads(path.read_text())
        C = PointedPhaseCone(R,k,fourier)
        require(C.a["B"].tolist() == B, "imported Gram differs from direct tensor expansion")
        require({tuple(t) for t in C.types} == direct and len(direct) == 13,
                "all-order type domain differs from independent cyclotomic averaging")
        # Reconstruct the extra allowed-column mask independently.
        allowed = set(range(C.offset)) | set(range(C.high_end,C.nvars))
        for orbit_index, orbit in enumerate(C.orbits):
            for ti, traces in enumerate(C.types):
                good = True
                for j in orbit:
                    v = C.a["high"][j][0]
                    if v[0] or v[1]:
                        targets = ([[(0,0)]*4] if k == 1 else [[(0,0),(0,0),(0,0),(-1,0)]] if k == 2 else [
                            [(1,0)]*4, [(-1,0),(1,0),(-1,0),(1,0)], [(0,0),(-1,0),(0,0),(1,0)]])
                        good &= traces in targets
                        if fourier:
                            good &= (v[0]+v[1] == 1 and sum(v[t] for t in (2,3,4,5)) <= 11)
                    if v[6]:
                        targets = [[(0,0),(-1,0),(0,0),(1,0)]] if k == 1 else [
                            [(1,0)]*4, [(-1,0),(1,0),(-1,0),(1,0)]]
                        good &= traces in targets
                if good:
                    allowed.add(C.offset+orbit_index*C.nt+ti)
        require(allowed == C.allowed and len(allowed) == count, "allowed support mismatch")
        expected = [[0,0,0,0,1,e,(-1 if k == 1 else 1)] for e in (-1,1)]
        require([b["indicators"] for b in data["branches"]] == expected, "missing indicator branches")
        branch_reports = []
        for b in data["branches"]:
            require(b["status"] == "exact_infeasible", "nonexclusion branch")
            y = b["certificate"]["y"]
            require(len(y) == C.nrows and all(type(v) is int for v in y), "invalid integer ray")
            # Explicit independent full scan, without the producer's oracle.
            values = [sum(y[row]*coefficient for row,coefficient in C.column(i).items())
                      for i in sorted(allowed)]
            rhs_value = sum(u*v for u,v in zip(y,C.rhs_for(b["indicators"])))
            require(min(values) >= 0 and rhs_value < 0, "Farkas contradiction fails")
            require(rhs_value == b["certificate"]["bTy"], "RHS pairing mismatch")
            branch_reports.append({"indicators":b["indicators"],"minimum_column_pairing":min(values),
                                   "rhs_pairing":rhs_value})
        reports.append({"file":str(path.relative_to(ROOT)),"sha256":sha256(path.read_bytes()).hexdigest(),
                        "allowed_columns":len(allowed),"branches":branch_reports})

    out = {"verdict":"PASS; all four pointed associator classes directly covered by six exact separators",
           "source_tensor_sha256":source["tensor_sha256"],"pointed_indices":pointed,
           "generator_powers":powers,"pointed_Gram":[[B[i][j] for j in pointed] for i in pointed],
           "global_dimension_in_basis_1_d":D,"cyclic_indicator_exponents_mod_4":cyclic,
           "independent_joint_trace_types":len(direct),"trace_order_representatives_divide":40,
           "new_separators":reports}
    (HERE/"r65_independent_audit.json").write_text(json.dumps(out,indent=2)+"\n")
    print("PASS: direct pointed Gram and FP dimensions; cyclic classes; 13 independent trace types; six full-column separators covering all four associator classes")


if __name__ == "__main__":
    main()
