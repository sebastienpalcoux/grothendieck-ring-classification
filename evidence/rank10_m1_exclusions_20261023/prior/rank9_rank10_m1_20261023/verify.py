#!/usr/bin/env python3
"""Replay accepted evidence in a temporary copy, leaving the release immutable."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,time,datetime
from pathlib import Path
if not __debug__:raise SystemExit('Run without -O: some inherited verifiers use assertions.')
ROOT=Path(__file__).resolve().parent
def require(value,message):
 if not value:raise RuntimeError(message)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest-only',action='store_true');args=parser.parse_args()
 manifest=json.load(open(ROOT/'manifest.json'))
 for name,expected in manifest['sha256'].items():
  path=ROOT/name;require(path.is_file(),'Missing release file: '+name)
  require(hashlib.sha256(path.read_bytes()).hexdigest()==expected,'Release hash mismatch: '+name)
 print('PASS release manifest:',len(manifest['sha256']),'files',flush=True)
 if args.manifest_only:return
 config=json.load(open(ROOT/'verification_plan.json'));ledger=json.load(open(ROOT/'deliverable/ledger.json'))
 logs=ROOT/'verification_logs';logs.mkdir(exist_ok=True);results=[];start=time.time()
 with tempfile.TemporaryDirectory(prefix='fusion_rank9_10_verify_')as temp:
  dest=Path(temp)
  for name in manifest['sha256']:
   to=dest/name;to.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,to)
  for step in config['steps']:
   begun=time.time();command=[sys.executable,step['script']]
   done=subprocess.run(command,cwd=dest,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
   (logs/(step['name']+'.log')).write_text(done.stdout)
   require(done.returncode==0,step['name']+' FAILED; see verification_logs/'+step['name']+'.log')
   results.append({'name':step['name'],'status':'PASS','seconds':round(time.time()-begun,3)})
   print('PASS',step['name'],flush=True)
  regenerated=json.load(open(dest/'deliverable/ledger.json'))
  old={r['id']:(r['status'],r['tensor_sha256_compact_json'])for r in ledger['records']}
  new={r['id']:(r['status'],r['tensor_sha256_compact_json'])for r in regenerated['records']}
  require(old==new and len(old)==336,'Ledger classifications or input identities changed on replay')
  require(ledger['counts']==regenerated['counts'],'Ledger counts changed on replay')
  for r in ledger['records']:
   require(not(r['exclusions']and r['models']),'Conflicting status: '+r['id'])
   for e in r['exclusions']+r['models']:
    require((ROOT/e['proof']).is_file(),'Missing proof: '+e['proof'])
    require((ROOT/e['certificate']).is_file(),'Missing certificate: '+e['certificate'])
 result={'status':'PASS','input_count':336,'counts':ledger['counts'],'steps':results,'total_seconds':round(time.time()-start,3),'manifest_sha256':hashlib.sha256((ROOT/'manifest.json').read_bytes()).hexdigest(),'python_version':sys.version.split()[0],'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Exact finite evidence replay plus cited mathematical proofs; not proof-assistant formalization.'}
 (ROOT/'verification_report.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS all 336 ledger entries; elapsed',result['total_seconds'],'seconds',flush=True)
if __name__=='__main__':main()
