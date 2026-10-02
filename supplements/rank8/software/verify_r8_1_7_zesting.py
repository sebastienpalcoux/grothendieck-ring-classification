"""Exact associator/half-braiding and fusion replay for the R8_1_7 model.

The categorical existence/unitarity argument is in the accompanying rank-eight manuscript.
This script needs SymPy only and never solves polynomial equations.
"""
import hashlib
import itertools
import json
import re
from pathlib import Path

import sympy as s
from sympy import QQ
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parents[1] / 'data'
HASHES = {
    1: '0b18136ec84580b9ed808c73fdc43b4f693b74ec69384c3a5a0a6265f3cbf640',
    2: '7d80ef3cfc12087627f5a97e24b5641152ec6df8df949b24c2f4b026fe8cd0a9',
}


def require(condition, message='certificate condition failed'):
    if not condition:
        raise ValueError(message)


def check_base(category):
    path = HERE / f'cat_4_1_2_4_{category}_0_1.jl'
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == HASHES[category], 'source hash')
    t = s.Symbol('t')
    K = QQ.alg_field_from_poly(s.Poly(t**4 + 1, t))
    z = K([1, 0])
    F = {}
    for labels, coeffs in re.findall(
            r'\[([\d, ]+)\]\s*=>\s*QQFieldElem\[([^\]]+)\]', raw.decode()):
        key = tuple(int(x.strip()) - 1 for x in labels.split(','))
        require(key not in F, 'duplicate F symbol')
        F[key] = K([QQ(x.strip().replace('//', '/'))
                    for x in reversed(coeffs.split(','))])
    R = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for a, b, c, d, e, f in F:
        if a == 0:
            require(e == b and f == d and F[a,b,c,d,e,f] == K.one)
            R[b][c][d] = 1
    support = [[tuple(k for k in range(4) if R[i][j][k])
                for j in range(4)] for i in range(4)]
    expected = set()
    blocks = 0
    for a,b,c,d in itertools.product(range(4), repeat=4):
        left = [e for e in support[a][b] if R[e][c][d]]
        right = [f for f in support[b][c] if R[a][f][d]]
        require(len(left) == len(right), 'fusion associativity')
        if not left:
            continue
        expected.update((a,b,c,d,e,f) for e in left for f in right)
        M = DomainMatrix([[F[a,b,c,d,e,f] for f in right] for e in left],
                         (len(left), len(right)), K)
        require(M.det() != K.zero, 'singular associator')
        blocks += 1
    require(set(F) == expected, 'associator support')
    for a,b,c,d,e,f in F:
        if 0 in (a,b,c):
            require(F[a,b,c,d,e,f] == K.one, 'unit associator')
    dual = [next(j for j in range(4) if R[i][j][0]) for i in range(4)]
    for i in range(4):
        require(F[i,dual[i],i,i,0,0] != K.zero, 'rigidity coefficient')
    equations = 0
    for a,b,c,d in itertools.product(range(4), repeat=4):
        for e in support[a][b]:
            for p in support[e][c]:
                for q in support[p][d]:
                    for l in support[c][d]:
                        for k in support[b][l]:
                            if not R[a][k][q]:
                                continue
                            lhs = K.zero
                            for h in support[b][c]:
                                if R[a][h][p] and R[h][d][k]:
                                    lhs += (F[a,b,c,p,e,h] * F[a,h,d,q,p,k]
                                            * F[b,c,d,k,h,l])
                            rhs = K.zero
                            if R[e][l][q]:
                                rhs = F[e,c,d,q,p,l] * F[a,b,l,q,e,k]
                            require(lhs == rhs, 'pentagon')
                            equations += 1
    # g is simple 1 in zero-based indexing; tensoring by g permutes the basis.
    g, act = 1, [1,0,3,2]
    require(R[g] == [[int(k == act[i]) for k in range(4)] for i in range(4)])
    lam = [K.one, z**2, z, z**3] if category == 1 else [K.one, -z**2, -z**3, -z]
    hexagons = 0
    for i,j in itertools.product(range(4), repeat=2):
        for k in support[i][j]:
            require(lam[i] * lam[j] * F[i,g,j,act[k],act[i],act[j]] ==
                    lam[k] * F[g,i,j,act[k],act[i],k]
                    * F[i,j,g,act[k],k,act[j]], 'half-braiding hexagon')
            hexagons += 1
    require(F[g,g,g,g,0,0] == -K.one)
    require(lam[g]**2 == -K.one)
    return R, dict(category=[4,1,2,4,category,0,1], conductor=8,
                   source_sha256=HASHES[category], f_symbols=len(F),
                   invertible_associator_blocks=blocks, pentagons=equations,
                   scalar_half_braiding_hexagons=hexagons,
                   lambda_powers='[1,z^2,z,z^3]' if category == 1
                   else '[1,-z^2,-z^3,-z]', central_self_braiding_squared=-1)


def check_fusion(R, certificate):
    act = [1,0,3,2]
    T = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for a,b,i,j,k in itertools.product(range(2),range(2),range(4),range(4),range(4)):
        output = 4*((a+b) % 2) + (act[k] if a*b else k)
        T[4*a+i][4*b+j][output] = R[i][j][k]
    N, p = certificate['tensor'], certificate['model_to_census']
    require(certificate['id'] == 'R8_1_7')
    require(p == [0,7,3,4,1,2,6,5], 'basis permutation')
    sha = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(sha == certificate['tensor_sha256'] ==
            '796289d029c66a86bc4c64cbed56f02a03324a41e36a64dc914f28ddc2bb94fb')
    require(T == certificate['model_tensor'] and R == certificate['base_tensor'])
    require(all(T[i][j][k] == N[p[i]][p[j]][p[k]]
                for i,j,k in itertools.product(range(8), repeat=3)), 'census equality')
    require(T[4][4] == [0,1,0,0,0,0,0,0], 'z squared is g')
    require(T[2][2] == [0,1,1,1,0,0,0,0], 'x squared is g+x+y')
    return dict(id='R8_1_7', tensor_sha256=sha, model_to_census=p,
                coefficient_equalities=512, rank=8)


def verify():
    bases = [check_base(a) for a in (1,2)]
    require(bases[0][0] == bases[1][0], 'base tensor agreement')
    certificate = json.loads((HERE/'r8_1_7_zesting_certificate.json').read_text())
    fusion = check_fusion(bases[0][0], certificate)
    return dict(status='PASS', exact=True, bases=[b[1] for b in bases], fusion=fusion)


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
