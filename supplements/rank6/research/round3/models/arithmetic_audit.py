#!/usr/bin/env python3
"""Small independent spectrum enumeration for the q=149 application."""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

def run():
    q,c,T = 149,9,6741
    out=[]
    for y in range(1,(T-5)//(c*q)+1):
        for x in range(-math.isqrt(q*y*y-1),math.isqrt(q*y*y-1)+1):
            if (x-y)%2:
                continue
            n=q*y*y-x*x
            if (4*q*y*y)%n:
                continue
            rem=1-Fraction(4*y,c*n)
            if rem<=0:
                continue
            content=math.gcd(c*(q*y-x)//2,c*x)
            # The original rational codegree is 9.
            if content%9:
                continue
            ds=[f for f in range(2,content+1) if content%f==0]
            for fs in itertools.combinations_with_replacement(ds,4):
                if sum(fs)+c*q*y>T:
                    continue
                if sum((Fraction(1,f) for f in fs),Fraction(0)) != rem:
                    continue
                out.append({'x':x,'y':y,'complementary':list(fs),
                            'signed_trace':c*q*y+sum(fs)})
    expected=[{'x':x,'y':5,'complementary':[9,9,9,9],'signed_trace':6741}
              for x in (-61,61)]
    if out != expected:
        raise ValueError('independent finite spectrum differs')
    return {'passed':True,'optimized':not __debug__,
            'method':'direct finite divisor four-tuples; no optimizer',
            'parameters':{'q':q,'c':c,'T':T},'spectra':out,
            'parity_filter_needed':False}

if __name__=='__main__':
    result=run()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
