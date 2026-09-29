import json,hashlib
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
rows={r['id']:r for r in json.load(open(P/'data/census.json'))}
report={'new_general_exclusions':[],'surviving_multiplicity_four':['R6_4_155','R6_4_629'],'controls':{},'scope':'General allocations require the complete exact replay; bounded scans remain inconclusive. no_exact_obstruction is a search outcome, not certified primal feasibility.'}
for rid,module in [('R6_4_211','round3_m4'),('R6_4_243','round3_verlinde')]:
 f=D/(rid+'_general.json');c=json.load(open(f));replay=json.load(open(D/(rid+'_exact_replay.json')))
 if not (replay['passed'] and replay['general'] and replay['optimized'] and replay['optimizer_used'] is False):raise RuntimeError('unverified general certificate')
 report['new_general_exclusions'].append({'id':rid,'certificate':str(f.relative_to(P)),'certificate_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'tensor_sha256':hashlib.sha256(json.dumps(rows[rid]['N'],separators=(',',':')).encode()).hexdigest(),'verifier':'software/'+module+'.py:verify_general','replay':replay})
for name,retry in [('scan_controls','retry_positive_controls'),('verlinde_controls','retry_verlinde_controls')]:
 x=json.load(open(D/(name+'.json')));rr={r['id']:r for r in x['records']};rp=D/(retry+'.json')
 if rp.exists():
  for r in json.load(open(rp))['records']:
   if r['outcome']=='no_exact_obstruction':rr[r['id']]={**rr[r['id']],**r,'followup':str(rp.relative_to(P))}
 report['controls'][name]={'original_records':len(x['records']),'positive_model':dict(Counter(r['outcome'] for r in rr.values() if r['input_kind']=='positive_model')),'frozen_frontier':dict(Counter(r['outcome'] for r in rr.values() if r['input_kind']=='frontier')),'positive_timeouts':[r['id'] for r in rr.values() if r['input_kind']=='positive_model' and r['outcome']=='budget_incomplete'],'errors':[r for r in rr.values() if r['outcome']=='error']}
 if report['controls'][name]['errors']:raise RuntimeError('control errors remain')
if (D/'probe_629_verlinde.json').exists():report['additional_R6_4_629_probe']=json.load(open(D/'probe_629_verlinde.json'))
report['relative_trace_controls']=json.load(open(D/'trace_formula_controls.json'))
report['mutation_controls']=json.load(open(D/'certificate_mutation_controls.json'))
(D/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k not in ['relative_trace_controls','mutation_controls']})
