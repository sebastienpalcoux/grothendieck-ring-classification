#!/usr/bin/env python3
"""Fresh bounded model-search audit for all 277 baseline survivors.

This reconstructs 72 explicit based tensors and records exact model-family
filters. It never turns a bounded negative search into a general exclusion.
Default compares the saved audit; --write regenerates it after recovery.
"""
from collections import Counter
from fractions import Fraction
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import sys
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'supplements/rank8/software'))
sys.path.insert(0,str(HERE))
from prepare import key
from model_constructors import all_models,product,frobenius13,require

def fp(v):
    return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()
def maximum(R):
    return max(v for A in R for row in A for v in row)
def dual(R):
    return [next(j for j in range(8) if R[i][j][0]) for i in range(8)]
def axioms(R):
    require(len(R)==8,'constructed tensor has wrong rank')
    require(all(isinstance(v,int) and v>=0 for A in R for row in A for v in row),'negative/nonintegral coefficient')
    require(all(R[0][i]==R[i][0]==[int(i==j) for j in range(8)] for i in range(8)),'wrong unit')
    du=dual(R)
    require(all(R[i][j][0]==int(j==du[i]) for i,j in itertools.product(range(8),repeat=2)),'wrong duality')
    require(all(R[i][j][k]==R[du[j]][du[i]][du[k]]==R[du[i]][k][j]
                for i,j,k in itertools.product(range(8),repeat=3)),'wrong reciprocity')
    require(all(sum(R[i][j][a]*R[a][k][b] for a in range(8))==
                sum(R[j][k][a]*R[i][a][b] for a in range(8))
                for i,j,k,b in itertools.product(range(8),repeat=4)),'nonassociative candidate tensor')
def su2(level,even=False):
    labels=list(range(0,level+1,2 if even else 1))
    require(len(labels)==8,'wrong SU2 sector rank')
    return [[[int(abs(i-j)<=k<=min(i+j,2*level-i-j) and (i+j+k)%2==0)
              for k in labels] for j in labels] for i in labels]
def frobenius16():
    def action(v): return ((v<<1)&15)^(15 if v&8 else 0)
    orbits=[];remaining=set(range(1,16))
    while remaining:
        v=min(remaining);O=[];w=v
        for _ in range(5): O.append(w);w=action(w)
        require(w==v and len(set(O))==5,'bad F16 orbit')
        orbits.append(sorted(O));remaining-=set(O)
    R=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i,j in itertools.product(range(5),repeat=2): R[i][j][(i+j)%5]=1
    for a,i in itertools.product(range(5),range(3)): R[a][5+i][5+i]=R[5+i][a][5+i]=1
    for i,j in itertools.product(range(3),repeat=2):
        for a in range(5): R[5+i][5+j][a]=int(i==j)
        for k in range(3): R[5+i][5+j][5+k]=sum(a^b==orbits[k][0] for a in orbits[i] for b in orbits[j])
    return R
def tensors():
    lower=[r for r in json.loads((ROOT/'supplements/rank8/data/lower_rank_positive_models.json').read_text()) if len(r['tensor'])==4]
    require(len(lower)==15,'rank-four catalog changed')
    C2=[[[1,0],[0,1]],[[0,1],[1,0]]]
    Fib=[[[1,0],[0,1]],[[0,1],[1,1]]]
    for row in lower:
        for name,B in [('Vec(C2)',C2),('Fibonacci',Fib)]:
            yield row['name']+' x '+name,product(row['tensor'],B),'Deligne product of catalog models',{'catalog_reference':row.get('reference')}
    for row in lower:
        A=row['tensor']
        for tail in itertools.permutations(range(1,4)):
            p=(0,)+tail
            if not all(p[p[i]]==i for i in range(4)): continue
            if not all(A[i][j][k]==A[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(4),repeat=3)): continue
            R=[[[0]*8 for _ in range(8)] for _ in range(8)]
            for i,e,j,f,k in itertools.product(range(4),range(2),range(4),range(2),range(4)):
                R[2*i+e][2*j+f][2*k+(e+f)%2]=A[i][p[j] if e else j][k]
            yield row['name']+' abstract C2 crossed tensor '+str(list(p)),R,'based-ring construction only; categorical action and coherence not asserted',{'automorphism':list(p)}
    for level,even in [(7,False),(14,True),(15,True)]:
        yield ('PSU' if even else 'SU')+'(2)_'+str(level),su2(level,even),'standard quantum-group fusion tensor',{}
    yield 'Rep(C13 semidirect C6)',frobenius13(),'finite-group representation category',{}
    yield 'Rep((C2)^4 semidirect C5)',frobenius16(),'finite-group representation category',{}
    sys.path.insert(0,str(HERE/'psl2_11'))
    from verify_psl2_11 import reconstructed_model
    q=reconstructed_model()
    yield q['model'],q['tensor'],'finite-group class-algebra certified model',{}
    for ident,name,R,ref,extra in all_models():
        if ident not in [331,471,1456,3314,342]:
            yield name,R,'independently certified categorical construction',{'reference':ref,'accepted_id':'R8_3_'+str(ident)}
    sys.path.insert(0,str(HERE/'psl2_11/r360'))
    from verify_a6_twist import model_tensor
    R,_=model_tensor()
    yield 'Twisted C(A6,omega,A5,psi)',R,'independently certified categorical construction',{'proof':'psl2_11/r360/proof.md','accepted_id':'R8_3_3342'}

