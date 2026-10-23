"""Exact formal-codegree dimension-lattice obstruction for four rank-nine rings.

Only rational linear algebra and the input fusion tensor are used.  General
categorification is reduced to pseudo-unitarity by the separate signed audit.
"""
import json, sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'work/obstructions'))
from arithmetic import read
from rings import Characters,codegree_poly
from exact import vector,ec,pc

IDS=['R9_1_15','R9_1_68','R9_1_88','R9_1_116']

def verify():
    out=[]
    for r in read():
        if r['id'] not in IDS:continue
        R=r['tensor'];ch=Characters(R);f,K,ds,D,pD,emb=ch.fp()
        if f.degree()!=3:raise ValueError('wrong field degree')
        nonrational=[]
        for d in ds:
            if d not in [K.one,K(2)] and d not in nonrational:nonrational.append(d)
        if len(nonrational)!=2:raise ValueError('wrong dimension types')
        # Order the two irrational dimensions by the exact positive embedding.
        a,b=nonrational
        if emb.sign(a-b)>0:a,b=b,a
        V=s.Matrix.hstack(*[vector(d,3) for d in [K.one,a,b]])
        if not V.det():raise ValueError('dimension generators dependent')
        coords=[list(V.inv()*vector(d,3)) for d in ds]
        if any(x.q!=1 for row in coords for x in row):raise ValueError('not an integral dimension lattice')
        cp=codegree_poly(R)
        if cp.eval(8)!=0:raise ValueError('formal codegree eight absent')
        total=list(V.inv()*vector(D,3));beta=list(V.inv()*vector(D/K(8),3))
        if total!=[24,4,8] or beta!=[3,s.Rational(1,2),1]:raise ValueError('wrong lattice obstruction')
        rec={'id':r['id'],'tensor_sha256':r['tensor_sha256'],
             'status':'excluded_after_Galois_pseudo_unitary_reduction',
             'kind':'formal_codegree_dimension_lattice','formal_codegree':8,
             'separating_k':ch.k,'field_polynomial':pc(f),
             'basis':['1','a','b'],'basis_in_field':[ec(K.one),ec(a),ec(b)],
             'simple_dimension_coordinates':[[str(x) for x in row] for row in coords],
             'global_dimension_coordinates':[str(x) for x in total],
             'required_central_dimension_coordinates':[str(x) for x in beta],
             'obstruction':'The coefficient of a is 1/2, whereas every object dimension lies in Z + Z*a + Z*b.'}
        out.append(rec)
    if [r['id'] for r in out]!=IDS:raise ValueError('missing inputs')
    return out

if __name__=='__main__':
    records=verify()
    (HERE/'cubic_lattice_certificates.json').write_text(json.dumps(records,indent=2)+'\n')
    print('PASS: all four cubic-family rings have the exact dimension-lattice obstruction.')
