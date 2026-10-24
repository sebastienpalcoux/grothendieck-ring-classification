"""Independent exact checks for new R9_2_1975 restrictions; standard library only.

The categorical premises are stated in NEW_RESTRICTIONS.md. This checker
does not turn a based tensor or a bimodule cocycle into a fusion category.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import gzip
from fractions import Fraction
from functools import reduce
from operator import xor

P = Path(__file__).resolve().parent
D = json.loads((P / 'new_results_inputs.json').read_text())
dependency = json.loads((P / 'R6_4_1_dependency.json').read_text())['rows'][0]
assert dependency['id'] == 'R6_4_1'
assert dependency['N'] == D['lower_tensors']['R6_4_1']
assert dependency['decision']['existence']['general'] == 'no'
assert dependency['decision']['certificate']['kind'] == 'oriented_pseudo_gate'
assert hashlib.sha256(json.dumps(dependency['N'],separators=(',',':')).encode()).hexdigest() == dependency['tensor_sha256']
S = D['source_tensor']
N = D['morita_candidates'][0]['N']
C = D['extreme_subcategory']
R = D['lower_tensors']['R6_4_155']
p = D['extreme_to_R155']
assert D['morita_candidates'][0]['alpha'] == 2
assert D['morita_candidates'][0]['a'] == 0
dual = [next(j for j in range(12) if N[i][j][0]) for i in range(12)]
assert all(dual[i] in C for i in C)
assert all(not N[i][j][k] for i, j in product(C, repeat=2)
           for k in set(range(12)) - set(C))
assert all(N[C[i]][C[j]][C[k]] == R[p[i]][p[j]][p[k]]
           for i, j, k in product(range(6), repeat=3))
g = D['conjugating_invertible']
conjugation = []
for i in C:
    a = next(k for k in range(12) if N[g][i][k])
    j = next(k for k in range(12) if N[a][dual[g]][k])
    conjugation.append(j)
assert conjugation == [0, 1, 5, 4, 9, 11]

# The source has trivial universal grading: its adjoint subring is all of S.
sd = [next(j for j in range(9) if S[i][j][0]) for i in range(9)]
adj = {k for i in range(9) for k in range(9) if S[i][sd[i]][k]}
while True:
    nxt = adj | {k for i, j in product(adj, repeat=2)
                 for k in range(9) if S[i][j][k]}
    if nxt == adj:
        break
    adj = nxt
assert adj == set(range(9))
invs = [i for i in range(9) if sum(S[i][sd[i]]) == 1]
central_invs = [i for i in invs if all(S[i][j] == S[j][i] for j in range(9))]
assert central_invs == [0, 5]

bindings = []
for Q in D['conditional_quotients']:
    T, F = Q['quotient_tensor'], Q['source_to_quotient']
    assert all(sum(S[i][j][r] * F[r][k] for r in range(9)) ==
               sum(F[i][a] * F[j][b] * T[a][b][k]
                   for a, b in product(range(6), repeat=2))
               for i, j, k in product(range(9), range(9), range(6)))
    match = Q['matches'][0]
    U, q = D['lower_tensors'][match['id']], match['basis_map']
    assert all(T[i][j][k] == U[q[i]][q[j]][q[k]]
               for i, j, k in product(range(6), repeat=3))
    bindings.append({'group': Q['group'], **match})

# D8 in right semidirect coordinates (x,y,n), and L=D8 x C2.
G = list(product(range(2), repeat=3))
L = list(product(range(2), repeat=4))
def mul(a, b):
    x, y, n = a
    u, v, m = b
    if m:
        x, y = y, x
    return (x ^ u, y ^ v, n ^ m)

def omega(a, b, c, sign=0):
    x, y, n = a
    u, v, m = b
    ell = c[2]
    parity = x ^ y
    if m:
        x, y = y, x
    return (ell * (3 * m * parity + x*u + y*v + 2*y*u)
            + 2 * sign * n*m*ell) % 4

def lm(a, b):
    return (*mul(a[:3], b[:3]), a[3] ^ b[3])

def shear(a):
    return (a[0] ^ a[3], a[1] ^ a[3], a[2])

def beta(a, b):
    x, y, n, eps = a
    u, v, m, eta = b
    return (2*n*eta + 2*n*m + 2*y*eta + 3*y*m + 2*y*m*eta
            + 2*y*u + y*eps*m + x*m + 2*x*m*eta + 2*x*u
            + 3*x*eps*m + 2*x*y*m) % 4

for sign in range(2):
    assert all((omega(b,c,d,sign) - omega(mul(a,b),c,d,sign)
                + omega(a,mul(b,c),d,sign) - omega(a,b,mul(c,d),sign)
                + omega(a,b,c,sign)) % 4 == 0
               for a,b,c,d in product(G, repeat=4))
    assert all((beta(b,c) - beta(lm(a,b),c) + beta(a,lm(b,c))
                - beta(a,b) - omega(a[:3],b[:3],c[:3],sign)
                + omega(shear(a),shear(b),shear(c),sign)) % 4 == 0
               for a,b,c in product(L, repeat=3))
    # Standard cyclic invariant prod_j omega(t,t^j,t).
    restrictions = []
    for t in G:
        power = (0,0,0)
        exponent, order = 0, 0
        while True:
            exponent += omega(t, power, t, sign)
            power = mul(power, t)
            order += 1
            if power == (0,0,0):
                break
        exponent %= 4
        assert order != 4 or exponent == 2
        if order == 2:
            assert exponent == 2*sign*t[2]
        restrictions.append([list(t), order, exponent])

# Exactly replay both feasible solutions of the strengthened necessary
# center relaxation. Rebuilding its categorical column domain is a
# separate, explicitly recorded dependency in the report.
with gzip.open(P / 'no_integral_center_system.json.gz', 'rt') as f:
    relaxation = json.load(f)
witness = json.loads((P / 'no_integral_center_feasibility.json').read_text())
A, b = relaxation['A'], relaxation['b']
system_hash = hashlib.sha256(json.dumps([A,b],separators=(',',':')).encode()).hexdigest()
assert system_hash == witness['system_hash']
assert len(A) == 253 and len(A[0]) == 1109
for kind in ('rational_witness', 'integer_witness'):
    x = [Fraction(0)] * len(A[0])
    for j, value in witness[kind]:
        x[j] = Fraction(value)
    assert all(v >= 0 for v in x)
    assert all(sum(c*v for c,v in zip(row,x)) == target
               for row,target in zip(A,b))
    if kind == 'integer_witness':
        assert all(v.denominator == 1 for v in x)

# Shimizu's finite TY indicator sums for the forced nonalternating V4
# bicharacter, and the ambient induction column of the dimension-two Y.
for epsilon in (-1,1):
    indicators = []
    for k in range(1,5):
        total = sum((-1)**sum((a&b).bit_count()
                             for i,a in enumerate(z) for b in z[i+1:])
                    for z in product(range(4),repeat=k) if reduce(xor,z,0)==0)
        indicators.extend([0,Fraction(epsilon**k*total,2**(k-1))])
    assert indicators == [0,epsilon,0,0,0,epsilon,0,2]
induce_Y = [sum(S[j][8][k]*S[k][sd[j]][i]
                for j,k in product(range(9),repeat=2)) for i in range(9)]
assert induce_Y == [0,16,16,16,16,0,0,0,16]

ty_results = []
for tau in (-1,1):
    with gzip.open(P / f'ty_spectrum_h6_tau{tau}_system.json.gz','rt') as f:
        system = json.load(f)
    cert = json.loads((P / f'ty_spectrum_h6_tau{tau}.json').read_text())
    AA,bb = system['A'],system['b']
    assert cert['system_sha256'] == hashlib.sha256(json.dumps([AA,bb],separators=(',',':')).encode()).hexdigest()
    if tau == 1:
        y = cert['ray']
        assert len(y) == len(AA)
        assert all(type(v) is int for v in y)
        by = sum(v*w for v,w in zip(bb,y))
        aty = [sum(row[j]*v for row,v in zip(AA,y)) for j in range(len(AA[0]))]
        assert by == -32832 and min(aty) == 0
        ty_results.append({'tau_sign':tau,'outcome':'exact Farkas exclusion',
                           'bTy':by,'min_ATy':min(aty)})
    else:
        for kind in ('rational_witness','integer_witness'):
            x = [Fraction(0)] * len(AA[0])
            for j,value in cert[kind]:
                x[j] = Fraction(value)
            assert all(v >= 0 for v in x)
            if kind == 'integer_witness':
                assert all(v.denominator == 1 for v in x)
            assert all(sum(c*v for c,v in zip(row,x)) == target
                       for row,target in zip(AA,bb))
        ty_results.append({'tau_sign':tau,'outcome':'exact necessary integer witness',
                           'support':len(cert['integer_witness'])})

result = {
    'status': 'PASS', 'source': 'R9_2_1975',
    'source_sha256': hashlib.sha256(json.dumps(S,separators=(',',':')).encode()).hexdigest(),
    'excluded_morita_branch': {'alpha':2, 'a':0, 'subring':'R6_4_155',
                              'basis':C, 'basis_map':p,
                              'conjugator':g, 'conjugation':conjugation},
    'remaining_morita_branches': [{'alpha':2,'a':2},{'alpha':3,'a':2}],
    'conditional_central_quotient_bindings': bindings,
    'source_based_central_invertibles': central_invs,
    'source_adjoint_subring_rank': len(adj),
    'full_stabilizer_cocycle_tests': 8192,
    'full_stabilizer_coboundary_tests': 8192,
    'strengthened_center_system': {
        'rows':len(A), 'columns':len(A[0]), 'system_sha256':system_hash,
        'integer_witness_support':len(witness['integer_witness']),
        'outcome':'necessary relaxation feasible, no categorical model'},
    'TY_spectrum_sign_results':ty_results,
    'remaining_TY_sign':-1,
    'source_status': 'unresolved', 'new_models':0,
    'categorical_dependencies': [
        'Rank6 R155 central twist separation from published center proof',
        'Prior complete rank12 Morita reduction',
        'Prior general-complex exclusion of R6_4_1',
        'Central TY lift restriction and de-equivariantization theorem',
        'Shimizu TY indicators and Ng-Schauenburg center trace formula',
        'Prior noncommutative labeled-S and complete central-column domain'],
    'scope': 'Extreme Morita branch and positive TY sign excluded; no whole-source exclusion or model.'}
(P / 'new_results_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
