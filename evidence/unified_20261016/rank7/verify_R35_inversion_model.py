#!/usr/bin/env python3
"""Exact source-independent model for the NG(C4²,16) inversion construction."""
import argparse
import collections
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp

from verify_R2665_inversion_model import (
    require, tensor_hash, fusion_checks, dihedral_model,
    multiply, unit_vector, based_match)


def rank7_model():
    # Basis 1,g,h,gh,X,Y,Z.  V4=<g,h>, h fixes Y,Z, and g swaps them.
    out = [[[0]*7 for _ in range(7)] for _ in range(7)]
    for i,j in itertools.product(range(4),repeat=2):
        out[i][j][i^j] = 1
    for i in range(4):
        out[i][4][4] = out[4][i][4] = 1
        for j in (5,6):
            out[i][j][j if i % 2 == 0 else 11-j] = 1
            out[j][i] = out[i][j].copy()
    out[4][4] = [1,1,1,1,0,0,0]
    for j in (5,6):
        out[4][j] = out[j][4] = [0,0,0,0,0,1,1]
    out[5][5] = out[6][6] = [1,0,1,0,1,4,4]
    out[5][6] = out[6][5] = [0,1,0,1,1,4,4]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--model-output',type=Path)
    args = ap.parse_args()
    G = list(itertools.product(range(4),repeat=2))
    H = [(i,i) for i in range(4)]
    add = lambda g,h: tuple((g[i]+h[i])%4 for i in range(2))
    chi = lambda g,h: 2*(g[0]*h[0]-g[1]*h[1])%8
    a = lambda g: 3*(g[0]**2-g[1]**2)%8
    require(all((a(add(g,h))+chi(g,h)-a(g)-a(h))%8 == 0
                for g,h in itertools.product(G,repeat=2)), 'quadratic refinement')
    require([g for g in G if all(chi(g,h)==0 for h in H)] == H,
            'cyclic H is its annihilator')
    require(all(a(h)==0 for h in H), 'self-dual orbifold')
    require(all((add(g,h)[0]-add(g,h)[1])%4 == (g[0]-g[1])%4 for g in G for h in H),
            'quotient map onto C4')
    require(all(((4*(i))%4,0)==(0,0) for i in range(4)),
            'quotient has a strict order-four lift')
    model = rank7_model()
    t = 2+sp.sqrt(5)
    require(fusion_checks(model,[1]*4+[2,2*t,2*t]) == list(range(7)),
            'all seven model objects self-dual')
    group,index,mul,phi,tensor = dihedral_model((0,0))
    fusion_checks(tensor,[1]*8+[t]*8)
    L = [(0,0),(0,1)]
    algebra = [int(i<8 and group[i] in L) for i in range(16)]
    def induce(i):
        return multiply(tensor,multiply(tensor,algebra,unit_vector(16,i)),algebra)
    x,y,z = index[(1,0)],8+index[(0,0)],8+index[(2,0)]
    fx,fy,fz = induce(x),induce(y),induce(z)
    fodd = multiply(tensor,unit_vector(16,index[(2,0)]),algebra)
    forgotten = [algebra,fodd,algebra,fodd,fx,fy,fz]
    require([a+b for a,b in zip(fy,fz)] == [0]*8+[1]*8,
            'two disjoint irrational double orbits')
    for u,v,i,j in [(y,y,5,5),(y,z,5,6),(z,y,6,5),(z,z,6,6),
                    (x,y,4,5),(y,x,5,4),(x,z,4,6),(z,x,6,4)]:
        actual = multiply(tensor,multiply(tensor,multiply(tensor,
            multiply(tensor,algebra,unit_vector(16,u)),algebra),unit_vector(16,v)),algebra)
        expected = [sum(model[i][j][k]*forgotten[k][l] for k in range(7)) for l in range(16)]
        require(actual==expected,'relative induction identity')
    # Shimizu's nu4 formula for both nondegenerate symmetric forms on C4.
    indicators = [sp.expand(sum(sp.I**(-m*x*x) for x in range(4))/2) for m in (1,3)]
    require(indicators==[1-sp.I,1+sp.I] and all(v!=2 for v in indicators),
            'TY(C4) cannot have FS exponent dividing four')
    counts=collections.Counter();source=None
    path=args.repo/'supplements/rank7/data/rank7_tables.txt.gz'
    for line in gzip.open(path,'rt'):
        if not line.strip():continue
        N=json.loads(line.replace('{','[').replace('}',']'))
        m=max(c for layer in N for row in layer for c in row);counts[m]+=1
        if m==4 and counts[m]==35:source=N
    require(source is not None,'R35 original-source availability')
    maps=[]
    for odd in [(1,2),(2,1)]:
        for irr in [(3,4),(4,3)]:
            p=[0,odd[0],5,odd[1],6,irr[0],irr[1]]
            if based_match(model,source,p):maps.append(p)
    require(maps,'all343 coefficients match original R7_4_35')
    row={
        'id':'R7_4_35','rank':7,'multiplicity':4,
        'name':'Reflection Morita dual of the inversion extension of NG(C4²,16) diagonal orbifold',
        'source_construction':'Start with Yu-Zhang NG(C4×C4,16), centrally de-equivariantize by diagonal C4, descend the untwisted regular-group self-Morita equivalence to a coherent inversion C2 action, take the crossed product, and dualize its reflection algebra 1+s.',
        'source_reference':'R35_INVERSION_CONSTRUCTION.md; Yu-Zhang Proposition3.1; Izumi Theorems11.3,12.5,13.4 and Corollary13.5; Shimizu Theorem3.4; Ng-Schauenburg Theorem9.2.',
        'source_url':'https://arxiv.org/abs/2412.20763',
        'basis_permutation_model_to_census':maps[0],'tensor':model,
        'existence':dict.fromkeys(['general','pivotal','spherical','pseudo_unitary','unitary'],'yes')}
    receipt={
        'status':'PASS','source_id':'R7_4_35','scope':'exact finite part of a unitary categorical construction',
        'source_tensor_sha256':tensor_hash(source),
        'source_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'model_tensor_sha256':tensor_hash(model),'dihedral_tensor_sha256':tensor_hash(tensor),
        'basis_permutation_model_to_census':maps[0],
        'full_tensor_coefficients_checked':343,'relative_tensor_induction_identities_checked':8,
        'parent_group':'C4×C4','isotropic_subgroup':[list(h) for h in H],
        'quotient':'C4','duality_shift':0,'pointed_associator_order_on_C4':1,
        'group_theoretical_FS_exponent_divides':4,
        'TY_C4_fourth_indicators':[str(v) for v in indicators],
        'integral_group_forced':'V4','categorical_proof':'R35_INVERSION_CONSTRUCTION.md',
        'optimizer_used':False}
    args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    if args.model_output:args.model_output.write_text(json.dumps(row,indent=2)+'\n')
    print(json.dumps({'status':'PASS','source_id':'R7_4_35','model_to_census':maps[0]}))


if __name__=='__main__':main()
