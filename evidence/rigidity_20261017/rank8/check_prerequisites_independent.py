#!/usr/bin/env python3
"""Exact, independent arithmetic checks for the R24 prerequisite audit.

This checks tensors, quadratic identities, and a finite model of the
compression equality space. It does not check categorical coherence.
"""
import argparse
import gzip
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import sympy as sp

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument('--output', type=Path)
args = parser.parse_args()
ROOT = args.repo.resolve()
OUT = args.output
checks = []

def require(value, name):
    if not value:
        raise RuntimeError(name)
    checks.append(name)

with gzip.open(ROOT / 'supplements/rank8/data/rank8_tables.txt.gz', 'rt') as stream:
    candidates = [json.loads(line.translate(str.maketrans('{}', '[]')))
                  for line in stream if line.strip()]
candidates = sorted(t for t in candidates if max(itertools.chain.from_iterable(
    itertools.chain.from_iterable(t))) == 2)
tensor = candidates[23]
digest = hashlib.sha256(json.dumps(tensor, separators=(',', ':')).encode()).hexdigest()
require(digest == '2b4780441d9590e8e7269cd82b7675aa75cec11c39bd3e94bb372cca1ada6738',
        'canonical lexicographic source digest')
decisions = json.loads((ROOT / 'supplements/rank8/data/decisions.json').read_text())
decision = next(t for t in decisions if t['id'] == 'R8_2_24')
require(digest == decision['tensor_sha256'], 'published decision source binding')

unit = [1] + [0]*7
dual = [next(j for j in range(8) if tensor[i][j][0]) for i in range(8)]
invertible = [i for i in range(8) if tensor[i][dual[i]] == unit]
require(invertible == [0, 1, 2, 7], 'four source invertibles')
require(all(tensor[i][j] == tensor[j][i] for i,j in itertools.product(range(8),repeat=2)),
        'commutative source')
require(all(sum(tensor[i][j][u]*tensor[u][k][l] for u in range(8)) ==
            sum(tensor[j][k][u]*tensor[i][u][l] for u in range(8))
            for i,j,k,l in itertools.product(range(8),repeat=4)), 'full source associativity')
neutral = [0, 7, 5, 6]
degree = [0 if i in neutral else 1 for i in range(8)]
require(all(not tensor[i][j][k] or degree[k] == (degree[i]+degree[j]) % 2
            for i,j,k in itertools.product(range(8),repeat=3)), 'faithful source Z2 grading')
adjoint = {0}
for i in range(8):
    adjoint.update(k for k in range(8) if tensor[i][dual[i]][k])
while True:
    grown = adjoint | {k for i,j in itertools.product(adjoint,repeat=2)
                       for k in range(8) if tensor[i][j][k]}
    if grown == adjoint:
        break
    adjoint = grown
require(adjoint == set(neutral), 'neutral category is the adjoint subcategory')
q = [[[tensor[i][j][k] for k in neutral] for j in neutral] for i in neutral]
expected = [
 [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
 [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]],
 [[0,0,1,0],[0,0,0,1],[1,0,2,2],[0,1,2,2]],
 [[0,0,0,1],[0,0,1,0],[0,1,2,2],[1,0,2,2]],
]
require(q == expected, 'all 64 neutral fusion coefficients')
require(all(dual[i] == i for i in neutral), 'neutral self-duality')
require(dual[1] == 2 and tensor[1][1] == [int(i==7) for i in range(8)],
        'actual odd invertible a has inverse 2 and square g')
require(all([sum(tensor[1][x][u]*tensor[u][2][k] for u in range(8))
             for k in range(8)] == [int(k==x) for k in range(8)]
            for x in neutral), 'Ad(a) fixes every neutral simple')

sqrt5 = sp.sqrt(5)
d, dc = 2+sqrt5, 2-sqrt5
dims = [sp.Integer(1) if i in invertible else d for i in range(8)]
require(all(sp.expand(dims[i]*dims[j]-sum(tensor[i][j][k]*dims[k] for k in range(8)))==0
            for i,j in itertools.product(range(8),repeat=2)), 'positive full dimension character')
D, Dc = 20+8*sqrt5, 20-8*sqrt5
require(sp.expand(sum(x*x for x in dims)-2*D)==0, 'full global dimension twice neutral')
characters = [[1,1,d,d],[1,1,dc,dc],[1,-1,1,-1],[1,-1,-1,1]]
require(all(sp.expand(c[i]*c[j]-sum(q[i][j][k]*c[k] for k in range(4)))==0
            for c in characters for i,j in itertools.product(range(4),repeat=2)),
        'four neutral ring characters')
require(sp.simplify(sp.Matrix(characters).det()) != 0, 'neutral character completeness')
codegrees = [sp.expand(sum(x*x for x in c)) for c in characters]
require(codegrees == [D,Dc,4,4], 'neutral formal codegrees')
require(sp.simplify(1/D-1/Dc+1/sqrt5)==0, 'saturated quadratic eigenvalue')

