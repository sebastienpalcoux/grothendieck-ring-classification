"""Quintic spherical descent by exact integral coordinates and field traces."""

if not __debug__:
    raise RuntimeError("Run this verifier with Python assertions enabled")

from itertools import combinations, product

# Multiplication by 2 generates (Z/11)^*/{1,-1}.
group = (1, 2, 4, 3, 5)
scale = 10**6
root_intervals = (
    (1682507, 1682508), (830830, 830831), (-284630, -284629),
    (-1309722, -1309721), (-1918986, -1918985),
)


def scaled_polynomial(x):
    value = 1
    for degree, coefficient in enumerate((1, -4, -3, 3, 1), 1):
        value = value * x + coefficient * scale**degree
    return value


assert all(scaled_polynomial(lo) * scaled_polynomial(hi) < 0
           for lo, hi in root_intervals)


def index(residue):
    return min(residue % 11, -residue % 11) - 1


def conjugate(coefficients, g):
    # The group acts by pullback on coordinates. Inversion permutes its elements.
    return [coefficients[index(j*g)] for j in range(1, 6)]


def embedding_bounds(c, g):
    intervals = [root_intervals[index(j*g)] for j in range(1, 6)]
    # All c_j are positive, and the represented field element is -sum c_j b_j.
    return (-sum(x*hi for x, (_, hi) in zip(c, intervals)),
            -sum(x*lo for x, (lo, _) in zip(c, intervals)))


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum((-1)**i * coefficient *
               determinant([row[:i]+row[i+1:] for row in matrix[1:]])
               for i, coefficient in enumerate(matrix[0]))


def adjugate(matrix):
    return [[(-1)**(i+j) * determinant([
                 row[:i]+row[i+1:] for k, row in enumerate(matrix) if k != j])
             for j in range(5)] for i in range(5)]


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def multiply(c, u):
    # Coordinates use the basis -b_j, with b_i b_j = b_(i+j) + b_(i-j).
    result = [0]*5
    for i, x in enumerate(c, 1):
        for j, y in enumerate(u, 1):
            for residue in (i+j, i-j):
                k = index(residue)
                if k < 0:  # b_0=2=-2 sum_j b_j
                    result = [v + 2*x*y for v in result]
                else:
                    result[k] -= x*y
    return result


ratios = trials = signed_pass = joint_pass = 0
for c in product(range(1, 8), repeat=5):
    A = sum(c)
    if A > 20 or len(set(c)) == 1:
        continue
    bounds = [embedding_bounds(c, g) for g in group]
    if (any(hi < 0 for _, hi in bounds) or bounds[0][0] > scale or
            any(bounds[0][0] > hi for _, hi in bounds)):
        continue
    ratios += 1
    matrix = [conjugate(c, g) for g in group]
    denominator = 11 * determinant(matrix)
    assert denominator
    inverse_numerator = adjugate(matrix)
    for i, j, k in combinations(range(2, A), 3):
        h = (1, i-1, j-i, k-j, A-k)
        rhs = [t + 2*A for t in h]
        u = [dot(row, rhs) for row in inverse_numerator]
        assert sum(u) == denominator
        trials += 1
        if 121*dot(u, u) > 25*denominator**2:
            continue
        signed_pass += 1
        w = multiply(c, u)
        assert sum(w) == denominator
        if 121*dot(w, w) > 25*denominator**2:
            continue
        joint_pass += 1
        assert any(w == conjugate(u, g) for g in group)

assert (ratios, trials, signed_pass, joint_pass) == (34, 15396, 39, 4)
print("quintic trace check: 34 ratios, 15396 trace vectors, "
      "39 signed passes, 4 joint passes, all Galois conjugate")
