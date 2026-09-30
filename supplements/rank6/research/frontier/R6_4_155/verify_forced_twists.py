"""Exact arithmetic for the analytic profile-296 forced-twist reduction.

This verifies the polynomial moment identities and final low balancing, not
existence of modular data or a fusion category. No optimizer is used.
Run from an unpacked release, or pass --package /path/to/release.
"""
from pathlib import Path
from collections import Counter
import sys, json, argparse, hashlib


def detect_package():
    for ancestor in Path(__file__).resolve().parents:
        for candidate in (ancestor, ancestor/'work_round6/Rank6_Categorification_M8'):
            if (candidate/'software/round3_m4.py').is_file() and (candidate/'data/census.json').is_file():
                return candidate
    raise FileNotFoundError('Cannot locate the release; supply --package')


p = argparse.ArgumentParser()
p.add_argument('--package', type=Path)
p.add_argument('--output', type=Path)
args = p.parse_args()
P = args.package.resolve() if args.package else detect_package()
sys.path.insert(0, str(P/'software'))
import scipy.optimize


def forbidden(*a, **k):
    raise RuntimeError('Optimizer forbidden in this exact verifier')


scipy.optimize.linprog = scipy.optimize.milp = forbidden


def require(value, message):
    if not value:
        raise ValueError(message)


import round3_m4 as M
R = next(x['N'] for x in json.load(open(P/'data/census.json')) if x['id'] == 'R6_4_155')
dat = M.data_for(R, 3, 24)
C, tab = dat['C'], dat['tab']
cols = dat['lows'][6]
lab = tab.assignments(cols)[0]
d = dat['dims'][1]
bd, DD = C(2)+4*d, dat['DD']
DB = DD**2/C(2)
roots = [C.unit**j for j in range(24)]
ii = roots[6]
packet_path = P/'research/round5/m4_155/packet_frontier.json'
cc = json.load(open(packet_path))
q = next(x for x in cc['splittings'] if x['profile'] == 296 and x['survivors'])
require(len(q['survivors']) == 1, 'Expected the sole frozen packet')
pac = next(x for x in cc['cases'] if x['profile'] == 296)['survivors'][q['orientation']]
z = q['survivors'][0]
W, eps = list(map(tuple, pac['W'])), z['charges']
Na, Nb = z['Na'], z['Nb']
dims = [sum((C(a)*b for a, b in zip(v, dat['dims'])), C.zero) for v in W]
require(len(W) == 26 and eps.count(1) == 16 and eps.count(-1) == 10, 'Wrong rank or charges')
require([i for i,e in enumerate(eps) if e == -1] == [4,7,12,13,14,15,20,21,24,25], 'Wrong odd positions')
require(DB == 8*bd**2 == 144*d**2, 'Dimension normalization failed')
for i in range(26):
    for j in range(26):
        dot = sum(a*b for a,b in zip(W[i], W[j]))
        require(Na[i][j] == (dot-int(i==j) if eps[i]==eps[j] else 0), 'N_A Gram identity failed')
        require(Nb[i][j] == (dot if eps[i]!=eps[j] else 0), 'N_B Gram identity failed')

# Sparse Laurent polynomials in t=a^2, p=c^2, q=e^2, over Q(zeta_24).
zero = (0,0,0)

def poly(value):
    return {} if value == C.zero else {zero:C.convert(value)}

def add(*polys):
    result = {}
    for x in polys:
        for k,v in x.items():
            result[k] = result.get(k,C.zero)+v
    return {k:v for k,v in result.items() if v != C.zero}

def scale(x, a):
    return {k:v*a for k,v in x.items() if v*a != C.zero}

def mul(x,y):
    result = {}
    for k,v in x.items():
        for l,w in y.items():
            m = tuple(a+b for a,b in zip(k,l))
            result[m] = result.get(m,C.zero)+v*w
    return {k:v for k,v in result.items() if v != C.zero}

def bar(x):
    # The expressions used here have real coefficients.
    return {tuple(-a for a in k):v for k,v in x.items()}

variables = {2:0,3:0,5:0,6:0,8:1,9:1,10:2,11:2}
base = {0:12,1:0,4:21,7:21,12:5,13:5,14:13,15:13,16:6,17:6,18:18,19:18,20:9,21:9,22:12,23:0,24:18,25:0}

