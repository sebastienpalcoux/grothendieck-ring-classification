#!/usr/bin/env python3
"""Independent cyclotomic-quotient check of all bounded joint trace types."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,math
import numpy as np
import sympy as s
from flint import fmpz_poly
import general_biquadratic as gb
HERE=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise ValueError(msg)

def validate(q,r,height,primes):
    gb.configure(q,r);gb.PRIMES=primes
    all_types,bound=gb.trace_types(height)
    L=math.lcm(int(bound),math.lcm(*range(1,height+1)));x=s.Symbol('x');phi=s.Poly(s.cyclotomic_poly(L,x),x)
    degree=phi.degree();co=np.array(list(reversed(list(map(int,phi.all_coeffs())))),dtype=np.int64)
    powers=np.zeros((L,degree),dtype=np.int64);powers[0,0]=1
    for j in range(1,L):
        old=powers[j-1]
        require(max(map(abs,map(int,old)))*(1+max(map(abs,map(int,co))))<2**60,'cyclotomic recurrence overflow bound')
        powers[j,1:]=old[:-1];powers[j]-=int(old[-1])*co[:-1]
    max_power=max(map(abs,map(int,powers.flat)))
    require(max_power*L<2**50 and L**3*height<2**60,'cyclotomic summation/index overflow bound')
    modulus=fmpz_poly(list(map(int,co)))
    def gauss(d):
        D=gb.conductor(d);scale=math.isqrt(D//d);out=np.zeros(degree,dtype=np.int64)
        require(L%D==0,'field conductor absent')
        for a in range(D):out+=int(s.kronecker_symbol(D,a))*powers[(a*(L//D))%L]
        require(all(int(v)%scale==0 for v in out),'Gauss basis not divisible')
        return out//scale
    b0=np.zeros(degree,dtype=np.int64);b0[0]=1
    basis=[b0,gauss(q),gauss(r),gauss(q*r)]
    polynomials=[fmpz_poly(list(map(int,b))) for b in basis]
    require((polynomials[1]**2-q)%modulus==0,'first Gauss square')
    require((polynomials[2]**2-r)%modulus==0,'second Gauss square')
    require((polynomials[1]*polynomials[2]-polynomials[3])%modulus==0,'correlated third Gauss sign')
    B=s.Matrix(np.stack(basis,axis=1).tolist());pivots=list(B.T.rref()[1]);require(len(pivots)==4,'degree-four Gauss basis')
    inverse=B.extract(pivots,range(4)).inv()
    units=[u for u in range(L) if math.gcd(u,L)==1]
    signs=lambda u:(int(s.kronecker_symbol(gb.conductor(q),u)),int(s.kronecker_symbol(gb.conductor(r),u)))
    H=np.array([u for u in units if signs(u)==(1,1)],dtype=np.int64)
    require(len(H)*4==len(units),'fixed subgroup index')
    representatives={signs(u):u for u in units};require(len(representatives)==4,'all four field automorphisms')
    def exact_trace(n,k,u):
        sums=powers[(H*(L//n)*k*u)%L].sum(axis=0)
        values=inverse*s.Matrix([int(sums[p]) for p in pivots])/len(H)
        coords=tuple(F(int(v.p),int(v.q)) for v in values)
        denominator=math.lcm(*(v.denominator for v in coords))
        predicted=[sum(int(basis[j][i])*int(coords[j]*denominator) for j in range(4)) for i in range(degree)]
        require(all(predicted[i]*len(H)==int(sums[i])*denominator for i in range(degree)),'full relative-trace polynomial identity')
        return coords
    records=[];joint=set()
    requests=[(int(n),list(range(1,height+1)),'central') for n in s.divisors(bound)]
    requests += [(int(n),[int(k) for k in s.divisors(m) if k<m],'rotation_'+str(m)) for m in range(3,height+1) for n in s.divisors(m)]
    for n,ps,kind in requests:
        actual={tuple(exact_trace(n,k,u) for k in ps) for u in representatives.values()}
        formula,_=gb.trace_types(height,[n],ps)
        require(actual==set(formula),'joint trace formula '+str((q,r,n,ps)))
        records.append(dict(kind=kind,order=n,powers=ps,types=len(actual)))
        if kind=='central':joint|=actual
    # The analytic prime-power bound proves that all orders outside the box
    # give the joint zero type; direct enumeration checks every in-box order.
    joint.add(tuple((F(0),)*4 for _ in range(height)))
    require(joint==set(all_types),'complete bounded joint types')
    return dict(radicands=[q,r],height=height,primes=primes,order_bound=int(bound),ambient_cyclotomic_order=L,cyclotomic_degree=degree,fixed_subgroup_size=len(H),joint_types=len(joint),checks=records)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    records=[validate(q,r,h,ps) for q,r,h,ps in [(2,3,6,[2,3]),(3,7,4,[2,3,7]),(3,5,4,[2,3,5]),(3,13,4,[2,3,13])]]
    files=[Path(__file__),HERE/'general_biquadratic.py',HERE/'biquadratic_traces.py']
    result=dict(schema='independent-cyclotomic-relative-traces-v1',status='PASS',method='Exact quotient by cyclotomic polynomial; explicit quadratic Gauss sums; complete fixed-subgroup averages and full coefficient identities',records=records,source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
    target=HERE/'general_biquadratic_trace_validation.json'
    if args.write:target.write_text(json.dumps(result,indent=2)+'\n')
    else:require(json.loads(target.read_text())==result,'trace validation receipt differs')
    print('PASS: four biquadratic families, all bounded orders, correlated joint powers, exact cyclotomic identities',flush=True)
if __name__=='__main__':main()
