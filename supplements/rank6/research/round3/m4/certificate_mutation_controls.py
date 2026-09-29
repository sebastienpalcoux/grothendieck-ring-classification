import sys,json,copy,time
from pathlib import Path
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'software'))
from exact import VerificationError,require
import round3_m4 as A
import round3_verlinde as V
rows={r['id']:r for r in json.load(open(P/'data/census.json'))};out=[];st=time.monotonic()
for rid,mod in [('R6_4_211',A),('R6_4_243',V)]:
 c=json.load(open(Path(__file__).with_name(rid+'_general.json')))['certificate']['pseudo'];R=rows[rid]['N']
 for mutation in ['omitted_low_frame','omitted_indicator_case']:
  bad=copy.deepcopy(c)
  if mutation=='omitted_low_frame':bad['branches'].pop()
  else:next(b for b in bad['branches'] if b.get('cases'))['cases'].pop()
  try:mod.verify(R,bad)
  except VerificationError as e:out.append({'id':rid,'mutation':mutation,'rejected':True,'reason':str(e)})
  else:raise RuntimeError('incomplete certificate accepted')
report={'passed':True,'seconds':time.monotonic()-st,'controls':out};Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
