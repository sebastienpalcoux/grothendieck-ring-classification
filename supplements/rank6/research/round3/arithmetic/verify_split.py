import copy,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize
scipy.optimize.linprog=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('optimizer forbidden'))
scipy.optimize.milp=scipy.optimize.linprog
from round3_split_arithmetic import hypotheses,arithmetic,certificate,verify,reduction,verify_reduction
from induction import pseudo_certificate
from rings import permute
from exact import VerificationError,require
rows=json.load(open(P/'data/census.json'));byid={r['id']:r for r in rows};R=byid['R6_8_6526']['N'];start=time.monotonic()
c=certificate(R,pseudo_certificate(R));require(c is not None,'missing general exclusion');verify(R,c)
(P/'research/round3/arithmetic/R6_8_6526_general.json').write_text(json.dumps(c,indent=2)+'\n')
Rp=permute(R,[0,5,3,1,4,2]);r=reduction(Rp);require(r is not None,'lost permuted reduction');verify_reduction(Rp,r)
corruptions=[]
for label,alter in [('local_rank',lambda b:b['reduction']['arithmetic']['hypotheses']['local_factors'][0].__setitem__('rank',99)),('quartic_candidate',lambda b:b['reduction']['arithmetic']['cyclic_quartic'][0]['cases'][0]['positive_candidates'].pop()),('sextic_norm',lambda b:b['reduction']['arithmetic']['sextic'].__setitem__('cubic_norm_lower_bound',1)),('signed_table',lambda b:b['reduction']['signed_tables'].clear())]:
 b=copy.deepcopy(c);alter(b)
 try:verify(R,b)
 except VerificationError:corruptions.append(label)
 else:raise RuntimeError('accepted corruption '+label)
positive=[]
for m in json.load(open(P/'data/model_catalog.json')):
 h=hypotheses(byid[m['id']]['N']);require(h is None,'positive model has excluded profile');positive.append({'id':m['id'],'applicable':False,'excluded':False})
eligible=[]
for row in rows:
 h=hypotheses(row['N'])
 if h is not None:eligible.append({'id':row['id'],'hypotheses':h})
report={'passed':True,'optimized':not __debug__,'optimizer_disabled':True,'seconds':time.monotonic()-start,'general_exclusion':'R6_8_6526','permutation_checked':[0,5,3,1,4,2],'corruptions_rejected':corruptions,'positive_models_checked':len(positive),'positive_controls':positive,'census_checked':len(rows),'census_applicable':eligible}
(P/f"research/round3/arithmetic/split_verification{'_optimized' if not __debug__ else ''}.json").write_text(json.dumps(report,indent=2)+'\n')
print('passed',report['seconds'],'census applicable',[z['id'] for z in eligible],flush=True)
