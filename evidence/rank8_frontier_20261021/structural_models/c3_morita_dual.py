#!/usr/bin/env python3
"""Exact conditional Morita-dual based rings for the two S3 frontier rings."""
from pathlib import Path
import argparse
import hashlib
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
SHAS={439:'dd40ef78c0af51291aedd91134123f7177c18cc9de9c9d3b039a6308bb340791',
      567:'0efab5b3d7571872f46dd6ccc95c4b228123b252062d758318ee51834288ef4d'}


def require(c,m):
    if not c:
        raise ValueError(m)


def permutation(images):
    return sp.Matrix(8,8,lambda i,j:int(images[j]==i))


def family(R, group_generator, odd, noninvertible, G, H, X):
    mats=[None]*8
    mats[0]=sp.eye(8)
    for exponent in range(3):
        g=0
        for _ in range(exponent):
            g=R[group_generator][g].index(1)
        mats[g]=G**exponent
        hg=R[odd][g].index(1)
        mats[hg]=H*G**exponent
    mats[noninvertible]=X
    other=R[odd][noninvertible].index(1)
    mats[other]=H*X
    require(all(M is not None for M in mats),'basis not generated')
    return mats


def relation_checks(R,mats,opposite=False):
    for i in range(8):
        for j in range(8):
            coeff=R[j][i] if opposite else R[i][j]
            require(mats[i]*mats[j] == sum((coeff[k]*mats[k] for k in range(8)),sp.zeros(8)),
                    f'fusion relation {i},{j}')


def one(row):
    R=row['tensor'];ident=int(row['id'].rsplit('_',1)[1])
    sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    require(sha==SHAS[ident]==row['tensor_sha256'],'source hash')
    g=1;h=3 if ident==439 else 5;x=4 if ident==439 else 3
    y=R[h][x].index(1)
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    require(dual[x] == (x if ident==439 else y),'noninvertible duality')
    # Right-A module basis: f0,f1,X0,X1,X2,Y0,Y1,Y2.
    G=permutation([0,1]+[2+(i+1)%3 for i in range(3)]+[5+(i-1)%3 for i in range(3)])
    H=permutation([1,0,5,6,7,2,3,4])
    T=permutation([0,1]+[2+(i+1)%3 for i in range(3)]+[5+(i+1)%3 for i in range(3)])
    U=permutation([1,0]+[5+(-i)%3 for i in range(3)]+[2+(-i)%3 for i in range(3)])
    X=sp.zeros(8)
    for i in range(3):
        X[2+i,0]=X[5+i,1]=1
        X[0 if ident==439 else 1,2+i]=1
        X[1 if ident==439 else 0,5+i]=1
    for i in range(2,8):
        for j in range(2,8):
            X[i,j]=1
    left=family(R,g,h,x,G,H,X)
    relation_checks(R,left)
    for i in range(8):
        require(left[dual[i]]==left[i].T,'module rigidity')
    require(all(T*M==M*T and U*M==M*U for M in left),'right group actions commute left fusion')
    require(T**3==sp.eye(8) and U**2==sp.eye(8) and U*T*U==T**2,'right S3')
    require(T*X==X==X*T,'dual noninvertible fixed by right C3')
    require(U*X==H*X,'dual odd translate')
    # The unknown action B of the dual noninvertible commutes with the left ring,
    # is fixed on both sides by T, and has B f0 = sum_i Xi.
    # Encode the homogeneous difference B-X as an integer 328-by-64 system.
    units=[]
    for i in range(8):
        for j in range(8):
            E=sp.zeros(8);E[i,j]=1;units.append(E)
    def constraints(E):
        values=[]
        for M in (G,H,X):
            values.extend(E*M-M*E)
        values.extend(T*E-E)
        values.extend(E*T-E)
        values.extend(E[:,0])
        return sp.Matrix(values)
    coefficients=sp.Matrix.hstack(*(constraints(E)for E in units))
    rank=coefficients.rank()
    require(rank==64,'nonunique dual noninvertible action')
    require(X[:,0]==sp.Matrix([0,0,1,1,1,0,0,0]),'dual X forgetful column')
    # Right tensor actions represent the opposite dual ring. Assigning the
    # inverse deck generator gives its source-labelled opposite representation.
    right=family(R,g,h,x,T**2,U,X)
    # family() orders H G^a; for a right action use G^a H instead.
    for exponent in range(3):
        sourceg=0
        for _ in range(exponent):sourceg=R[g][sourceg].index(1)
        right[R[h][sourceg].index(1)]=(T**2)**exponent*U
    relation_checks(R,right,opposite=True)
    require(all(A*B==B*A for A in left for B in right),'all left/right commutators')
    require(sp.Matrix.hstack(*(sp.Matrix(M).reshape(64,1)for M in right)).rank()==8,
            'dual actions not independent')
    for i in range(8):
        require(right[dual[i]]==right[i].T,'dual action rigidity')
    return {'id':row['id'],'tensor_sha256':sha,
            'outcome':'conditional_Morita_dual_has_same_based_ring',
            'categorification_claimed':False,'general_exclusion_claimed':False,
            'algebra_source_basis':[0,1,2],
            'right_module_basis':['f0','f1','X0','X1','X2','Y0','Y1','Y2'],
            'source_generators':{'g':g,'h':h,'X':x,'Y':y},
            'left_module_matrices':[[list(M.row(i))for i in range(8)]for M in left],
            'right_dual_opposite_matrices':[[list(M.row(i))for i in range(8)]for M in right],
            'dual_noninvertible_uniqueness_constraint_rank':rank,
            'dual_noninvertible_uniqueness_variables':64,
            'dual_simple_count':8,'dual_invertible_group':'S3',
            'dual_noninvertible_dimension_polynomial':[1,-6,-3],
            'dual_noninvertible_source_underlying_objects':{'X':f'3*{x}','Y':f'3*{y}'},
            'fusion_coefficients_checked':512,
            'scope':'For any complex categorification, its subgroup-algebra Morita dual has the same based ring; no associator equivalence is asserted.'}


