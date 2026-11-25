"""Exact interval and half-space certificates for irrational signed pairs at conductor 16."""
import json,sys
from pathlib import Path
from fractions import Fraction as F
from math import gcd,isqrt
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]/'generic_quartic'))
from sixteen import S,upper,conjugates,examples,template,transform,tryone,gap
Z=[0]*4;O=[1]*4;M=[-1]*4

def add(T,p,q,b):T.append(([(v*S).__floor__() for v in p],[(v*S).__floor__() for v in q],(S*b).__ceil__()))

def extra_ball(T,coeff,two):
    for a in range(-coeff,coeff+1):
        for b in range(-coeff,coeff+1):
            for h in range(0 if two==1 else 1,coeff+1):
                if gcd(gcd(a,b),h)!=1:continue
                add(T,[a*(-1)**i for i in range(4)],[b*(-1)**i-h for i in range(4)],upper(F(1,2)*(F(a*a,2)+b*b+F(h*h,two)))-h)

def base():
    T=template(F(1,2),F(1,2));add(T,Z,O,F(71,100));add(T,Z,[-2,0,-2,0],F(-2,94));add(T,Z,[0,-2,0,-2],F(-2,94));extra_ball(T,4,F(1));return T

def extended(typ,T):
    T=T.copy()
    if typ in ('half','short'):
        add(T,O,Z,F(1,2));add(T,Z,O,F(1,2));B=F(1,100) if typ=='half' else F(1,4)
    else:
        add(T,M,Z,F(-5,8));B=F(1,2)
    if typ=='scaled':
        add(T,Z,O,F(2,3));add(T,Z,M,F(-2,3));B=F(1,2)-F(1,9)
    for a in range(-5,6):
        for b in range(-5,6):
            if gcd(a,b)==1:add(T,[a*(-1)**i for i in range(4)],[b*(-1)**i for i in range(4)],upper(B*(F(a*a,2)+b*b)))
    if typ=='long':extra_ball(T,3,F(16,9))
    return T

def projections(T,x,typ):
    R=transform(T,x)
    for j in ((1,2,3) if typ in ('short','half') else (2,)):
        R.append(([x[i][0]-x[(i+j)%4][1] for i in range(4)],0))
        if typ=='short':R.append(([S-(x[i][1]*x[(i+j)%4][1]+S-1)//S for i in range(4)],0))
    return R

def height():
    e=F(1,1000); rtlow=F(isqrt(2*S*S),S)
    def bound(t,v):return 4*e+upper(max(F(0),2-2*rtlow*(t-4*e)))/2+upper(F(1,4)-v)
    bounds=[]
    for n in range(1,10000):
        for l in range(max(16,(29*n//100//8)*8),n//2+1,8):
            x=l*l-4*n
            if n*29>=100*l or l*l%n or x<=0 or x%8 or isqrt(x//8)**2!=x//8 or 4*x>n*n or (l,n)==(16,32):continue
            bounds.append(bound(1-F(l,n),F(x,n*n)))
    for i in range(500,710):bounds.append(bound(F(i,1000),(1-F(i+1,1000))**2-F(4,10000)))
    assert max(bounds)<F(5,8)
    assert len(bounds)==230
    ordinary=[]
    for n in range(1,257):
        for l in range(16,n//2+1,8):
            d=l*l-4*n
            if 8*l>3*n and l*l%n==0 and d>0 and d%8==0 and isqrt(d//8)**2==d//8 and 8*d<=n*n:ordinary.append((l,n))
    assert ordinary==[(16,32)]
    print('uniform adjacent-bound tests',len(bounds),'all below 5/8',flush=True)

def main(generate=False):
    cert=HERE/'irr_duals.json';data=[] if generate else json.loads(cert.read_text());T=base();ratios=examples(1000);stage=[];ex=0;idx=0
    def check(R):
        nonlocal idx,ex
        w=tryone(R) if generate else data[idx];idx+=1
        if generate:data.append(w)
        if w:assert gap(R,w)>0;ex+=1
        return bool(w)
    height()
    for r in ratios:
        x=conjugates(*r[:4]);R=projections(T,x,'generic')
        if not check(R):stage.append(r)
    last=[]
    for typ in ('short','half','scaled','long'):
        new=extended(typ,T)
        for r in stage:
            x=conjugates(*r[:4]);R=projections(new,x,typ)
            if not check(R):last.append((typ,r))
    assert len(ratios)==915 and len(stage)==12 and last==[('long',(24,8,5,2,36,16,2))],last
    typ,r=last[0];x=conjugates(*r[:4]);new=extended(typ,T);R=projections(new,x,typ)
    for q,b in ((O,F(51,100)),(M,F(-7,10))): # 0.51<t<0.70
        tmp=[];add(tmp,Z,q,b);assert check(R+transform(tmp,x))
    import sympy as sym
    X=sym.symbols('X');p=X**4-24*X**3+36*X**2-16*X+2
    assert sym.discriminant(p,X)==2**11*17**2
    # 1,x,sigma(x),sigma^2(x) on the integral basis (1,sqrt2,y,z)
    assert sym.Matrix([[1,0,0,0],[6,4,5,2],[6,-4,-2,5],[6,4,-5,-2]]).det()%17!=0
    assert 58**2-2*41**2==2
    print('verified',idx,'candidate tests,',ex,'strict certificates; last ratio excluded by the codifferent',flush=True)
    if generate:cert.write_text(json.dumps(data,separators=(',',':'))+'\n')
    assert len(data)==idx
if __name__=='__main__':main('--generate' in sys.argv)
