"""Uniform Fourier bounds for the signed codegree pairs (4,16) and (4,9)."""
from fractions import Fraction
from itertools import product

F = Fraction
u_interval = F(5828427, 10**6), F(5828428, 10**6)
v_over_two = tuple((endpoint + 1) / 4 for endpoint in u_interval)
eta = F(989, 1000)


def bounds(interval, exponent):
    left, right = (point ** exponent for point in interval)
    return min(left, right), max(left, right)


def survives(mass, threshold, e, f, r, a, h, b):
    x_low, x_high = (h * value for value in bounds(u_interval, b))
    ratio_low, ratio_high = bounds(v_over_two, f - e)
    power_low, power_high = bounds(u_interval, r)
    y_low = a * ratio_low * power_low
    y_high = a * ratio_high * power_high
    gap = (mass * eta / (1 + x_high)) ** 2 * (1 + x_low**2 + 2*y_low**2)
    s_max = mass * y_high / (eta * (1 + x_low))
    return gap <= F(1, 2) and (
        s_max >= threshold or gap + max(0, F(1, 2) - s_max) ** 2 <= F(1, 2)
    )


def candidates(mass, threshold):
    q = mass.denominator
    tested, remaining = 0, []
    for e in (0, 1):
        families = ((e, 1, 1), (e, 1, 2), (1-e, e, 2-e))
        for (f, r, a), h, b in product(families, range(1, 2*q+1), (-2, -1, 0)):
            if (2*q) % h or (h % 2 == 0 and (2*q) % (h * (4 // (1+e)))):
                continue
            tested += 1
            if survives(mass, threshold, e, f, r, a, h, b):
                remaining.append((e, f, r, a, h, b))
    return tested, remaining


if __name__ == "__main__":
    small, left = candidates(F(11, 16), F(1, 4))
    large, right = candidates(F(23, 36), F(1, 4))
    assert left == []
    assert right == [
        (0, 1, 0, 2, 6, 0), (0, 1, 0, 2, 9, 0),
        (1, 0, 1, 1, 6, 0), (1, 0, 1, 1, 9, 0), (1, 0, 1, 1, 36, -1)
    ]
    for _, _, _, _, h, b in right:
        norm = 1 + h*h + h * (2 if b == 0 else 6)
        assert pow(-norm, 11, 23) == 22
    print(f"{small} + {large} quadratic comparisons; five candidates excluded modulo 23.")
