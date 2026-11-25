"""Enumerate totally positive d-numbers in Q(sqrt(2),sqrt(5)) through trace 1001."""

from itertools import product

ONE = (1, 0, 0, 0)
# Basis (1, sqrt(2), phi, sqrt(2)*phi), where phi^2=phi+1.
RADICALS = [
    (0, 0, ONE),
    (1, 0, (0, 1, 0, 0)),
    (0, 1, (-1, 0, 2, 0)),
    (1, 1, (0, -1, 0, 2)),
]


def multiply(x, y):
    result = [0] * 4
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            coeff = a * b * (2 if i & j & 1 else 1)
            parity = (i ^ j) & 1
            power = (i >> 1) + (j >> 1)
            if power != 1:
                result[parity] += coeff
            if power != 0:
                result[parity + 2] += coeff
    return tuple(result)


def trace(x):
    return 4 * x[0] + 2 * x[2]


def powers(unit, inverse, bound):
    assert multiply(unit, inverse) == ONE
    table = {0: ONE}
    for i in range(1, bound + 1):
        table[i] = multiply(table[i - 1], unit)
        table[-i] = multiply(table[1 - i], inverse)
    # The first omitted positive unit-power exceeds 1001/2 in the
    # distinguished embedding, by its (even-powered) quadratic trace:
    # u^(2(bound+1)) + u^(-2(bound+1)) > (1001/2)^2 + 1.
    next_unit = multiply(table[bound], unit)
    assert 2 * trace(multiply(next_unit, next_unit)) > 1001**2 + 4
    return table


def census():
    cap = 1001
    u = powers((1, 1, 0, 0), (-1, 1, 0, 0), 7)
    v = powers((0, 0, 1, 0), (-1, 0, 1, 0), 12)
    w = powers((3, -1, 0, 2), (-3, -1, 0, 2), 3)
    rows = set()
    for e2, e5, radical in RADICALS:
        discr = 2**e2 * 5**e5
        for i, j, k in product(u, v, w):
            if (e2 + i + k) % 2 or (e5 + j + k) % 2:
                continue
            x = multiply(multiply(radical, u[i]), multiply(v[j], w[k]))
            tr = trace(x)
            if tr > cap:
                continue
            X, Y, Z = 2*x[1] + x[3], 2*x[2], x[3]
            if sum(t != 0 for t in (X, Y, Z)) < 2:
                continue
            X, Y, Z = max((a*X, b*Y, a*b*Z) for a, b in product((1,-1), repeat=2))
            x2 = multiply(x, x)
            c2 = (tr*tr - trace(x2)) // 2
            c3 = (trace(multiply(x2, x)) - tr*trace(x2) + c2*tr) // 3
            for h in range(1, cap // tr + 1):
                A = h * tr
                B = h**2 * c2
                C = h**3 * c3
                N = h**4 * discr**2
                # All four real conjugates exceed one iff all elementary
                # symmetric coefficients shifted by one are positive.
                if min(A-4, B-3*A+6, C-2*B+3*A-4, N-C+B-A+1) > 0:
                    continue
                rows.add((8,5,40,A,h*X,h*Y,h*Z,B,C,N))
    return sorted(rows)


def proper_dimension_height():
    """Check the twelve Fibonacci indices below 75 using integer arithmetic."""
    from sympy import factorint, isprime

    fib = [0, 1]
    lucas = [2, 1]
    for _ in range(2, 76):
        fib.append(sum(fib[-2:]))
        lucas.append(sum(lucas[-2:]))
    assert fib[75] == 2111485077978050
    witnesses = {45: [3, 7, 3], 63: [23627, 3, 3, 3, 3]}

    def factorization(n):
        # All factored integers lie below 2^64 (deterministic primality range).
        factors = factorint(n)
        check = 1
        for p, e in factors.items():
            assert p < 2**64 and isprime(p)
            check *= p**e
        assert check == n
        return factors

    for j in range(3, 75, 6):
        a, b = fib[j], lucas[j]
        assert b*b == 5*a*a - 4 and a % 4 == 2 and b % 8 == 4
        a_primes = factorization(a // 2)
        b_primes = factorization(b // 4)
        assert not (a_primes.keys() & b_primes.keys())
        powers = dict(a_primes)
        powers.update((p, 2*e) for p, e in b_primes.items())
        divisors = [1]
        for p, e in powers.items():
            step = 2 if p % 4 == 3 else 1
            divisors = [v*p**i for v in divisors for i in range(0, e+1, step)]
        candidates = sorted(4*v for v in divisors
                            if 2850*4*v < 10000*a < 3163*4*v
                            and any(v % (p*p) == 0 for p in b_primes))
        factors = witnesses.get(j, [])
        assert len(candidates) == len(factors)
        for k, q in zip(candidates, factors):
            assert q % 4 == 3 and ((k-a)//2) % q == 0


if __name__ == '__main__':
    data = census()
    print(len(data), 'totally positive primitive d-number ratios through trace 1001')
