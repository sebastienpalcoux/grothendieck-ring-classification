# Locate the enclosing frozen release or the explicitly supplied base.
import os as _task_os
from pathlib import Path as _TaskPath
def _find_release():
    if _task_os.environ.get("RANK6_PACKAGE"):
        return _TaskPath(_task_os.environ["RANK6_PACKAGE"]).resolve()
    for _p in _TaskPath(__file__).resolve().parents:
        for _c in (_p, _p / "Rank6_Categorification_M9"):
            if (_c / "software/round3_m4.py").is_file() and (_c / "data/census.json").is_file():
                return _c
    raise FileNotFoundError("Set RANK6_PACKAGE to the extracted multiplicity-nine package")
_TASK_PACKAGE = _find_release()

"""Exact small checks for the conditional full-B categorical consequences."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = _TASK_PACKAGE
HERE = Path(__file__).resolve().parent
data = json.loads((HERE.parent/'r155_modular/reconstruction.json').read_text())
N = data['fusion_rules']
dual = data['duality']
unit = data['unit']
twists = [12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0]

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

require(unit == 1, 'unit label changed')
bosons = {i for i,t in enumerate(twists) if t == 0}
require(bosons == {1,2,5,23,25}, 'twist-one support')
require(dual[2] == 5, 'bosonic dual pair')
square = {k for k,n in enumerate(N[2][2]) if n}
norm_product = {k for k,n in enumerate(N[2][5]) if n}
require(not square & bosons, 'square must have no allowed algebra constituent')
require(norm_product & bosons == {unit}, 'dual product must meet algebra only at unit')

def close(initial):
    a = {unit} | set(initial)
    while True:
        b = a | {dual[i] for i in a}
        b |= {k for i in a for j in a for k,n in enumerate(N[i][j]) if n}
        if b == a:
            return tuple(sorted(a))
        a = b

subcats = {close(())}
queue = list(subcats)
while queue:
    a = queue.pop()
    for i in range(26):
        b = close((*a, i))
        if b not in subcats:
            subcats.add(b)
            queue.append(b)
require(sorted(map(len,subcats)) == [1,2,16,26], 'fusion subcategory lattice')

packets = json.loads((PACKAGE/'research/round5/m4_155/packet_frontier.json').read_text())
q = next(x for x in packets['splittings'] if x['profile']==296 and x['survivors'])
packet = next(x for x in packets['cases'] if x['profile']==296)['survivors'][q['orientation']]
W = packet['W']
R = next(x['N'] for x in json.loads((PACKAGE/'data/census.json').read_text()) if x['id']=='R6_4_155')
for i in range(26):
    for j in range(26):
        lhs = [sum(W[i][k]*W[j][l]*R[k][l][c] for k in range(6) for l in range(6)) for c in range(6)]
        rhs = [sum(N[i][j][k]*W[k][c] for k in range(26)) for c in range(6)]
        require(lhs == rhs, f'restriction product {(i,j)}')

# b=18+12sqrt(2); these are exact quadratic norms.
dim_norm = 8**2*(18**2-2*12**2)**2
rejected = {'b+1':19**2-2*12**2, '2b-1':35**2-2*24**2, '2b+1':37**2-2*24**2}
require(dim_norm == 82944, 'global dimension norm')
for name,norm in rejected.items():
    require(dim_norm % (norm*norm) != 0, f'norm obstruction for {name}')

receipt = {
    'scope':'Necessary categorical consequences of the reconstructed B fusion ring; not categorification',
    'bosons':sorted(bosons),
    'square_2_support':sorted(square),
    'product_2_5_support':sorted(norm_product),
    'allowed_connected_etale_underlying_objects':[[1],[1,23],[1,23,25]],
    'rejected_dimension_norms':rejected,
    'global_dimension_norm':dim_norm,
    'fusion_subcategories':sorted(subcats,key=lambda a:(len(a),a)),
    'restriction_products_checked':676,
    'restriction_products_pass':True,
}
(HERE/'full_fusion_categorical_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
