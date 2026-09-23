"""Quadratic parity descent, tested on the input tensor, never on its label.

All arithmetic here is integer arithmetic. A successful certificate establishes
sphericality and a pseudo-unitary Galois conjugate; it is not itself an exclusion.
"""
import itertools, hashlib, json
from exact import require, VerificationError
Matrix = list[list[int]]
Tensor = list[list[list[int]]]
Pair = tuple[int, int]


def identity(n: int) -> Matrix:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def charpoly(a: Matrix) -> list[int]:
    """Faddeev--LeVerrier; return descending integer coefficients."""
    n = len(a)
    b = identity(n)
    coefficients = [1]
    for k in range(1, n + 1):
        ab = matmul(a, b)
        tr = sum(ab[i][i] for i in range(n))
        require(tr % k == 0, 'nonintegral characteristic coefficient')
        c = -tr // k
        coefficients.append(c)
        b = [[ab[i][j] + (c if i == j else 0) for j in range(n)] for i in range(n)]
    require(all(x == 0 for row in b for x in row), 'Cayley--Hamilton check failed')
    return coefficients


def polynomial_quotient(a: list[int], b: list[int]) -> list[int]:
    require(b[0] == 1 and len(a) >= len(b), 'invalid monic polynomial division')
    remainder = a[:]
    result: list[int] = []
    for i in range(len(a) - len(b) + 1):
        c = remainder[i]
        result.append(c)
        for j, value in enumerate(b):
            remainder[i + j] -= c * value
    require(not any(remainder), 'quadratic formal-codegree factor not present')
    return result


def rank_mod_two(a: Matrix) -> int:
    a = [[x % 2 for x in row] for row in a]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((row for row in range(rank, len(a)) if a[row][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for row in range(len(a)):
            if row != rank and a[row][col]:
                a[row] = [x ^ y for x, y in zip(a[row], a[rank])]
        rank += 1
    return rank


def det(a: Matrix) -> int:
    n = len(a)
    result = 0
    for p in itertools.permutations(range(n)):
        sign = -1 if sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n)) % 2 else 1
        term = sign
        for i in range(n):
            term *= a[i][p[i]]
        result += term
    return result


def squarefree(q: int) -> bool:
    p = 2
    while p * p <= q:
        if q % (p * p) == 0:
            return False
        p += 1
    return True


def connected(a: Matrix) -> bool:
    reached = {0}
    todo = [0]
    while todo:
        i = todo.pop()
        for j, value in enumerate(a[i]):
            if value and j not in reached:
                reached.add(j)
                todo.append(j)
    return len(reached) == len(a)


def times(x: Pair, y: Pair, q: int) -> Pair:
    return (x[0] * y[0] + q * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def verify_ring(nijk: Tensor) -> None:
    n = len(nijk)
    require(n == 5, 'the application file must contain rank-five tensors')
    require(all(len(matrix) == n and all(len(row) == n for row in matrix) for matrix in nijk), 'tensor shape')
    require(all(type(x) is int and x >= 0 for matrix in nijk for row in matrix for x in row), 'invalid structure constants')
    for i, j, k in itertools.product(range(n), repeat=3):
        require(nijk[0][i][j] == int(i == j), 'left unit')
        require(nijk[i][0][j] == int(i == j), 'right unit')
        require(nijk[i][j][0] == int(i == j), 'self-dual basis axiom')
        require(nijk[i][j][k] == nijk[j][i][k] == nijk[i][k][j], 'self-dual reciprocity')
    for i, j, k, ell in itertools.product(range(n), repeat=4):
        left = sum(nijk[i][j][m] * nijk[m][k][ell] for m in range(n))
        right = sum(nijk[j][k][m] * nijk[i][m][ell] for m in range(n))
        require(left == right, 'associativity')



def certificate(nijk):
    if len(nijk)!=5 or any(nijk[i][j][0]!=int(i==j) for i in range(5) for j in range(5)):return None
    n=len(nijk)
    m=[[nijk[j][j][i] for i in range(1,n)] for j in range(1,n)]
    if any(sum(row)%2 for row in m):return None
    a=[sum(row)//2 for row in m]
    norm=1+sum(x*x for x in a)
    if norm%4:return None
    q=norm//4
    if q<=1 or q%4 not in (2,3) or not squarefree(q):return None
    dims=[(1,0)]+[(x,1) for x in a]
    for i,j in itertools.product(range(n),repeat=2):
        rhs=tuple(sum(nijk[i][j][k]*dims[k][c] for k in range(n)) for c in range(2))
        if times(dims[i],dims[j],q)!=rhs:return None
    cr=[[0]*n for _ in range(n)]
    for mat in nijk:
        square=matmul(mat,mat)
        cr=[[cr[i][j]+square[i][j] for j in range(n)] for i in range(n)]
    cp=charpoly(cr);mu=0
    for v in reversed(cp):
        if v%2:break
        mu+=1
    if mu!=2 or rank_mod_two(m)!=3:return None
    irr=[i for i in range(1,n) if a[i-1]>0 and connected(nijk[i])]
    if not irr:return None
    squares=[times(x,x,q) for x in dims]
    D=tuple(sum(x[c] for x in squares) for c in range(2))
    if D[1]<=0:return None
    fp=[1,-2*D[0],D[0]*D[0]-q*D[1]*D[1]]
    if any(x%2 for x in fp[1:]):return None
    quotient=polynomial_quotient(cp,fp)
    minor=None
    for rows in itertools.combinations(range(4),3):
        for cols in itertools.combinations(range(4),3):
            v=det([[m[i][j] for j in cols] for i in rows])
            if v%2:minor={'rows':list(rows),'columns':list(cols),'determinant':v};break
        if minor:break
    require(minor is not None,'parity rank/minor inconsistency')
    return {'kind':'quadratic_parity_descent','q':q,'A':a,'M':m,'casimir_polynomial':cp,
            'zero_multiplicity_mod2':mu,'parity_rank':3,'minor':minor,
            'FP_dimension':list(D),'FP_codegree_polynomial':fp,'remaining_factor':quotient,
            'irreducible_matrix':irr[0]}


def verify(R,c):
    require(c==certificate(R),'quadratic parity hypotheses not verified')
