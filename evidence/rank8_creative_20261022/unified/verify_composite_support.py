#!/usr/bin/env python3
"""Exact finite-group spectral projectors for the conductor12/24 refinement."""
from pathlib import Path
from math import gcd,lcm
import argparse,hashlib,json
import sympy as s


def need(ok,message):
    if not ok: raise ValueError(message)


def chi(q,b):
    b%=q
    if gcd(b,q)!=1:return 0
    if q==3:return 1 if b==1 else -1
    if q==4:return 1 if b==1 else -1
    if q==8:return 1 if b in (1,3) else -1
    raise ValueError('Unsupported local conductor')


def local_spectrum(q,epsilon,other_epsilon=None):
    z=s.Symbol('z');mod=s.Poly(s.cyclotomic_poly(q,z),z,domain=s.QQ)
    def reduce(x):return s.Poly(x,z,domain=s.QQ).rem(mod).as_expr()
    def bar(x):
        poly=s.Poly(x,z,domain=s.QQ)
        return reduce(sum(coeff*z**((-monomial[0])%q) for monomial,coeff in poly.terms()))
    gauss=reduce(sum(chi(q,b)*z**b for b in range(q)))
    need(reduce(gauss*gauss)==-q,'Odd quadratic Gauss square')
    points={(x,y) for x in range(q) for y in range(q) if gcd(gcd(x,y),q)==1}
    # s acts by f(x,y)->f(y,-x). For v=F+epsilon*G*H this is:
    Sv={(x,y):reduce(chi(q,-x)+epsilon*gauss*chi(q,y)*int(x==0)) for x,y in points}
    other_epsilon=epsilon if other_epsilon is None else other_epsilon
    Sv2={(x,y):reduce(chi(q,-x)+other_epsilon*gauss*chi(q,y)*int(x==0)) for x,y in points}
    seen=set();norms=[s.Rational(0) for _ in range(q)]
    for x,y in sorted(points):
        if (x,y) in seen:continue
        orbit=[];j=0
        while ((x-j*y)%q,y) not in orbit:
            orbit.append(((x-j*y)%q,y));j+=1
        seen.update(orbit);L=len(orbit)
        for k in range(q):
            if (k*L)%q:continue
            coefficient=reduce(sum(z**((-k*j)%q)*Sv[v] for j,v in enumerate(orbit))/L)
            coefficient2=reduce(sum(z**((-k*j)%q)*Sv2[v] for j,v in enumerate(orbit))/L)
            square=reduce(coefficient*bar(coefficient2))
            need(square.is_Rational,'Nonrational projector pairing')
            if epsilon==other_epsilon:need(square>=0,'Negative projector norm')
            norms[k]+=L*square
    total=2*q*sum(gcd(b,q)==1 for b in range(q))
    need(sum(norms)==(total if epsilon==other_epsilon else 0),'Spectral projectors not complete')
    return [v/total for v in norms]


def composite(q,epsilon):
    n=lcm(q,3);a=local_spectrum(q,epsilon);b=local_spectrum(3,epsilon)
    weights=[s.Rational(0) for _ in range(n)]
    for i,x in enumerate(a):
        for j,y in enumerate(b):weights[((n//q)*i+(n//3)*j)%n]+=x*y
    return weights


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    local={f'{q}:{e}':[str(x) for x in local_spectrum(q,e)] for q in (3,4,8) for e in (-1,1)}
    cross={str(q):[str(x) for x in local_spectrum(q,1,-1)] for q in (3,4,8)}
    need(all(all(x=='0' for x in row) for row in cross.values()),'Nonzero mixed spectral projector pairing')
    rows=[]
    for q in (4,8):
        n=3*q;minus=composite(q,-1);plus=composite(q,1)
        allowed=[k for k in range(n) if minus[k] or plus[k]]
        forbidden=[k for k in range(n) if not minus[k] and not plus[k]]
        expected=[1,11] if n==12 else [1,5,19,23]
        need(forbidden==expected,'Wrong signed conductor support')
        fixed={str(k):str(4*minus[k]) for k in range(n) if minus[k]==plus[k] and minus[k]}
        need(fixed==({'0':'1/3','6':'1/3'} if n==12 else
                     {'0':'1/6','6':'1/6','12':'1/6','18':'1/6'}),'Wrong fixed capacities')
        # c_Z = L_f/sqrt(f), and ||w||^2=4 in the quartic case.
        capacity={k:str(n*s.Rational(v)) for k,v in fixed.items()}
        need(set(capacity.values())=={'4'},'Wrong integer capacity')
        need(4*n*max(minus+plus)==16,'Wrong universal squared integer-mask bound')
        rows.append({'conductor':n,'epsilon_minus_weights':[str(x) for x in minus],
                     'epsilon_plus_weights':[str(x) for x in plus],
                     'allowed_exponents':allowed,'forbidden_exponents':forbidden,
                     'fixed_squared_Fourier_masses':fixed,
                     'fixed_integer_mask_square_capacities':capacity,
                     'universal_integer_mask_absolute_bound':4})
    here=Path(__file__).resolve().parent
    report={'status':'PASS','scope':'Exact local spectral projector calculations and CRT convolution; conceptual arbitrary-representation argument is in COMPOSITE_SIGNED_SUPPORT.md.',
            'local_projector_ratios':local,'local_cross_projector_ratios':cross,'quartic_controls':rows,
            'source_sha256':{name:hashlib.sha256((here/name).read_bytes()).hexdigest()
                             for name in ('verify_composite_support.py','COMPOSITE_SIGNED_SUPPORT.md')}}
    data=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(data)
    print(data,end='')


if __name__=='__main__':main()
