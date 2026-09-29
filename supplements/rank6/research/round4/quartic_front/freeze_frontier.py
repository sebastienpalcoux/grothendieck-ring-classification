import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'software'))
import round4_quartic_twists as T
import galois_pseudo_reduction as G
from exact import require
rid=sys.argv[1];root=Path(__file__).parent;R=next(r['N'] for r in json.load(open(ROOT/'data/census.json')) if r['id']==rid);profiles=json.load(open(root/(rid+'_profiles_certificate.json')))['certificate'];preliminary=next(x for x in json.load(open(ROOT/'research/round2_literature/quartic/modular_trace_scan.json')) if x['id']==rid);raw=json.load(open(root/(rid+'_profile_twists_probe.json')));cases=[]
for old in preliminary['branches']:
 if 'excluded' not in old or old['excluded']:continue
 ix=old['low'];lab=old['labelling'];ep=old['indicators'];br=profiles['branches'][ix];case=next(x for x in br['cases'] if x['labelling']==lab)
 for profile in case['survivors']:
  rec=next(x for x in raw if x['lab']==lab and x['profile_index']==profile['profile_index']);copy={k:v for k,v in rec.items() if k not in ('id','status','integer_status','exact')}
  if not any(k in copy for k in ('congruence','ray','variables')):
   copy['retained_without_exact_decision']=True
  copy.update(low=ix,indicators=ep);cases.append(copy)
record=dict(kind='quartic_profile_frontier',version=1,scope='general_necessary_profile_reduction',profiles=profiles,preliminary=preliminary,recognized_subcategories=T.recognize(R),cases=cases,categorification_claimed=False)
print('general reduction',rid,flush=True);reduction=G.certificate(R);require(reduction is not None,'general reduction unavailable');record['general_reduction']=reduction
print('start verify',rid,flush=True);started=time.monotonic();report=T.verify(R,record);report.update(seconds=time.monotonic()-started,id=rid)
(root/(rid+'_frontier_certificate.json')).write_text(json.dumps({'id':rid,'certificate':record},separators=(',',':'))+'\n');(root/(rid+'_frontier_replay.json')).write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
