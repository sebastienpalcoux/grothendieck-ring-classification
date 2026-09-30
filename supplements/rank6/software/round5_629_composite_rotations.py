"""Exact composite generalized rotations for the completed R6_4_629 center.

This invokes the common modular-check engine on frozen reconstruction data.
It does not construct a categorification.
"""
import argparse,json,time
from pathlib import Path
import sympy as s
from exact import require
from round5_629 import source_data
from round5_modular_checks import check_variant
from round5_quartic_pair import digest
ROOT=Path(__file__).resolve().parents[1]


def reconstruct():
    R,data,cols,lab,src=source_data();C=data['C'];here=ROOT/'research/round5/m4_629'
    f=json.loads((here/'rank35_fusion_data.json').read_text());mod=json.loads((here/'rank35_modular_completions.json').read_text());br=next(x for x in mod['branches'] if x['signs']==f['signs'])
    S=[[C([s.Rational(z) for z in vals]) for vals in row] for row in br['S']];ds=[z/S[0][0] for z in S[0]]
    decoded=json.loads((here/'decoded_twists.json').read_text());case=next(x for x in decoded if x['rank']==35 and x['solution']==0);W=list(cols);ee=[0]*len(cols)
    for o in case['orbits']:
        W.extend([(0,)+tuple(o['column'])]*o['copies']);ee.extend([15//o['root_order']*o['root_power']%15]*o['copies'])
    require(data['F']==15 and len(W)==35 and len(ee)==35,'wrong completed center')
    orders=[4,6,8,9,10,12,14,15,16];checks=check_variant(R,data,W,ds,S,ee,orders)
    return dict(kind='completed_center_composite_rotations',version=1,id='R6_4_629',source_sha256=dict(fusion=digest(f),modular=digest(mod),twists=digest(decoded)),checks=checks,categorification_claimed=False)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    if a.verify:
        import scipy.optimize
        def denied(*_,**__):raise RuntimeError('numerical optimizer disabled during replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied
    start=time.monotonic();cert=reconstruct()
    if a.verify:require(cert==json.loads(a.output.read_text()),'composite rotation certificate differs')
    else:a.output.write_text(json.dumps(cert,separators=(',',':'))+'\n')
    print(json.dumps(dict(passed=True,optimizer_used=False,orders=[x['order'] for x in cert['checks']['generalized_rotations']],seconds=time.monotonic()-start)),flush=True)
