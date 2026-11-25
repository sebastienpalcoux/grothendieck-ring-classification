"""Cyclic-16 equal half masses and saturated ordinary silver pair."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE.parents[1]/'generic_quartic'))
from sixteen import S,examples,conjugates,transform,template,gap,tryone

def main(generate=False):
    cert=HERE/'half_silver_duals.json';data=[] if generate else json.loads(cert.read_text());T=template(F(1,2),F(1,2));z=[0]*4
    for side in (0,1):
        for dir in (-1,1):
            v=[S*dir*(-1)**i for i in range(4)];T.append((v if side==0 else z,v if side==1 else z,0))
        u=[S]*4;T.append((u if side==0 else z,u if side==1 else z,S//2))
    ratios=examples(100);failed=[]
    for k,r in enumerate(ratios):
        x=conjugates(*r[:4]);R=transform(T,x)
        for j in range(1,4):
            R.append(([S-x[(i+j)%4][1] for i in range(4)],0))
            R.append(([S-(x[i][1]*x[(i+j)%4][1]+S-1)//S for i in range(4)],0))
        w=tryone(R) if generate else data[k]
        if generate:data.append(w)
        if not w:failed.append(r)
        else:assert gap(R,w)>0
    print('ratios',len(ratios),'unexcluded',failed,flush=True)
    if generate:cert.write_text(json.dumps(data,separators=(',',':'))+'\n')
    assert len(ratios)==len(data) and not failed
if __name__=='__main__':main('--generate' in sys.argv)
