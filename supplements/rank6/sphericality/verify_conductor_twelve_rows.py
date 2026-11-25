"""Check the two rational row configurations used in Theorem 3,8."""
from itertools import combinations, permutations, product

from sympy import Matrix, linsolve


THREE_ROW = (1, 1, -1, 0, 0, 0)


def dot(left, right):
    return sum(x * y for x, y in zip(left, right))


def canonical(four, first, second):
    representatives = []
    for suffix in permutations((3, 4, 5)):
        columns = (0, 1, 2, *suffix)
        permuted = [tuple(row[col] for col in columns) for row in (four, first, second)]
        representatives.append((permuted[0], *sorted(permuted[1:])))
    return min(representatives)


def admits_positive_dimensions(rows):
    matrix = Matrix((THREE_ROW, *rows))
    dimensions = next(iter(linsolve((matrix[:, 1:], -matrix[:, 0]))))
    parameters = set().union(*(x.free_symbols for x in dimensions))
    assert len(parameters) == 1
    parameter = parameters.pop()
    lower_bounds, upper_bounds = [], []
    for dimension in dimensions:
        slope = dimension.coeff(parameter)
        intercept = dimension.subs(parameter, 0)
        if slope > 0:
            lower_bounds.append((1 - intercept) / slope)
        elif slope < 0:
            upper_bounds.append((1 - intercept) / slope)
        elif intercept <= 1:
            return False
    return not lower_bounds or not upper_bounds or max(lower_bounds) < min(upper_bounds)


def verify():
    candidates = [(1, *tail) for tail in product(range(-2, 3), repeat=5)]
    rows = [row for row in candidates if dot(row, THREE_ROW) == 0]
    fours = [row for row in rows if dot(row, row) == 4]
    eights = [row for row in rows if dot(row, row) == 8]
    assert (len(fours), len(eights)) == (24, 72)
    triples = set()
    for four in fours:
        partners = [row for row in eights if dot(row, four) == 0 and
                    all((x - y) % 2 == 0 for x, y in zip(row, four))]
        for first, second in combinations(partners, 2):
            if dot(first, second) == 0:
                triples.add(canonical(four, first, second))
    assert len(triples) == 22
    feasible = {rows for rows in triples if admits_positive_dimensions(rows)}
    assert feasible == {
        ((1, -1, 0, -1, 0, 1), (1, -1, 0, 1, 2, -1), (1, 1, 2, -1, 0, -1)),
        ((1, 0, 1, -1, 0, 1), (1, -2, -1, 1, 0, 1), (1, 0, 1, 1, -2, -1)),
    }
    print('Verified 24 four-rows, 72 eight-rows, 22 triples, and 2 feasible configurations.')


if __name__ == '__main__':
    verify()
