"""Exact independent balance and permutation-source audit of the R10_1_21 model."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mm(A, B):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*B)] for row in A]


def mv(A, x):
    return [sum(a*b for a, b in zip(row, x)) for row in A]


def kron(A, B):
    return [[a*b for a in rowa for b in rowb] for rowa in A for rowb in B]


def rank(A):
    A = [list(map(Fraction, row)) for row in A]
    p = 0
    for j in range(len(A[0])):
        q = next((i for i in range(p, len(A)) if A[i][j]), None)
        if q is None:
            continue
        A[p], A[q] = A[q], A[p]
        d = A[p][j]
        A[p] = [x/d for x in A[p]]
        for i in range(len(A)):
            if i != p:
                d = A[i][j]
                A[i] = [x-d*y for x, y in zip(A[i], A[p])]
        p += 1
    return p


def balance():
    # The actual right action is R=iJ. These integer calculations retain the
    # exact scalar i symbolically, so no floating-point complex arithmetic occurs.
    J = [[0,-1],[1,0]]
    I = [[1,0],[0,1]]
    P = [[0,1],[1,0]]
    require(mm(J,J) == [[-1,0],[0,-1]], 'R squared is identity')
    require(mm(P,J) == [[-x for x in row] for row in mm(J,P)],
            'h-minus equivariance')
    L, R = kron(J,I), kron(I,J)
    T = [[a+b for a,b in zip(r,s)] for r,s in zip(L,R)]
    u = [1,0,0,1]
    v = [0,1,-1,0]
    require(mv(T,u) == mv(T,v) == [0]*4 and rank(T) == 2,
            'entire balanced kernel')
    swap = kron(P,P)
    require(mv(swap,u) == u and mv(swap,v) == [-x for x in v],
            'kernel equivariance gives unit-plus and ff-minus')
    require(mv(R,u) == v and mv(R,v) == [-x for x in u],
            'residual right action; rescale v by i to obtain regular A-module')
    return dict(right_action='i*[[0,-1],[1,0]]',
                balanced_kernel_basis=[u,v], equivariance_signs=[1,-1],
                invertible_square='unit')


def pointed_even_su2():
    # Basis 1,f,x,y of PSU(2)_6.
    P = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        P[0][i][i] = P[i][0][i] = 1
    P[1][1][0] = 1
    P[1][2][3] = P[2][1][3] = 1
    P[1][3][2] = P[3][1][2] = 1
    for i in (2,3):
        P[i][i] = [1,0,1,1]
    P[2][3] = P[3][2] = [0,1,1,1]
    return P


def permutation_equivariantization(P):
    labels = [('d',i,e) for i in range(4) for e in (1,-1)]
    labels += [('p',i,j) for i in range(4) for j in range(i+1,4)]
    fibers, traces = [], []
    for typ,i,j in labels:
        M = [[0]*4 for _ in range(4)]
        t = [0]*4
        if typ == 'd':
            M[i][i], t[i] = 1,j
        else:
            M[i][j] = M[j][i] = 1
        fibers.append(M)
        traces.append(t)
    W = [[[0]*14 for _ in range(14)] for _ in range(14)]
    for i,j in product(range(14),repeat=2):
        M = [[sum(fibers[i][a][b]*fibers[j][c][d]*P[a][c][u]*P[b][d][v]
                  for a,b,c,d in product(range(4),repeat=4))
              for v in range(4)] for u in range(4)]
        tr = [sum(traces[i][a]*traces[j][b]*P[a][b][u]
                  for a,b in product(range(4),repeat=2)) for u in range(4)]
        for k,(typ,a,b) in enumerate(labels):
            if typ == 'd':
                z = M[a][a]+b*tr[a]
                require(z % 2 == 0 and z >= 0, 'equivariant diagonal multiplicity')
                W[i][j][k] = z//2
            else:
                W[i][j][k] = M[a][b]
    return labels,W


def main():
    balance_report = balance()
    receipt = json.loads((ROOT/'work/resolve_rank10_quadratic/model21.json').read_text())
    N = receipt['tensor']
    def translate(g, x):
        if x < 4:
            return g ^ x
        if x < 6:
            return 4 + ((x-4) ^ (g//2))
        return 6 + ((x-6) ^ g)
    bases = {
        ('a','a'): [1,1,0,0,1,1,1,1,0,0],
        ('a','b'): [0,0,0,0,1,0,1,1,1,1],
        ('b','b'): [1,0,0,0,1,1,1,1,1,1]}
    # This is the unique completion forced by the hand calculation, the
    # invertible action, and the three source products, not an associativity fit.
    for i,j in product(range(10),repeat=2):
        expected = [0]*10
        if i < 4 or j < 4:
            g,x = (i,j) if i < 4 else (j,i)
            expected[translate(g,x)] = 1
        else:
            typ_i,g_i = ('a',2*(i-4)) if i < 6 else ('b',i-6)
            typ_j,g_j = ('a',2*(j-4)) if j < 6 else ('b',j-6)
            for k,c in enumerate(bases[tuple(sorted((typ_i,typ_j)))]):
                expected[translate(g_i ^ g_j,k)] += c
        require(N[i][j] == expected, 'unique completion of categorical rules')
    labels,W = permutation_equivariantization(pointed_even_su2())
    F = {
        ('d',0,1):[0], ('d',0,-1):[1],
        ('d',1,1):[1], ('d',1,-1):[0],
        ('d',2,1):[6], ('d',2,-1):[7],
        ('d',3,1):[7], ('d',3,-1):[6],
        ('p',0,1):[2,3], ('p',0,2):[4], ('p',0,3):[5],
        ('p',1,2):[5], ('p',1,3):[4], ('p',2,3):[8,9]}
    for i,j in product(range(14),repeat=2):
        left = [sum(N[a][b][c] for a in F[labels[i]] for b in F[labels[j]])
                for c in range(10)]
        right = [sum(W[i][j][k]*F[labels[k]].count(c) for k in range(14))
                 for c in range(10)]
        require(left == right, 'all permutation-source fusion products descend')
    T = json.loads((ROOT/'work/input_audit/tensors.json').read_text())['R10_1_21']
    p = [0,9,1,2,3,8,6,7,5,4]
    require(all(N[i][j][k] == T[p[i]][p[j]][p[k]]
                for i,j,k in product(range(10),repeat=3)), 'original based tensor')
    require(all(N[i][j][0] == int(i == j) for i,j in product(range(10),repeat=2)),
            'all simples self-dual')
    report = dict(status='PASS', construction='((PSU(2)_6)^2)^C2 condensed by 1+(f,f)_minus',
                  balance=balance_report, source_fusion_products=14**2,
                  original_tensor_coefficients=10**3, model_to_input_basis=p)
    (OUT/'model21_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
