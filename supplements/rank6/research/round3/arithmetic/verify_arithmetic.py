import copy,json,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import scipy.optimize
scipy.optimize.linprog=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('optimizer forbidden'))
scipy.optimize.milp=scipy.optimize.linprog
from round3_arithmetic import arithmetic,reduction,certificate,verify,verify_reduction
from rings import permute
from exact import VerificationError,require
rows=json.load(open(P/'data/census.json'));byid={r['id']:r for r in rows};reports=[]
for rid in ['R6_8_6524','R6_8_6525','R6_8_6999']:
 R=byid[rid]['N'];t=time.monotonic();pseudo=json.load(open(P/f'research/round3/arithmetic/{rid}_pseudo.json'))
 c=certificate(R,pseudo);require(c is not None,'missing general exclusion');verify(R,c)
 (P/f'research/round3/arithmetic/{rid}_general.json').write_text(json.dumps(c,indent=2)+'\n')
 p=[0,5,3,1,4,2];Rp=permute(R,p);rp=reduction(Rp);require(rp is not None,'permuted general reduction lost');verify_reduction(Rp,rp)
 bad=[]
 for label,change in [('local_rank',lambda b:b['reduction']['arithmetic']['hypotheses']['local_factors'][0].__setitem__('rank',99)),('omit_spectrum',lambda b:b['reduction']['arithmetic']['spectra'].pop()),('omit_sign_table',lambda b:b['reduction']['signed_tables'].clear()),('trace_bound',lambda b:b['reduction']['arithmetic'].__setitem__('signed_Casimir_lower_bound',0))]:
  b=copy.deepcopy(c);change(b)
  try:verify(R,b)
  except VerificationError:bad.append(label)
  else:raise RuntimeError('accepted alteration '+label)
 reports.append({'id':rid,'passed':True,'seconds':time.monotonic()-t,'permutation':p,'corruptions_rejected':bad})
 print(rid,'passed',flush=True)
positive=[]
for m in json.load(open(P/'data/model_catalog.json')):
 a=arithmetic(byid[m['id']]['N']);require(a is None or not a['excluded'],'positive model excluded')
 positive.append({'id':m['id'],'applicable':a is not None,'excluded':False})
report={'passed':True,'optimized':not __debug__,'optimizer_disabled':True,'general_exclusions':reports,'positive_models_checked':len(positive),'positive_controls':positive}
(P/f"research/round3/arithmetic/verification{'_optimized' if not __debug__ else ''}.json").write_text(json.dumps(report,indent=2)+'\n')
