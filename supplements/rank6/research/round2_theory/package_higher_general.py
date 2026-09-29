"""Replay a full composite with assertion removal and optimizers disabled."""
import argparse,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import stabilizer_rotation_higher as H
import scipy.optimize as so
p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('--pseudo',type=Path,required=True);p.add_argument('--reduction',type=Path);p.add_argument('--two-fp-values',action='store_true');a=p.parse_args()
def blocked(*args,**kw):raise RuntimeError('optimizer invoked during exact replay')
so.linprog=so.milp=so.minimize=blocked
H.farkas=H.cached_farkas=blocked;H.C.farkas=H.I.farkas=blocked
import higher_traces;higher_traces.farkas=blocked
R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==a.id)
record=json.load(open(a.pseudo));pseudo=record['certificate']
if a.two_fp_values:reduction={'kind':'two_fp_values'}
else:reduction=json.load(open(a.reduction))['certificate']
c={'kind':'general_stabilizer_rotation_higher','version':1,'scope':'general','reduction':reduction,'pseudo':pseudo}
start=time.monotonic();H.verify_general(R,c);elapsed=time.monotonic()-start
out={'id':a.id,'kind':c['kind'],'scope':'general','outcome':'general_excluded','certificate':c,'verification':{'assertions_disabled':not __debug__,'optimizers_disabled':True,'seconds':elapsed,'engine':'stabilizer_rotation_higher.verify_general'}}
q=ROOT/'research/round2_theory'/f'{a.id}_general.json';q.write_text(json.dumps(out,separators=(',',':'))+'\n')
number=a.id.removeprefix('R6_').replace('_','_');canonical=ROOT/'certificates'/f'stabilizer_rotation_{number}.json';canonical.write_text(json.dumps({'id':a.id,'certificate':c},separators=(',',':'))+'\n')
record['outcome']='pseudo_unitary_excluded';record['verification_seconds']=elapsed;a.pseudo.write_text(json.dumps(record,separators=(',',':'))+'\n')
print(json.dumps({'id':a.id,'general':'EXACT VERIFIED','seconds':elapsed,'canonical':str(canonical.relative_to(ROOT))}),flush=True)
