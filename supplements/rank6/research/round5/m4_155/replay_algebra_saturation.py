"""Fresh exact replay and controls for the R155 unit-column necessary tests."""
import contextlib,hashlib,io,json,time
from pathlib import Path
import sympy as s
import scipy.optimize as op
def denied(*a,**k):raise RuntimeError('numerical optimizer forbidden in algebra saturation replay')
op.linprog=op.milp=denied
import algebra_saturation as A,fermion_saturation as F
from exact import require
P=Path(__file__).resolve().parents[3];here=Path(__file__).parent;st=time.monotonic()
controls={}
for name,M,expected in [('fibonacci',s.Matrix([[0,1],[1,1]]),'unit_saturation_survives'),('faithfulness_failure',s.diag(1,2),'noninjective_unit_column'),('integrality_failure',s.Matrix([[0,2],[2,1]]),'nonintegral_saturated_action'),('positivity_failure',s.Matrix([[0,1],[1,-1]]),'negative_positive_cone_action')]:
    r=A.check_pair(M,s.eye(2),0);require(r['reason']==expected,'unit-column control failed');controls[name]=expected
with contextlib.redirect_stdout(io.StringIO()):
    aa=A.calculate();ff=F.calculate()
require(aa==json.loads((here/'algebra_saturation.json').read_text()),'six-pair replay differs')
require(ff==json.loads((here/'fermion_saturation.json').read_text()),'fermion-action replay differs')
require(len(aa['cases'])==6 and all(c['passed'] and c.get('positive_cone_passed') for c in aa['cases']),'six low algebras do not pass')
actions=[a for c in ff['cases'] for a in c['actions']];require(len(actions)==48 and all(a['passed'] and a.get('positive_cone_passed') for a in actions),'forty-eight actions do not pass')
files=[here/name for name in ('replay_algebra_saturation.py','algebra_saturation.py','algebra_saturation.json','fermion_saturation.py','fermion_saturation.json','packet_frontier.json')]+[P/'data/census.json',P/'software/exact.py']
receipt=dict(passed=True,optimizer_used=False,optimized_python=not __debug__,scope='necessary_tests_on_six_low_matrix_pairs_and_all48_fermion_actions',controls=controls,low_algebra_dimension=8,fermion_algebra_dimension=9,profile_exclusions=0,elapsed_seconds=round(time.monotonic()-st,3),files={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(here/'algebra_saturation_replay_O.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt,flush=True)
