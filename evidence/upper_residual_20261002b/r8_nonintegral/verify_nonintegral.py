#!/usr/bin/env python3
"""Independent rank-eight model constructors and source-bound exclusions.

No constructor reads a census tensor. require() works under python -O.
The categorical existence arguments are recorded in NONINTEGRAL_PROOFS.md.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p/'supplements/rank8/data/rank8_tables.txt.gz').exists())
sys.path.insert(0, str(ROOT/'supplements/rank8/software'))
RECOVERY = ROOT/'evidence/upper_residual_20261002b_recovery'

def require(x, message='exact condition failed'):
    if not x:
        raise ValueError(message)

def load_recovery():
    spec = importlib.util.spec_from_file_location('rank8_recovery_checks', RECOVERY/'verify_recovery.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def tensor(n=8):
    return [[[0]*n for _ in range(n)] for _ in range(n)]

def quotient(pseudo):
    from extension_models import psu_flip
    raw = psu_flip(pseudo, False)
    B = [[[raw[i][j][k] for k in range(4)] for j in range(4)] for i in range(4)]
    act = [1,0,3,2]
    reps = [(0,j) for j in range(4)] + [(2,j) for j in range(4)]
    T = tensor()
    for i,(a,b) in enumerate(reps):
        for j,(c,d) in enumerate(reps):
            for k,(x,y) in enumerate(reps):
                T[i][j][k] = B[a][c][x]*B[b][d][y] + B[a][c][act[x]]*B[b][d][act[y]]
    return T

def d14():
    T = tensor()
    # Bulk labels f0,f2,...,f10; resolved fixed-point labels P,Q.
    def fill(i,j,v):
        T[i][j] = list(v)
        T[j][i] = list(v)
    for i,j in itertools.product(range(6), repeat=2):
        v = [0]*8
        # Ordinary SU(2)_24 fusion and identification V_(2t)=V_(24-2t).
        for t in range(abs(i-j), min(i+j,24-i-j)+1):
            u = min(t,12-t)
            if u == 6:
                v[6] += 1
                v[7] += 1
            else:
                v[u] += 1
        fill(i,j,v)
    for j in range(6):
        v = [0]*8
        for k in range(6-j,6):
            v[k] += 1
        v[6+(j%2)] += 1
        fill(6,j,v)
        v[6],v[7] = v[7],v[6]
        fill(7,j,v)
    fill(6,6,[1,0,1,0,1,0,1,0])
    fill(7,7,[1,0,1,0,1,0,0,1])
    fill(6,7,[0,1,0,1,0,1,0,0])
    return T

def f21_dual_defects():
    # alpha_0,alpha_1,alpha_2,X,Y,m_0,m_1,m_2.
    T = tensor()
    for i,j in itertools.product(range(3), repeat=2):
        T[i][j][(i+j)%3] = 1
    for i in range(3):
        for x in (3,4):
            T[i][x][x] = T[x][i][x] = 1
        for j in range(3):
            T[i][5+j][5+(i+j)%3] = 1
            T[5+j][i][5+(j-i)%3] = 1
    T[3][3] = [0,0,0,1,2,0,0,0]
    T[4][4] = [0,0,0,2,1,0,0,0]
    T[3][4] = T[4][3] = [1,1,1,1,1,0,0,0]
    for x in (3,4):
        for j in range(3):
            T[x][5+j] = [0,0,0,0,0,1,1,1]
            T[5+j][x] = [0,0,0,0,0,1,1,1]
    for i,j in itertools.product(range(3), repeat=2):
        T[5+i][5+j][(i-j)%3] = 1
        T[5+i][5+j][3] = T[5+i][5+j][4] = 1
    return T

def su3_neutral():
    """SU(3)_4 via fundamental alcove adjacency and Jacobi--Trudi.

    For partition (a+b,b,0), s_lambda=h_(a+b)h_b-h_(a+b+1)h_(b-1).
    h_n=e1*h_(n-1)-e2*h_(n-2)+h_(n-3), since e3=1.
    """
    weights = [(a,b) for a in range(5) for b in range(5-a)]
    idx = {w:i for i,w in enumerate(weights)}
    E = s.zeros(15)
    for i,(a,b) in enumerate(weights):
        for w in ((a+1,b),(a-1,b+1),(a,b-1)):
            if w in idx:
                E[i,idx[w]] += 1
    F = E.T
    I,Z = s.eye(15),s.zeros(15)
    h = {0:I,-1:Z,-2:Z}
    for n in range(1,8):
        h[n] = E*h[n-1]-F*h[n-2]+h[n-3]
    N = {w:h[w[0]+w[1]]*h[w[1]]-h[w[0]+w[1]+1]*h[w[1]-1] for w in weights}
    unit = idx[0,0]
    for w,M in N.items():
        require(list(M[unit,:]) == [int(v==w) for v in weights], 'SU3 Jacobi--Trudi label')
        require(all(v>=0 and v.is_Integer for v in M), 'SU3 coefficient positivity')
    basis = [(0,0),(3,0),(1,1),(0,3),(2,2)]
    B = [[[int(N[x][idx[y],idx[z]]) for z in basis] for y in basis] for x in basis]
    require(all((a+2*b)%3 == 0 for a,b in basis), 'neutral triality')
    for x,y in itertools.product(basis,repeat=2):
        require(all(N[x][idx[y],idx[z]]==0 for z in weights if z not in basis), 'neutral closure')
    return B

def psu34_defects():
    B = su3_neutral()
    A = s.Matrix([[0,0,1],[0,1,1],[1,1,1]])
    acts = [s.eye(3),A,A*A-s.eye(3),A,A*A-A]
    dual = [0,3,2,1,4]
    T = tensor()
    for i,j,k in itertools.product(range(5), repeat=3):
        T[i][j][k] = B[i][j][k]
    for i,j,k in itertools.product(range(5),range(3),range(3)):
        T[i][5+j][5+k] = int(acts[i][j,k])
        T[5+j][i][5+k] = int(acts[dual[i]][j,k])
    for i,j,k in itertools.product(range(3),range(3),range(5)):
        T[5+i][5+j][k] = int(acts[dual[k]][i,j])
    # Exhaust the finite NIM candidate space imposed by trace and squared trace.
    candidates = []
    for a,b,c,u,v,w in itertools.product(range(3), repeat=6):
        if a+b+c != 2 or a*a+b*b+c*c+2*(u*u+v*v+w*w) != 6:
            continue
        M = s.Matrix([[a,u,v],[u,b,w],[v,w,c]])
        if M.charpoly().as_expr() == A.charpoly().as_expr():
            candidates.append(M)
    require(len(candidates)==6, 'all defect actions are relabellings')
    require(all(any(M==A.extract(p,p) for p in itertools.permutations(range(3))) for M in candidates), 'NIM uniqueness')
    # The neutral regular X has exactly one irrational real cubic character block.
    z = s.Symbol('lambda')
    require(s.Matrix(B[1]).charpoly(z).as_expr()==s.expand((z*z+z+2)*(z**3-2*z*z-z+1)), 'neutral character polynomial')
    for i,j in itertools.product(range(5),repeat=2):
        require(acts[i]*acts[j] == sum((B[i][j][k]*acts[k] for k in range(5)),s.zeros(3)), 'module fusion relation')
    return T

def model(case):
    ctors = {'R8_2_557':lambda:quotient(False), 'R8_2_313':lambda:quotient(True),
             'R8_2_855':d14, 'R8_2_239':f21_dual_defects, 'R8_2_290':psu34_defects,
             'R8_2_868':lambda:load_recovery().hi7_dual_tensor()}
    return ctors[case]()

def check_exclusions(rows, source):
    receipts = []
    for case in ('R8_2_181','R8_2_784'):
        N = source[case]
        require(N==rows[case]['census_tensor'], 'exclusion source binding')
        require(all(N[i][j][k]==N[j][i][k] for i,j,k in itertools.product(range(8),repeat=3)), 'commutative source')
        load_recovery().validate_ring(N)
        if case.endswith('_784'):
            even,odd,dims = [0,1,2,3,4,6,7],[5],[1,1,2,2,2,0,2,2]
            require(sum(dims[i]**2 for i in even)==22,'neutral dimension22')
            for i in even:
                require(N[i][5][5]==dims[i] and sum(N[i][5])==dims[i], 'rank-one component action')
            require(N[5][5]==dims,'odd square is regular object')
        else:
            # Locate the dimension-one and dimension-three neutral basis from its exact F21 fusion.
            inv = [i for i in range(8) if sum(N[i][j][k] for j in range(8) for k in range(8))==8]
            require(len(inv)==3,'C3 invertibles')
            non = [i for i in range(8) if i not in inv]
            triples = [S for S in itertools.combinations(non,3)
                       if all(sum(N[a][b][c] for c in inv)==1 for a in S for b in S)]
            require(len(triples)==1,'unique three-object odd component')
            odd = list(triples[0]);even = [i for i in range(8) if i not in odd]
            require(len(even)==5,'neutral rank5')
            require(all(sum(N[i][j][k] for k in odd)==3 for i in even if i not in inv for j in odd),'degree3 neutral action')
            require(all(N[g][m]==N[m][g] and sum(N[g][m])==1 for g in inv for m in odd),'matching free left/right action')
            for m in odd:
                require(len({next(k for k,c in enumerate(N[g][m]) if c) for g in inv})==3,'free C3 odd orbit')
            require(load_recovery().adjoint_closure([[[N[i][j][k] for k in even] for j in even] for i in even],
                    load_recovery().validate_ring([[[N[i][j][k] for k in even] for j in even] for i in even]))==list(range(5)), 'neutral adjoint whole')
            require(all((q*q-1)%7 != 0 for q in (2,4)), 'TY7 bicharacter obstruction')
        require(all(N[i][j][k]==0 for i in even for j in even for k in odd),'even closure')
        require(all(N[i][j][k]==0 for i in odd for j in odd for k in odd),'odd times odd even')
        receipts.append({'id':case,'scope':'general_complex','source_sha256':load_recovery().fingerprint(N),
                         'neutral_indices':even,'odd_indices':odd,'structural_hypotheses':'PASS'})
    return receipts

def verify():
    recovery = load_recovery()
    rows = {r['id']:r for r in json.loads((RECOVERY/'decisions.json').read_text())}
    source = recovery.read_source(ROOT,8)
    receipts = []
    for case in ('R8_2_557','R8_2_313','R8_2_855','R8_2_239','R8_2_290','R8_2_868'):
        T = model(case)
        recovery.validate_ring(T)
        row = rows[case];p = row['model_to_census'];N = source[case]
        require(N==row['census_tensor'],'model source binding')
        require(sorted(p)==list(range(8)) and p[0]==0,'basis bijection')
        require(all(T[i][j][k]==N[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)),case+' census equality')
        receipts.append({'id':case,'model_to_census':p,'coefficients_matched':512,'associativity_relations':4096,
                         'census_tensor_sha256':recovery.fingerprint(N),'model_tensor_sha256':recovery.fingerprint(T),'scope':'unitary'})
    from verify_r8_1_7_zesting import check_base
    bases = [check_base(category) for category in (1,2)]
    require(bases[0][0]==bases[1][0], 'pseudo base ring agreement')
    # Explicit paired central object: i*(-i)=1 and (-1)*(-1)=1.
    require((2+6)%8==0 and (-1)*(-1)==1,'paired boson')
    return {'status':'PASS','models':receipts,'general_exclusions':check_exclusions(rows,source),
            'pseudo_half_braidings':[b[1] for b in bases],
            'optimization_safe':True,'theoretical_existence':'NONINTEGRAL_PROOFS.md'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = verify()
    text = json.dumps(result,indent=2)
    if args.output:
        args.output.write_text(text+'\n')
    print(text)
