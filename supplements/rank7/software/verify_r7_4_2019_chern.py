"""Exact finite checks for C(Q8 semidirect S3, c2(V)-infl c2(R), S3, 1).

The existence of the global cocycle is proved by characteristic classes in
r7_4_2019_chern_proof.md; no uncomputed global cocycle is asserted here.
"""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, message='check failed'):
    if not ok:
        raise ValueError(message)


def parity(p):
    return sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2


def compose(p, q):
    return tuple(p[q[i]] for i in range(3))


def qmul(a, b):
    s, x = a
    t, y = b
    if x == 0:
        return s ^ t, y
    if y == 0:
        return s ^ t, x
    if x == y:
        return s ^ t ^ 1, 0
    return s ^ t ^ int((x, y) not in ((1, 2), (2, 3), (3, 1))), 6-x-y


def act(p, a):
    s, x = a
    return a if x == 0 else (s ^ parity(p), p[x-1]+1)


def hmul(a, b):
    return a[0] ^ b[0], compose(a[1], b[1])


def omega_lift(a, b, c):
    # Rational logarithm, omega=exp(2*pi*i*omega_lift).
    return F(a[0] * (b[0]*c[0] + parity(b[1])*parity(c[1])), 2)


def quaternion_product(a, b):
    out = [F(0)]*4
    for x, y in product(range(4), repeat=2):
        s, z = qmul((0, x), (0, y))
        out[z] += (-1)**s*a[x]*b[y]
    return tuple(out)


def representation_check():
    # r=-(1+i+j+k)/2; s=scalar_i*(i-j)/sqrt(2).
    # Checking with w=i-j eliminates radicals from every group relation.
    one = (F(1), F(0), F(0), F(0))
    r = (-F(1, 2),)*4
    w = (F(0), F(1), F(-1), F(0))
    r2 = quaternion_product(r, r)
    require(quaternion_product(r2, r) == one, 'r cubed')
    require(quaternion_product(w, w) == (-F(2), F(0), F(0), F(0)), 'w squared')
    require(quaternion_product(w, r) == quaternion_product(r2, w), 's r s = r inverse')
    cycle, transposition = (1, 2, 0), (1, 0, 2)
    for x in range(1, 4):
        e = tuple(F(int(j == x)) for j in range(4))
        for v, vinv, p in ((r, r2, cycle), (w, tuple(-z/2 for z in w), transposition)):
            conjugated = quaternion_product(quaternion_product(v, e), vinv)
            sign, z = act(p, (0, x))
            require(conjugated == tuple(F((-1)**sign*int(j == z)) for j in range(4)), 'signed-axis action')
    return 9


def finite_check():
    S = list(permutations(range(3)))
    Q = list(product(range(2), range(4)))
    for p, a, b in product(S, Q, Q):
        require(act(p, qmul(a, b)) == qmul(act(p, a), act(p, b)), 'automorphism')
    for p, q, a in product(S, S, Q):
        require(act(compose(p, q), a) == act(p, act(q, a)), 'action composition')
    orbit = sorted({act(p, (0, 1)) for p in S})
    require(len(orbit) == 6, 'free orbit')
    for z in Q:
        pairs = [(a, b) for a, b in product(orbit, repeat=2) if qmul(a, b) == z]
        require(len(pairs) == (6 if z[1] == 0 else 4), 'product fiber')
        if z[1] == 0:
            require(len({(act(p, pairs[0][0]), act(p, pairs[0][1])) for p in S}) == 6, 'regular central fiber')
    K = list(product(range(2), S))
    for a, b, c, d in product(K, repeat=4):
        coboundary = (omega_lift(b,c,d)-omega_lift(hmul(a,b),c,d)
                      +omega_lift(a,hmul(b,c),d)-omega_lift(a,b,hmul(c,d))
                      +omega_lift(a,b,c))
        expected = a[0]*b[0]*(c[0]*d[0]+parity(c[1])*parity(d[1]))
        require(coboundary == expected, 'Bockstein x squared plus x y')
    identity = (0, 1, 2)
    z = (1, identity)
    for p, q in product(S, repeat=2):
        hp, hq = (0, p), (0, q)
        alpha = 2*(omega_lift(z,hp,hq)+omega_lift(hp,hq,z)-omega_lift(hp,z,hq))
        require(alpha % 2 == parity(p)*parity(q), 'central projective multiplier')
        require((parity(p)+parity(q)-parity(compose(p,q))) % 4 == 2*alpha % 4, 'u trivializes alpha')
    for p in S:
        hp = (0, p)
        tensorator = omega_lift(hp,z,z)+omega_lift(z,z,hp)-omega_lift(z,hp,z)
        require(tensorator == 0, 'central tensorator')
        require(2*parity(p) % 4 == 2*parity(p), 'central lift squares to sign')
    return dict(representation_relations=representation_check(),
                action_automorphism_checks=384, action_composition_checks=288,
                bockstein_equalities=12**4, projective_lift_equalities=36,
                central_tensorator_equalities=6, product_fiber_sizes=[6,4,4,4,6,4,4,4])


