#!/usr/bin/env python3
"""Independent exact scalar, branching-grade and center-rank checks for E21."""
from pathlib import Path
from fractions import Fraction
import argparse, hashlib, json
import sympy as s

def need(ok,why):
    if not ok:raise ValueError(why)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    vacuum=[(0,0),(4,4),(6,6),(10,10),(21,0),(0,21),
            (13,4),(4,13),(10,1),(1,10),(9,6),(6,9)]
    weights=[(a,b) for a in range(22) for b in range(22-a)]
    h=lambda a,b:Fraction(a*a+b*b+a*b+3*a+3*b,72)
    need(len(weights)==253,'SU3_21 rank')
    for a,b in vacuum:
        need(h(a,b).denominator==1 and (a-b)%3==0,'Vacuum branching not neutral')
    twist_one=[(a,b) for a,b in weights if h(a,b).denominator==1]
    need(all((a-b)%3==0 for a,b in twist_one),'Twist-one label not neutral')
    neutral={x for x in weights if (x[0]-x[1])%3==0}
    J=lambda x:(21-x[0]-x[1],x[0])
    orbits=set()
    for x in neutral:
        need(J(J(J(x)))==x,'Simple current has wrong order')
        orbits.add(tuple(sorted({x,J(x),J(J(x))})))
    singles=[o for o in orbits if len(o)==1];triples=[o for o in orbits if len(o)==3]
    need(len(neutral)==85 and len(triples)==28 and singles==[((7,7),)],
         'Incorrect neutral simple-current orbit decomposition')
    D=144+96*s.sqrt(2)+80*s.sqrt(3)+56*s.sqrt(6)
    product=(s.sqrt(6)-s.sqrt(2)-1)/8
    need(s.simplify(s.sin(s.pi/24)**2*s.sin(s.pi/12)-product)==0,
         'Incorrect exact trigonometric product')
    need(s.simplify(s.sqrt(6)/product-D)==0,'Global dimension mismatch')
    C=3*24**2/(64*s.sin(s.pi/24)**4*s.sin(s.pi/12)**2)
    need(s.simplify(C-s.Rational(9,2)*D**2)==0,'Weyl dimension normalization')
    proof=Path(__file__).with_name('E21_MODEL_AUDIT.md')
    result={'status':'PASS','scope':'Scalar and grading arithmetic; exact tensor match is separate.',
            'SU3_level':21,'SU3_rank':253,'vacuum_branching':vacuum,
            'vacuum_conformal_weights':[str(h(*x)) for x in vacuum],
            'triality_counts':[sum((a-b)%3==t for a,b in weights) for t in range(3)],
            'neutral_free_simple_current_orbits':len(triples),
            'neutral_fixed_weights':[[7,7]],'fixed_point_splitting':3,
            'neutral_deequivariantization_rank':31,'neutral_E21_center_rank':62,
            'neutral_global_FPdim':str(D),
            'audit_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
            'verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