def integrality(R,profile):
    approximate=profile['fp_dimensions_approx']
    integer=[round(x) for x in approximate]
    if all(x>0 for x in integer) and all(sum(R[i][j][k]*integer[k] for k in range(8))==integer[i]*integer[j]
                                        for i,j in itertools.product(range(8),repeat=2)):
        require(integer[0]==1,'dimension character not normalized')
        return {'integral':True,'dimensions':integer,'global_dimension':sum(x*x for x in integer),
                'verification':'all64 positive dimension-character identities'}
    vector=[max(1,round(x*10**6)) for x in approximate]
    for iteration in range(25):
        for i in range(8):
            ratios=[Fraction(sum(R[i][j][k]*vector[k] for k in range(8)),vector[j]) for j in range(8)]
            lo,hi=min(ratios),max(ratios)
            m=lo.numerator//lo.denominator
            if m<lo<=hi<m+1:
                return {'integral':False,'basis_index':i,'positive_integer_test_vector':vector,
                        'lower_bound':[lo.numerator,lo.denominator],'upper_bound':[hi.numerator,hi.denominator],
                        'consecutive_integers':[m,m+1],'verification':'exact rational Collatz-Wielandt strict noninteger interval'}
        vector=[sum(R[i][j][k]*vector[k] for i in range(8) for k in range(8)) for j in range(8)]
    raise ValueError('no exact nonintegrality witness found')
def center_filter(R):
    du=dual(R)
    inv=[i for i in range(8) if all(sum(row)==1 for row in R[i])]
    central=[i for i in inv if all(R[i][j]==R[j][i] for j in range(8))]
    basis={0}|{k for i in range(8) for k in range(8) if R[i][du[i]][k]}
    while True:
        expanded=basis|{k for i in basis for j in basis for k in range(8) if R[i][j][k]}
        if expanded==basis: break
        basis=expanded
    applies=len(basis)==8 and central==[0]
    return {'invertible_indices':inv,'central_invertible_indices':central,'adjoint_basis':sorted(basis),
            'center_has_no_nontrivial_invertible_if_categorified':applies,
            'scope':'if applicable, excludes Morita equivalence to a nontrivial cyclic-prime extension or equivariantization; not arbitrary categorification'}

