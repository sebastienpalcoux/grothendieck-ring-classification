"""Portable exact follow-up replay dispatcher; no writes without --output.

Full mode runs every manifest-listed mathematical checker sequentially.
Metadata mode checks all bindings and requires completed normal and optimized
full receipts for this exact manifest. Neither mode changes category decisions.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
PACKAGE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, required=True)
parser.add_argument('--metadata-only', action='store_true')
parser.add_argument('--output', type=Path)
args = parser.parse_args()
ROOT = args.root.resolve()


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def local(base, name):
    need(isinstance(name,str) and name and not Path(name).is_absolute(), 'Manifest paths must be relative')
    path = (base/name).resolve()
    need(path.is_relative_to(base), 'Manifest path escapes its root: '+name)
    need(path.is_file(), 'Missing bound file: '+name)
    return path


def read(path):
    return json.loads(path.read_text())


def validate_manifest(manifest):
    need(manifest.get('schema') == 1, 'Unsupported source manifest schema')
    for field,base in [('package_files',PACKAGE),('baseline_files',ROOT)]:
        entries = manifest.get(field)
        need(isinstance(entries,dict) and entries, 'Empty manifest section: '+field)
        for name,expected in sorted(entries.items()):
            need(digest(local(base,name)) == expected, 'Source hash mismatch: '+field+'/'+name)
    need('verify.py' in manifest['package_files'], 'Dispatcher must be source-bound')
    checks = manifest.get('checks')
    need(isinstance(checks,list) and checks, 'No mathematical replay checks')
    names = [check.get('script') for check in checks]
    need(len(names)==len(set(names)), 'Duplicate replay script')
    for check in checks:
        script=check['script']
        need(script in manifest['package_files'] and script.endswith('.py'), 'Unbound replay script: '+script)
        need(check.get('kind') in ('json_receipt','internal_replay','quartic_summary'), 'Unknown replay kind')
        if check['kind'] in ('json_receipt','internal_replay'):
            need(check.get('receipt') in manifest['package_files'], 'Replay receipt must be source-bound')
    baseline_manifest = manifest.get('baseline_source_manifest','evidence/rank8_frontier_20261021/publication/source_manifest.json')
    need(baseline_manifest in manifest['baseline_files'], 'Frozen baseline manifest must be bound')
    baseline_entries=read(local(ROOT,baseline_manifest))
    need(isinstance(baseline_entries,dict), 'Frozen baseline manifest must map paths to hashes')
    for name,expected in manifest['baseline_files'].items():
        if name!=baseline_manifest:
            need(baseline_entries.get(name)==expected, 'Input differs from frozen baseline manifest: '+name)
    return baseline_manifest,manifest['baseline_files'][baseline_manifest]


def small_summary(parsed):
    names=('status','cases','excluded','survived','pattern_exclusions','remaining_Gram_patterns',
           'coordinate_exclusions','additional_coordinate_exclusions','remaining_patterns',
           'quartic_total_excluded','new_exclusions_beyond_height6','combined_remaining_patterns')
    return {name:parsed[name] for name in names if name in parsed and isinstance(parsed[name],(str,int,bool))}


def validate_output(manifest):
    if args.output is None:
        return None
    target=args.output.resolve()
    protected={PACKAGE/'source_manifest.json'}
    protected.update(local(PACKAGE,name) for name in manifest['package_files'])
    protected.update(local(ROOT,name) for name in manifest['baseline_files'])
    need(target not in protected, 'Output would overwrite a source-bound file')
    for name,optimized in [('replay_normal.json',False),('replay_optimized.json',True)]:
        if target==(PACKAGE/'publication'/name).resolve():
            need(not args.metadata_only, 'Metadata cannot overwrite a canonical full receipt')
            need(bool(sys.flags.optimize) is optimized, 'Output targets the wrong canonical optimization lane')
    return target


def run_check(check):
    command=[sys.executable,'-B']
    if sys.flags.optimize:
        command.append('-O' if sys.flags.optimize==1 else '-OO')
    command += [str(local(PACKAGE,check['script'])),'--root',str(ROOT)]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE',None)
    completed=subprocess.run(command,cwd=PACKAGE,env=env,capture_output=True)
    need(completed.returncode==0, 'Checker failed: '+check['script']+'\n'+completed.stderr.decode(errors='replace')[-3000:])
    try:
        parsed=json.loads(completed.stdout)
    except Exception as error:
        raise RuntimeError('Checker did not return JSON: '+check['script']) from error
    kind=check['kind']
    receipt_hash=None
    if kind in ('json_receipt','internal_replay'):
        receipt=local(PACKAGE,check['receipt'])
        receipt_hash=digest(receipt)
        if kind=='json_receipt':
            need(parsed==read(receipt), 'Mathematical replay differs from primary receipt: '+check['script'])
        else:
            need(parsed.get('status')=='PASS','Independent replay did not report PASS: '+check['script'])
    else:
        need(parsed.get('control',{}).get('status')=='pass','Fourth-moment control failed')
        need(parsed.get('R721',{}).get('cases')==8,'Incomplete R721 fourth-moment domain')
        need(parsed.get('R721',{}).get('status')=='all_patterns_survive_with_unique_high_pair_coefficients','Unexpected R721 fourth-moment conclusion')
        need(parsed.get('R1154',{}).get('patterns')==1238 and parsed.get('R1154',{}).get('failures')==[], 'Incomplete scalar R1154 fourth-moment domain')
    result={'script':check['script'],'kind':kind,'status':'PASS',
            'stdout_sha256':hashlib.sha256(completed.stdout).hexdigest(),
            'summary':small_summary(parsed)}
    if receipt_hash is not None:
        result['stored_receipt']=check['receipt']
        result['stored_receipt_sha256']=receipt_hash
    return result


result={'schema':1,'optimized_python':bool(sys.flags.optimize),
        'mathematical_replay_performed':False,
        'scope':'Exact necessary center-data follow-up only; no categorical decision changes.'}
exit_code=0
output_path=None
try:
    manifest_path=PACKAGE/'source_manifest.json'
    manifest=read(manifest_path)
    manifest_hash=digest(manifest_path)
    baseline_path,baseline_hash=validate_manifest(manifest)
    output_path=validate_output(manifest)
    result.update(source_manifest_sha256=manifest_hash,
                  baseline_source_manifest=baseline_path,
                  baseline_source_manifest_sha256=baseline_hash)
    if args.metadata_only:
        lanes=[]
        for name,optimized in [('replay_normal.json',False),('replay_optimized.json',True)]:
            receipt=local(PACKAGE,'publication/'+name)
            value=read(receipt)
            need(value.get('status')=='PASS' and value.get('completed') is True, 'Incomplete full replay: '+name)
            need(value.get('mathematical_replay_performed') is True, 'Metadata cannot replace mathematics: '+name)
            need(value.get('optimized_python') is optimized, 'Wrong optimization lane: '+name)
            need(value.get('source_manifest_sha256')==manifest_hash, 'Stale full replay manifest: '+name)
            need(value.get('baseline_source_manifest_sha256')==baseline_hash, 'Stale frozen baseline binding: '+name)
            need([x.get('script') for x in value.get('checks',[])]==[x['script'] for x in manifest['checks']], 'Incomplete full replay commands: '+name)
            need(all(x.get('status')=='PASS' for x in value['checks']), 'Failed mathematical check: '+name)
            lanes.append({'receipt':'publication/'+name,'sha256':digest(receipt),'optimized_python':optimized})
        result.update(status='METADATA_PASS',completed=True,full_replays=lanes)
    else:
        checks=[run_check(check) for check in manifest['checks']]
        need(digest(manifest_path)==manifest_hash,'Source manifest changed during replay')
        validate_manifest(manifest)
        result.update(status='PASS',completed=True,mathematical_replay_performed=True,checks=checks)
except Exception as error:
    result.update(status='FAIL',completed=False,error=str(error))
    exit_code=1

serialized=json.dumps(result,indent=2)+'\n'
if output_path is not None:
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.write_text(serialized)
print(serialized,end='')
raise SystemExit(exit_code)
