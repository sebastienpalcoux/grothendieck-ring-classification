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
SPECIAL=(16,52)
M=10**6

def sqrtup(x):
    x=F(x)
    return F(isqrt(x.numerator*S*S//x.denominator)+1,S)

def analytic():
    e=F(1,500);tested=[]
    for n in range(1,10000):
        for ell in range(16,n//2+1,8):
            d=ell*ell-4*n
            if ell*ell%n or d<=0 or d%8 or isqrt(d//8)**2!=d//8 or 4*d>n*n:continue
            t=1-F(ell,n)
            if (t-4*e)**2>F(1,3):continue
            if (ell,n)==(16,32):continue
            b=4*e+sqrtup(F(1,4)-F(d,n*n))+sqrtup(F(1,12))+sqrtup((2-F(3464,1000)*(t-4*e))/12)
            assert b<F(5,8);tested.append((ell,n))
    assert len(tested)==8
    for c in CS:
        for n in range(1,338):
            for ell in range(2*c,n,c):
                d=ell*ell-4*n
                if 100*ell<=37*n or ell*ell%n or d<=0 or d%c or isqrt(d//c)**2!=d//c or c*d>n*n:continue
                assert (c,ell,n) in ((8,16,32),(8,96,256)) and c*d==n*n

def templates():
    out=[]
    z=(0,)*4;o=(1,)*4
    def add(p,q,v):
        out.append(([F(M*x).__floor__() for x in p],[F(M*x).__floor__() for x in q],F(M*v).__ceil__()))
    for s in (1,-1):
        h=[s]*4
        add(h,z,1 if s==1 else F(-1,2));add(z,h,1 if s==1 else F(-1,2))
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
        fld.write_text('8 12 24 500\n')
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'quartic_more'/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(fld),str(out)],check=True)
        cases=[tuple(map(int,l.split()))[3:] for l in out.read_text().splitlines()]
    assert len(cases)==len(set(cases))==696
    dual={} if make else json.loads(FILE.read_text());base=templates();counts=[0,0,0]
    for x in cases:
        A=x[0];key=','.join(map(str,x));lo,hi=embedding_boxes(CS,x[:4])
        R=[[((p[i]*(lo[i] if p[i]>=0 else hi[i]))//M+q[i]*S//M) for i in range(4)] for p,q,b in base]
        B=[-(-b*S//M) for p,q,b in base]
        # h_l-s: l=1 fixes sqrt(2).
        h=[lo[i^1]-hi[i] for i in range(4)]
        neg=[lo[i]-hi[i^1] for i in range(4)]
        R.append(neg);B.append(0)
        def close(suffix,rr,bb):
            code=key+suffix
            if make:
                w=propose(rr,bb)
                if w is None:return False
                dual[code]=w
            if code not in dual:return False
            assert gap(rr,bb,dual[code])>0
            return True
        if close('',R,B):counts[0]+=1;continue
        assert x[:4] in [(16,5,4,3),(52,18,14,10)]
        assert close(' U',R+[[-v for v in hi]],B+[-63*S//100]);counts[1]+=1
        for k in range(A+1):
            assert close(' '+str(k),R+[lo,[-v for v in hi],h,neg],B+[5*S//8,-5*S//8,k*S,-k*S]);counts[2]+=1
    assert counts==[694,2,70] and len(dual)==sum(counts)
    if make:FILE.write_text(json.dumps(dual,separators=(',',':'))+'\n')
    print('Verified all 696 quartic ratios, including 70 shifted-moment cases.')
if __name__=='__main__':test('--make' in sys.argv)
