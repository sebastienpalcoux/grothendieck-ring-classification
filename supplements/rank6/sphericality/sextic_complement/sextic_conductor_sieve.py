#!/usr/bin/env python3
"""Exact necessary conductor conditions for full-degree rank-six categories.

Check all conductor pairs in the proved ranges a < 578 and b < 121.

The ordinary reciprocal codegrees have trace one and Fourier bounds
    |p_hat(eta)|^2 <= gcd(conductor(eta), 2) / conductor(eta).
For quadratic conductor a, cubic conductor b, c=lcm(a,b), h=gcd(a,2),
all six coordinates are at least
    m=(1-sqrt(h/a)-2/sqrt(b)-2*sqrt(h/c))/6.
If m>0, their product is at least m^5*(1-5*m), but is at most
1/(a*b^2*c^2). Reciprocal square roots are rounded upward using integer
square roots, so every rejection is an exact rational implication.

The trace-form norm identity also forces the quadratic subfield to contain
an element of rational norm -1. Its squarefree radicand therefore has no
prime congruent to 3 modulo 4. This removes 53 of the 94 Fourier candidates.
"""

from fractions import Fraction
from math import gcd, isqrt, lcm
import json
from pathlib import Path


def factor(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def squarefree(n):
    return all(e == 1 for e in factor(n).values())


def positive_fundamental_discriminant(a):
    return ((a % 4 == 1 and squarefree(a)) or
            (a % 4 == 0 and (a//4) % 4 in (2, 3) and squarefree(a//4)))


def cubic_conductor(b):
    return b > 1 and all((p == 3 and e == 2) or
                        (p % 3 == 1 and e == 1)
                        for p, e in factor(b).items())


def norm_obstruction_primes(a):
    """Odd primes obstructing rational norm -1 in Q(sqrt(a))."""
    return [p for p in factor(a) if p % 4 == 3]


def reciprocal_sqrt_upper(n):
    scale = 10**15
    return Fraction(scale, isqrt(n*scale*scale))


def sqrt_ratio_upper(numerator, denominator):
    scale = 10**15
    return Fraction(isqrt(numerator*denominator*scale*scale)+1,
                    denominator*scale)


def alpha_trace_bounds(retained):
    """Certified ratio-trace bounds from pair masses and the mixed estimate.

    The identity embedding is chosen with q_0 minimal and p_0<=q_0.
    If all q_k (k!=0) are >=beta>0, then Tr(alpha)<1+1/beta.
    At even conductors, 2*p_0+q_0+q_2 has the mixed lower bound B/6;
    since it is <=4*q_2, q_2>=B/24. This bounds two further retained fields.
    """
    out = []
    for row in retained:
        a, b, c = (row[key] for key in
                   ("quadratic_conductor", "cubic_conductor", "sextic_conductor"))
        h = gcd(a, 4)
        aa, cc = a//h, c//h
        beta1 = (1-reciprocal_sqrt_upper(b)-sqrt_ratio_upper(3, cc))/6
        beta2 = (1-reciprocal_sqrt_upper(aa)-reciprocal_sqrt_upper(b)
                 -reciprocal_sqrt_upper(cc))/6
        beta3 = (1-2*reciprocal_sqrt_upper(b))/6
        method = "separate"
        if a % 2 == 0:
            mixed = (4-2*sqrt_ratio_upper(6, a)-6*reciprocal_sqrt_upper(b)
                     -4*sqrt_ratio_upper(3, c))/24
            if mixed > beta2:
                beta2 = mixed
                method = "mixed"
        beta = min(beta1, beta2, beta3)
        cap = None
        if beta > 0:
            strict_bound = 1+1/beta
            cap = ((strict_bound.numerator+strict_bound.denominator-1)
                   //strict_bound.denominator-1)
        out.append(dict(row, alpha_trace_bound=cap, trace_bound_method=method))
    return out


def sieve():
    quadratic = [a for a in range(5, 578)
                 if positive_fundamental_discriminant(a)]
    cubic = [b for b in range(7, 121) if cubic_conductor(b)]
    retained = []
    for a in quadratic:
        for b in cubic:
            c = lcm(a, b)
            h = gcd(a, 2)
            upper = (reciprocal_sqrt_upper(a//h)
                     + 2*reciprocal_sqrt_upper(b)
                     + 2*reciprocal_sqrt_upper(c//h))
            lower = (1-upper)/6
            discriminant = a*b*b*c*c
            if lower > 0 and discriminant*lower**5*(1-5*lower) > 1:
                continue
            retained.append({"quadratic_conductor": a,
                             "cubic_conductor": b,
                             "sextic_conductor": c,
                             "field_discriminant": discriminant})
    return len(quadratic)*len(cubic), retained


if __name__ == "__main__":
    # Exact endpoint inequalities used to justify the unbounded search cutoff.
    a_lower = Fraction(9, 850)
    b_lower = Fraction(1, 44)
    assert 49*578**3*a_lower**5*(1-5*a_lower) > 1
    assert 5*121**4*b_lower**5*(1-5*b_lower) > 1
    tested, fourier_retained = sieve()
    assert len(fourier_retained) == 94
    retained = [r for r in fourier_retained
                if not norm_obstruction_primes(r["quadratic_conductor"])]
    removed = [dict(r, obstructing_primes=norm_obstruction_primes(r["quadratic_conductor"]))
               for r in fourier_retained
               if norm_obstruction_primes(r["quadratic_conductor"])]
    assert len(retained) == 41 and len(removed) == 53
    assert {r["cubic_conductor"] for r in retained} == {7, 9, 13, 19, 31, 37, 43}
    # Each surviving cubic conductor has exactly one cyclic cubic field.
    assert all(len(factor(r["cubic_conductor"])) == 1 for r in retained)
    destination = Path(__file__).with_name("sextic_conductor_candidates.json")
    destination.write_text(json.dumps(retained, indent=2) + "\n")
    Path(__file__).with_name("sextic_norm_exclusions.json").write_text(
        json.dumps(removed, indent=2) + "\n")
    traces = alpha_trace_bounds(retained)
    assert sum(r["alpha_trace_bound"] is not None for r in traces) == 38
    assert max(r["alpha_trace_bound"] or 0 for r in traces) == 1037
    assert {(r["quadratic_conductor"], r["cubic_conductor"])
            for r in traces if r["alpha_trace_bound"] is None} == {
                (8, 7), (8, 9), (8, 13)}
    Path(__file__).with_name("sextic_trace_bounds.json").write_text(
        json.dumps(traces, indent=2) + "\n")
    print(f"Exact conductor sieve: {tested} pairs tested; 94 pass the Fourier test;")
    print(f"53 fail the rational norm obstruction; {len(retained)} fields retained.")
    print("Largest surviving quadratic, cubic and sextic conductors:",
          *(max(r[key] for r in retained) for key in
            ("quadratic_conductor", "cubic_conductor", "sextic_conductor")))
    print("Exact ratio-trace bounds: 38 fields bounded; largest bound 1037; 3 unresolved.")
