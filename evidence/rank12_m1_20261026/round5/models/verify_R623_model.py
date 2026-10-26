#!/usr/bin/env python3
"""Exact application/binding certificate for the cyclic near-group quotient."""
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

frozen = json.loads((P / 'R623_model_frozen.json').read_text())
tensor = frozen['fusion_tensor']
coordinates = frozen['coordinate_to_input']
require(sorted(coordinates) == list(range(12)), 'coordinate map not bijective')

# All roots of unity are represented by integral exponents modulo72.
# chi_I(x,y)=exp(2pi i*(-2xy)/72), a_I(x)=exp(2pi i*(-x(36-x))/72).
b = lambda x, y: (-2*x*y) % 72
a = lambda x: (-x*(36-x)) % 72
H = list(range(0, 36, 6))
perp = [g for g in range(36) if all(b(h,g) == 0 for h in H)]
require(perp == H, 'H is not maximal isotropic')
require(all(b(h,k) == 0 for h in H for k in H), 'nontrivial H braiding')
ga = [g for g in range(36) if all(a(h) == b(h,g) for h in H)]
require(ga == list(range(3, 36, 6)), 'wrong shifted pointed character')
require(all(a(6*j) == 36*(j % 2) for j in range(6)), 'wrong restriction a|H')

# TPE Eq4.56 mixed-vertex identity in the paper's (non-inverted) convention:
# X(g)Y(g)Z(g) v_h = a(g)^(-1) v_h. This uses no beta/all-X coefficient.
atpe = lambda x: (x*(36-x)) % 72
for g in range(36):
    for h in range(36):
        phase = (2*g*h+atpe(h)-atpe((h-g)%36)) % 72
        require(phase == (-atpe(g)) % 72, 'mixed vertex identity failed')

model = [[[0]*12 for _ in range(12)] for _ in range(12)]
for i in range(12):
    x,u = i%6,i//6
    for j in range(12):
        y,v = j%6,j//6
        row = model[i][j]
        if not (u and v):
            row[(x+(-1 if u else 1)*y)%6+6*(u+v)] = 1
        else:
            row[(x-y+3)%6] = 1
            for k in range(6,12):
                row[k] = 1
        for k in range(12):
            require(tensor[coordinates[i]][coordinates[j]][coordinates[k]] == row[k],
                    f'tensor mismatch at {i,j,k}')

dual = []
for i in range(12):
    candidates = [j for j in range(12) if model[i][j][0]]
    require(len(candidates) == 1, 'nonunique dual')
    dual.append(candidates[0])
require(dual == [(-i)%6 for i in range(6)] + [6+(i+3)%6 for i in range(6)],
        'wrong duality')
require(all(dual[i] != i for i in range(6,12)), 'selfdual noninvertible')

report = {
    'status': 'PASS',
    'ring': 'R12_1_623',
    'construction': 'C36+36 near-group category / central regular H, H=6C36',
    'existence_source': 'arXiv:2610.11652v1, Theorems2.3 and2.10',
    'quotient_proof': 'R623_NEAR_GROUP_MODEL.md (algebraic Izumi12.5)',
    'central_subgroup': H,
    'annihilator': perp,
    'shift_representatives': ga,
    'pointed_square_term_mod6': 3,
    'coordinate_to_input': coordinates,
    'coefficients_checked': 1728,
    'mixed_vertex_phase_identities_checked':1296,
    'duality_coordinates': dual,
    'unitarity_claimed': False,
    'optimizer_used': False,
    'frozen_file_sha256': hashlib.sha256((P/'R623_model_frozen.json').read_bytes()).hexdigest(),
}
(P/'R623_model_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