def audit():
    rows=json.loads((HERE.parent/'pipeline/survivors_baseline.json').read_text())
    profiles={r['id']:r for r in json.loads((HERE.parent/'pipeline/survivor_profiles.json').read_text())}
    require(len(rows)==len(profiles)==277,'baseline scope changed')
    for row in rows: require(fp(row['tensor'])==row['tensor_sha256']==profiles[row['id']]['tensor_sha256'],'source binding failed')
    keys={row['id']:key(row['tensor'],True) for row in rows}
    tests=[];by_source={r['id']:[] for r in rows}
    for number,(name,R,scope,details) in enumerate(tensors(),1):
        axioms(R);matches=[];m=maximum(R)
        if m==3:
            modelkey,pm=key(R,True)
            for row in rows:
                sourcekey,ps=keys[row['id']]
                if sourcekey!=modelkey: continue
                p=[None]*8
                for i,j in zip(ps,pm): p[i]=j
                require(all(row['tensor'][i][j][k]==R[p[i]][p[j]][p[k]] for i,j,k in itertools.product(range(8),repeat=3)),'full tensor matching failed')
                matches.append({'id':row['id'],'source_to_model_basis_map':p,'verified_coefficients':512})
                by_source[row['id']].append(number)
        tests.append({'test_number':number,'name':name,'scope':scope,'details':details,'tensor':R,
                      'tensor_sha256':fp(R),'maximum_multiplicity':m,'matches':matches,
                      'negative_test_method':'full based-tensor canonical comparison' if m==3 else 'exact maximum-multiplicity invariant differs from3'})
    require(len(tests)==72,'bounded tensor test count changed')
    quantum=json.loads((HERE/'quantum_model_attempts.json').read_text())
    leads={r['id']:r for r in quantum['all_baseline_numerical_scan']['per_ring']}
    require(set(leads)==set(profiles),'quantum search scope differs')
    x=sp.Symbol('x');f4=sp.Poly(x*x-480*x+2304,x)
    records=[];quartic=[]
    for row in rows:
        R=row['tensor'];name=row['id'];profile=profiles[name]
        integral=integrality(R,profile)
        comm=all(R[i][j]==R[j][i] for i,j in itertools.product(range(8),repeat=2))
        attempts=[{'family':'72 explicitly constructed rank-eight tensors','matching_test_numbers':by_source[name],
                   'scope':'negative means no match in this finite list; crossed products are only abstract ring tests unless separately certified'},
                  {'family':'ordinary finite-group representation categories','rejected_by_elementary_filter':not comm or not integral['integral'],
                   'reason':'noncommutative ring' if not comm else 'verified nonintegral simple dimension' if not integral['integral'] else 'not settled by integrality/commutativity alone'},
                  {'family':'pointed and ordinary Tambara-Yamagami categories','rejected':True,'reason':'their fusion multiplicities are at most1, but this source has maximum3'},
                  {'family':'Morita sources obtained by cyclic-prime extension/equivariantization','certificate':center_filter(R)},
                  {'family':'bounded classical WZW dimension-ratio search','tested_models':quantum['all_baseline_numerical_scan']['tested_classical_models'],
                   'leads':leads[name]['matches'],'scope':'heuristic numerical leads only; no tensor identification or general exclusion'}]
        if len(profile.get('global_dimension_polynomial',[]))==5:
            du=dual(R);matrices=[sp.Matrix(A) for A in R]
            casimir=sum((matrices[i]*matrices[du[i]] for i in range(8)),sp.zeros(8))
            cp=casimir.charpoly(x).as_poly();remainder=cp.rem(f4)
            receipt={'id':name,'source_casimir_characteristic_polynomial':[int(c) for c in cp.all_coeffs()],
                     'F4_level3_global_dimension_minimal_polynomial':[1,-480,2304],
                     'remainder':[int(c) for c in remainder.all_coeffs()],
                     'specific_Morita_source_excluded':not remainder.is_zero}
            quartic.append(receipt)
            attempts.append({'family':'unitary F4 level3 as a Morita source','exact_certificate':receipt,
                             'scope':'only this one candidate source; FP dimension is Morita invariant'})
        if name in ['R8_3_65','R8_3_1453']:
            attempts.append({'family':'unitary PSU(3)_7 Morita duals','receipt':quantum['su3_7'],
                             'scope':'unitary model-family restriction only; detailed proof in QUANTUM_MODEL_SEARCH.md'})
        if name=='R8_3_3344':
            indices=[i for i,d in enumerate(integral['dimensions']) if d==10]
            require(len(indices)==3 and all(R[i][i][i]==3 for i in indices),'A6 comparison changed')
            attempts.append({'family':'the stable-relative-mu2 A6/A5 construction','source_dimension10_square_diagonal_coefficients':[3,3,3],
                             'constructed_model_has_determinant_trivial_spin_anchor':2,
                             'scope':'excludes this construction only; proof psl2_11/r360/proof.md'})
        records.append({'id':name,'tensor_sha256':row['tensor_sha256'],'integrality_certificate':integral,
                        'commutative':comm,'attempts':attempts})
    return {'scope':'Bounded model investigation only; no arbitrary categorification exclusion is inferred from negative searches.',
            'recovery':'fresh computations from restored inputs; unavailable historical targeted receipts are not asserted',
            'baseline_survivor_count':277,'explicit_tensor_test_count':72,'explicit_tensor_tests':tests,
            'quantum_scan_receipt_sha256':fp(quantum),'exact_F4_quartic_checks':quartic,'per_ring_attempts':records}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=audit();path=HERE/'model_search_attempts.json'
    if args.write: path.write_text(json.dumps(result,indent=2)+'\n')
    else: require(json.loads(path.read_text())==json.loads(json.dumps(result)),'saved audit differs from fresh replay')
    counts=Counter(r['integrality_certificate']['integral'] for r in result['per_ring_attempts'])
    print(json.dumps({'explicit_tensor_tests':72,'per_ring_attempt_records':277,'integral':counts[True],
                      'exact_nonintegrality_witnesses':counts[False],'F4_quartic_checks':len(result['exact_F4_quartic_checks']),
                      'mode':'write' if args.write else 'compare'}))
