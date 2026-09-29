import contextlib,hashlib,json,signal,sys,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
import round4_m8_ising as M
C={r['id']:r for r in json.load(open(P/'data/census.json'))};models=json.load(open(P/'data/model_catalog.json'));front=json.load(open(P/'verification/round4/campaign_manifest.json'))['tensors']
def stop(*a):raise TimeoutError('per-input 110 second budget')
signal.signal(signal.SIGALRM,stop);rows=[]
for typ,items in [('frontier',front),('positive_model',models)]:
 for rec in items:
  rid=rec['id'];R=C[rid]['N'];st=time.monotonic();o={'id':rid,'input_kind':typ,'tensor_sha256':hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest(),'ising_labels':[list(x) for x in M.ising_labels(R)]}
  if not o['ising_labels']:o.update(outcome='ineligible',reason='no Ising based subcategory')
  elif typ=='frontier':o.update(outcome='targeted_campaign',reason='proof or targeted bounded receipt recorded separately')
  else:
   signal.alarm(110)
   try:
    d=M.data_for(R,3,None)
    with open(P/f'research/round4/m8/ising_control_{rid}.log','w') as log,contextlib.redirect_stdout(log):q=M.run(R,3,d['F'],prepared=d)
    out=P/f'research/round4/m8/ising_control_{rid}.json';out.write_text(json.dumps(q,separators=(',',':'))+'\n');o.update(outcome=q['outcome'],metadata=q['metadata'])
    if q['outcome']=='pseudo_unitary_excluded':raise RuntimeError('known PU realization falsely excluded')
   except M.Ineligible as e:o.update(outcome='ineligible',reason=str(e))
   except TimeoutError as e:o.update(outcome='budget_incomplete',reason=str(e))
   finally:signal.alarm(0)
  o['seconds']=time.monotonic()-st;rows.append(o);print(rid,o['outcome'],o['seconds'],flush=True)
  (P/'research/round4/m8/ising_controls.json').write_text(json.dumps({'criterion':'Ising subcategory twist support and twist-resolved masses','rows':rows},indent=2)+'\n')
