"""Rational separation certificates for equal masses at cyclic conductor sixteen."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'generic_quartic'))
from sixteen import S,examples,conjugates,transform,template,gap,tryone

def main(generate=False):
    cert=HERE/'nonhalf_duals.json';data=[] if generate else json.loads(cert.read_text());T=template(F(5,8),F(5,8));T.extend([([u*S]*4,[-u*S]*4,0) for u in (-1,1)])
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
    assert not failed
    if generate:cert.write_text(json.dumps(data,separators=(',',':'))+'\n')
    assert len(ratios)==len(data)
if __name__=='__main__':main('--generate' in sys.argv)