def record():
    rows=json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
    source={r['id']:r for r in rows}
    split=json.loads((HERE.parent/'quadratic/cubic_split_module_results.json').read_text())
    for ident in SHAS:
        r=next(r for r in split['records']if r['id']==f'R8_3_{ident}')
        require(r['tensor_sha256']==SHAS[ident] and len(r['exact_solutions'])==2,'complete Fourier input')
        require(r['finite_cases_after_proved_phase_gauge']==30000,'Fourier domain')
        require({s['phase']for s in r['exact_solutions']}=={1,2},'Fourier primitive phases')
        g=1;h=3 if ident==439 else 5;x=4 if ident==439 else 3;y=5 if ident==439 else 4
        require(r['group_generator']==g and r['odd_involution']==h
                and r['noninvertible_generator']==x,'Fourier source generators')
        zero=[[[0,0],[0,0]],[[0,0],[0,0]]]
        swap=[[[0,0],[1,0]],[[1,0],[0,0]]]
        for solution in r['exact_solutions']:
            a,b=([0,1],[-1,-1]) if solution['phase']==1 else ([-1,-1],[0,1])
            require(solution['matrices'][g]==[[a,[0,0]],[[0,0],b]],'Fourier g action')
            require(solution['matrices'][h]==swap,'Fourier h action')
            require(solution['matrices'][x]==zero==solution['matrices'][y],
                    'Fourier noninvertibles must vanish')
    return {'kind':'exact_C3_subgroup_Morita_dual_based_ring_closure',
            'proof':'C3_MORITA_DUAL.md',
            'records':[one(source[f'R8_3_{i}'])for i in SHAS]}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=record();path=HERE/'c3_morita_dual.json'
    # Matrix entries are SymPy integers; canonical JSON is integral.
    actual=json.loads(json.dumps(actual,default=int))
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:require(actual==json.loads(path.read_text()),'Morita receipt differs')
    print('PASS:439/567 exact C3 Morita-dual based-ring closure; no model or general exclusion.')


if __name__=='__main__':main()
