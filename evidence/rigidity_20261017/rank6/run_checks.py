#!/usr/bin/env python3
"""Verify the current rank-six necessary-condition evidence.

Default: integrity, prerequisite identities and both complete case replays.
--metadata-only: exact identities and status only, without arithmetic replay.
This checker does not resolve either categorification question.
"""
from pathlib import Path
import argparse, ast, hashlib, json, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def exact_file(path, item, label):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == item['sha256'], 'SHA256 mismatch: ' + label)
    if 'bytes' in item:
        require(len(raw) == item['bytes'], 'byte length mismatch: ' + label)

def metadata(repo):
    manifest = json.loads((HERE/'MANIFEST.json').read_text())
    require(manifest['schema'] == 'rank6-necessary-evidence-manifest/v1', 'manifest schema')
    for name, item in manifest['files'].items():
        exact_file(HERE/name, item, name)
    for binding in manifest['external_inputs']:
        path = repo/binding['path']
        if binding['kind'] == 'file':
            exact_file(path, binding, binding['path'])
        elif binding['kind'] == 'literal_assignment':
            tree = ast.parse(path.read_text())
            values = [ast.literal_eval(node.value) for node in tree.body
                      if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == binding['name'] for t in node.targets)]
            require(len(values) == 1, 'unique tensor assignment: '+binding['name'])
            raw = json.dumps(values[0], separators=(',', ':')).encode()
            require(hashlib.sha256(raw).hexdigest() == binding['sha256'], 'tensor identity: '+binding['name'])
        else:
            raise ValueError('unknown external binding type')
    progress = json.loads((HERE/'research_progress.json').read_text())
    require(progress['classification_counts'] == {'total':25421,'excluded':25362,'realized':57,'unresolved':2}, 'rank-six classification counts')
    require({c['id'] for c in progress['cases']} == {'R6_4_155','R6_8_1660'}, 'residual case domain')
    require(all(c['categorical_status']=='unresolved' and c['categorification_claimed'] is False
                for c in progress['cases']), 'necessary-condition scope')
    baseline = progress['prerequisite_manifest']
    require(progress['previous_coverage'] == baseline['path'] and progress['previous_coverage_sha256'] == baseline['sha256'], 'coverage-chain identity')
    exact_file(repo/baseline['path'], baseline, baseline['path'])
    return {'internal_files_checked':len(manifest['files']),
            'external_inputs_checked':len(manifest['external_inputs']),
            'prerequisite_manifest_sha256':baseline['sha256']}

def replay(repo, directory, script, output):
    command = [sys.executable] + ['-O']*sys.flags.optimize + [str(HERE/directory/script), '--repo', str(repo), '--output', str(output)]
    result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    require(result.returncode == 0, directory+' replay failed: '+result.stdout[-6000:])
    return json.loads(output.read_text())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=HERE.parents[2])
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        repo = args.repo.resolve()
        summary = metadata(repo)
        summary.update({'status':'PASS', 'scope':'Necessary conditions only; both rank-six cases remain unresolved.',
                        'mode':'metadata-only' if args.metadata_only else 'complete-replay',
                        'optimization_level':sys.flags.optimize})
        if not args.metadata_only:
            with tempfile.TemporaryDirectory(prefix='rank6-necessary-replay-') as td:
                a = replay(repo,'r155','verify_odd_clifford.py',Path(td)/'r155.json')
                b = replay(repo,'r1660','verify.py',Path(td)/'r1660.json')
                require(a['all_passed'] and a['checked_blocks']==1144, 'R155 complete odd domain')
                require(a == json.loads((HERE/'r155/odd_clifford_receipt.json').read_text()), 'R155 bound receipt equality')
                require(b['status']=='PASS' and b['conjugate_choices']==2 and b['phase_masses_per_conjugate']==288, 'R1660 phase domain')
                require(b['independent_fourier_audit']['status']=='PASS', 'independent Fourier audit')
                require(b['phase_gram_audit']['status']=='PASS' and b['phase_gram_audit']['total_survivors']==640, 'R1660 complete restriction domain')
                require(b['optimized_python'] == bool(sys.flags.optimize), 'child optimization propagation')
                summary['case_replays'] = {'R6_4_155':{'odd_blocks':1144,'controls_rejected':len(a['negative_controls_rejected'])},
                                           'R6_8_1660':{'phase_masses_per_choice':288,'conjugate_choices':2,'restriction_profiles':640,
                                                         'controls_rejected':len(b['negative_controls'])}}
    except Exception as exc:
        summary = {'status':'FAIL','error':str(exc)}
    encoded = json.dumps(summary,indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    print(encoded,end='')
    return 0 if summary['status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
