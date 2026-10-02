#!/usr/bin/env python3
"""Exact conditional reduction, never a classification decision."""
import argparse,itertools,json,math,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if (p/'supplements/rank7/data/rank7_tables.txt.gz').exists())
sys.path.insert(0,str(ROOT/'evidence/upper_residual_20261002b/r7_nonintegral'))
from case_source import SOFTWARE,read_cases
sys.path.insert(0,str(SOFTWARE))
from rings import Characters,dual
from exact import pc
import sympy as s
z=s.symbols('z')
def require(c,m):
    if not c:raise ValueError(m)

def verify():
    tested=0;survive=[]
    for a in range(1,6):
        for b,c,d in itertools.product(range(1,3*a*a//8+1),range(1,a**3//16+1),range(1,a**4//256+1)):
            p=s.Poly(z**4-a*z**3+b*z*z-c*z+d,z);tested+=1
            if p.is_irreducible and p.count_roots(0,s.oo)==4:survive.append([str(x)for x in p.all_coeffs()])
    require(not survive,'totally positive quartic of trace<=5 survived')
    residual=[]
    for k in range(1,8):
        p=s.Poly(z*z-43*k*z+90*k,z)
        require(p.is_irreducible and s.Rational((43*k)**2,90*k).q!=1,'residual codegree dnumber survives')
        residual.append([str(x)for x in p.all_coeffs()])
    candidates=[(a,b)for a in range(1,6)for b in range(-5,6)if a%2==b%2 and a*a>5*b*b]
    require(candidates==[(2,0),(3,-1),(3,1),(4,0),(5,-1),(5,1)],'quadratic beta list changed')
    records=[]
    for id,c in read_cases(['R7_4_1212','R7_4_1213']).items():
        R=c['tensor'];a=Characters(R);integers=[int(-p.TC())for p,m in a.cf if p.degree()==1]
        require(dual(R)==list(range(7)),'self-dual source')
        require(R[1][1][0]==1 and all(R[1][i][i]==1 and sum(R[1][i])==1 for i in range(2,7)),'pointed order2 stabilizer')
        require(math.lcm(*integers)==180 and any(pc(p)==['1','-900','6480']for p,m in a.cf),'formalcodegrees')
        B=int(a.C.trace());require(B in(1036,1020) and 6*180+2>B,'degree6 bound')
        require(4*360+2>B and 4*180+2<=B,'degree4 rationaldelta bound')
        records.append({'id':id,'source_sha256':c['tensor_sha256'],'trace_bound':B,'remaining_character_field':'Q(sqrt5)','remaining_character_degree':2,'global_dimensions':[[90*x,90*y]for x,y in candidates],'general_status':'unresolved','pivotal_status':'excluded'})
    return {'status':'PASS','scope':'conditional_necessary_reduction','quartic_polynomials_checked':tested,'quartic_survivors':survive,'degree4_residual_dnumber_failures':residual,'cases':records,'classification_decisions':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();r=verify();t=json.dumps(r,indent=2)
    if args.output:args.output.write_text(t+'\n')
    print(t)
