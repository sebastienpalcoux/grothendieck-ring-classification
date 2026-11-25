"""Exclude the conductor-24 trace moments independently modulo 8 and 11.

Elements use the integral basis 1, sqrt(2), sqrt(3), (sqrt(2)+sqrt(6))/2.
In this basis the first coordinate equals the absolute trace divided by four.
The field involution j fixes sqrt(2) and negates sqrt(3).
"""
from itertools import product

ONE = (1, 0, 0, 0)
U = (3, 2, 0, 0)
V = (2, 0, 1, 0)
W = (5, -2, 0, 4)


def multiply(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (
        a*A + 2*b*B + 3*c*C + 2*d*D + b*D + d*B,
        a*B + b*A - b*C - c*B + c*D + d*C,
        a*C + c*A + d*D + b*D + d*B,
        a*D + d*A + 2*(b*C + c*B) + c*D + d*C,
    )


def conjugate(x):
    a, b, c, d = x
    return a, b+d, -c, -d


# For each representative z, give its norm and the unit j(z)/z, in the
# order of the conductor-24 seed table in the manuscript.
VW = multiply(V, W)
SEEDS = (
    ((1, 0, 0, 0), 1, ONE), ((2, -1, 0, 0), 4, ONE),
    ((2, 0, 0, -1), 1, VW), ((3, -2, -1, 1), 9, V),
    ((3, 0, -1, 0), 36, V), ((3, 1, 0, -2), 9, W),
    ((3, 2, -1, -2), 4, VW), ((6, -1, 2, -4), 36, W),
)


def residue(x, m):
    return tuple(t % m for t in x)


def unit_graph(m):
    """Map each unit u in the generated residue group to j(u)/u."""
    steps = [(U, ONE)] + [
        (g, multiply(conjugate(g), conjugate(g))) for g in (V, W)
    ]
    graph = {ONE: ONE}
    queue = [ONE]
    for u in queue:
        for g, ratio in steps:
            v = residue(multiply(u, g), m)
            image = residue(multiply(graph[u], ratio), m)
            if v in graph:
                assert graph[v] == image
            else:
                graph[v] = image
                queue.append(v)
    return graph


def trace_coordinate(z, x):
    return multiply(z, x)[0]


def compatible_seeds(m):
    graph = unit_graph(m)
    # The norm of x is odd. Thus its seed norm is odd and any integer
    # multiplier is odd. All scalar classes modulo 11 have odd lifts.
    scalars = range(1, m, 2) if m == 8 else range(m)
    x_values = {
        residue(tuple(n*t for t in multiply(seed, u)), m)
        for seed, norm, _ in SEEDS if norm % 2
        for u, n in product(graph, scalars)
    }
    moments = [
        (x, conjugate(x), multiply(x, conjugate(x)), multiply(conjugate(x), conjugate(x)))
        for x in x_values
    ]
    counts = []
    for seed, _, seed_ratio in SEEDS:
        assert multiply(seed, seed_ratio) == conjugate(seed)
        surviving = set()
        for u, unit_ratio in graph.items():
            z = residue(multiply(seed, u), m)
            ratio = residue(multiply(seed_ratio, unit_ratio), m)
            if (trace_coordinate(z, multiply(ratio, ratio)) - 5*z[0]) % m:
                continue
            for row in moments:
                if all((trace_coordinate(z, value)-k*z[0]) % m == 0
                       for value, k in zip(row, (1, 3, 1, 11))):
                    surviving.add(z)
                    break
        counts.append(len(surviving))
    return counts


if __name__ == '__main__':
    at_eight = compatible_seeds(8)
    at_eleven = compatible_seeds(11)
    print("Modulo 8:", at_eight)
    print("Modulo 11:", at_eleven)
    assert at_eight == [0, 8, 0, 0, 0, 0, 0, 16]
    assert at_eleven == [14, 0, 12, 12, 32, 14, 32, 0]
    assert all(a == 0 or b == 0 for a, b in zip(at_eight, at_eleven))
