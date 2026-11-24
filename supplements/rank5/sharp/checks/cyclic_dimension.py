"""Bounded global-dimension search for the four cyclic quartic fields at rational codegree four."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from math import gcd, isqrt


def quadratic_positive(a,b,d):
    """Test a+b sqrt(d)>0 exactly."""
    if b==0: return a>0
    if a==0: return b>0
    if (a>0)==(b>0): return a>0
    return (a*a>d*b*b) if a>0 else (a*a<d*b*b)


def norm_minus_one_units(d, limit):
    """Enumerate positive units of norm minus one, allowing either sign of a."""
    a, b = 2, 0
    norm = 1
    while a <= 2 * isqrt(11 * limit) + 5:
        if d == 2:
            a, b = a + 2 * b, a + b
        else:
            a, b = (a + 5 * b) // 2, (a + b) // 2
        norm = -norm
        if norm == -1:
            yield a, b
            if a <= 3:  # z^{-1}<11/sqrt(17)<3, hence its trace difference is <3.
                yield -a, b


def remaining_dimensions(conductor, limit):
    codegree = 4
    d = 2 if conductor == 16 else 5
    quadratic_discriminant = 8 if d == 2 else 5
    norm_factor = codegree * conductor**2 * quadratic_discriminant
    radical_multiplier = isqrt(norm_factor // d)
    assert d * radical_multiplier**2 == norm_factor
    survivors = set()

    for a, b in norm_minus_one_units(d, limit):
        # 2R = index * (C0 + E0 sqrt(d)).
        C0, E0 = b * d * radical_multiplier, a * radical_multiplier
        for index in range(1, isqrt(1331 * limit // norm_factor) + 1):
            C, E = C0 * index, E0 * index
            norm_D = norm_factor * index**2
            # sigma(R)=(C-E sqrt(d))/2 is the product of two numbers in (1,11).
            if not quadratic_positive(C-2,-E,d) or not quadratic_positive(242-C,E,d):
                continue

            # Enumerate 2U=A+B sqrt(d) via A*C0 = rhs (mod d*E0).
            rhs = 2 * (codegree - 1) * norm_factor * index // codegree
            modulus = d * E0
            common_factor = gcd(C0, modulus)
            if rhs % common_factor:
                continue
            step = abs(modulus) // common_factor
            residue = (rhs // common_factor * pow(C0 // common_factor, -1, step)) % step
            low = 21   # D>1+4*2^2 and each nonidentity conjugate exceeds one.
            high = limit + 33
            first = residue + ((low - residue + step - 1) // step) * step

            for A in range(first, high + 1, step):
                B = (A * C0 - rhs) // modulus
                if not quadratic_positive(A-4,-B,d) or not quadratic_positive(44-A,B,d):
                    continue
                if (A * A - d * B * B) % 4:
                    continue
                norm_U = (A * A - d * B * B) // 4
                delta0 = A * A + d * B * B - 8 * C
                delta1 = 2 * A * B - 8 * E
                cross = delta0**2 - d * delta1**2
                if cross <= 0 or isqrt(d * cross)**2 != d * cross:
                    continue

                e2 = norm_U + C
                e3 = (codegree - 1) * norm_D // codegree
                if A**4 % norm_D or e2**2 % norm_D:
                    continue
                # The faithful squared Fourier coefficient is at most 1/conductor.
                scaled = codegree**2 * (4 * norm_U - 8 * e2) + 2 * (codegree - 1)**2 * norm_D
                if conductor * scaled > 2 * codegree**2 * norm_D:
                    continue
                # Exact quadratic character, equal to s²-4 N(U)/N(D).
                if quadratic_discriminant*((codegree-1)**2*norm_D-4*codegree**2*norm_U) > codegree**2*norm_D:
                    continue
                survivors.add((A, e2, e3, norm_D))
    return sorted(survivors)


if __name__ == '__main__':
    from verify_quartic_moments import DATA, certificate_bound
    for row in DATA:
        if '-' in row['F']:
            continue
        conductor, limit = int(row['F']), certificate_bound(row)
        remaining = remaining_dimensions(conductor, limit)
        print(f"Conductor {conductor}, codegree four, D <= {limit}: {len(remaining)} candidates.")
        assert not remaining, remaining
