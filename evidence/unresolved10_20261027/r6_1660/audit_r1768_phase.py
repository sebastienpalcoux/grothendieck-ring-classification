"""Check the full RW cocycle indices in the R1768 diagonal phase proof."""
from pathlib import Path
import contextlib, io, json, runpy

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'root/verify_diagonal_phase.py'
with contextlib.redirect_stdout(io.StringIO()):
    data = runpy.run_path(str(SOURCE))
Q, F, need = data['Q'], data['F'], data['require']
w, epsilon = Q(7, 1), Q(73, 12)
gamma = ((157, -144), (12, -11))
gamma_inverse = ((-11, 144), (-12, 157))

def multiply(A, B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))

matrix = ((1, 0), (0, 1))
bs = [14] + [2]*11
for b in bs:
    matrix = multiply(matrix, ((b, -1), (1, 0)))
need(matrix == gamma, 'HJ monodromy mismatch')
rows = []
for l in range(1, 12):
    x, m = F(12-l, 12), l-12
    z0, z = x*w, l*w/(1/epsilon-1)
    need(z0-z == (l+1)*w-l, 'argument shift mismatch')
    shift = (l+1, -l)
    shifted_index = (
        l + sum(shift[k]*(gamma_inverse[k][0]-(k == 0)) for k in range(2)),
        sum(shift[k]*(gamma_inverse[k][1]-(k == 1)) for k in range(2)))
    need(shifted_index == (m, -12*m), 'index shift mismatch')
    need((1/epsilon-1)*z0 == m*w-12*m, 'new special argument mismatch')

    trajectory = data['rows'][l-1]['trajectory']
    xs = [F(r['x']) for r in trajectory]
    ys = [F(r['y']) for r in trajectory]
    ws = [Q(*r['w']) for r in trajectory]
    xs.append(xs[0]); ys.append(ys[0]); ws.append(ws[0])
    us, vs = [None]*13, [None]*13
    us[12], vs[12] = xs[12], ys[12]
    for j in range(12, 0, -1):
        us[j-1], vs[j-1] = -vs[j], us[j]+bs[j-1]*vs[j]
    ms = [xs[j]-us[j] for j in range(13)]
    need(all(t.denominator == 1 for t in ms), 'nonintegral cocycle index')
    need(ms[12] == 0 and ms[0] == -m, 'endpoint indices mismatch')
    for j in range(1, 13):
        zj = us[j]*ws[j]+vs[j]
        need(zj+ms[j]*ws[j]-ms[j-1] == xs[j]*ws[j]+ys[j]-1,
             'individual cocycle argument mismatch')
    rows.append({'l': l, 'm': m, 'm_j': [int(t) for t in ms]})

receipt = {'status': 'PASS', 'all_132_cocycle_arguments_exact': True,
           'all_143_cocycle_indices_integral': True,
           'all_11_endpoint_normalizations_exact': True,
           'phase_source_all_zero': True, 'rows': rows}
(HERE / 'r1768_phase_audit.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'rows'}, indent=2))