def squared_twist(j, sign=1):
    if j in variables:
        exponent = [0,0,0]
        exponent[variables[j]] = sign
        return {tuple(exponent):C.one}
    return poly(roots[(sign*2*base[j])%24])

def moments(charge, sign):
    return [add(*(scale(squared_twist(j,sign), C(W[j][k])*dims[j])
                  for j in range(26) if eps[j] == charge)) for k in range(6)]

F = add(poly(C(8)), {(1,0,0):C(2)}, {(0,1,0):C(4)}, {(0,0,1):C(4)})
Fb = bar(F)
Ep, Em, Op, Om = moments(1,1), moments(1,-1), moments(-1,1), moments(-1,-1)
for k in range(6):
    if k in (1,2):
        require(Ep[k] == scale(F,d) and Em[k] == scale(Fb,d), 'Even moment identity failed')
        require(Op[k] == poly(-6*ii*d) and Om[k] == poly(6*ii*d), 'Odd moment identity failed')
    else:
        expected = poly(bd if k in (0,3) else -bd)
        require(Ep[k] == Em[k] == Op[k] == Om[k] == expected, 'Invertible moment identity failed')

nu2a = scale(add(*(mul(x,y) for x,y in zip(Ep,Em)),
                  *(mul(x,y) for x,y in zip(Op,Om)), poly(-DB)), C.one/DB)
nu2b = scale(add(*(mul(x,y) for x,y in zip(Ep,Om)),
                  *(mul(x,y) for x,y in zip(Op,Em))), C.one/DB)
require(nu2a == scale(add(mul(F,Fb),poly(C(36))), C.one/C(72)), 'nu2(A) polynomial failed')
require(nu2b == add(poly(C.one),scale(add(F,scale(Fb,-C.one)),ii/C(12))), 'nu2(B) polynomial failed')

# For n=4 the semion partner contributes W_X+W_Y, because i^4=1.
nu4 = scale(add(*(scale(mul(squared_twist(j),squared_twist(j)),
                          C(W[j][1]+W[j][2])*dims[j]) for j in range(26))), C.one/DD)
sqrt2 = (d-C(4))/C(3)
nu4_expected = add(poly(C(4)), scale({zero:C.one,(2,0,0):C.one,(0,2,0):C(2),(0,0,2):C(2)}, C.one/(C(3)*sqrt2)))
require(nu4 == nu4_expected, 'nu4 polynomial failed')
require(sum(R[1][1][k]*R[1][1][l]*R[k][l][0] for k in range(6) for l in range(6)) == 34, 'Four-rotation dimension failed')

# The analytic proof forces t=1 and {p,q}={zeta_3,zeta_3^2}.
# Signs and swapping equal charged columns change only labels.
exps = [12,0,0,12,21,0,12,21,4,16,8,20,5,5,13,13,6,6,18,18,9,9,12,0,18,0]
for v in W:
    tab.prepare(v)
for a,N,dl in [(1,Na,C(1)+4*d),(2,Nb,bd)]:
    for j in range(26):
        rhs = sum((C(N[k][j])*dims[k]*roots[exps[k]] for k in range(26)),C.zero)
        lhs = roots[exps[j]]*dl*tab.values[lab[a],W[j]]
        require(rhs == lhs, 'Final complete low balancing failed')
require(sum((dims[j]**2*roots[exps[j]] for j in range(26)),C.zero) == DD/(C.one+ii), 'Gauss sum failed')
out = {'passed':True, 'optimizer_used':False, 'profile':296,
       'scope':'necessary_forced_twist_reduction_not_realization',
       'symbolic_second_indicator_identities':True, 'symbolic_fourth_indicator_identity':True,
       'complete_low_balancing':True, 'B_rank':26, 'B_twist_exponents_mod24':exps,
       'center_rank':52,
       'center_twist_multiplicities_mod24':dict(sorted(Counter(exps+[(x+6)%24 for x in exps]).items())),
       'source_packet_sha256':hashlib.sha256(packet_path.read_bytes()).hexdigest()}
if args.output:
    args.output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
