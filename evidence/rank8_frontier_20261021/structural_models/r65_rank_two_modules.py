#!/usr/bin/env python3
"""Complete rank-two based modules for R65, with explicit coherence limits."""
from pathlib import Path
import argparse
import hashlib
import json
import math
import itertools
import sympy as sp

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
SHA='fb2d70fa36311b2092190eb1ecd5e3e82fd4ab7ff646b11aa7c7e518d261a1c4'
RANK4_SOURCE='manuscripts/rank4/papers/companion_sections/14_finite_certification.tex'
RANK4_SHA='0ec47c3c3da2c46bfee20b06214b9f7704edea841955cb2c86b7b0522f199e8b'


def require(c,m):
    if not c:raise ValueError(m)


def record():
    row=next(r for r in json.loads((REPO/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())
             if r['id']=='R8_3_65')
    R=row['tensor'];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    require(sha==SHA==row['tensor_sha256'],'source hash')
    inv=[0,1,2,7];rho=5;g=1
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    require(dual[rho]==rho,'rho self-dual')
    require([R[rho][rho][i]for i in range(8)]==[1,0,0,3,3,3,2,0],'rho square')
    d=(11+5*sp.sqrt(5))/2
    dims=[sp.Integer(1)if i in inv else d for i in range(8)]
    for i in range(8):
        for j in range(8):
            require(sp.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k]for k in range(8)))==0,
                    'exact positive FP dimension equations')
    D=sp.expand(sum(v*v for v in dims))
    require(D==250+110*sp.sqrt(5),'global dimension')
    subrings=[]
    for mask in range(128):
        J=[0]+[i for i in range(1,8)if mask&(1<<(i-1))]
        if any(dual[i]not in J for i in J):continue
        if any(R[i][j][k]for i in J for j in J for k in range(8)if k not in J):continue
        subrings.append(J)
    require(subrings==[[0],[0,7],[0,1,2,7],list(range(8))], 'complete fusion subrings')
    # A proper Rep(G) must be pointed; its character group embeds into C4.
    # Every nontrivial such Rep(G) contains a central Rep(C2). Its character
    # acts freely, so all C2 base orbits are fixed and each has two lifts.
    perm=[next(k for k in range(8)if R[7][i][k])for i in range(8)]
    require(all(R[7][i]==[int(k==perm[i])for k in range(8)]and
                perm[perm[i]]==i and perm[i]!=i for i in range(8)), 'free central C2 character')
    orbits=sorted({tuple(sorted([i,perm[i]]))for i in range(8)})
    require(len(orbits)==4,'rank-four quotient')
    Q=[[[sum(R[a[0]][b[0]][k]for k in c)for c in orbits]for b in orbits]for a in orbits]
    require(all(sum(R[i][j][k]for k in c)==Q[a][b][h]
                for a,A in enumerate(orbits)for b,B in enumerate(orbits)
                for h,c in enumerate(orbits)for i in A for j in B), 'quotient representative independence')
    qdims=[dims[o[0]]for o in orbits]
    require(all(Q[0][i][j]==int(i==j)and Q[i][0][j]==int(i==j)
                for i,j in itertools.product(range(4),repeat=2)), 'quotient unit')
    require(all(sum(Q[i][j][a]*Q[a][k][h]for a in range(4))==
                sum(Q[j][k][a]*Q[i][a][h]for a in range(4))
                for i,j,k,h in itertools.product(range(4),repeat=4)), 'quotient associativity')
    require(all(sp.expand(qdims[i]*qdims[j]-sum(Q[i][j][k]*qdims[k]for k in range(4)))==0
                for i,j in itertools.product(range(4),repeat=2)), 'quotient positive dimensions')
    baseD=sp.expand(sum(v*v for v in qdims))
    require(baseD==125+55*sp.sqrt(5)and sp.expand(2*baseD-D)==0,'quotient dimension')
    rank4text=(REPO/RANK4_SOURCE).read_bytes()
    require(hashlib.sha256(rank4text).hexdigest()==RANK4_SHA,'pinned rank-four theorem changed')
    require(b'Every rank-four complex fusion category satisfies' in rank4text,'rank-four theorem statement')
    require(baseD>125 and 21**2>12**2*3 and 125>45,'exact dimension-bound comparison')
    # A nontrivial S2 action of g makes its commuting symmetric rho matrix
    # [[a,b],[b,a]], with integral PF eigenvalue a+b, contradicting d.
    a,b,c=sp.symbols('a b c')
    P=sp.Matrix([[0,1],[1,0]]);M=sp.Matrix([[a,b],[b,c]])
    require(M*P-P*M==sp.Matrix([[0,a-c],[c-a,0]]),'swap commutant')
    require(sp.Poly(sp.minpoly(d)).all_coeffs()==[1,-11,-1], 'irrational FP dimension')
    raw=[]
    for aa in range(12):
        cc=11-aa;bb2=aa*cc+1;bb=math.isqrt(bb2)
        if bb*bb!=bb2:continue
        N=sp.Matrix([[aa,bb],[bb,cc]])
        require(N*N==sp.eye(2)+11*N and bb>0,'rank-two module polynomial')
        mats=[sp.eye(2)if i in inv else N for i in range(8)]
        for i in range(8):
            require(mats[dual[i]]==mats[i].T,'module duality')
            for j in range(8):
                require(mats[i]*mats[j]==sum((R[i][j][k]*mats[k]for k in range(8)),sp.zeros(2)),
                        'full module fusion equations')
        raw.append((aa,bb,cc))
    require(raw==[(0,1,11),(3,5,8),(8,5,3),(11,1,0)],'complete rank-two box')
    classes=[]
    for aa,bb,cc in raw:
        if aa>cc:continue
        classes.append({'rho_matrix':[[aa,bb],[bb,cc]],
                        'all_invertible_matrices':[[1,0],[0,1]],
                        'all_four_noninvertible_matrices':[[aa,bb],[bb,cc]],
                        'internal_end_candidates':[[1 if i in inv else v for i in range(8)]for v in (aa,cc)]})
    return {'id':row['id'],'tensor_sha256':sha,
            'scope':'all connected rank-two based modules up to vertex permutation',
            'complete_diagonal_domain':list(range(12)),
            'nontrivial_C4_permutation_action':'excluded_by_integral_Perron_eigenvalue',
            'classes':classes,'class_count':2,
            'global_dimension':str(D),'all_unit_containing_subsets_tested':128,
            'fusion_subrings':subrings,
            'nontrivial_finite_group_equivariantizations':{
                'outcome':'excluded_for_all_nontrivial_finite_groups',
                'only_possible_groups':['C2','C4'],
                'reason':'Every possible central Rep(G) contains central Rep(C2); its free character action forces an impossible rank-four quotient.',
                'order_two_character':7,'orbits':[list(o)for o in orbits],
                'forced_quotient_tensor':Q,'forced_quotient_rank':4,
                'forced_quotient_fp_dimensions':list(map(str,qdims)),
                'forced_quotient_global_dimension':str(baseD),
                'rank_four_dependency':{'path':RANK4_SOURCE,'sha256':RANK4_SHA,
                    'label':'finite:cor:sharp-bounds',
                    'statement':'Every rank-four complex fusion category has FPdim <= 24+12sqrt(3)',
                    'scope':'repository theorem dependency, not independently re-proved by this verifier'}},
            'outcome':'exact_necessary_modules_survive; no_general_exclusion_or_new_model',
            'coherence_restriction':'Every actual rank-two module trivializes the pointed H3(C4,C*) class.',
            'trivial_cocycle_branch':'If that class is trivial, the subgroup algebra sum(C4) exists and realizes the first based module.',
            'canonical_dual_rank_if_pointed_class_trivial':8,
            'canonical_dual_simple_dimensions_if_pointed_class_trivial':['1','1','1','1','d','d','d','d'],
            'canonical_dual_invertible_group_if_pointed_class_trivial':'C4',
            'limitation':'Neither the pointed cocycle vanishing nor a module associator for the second based module is proved; the canonical dual fusion tensor is not identified.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    actual=record();path=HERE/'r65_rank_two_modules.json'
    if a.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:require(actual==json.loads(path.read_text()),'rank-two receipt differs')
    print('PASS:R65 two complete rank-two based modules; all nontrivial finite-group equivariantizations excluded; general categorification remains open.')


if __name__=='__main__':main()
