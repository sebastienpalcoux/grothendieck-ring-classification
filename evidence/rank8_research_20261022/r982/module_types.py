#!/usr/bin/env python3
"""Complete semionic R982 module-Gram/NIM-representation refinement.

No floating-point optimization, rank cutoff, or associator claim is used.
Read-only replay is the default; --write regenerates the exact receipt.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ALG=ROOT/'evidence/rank8_frontier_20261021/structural_models/algebra_candidates.json'
SOURCE=ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json'
TENSOR_SHA='f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c'
ALG_SHA='eecc23bde04d34be4038841c7d5d180d2ca4c3433770fcf8aa3d25fea62a9dde'
SEMION=ROOT/'evidence/rank8_next_20261021/r982/FINAL_SUMMARY.json'
SEMION_SHA='4b8f870ebb9e36931a0c270dbd4dd4661844a951a7648e8552cba7cc3bf8a5b5'
GATE=HERE.parent/'pivotality/general_spherical_gates.json'
GATE_SHA='89ad25baeb05b69c95519670eb4cdd894a29d3b7f4d920535b1f404f46ba13d4'
GP=[6,2,1,4,3,7,0,5]
INDS=[1,2,3,4,5,7]
# Integral isometries from the four determinant-four plus lattices to
# diag(1,2,2). Their identities, not their method of discovery, are checked.
ISOMETRIES={
 2:[[-1,0,1],[-1,1,0],[0,0,-1]],
 5:[[-1,0,1],[-2,0,3],[-1,1,0]],
 9:[[-1,0,1],[-2,2,-1],[-1,1,0]],
 23:[[-1,0,1],[-1,1,0],[0,-2,3]],
}

def need(c,m):
    if not c:raise ValueError(m)

def integers(M):return [[int(x)for x in row]for row in M.tolist()]

def gram(R,a):
    return s.Matrix([[sum(a[k]*R[j][k][i]for k in range(8))
                      for j in range(8)]for i in range(8)])

def vectors(norm,signed=False):
    b=math.isqrt(norm)
    return [v for v in itertools.product(range(-b if signed else 0,b+1),repeat=3)
            if sum(x*x for x in v)==norm]

def three_column_factors(H,signed=False):
    """All integral 3-by-3 Gram factors; positive columns modulo permutation."""
    V=[vectors(H[i][i],signed)for i in range(3)]
    out=set()
    for a in V[0]:
        # Positive column permutations are exhausted by sorting the first row.
        if not signed and a!=tuple(sorted(a)):continue
        for b in V[1]:
            if sum(x*y for x,y in zip(a,b))!=H[0][1]:continue
            for c in V[2]:
                if sum(x*y for x,y in zip(a,c))!=H[0][2]:continue
                if sum(x*y for x,y in zip(b,c))!=H[1][2]:continue
                cols=tuple(zip(a,b,c))
                out.add(cols if signed else tuple(sorted(cols)))
    return sorted(out)

def lattice_factors(P,T):
    """Complete nonnegative embeddings of diag(1,2,2), up to columns."""
    T=s.Matrix(T)
    need(abs(T.det())==1 and T*P*T.T==s.diag(1,2,2),'integral lattice isometry')
    L3=s.Matrix([[1,0,0],[0,1,1],[0,1,-1]])
    L5=s.Matrix([[1,0,0,0,0],[0,1,1,0,0],[0,0,0,1,1]])
    result=[]
    for L in [L3,L5]:
        U=T.inv()*L;cols=[]
        for j in range(U.cols):
            v=tuple(int(x)for x in U[:,j])
            if all(x<=0 for x in v):v=tuple(-x for x in v)
            need(all(x>=0 for x in v) and any(v),'nonnegative lattice representative')
            cols.append(v)
        cols=tuple(sorted(cols));C=s.Matrix(cols).T
        need(C*C.T==P,'lattice factor Gram')
        result.append(cols)
    return result

def paired_columns(a,Us,Ds):
    result=set()
    for us in Us:
        for ds in Ds:
            if not all((u+d)%2==0 and abs(d)<=u
                       for uc,dc in zip(us,ds)for u,d in zip(uc,dc)):continue
            pairs=[]
            for uc,dc in zip(us,ds):
                v1=[(u+d)//2 for u,d in zip(uc,dc)]
                v2=[(u-d)//2 for u,d in zip(uc,dc)]
                v=(0,v1[0],v2[0],v1[1],v2[1],v1[2],0,v2[2])
                w=tuple(v[GP[i]]for i in range(8))
                pairs.append(tuple(sorted((v,w))))
            result.add((tuple(a),tuple(a[GP[i]]for i in range(8)))+
                       sum(tuple(sorted(pairs)),()))
    return sorted(result)

def module_actions(R,cols):
    B=s.Matrix(cols).T
    need(B.shape==(8,8) and B.det()!=0,'full-rank induction matrix')
    actions=[B.inv()*s.Matrix(R[i])*B for i in range(8)]
    bad=[{'source_index':i,'row':j,'column':k,'entry':str(M[j,k])}
         for i,M in enumerate(actions)for j,k in itertools.product(range(8),repeat=2)
         if not (M[j,k].is_integer and M[j,k]>=0)]
    if bad:return actions,bad
    dual=[next(j for j in range(8)if R[i][j][0])for i in range(8)]
    need(actions[0]==s.eye(8),'unit action')
    for i,j in itertools.product(range(8),repeat=2):
        need(actions[i]*actions[j]==sum((R[i][j][k]*actions[k]for k in range(8)),s.zeros(8)),
             'full source multiplication')
    need(all(actions[dual[i]]==actions[i].T for i in range(8)),'module duality')
    need(actions[6]**2==s.eye(8) and actions[6].trace()==0,'free involution on modules')
    # Every vertex is reached from the distinguished simple by some source simple.
    need(all(any(actions[i][0,j]>0 for i in range(8))for j in range(8)), 'connected module')
    return actions,[]

def ends(actions):
    return [tuple(int(M[j,j])for M in actions)for j in range(8)]

def module_equivalence(A,B):
    ea,eb=ends(A),ends(B)
    domains=[[j for j in range(8)if ea[i]==eb[j]]for i in range(8)]
    for p in itertools.product(*domains):
        if len(set(p))!=8:continue
        if all(A[k][i,j]==B[k][p[i],p[j]]
               for k,i,j in itertools.product(range(8),repeat=3)):return list(p)
    return None

def run():
    need(hashlib.sha256(ALG.read_bytes()).hexdigest()==ALG_SHA,'complete prior algebra-domain binding')
    need(hashlib.sha256(SEMION.read_bytes()).hexdigest()==SEMION_SHA,'frozen semion/indicator audit binding')
    semion=json.loads(SEMION.read_text())
    need(semion['tensor_sha256']==TENSOR_SHA and semion['remaining_indicators'][5]==-1,
         'forced source g second indicator')
    need(hashlib.sha256(GATE.read_bytes()).hexdigest()==GATE_SHA,'general sphericalization gate binding')
    gate=next(r for r in json.loads(GATE.read_text())if r['id']=='R8_3_982')
    need(gate['tensor_sha256']==TENSOR_SHA and gate['normalized_signed_count']==3 and
         gate['conclusion']=='every categorification is spherical and has a pseudo-unitary Galois conjugate; no existence or general unbraided exclusion asserted',
         'general-to-spherical-to-Galois-pseudo-unitary conclusion')
    row=next(r for r in json.loads(SOURCE.read_text())if r['id']=='R8_3_982')
    R=row['tensor'];sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(sha==row['tensor_sha256']==TENSOR_SHA,'canonical tensor binding')
    need(all(R[6][i][GP[i]]==1 and sum(R[6][i])==1 for i in range(8)),'source g permutation')
    candidates=next(r for r in json.loads(ALG.read_text())['records']if r['id']==row['id'])['necessary_survivor_vectors']
    need(len(candidates)==31,'complete algebra candidate input')
    records=[];representatives=[];class_receipts=[]
    for ix,a in enumerate(candidates):
        if a[6]:continue
        ga=[a[GP[i]]for i in range(8)]
        H=gram(R,a)-s.Matrix(a)*s.Matrix([a])-s.Matrix(ga)*s.Matrix([ga])
        need(all(H[i,j]==0 for i in [0,6]for j in range(8)),'distinguished-pair removal')
        need(all(H[i,j]==H[GP[i],GP[j]]for i,j in itertools.product(range(8),repeat=2)), 'g equivariance')
        G=H.extract(INDS,INDS)
        P=s.Matrix(3,3,lambda i,j:G[2*i,2*j]+G[2*i,2*j+1])
        M=s.Matrix(3,3,lambda i,j:G[2*i,2*j]-G[2*i,2*j+1])
        det=int(P.det());need(det in [1,4],'complete lattice determinant alternatives')
        large=None
        if det==1:
            # Cauchy--Binet: determinant one permits exactly three nonzero columns.
            Us=three_column_factors(integers(P))
        else:
            U3,U5=lattice_factors(P,ISOMETRIES[ix]);Us=[U3]
            parity=[sum(v[i]%2 for v in U5)for i in range(3)]
            need(any(parity[i]>M[i,i]for i in range(3)), 'rank-twelve parity exclusion')
            large={'plus_columns':U5,'odd_coordinate_counts':parity,
                   'minus_squared_norms':[int(M[i,i])for i in range(3)]}
            need(Us==three_column_factors(integers(P)), 'independent complete rank-eight plus factors')
        Ds=three_column_factors(integers(M),True)
        factorizations=[]
        for cols in paired_columns(a,Us,Ds):
            B=s.Matrix(cols).T;need(B*B.T==gram(R,a),'full exact induction Gram')
            actions,bad=module_actions(R,cols)
            item={'induction_columns':cols,'nimrep':not bad}
            if bad:item['first_obstruction']=bad[0]
            else:
                match=None
                for c,rep in enumerate(representatives):
                    perm=module_equivalence(actions,rep)
                    if perm is not None:match=(c,perm);break
                if match is None:
                    representatives.append(actions);match=(len(representatives)-1,list(range(8)))
                    class_receipts.append({'class':match[0],'first_algebra_index':ix,
                        'actions':[integers(N)for N in actions],
                        'internal_end_vectors':sorted(set(ends(actions)))})
                item.update({'module_class':match[0],'permutation_to_class_representative':match[1]})
            factorizations.append(item)
        records.append({'algebra_index':ix,'algebra':a,'plus_gram':integers(P),
            'minus_gram':integers(M),'plus_determinant':det,
            'determinant_four_isometry':ISOMETRIES.get(ix),
            'rank_twelve_parity_obstruction':large,'positive_three_column_factors':Us,
            'signed_three_column_factor_count':len(Ds),'factorizations':factorizations})
    survivors=[r['algebra_index']for r in records if any(z['nimrep']for z in r['factorizations'])]
    need(survivors==[0,2,5,9,12,16,19,23],'eight complete surviving objects')
    need(len(representatives)==3,'three complete based-module types')
    need(module_equivalence([s.Matrix(R[i])for i in range(8)],representatives[0]) is not None,'regular module control')
    need(all(class_receipts[c]['internal_end_vectors']==[tuple(candidates[i])for i in [2,5,9,23]]
             for c in [1,2]), 'same four internal ends for the two new types')
    dual_perm=module_equivalence([M.T for M in representatives[1]],representatives[2])
    need(dual_perm is not None,'two nonregular types exchanged by source duality')
    return {'kind':'complete_R982_semionic_module_Gram_refinement',
        'tensor_sha256':sha,'prior_complete_algebra_domain_sha256':ALG_SHA,
        'semion_indicator_audit_sha256':SEMION_SHA,'general_spherical_gate_sha256':GATE_SHA,
        'categorical_input':'source pointed associator nontrivial; every module g-action is free',
        'scope':'all complex categorifications after the independently proved Galois-to-pseudo-unitary gate',
        'initial_algebra_objects':31,'semionic_stabilizer_exclusions':20,
        'paired_Gram_or_action_exclusions':[10,14,21],
        'surviving_algebra_indices':survivors,'all_indecomposable_module_ranks':[8],
        'based_module_types':class_receipts,'nonregular_duality_permutation':dual_perm,'records':records,
        'limitation':'NIM-representations are necessary decategorified modules, not module associators or fusion-category constructions.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    actual=json.loads(json.dumps(run()));path=HERE/'module_types.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'saved complete module receipt changed')
    print('PASS: 31 -> 11 -> 8 algebra objects; every module rank is 8; exactly three necessary based-module types; no associator claimed.')
