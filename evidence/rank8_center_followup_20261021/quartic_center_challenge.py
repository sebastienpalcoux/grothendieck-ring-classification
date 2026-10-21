"""Read-only exploratory checks; not an accepted frontier certificate.

Uses frozen source arithmetic but adds fourth Verlinde moments and the exact
pair-product/forgetful Gram intersection. Does not modify either repository.
All checks remain enabled under python -O. No numerical solvers are used.
"""
import argparse
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
ap = argparse.ArgumentParser()
ap.add_argument('--root', type=Path, default=Path.cwd())
args = ap.parse_args()
P = args.root / 'evidence/rank8_frontier_20261021/noncommutative'
sys.path.insert(0, str(P))
import central_support as c
import character_modular as md
import rotation_search as base
import verlinde_low


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def read(path):
    return json.loads(path.read_text())


def rational(x):
    co = list(map(c.s.Rational, c.ec(x)))
    need(len(co) <= 1, 'nonrational fourth moment')
    return co[0] if co else c.s.S.Zero


def s3_control():
    # Electric rows in Z(Vec(S3)). Fluxes e,e,e,(12),(12),(123),(123),(123).
    # The source matrix block has m=2,f=3; beta=6/(3*2)=1.
    ds = [1, 1, 2, 3, 3, 2, 2, 2]
    chs = [[1]*8, [1,1,1,-1,-1,1,1,1], [2,2,2,0,0,-1,-1,-1]]
    S = [[d*x for d,x in zip(ds,ch)] for ch in chs]
    N = [[[0]*3 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        N[0][i][i] = N[i][0][i] = 1
    N[1][1][0] = 1
    N[1][2][2] = N[2][1][2] = 1
    N[2][2] = [1,1,1]
    for i,j,k in itertools.product(range(3), repeat=3):
        val = sum(F(S[i][z]*S[j][z]*S[k][z], ds[z]*36) for z in range(8))
        need(val == N[i][j][k], 'S3 cubic control')
    for i,j,k,l in itertools.product(range(3), repeat=4):
        val = sum(F(S[i][z]*S[j][z]*S[k][z]*S[l][z], ds[z]**2*36) for z in range(8))
        need(val == sum(N[i][j][a]*N[k][l][a] for a in range(3)), 'S3 quartic control')
    return {'cubics':27, 'quartics':81, 'matrix_block_beta':'6/(3*2)=1', 'status':'pass'}


base.install()
census = {r['id']:r for r in read(c.OLD.parent / 'pipeline/census_m3.json')}
pairs = list(itertools.combinations_with_replacement(range(1,5), 2))
quads = list(itertools.combinations_with_replacement(range(1,5), 4))


def prepare(ring, low_index):
    R = census[ring]['tensor']
    a = c.w.data(R)
    K = a['K']
    cols = a['lows'][low_index]
    chs = md.characters(R,a)
    need(all(ch[i] == ch[a['du'][i]] for ch in chs for i in range(8)), 'selfdual low objects')
    high = md.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))[1]
    allcols = [tuple(v) for v in cols] + [(0,)+tuple(v) for v,z in high]
    values = [[a['D']/a['codegrees'][E]/K(a['multiplicities'][E])*md.value(ch,v,K)
               for E,ch in enumerate(chs)] for v in allcols]
    dims = [sum((K(x)*y for x,y in zip(v,a['ds'])),K.zero) for v in allcols]
    return R,a,cols,high,values,dims


def fourth_rows(a,values,dims,permutation):
    inverse = [permutation.index(i) for i in range(5)]
    rows = {}
    for quad in quads:
        i,j,k,l = [inverse[z] for z in quad]
        v = [sv[i]*sv[j]*sv[k]*sv[l]/(d*d*a['D']**2) for sv,d in zip(values,dims)]
        rows[quad] = [sum(v[:5],a['K'].zero)] + v[5:]
    return rows


