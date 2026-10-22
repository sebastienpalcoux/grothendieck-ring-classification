#!/usr/bin/env python3
"""Exact arithmetic audit for all-Morita R3472 restrictions (standard library).

Categorical inputs and their proofs are in manuscript.tex. This is an arithmetic
certificate, not an associator construction or a general exclusion of R3472.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TENSOR = ROOT / 'site/dist/downloads/fusion-tensors/R8_3_3472.txt'

def need(condition, message):
    if not condition:
        raise ValueError(message)

def mul(x, y):
    a, b = x; c, d = y
    return (a*c+2*b*d, a*d+b*c)

def dimension_profiles():
    # For a free C5 orbit representative the remaining moment sums are
    # (69,35,49), and the sum of (5a-7b)^2 is 10.
    types = [(a,b) for a in range(9) for b in range(1,6)
             if a*a <= 69 and b*b <= 35 and a*b <= 49
             and (5*a-7*b)**2 <= 10]
    answers = []
    def visit(i, A, B, C, chosen):
        if (A,B,C) == (0,0,0):
            answers.append(chosen); return
        if i == len(types) or C*C > A*B:
            return
        a,b = types[i]
        cap = min(A//(a*a), B//(b*b), C//(a*b))
        for n in range(cap+1):
            visit(i+1, A-n*a*a, B-n*b*b, C-n*a*b,
                  chosen + ([[a,b,n]] if n else []))
    visit(0,69,35,49,[])
    return types, sorted(answers)

def polynomial_mod2_remainder(p, q):
    # Binary polynomial encoding; addition/subtraction is xor.
    while p.bit_length() >= q.bit_length():
        p ^= q << (p.bit_length()-q.bit_length())
    return p

def main(write=False):
    N = ast.literal_eval(TENSOR.read_text())
    need(len(N)==8, 'Source rank changed')
    dual = [next(j for j in range(8) if N[i][j][0]) for i in range(8)]
    invertibles = [i for i in range(8) if sum(N[i][dual[i]])==1]
    need(invertibles == [0], 'Source invertibles changed')
    need(all(N[i][i][i] == 2 for i in range(1,8)),
         'Diagonal fusion no longer forces trivial tensor automorphisms')
    # Exact source FP character; all positive and positive-ring character.
    # Read the canonical ordering independently from the frozen source actions.
    actions_path=ROOT/'evidence/rank8_next_20261021/quadratic/action_classes.json'
    actions=json.loads(actions_path.read_text())['R8_3_3472']['complete_action_classes']
    action=next(x['actions'] for x in actions if x['module_rank']==2
                and x['actions'][1]==[[5,7],[7,7]])
    dims=[((x[0][0]+x[1][1])//2,5*x[0][1]//7) for x in action]
    need(dims[0]==(1,0) and all(a>=0 and b>=0 and a+b>0 for a,b in dims),
         'Source dimension vector not positive')
    for i in range(8):
        for j in range(8):
            need(mul(dims[i],dims[j]) == tuple(sum(N[i][j][k]*dims[k][c]
                 for k in range(8)) for c in (0,1)), 'Source FP character mismatch')
    D=tuple(sum(mul(x,x)[c] for x in dims) for c in (0,1))
    need(D==(700,490), 'Source global dimension changed')
    need(700**2-2*490**2==9800 and 1400*7==9800, 'Galois Gram bound changed')
    allowed=[h for h in range(1,8) if 1400%h==0 and 9800%(h*h)==0]
    need(allowed==[1,2,5,7], 'Lagrange domain changed')
    need(245%2==1, 'Order-two pointed-orbit parity obstruction changed')

    # Strong Lagrange says a fixed C5 object has square divisible by 5.
    nilpotents=[(a,b) for a in range(5) for b in range(5)
                if (a*a+2*b*b)%5==0 and (2*a*b)%5==0]
    need(nilpotents==[(0,0)], 'Unexpected nilpotent modulo five')
    fixed=[(a,b) for a in range(0,19,5) for b in (5,10)
           if a*a<=345 and b*b<=175 and (5*a-7*b)**2<=50]
    need(fixed==[(15,10)], 'Fixed-point candidate domain changed')
    need(2*225>345, 'More than one fixed-point candidate is possible')
    need(95**2 > 120*75, 'Residual Cauchy obstruction failed')
    types,profiles=dimension_profiles()
    expected=sorted([
       [[2,1,1],[4,3,1],[7,5,1]],
       [[1,1,1],[4,3,2],[6,4,1]],
       [[1,1,1],[3,2,4],[4,3,2]],
       [[1,1,2],[3,2,2],[7,5,1]],
    ])
    need(profiles==expected, 'Complete orbit-profile enumeration changed')
    need(all(max(x[2] for x in p)<5 for p in profiles),
         'Right C5 action may permute left orbits')
    # First profile: XX* - 1 has coordinates (5,4), whereas all available
    # nonintegral dimensions have even rational part or rational part >=7.
    need(mul((2,1),(2,1))==(6,4), 'First-profile dimension equation changed')
    decompositions=[(u,v,w) for u in range(6) for v in range(6) for w in range(2)
                    if 2*u+4*v+7*w==5 and u+3*v+5*w==4]
    need(not decompositions, 'First profile has an unexpected XX* decomposition')
    # In the other three profiles, delta^2=(3,2), delta=1+sqrt(2).
    # With one invertible summand the only possible nonintegral part is 2delta.
    # Without one, the only possible decomposition is a single delta^2 simple.
    for p in profiles:
        if p[0][:2] != [1,1]: continue
        available=[tuple(x[:2]) for x in p]
        def dec(target):
            out=[]
            def walk(i,A,B,chosen):
                if i==len(available):
                    if (A,B)==(0,0):out.append(chosen)
                    return
                a,b=available[i]
                for n in range(min(A//a,B//b)+1):
                    walk(i+1,A-n*a,B-n*b,chosen+[n])
            walk(0,*target,[])
            return out
        need(dec((2,2))==[[2]+[0]*(len(available)-1)],
             'Unexpected product with an invertible summand')
        no_unit=dec((3,2))
        need(all(sum(x)==1 and all(n==0 or available[k]==(3,2)
             for k,n in enumerate(x)) for x in no_unit),
             'Unexpected product without an invertible summand')

    # C5 + one free delta orbit: right action exponent squares to one.
    exponents=[a for a in range(1,5) if a*a%5==1]
    need(exponents==[1,4], 'Involution exponents changed')
    symmetric=[]
    for m0 in range(3):
        for m1 in range(2):
            for m2 in range(2):
                if m0+2*m1+2*m2==2:symmetric.append([m0,m1,m2,m2,m1])
    need(symmetric==[[0,0,1,1,0],[0,1,0,0,1],[2,0,0,0,0]],
         'C5 symmetric coefficient list changed')
    # Formal-codegree quartic P reduces mod2 to x^4+x^3+1.
    P=[1,-55,1000,-7250,18125]
    need([a%2 for a in P]==[1,1,0,0,1], 'Quartic reduction changed')
    p=0b11001
    need(p&1 and sum((p>>i)&1 for i in range(5))%2==1,
         'Quartic has an F2 root')
    need(polynomial_mod2_remainder(p,0b111)!=0,
         'Quartic has the irreducible F2 quadratic factor')
    need(55**4%18125==15625, 'd-number violation changed')
    # Put y=f/5=1+x^2. Then (y-1)t^2=(y-2)^2 and
    # t^2+t-1=0 imply (y-1)t=-y^2+5y-5. Substitution gives
    # y^4-11y^3+40y^2-58y+29=0, and f=5y.
    def polymul(a,b):
        c=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]+=x*y
        return c
    aa=polymul([-5,5,-1],[-5,5,-1])
    ab=polymul([-5,5,-1],[-1,1])+[0]
    bb=polymul([-1,1],[-1,1])+[0,0]
    need([x+y-z for x,y,z in zip(aa,ab,bb)]==[29,-58,40,-11,1],
         'Elimination polynomial identity changed')
    need(P==[1,-11*5,40*25,-58*125,29*625], 'Quartic scaling identity changed')

    spectra_path=ROOT/'evidence/rank8_research_20261022/r1768_r3472/r3472_rank_two_dual_spectra.json'
    old=json.loads(spectra_path.read_text())['spectra']
    old_retained=[1,2,4,6,7,8,10]
    retained=[i for i in old_retained if old[i]['invertible_count'] in (1,7)]
    need(retained==[1,2,4,10], 'First-branch consequences changed')
    out={
      'status':'PASS','case_id':'R8_3_3472',
      'scope':'Every complex fusion category categorifying R3472 and every Morita partner; no assumed rank-two module lift',
      'source_dimensions':[list(x) for x in dims],
      'source_central_invertibles':1,
      'global_dimension':list(D),
      'dimension_field':'Q(sqrt(2))',
      'dimension_moments':{'sum_a_squared':350,'sum_b_squared':175,'sum_ab':245},
      'integral_subcategory_dimensions_before_orbit_test':allowed,
      'C5_fixed_point_candidates':[list(x) for x in fixed],
      'C5_fixed_point_residual_cauchy':{'left':95**2,'right':120*75},
      'C5_orbit_representative_types':[list(x) for x in types],
      'C5_complete_orbit_profiles':profiles,
      'C5_rank10_formal_codegree_polynomial':P,
      'C5_d_number_remainder':55**4%18125,
      'morita_invertible_counts':[1,7],
      'first_rank_two_branch_retained_spectrum_indices':retained,
      'seven_invertible_profile':{'invertibles':7,'noninvertibles':[{'dimension':[7,5],'multiplicity':7}]},
      'general_categorification_status':'unresolved','new_model_constructed':False,
      'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (TENSOR,actions_path,spectra_path)}
    }
    path=HERE/'verification.json'
    if write:path.write_text(json.dumps(out,indent=2)+'\n')
    else:need(json.loads(path.read_text())==out, 'Saved receipt differs')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true')
    main(p.parse_args().write)
