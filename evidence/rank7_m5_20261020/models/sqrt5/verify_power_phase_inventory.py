#!/usr/bin/env python3
"""Independent Fraction/CRT replay of the power-of-two phase receipt.

Imports neither SymPy nor the phase generator. Also checks local higher-order
cancellation and source-fixed packet lengths beyond the receipt modulus.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import copy
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent
BASIS=['1','sqrt(5)','sqrt(2)','sqrt(10)','i','i*sqrt(5)','i*sqrt(2)','i*sqrt(10)']


def require(ok,why):
    if not ok:raise ValueError(why)


def multiply(a,b):
    out=[F(0)]*8
    for u,x in enumerate(a):
        for v,y in enumerate(b):
            overlap=u&v;factor=1
            for bit,square in ((1,5),(2,2),(4,-1)):
                if overlap&bit:factor*=square
            out[u^v]+=x*y*factor
    return tuple(out)


ONE=(F(1),)+(F(0),)*7
ZERO=(F(0),)*8
XI=(F(0),F(0),F(1,2),F(0),F(0),F(0),F(1,2),F(0))
XI_POWERS=[ONE]
for unused in range(7):XI_POWERS.append(multiply(XI_POWERS[-1],XI))
require(multiply(XI_POWERS[-1],XI)==ONE,'primitive eighth-root arithmetic')


def relative_five(e):
    e%=5
    if not e:return ONE
    sign=1 if e in (1,4) else -1
    return (F(-1,4),F(sign,4))+(F(0),)*6


def independent_moments(k,power):
    n2=2**(power+3)
    alpha=pow(5,-1,n2);beta=pow(n2,-1,5)
    answer=()
    for j in range(power+1):
        exponent=(alpha*k*2**j)%n2;den=n2//8
        two=ZERO if exponent%den else XI_POWERS[(exponent//den)%8]
        answer+=multiply(two,relative_five(beta*k*2**j))
    scaled=tuple(8*x for x in answer)
    require(all(x.denominator==1 for x in scaled),'independent denominator bound')
    return tuple(int(x) for x in scaled)


def source_square_packet(order):
    units=[u for u in range(order) if math.gcd(u,order)==1
           and (order%5!=0 or u%5 in (1,4))
           and (order%8!=0 or u%8 in (1,3))]
    return {u*u%order for u in units}


def verify(receipt):
    p=receipt['max_power'];M=40*2**p
    require(receipt['basis']==BASIS and receipt['scale']==8,'receipt field and scale')
    require(receipt['moments']==[2**j for j in range(p+1)],'moment powers')
    require(receipt['cyclotomic_modulus']==M and receipt['cyclotomic_degree']==16*2**p,'cyclotomic data')
    groups={}
    for k in range(M):groups.setdefault(independent_moments(k,p),[]).append(k)
    require(len(groups)==24+12*p and (0,)*(8*(p+1)) not in groups,'independent inventory count')
    records=receipt['phases'];require(len(records)==25+12*p,'receipt count')
    for rec in records[:-1]:
        row=tuple(rec['moments_scaled8']);require(row in groups,'receipt moment tuple')
        require(rec['exponents_modulus']==groups.pop(row),'complete exact exponent fiber')
        require(rec['exponents'+str(M)]==rec['exponents_modulus'],'named exponent alias')
        require(tuple(rec['scaled8'])==row[:16],'old moment interface')
        if p>=2:require(tuple(rec['fourth_scaled8'])==row[16:24],'fourth moment field')
        if p>=3:require(tuple(rec['eighth_scaled8'])==row[24:32],'eighth moment field')
        orders={M//math.gcd(M,k) for k in rec['exponents_modulus']}
        require(len(orders)==1 and rec['orders']==sorted(orders),'exact order provenance')
        order=next(iter(orders));a=0;t=order
        while t%2==0:a+=1;t//=2
        require(t in (1,5) and rec['fixed_row_multiple']==2**max(a-3,0),'finite source packet formula')
    require(not groups,'every CRT phase included')
    zero=records[-1]
    require(zero['moments_scaled8']==[0]*(8*(p+1)) and zero['orders']==[],'truezero record')
    require(zero['zero_semigroup']==[2**(p+1),5],'truezero semigroup')
    require(zero['actual_T_fixed_up_to_duality_zero_multiples']=={'five_part_1':2**(p+1),'five_part_5':2**(p+2),'five_part_at_least_25':10},'conditional truezero packet divisors')
    packet_controls=[]
    for a,b in ((3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(3,1),(4,1),(5,1),(6,1),(7,1),(3,2),(4,2),(5,2),(6,2),(3,3),(4,3)):
        order=2**a*5**b;actual=len(source_square_packet(order));expected=2**max(a-3,0)*5**max(b-1,0)
        require(actual==expected,'higher-order source packet control')
        packet_controls.append({'a':a,'b':b,'order':order,'packet_size':actual})
    # Direct cyclic coefficient cancellation, independent of all field bases.
    # For a>j+3, pairs of exponents differing by2^(a-1) cancel in Q(zeta_2^a).
    cancel2=0
    for a in range(4,11):
        n=2**a;subgroup=range(1,n,8)
        for j in range(p+1):
            if a<=j+3:continue
            coeff=[0]*n
            for u in subgroup:coeff[(u*2**j)%n]+=1
            require(all(coeff[e]==coeff[e+n//2] for e in range(n//2)),'higher2 exact cancellation')
            cancel2+=1
    # Principal5 action is already a union of Phi_(5^b) multiples.
    cancel5=0
    for b in range(2,5):
        n=5**b;step=n//5
        for j in range(p+1):
            coeff=[0]*n
            for u in range(1,n,5):coeff[(u*2**j)%n]+=1
            require(all(len({coeff[e+t*step] for t in range(5)})==1 for e in range(step)),'higher5 exact cancellation')
            cancel5+=1
    return {'status':'PASS','max_power':p,'modulus':M,'phase_count':len(records),'arithmetic':'independent Fraction CRT; no SymPy or generator import',
            'higher_order_packet_controls':packet_controls,'higher2_cancellation_controls':cancel2,'higher5_cancellation_controls':cancel5}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--max-power',type=int,default=3);args=parser.parse_args()
    path=HERE/f'power_{args.max_power}_moment_phases_certificate.json';record=json.loads(path.read_text());out=verify(record)
    altered=copy.deepcopy(record);altered['phases'][0]['moments_scaled8'][0]+=1
    try:verify(altered)
    except ValueError:out['altered_phase_control_rejected']=True
    else:raise ValueError('altered phase accepted')
    out.update(optimized_python=not __debug__,certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    target=HERE/f'power_{args.max_power}_phase_inventory_{"optimized" if not __debug__ else "normal"}.json'
    target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
