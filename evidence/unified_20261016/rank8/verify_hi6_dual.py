#!/usr/bin/env python3
"""Exact identification of the HI(C6) Q-system dual with R8_2_535.

The categorical construction and theoretical uniqueness argument are in
HI6_DUAL_PROOF.md. This standard-library replay checks the full reconstructed
character table, all structure constants, the canonical module, and the
independent census/ledger binding. It does not solve pentagon equations.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import gzip
import hashlib
import itertools
import json


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def q(a=0,b=0):
    return F(a),F(b)


def add(x,y):
    return x[0]+y[0],x[1]+y[1]


def mul(x,y):
    return x[0]*y[0]+10*x[1]*y[1],x[0]*y[1]+x[1]*y[0]


def inv(x):
    n=x[0]*x[0]-10*x[1]*x[1]
    return x[0]/n,-x[1]/n


def total(xs):
    out=q()
    for x in xs: out=add(out,x)
    return out


def flat(x):
    return tuple(c for m in x for row in m for c in row)


def rank(A):
    A=[[F(x)for x in row]for row in A]
    r=0
    for c in range(len(A[0])):
        pivot=next((i for i in range(r,len(A))if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        den=A[r][c];A[r]=[x/den for x in A[r]]
        for i in range(r+1,len(A)):
            den=A[i][c]
            if den:A[i]=[x-den*y for x,y in zip(A[i],A[r])]
        r+=1
    return r


def module():
    I=[[int(i==j)for j in range(7)]for i in range(7)]
    B=[[0]*7 for i in range(7)]
    for i in range(6): B[i][(i+3)%6]=1
    B[6][6]=1
    def mat(shifts,bottom):
        M=[[0]*7 for i in range(7)]
        for i in range(6):
            for j in shifts:M[i][(i+j)%6]+=1
            M[i][6]=M[6][i]=1
        M[6][6]=bottom
        return M
    return [I,B,mat([0],5),mat([3],5),mat([1,5],6),mat([2,4],6),mat([],4),mat([],4)]


def character_table():
    chars=[
        [q(1),q(1),q(3,1),q(3,1),q(4,1),q(4,1),q(2,1),q(2,1)],
        [q(1),q(1),q(3,-1),q(3,-1),q(4,-1),q(4,-1),q(2,-1),q(2,-1)],
    ]+[[q(x)for x in row]for row in [
        [1,-1,1,-1,1,-1,0,0],
        [1,1,1,1,-1,-1,0,0],
        [1,-1,1,-1,-2,2,0,0],
        [1,1,-1,-1,0,0,1,1],
        [1,-1,-1,1,0,0,1,-1],
        [1,-1,-1,1,0,0,-2,2],
    ]]
    f=[q(120,36),q(120,-36),q(6),q(6),q(12),q(6),q(6),q(12)]
    return chars,f


def model():
    """Reconstruct the tensor independently of the census and its ordering."""
    chars,f=character_table()
    for a,b in itertools.product(range(8),repeat=2):
        require(total(mul(chars[a][i],chars[b][i])for i in range(8))==(f[a]if a==b else q()),'character orthogonality')
    require(total(inv(x)for x in f)==q(1),'formal-codegree reciprocity')
    N=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i,j,k in itertools.product(range(8),repeat=3):
        x=total(mul(mul(mul(chars[a][i],chars[a][j]),chars[a][k]),inv(f[a]))for a in range(8))
        require(x[1]==0 and x[0].denominator==1 and x[0]>=0,'nonintegral or negative structure constant')
        N[i][j][k]=int(x[0])
    require(max(flat(N))==2,'unexpected derived multiplicity')
    return N


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);args=p.parse_args()
    N=model()
    for i,j,k,t in itertools.product(range(8),repeat=4):
        require(sum(N[i][j][a]*N[a][k][t]for a in range(8))==sum(N[j][k][a]*N[i][a][t]for a in range(8)),'associativity')
    M=module()
    require(rank([[M[i][a][b]for i in range(8)]for a,b in itertools.product(range(7),repeat=2)])==5,'canonical module image rank')
    for i,j,a,b in itertools.product(range(8),range(8),range(7),range(7)):
        require(sum(M[i][a][c]*M[j][c][b]for c in range(7))==sum(N[i][j][k]*M[k][a][b]for k in range(8)),'canonical module multiplication')
    source=args.repo/'supplements/rank8/data/rank8_tables.txt.gz'
    with gzip.open(source,'rt')as stream:
        rows=[json.loads(line.replace('{','[').replace('}',']'))for line in stream]
    rows=sorted((r for r in rows if max(flat(r))==2),key=flat)
    R=rows[534]
    tensor_sha=hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()
    ledger=json.loads((args.repo/'supplements/rank8/data/decisions.json').read_text())
    record=next(x for x in ledger if x['id']=='R8_2_535')
    require(record['tensor_sha256']==tensor_sha,'independent census-ledger binding')
    perm=[0,1,3,6,4,5,2,7]
    for i,j,k in itertools.product(range(8),repeat=3):
        require(N[i][j][k]==R[perm[i]][perm[j]][perm[k]],'complete source tensor comparison')
    print(json.dumps({
        'status':'PASS','id':'R8_2_535',
        'mathematical_verdict':'unitary_categorification_exists',
        'construction':'dual of the Q-system 1+rho in a known unitary HI(C6) category',
        'model_basis':['1','beta3','rhohat','rhohat_beta3','eta1','eta2','sigma1','sigma2'],
        'model_basis_to_census_zero_based':perm,
        'tensor_sha256':tensor_sha,
        'structure_constants_compared':512,
        'associativity_coefficients_checked':4096,
        'canonical_module_image_rank':5,
        'module_multiplication_coefficients_checked':3136,
        'module_eta_bottom_right_entries':[6,6],
        'formal_codegrees':['120+36sqrt(10)','120-36sqrt(10)',6,6,12,6,6,12],
        'all_simple_objects_self_dual':True,
        'categorical_proof_checked_by_this_program':False,
    },indent=2))

if __name__=='__main__':main()
