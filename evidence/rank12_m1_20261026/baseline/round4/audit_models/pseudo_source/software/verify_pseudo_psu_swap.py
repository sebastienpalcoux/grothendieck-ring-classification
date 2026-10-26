"""Exact tensor-auto-equivalence and C2-action for unitary pseudo-PSU(2)_6."""
import hashlib
import itertools
import json
import re
from pathlib import Path

import sympy as s
from sympy import QQ

from verify_r8_1_7_zesting import check_base, require

HERE = Path(__file__).resolve().parents[1] / 'data'
PHI = [0,1,3,2]
AMP = [-1,-1,0,-1,-1,-1,-1,-1,0,-1,0,-1,0,-1,0,0,0]
PHASE = [29,15,10,17,1,5,5,11,0,1,16,15,4,5,0,0,0]


def check_action():
    R, base_receipt = check_base(2)
    t = s.Symbol('t')
    K = QQ.alg_field_from_poly(s.Poly(t**4+1,t))
    z = K([1,0])
    root2 = z-z**3
    raw = (HERE/'cat_4_1_2_4_2_0_1.jl').read_text()
    F = {tuple(int(x)-1 for x in keys.split(',')):
         K([QQ(x.strip().replace('//','/')) for x in reversed(cs.split(','))])
         for keys,cs in re.findall(r'\[([\d, ]+)\]\s*=>\s*QQFieldElem\[([^\]]+)\]',raw)}
    support = [(i,j,k) for i,j,k in itertools.product(range(4), repeat=3)
               if R[i][j][k]]
    variables = [(i,j,k) for i,j,k in support if i and j]
    require(len(variables) == len(AMP) == len(PHASE) == 17)
    J = {tr: K.one for tr in support}
    J.update({tr: root2**a*z**b for tr,a,b in zip(variables,AMP,PHASE)})
    require(all(R[i][j][k] == R[PHI[i]][PHI[j]][PHI[k]]
                for i,j,k in itertools.product(range(4), repeat=3)))
    # Tensorator J: tau(X) tensor tau(Y) -> tau(X tensor Y).
    # With this source F convention, its coherence is the displayed identity.
    for key, value in F.items():
        a,b,c,d,e,f = key
        require(J[a,b,e]*J[e,c,d]*value ==
                F[tuple(PHI[i] for i in key)]*J[b,c,f]*J[a,f,d],
                'tensor functor associativity')
    eta = [K.one, (K.one+z**2)/2, -(K.one+z**2)/2, -(K.one+z**2)/2]
    square = {tr: J[tr]*J[tuple(PHI[i] for i in tr)] for tr in support}
    for i,j,k in support:
        require(eta[i]*eta[j] == eta[k]*square[i,j,k], 'tau squared monoidality')
    require(all(eta[PHI[i]] == eta[i] for i in range(4)), 'C2 action coherence')
    # Any tensor automorphism of Id has chi_i chi_j=chi_k on fusion support.
    # xy contains 1,x,y, forcing chi_x=chi_y=1; x² contains g, forcing chi_g=1.
    require(R[2][3] == [1,0,1,1] and R[2][2] == [0,1,1,1])
    return R, dict(status='PASS', base=base_receipt, permutation=PHI,
                   tensorator_variables=[list(tr) for tr in variables],
                   sqrt2_exponents=AMP, zeta8_exponents=PHASE,
                   tensorator_equations=len(F), square_equations=len(support),
                   eta_coefficients=[[1,0],[s.Rational(1,2),s.Rational(1,2)],
                                     [-s.Rational(1,2),-s.Rational(1,2)],
                                     [-s.Rational(1,2),-s.Rational(1,2)]],
                   group_action_coherence=True, tensor_identity_automorphisms_trivial=True)


def model_tensor(R, epsilon):
    require(epsilon in (0,1))
    act = [1,0,3,2]
    T = [[[0]*8 for _ in range(8)] for _ in range(8)]
    for a,b,i,j,k in itertools.product(range(2),range(2),range(4),range(4),range(4)):
        out = 4*((a+b)%2)+(act[k] if epsilon*a*b else k)
        T[4*a+i][4*b+j][out] = R[i][PHI[j] if a else j][k]
    return T


def verify_record(record, R=None):
    if R is None:
        R, _ = check_action()
    require(record['id'] in ('R8_1_11','R8_1_42'))
    epsilon = int(record['id'] == 'R8_1_11')
    require(record['central_twist_exponent'] == epsilon)
    T = model_tensor(R, epsilon)
    N,p = record['tensor'],record['model_to_census']
    sha = hashlib.sha256(json.dumps(N,separators=(',',':')).encode()).hexdigest()
    require(sha == record['tensor_sha256'])
    require(sorted(p) == list(range(8)) and p[0] == 0)
    require(all(T[i][j][k] == N[p[i]][p[j]][p[k]]
                for i,j,k in itertools.product(range(8), repeat=3)), 'census equality')
    require(T[4][4][epsilon] == 1 and sum(T[4][4]) == 1)
    return dict(id=record['id'], tensor_sha256=sha, coefficient_equalities=512,
                model_to_census=p, central_twist_exponent=epsilon)


def verify():
    R, action = check_action()
    records = json.loads((HERE/'pseudo_psu_swap_certificates.json').read_text())
    require([r['id'] for r in records] == ['R8_1_11','R8_1_42'])
    return dict(status='PASS', exact=True, action=action,
                models=[verify_record(r,R) for r in records])


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, default=str))
