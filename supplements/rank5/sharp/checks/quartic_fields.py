"""Quartic fields and rational formal codegrees in every dimension D>17.

Inputs are the rank, the norm identity, and the reciprocal Fourier bounds.
All comparisons are rational and all field-conductor lists are generated.
"""
from fractions import Fraction
from math import gcd, isqrt, prod

Q = Fraction
SCALE = 10**8
MAX_RECIPROCAL = Q(1, 17)
MIN_MASS = Q(3, 4)


def upper_sqrt_ratio(numerator, denominator):
    return Q(1 + isqrt(numerator * SCALE**2 // denominator), SCALE)


def reciprocal_root(conductor):
    return upper_sqrt_ratio(1, conductor)


def factor(n):
    factors = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1
    if n != 1:
        factors[n] = 1
    return factors


def meets_product_bound(mass, sum_bound, pair_bounds, min_norm):
    """The actual reciprocal p lies in [left,right] and has product <= 1."""
    left = max(0, (mass - sum_bound) / 4)
    right = MAX_RECIPROCAL
    if left > right:
        return False
    centers = [(mass - b) / 2 for b in pair_bounds]
    if min(centers) <= right:
        raise ValueError("positive factors required for log-concavity")

    def product_bound(p):
        return min_norm * p * prod(a-p for a in centers)

    return min(product_bound(left), product_bound(right)) <= 1


def fundamental(d):
    return d if d % 4 == 1 else 4*d


def biquadratic_fields(conductor_limit):
    # The two smallest subfield discriminants specify the third subfield.
    radicals = [d for d in range(2, conductor_limit+1)
                if fundamental(d) <= conductor_limit and max(factor(d).values()) == 1]
    fields = set()
    for i, a in enumerate(radicals):
        for b in radicals[i+1:]:
            c = a*b // gcd(a, b)**2
            fields.add(tuple(sorted(fundamental(d) for d in (a, b, c))))
    return sorted(fields)


def kernel_conductor(n, units, kernel):
    return next(d for d in range(1, n+1)
                if n % d == 0 and all(u in kernel for u in units if (u-1) % d == 0))


def cyclic_fields(conductor_limit):
    answer = []
    for n in range(5, conductor_limit+1):
        units = [u for u in range(1, n) if gcd(n, u) == 1]
        if len(units) % 8:
            continue
        size = len(units) // 4
        start = frozenset((1, n-1))
        seen, pending = {start}, [start]
        while pending:
            subgroup = pending.pop()
            if len(subgroup) == size:
                square_kernel = {u for u in units if u*u % n in subgroup}
                if len(square_kernel) != len(units)//2:
                    continue
                if kernel_conductor(n, units, subgroup) != n:
                    continue
                q = kernel_conductor(n, units, square_kernel)
                answer.append(((q, n, n), tuple(sorted(subgroup))))
                continue
            for u in units:
                if u in subgroup:
                    continue
                coset, generated = subgroup, set(subgroup)
                while True:
                    coset = {u*v % n for v in coset}
                    if coset == subgroup:
                        break
                    generated.update(coset)
                extension = frozenset(generated)
                if size % len(extension) == 0 and extension not in seen:
                    seen.add(extension)
                    pending.append(extension)
    return sorted(answer)


def minimum_norm(codegree, conductors):
    norm_factor = codegree * prod(conductors)
    codegree_factors = factor(codegree)
    result = 1
    for p, v in factor(norm_factor).items():
        ramified_characters = sum(c % p == 0 for c in conductors)
        inertia = {0: 1, 2: 2, 3: 4}[ramified_characters]
        step = 4 // inertia
        if step % 2 == 0 and v % 2:
            return None
        m = codegree_factors.get(p, 0)
        while v < 4*m or v % step:
            v += 2
        result *= p**v
    return result


def run():
    # For c_2>=47 the true product dominates the product used here, while
    # the interval for p is contained in the one used here.
    n = 47
    b = reciprocal_root(5)
    possible = meets_product_bound(MIN_MASS, b+2*reciprocal_root(n),
                                   [b, upper_sqrt_ratio(2, n), upper_sqrt_ratio(2, n)],
                                   20*n*n)
    if possible:
        raise ValueError("second conductor bound failed")
    fields = [(cs, None) for cs in biquadratic_fields(n-1)] + cyclic_fields(n-1)
    largest_sum = max(sum(reciprocal_root(c) for c in cs) for cs, kernel in fields)
    exact_maximizer = (5, 15, 15)
    largest_lower = largest_sum - Q(3, SCALE)
    if largest_sum != sum(reciprocal_root(c) for c in exact_maximizer):
        raise ValueError("unexpected largest Fourier sum")
    if any(sum(reciprocal_root(c) for c in cs) >= largest_lower
           for cs, kernel in fields if cs != exact_maximizer):
        raise ValueError("Fourier maximum needs tighter root intervals")
    # For f>=28 all factors increase and the interval shrinks.
    if meets_product_bound(Q(27, 28), largest_sum, [b]*3, 28**4):
        raise ValueError("codegree bound failed")

    allowed = {}
    for f in range(4, 28):
        if f % 8 == 1:
            continue
        for cs, kernel in fields:
            norm = minimum_norm(f, cs)
            if norm is None:
                continue
            field_bounds = [reciprocal_root(c) for c in cs]
            pair_bounds = field_bounds if kernel is None else [
                field_bounds[0], upper_sqrt_ratio(2, cs[1]), upper_sqrt_ratio(2, cs[1])]
            if meets_product_bound(Q(f-1, f), sum(field_bounds), pair_bounds, norm):
                field = cs if kernel is None else (cs[-1], kernel)
                allowed.setdefault(f, []).append(field)

    k15 = (15, (1, 14))
    k16 = (16, (1, 15))
    k20 = (20, (1, 19))
    k35 = (35, (1, 11, 16, 19, 24, 34))
    k40 = (40, (1, 11, 29, 39))
    expected = {
        4: [(5, 8, 40), (5, 12, 60), (5, 13, 65), (5, 17, 85),
            (5, 21, 105), (8, 12, 24), k15, k16, k20, k35, k40],
        5: [k15, k20], 16: [(5, 8, 40), k15], 20: [k15],
    }
    if {f: set(v) for f, v in allowed.items()} != {f: set(v) for f, v in expected.items()}:
        raise ValueError(f"unexpected quartic profiles: {allowed}")
    print("Quartic profiles for D>17 from the norm and Fourier inequalities")
    for f, fields_for_f in expected.items():
        print(f"f={f}: {fields_for_f}")


if __name__ == "__main__":
    run()
