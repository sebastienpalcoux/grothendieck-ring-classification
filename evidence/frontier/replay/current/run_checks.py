#!/usr/bin/env python3
"""Replay curated exact checks in a temporary copy, leaving shipped files unchanged."""
from pathlib import Path
import argparse,gzip,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--include-native',action='store_true',help='also compile and run the optional finite C++ spectrum check')
 parser.add_argument('--receipt',type=Path,help='save the JSON run receipt outside this checks directory; always also prints it')
 args=parser.parse_args()
 if sys.version_info<(3,10):raise RuntimeError('Python 3.10 or later is required.')
 if not __debug__ or sys.flags.optimize:raise RuntimeError('Run ordinary Python without -O or -OO: several verifiers use assertions.')
 if args.receipt and (args.receipt.resolve()==ROOT or ROOT in args.receipt.resolve().parents):raise RuntimeError('--receipt must be outside the shipped checks directory.')
 manifest=json.loads((ROOT/'manifest.json').read_text())
 missing=[name for name in manifest['python_dependencies'] if importlib.util.find_spec(name) is None]
 if missing:raise RuntimeError('Missing Python dependencies: '+', '.join(missing)+'. Install these in your environment before running checks.')
 if args.include_native and not shutil.which('g++'):raise RuntimeError('--include-native requires g++ with C++17 support.')
 for rel,sha in manifest['files'].items():
  if not (ROOT/rel).is_file() or digest(ROOT/rel)!=sha:raise RuntimeError(f'Shipped-file digest mismatch: {rel}')
 checks=[c for c in manifest['checks'] if not c.get('optional_native') or args.include_native]
 receipt={'status':'RUNNING','scope':manifest['scope'],'python':sys.version.split()[0],'dependencies':{},'checked_input_files':len(manifest['files']),'run_mode':'temporary copy; shipped files untouched','checks':[]}
 for dep in manifest['python_dependencies']:
  module=__import__(dep);receipt['dependencies'][dep]=getattr(module,'__version__','available')
 started=time.monotonic()
 with tempfile.TemporaryDirectory(prefix='fusion-six-checks-') as temp:
  work=Path(temp)/'checks';shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  for rel,item in manifest.get('compressed_inputs',{}).items():
   raw=gzip.decompress((work/item['archive']).read_bytes())
   if len(raw)!=item['bytes'] or hashlib.sha256(raw).hexdigest()!=item['sha256']:
    raise RuntimeError('Expanded input digest mismatch: '+rel)
   target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
  env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONOPTIMIZE']='0';env['PYTHONHASHSEED']='0'
  for item in checks:
   print('Running '+item['name'],file=sys.stderr,flush=True);tick=time.monotonic()
   try:
    result=subprocess.run([sys.executable,'-B',str(work/item['script'])],cwd=work,env=env,capture_output=True,text=True,timeout=item.get('timeout_seconds',60))
    record={'name':item['name'],'script':item['script'],'status':'PASS' if result.returncode==0 else 'FAIL','returncode':result.returncode,'seconds':round(time.monotonic()-tick,3),'stdout':result.stdout,'stderr':result.stderr}
   except subprocess.TimeoutExpired as error:
    record={'name':item['name'],'script':item['script'],'status':'TIMEOUT','seconds':round(time.monotonic()-tick,3),'timeout_seconds':item.get('timeout_seconds',60)}
   record['receipts']={rel:digest(work/rel) for rel in item.get('receipts',[]) if (work/rel).is_file()}
   receipt['checks'].append(record)
   if record['status']!='PASS':break
  receipt['status']='PASS' if len(receipt['checks'])==len(checks) and all(r['status']=='PASS' for r in receipt['checks']) else 'FAIL'
 for rel,sha in manifest['files'].items():
  if digest(ROOT/rel)!=sha:raise RuntimeError(f'Shipped file changed unexpectedly: {rel}')
 receipt['shipped_files_unchanged']=True;receipt['seconds']=round(time.monotonic()-started,3)
 rendered=json.dumps(receipt,indent=2)+'\n'
 if args.receipt:
  args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(rendered)
 print(rendered,end='')
 return 0 if receipt['status']=='PASS' else 1
if __name__=='__main__':
 try:sys.exit(main())
 except (RuntimeError,ValueError,FileNotFoundError,json.JSONDecodeError) as error:
  print(f'ERROR: {error}',file=sys.stderr);sys.exit(2)
