"""Independent finite checks supporting the dimension-160 commutativity proof.

No import of the model search, action construction, or fusion reconstruction.
Only Python's standard library is required. Run from any current directory.
"""
from itertools import combinations, product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mul(x, y):
    z = 0
    for _ in range(4):
        if y & 1:
            z ^= x
        y >>= 1
        x <<= 1
        if x & 16:
            x ^= 19
    return z


def power(x, n):
    z = 1
    for _ in range(n):
        z = mul(z, x)
    return z


def trace(x):
    z = x ^ power(x, 2) ^ power(x, 4) ^ power(x, 8)
    require(z in (0, 1), 'absolute trace')
    return z


V = range(16)
A = [mul(8, x) for x in V]
B = [power(x, 4) for x in V]
H = list(product(range(5), range(2)))


def hmul(g, h):
    return ((g[0] + (1 if g[1] == 0 else -1) * h[0]) % 5,
            g[1] ^ h[1])


def action(h, x):
    return mul(power(8, h[0]), power(x, 4 ** h[1]))


def rank2(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p not in pivots:
                pivots[p] = row
                break
            row ^= pivots[p]
    return len(pivots)


def ring_audit(ident, N):
    n = len(N)
    unit = next(u for u in range(n) if all(
        N[u][i][j] == N[i][u][j] == int(i == j)
        for i, j in product(range(n), repeat=2)))
    dual = [next(j for j in range(n) if N[i][j][unit]) for i in range(n)]
    invertibles = [i for i in range(n) if sum(N[i][dual[i]]) == 1]
    require(len(invertibles) == 2, ident + ': two invertibles')
    g = next(i for i in invertibles if i != unit)
    others = [i for i in range(n) if i not in invertibles]
    solutions = []
    for twos in combinations(others, 2):
        d = [1 if i in invertibles else 2 if i in twos else 5
             for i in range(n)]
        if all(sum(N[i][j][k] * d[k] for k in range(n)) == d[i] * d[j]
               for i, j in product(range(n), repeat=2)):
            solutions.append(d)
    require(len(solutions) == 1, ident + ': exact positive FP character')
    dims = solutions[0]
    require(sum(d*d for d in dims) == 160, ident + ': total dimension')
    adj = {k for i in range(n) for k in range(n) if N[i][dual[i]][k]}
    while True:
        new = adj | {k for i in adj for j in adj for k in range(n)
                     if N[i][j][k]}
        if new == adj:
            break
        adj = new
    require(len(adj) == n, ident + ': trivial universal grading')
    perm = []
    for i in range(n):
        require(N[g][i] == N[i][g] and sum(N[g][i]) == 1,
                ident + ': central invertible permutation')
        perm.append(N[g][i].index(1))
    require(all((perm[i] == i) == (dims[i] == 2) for i in range(n)),
            ident + ': fixed objects of the invertible')
    witness = next(((i, j, k, N[i][j][k], N[j][i][k])
                    for i, j, k in product(range(n), repeat=3)
                    if N[i][j][k] != N[j][i][k]), None)
    require(witness is not None, ident + ': noncommutativity')
    return dict(id=ident, dimensions=dims, unit=unit, dual=dual,
                invertible=g, invertible_permutation=perm,
                adjoint_closure=sorted(adj), noncommutativity_witness=witness)


def field_and_cohomology_audit():
    require(power(8, 5) == 1 and 8 != 1, 'rotation order5')
    require(all(B[A[x]] == action((4, 0), B[x]) for x in V),
            'dihedral action')
    seen, orbits = {0}, []
    for x in range(1, 16):
        if x not in seen:
            orb = sorted({action((k, 0), x) for k in range(5)})
            orbits.append(orb)
            seen.update(orb)
    require([len(o) for o in orbits] == [5, 5, 5], 'three rotation orbits')
    require(all({B[x] for x in o} == set(o) for o in orbits),
            'reflection preserves each rotation orbit')
    fixed = [x for x in V if B[x] == x]
    require(len(fixed) == 4, 'fixed subfield has order4')

    # The diagonals of the standard 14 H^3 generators are all nonconstant
    # squarefree monomials of degrees at most3. Their independence verifies
    # detection by cyclic restrictions, given the standard H^3 presentation.
    monomials = [s for s in range(1, 16) if s.bit_count() <= 3]
    rows = [sum(int(x & s == s) << (x-1) for x in range(1, 16))
            for s in monomials]
    require(rank2(rows) == 14, 'independent cyclic restrictions')
    require(all(r.bit_count() % 2 == 0 for r in rows), 'even parity diagonals')
    # Exhaust all 64 alternating bilinear forms, independently of the trace
    # formula; exactly4 are invariant, and all restrict trivially to F4.
    pairs = list(combinations(range(4), 2))
    invariant = []
    for mask in range(64):
        def form(x, y):
            return sum(((x >> i & 1)*(y >> j & 1) +
                        (x >> j & 1)*(y >> i & 1))
                       for bit, (i, j) in enumerate(pairs)
                       if mask >> bit & 1) % 2
        if all(form(A[x], A[y]) == form(x, y) for x, y in product(V, repeat=2)):
            table = [[form(x, y) for y in V] for x in V]
            require(all(table[x][y] == 0 for x, y in product(fixed, repeat=2)),
                    'invariant alternating form vanishes on fixed space')
            invariant.append(table)
    trace_forms = [[[trace(mul(c, mul(x, power(y, 4)))) for y in V]
                    for x in V] for c in fixed]
    require(len(invariant) == 4 and all(t in invariant for t in trace_forms),
            'all invariant alternating forms are the trace forms')
    return dict(rotation_orbits=orbits, fixed_subfield=fixed,
                diagonal_rank=14, invariant_H3_dimension=2,
                invariant_alternating_forms=4), orbits, fixed


def normal_form_audit(r, orbits, fixed):
    W, J, q = r['omega'], r['J'], r['q']
    mask = r['omega_basis_mask']
    require(mask in (0, 16, 32, 48), 'normal form index')
    require(all(W[0][x][y] == W[x][0][y] == W[x][y][0] == 0 and
                J[0][x] == J[x][0] == q[0] == 0 for x, y in product(V, repeat=2)),
            'normalization')
    require(all((W[y][z][t] - W[x ^ y][z][t] + W[x][y ^ z][t]
                 - W[x][y][z ^ t] + W[x][y][z]) % 2 == 0
                for x, y, z, t in product(V, repeat=4)), 'associator pentagon')
    require(all(W[A[x]][A[y]][A[z]] == W[x][y][z]
                for x, y, z in product(V, repeat=3)), 'strict rotation monoidality')
    require(all(J[A[x]][A[y]] == J[x][y] for x, y in product(V, repeat=2)),
            'rotation invariant reference tensorator')
    # J: F_b(x) tensor F_b(y) -> F_b(x+y). Direct monoidal-functor diagram.
    require(all((J[y][z] + J[x][y ^ z] - J[x][y] - J[x ^ y][z]
                 - 2*(W[x][y][z] - W[B[x]][B[y]][B[z]])) % 4 == 0
                for x, y, z in product(V, repeat=3)), 'reflection monoidality')
    require(all(J[x][y] == J[y][x] for x, y in product(fixed, repeat=2)),
            'reference tensorator symmetric on fixed space')
    require(all((J[x][y]+J[B[x]][B[y]]-q[x]-q[y]+q[x ^ y]) % 4 == 0
                for x, y in product(V, repeat=2)), 'monoidal square compositor')
    require(all(q[action(h, x)] == q[x] for h in H for x in V),
            'square compositor invariance')
    for g, h in product(H, repeat=2):
        gh = hmul(g, h)
        require(all((g[1]*J[action(h, x)][action(h, y)] + h[1]*J[x][y]
                     - gh[1]*J[x][y] - g[1]*h[1]*(q[x]+q[y]-q[x ^ y])) % 4 == 0
                    for x, y in product(V, repeat=2)), 'compositor monoidality')
    for g, h, k in product(H, repeat=3):
        require(all((g[1]*h[1]*q[action(k, x)] + hmul(g,h)[1]*k[1]*q[x]
                     - h[1]*k[1]*q[x] - g[1]*hmul(h,k)[1]*q[x]) % 4 == 0
                    for x in V), 'action pentagon')
    pattern = [W[o[0]][o[0]][o[0]] for o in orbits]
    require(sum(pattern) % 2 == 0, 'invariant diagonal parity')
    return dict(mask=mask, cyclic_restriction_pattern=pattern,
                pointed_pentagons=16**4, reflection_monoidality=16**3,
                full_action_coherence=True, fixed_space_symmetric=True)


def main():
    tensors = json.loads((ROOT/'work/input_audit/tensors.json').read_text())
    ring_checks = [ring_audit(i, tensors[i]) for i in ('R10_1_83', 'R10_1_177')]
    field_checks, orbits, fixed = field_and_cohomology_audit()
    source = ROOT/'work/resolve_integral/normal_forms160.json'
    forms = json.loads(source.read_text())
    form_checks = [normal_form_audit(r, orbits, fixed) for r in forms]
    require({tuple(r['cyclic_restriction_pattern']) for r in form_checks} ==
            {(0,0,0), (0,1,1), (1,0,1), (1,1,0)}, 'all four invariant H3 classes')
    report = dict(status='PASS', input_checks=ring_checks,
                  field_and_cohomology=field_checks, normal_forms=form_checks,
                  normal_forms_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (OUT/'int160_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
