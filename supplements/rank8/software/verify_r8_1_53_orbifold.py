"""Exact finite-group application of Izumi Theorem 12.5 to Yu--Zhang NG(C4^2,16).

Categorical existence is the cited theorem; this checks its finite-group
hypotheses, the resulting complete fusion tensor, and the census isomorphism.
No numerical near-group reconstruction is used.
"""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / 'data'


def require(value, message='check failed'):
    if not value:
        raise ValueError(message)


def finite_group_check():
    G = list(itertools.product(range(4), repeat=2))
    H = [g for g in G if not g[0] % 2 and not g[1] % 2]
    add = lambda g, h: tuple((g[i]+h[i]) % 4 for i in range(2))
    # Exponents in zeta_8: chi(g,h)=i^(g1 h1-g2 h2).
    chi = lambda g, h: 2*(g[0]*h[0]-g[1]*h[1]) % 8
    a = lambda g: 3*(g[0]**2-g[1]**2) % 8
    require(all((a(add(g,h))+chi(g,h)-a(g)-a(h)) % 8 == 0
                for g,h in itertools.product(G, repeat=2)), 'quadratic refinement')
    require(all(any(chi(g,h) for h in G) for g in G if g != (0,0)),
            'nondegenerate bicharacter')
    perp = [g for g in G if all(chi(g,h) == 0 for h in H)]
    require(perp == H, 'H=H-perp')
    ga = (1,1)
    require(all(a(h) == chi(h,ga) for h in H), 'duality character')
    require(any(a(h) for h in H) and ga not in H, 'nontrivial duality shift')
    require(all(chi(h,h) == 0 for h in H), 'central boson twists')
    require(all(tuple(v % 2 for v in add(g,h)) == tuple((g[i]+h[i]) % 2 for i in range(2))
                for g,h in itertools.product(G, repeat=2)), 'quotient V4')
    return dict(group='C4 x C4', subgroup=[list(h) for h in H],
                annihilator_equals_subgroup=True,
                a_on_subgroup_exponents_mod8=[a(h) for h in H],
                duality_shift=list(ga), quotient='C2 x C2')


def model_tensor():
    # G/H basis 00,01,10,11 followed by sigma,01sigma,10sigma,11sigma.
    T = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(8), repeat=2):
        a,b = i % 4, j % 4
        if i < 4 and j < 4:
            T[i][j][a ^ b] = 1
        elif (i < 4) != (j < 4):
            T[i][j][4+(a ^ b)] = 1
        else:
            T[i][j][a ^ b ^ 3] = 1
            T[i][j][4:] = [1]*4
    return T


def verify_record(record):
    require(record['id'] == 'R8_1_53')
    require(record['model'] == 'Yu-Zhang C4^2+16 / Izumi isotropic H=2G')
    group = finite_group_check()
    T = model_tensor()
    N,p = record['tensor'], record['model_to_census']
    sha = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(sha == record['tensor_sha256'])
    require(sorted(p) == list(range(8)) and p[0] == 0)
    require(all(T[i][j][k] == N[p[i]][p[j]][p[k]]
                for i,j,k in itertools.product(range(8), repeat=3)), '512 tensor coefficients')
    require(all(sum(T[i][j][s]*T[s][k][l] for s in range(8)) ==
                sum(T[j][k][s]*T[i][s][l] for s in range(8))
                for i,j,k,l in itertools.product(range(8), repeat=4)), 'associativity')
    dual = [next(j for j in range(8) if T[i][j][0]) for i in range(8)]
    require(dual == [0,1,2,3,7,6,5,4])
    return dict(status='PASS', id=record['id'], scope='unitary fusion category',
                finite_group=group, tensor_sha256=sha, model_to_census=p,
                coefficient_equalities=512, associativity_equalities=4096, dual=dual)


def verify():
    return verify_record(json.loads((HERE/'r8_1_53_orbifold_certificate.json').read_text()))


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