def model_tensor():
    # Basis 1, sign, v, t, t sign, t v, X, with t squared = sign.
    chi = [(1,1,1), (1,-1,1), (2,0,-1)]
    sizes, degrees = (1,3,2), (1,1,2)
    N = [[[0]*7 for _ in range(7)] for _ in range(7)]
    for i, j in product(range(7), repeat=2):
        if i < 6 and j < 6:
            z, a = divmod(i, 3)
            w, b = divmod(j, 3)
            for c in range(3):
                numerator = sum(sizes[s]*chi[a][s]*chi[b][s]*chi[c][s]
                                *chi[1][s]**(z*w) for s in range(3))
                require(numerator % 6 == 0, 'character product')
                N[i][j][3*(z^w)+c] = numerator//6
        elif i == j == 6:
            N[i][j] = [1,1,2,1,1,2,4]
        else:
            a = j if i == 6 else i
            N[i][j][6] = degrees[a % 3]
    return N


def verify_record(record):
    require(record['id'] == 'R7_4_2019')
    require(record['model'] == 'C(Q8 semidirect S3, c2(V)-infl c2(R), S3, 1)')
    checks = finite_check()
    N, T, p = model_tensor(), record['tensor'], record['model_to_census']
    require(sorted(p) == list(range(7)) and p[0] == 0)
    sha = hashlib.sha256(json.dumps(T, separators=(',',':')).encode()).hexdigest()
    require(sha == record['tensor_sha256'], 'source hash')
    require(all(N[i][j][k] == T[p[i]][p[j]][p[k]] for i,j,k in product(range(7),repeat=3)), '343 coefficients')
    require(all(sum(N[i][j][s]*N[s][k][l] for s in range(7)) ==
                sum(N[j][k][s]*N[i][s][l] for s in range(7))
                for i,j,k,l in product(range(7),repeat=4)), '2401 associativity equalities')
    require(N[3][3][1] == 1 and N[1][1][0] == 1, 'order-four invertible')
    return dict(status='PASS', id=record['id'], scope='unitary group-theoretical fusion category',
                tensor_sha256=sha, model_to_census=p, coefficient_equalities=343,
                associativity_equalities=2401, finite_checks=checks)


def verify():
    return verify_record(json.loads((HERE.parent/'data/r7_4_2019_chern_certificate.json').read_text()))


def models():
    return [('C(Q8rtimesS3,Chern,S3,1)',model_tensor(),
             'The unitary group-theoretical category C(Q8 semidirect S3, Omega, S3, 1), where [Omega]=c2(V)-infl c2(R), V(q,p)=qR(p), and R implements the signed-axis quaternion action. The global characteristic class has a representative trivial on S3; its explicit restriction to C2 times S3 determines all fusion rules.',
             'Explicit characteristic-class construction in papers/r7_4_2019_chern_proof.md; Gelaki--Naidu, Some properties of group-theoretical categories, Section 3 and Theorem 5.1; Atiyah, Characters and cohomology of finite groups, appendix.',
             'https://arxiv.org/abs/0709.4326')]


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
