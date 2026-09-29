"""Replay and freeze the third continuation without rewriting earlier campaigns."""
import argparse,hashlib,json,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KINDS={
 'c4_associator_stabilizer':'continuation_c4_associator',
 'inert_quadratic_pseudo_exclusion':'continuation_signed_spectrum',
 'inert_quadratic_signed_spectrum':'continuation_signed_spectrum',
 'split_quadratic_different_pseudo_exclusion':'continuation_signed_spectrum',
 'noncommutative_signed_exclusion':'continuation_noncommutative_spectrum',
 'general_stabilizer_rotation_higher':'continuation_stabilizer_rotation',
 'general_integral_morita_rotation':'continuation_integral_morita',
 'general_ambient_full_character_rotation':'continuation_ambient_character',
 'general_low_verlinde_restriction':'continuation_ambient_character',
}

def replay(payload):
 rid,R,c=payload
 import scipy.optimize
 def forbidden(*a,**kw):raise RuntimeError('optimizer forbidden during exact third-continuation replay')
 scipy.optimize.linprog=scipy.optimize.milp=forbidden
 from check import verify
 started=time.monotonic();verify(R,c)
 return {'id':rid,'kind':c['kind'],'passed':True,'seconds':time.monotonic()-started,
         'optimized_python':not __debug__,'optimizer_disabled':True}

def main(jobs=3):
 from exact import require
 from release import ROUND3,CONTINUATION,ROUND2,load,build,continuation_records
 rows=json.load(open(ROOT/'data/census.json'));byid={r['id']:r for r in rows}
 domain=json.load(open(ROOT/'verification/round3/campaign_manifest.json'))
 require(len(domain['inputs'])==domain['input_count'] and [r['id'] for r in domain['inputs']]==domain['input_ids'],'invalid input manifest')
 require(all(byid[r['id']]['N']==r['N'] for r in domain['inputs']),'input tensor changed')
 prior=load(CONTINUATION)+load(ROUND2)
 receipts=json.load(open(ROOT/'verification/round3/proof_sources.json'))
 selected=[]
 for source in receipts:
  path=ROOT/source['path'];obj=json.load(open(path));c=obj[source['field']] if source.get('field') else obj
  rid=source['id'];require(rid in domain['input_ids'],'new proof outside frozen domain')
  require(c['kind'] in KINDS,'unregistered third-continuation proof kind')
  selected.append({'id':rid,'m':byid[rid]['m'],'status':'excluded','stage':KINDS[c['kind']],
                   'certificate':c,'exact_checked':True,'source':source['path'],
                   'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 require(len({r['id'] for r in selected})==len(selected),'duplicate new proof')
 require(not({r['id'] for r in selected}&{r['id'] for r in prior}),'overlapping proof campaigns')
 selected.sort(key=lambda r:(list(dict.fromkeys(KINDS.values())).index(r['stage']),r['m'],byid[r['id']]['index']))
 results=[]
 with ProcessPoolExecutor(max_workers=jobs) as pool:
  futures=[pool.submit(replay,(r['id'],byid[r['id']]['N'],r['certificate'])) for r in selected]
  for f in as_completed(futures):
   result=f.result();results.append(result);print(json.dumps(result),flush=True)
 for r in selected:
  require(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['source_sha256'],'proof source changed during replay')
 ROUND3.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in selected))
 combined=continuation_records(rows,verify_certificates=False)
 require(combined==prior+selected,'combined proof files differ')
 ledger=build(verified_continuation=combined)
 report={'passed':True,'optimized_python':not __debug__,'optimizer_disabled':True,'new_exclusions':len(selected),
         'new_ids':[r['id'] for r in selected],'jobs':jobs,'replays':sorted(results,key=lambda r:r['id']),
         'prior_continuation_certificates':len(prior),'prior_continuations_replayed':False,
         'prior_evidence':'verification/round2/replay_optimized.json and original source-bound replay reports',
         'certificate_file':str(ROUND3.relative_to(ROOT)),
         'certificate_sha256':hashlib.sha256(ROUND3.read_bytes()).hexdigest(),
         'ledger_sha256':hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest()}
 out=ROOT/'verification/round3/release_replay.json';out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--jobs',type=int,default=3);args=ap.parse_args()
 if args.jobs<1:ap.error('--jobs must be positive')
 main(args.jobs)
