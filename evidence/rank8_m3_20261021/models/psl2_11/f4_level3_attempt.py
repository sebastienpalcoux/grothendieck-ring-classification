#!/usr/bin/env python3
"""Exact F4 level-3 Weyl-dimension comparison; a model-attempt bound only.

This does not exclude categorifications of the census rings. It proves that
the unitary F4 level-3 category, of dimension 240+96 sqrt(6), is not a
Morita source for the specified quartic-dimension family. Default replays
the saved result; --write regenerates it. Arithmetic is in Q(zeta_48).
"""
import argparse
import itertools
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent

def require(condition,message):
    if not condition:
        raise ValueError(message)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    z=s.Symbol('z')
    modulus=s.Poly(s.cyclotomic_poly(48,z),z,domain=s.QQ)
    def reduced(p):
        return s.rem(s.Poly(p,z,domain=s.QQ),modulus).as_expr()
    def multiply(a,b):
        return reduced(a*b)
    def power(n):
        return reduced(z**(n%48))
    def vector(*x):
        return s.Matrix(x)
    e=[s.eye(4)[:,i] for i in range(4)]
    simple=[e[1]-e[2],e[2]-e[3],e[3],(e[0]-e[1]-e[2]-e[3])/2]
    B=s.Matrix.hstack(*simple)
    roots=[]
    for i,j in itertools.combinations(range(4),2):
        roots += [a*e[i]+b*e[j] for a,b in itertools.product([-1,1],repeat=2)]
    roots += [a*e[i] for i in range(4) for a in [-1,1]]
    roots += [vector(*signs)/2 for signs in itertools.product([-1,1],repeat=4)]
    positive=[a for a in roots if all(x>=0 for x in B.inv()*a)]
    require(len(roots)==48 and len(positive)==24,'wrong F4 root system')
    fundamental=[]
    for i in range(4):
        rhs=s.zeros(4,1)
        rhs[i]=simple[i].dot(simple[i])/2
        fundamental.append(B.T.inv()*rhs)
    rho=sum(fundamental,s.zeros(4,1))
    theta=e[0]+e[1]
    comarks=[int(w.dot(theta)) for w in fundamental]
    require(comarks==[2,3,2,1],'wrong integrability comarks')
    weights=[v for v in itertools.product(range(4),repeat=4)
             if sum(comarks[i]*v[i] for i in range(4))<=3]
    require(len(weights)==9,'wrong level-three rank')
    denominator=1
    for a in positive:
        m=2*rho.dot(a)
        require(m.is_Integer,'nonintegral cyclotomic exponent')
        denominator=multiply(denominator,power(int(m))-power(-int(m)))
    denominator_inverse=s.invert(denominator,modulus.as_expr(),z)
    sqrt2=power(6)+power(-6)
    sqrt3=power(4)+power(-4)
    sqrt6=multiply(sqrt2,sqrt3)
    expected=[(1,0),(3,1),(4,2),(2,1),(5,2),(6,2),(3,1),(2,1),(4,2)]
    records=[]
    dimension=0
    for labels,(a,b) in zip(weights,expected):
        lam=sum((labels[i]*fundamental[i] for i in range(4)),s.zeros(4,1))
        numerator=1
        for root in positive:
            m=2*(lam+rho).dot(root)
            require(m.is_Integer,'nonintegral cyclotomic exponent')
            numerator=multiply(numerator,power(int(m))-power(-int(m)))
        qdim=multiply(numerator,denominator_inverse)
        require(reduced(qdim-a-b*sqrt6)==0,'Weyl dimension differs from claimed radical')
        dimension=reduced(dimension+multiply(qdim,qdim))
        records.append({'dynkin_labels':labels,'dimension_coefficients_in_1_sqrt6':[a,b],
                        'cyclotomic_polynomial':str(qdim)})
    require(reduced(dimension-240-96*sqrt6)==0,'wrong global dimension')
    target=reduced(144+96*sqrt2+80*sqrt3+56*sqrt6)
    require(reduced(dimension-target)!=0,'unexpected target dimension match')
    result={'scope':'failure of this one Morita-source attempt; no categorical exclusion',
            'category':'unitary WZW F4 at level 3','dual_coxeter_number':9,
            'cyclotomic_order':48,'cyclotomic_modulus':str(modulus.as_expr()),
            'positive_root_count':24,'comarks':comarks,'simple_objects':records,
            'global_dimension':'240+96*sqrt(6)',
            'target_global_dimension':'144+96*sqrt(2)+80*sqrt(3)+56*sqrt(6)',
            'target_ids':['R8_3_916','R8_3_928','R8_3_941','R8_3_1348'],
            'exact_difference_polynomial':str(reduced(dimension-target)),
            'conclusion':'different global dimension; not Morita equivalent'}
    path=HERE/'f4_level3_attempt.json'
    if args.write:
        path.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(json.loads(path.read_text())==json.loads(json.dumps(result)),'saved result does not replay')
    print(json.dumps({'rank':9,'global_dimension':result['global_dimension'],
                      'quartic_target_dimension_match':False,'mode':'write' if args.write else 'compare'}))

if __name__=='__main__':
    main()
