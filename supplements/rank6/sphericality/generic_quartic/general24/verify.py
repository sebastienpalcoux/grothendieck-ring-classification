"""Exact conductor-24 checks for arbitrary distinct signed silver codegrees."""
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
from pathlib import Path
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT))
from verify_quartic_silver_fields import embedding_boxes, gap, propose, S
CS=(8,12,24)
CHAR=((1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))
FILE=HERE/'duals.json'
M=10**6

def sqrtup(x):
    x=F(x)
    return F(isqrt(x.numerator*S*S//x.denominator)+1,S)

def analytic():
    # Rational upper bounds for the radicals in the weighted Cauchy estimate.
    e = F(1,188)
    root3_half_lower = F(86602,100000)
    invroot12_upper = F(28868,100000)
    assert root3_half_lower**2 < F(3,4)
    assert invroot12_upper**2 > F(1,12)
    assert 2*invroot12_upper + 4*e < F(3,5)
    assert F(49,50)*F(2,5)**2 > F(5,36)
    square = F(4,3)*(F(3,4)-(1-4*e)*root3_half_lower+F(75,392))
    assert square < F(355,1000)**2
    assert 4*e + invroot12_upper + F(355,1000) < F(2,3)

def templates():
    out=[]
    z=(0,)*4;o=(1,)*4
    def add(p,q,v):
        out.append(([F(M*x).__floor__() for x in p],[F(M*x).__floor__() for x in q],F(M*v).__ceil__()))
    for s in (1,-1):
        h=[s]*4
        add(h,z,1 if s==1 else F(-63,100));add(z,h,1 if s==1 else F(-1,2))
    for i in range(1,4):
        w=[1,0,0,0];w[i]=-1
        add(w,z,0);add(z,w,0)
    for c,h in zip(CS,CHAR):
        rad=F(isqrt(c*S*S),S)
        for s in (-1,1):
            sign=[s*v for v in h]
            add(sign,z,sqrtup(F(gcd(c,2),c)));add(z,sign,sqrtup(F(gcd(c,4),c)))
            for k in range(-12,13):
                a=F(k,16);add([2*c*a*v for v in h],[rad*v for v in sign],2+c*a*a)
        if c==8:
            for a,b,d in product(range(-3,4),repeat=3):
                if gcd(gcd(a,b),d)!=1:continue
                rhs=sqrtup((F(a*a,2)+b*b+F(d*d,2))*(F(1,2)+F(2,144)))-F(11*d,12)
                add([a*v for v in h],[b*v-d for v in h],rhs)
    return out

def test(make):
    analytic()
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);fld=tmp/'fields';out=tmp/'ratios';exe=tmp/'list'
        fld.write_text('8 12 24 188\n')
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'quartic_more'/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(fld),str(out)],check=True)
        cases=[tuple(map(int,l.split()))[3:] for l in out.read_text().splitlines()]
    assert len(cases)==len(set(cases))==247
    dual={} if make else json.loads(FILE.read_text());base=templates()
    for x in cases:
        A=x[0];key=','.join(map(str,x));lo,hi=embedding_boxes(CS,x[:4])
        R=[[((p[i]*(lo[i] if p[i]>=0 else hi[i]))//M+q[i]*S//M) for i in range(4)] for p,q,b in base]
        B=[-(-b*S//M) for p,q,b in base]
        # The involution at index one fixes sqrt(2), giving Tr(q sigma(x)) >= s.
        R.append([lo[i]-hi[i^1] for i in range(4)])
        B.append(0)
        if make:
            dual[key]=propose(R,B)
        assert key in dual and dual[key] and gap(R,B,dual[key])>0,key
    assert len(dual)==len(cases)
    if make:
        FILE.write_text(json.dumps(dual,separators=(',',':'))+'\n')
    print('Verified the Cauchy height bound and all',len(cases),'conductor-24 ratios through trace 188.')
if __name__=='__main__':test('--make' in sys.argv)
