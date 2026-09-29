"""Independent exact audit of the quartic-field general exclusions.

Run under -O. Optimizer entry points are blocked before importing the proof
engine. The mathematical verifier reconstructs all induction and module data.
This file also runs deliberately invalid proof variants through that verifier.
"""
import argparse,copy,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'software'))
import scipy.optimize

def forbidden(*args,**kwargs):raise RuntimeError('optimizer called by exact quartic replay')
for name in ('linprog','milp','minimize','least_squares'):
 if hasattr(scipy.optimize,name):setattr(scipy.optimize,name,forbidden)
from exact import require,VerificationError
import cyclotomic_stabilizer_trace as C
from galois_pseudo_reduction import verify as verify_reduction
census={r['id']:r['N'] for r in json.loads((ROOT/'data/census.json').read_text())}
reports=[]
ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='*',default=['R6_4_258','R6_4_325']);ap.add_argument('--output',type=Path,default=Path(__file__).with_name('quartic_independent_audit_report.json'));args=ap.parse_args()

def rejected(name,checker,R,c):
 try:checker(R,c)
 except VerificationError as e:return {'mutation':name,'rejected':True,'reason':str(e)}
 raise RuntimeError('malformed quartic proof accepted: '+name)

for rid in args.ids:
 path=ROOT/'certificates'/('cyclotomic_stabilizer_'+rid+'.json')
 raw=path.read_bytes();record=json.loads(raw);require(record['id']==rid,'wrong external proof label')
 c=record['certificate'];R=census[rid];started=time.monotonic();report=C.verify_general(R,c)
 report.update(id=rid,optimized_python=not __debug__,optimizer_disabled=True,seconds=time.monotonic()-started,certificate_sha256=hashlib.sha256(raw).hexdigest())
 controls=[]
 q=copy.deepcopy(c);q['scope']='pseudo_unitary';controls.append(rejected('false_general_scope',C.verify_general,R,q))
 q=copy.deepcopy(c['reduction']);q['all_values'].pop();controls.append(rejected('omitted_unrestricted_signed_quotient',verify_reduction,R,q))
 q=copy.deepcopy(c['pseudo']);q['modules']['representations'].pop();controls.append(rejected('omitted_involution_module_branch',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);q['modules']['objects']=[];controls.append(rejected('missing_forced_stabilizer_objects',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);q['field']['order_bound']*=2;controls.append(rejected('altered_conductor_box',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);q['field']['trace_types']-=1;controls.append(rejected('omitted_relative_trace_type',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);q['field']['global_dimension_in_real_generator'][0]='987654321';controls.append(rejected('wrong_cyclotomic_dimension_embedding',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);q['branches'].pop();controls.append(rejected('omitted_low_induction_frame',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);bb=next(b for b in q['branches'] if b.get('cases'));bb['cases'].pop();controls.append(rejected('omitted_second_indicator_case',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);bb=next(b for b in q['branches'] if b.get('cases'));bb['cases'][0]['meta']['vectors']-=1;controls.append(rejected('altered_high_column_pruning_count',C.verify,R,q))
 q=copy.deepcopy(c['pseudo']);bb=next(b for b in q['branches'] if b.get('cases'));bb['cases'][0]['ray']=[0]*len(bb['cases'][0]['ray']);controls.append(rejected('zero_separating_vector',C.verify,R,q))
 report.update(mutation_controls=controls,all_mutations_rejected=True)
 reports.append(report)
 args.output.write_text(json.dumps({'reports':reports,'complete':len(reports)==len(args.ids)},indent=2)+'\n')
 print(json.dumps({'id':rid,'general_exclusion_verified':True,'optimized_python':not __debug__,'optimizer_disabled':True,'mutations_rejected':len(controls),'seconds_with_controls':time.monotonic()-started}),flush=True)
