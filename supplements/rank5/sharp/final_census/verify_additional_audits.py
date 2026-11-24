"""Optional targeted audits of certificates, dimension bounds and enclosures.

The trace check computes Galois averages directly in cyclotomic quotient
rings. The column check compares direct Cartesian enumeration with the
optimized joins/native Gram enumeration. The enclosure check uses rational
interval arithmetic with no heuristic padding. The dimension-bound check
compares exact root isolation with shifted-polynomial coefficients. These
checks share the package's generators, algebraic field data and restriction-
column construction, and do not independently prove the categorical
hypotheses behind the certificates.
No stored exclusion is changed, and no network access is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import itertools
import json
import math
import os
import subprocess
import sys
import tempfile

import sympy as s

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / "criteria"), str(ROOT / "generator"), str(ROOT.parent / "checks")]
from exact import VerificationError, require, discover_roots, check_roots
from rings import Characters, codegree_poly, validate
from induction import restriction_columns, low_matrices
from decisions import check_subring
from dimension_test import at_most_sharp_bound
from export_tables import tensor
from models import dihedral14
import higher_traces as ht
import small_simple as ss


def subring_input_check():
    R = dihedral14()
    validate(R)
    # -4 aliases basis index 1. Without an index-range check this counts
    # the same invertible twice, inventing dimension 3 instead of 2.
    invalid = {"kind": "subring", "subset": [0, 1, -4],
               "quotient_polynomial": ["1", "-14/3"]}
    try:
        check_subring(R, invalid)
    except VerificationError:
        pass
    else:
        raise VerificationError("invalid subring certificate excluded the realized Rep(D14) ring")
    print("Certificate input: invalid subring indices rejected for Rep(D14).", flush=True)


def quadratic_cutoff_check():
    # For gamma >= 3, J >= 2 already forces s <= 1/4.
    require(1-Q(3, 4)-Q(2, 9) <= Q(1, 4), "invalid finite gamma cutoff")
    masses = [1-Q(gamma, 4)-Q(J, 9) for gamma in (1, 2) for J in (2, 4)
              if 1-Q(gamma, 4)-Q(J, 9) > Q(1, 4)]
    lower = min(masses)
    require(lower == Q(5, 18), "incorrect lower bound in the M=9 quadratic subcase")
    lhs = 2*(lower-Q(2, 120))**2+Q(32, 81)
    require(lhs == Q(8609, 16200) and lhs > Q(1, 2), "the repaired E<=120 contradiction failed")
    print(f"Quadratic cutoff: least mass {lower}; contradiction margin {lhs-Q(1, 2)}.", flush=True)


def dimension_cutoff_check():
    # Compare the largest root with 48+24*sqrt(3), using isolating intervals
    # and its minimal polynomial rather than the shifted-coefficient test.
    def compare_rational(r):
        if r <= 48:
            return 1
        gap = 1728-(r-48)**2
        return 1 if gap > 0 else -1

    def root_test(polynomial):
        variable = polynomial.gen
        endpoint = s.Poly(variable**2-96*variable+576, variable)
        lo, hi = max((interval for interval, multiplicity in
                      polynomial.intervals(eps=s.Rational(1, 10**8))),
                     key=lambda interval: interval[1])
        for _ in range(100):
            if compare_rational(hi) > 0:
                return True, False
            if compare_rational(lo) < 0:
                return False, False
            if polynomial.rem(endpoint).is_zero:
                return True, True
            lo, hi = polynomial.refine_root(lo, hi, steps=4)
        raise VerificationError("could not separate the largest root from the sharp endpoint")

    generated = within = equal = 0
    with tempfile.TemporaryDirectory() as temporary:
        for kind in ("selfdual", "nonselfdual"):
            binary = Path(temporary) / kind
            source = ROOT / "generator" / f"enumerate_{kind}.cpp"
            subprocess.run(["g++", "-O3", "-std=c++17", "-fopenmp", str(source),
                            "-o", str(binary)], check=True, capture_output=True)
            run = subprocess.run([str(binary), "4"], check=True, capture_output=True, text=True)
            for line in run.stdout.splitlines():
                R = tensor(5, line, ROOT / "generator")
                validate(R)
                polynomial = codegree_poly(R)
                passes, equality = root_test(polynomial)
                require(passes == at_most_sharp_bound(polynomial.all_coeffs()),
                        "dimension cutoff differs from exact root isolation")
                generated += 1
                within += passes
                equal += equality
    require((generated, within, equal) == (269, 114, 3), "incorrect dimension-bound audit coverage")
    print(f"Sharp dimension cutoff: {generated} rings checked by exact root isolation; "
          f"{within} within bound; {equal} at the exact endpoint.", flush=True)


def trace_check():
    q, conductor, height = 3, 12, 6
    expected, bound = ht.trace_types(q, [2, 3], height)
    require(bound == 144, "incorrect conductor-12, height-six order cutoff")
    X = s.Symbol("X")
    answer, trials = set(), 0
    for n in s.divisors(bound):
        n = int(n)
        M = math.lcm(n, conductor)
        P = s.Poly(s.cyclotomic_poly(M, X), X, domain=s.QQ)
        subgroup = [u for u in range(M) if math.gcd(u, M) == 1
                    and s.kronecker_symbol(conductor, u) == 1]
        gauss = sum(s.kronecker_symbol(conductor, u)*X**(u*(M//conductor))
                    for u in range(conductor) if math.gcd(u, conductor) == 1)
        radical = s.Poly(gauss/math.isqrt(conductor//q), X, domain=s.QQ).rem(P)
        j = next(j for j in range(1, P.degree()) if radical.nth(j))
        for a in range(n):
            if math.gcd(a, n) != 1:
                continue
            values = []
            for k in range(1, height+1):
                value = s.Poly(sum(X**((a*(M//n)*k*u) % M) for u in subgroup)
                               / len(subgroup), X, domain=s.QQ).rem(P)
                b = value.nth(j)/radical.nth(j)
                rational = value-b*radical
                require(rational.degree() <= 0, "direct trace did not land in the quadratic field")
                values.append((Q(rational.nth(0)), Q(b)))
                trials += 1
            answer.add(tuple(values))
    zero = tuple((Q(0), Q(0)) for _ in range(height))
    require(answer | {zero} == set(expected), "relative-trace vectors differ from direct Galois averages")
    print(f"Relative traces: {trials} exact moments, {len(expected)} joint vectors, conductor {conductor}.", flush=True)


def positive_gram(columns, B):
    L = s.Matrix.hstack(*map(s.Matrix, columns))
    residual = B-L*L.T
    return (all(x >= 0 for x in residual)
            and all(residual.extract(ix, ix).det() >= 0
                    for size in range(1, 5) for ix in itertools.combinations(range(1, 5), size)))


def column_check():
    records = json.loads((ROOT / "data/bounded_witnesses.json").read_text())
    require(len(records) == 114, "incomplete bounded witness table")
    rings = grams = 0
    for record in records:
        kind = record.get("exclusion", {}).get("kind")
        if kind not in ("induction", "finite_indicator_traces"):
            continue
        R = record["N"]
        validate(R)
        ch = Characters(R)
        f, K, ds, D, pD, embedding = ch.fp()
        roots = discover_roots(codegree_poly(R), K)
        require(roots is not None, "codegrees do not split in the dimension field")
        check_roots(codegree_poly(R), K, roots)
        roots.remove(D)
        choices = [restriction_columns(ds, D/r, K, ch.C) for r in roots]
        direct = []
        for tail in itertools.product(*choices):
            if any(choices[a] == choices[b] and tail[a] > tail[b]
                   for a in range(4) for b in range(a+1, 4)):
                continue
            columns = ((1, 0, 0, 0, 0),)+tail
            if all(sum(v[j] for v in columns) == ch.C[0, j] for j in range(5)):
                direct.append(columns)
        direct.sort()
        require(low_matrices(choices, ch.C) == direct, "optimized low-column join omitted a Cartesian solution")
        require(low_matrices(choices, ch.C, gram_prune=True)
                == [v for v in direct if positive_gram(v, ch.C)], "native Gram pruning differs from exact principal minors")
        rings += 1
        if kind == "finite_indicator_traces":
            data = ht.quadratic_data(R, gram_prune=True)
            previous = os.environ.pop("RANK5_REFERENCE_GRAM", None)
            try:
                for columns in data["lows"]:
                    L = s.Matrix.hstack(*map(s.Matrix, columns))
                    native = ht.high_columns(data, L)
                    os.environ["RANK5_REFERENCE_GRAM"] = "1"
                    reference = ht.high_columns(data, L)
                    del os.environ["RANK5_REFERENCE_GRAM"]
                    require(native == reference, "native and direct high-column enumerations differ")
                    grams += 1
            finally:
                os.environ.pop("RANK5_REFERENCE_GRAM", None)
                if previous is not None:
                    os.environ["RANK5_REFERENCE_GRAM"] = previous
    require((rings, grams) == (14, 11), "incomplete induction/indicator audit coverage")
    print(f"Gram columns: {rings} certificate rings and {grams} residual matrices checked directly.", flush=True)


def iadd(*values):
    return sum(v[0] for v in values), sum(v[1] for v in values)


def ineg(v):
    return -v[1], -v[0]


def imul(v, w):
    values = [a*b for a in v for b in w]
    return min(values), max(values)


def iscale(v, c):
    return imul(v, (Q(c), Q(c)))


def iinv(v):
    require(v[0]*v[1] > 0, "interval reciprocal crosses zero")
    return 1/v[1], 1/v[0]


def isquare(v):
    a, b = v
    return Q(0) if a <= 0 <= b else min(a*a, b*b), max(a*a, b*b)


def integers(v):
    return range(math.ceil(v[0]), math.floor(v[1])+1)


def evaluate(coefficients, t):
    value = (Q(0), Q(0))
    for c in reversed(coefficients):
        value = iadd(imul(value, t), (Q(c), Q(c)))
    return value


def enclosure_check(F, M):
    polynomial = ss.FIELDS[F]
    roots = [(Q(r, ss.SCALE), Q(r+1, ss.SCALE)) for r in ss.roots(polynomial)]
    small, large = roots[:3], roots[3]
    cap = Q(317, 100)
    bounds = [(-cap, cap)]*3+[(Q(2), Q(M))]
    derivatives = [evaluate([polynomial[1], 2*polynomial[2], 3*polynomial[3], 4], t) for t in roots]
    erange = iadd(*(imul(z, iinv(d)) for z, d in zip(bounds, derivatives)))
    cd = cap*sum(max(abs(x) for x in iinv(imul(iadd(t, ineg(u)), iadd(t, ineg(v)))))
                 for t, u, v in itertools.permutations(small, 3))/2
    bd = 2*cap*max(abs(x) for x in iinv(iadd(small[2], ineg(small[0]))))
    r1, r2, r3 = small
    ccenter = ineg(iadd(*small))
    bcenter1 = ineg(iadd(r1, r3))
    bcenter2 = ineg(iadd(isquare(r1), imul(r1, r3), isquare(r3)))
    candidates = set()
    for E in integers(erange):
        for C in integers(iadd(iscale(ccenter, E), (-cd, cd))):
            for B in integers(iadd(iscale(bcenter1, C), iscale(bcenter2, E), (-bd, bd))):
                center = ineg(iadd(iscale(r2, B), iscale(isquare(r2), C), iscale(imul(isquare(r2), r2), E)))
                for A in integers(iadd(center, (-cap, cap))):
                    x = (A, B, C, E)
                    boxes = [evaluate(x, t) for t in roots]
                    if any(v[1] < lo or v[0] > hi for v, (lo, hi) in zip(boxes, bounds)):
                        continue
                    candidates.add(x)
    reported = dict(ss.embedding_boxes(polynomial, M))
    require(candidates <= set(reported), "packaged generator bounds omitted an interval candidate")
    require(all(evaluate(x, large)[1] < hi for x, hi in reported.items()), "reported Perron upper endpoint is not an enclosure")
    print(f"Generator enclosures: conductor {F}, cap {M}, {len(candidates)} interval candidates inside {len(reported)} packaged candidates; all upper endpoints certified.", flush=True)


def main():
    subring_input_check()
    quadratic_cutoff_check()
    dimension_cutoff_check()
    trace_check()
    column_check()
    for F, M in ((15, 125), (15, 155), (20, 153)):
        enclosure_check(F, M)


if __name__ == "__main__":
    main()
