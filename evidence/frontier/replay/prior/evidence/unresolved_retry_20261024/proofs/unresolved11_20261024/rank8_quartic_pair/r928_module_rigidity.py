#!/usr/bin/env python3
"""Complete, rank-unbounded module classification conditional on R928 existence.

The source's forced semion associator means every module g-action is free.
The preceding exhaustive internal-end filter leaves four candidates. Their
paired plus Gram has determinant one: Cauchy--Binet forces three residual
column pairs. This script checks every factor in the resulting exact domain.
It never treats a based module as an actual category.
"""
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
import sympy as s

HERE=Path(__file__).resolve().parent
PROFILE=HERE/'r928_dependencies.json'
BORROW=HERE/'r928_module_helpers.py'
spec=importlib.util.spec_from_file_location('paired_module_helpers',BORROW)
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def need(x,m):
    if not x: raise ValueError(m)
def mat(M):return [[int(x) for x in row] for row in M.tolist()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def psd_exact(H):
    """Rational Schur elimination, including singular zero-pivot rows."""
    H=[[Fraction(x) for x in row] for row in H.tolist()]
    while H:
        if any(H[i][i]<0 for i in range(len(H))):return False
        for i in range(len(H)):
            if H[i][i]==0 and any(H[i]):return False
        p=next((i for i in range(len(H)) if H[i][i]>0),None)
        if p is None:return True
        ix=[i for i in range(len(H)) if i!=p]
        H=[[H[i][j]-H[i][p]*H[p][j]/H[p][p] for j in ix] for i in ix]
    return True

def independent_algebra_filter(R):
    """All960 semionic self-dual coefficient vectors, no inherited cutoff."""
    a=2+s.sqrt(2)+s.sqrt(3)+s.sqrt(6)
    b=2+2*s.sqrt(2)+s.sqrt(3)+s.sqrt(6)
    c=3+2*s.sqrt(2)+2*s.sqrt(3)+s.sqrt(6)
    dims=[s.Integer(1),a,a,b,b,c,c,s.Integer(1)]
    need(all(s.expand(dims[i]*dims[j]-sum(R[i][j][k]*dims[k] for k in range(8)))==0 for i,j in itertools.product(range(8),repeat=2)), 'positive exact FP dimension character')
    bounds={2:(Fraction(1414,1000),Fraction(1415,1000)),3:(Fraction(1732,1000),Fraction(1733,1000)),6:(Fraction(2449,1000),Fraction(2450,1000))}
    need(all(lo>0 and lo*lo<n<hi*hi for n,(lo,hi) in bounds.items()), 'strict rational radical bounds')
    for coeff,floor in [((2,1,1,1),7),((2,2,1,1),9),((3,2,2,1),11)]:
        lo=coeff[0]+sum(coeff[i]*bounds[n][0] for i,n in enumerate((2,3,6),1))
        hi=coeff[0]+sum(coeff[i]*bounds[n][1] for i,n in enumerate((2,3,6),1))
        need(floor<lo<=hi<floor+1,'proved dimension floor')
    survivors=[];entrywise=0
    for aa,bb,cc in itertools.product(range(8),range(10),range(12)):
        v=[1,aa,aa,bb,bb,cc,cc,0]
        G=helper.gram(R,v)-s.Matrix(v)*s.Matrix([v])
        if any(x<0 for x in G):continue
        entrywise+=1
        if psd_exact(G):survivors.append(v)
    return survivors,{'complete_semionic_domain':960,'entrywise_gram_survivors':entrywise,'exact_psd_survivors':len(survivors),'FP_dimension_floors':[1,7,7,9,9,11,11,1]}

def run():
    profile=json.loads(PROFILE.read_text());R=profile['fusion_tensor']
    th=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    need(th==profile['tensor_sha256'],'tensor binding')
    dual=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
    GP=[7,2,1,4,3,6,5,0];pairs=[(1,2),(3,4),(5,6)]
    need(all(R[7][i][GP[i]]==1 and sum(R[7][i])==1 for i in range(8)), 'g action')
    need(profile['published_algebra_candidate_count']==24,'published receipt provenance')
    regular=[s.Matrix(R[i]) for i in range(8)]
    regular_ends={tuple(R[i][j][j] for i in range(8)) for j in range(8)}
    eligible=[(row['published_index'],row['vector']) for row in profile['eligible_algebras']]
    need([ix for ix,a in eligible]==[0,7,9,14], 'semionic candidate domain')
    independent,filter_receipt=independent_algebra_filter(R)
    need(independent==[a for ix,a in eligible],'independent complete960-vector algebra filter')
    need({tuple(a) for ix,a in eligible}==regular_ends, 'all four candidates are regular internal ends')
    records=[]
    for ix,a in eligible:
        ga=[a[GP[i]] for i in range(8)]
        G=helper.gram(R,a)
        H=G-s.Matrix(a)*s.Matrix([a])-s.Matrix(ga)*s.Matrix([ga])
        need(all(H[i,j]==H[GP[i],GP[j]] for i,j in itertools.product(range(8),repeat=2)), 'g equivariance')
        need(all(H[i,j]==0 for i in (0,7) for j in range(8)), 'distinguished pair removal')
        P=s.Matrix(3,3,lambda i,j:H[pairs[i][0],pairs[j][0]]+H[pairs[i][0],pairs[j][1]])
        M=s.Matrix(3,3,lambda i,j:H[pairs[i][0],pairs[j][0]]-H[pairs[i][0],pairs[j][1]])
        need(P.det()==1,'Cauchy-Binet all-rank exhaustion')
        need(M==s.eye(3),'minus Gram identity')
        Us=helper.three_column_factors(mat(P));Ds=helper.three_column_factors(mat(M),True)
        Bs=set()
        for us,ds in itertools.product(Us,Ds):
            if not all((u+d)%2==0 and abs(d)<=u for uc,dc in zip(us,ds) for u,d in zip(uc,dc)):continue
            cps=[]
            for uc,dc in zip(us,ds):
                v=[0]*8
                for (p,q),u,d in zip(pairs,uc,dc):v[p],v[q]=(u+d)//2,(u-d)//2
                w=tuple(v[GP[i]] for i in range(8))
                cps.append(tuple(sorted((tuple(v),w))))
            cols=(tuple(a),tuple(ga))+sum(tuple(sorted(cps)),())
            Bs.add(cols)
        factors=[]
        for cols in sorted(Bs):
            B=s.Matrix(cols).T
            need(B*B.T==G and B.det()!=0,'induction Gram and invertibility')
            actions=[B.inv()*N*B for N in regular]
            bad=next(((i,j,k,str(N[j,k])) for i,N in enumerate(actions) for j,k in itertools.product(range(8),repeat=2) if not(N[j,k].is_integer and N[j,k]>=0)),None)
            item={'columns':cols,'first_bad_entry':bad}
            if bad is None:
                need(all(actions[dual[i]]==actions[i].T for i in range(8)), 'dual transpose')
                # Row-transition convention reverses multiplication order.
                for i,j in itertools.product(range(8),repeat=2):
                    need(actions[j]*actions[i]==sum((R[i][j][k]*actions[k] for k in range(8)),s.zeros(8)), 'noncommutative module multiplication')
                perm=helper.module_equivalence(actions,regular)
                need(perm is not None,'only regular based module')
                need(any(all(actions[i][j,j]==(i==0) for i in range(8)) for j in range(8)), 'internal end unit')
                item.update(actions=[mat(N) for N in actions],permutation_to_regular=perm)
            factors.append(item)
        need(any(f['first_bad_entry'] is None for f in factors), 'regular control survives')
        records.append({'algebra_index':ix,'algebra':a,'plus_gram':mat(P),'minus_gram':mat(M),'nonnegative_plus_factors':Us,'signed_minus_factor_count':len(Ds),'paired_factors':factors})
    return {'kind':'complete_R928_all_rank_module_rigidity','source_tensor_sha256':th,'input_algebra_receipt_sha256':profile['published_algebra_receipt_sha256'],'published_helper_sha256':profile['published_helper_sha256'],'portable_dependency_sha256':sha(PROFILE),'helper_sha256':sha(BORROW),'independent_complete_algebra_filter':filter_receipt,'source_pointed_associator':'nontrivial, inherited proved semion criterion','all_indecomposable_module_ranks':[8],'all_indecomposable_based_module_types':['regular'],'categorical_conclusion':'Every indecomposable semisimple module category is equivalent to the regular module category: each contains an object with internal end 1. Consequently every categorical Morita partner is tensor equivalent to the original categorification.','records':records,'limitation':'Conditional structural theorem; neither an exclusion nor a category construction.'}

if __name__=='__main__':
    out=run();p=HERE/'r928_module_rigidity.json';p.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: 24 -> 4 internal ends; every module rank8; every based module regular; categorical Morita rigidity.')