def conjugate(value):
    return sp.expand(value).subs(sqrt5,-sqrt5)

def ell(value):
    return sp.simplify(-20*sp.expand(sp.radsimp(value/D)).coeff(sqrt5))

require([ell(x) for x in [1,1,d,d]] == [2,2,-1,-1], 'source indicator weights')
require([ell(x) for x in [1,sp.simplify(D/Dc),D/4,D/4]] == [2,-2,0,0],
        'induced-unit constituent weights')
a,b = sp.symbols('a b', rational=True)
z = a+b*sqrt5
require(sp.simplify((z/D-conjugate(sp.radsimp(z/D)))+sqrt5*ell(z)/10)==0,
        'S difference coordinate equals nonzero scalar times ell')
for sign,chi in itertools.product([-1,1],repeat=2):
    sigmaD = D if chi==1 else Dc
    sigmaz = z if chi==1 else conjugate(z)
    zpi = sp.radsimp(sign*D*sigmaz/sigmaD)
    require(sp.simplify(ell(zpi)-sign*chi*ell(z))==0,
            f'quadratic coordinate signed Galois transformation {sign} {chi}')
    require(sp.simplify(ell(z)*sigmaz-chi*sigmaD*ell(zpi)*zpi/D)==0,
            f'weighted Galois sign cancellation {sign} {chi}')
forced = [list(t) for t in itertools.product([-1,1],repeat=3)
          if 2+2*t[0]-t[1]-t[2] == -2]
require(forced == [[-1,1,1]], 'unique self-dual indicator sign solution')

# A concrete exact consistency check of the local equality-space refinement.
# This is not used in the theoretical proof for arbitrary prime powers.
M = 25
omega = [(p,qv) for p in range(M) for qv in range(M) if p%5 or qv%5]
index = {v:i for i,v in enumerate(omega)}
chi5 = lambda x: 1 if x%5 in (1,4) else -1
orbits, remaining = [], set(omega)
while remaining:
    p,qv = min(remaining)
    orb = {( (p+t*qv)%M, qv) for t in range(M)}
    orbits.append(orb)
    remaining -= orb
oi = {v:i for i,orb in enumerate(orbits) for v in orb}
torus_map = {i:oi[((13*next(iter(orb))[0])%M,(2*next(iter(orb))[1])%M)]
             for i,orb in enumerate(orbits)}
# Torus pullback h_2 f(p,q)=f(2^-1 p,2q); chi5(2)=-1.
basis = []
remaining = set(range(len(orbits)))
while remaining:
    start = min(remaining)
    cycle, cur = [], start
    while cur not in cycle:
        cycle.append(cur)
        cur = torus_map[cur]
    remaining -= set(cycle)
    if len(cycle)%2:
        continue
    values = {j:(-1)**k for k,j in enumerate(cycle)}
    basis.append(sp.Matrix([values.get(oi[v],0) for v in omega]))
B = sp.Matrix.hstack(*basis)
def ps(v):
    sv = [v[index[(qv,(-p)%M)]] for p,qv in omega]
    means = [sum(sv[index[x]] for x in orb)/len(orb) for orb in orbits]
    return sp.Matrix([means[oi[x]] for x in omega])
A = sp.Matrix.hstack(*(ps(v) for v in basis))
defect = B.T*B/5-A.T*A
kernel = defect.nullspace()
require(len(basis)==6 and len(kernel)==2, 'level25 quadratic local maximal space has dimension two')
F = sp.Matrix([chi5(qv) if qv%5 else 0 for p,qv in omega])
G = sp.Matrix([chi5(-p) if qv%5==0 else 0 for p,qv in omega])
FG = sp.Matrix.hstack(F,G)
maximal = B*sp.Matrix.hstack(*kernel)
require(FG.row_join(maximal).rank()==2, 'local maximal space equals span(F,G)')
require(all(F[index[(p,qv)]] == F[index[(pp,qq)]] and
            G[index[(p,qv)]] == G[index[(pp,qq)]]
            for p,qv in omega for pp,qq in omega
            if p%5==pp%5 and qv%5==qq%5), 'both equality functions factor through reduction modulo five')
receipt = {
 'status':'PASS','check_count':len(checks),'checks':checks,
 'tensor_sha256':digest,'neutral_basis_1_g_r_s':neutral,'source_duality':dual,
 'invertibles':invertible,'grading':degree,'formal_codegrees':[str(x) for x in codegrees],
 'forced_indicators_g_r_s':forced[0],
 'local_test':{'modulus':M,'primitive_vectors':len(omega),'unipotent_orbits':len(orbits),
               'quadratic_torus_space_dimension':len(basis),'maximal_space_dimension':len(kernel)},
 'scope':'exact source/arithmetic/finite-model consistency only; categorical arguments are in final_prerequisite_audit.md'
}
if OUT is not None:
    OUT.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
