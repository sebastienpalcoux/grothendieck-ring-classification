"""Exact quartic conductor-24 exclusions at dimension-orbit mass at least 71/100."""
from fractions import Fraction as F
from math import gcd,isqrt
import json,sys,tempfile,subprocess
from pathlib import Path
from verify import HERE,ROOT,S,M,CS,CHARS,upperroot,materialize,propose


def constraints():
    rows=[];z=(0,)*4
    def add(p,q,b):
        rows.append(([F(M*v).__floor__() for v in p],[F(M*v).__floor__() for v in q],F(M*b).__ceil__()))
    add([1]*4,z,1);add(z,[1]*4,1);add(z,[-1]*4,F(-71,100))
    for i in range(1,4):
        v=[1,0,0,0];v[i]=-1;add(v,z,0);add(z,v,0)
    for c,h in zip(CS,CHARS):
        root=F(isqrt(c*S*S),S)
        for sg in (-1,1):
            add([sg*v for v in h],z,upperroot(F(gcd(c,2),c)))
            add(z,[sg*v for v in h],upperroot(F(gcd(c,4),c)))
            for k in range(-12,13):
                r=F(k,16);add([2*c*r*v for v in h],[sg*root*v for v in h],2+c*r*r)
    return rows


def exact(rs,weights):
    assert all(type(i) is int and 0<=i<len(rs) and type(w) is int and w>0 for i,w in weights)
    h=[sum(w*rs[i][0][k] for i,w in weights) for k in range(4)]
    return min(0,*h)>sum(w*rs[i][1] for i,w in weights)


def run(generate=False):
    sr2=upperroot(F(1,2));sr3=upperroot(F(1,3));t=F(71,100)
    assert F(51,1000)**2>(2-F(isqrt(8*S*S),S)*F(7,10))/8
    assert 1+4*F(1051,2000)/(t-sr2)+4/(t-sr3)<758
    with tempfile.TemporaryDirectory() as td:
        w=Path(td);exe=w/'enumerate';out=w/'ratios';fld=w/'field';fld.write_text('8 12 24 760\n')
        subprocess.run(['c++','-O3','-std=c++17',str(ROOT/'quartic_more'/'biquadratic.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(fld),str(out)],check=True)
        data=[tuple(map(int,l.split()))[3:] for l in out.read_text().splitlines()]
    assert len(data)==len(set(data))==1061
    rows=constraints();cert=HERE/'large_mass_duals.json';duals={} if generate else json.loads(cert.read_text())
    for r in data:
        rs=materialize(rows,r);key=','.join(map(str,r))
        if generate:duals[key]=propose(rs)
        assert exact(rs,duals[key]),r
    assert len(duals)==1061
    if generate:cert.write_text(json.dumps(duals,separators=(',',':'))+'\n')
    print('All 1061 ratios excluded at orbit mass at least 71/100.')


if __name__=='__main__':run('--generate' in sys.argv)
