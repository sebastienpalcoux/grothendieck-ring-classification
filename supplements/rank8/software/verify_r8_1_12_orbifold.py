"""Budinski's NG(C16,16), Izumi Theorem12.5 with H=4C16: exact R8_1_12."""
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / 'data'


def require(value, message='check failed'):
    if not value:
        raise ValueError(message)


def finite_group_check():
    G,H = list(range(16)), [0,4,8,12]
    # Budinski J16^1: m=3, c=exp(pi*i/4). Exponents in zeta_32.
    chi = lambda g,h: 6*g*h % 32
    a = lambda g: -3*g*g % 32
    require(all((a((g+h)%16)+chi(g,h)-a(g)-a(h)) % 32 == 0
                for g,h in itertools.product(G, repeat=2)), 'quadratic refinement')
    require(all(any(chi(g,h) for h in G) for g in G if g), 'nondegenerate')
    perp = [g for g in G if all(chi(g,h) == 0 for h in H)]
    require(perp == H, 'H=H-perp')
    ga = 2
    require(all(a(h) == chi(h,ga) for h in H), 'duality character')
    require(any(a(h) for h in H) and ga not in H, 'nontrivial duality shift')
    require(all(chi(h,h) == 0 for h in H), 'central bosons')
    return dict(group='C16', source_category='Budinski J16^1', m=3,
                subgroup=H, annihilator_equals_subgroup=True,
                a_on_subgroup_exponents_mod32=[a(h) for h in H],
                duality_shift=ga, quotient='C4')


def model_tensor():
    # Basis 1,g,g²,g³,sigma,g sigma,g² sigma,g³ sigma.
    T = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(8), repeat=2):
        a,b = i % 4, j % 4
        if i < 4 and j < 4:
            T[i][j][(a+b)%4] = 1
        elif i < 4:
            T[i][j][4+(a+b)%4] = 1
        elif j < 4:
            T[i][j][4+(a-b)%4] = 1
        else:
            T[i][j][(a-b+2)%4] = 1
            T[i][j][4:] = [1]*4
    return T


def verify_record(record):
    require(record['id'] == 'R8_1_12')
    require(record['model'] == 'Budinski C16+16 / Izumi isotropic H=4G')
    group = finite_group_check()
    T = model_tensor()
    N,p = record['tensor'], record['model_to_census']
    sha = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(sha == record['tensor_sha256'])
    require(sorted(p) == list(range(8)) and p[0] == 0)
    require(all(T[i][j][k] == N[p[i]][p[j]][p[k]]
                for i,j,k in itertools.product(range(8), repeat=3)), '512 coefficients')
    require(all(sum(T[i][j][s]*T[s][k][l] for s in range(8)) ==
                sum(T[j][k][s]*T[i][s][l] for s in range(8))
                for i,j,k,l in itertools.product(range(8), repeat=4)), 'associativity')
    dual = [next(j for j in range(8) if T[i][j][0]) for i in range(8)]
    require(dual == [0,3,2,1,6,7,4,5])
    return dict(status='PASS', id=record['id'], scope='unitary fusion category',
                finite_group=group, tensor_sha256=sha, model_to_census=p,
                coefficient_equalities=512, associativity_equalities=4096, dual=dual)


def verify():
    return verify_record(json.loads((HERE/'r8_1_12_orbifold_certificate.json').read_text()))


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
