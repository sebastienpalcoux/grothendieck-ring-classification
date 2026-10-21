#!/usr/bin/env python3
"""Independent partition enumeration and commutant/scope audit for R3472."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def need(c,m):
    if not c:raise ValueError(m)

def product(A,B):
    return [[sum(A[i][k]*B[k][j]for k in range(2))for j in range(2)]for i in range(2)]

def run():
    certificate=HERE/'r3472_rank_two_dual_spectra.json'
    saved=json.loads(certificate.read_text())
    need(saved['covered_module_generator']==[[5,7],[7,7]],'covered branch')
    need(saved['not_covered_module_generator']==[[1,5],[5,11]],'uncovered branch explicit')
    # Independent enumeration by the TWO partitions of 7 into positive squares:
    # seven 1's, or three 1's and one 4. No multiplicity-recursion code is reused.
    exact=set()
    for g in [1,2,5,7]:
        for ones,twos in [(7,0),(3,1)]:
            for k1 in itertools.combinations_with_replacement(range(-2,3),ones):
                for k2 in itertools.combinations_with_replacement(range(-2,3),twos):
                    if sum(k*k for k in k1+k2)!=7-g:continue
                    if sum(k1)+2*sum(k2)!=0:continue
                    exact.add((g,tuple((1,k)for k in k1)+tuple((2,k)for k in k2)))
    recorded=set()
    for item in saved['spectra']:
        pairs=[]
        for row in item['nonintegral_dimensions']:
            t,k,n=row['t'],row['k'],row['multiplicity']
            need(row['dimension']==[7*t+k,5*t],'dimension encoding')
            pairs.extend([(t,k)]*n)
        key=(item['invertible_count'],tuple(sorted(pairs)))
        need(key not in recorded,'distinct saved spectrum')
        recorded.add(key)
        need(item['rank']==item['invertible_count']+len(pairs),'spectrum rank')
        g=key[0]
        orbit_bad=(g==7 and sum(t==1 for t,k in pairs)%7!=0)
        need(item['excluded_by_orbit_test']==orbit_bad,'exact invertible-orbit obstruction')
    need(exact==recorded and len(exact)==11,'independent complete partition enumeration')
    # The covered commutant has b=c and 7(a-d)=2b. Check every matrix in
    # a finite control box against its exact integral parameterization.
    A=[[7,7],[7,5]];controls=0
    for a,b,d in itertools.product(range(31),repeat=3):
        Y=[[a,b],[b,d]]
        if product(A,Y)!=product(Y,A):continue
        need(b%7==0 and (a+d)%2==0,'covered integral commutant divisibility')
        t=b//7;s=(a+d)//2
        need(Y==[[s+t,7*t],[7*t,s-t]],'covered complete parameterization')
        controls+=1
    # This is a concrete counterexample to imposing 5-divisibility in the
    # other branch. It is only a commuting matrix, not a categorical model.
    A2=[[11,5],[5,1]];Y2=[[2,1],[1,0]]
    need(product(A2,Y2)==product(Y2,A2) and Y2[0][1]%5!=0,'uncovered-branch control')
    return {'kind':'independent_R3472_single_branch_spectrum_review',
        'reviewed_receipt_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
        'covered_module_generator':saved['covered_module_generator'],
        'independent_partition_spectra':len(exact),
        'spectra_by_invertible_count':dict(sorted(Counter(g for g,_ in exact).items())),
        'orbit_exclusions':sum(r['excluded_by_orbit_test']for r in saved['spectra']),
        'surviving_necessary_spectra':10,'covered_commutant_control_matrices':controls,
        'other_branch_nondivisible_commuting_matrix':Y2,
        'scope':'one recorded rank-two action only; no categorification, fusion multiplication, or general ring exclusion'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    out=json.loads(json.dumps(run()));path=HERE/'r3472_independent_review.json'
    if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==json.loads(path.read_text()),'saved independent review changed')
    print('PASS: independent square-partition enumeration gives 11 -> 10 spectra for one R3472 module branch; other branch explicitly out of scope.')
