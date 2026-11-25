"""Check all biquadratic fields containing sqrt(5) but neither sqrt(2) nor sqrt(3)."""
from itertools import permutations
from pathlib import Path
from tempfile import TemporaryDirectory
from math import isqrt
from fractions import Fraction
import subprocess,sys,json
from verify_quartic_fields import rows,solve,gap,conductor

BASE=Path(__file__).resolve().parent
CERT=BASE/'golden_biquadratic_duals.json'

def candidates():
    fields=set()
    for r in range(2,484):
        d,e=sorted([conductor(r),conductor(5*r)])
        if d>5 and d<484 and 8 not in (d,e) and 12 not in (d,e):
            fields.add((5,d,e,22))
    assert len(fields)==120
    with TemporaryDirectory() as tmp:
        p=Path(tmp)
        pairs=p/'fields'
        pairs.write_text(''.join('%d %d %d %d\n'%r for r in sorted(fields)))
        subprocess.run(['c++','-O3','-std=c++17',str(BASE.parent/'quartic_more/biquadratic.cpp'),'-o',str(p/'enum')],check=True)
        subprocess.run([str(p/'enum'),str(pairs),str(p/'alpha')],check=True)
        return [tuple(map(int,l.split())) for l in (p/'alpha').read_text().splitlines()]

def ordering(disc,coeff):
    scale=10**10
    scores=[]
    for sx,sy in ((1,1),(1,-1),(-1,1),(-1,-1)):
        low,high=0,0
        for c,k,sg in zip(coeff,disc,(sx,sy,sx*sy)):
            t=isqrt(k*scale*scale)
            low+=min(sg*c*t,sg*c*(t+1))
            high+=max(sg*c*t,sg*c*(t+1))
        scores.append((low,high))
    order=sorted(range(4),key=lambda i:scores[i][0])
    assert all(scores[i][1]<scores[j][0] for i,j in zip(order,order[1:]))
    return tuple(order.index(j^order[0]) for j in range(4))

if __name__=='__main__':
    gen='--generate' in sys.argv
    data=[] if gen else json.loads(CERT.read_text())
    gaps=[]
    cand=candidates()
    assert len(cand)==10
    for d,e,f,a,u,v,w,b,c,n in cand:
        j=ordering((d,e,f),(u,v,w))
        for mode in ('gold-long','gold-short'):
            R=rows((a,b,c,n),(d,e,f),j,mode)
            if gen:data.append(solve(R))
            gaps.append(gap(R,data[len(gaps)]))
    assert len(gaps)==len(data)==20 and min(gaps)>0
    if gen:CERT.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print('Ten golden biquadratic ratios; 20 certified exclusions. Least scaled margin',min(gaps))
