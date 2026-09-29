"""Replay and freeze the fourth continuation; preserve preceding campaigns."""
import argparse,hashlib,json,time
from concurrent.futures import ProcessPoolExecutor,as_completed
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KINDS={'general_fibonacci_subfield_rotation':'continuation_subcategory_projection',
       'general_ising_projection_rotation':'continuation_subcategory_projection',
       'general_cyclic_three_projection':'continuation_subcategory_projection',
       'general_half_e6_projection':'continuation_subcategory_projection'}

def replay(payload):
 rid,R,c=payload
 import scipy.optimize
 def forbidden(*a,**kw):raise RuntimeError('optimizer forbidden during exact fourth-continuation replay')
 scipy.optimize.linprog=scipy.optimize.milp=forbidden
 from check import verify
 started=time.monotonic();verify(R,c)
 return {'id':rid,'kind':c['kind'],'passed':True,'seconds':time.monotonic()-started,
         'optimized_python':not __debug__,'optimizer_disabled':True}

def main(jobs=3):
 from exact import require
 from release import ROUND4,ROUND3,CONTINUATION,ROUND2,load,build,continuation_records
 rows=json.load(open(ROOT/'data/census.json'));byid={r['id']:r for r in rows}
 domain=json.load(open(ROOT/'verification/round4/campaign_manifest.json'))
 require(len(domain['tensors'])==domain['input_count'] and [r['id'] for r in domain['tensors']]==domain['ids'],'invalid input manifest')
 require(all(byid[r['id']]['N']==r['N'] for r in domain['tensors']),'input tensor changed')
 prior=load(CONTINUATION)+load(ROUND2)+load(ROUND3)
 receipts=json.load(open(ROOT/'verification/round4/proof_sources.json'));selected=[]
 for source in receipts:
  path=ROOT/source['path'];obj=json.load(open(path));c=obj[source['field']] if source.get('field') else obj
  rid=source['id'];require(rid in domain['ids'],'new proof outside frozen domain')
  require(c['kind'] in KINDS,'unregistered fourth-continuation proof kind')
  selected.append({'id':rid,'m':byid[rid]['m'],'status':'excluded','stage':KINDS[c['kind']],
                   'certificate':c,'exact_checked':True,'source':source['path'],
                   'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 require(len({r['id'] for r in selected})==len(selected),'duplicate new proof')
 require(not({r['id'] for r in selected}&{r['id'] for r in prior}),'overlapping proof campaigns')
 selected.sort(key=lambda r:(r['m'],byid[r['id']]['index']))
 results=[]
 with ProcessPoolExecutor(max_workers=jobs) as pool:
  futures=[pool.submit(replay,(r['id'],byid[r['id']]['N'],r['certificate'])) for r in selected]
  for f in as_completed(futures):
   result=f.result();results.append(result);print(json.dumps(result),flush=True)
 for r in selected:require(hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest()==r['source_sha256'],'proof source changed during replay')
 ROUND4.write_text(''.join(json.dumps(r,separators=(',',':'))+'\n' for r in selected))
 combined=continuation_records(rows,verify_certificates=False)
 require(combined==prior+selected,'combined proof files differ')
 build(verified_continuation=combined)
 report={'passed':True,'optimized_python':not __debug__,'optimizer_disabled':True,'new_exclusions':len(selected),
         'new_ids':[r['id'] for r in selected],'jobs':jobs,'replays':sorted(results,key=lambda r:r['id']),
         'prior_continuation_certificates':len(prior),'prior_continuations_replayed':False,
         'prior_evidence':'verification/round3/release_replay.json and unchanged earlier source-bound reports',
         'certificate_file':str(ROUND4.relative_to(ROOT)),
         'certificate_sha256':hashlib.sha256(ROUND4.read_bytes()).hexdigest(),
         'ledger_sha256':hashlib.sha256((ROOT/'data/decisions.json').read_bytes()).hexdigest()}
 out=ROOT/'verification/round4/release_replay.json';out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--jobs',type=int,default=3);args=ap.parse_args()
 if args.jobs<1:ap.error('--jobs must be positive')
 main(args.jobs)
