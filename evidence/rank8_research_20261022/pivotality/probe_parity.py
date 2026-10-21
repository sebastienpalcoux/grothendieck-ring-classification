from pathlib import Path
import sys,json,itertools,time
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'evidence/rank8_frontier_20261021/review'))
import verify_nc_gate_unrestricted as u
census={r['id']:r for r in json.loads((ROOT/'evidence/rank8_m3_20261021/pipeline/census_m3.json').read_text())}
rid='R8_3_3472';R=census[rid]['tensor'];start=time.monotonic()
vals,p,stats=u.old.enumerate_all(R,timeout=180);print('enumerated',len(vals),stats,'seconds',time.monotonic()-start,flush=True)
a=u.old.ScalarCharacters(R);reports=[]
for i,v in enumerate(vals):
 T=u.old.from_values(R,p,v);u.old.validate_general(T);gauge=u.old.proofs.gauge_original(T,R)
 if gauge is not None:report={'kind':'gauge_original','signs':gauge}
 else:
  signed=u.old.ScalarCharacters(T);cc=u.old.character_obstructions(T,a.cf+signed.cf)
  report={'kind':'nongauge','characters':cc,'survivors':sum(c['obstruction'] is None for c in cc)}
 reports.append({'values':v,**report});print('class',i,report,flush=True)
out={'id':rid,'tensor_sha256':census[rid]['tensor_sha256'],'statistics':stats,'domains':p['domains'],'active':p['active'],'signed_values':vals,'branches':reports,'normalization':'positive_second_indicator_lifts_justified_by_FRS_parity'}
(HERE/(rid+'_parity_gate.json')).write_text(json.dumps(out,indent=2)+'\n');print('done',time.monotonic()-start,flush=True)
