"""An explicit feasible higher-trace system from Z(Rep(D14))."""
if not __debug__:
    raise RuntimeError("Run this audit with Python assertions enabled")

from pathlib import Path
from fractions import Fraction as Q
import sys
import sympy as s

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'final_census/criteria'))
from models import dihedral14
from exact import require
import higher_traces as ht

R = dihedral14()
data = ht.quadratic_data(R)
# Conjugacy classes: identity, the reflections, three pairs of rotations.
# Their trivial-centralizer representations give the five I(1) columns.
low = [(1,0,0,0,0), (1,0,1,1,1)]+[(1,1,0,0,0)]*3
require(tuple(low) in data['lows'], 'explicit unit-induction matrix absent')
L = s.Matrix.hstack(*map(s.Matrix, low))
require(ht.low_failure(tuple(low), data['ch'].C, data['ds'], data['D'],
                       data['K'], data['embedding'], data['ch'].du) is None,
        'explicit unit-induction matrix falsely excluded')
A, b, meta = ht.build_system(R, data, L, (1,1,1,1), height=6)
types, _ = ht.trace_types(1, [2,7], 6)
one = tuple((Q(1), Q(0)) for _ in range(6))
minus = tuple((Q((-1)**j), Q(0)) for j in range(1,7))
seven = tuple((Q(-1,6), Q(0)) for _ in range(6))
counts = {}
for i in range(4):
    v = tuple(int(i==j) for j in range(4))
    counts[v, types.index(one)] = 1
    if i:
        counts[v, types.index(seven)] = 6
counts[(1,1,1,1), types.index(minus)] = 1
labels = {(tuple(v), index): k for k, (v, index) in enumerate(meta['labels'])}
require(set(counts) <= set(labels), 'a genuine central-simple column was omitted')
x = [0]*meta['high_variables']
for label, count in counts.items():
    x[labels[label]] = count
require(sum(x)==23, 'incorrect number of remaining center simples')
residual = [rhs-sum(row[j]*x[j] for j in range(len(x))) for row, rhs in zip(A,b)]
slack = 2*4*4  # two inequalities for four nonunit objects at orders 3,4,5,6
require(all(v==0 for v in residual[:-slack]), 'a genuine center violates the equality rows')
require(all(v>=0 for v in residual[-slack:]), 'a genuine center violates an indicator inequality')
print('Explicit Z(Rep(D14)) center: all five low and 23 high simples survive the column filters;')
print('all Gram/moment equalities and 32 higher-indicator inequalities hold exactly through order 6.')
