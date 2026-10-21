#!/usr/bin/env python3
"""Complete correlated semion-pair trace domain at height six over Q(sqrt2,sqrt3)."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json,math
import sympy as s
import numpy as np
from flint import fmpz_poly
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def compute():
    n=288;x=s.Symbol('x');phi=s.Poly(s.cyclotomic_poly(n,x),x);degree=phi.degree()
    co=np.array(list(reversed(list(map(int,phi.all_coeffs())))),dtype=np.int64)
    powers=np.zeros((n,degree),dtype=np.int64);powers[0,0]=1
    for j in range(1,n):
        old=powers[j-1];need(max(map(abs,map(int,old)))*(1+max(map(abs,map(int,co))))<2**60,'recurrence overflow bound')
        powers[j,1:]=old[:-1];powers[j]-=int(old[-1])*co[:-1]
    need(max(map(abs,map(int,powers.flat)))*n<2**50,'sum overflow bound')
    def gauss(q,D):
        ans=np.zeros(degree,dtype=np.int64)
        for j in range(D):ans+=int(s.kronecker_symbol(D,j))*powers[(n//D*j)%n]
        scale=math.isqrt(D//q);need(all(int(a)%scale==0 for a in ans),'exact normalized Gauss basis');return ans//scale
    basis=[powers[0],gauss(2,8),gauss(3,12),gauss(6,24)];mod=fmpz_poly(list(map(int,co)))
    bs=[fmpz_poly(list(map(int,b)))for b in basis]
    need((bs[1]**2-2)%mod==0 and(bs[2]**2-3)%mod==0 and(bs[1]*bs[2]-bs[3])%mod==0,'radical basis product')
    B=s.Matrix(np.stack(basis,axis=1).tolist());piv=list(B.T.rref()[1]);need(len(piv)==4,'full field degree');inverse=B.extract(piv,range(4)).inv()
    H=np.array([u for u in range(n)if math.gcd(u,n)==1 and s.kronecker_symbol(8,u)==1 and s.kronecker_symbol(12,u)==1],dtype=np.int64)
    need(len(H)==24,'relative trace subgroup')
    traces=[]
    for exponent in range(n):
        total=powers[(H*exponent)%n].sum(axis=0);z=inverse*s.Matrix([int(total[i])for i in piv])/len(H)
        row=tuple(F(int(v.p),int(v.q))for v in z);den=math.lcm(*(v.denominator for v in row))
        need(all(sum(int(basis[j][i])*int(row[j]*den)for j in range(4))*len(H)==int(total[i])*den for i in range(degree)),'full polynomial relative-trace identity')
        traces.append(row)
    pairs=set();witness={}
    for exponent in range(n):
        row=tuple(tuple(a+b for a,b in zip(traces[(exponent*k)%n],traces[((exponent+n//4)*k)%n]))for k in range(1,7))
        need(not any(row[1])and not any(row[5]),'pair second and sixth moments vanish')
        pairs.add(row);witness.setdefault(row,exponent)
    zero=tuple((F(0),)*4 for _ in range(6));pairs.add(zero)
    ordered=sorted(pairs);need(tuple((F(v),F(0),F(0),F(0))for v in(1,0,1,2,1,0))in pairs,'actual semion pair 1,i control')
    need(all(tuple(tuple(a+b for a,b in zip(traces[(e*k)%n],traces[((e-n//4)*k)%n]))for k in range(1,7))in pairs for e in range(n)),'both semion twist-ratio signs')
    return {'kind':'complete_semion_pair_relative_traces','height':6,'prime_support':[2,3],
        'root_order_box':288,'cyclotomic_degree':degree,'relative_subgroup_size':len(H),
        'pair_twists':'theta,i*theta; also covers theta,-i*theta by interchanging the pair',
        'coordinate_basis':['1','sqrt2','sqrt3','sqrt6'],'pair_trace_type_count':len(ordered),
        'pair_trace_types':[[list(map(str,row))for row in typ]for typ in ordered],
        'bounded_exponent_witnesses':[witness.get(typ)for typ in ordered],
        'all_zero_included_for_unbounded_tail':True,'known_control':'pointed semion pair 1,i',
        'scope':'complete necessary pair trace domain; weights count pairs, hence sum to half the column multiplicity',
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();actual=compute();path=HERE/'semion_pair_traces.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'semion-pair receipt differs')
    print('PASS complete height-six semion-pair trace domain:',actual['pair_trace_type_count'],'types')