def check_721():
    saved = read(P/'verlinde_low_721.json')
    R,a,cols,high,values,dims = prepare('R8_3_721',10)
    need(saved['tensor_sha256'] == census['R8_3_721']['tensor_sha256'], 'R721 source binding')
    cases = saved['cases']
    expected_counts,_ = verlinde_low.central_fusion.integral_gram.completions(a,cols)
    assignments = md.assignments(a,md.characters(R,a),cols)
    need(sorted((tuple(x['permutation']),tuple(x['multiplicities'])) for x in cases)
         == sorted((p,m) for p in assignments for m in expected_counts), 'R721 complete case coverage')
    rows_by_perm = {p:fourth_rows(a,values,dims,p) for p in assignments}
    h = c.s.Matrix([[0,0,0,0,1,1,-1,1,-1,1]])
    bytype = {}
    for case in cases:
        perm = tuple(case['permutation'])
        counts = case['multiplicities']
        need(verlinde_low.coefficients(R,a,cols,counts,perm) == case['coefficients'], 'cubic replay')
        lo = {tuple(x['triple']):x['value'] for x in case['coefficients']}
        moments = {q:rational(sum((a['K'](n)*v for n,v in zip([1]+counts,row)),a['K'].zero))
                   for q,row in rows_by_perm[perm].items()}
        need(all(x.q == 1 and x >= 0 for x in moments.values()), 'nonnegative integral fourth moments')
        G = c.s.Matrix(10,10, lambda p,q: moments[tuple(sorted(pairs[p]+pairs[q]))]
             - int(pairs[p][0] == pairs[p][1])*int(pairs[q][0] == pairs[q][1])
             - sum(lo[tuple(sorted(pairs[p]+(e,)))]*lo[tuple(sorted(pairs[q]+(e,)))] for e in range(1,5)))
        T = c.s.Matrix(8,10, lambda k,p:
             sum(cols[pairs[p][0]][u]*cols[pairs[p][1]][v]*R[u][v][k] for u in range(8) for v in range(8))
             - int(pairs[p][0] == pairs[p][1] and k == 0)
             - sum(lo[tuple(sorted(pairs[p]+(e,)))]*cols[e][k] for e in range(1,5)))
        types = [i for i,n in enumerate(counts) for _ in range(n)]
        M = c.s.Matrix.hstack(*(c.s.Matrix((0,)+tuple(high[i][0])) for i in types))
        independent = list(M.T.rref()[1])
        B = M[independent,:]
        X0 = B.T*(B*B.T).inv()*T[independent,:]
        need(M*X0 == T, 'exact minimum-norm forgetful solution')
        need(G.rank() == 4 and M.rank() == 3, 'R721 ranks')
        need(G-X0.T*X0 == c.s.Rational(2,3)*h.T*h, 'rank-one residual Gram')
        choices = []
        for row in range(X0.rows):
            # Every solution is X=X0+t*h, M*t=0, ||t||^2=2/3.
            # Thus |t_i|<1; integrality at pair22 fixes t_i modulo Z.
            ts = [c.s.Integer(n)-X0[row,4] for n in range(math.floor(X0[row,4])-1,math.floor(X0[row,4])+3)]
            ts = [t for t in ts if t*t <= c.s.Rational(2,3)
                  and all((X0[row,j]+t*h[j]).q == 1 and X0[row,j]+t*h[j] >= 0 for j in range(10))]
            need(ts, 'nonempty coordinate correction domain')
            best = min(t*t for t in ts)
            ts = [t for t in ts if t*t == best]
            need(len(ts) == 1, 'unique coordinate minimum')
            choices.append(ts[0])
        t = c.s.Matrix(choices)
        need((t.T*t)[0] == c.s.Rational(2,3), 'minimum squares exhaust exact norm')
        X = X0+t*h
        need(M*X == T and X.T*X == G, 'exact nonnegative integer witness')
        for typ,row in zip(types,X.tolist()):
            row = list(map(int,row))
            need(typ not in bytype or bytype[typ] == row, 'consistent coefficient type')
            bytype[typ] = row
    return {'status':'all_patterns_survive_with_unique_high_pair_coefficients', 'cases':len(cases),
            'quartics_per_case':35, 'pair_order':pairs,
            'high_types':{i:{'restriction':(0,)+tuple(high[i][0]),'coefficients':row} for i,row in sorted(bytype.items())}}


def check_1154():
    domain = read(P.parent/'central_integrality/integer_gram_1154.json')
    filt = read(P/'central_integral_filters_1154.json')
    R,a,cols,high,values,dims = prepare('R8_3_1154',31)
    need(domain['tensor_sha256'] == census['R8_3_1154']['tensor_sha256'], 'R1154 binding')
    need([list(v) for v,z in high] == domain['high_columns'], 'R1154 high ordering')
    need(md.assignments(a,md.characters(R,a),cols) == [(0,1,2,3,4)], 'R1154 unique assignment')
    rows = []
    for quad,raw in fourth_rows(a,values,dims,(0,1,2,3,4)).items():
        co = []
        for value in raw:
            z = list(map(F,c.ec(value)))
            need(len(z) <= 2, 'quadratic field')
            co.append([F(0)]*(2-len(z))+z)
        den = math.lcm(*(x.denominator for z in co for x in z))
        rows.append((quad,[[int(x*den) for x in z] for z in co],den))
    failed = []
    for index in filt['cubic_survivor_indices']:
        m = [1]+domain['completions'][index]
        for quad,co,den in rows:
            irrational = sum(n*z[0] for n,z in zip(m,co))
            rational_part = sum(n*z[1] for n,z in zip(m,co))
            if irrational or rational_part < 0 or rational_part % den:
                failed.append(index)
                break
    need(not failed, 'unexpected R1154 scalar quartic failure')
    return {'status':'scalar_fourth_moment_screen_passes', 'patterns':len(filt['cubic_survivor_indices']),
            'quartics_per_pattern':35, 'high_types':len(high), 'failures':failed,
            'not_tested':'integral simultaneous pair-product Gram factorization'}


sources = [P/'verlinde_low_721.json', P/'central_integral_filters_1154.json',
           P.parent/'central_integrality/integer_gram_1154.json', P/'character_modular.py',
           P/'verlinde_low.py', P/'central_fusion.py']
print(json.dumps({'scope':'exploratory read-only necessary-condition checks; no exclusions or models',
                  'control':s3_control(), 'R721':check_721(), 'R1154':check_1154(),
                  'source_sha256':{str(p.relative_to(args.root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}, indent=2))
