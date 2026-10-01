"""Replay exact necessary conditions for the two unresolved rank-six rings.

Use --list for canonical commands, --select R6_4_155 for one case, or
--check-receipts for a hash/predicate audit without mathematical replay.
Every command has an independent 15-minute deadline. A timeout proves nothing.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
COVERAGE = ROOT / 'research/frontier/coverage.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path):
    """Read a JSON receipt or explicit dictionaries printed in a replay log."""
    raw = path.read_text()
    try:
        data = json.loads(raw)
        return [data] if isinstance(data, dict) else []
    except json.JSONDecodeError:
        found, cursor = [], 0
        decoder = json.JSONDecoder()
        while True:
            match = re.search(r'(?m)^[ \t]*\{',raw[cursor:])
            if match is None:
                break
            begin = cursor+match.end()-1
            endline = raw.find('\n',begin)
            if endline<0:
                endline=len(raw)
            try:
                data, length = decoder.raw_decode(raw[begin:])
                cursor = begin+length
            except json.JSONDecodeError:
                cursor = endline+1
                try:
                    data = ast.literal_eval(raw[begin:endline])
                except (ValueError, SyntaxError):
                    continue
            if isinstance(data,dict):
                found.append(data)
        return found


def matches(value, predicate):
    return all(key in value and type(value[key]) is type(expected)
               and value[key] == expected for key, expected in predicate.items())


def receipt_ok(path, predicate):
    if not path.exists():
        return False
    found = records(path)
    return bool(found) and matches(found[-1], predicate)


def embedded_hashes(path):
    """Only formats actually used by the retained exact receipts are read."""
    result = {}
    for value in records(path):
        for key in ('source_sha256', 'sources_sha256', 'inputs_sha256', 'files_sha256', 'files', 'sources', 'inputs'):
            mapping = value.get(key)
            if isinstance(mapping, dict):
                result.update(mapping)
        for name, digest in value.get('output_sha256', {}).items():
            result[str((path.parent/name).relative_to(ROOT))] = digest
        if isinstance(value.get('source_sha256'), str) and value.get('source') and '://' not in value['source']:
            result[value['source']] = value['source_sha256']
        if value.get('native_source') and value.get('native_source_sha256'):
            result[value['native_source']] = value['native_source_sha256']
        if value.get('certificate') and value.get('certificate_sha256'):
            result[str((path.parent/value['certificate']).relative_to(ROOT))] = value['certificate_sha256']
    return result


def audit(entry, binding_check=None):
    issues = []
    binding = entry.get('binding', {})
    if binding.get('status') != 'frozen':
        issues.append('Source bindings remain pending: ' + binding.get('reason', 'not frozen'))
    check = binding_check or (lambda name, expected: (ROOT/name).exists() and sha(ROOT/name) == expected)
    frozen = binding.get('files_sha256', {})
    if not frozen:
        issues.append('No frozen file inventory')
    for name, expected in frozen.items():
        path = ROOT/name
        if not check(name, expected):
            issues.append('Frozen file mismatch: ' + name)
    receipts = []
    for receipt in entry.get('retained_receipts', []):
        path = ROOT/receipt['path']
        passed = receipt_ok(path, receipt['predicate'])
        if not passed:
            issues.append('Receipt predicate failed: ' + receipt['path'])
        source_issues = []
        if path.exists():
            for name, digest in embedded_hashes(path).items():
                item = ROOT/name
                if not check(name, digest):
                    source_issues.append(name)
            issues.extend('Embedded receipt hash mismatch: ' + name for name in source_issues)
        receipts.append(dict(path=receipt['path'],predicate_passed=passed,
                             embedded_hash_mismatches=source_issues))
    if not receipts:
        issues.append('No retained replay receipt')
    return dict(id=entry['id'],passed=not issues,mathematical_replay_performed=False,
                frozen_files_checked=len(frozen),receipts=receipts,issues=issues,
                source_binding_scope=binding.get('scope'))


def run_entry(entry, destination, timeout):
    start = time.monotonic()
    result = dict(id=entry['id'],passed=False,mathematical_replay_performed=True,steps=[])
    if entry.get('replay_status') == 'pending':
        result['reason'] = entry.get('pending_reason', 'Canonical replay command pending')
        return result
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    case_dir = destination/entry['id']
    case_dir.mkdir(parents=True, exist_ok=True)
    for index, step in enumerate(entry['commands']):
        log = case_dir/f'{index+1:02d}.log'
        argv = [sys.executable, '-O'] + step['argv']
        expected = {name:sha(ROOT/name) for name in entry.get('protected_files', [])}
        retained = {r['path']:(ROOT/r['path']).read_bytes()
                    for r in entry.get('retained_receipts', [])
                    if r['path'] not in expected and (ROOT/r['path']).exists()}
        started = time.monotonic()
        item = dict(argv=['python','-O']+step['argv'],log=str(log.relative_to(ROOT)),passed=False)
        try:
            with log.open('w') as stream:
                proc = subprocess.run(argv,cwd=ROOT,env=env,stdout=stream,
                                      stderr=subprocess.STDOUT,timeout=timeout,check=False)
            item['returncode'] = proc.returncode
            if proc.returncode:
                item['reason'] = 'Verifier process returned a failure'
            else:
                receipt = ROOT/step['receipt'] if step.get('receipt') else log
                item['receipt'] = str(receipt.relative_to(ROOT))
                item['passed'] = receipt_ok(receipt,step.get('predicate',{'passed':True}))
                if not item['passed']:
                    item['reason'] = 'Required explicit completion predicate absent'
        except subprocess.TimeoutExpired:
            item['reason'] = 'Explicit per-command deadline; incomplete, no exclusion'
            item['timed_out'] = True
        except OSError as exc:
            item['reason'] = str(exc)
        finally:
            refreshed = []
            for name, original in retained.items():
                path = ROOT/name
                if not path.exists() or path.read_bytes() != original:
                    if path.exists():
                        saved = case_dir/f'{index+1:02d}.{path.name}'
                        saved.write_bytes(path.read_bytes())
                        refreshed.append(str(saved.relative_to(ROOT)))
                        if item.get('receipt') == name:
                            item['receipt'] = str(saved.relative_to(ROOT))
                    path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_bytes(original)
            if refreshed:
                item['fresh_receipts'] = refreshed
        changed = [name for name,digest in expected.items()
                   if not (ROOT/name).exists() or sha(ROOT/name)!=digest]
        if changed:
            item['passed'] = False
            item['protected_files_changed'] = changed
        item['seconds'] = round(time.monotonic()-started,3)
        result['steps'].append(item)
        print(json.dumps({'id':entry['id'],'step':index+1,'passed':item['passed'],
                          'seconds':item['seconds']}),flush=True)
        if not item['passed']:
            break
    result['passed'] = len(result['steps'])==len(entry['commands']) and all(s['passed'] for s in result['steps'])
    result['seconds'] = round(time.monotonic()-start,3)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--select',action='append',help='Comma-separated case IDs; repeatable')
    ap.add_argument('--list',action='store_true',help='Print canonical commands without running them')
    ap.add_argument('--general-reduction',help='Replay one declared inherited general reduction and print its exact receipt')
    ap.add_argument('--check-receipts',action='store_true',help='Hash/predicate audit only; no mathematical replay')
    ap.add_argument('--jobs',type=int,default=1,help='Independent cases in parallel (default 1)')
    ap.add_argument('--timeout',type=int,default=900,help='Per-command deadline in seconds (default/max 900)')
    ap.add_argument('--output',type=Path,help='Output directory under this package; default verification/current/frontier_TIMESTAMP')
    args = ap.parse_args()
    if args.jobs<1 or args.jobs>7 or args.timeout<1 or args.timeout>900:
        ap.error('jobs must be 1..7 and timeout 1..900')
    coverage = json.loads(COVERAGE.read_text())
    manifest_path = ROOT/coverage['input_manifest']
    if sha(manifest_path) != coverage['input_manifest_sha256']:
        ap.error('frozen input manifest hash mismatch')
    manifest = json.loads(manifest_path.read_text())
    from frontier_m9 import HistoricalBinding
    historical = HistoricalBinding(ROOT)
    historical.validate_inventory()
    if not historical.check(manifest['source_census'], manifest['source_census_sha256']):
        ap.error('frozen source census hash mismatch')
    census = {r['id']:r for r in json.loads((ROOT/manifest['source_census']).read_text())}
    for row in manifest['tensors']:
        raw = json.dumps(row['N'],sort_keys=True,separators=(',',':')).encode()
        if hashlib.sha256(raw).hexdigest()!=row['tensor_sha256'] or census[row['id']]['N']!=row['N']:
            ap.error('frozen tensor mismatch: '+row['id'])
    if manifest['ids'] != [e['id'] for e in coverage['cases']]:
        ap.error('coverage differs from the frozen current-input domain')
    if args.general_reduction:
        entry = next((e for e in coverage['cases'] if e['id']==args.general_reduction),None)
        if entry is None or not entry.get('general_reduction'):
            ap.error('no declared standalone general reduction for this case')
        import scipy.optimize
        def denied(*_a,**_kw):
            raise RuntimeError('numerical optimizer disabled for general reduction replay')
        scipy.optimize.linprog=scipy.optimize.milp=denied
        sys.path.insert(0,str(ROOT/'software'))
        import galois_pseudo_reduction as G
        spec=entry['general_reduction'];source=ROOT/spec['certificate']
        record=json.loads(source.read_text());payload=record[spec['payload_key']]
        result=G.verify(census[entry['id']]['N'],payload)
        if spec.get('expected_key') and result!=record[spec['expected_key']]:
            raise ValueError('inherited reduction summary changed')
        files={source,ROOT/manifest['source_census']}
        for module in list(sys.modules.values()):
            path=getattr(module,'__file__',None)
            if path:
                path=Path(path).resolve()
                if path.is_relative_to(ROOT) and path.suffix=='.py':
                    files.add(path)
        result.update(passed=True,optimizer_used=False,optimized_python=not __debug__,
                      source_sha256={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)})
        print(json.dumps(result,sort_keys=True))
        return
    entries = coverage['cases']
    selected = set(','.join(args.select).split(',')) if args.select else {e['id'] for e in entries}
    unknown = selected-{e['id'] for e in entries}
    if unknown:
        ap.error('unknown selections: '+', '.join(sorted(unknown)))
    entries = [e for e in entries if e['id'] in selected]
    if args.list:
        for entry in entries:
            print(entry['id']+': '+entry.get('replay_status','ready'))
            for step in entry['commands']:
                print('  '+' '.join(['python','-O']+step['argv']))
        return
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    out = (args.output or ROOT/'verification/current'/('frontier_'+stamp)).resolve()
    if not out.is_relative_to(ROOT):
        ap.error('--output must be inside the package')
    out.mkdir(parents=True,exist_ok=True)
    if args.check_receipts:
        results = [audit(entry, historical.check) for entry in entries]
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(run_entry,e,out,args.timeout):e['id'] for e in entries}
            results = [future.result() for future in as_completed(futures)]
        results.sort(key=lambda r:next(i for i,e in enumerate(entries) if e['id']==r['id']))
    report = dict(schema='rank6-frontier-replay/v1',passed=all(r['passed'] for r in results),
                  mode='retained_receipt_audit' if args.check_receipts else 'fresh_exact_frontier_replay',
                  mathematical_replay_performed=not args.check_receipts,
                  historical_binding=historical.report(),
                  whole_ring_decisions_changed=False,coverage_sha256=sha(COVERAGE),
                  results=results,scope='Only the selected necessary reductions and controls; no full-census replay.')
    target = out/'receipt.json';target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'passed':report['passed'],'mode':report['mode'],
                      'receipt':str(target.relative_to(ROOT))}))
    if not report['passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
