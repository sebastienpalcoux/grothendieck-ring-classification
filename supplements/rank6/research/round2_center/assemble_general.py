"""Assemble the existing unrestricted reduction and new pseudo-unitary proof.

Both are then replayed by tensor-parametric generic verifiers; this packaging
step introduces no mathematical assumptions or census-dependent verifier rule.
"""
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
from stabilizer_rotation import verify_general
R=next(r['N'] for r in json.loads((ROOT/'data/census.json').read_text()) if r['id']=='R6_3_215')
pseudo=json.loads(Path(__file__).with_name('stabilizer_rotation_215.json').read_text())['certificate']
old=json.loads((ROOT/'research/new_frontier/frontier_spherical_reduction.json').read_text())
reduction={k:v for k,v in old.items() if k not in ('id','claim')};reduction.update(kind='galois_pseudo_reduction',version=1)
c={'kind':'general_stabilizer_rotation','version':1,'scope':'general','reduction':reduction,'pseudo':pseudo}
start=time.monotonic();report=verify_general(R,c)
record={'id':'R6_3_215','status':'excluded','scope':'general','certificate':c}
(ROOT/'certificates/stabilizer_rotation_215.json').write_text(json.dumps(record,separators=(',',':'))+'\n')
report.update(seconds=time.monotonic()-start)
Path(__file__).with_name('general_replay_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
