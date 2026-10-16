#!/usr/bin/env python3
"""Replay the unified continuation and preserve the complete preceding release."""
from pathlib import Path
import argparse, collections, copy, hashlib, json, shutil, subprocess, sys, tempfile, zipfile

ROOT = Path(__file__).resolve().parents[1]
STAGE = 'evidence/unified_20261016'
MANIFEST_SHA256 = 'aea53af376ee1622554e969a3d178b0c42124abd8da3eadc08d62cc5ee5cd851'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def cd(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def run(root, relative, arguments=()):
    with tempfile.TemporaryDirectory(prefix='unified-receipt-') as directory:
        replacements = {'{repo}': str(root), '{output}': str(Path(directory) / 'receipt.json')}
        command = [sys.executable] + (['-O'] if sys.flags.optimize else [])
        command += [str(root / relative)] + [replacements.get(v, v) for v in arguments]
        result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    need(result.returncode == 0, relative + ' failed:\n' + result.stdout + result.stderr)
    report = json.loads(result.stdout)
    if isinstance(report, list):
        need(report and all(isinstance(item, dict) and item.get('status') == 'PASS'
                            for item in report), relative + ' has a failed case receipt')
        report = {'status': 'PASS', 'cases': report}
    need(report.get('status') == 'PASS', relative + ' did not report PASS')
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--historical', action='store_true')
    args = parser.parse_args()
    root = args.repo.resolve(); e = root / STAGE
    need(sha(e / 'source_files.json') == MANIFEST_SHA256, 'Frozen source manifest identity')
    for relative, digest in read(e / 'source_files.json').items():
        p = root / relative
        need(p.is_file() and sha(p) == digest, 'Source changed: ' + relative)
    decisions = read(e / 'decisions.json'); prior = read(e / 'previous_records.json')
    remaining = read(e / 'remaining_ids.json'); expected = read(e / 'expected_totals.json')
    need(decisions and len(decisions) == len({x['id'] for x in decisions}), 'Distinct nonempty decisions')
    need(all(x['scope'] == 'general_complex' and x['status'] in ('excluded', 'unitarily_realized')
             for x in decisions), 'Decision scope')
    restored = {}; totals = {}; baseline_open = set(); current_status = {}
    for rank, meta in prior['ranks'].items():
        rows = read(root / meta['ledger']); by = {x['id']: x for x in rows}
        changes = {x['id']: x for x in decisions if str(x['rank']) == rank}
        old = {x['id']: x for x in meta['previous_records']}
        need(len(rows) == len(by) == meta['records'], 'Census coverage')
        need(set(old) == set(changes) == set(meta['transitions']), 'Transition coverage')
        for rid, d in changes.items():
            row = by[rid]
            need(old[rid]['status'] == 'unresolved' and row['status'] == d['status'], 'Transition ' + rid)
            need(cd(row) == meta['transitions'][rid]['new_record_sha256'], 'Updated record ' + rid)
            stable = ('id', 'rank', 'multiplicity', 'source_line', 'commutative', 'tensor') if rank == '7' else ('id', 'multiplicity', 'index', 'tensor_sha256', 'commutative')
            need(all(row[k] == old[rid][k] for k in stable), 'Source identity ' + rid)
            need(row['certificate']['scope'] == 'general_complex' and
                 row['certificate']['proof'] == STAGE + '/' + d['proof'] and
                 row['certificate']['verifier'] == STAGE + '/' + d['verifier'], 'Proof binding ' + rid)
        need(cd([x for x in rows if x['id'] not in changes]) == meta['unchanged_records_sha256'], 'Unaffected records')
        historical = [copy.deepcopy(old.get(x['id'], x)) for x in rows]
        baseline_open.update(x['id'] for x in historical if x['status'] == 'unresolved')
        current_status.update({x['id']: x['status'] for x in rows})
        need(cd(historical) == meta['baseline_canonical_sha256'], 'Complete baseline ledger')
        need(cd([x for x in historical if x['status'] == 'excluded']) == meta['previous_negative_records_sha256'], 'Previous exclusions')
        need([x['id'] for x in rows if x['status'] == 'unresolved'] == remaining[rank], 'Remaining inventory')
        totals[rank] = dict(collections.Counter(x['status'] for x in rows))
        totals[rank].setdefault('unresolved', 0)
        need(totals[rank] == expected[rank], 'Current totals')
        restored[meta['ledger']] = historical
    coverage = read(e / 'all_cases.json')
    need(len(coverage) == len({r['id'] for r in coverage}) == len(baseline_open) == 38,
         'Complete original-case coverage')
    need({r['id'] for r in coverage} == baseline_open and
         all(r['previous_status'] == 'unresolved' and r['status'] == current_status[r['id']]
             for r in coverage), 'Coverage status agreement')
    model_path = 'supplements/rank8/data/model_catalog.json'
    models = read(root / model_path)
    new_models = {d['id'] for d in decisions if d['status'] == 'unitarily_realized' and d['rank'] == 8}
    need(len(models) == len({m['id'] for m in models}), 'Distinct model catalog')
    old_models = [m for m in models if m['id'] not in new_models]
    need(cd(old_models) == prior['rank8_previous_models_canonical_sha256'], 'Previous constructions unchanged')
    model_ids = {m['id'] for m in models}
    ledger8 = read(root / prior['ranks']['8']['ledger'])
    need(model_ids == {r['id'] for r in ledger8 if r['status'] == 'unitarily_realized'}, 'Complete model catalog')
    for m in models:
        if m['id'] not in new_models:
            continue
        d = next(d for d in decisions if d['id'] == m['id'])
        need(m['constructors'] and all(c.get('proof') == STAGE + '/' + d['proof'] for c in m['constructors']), 'Constructor proof')
        for c in m['constructors']:
            p = c['basis_map_source_to_model']; n = len(p)
            need(sorted(p) == list(range(n)), 'Constructor basis bijection')
            need(all(m['tensor'][i][j][k] == c['tensor'][p[i]][p[j]][p[k]]
                     for i in range(n) for j in range(n) for k in range(n)), 'Complete constructor tensor')
    model7_path = 'supplements/rank7/data/model_catalog.json'
    models7 = read(root / model7_path)
    new_models7 = {d['id'] for d in decisions if d['status'] == 'unitarily_realized' and d['rank'] == 7}
    old_models7 = [m for m in models7 if m['id'] not in new_models7]
    need(cd(old_models7) == prior['rank7_previous_models_canonical_sha256'], 'Previous rank-seven constructions unchanged')
    ledger7 = {r['id']: r for r in read(root / prior['ranks']['7']['ledger'])}
    need(len(models7) == len({m['id'] for m in models7}) and
         {m['id'] for m in models7} == {rid for rid, r in ledger7.items() if r['status'] == 'unitarily_realized'},
         'Complete rank-seven model catalog')
    for m in models7:
        if m['id'] not in new_models7:
            continue
        p = m['basis_permutation_model_to_census']; n = len(p)
        need(sorted(p) == list(range(n)) and p[0] == 0, 'Rank-seven constructor basis bijection')
        need(all(m['tensor'][i][j][k] == ledger7[m['id']]['tensor'][p[i]][p[j]][p[k]]
                 for i in range(n) for j in range(n) for k in range(n)), 'Complete rank-seven constructor tensor')
    replays = read(e / 'replay_manifest.json')
    need({STAGE + '/' + d['verifier'] for d in decisions} <= {r['script'] for r in replays}, 'Every decision replayed')
    reports = {r['script']: run(root, r['script'], r.get('arguments', [])) for r in replays}
    historical_status = 'not requested; exact parent files and ledgers preserved'
    if args.historical:
        with tempfile.TemporaryDirectory(prefix='unified-parent-') as directory:
            target = Path(directory) / 'repo'
            shutil.copytree(root, target, ignore=shutil.ignore_patterns(
                '.git', 'work', 'node_modules', '__pycache__', '*.pdf', '*.zip', '*.bin',
                '*.log', '*.aux', '*.out', '*.toc', '*.fls', '*.fdb_latexmk'))
            parent = read(e / 'parent_files.json')
            with zipfile.ZipFile(e / 'parent_files.zip') as archive:
                need(set(archive.namelist()) == set(parent), 'Parent file inventory')
                for relative, meta in parent.items():
                    raw = archive.read(relative)
                    need(len(raw) == meta['bytes'] and hashlib.sha256(raw).hexdigest() == meta['sha256'], 'Parent identity ' + relative)
                    p = target / relative; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(raw)
            for relative, rows in restored.items():
                (target / relative).write_text(json.dumps(rows, indent=2) + '\n')
            (target / model_path).write_text(json.dumps(old_models, indent=2) + '\n')
            (target / model7_path).write_text(json.dumps(old_models7, indent=2) + '\n')
            shutil.rmtree(target / STAGE)
            run(target, 'tools/verify_theoretical_20261016.py', ['--historical'])
            historical_status = 'PASS'
    print(json.dumps({
        'status': 'PASS', 'python_optimized': bool(sys.flags.optimize),
        'changed_records': len(decisions),
        'new_general_exclusions': sum(d['status'] == 'excluded' for d in decisions),
        'new_unitary_models': len(new_models) + len(new_models7), 'status_totals': totals,
        'previous_negative_records_unchanged': True, 'unaffected_records_unchanged': True,
        'previous_models_unchanged': True, 'complete_baseline_ledgers_reconstructed': True,
        'source_manifest_sha256': MANIFEST_SHA256,
        'exact_replays': {p: r['status'] for p, r in reports.items()},
        'historical_replay': historical_status,
        'scope': 'Proofs establish the stated general exclusions and constructions. Scoped reductions do not change other decisions.'
    }, indent=2))

if __name__ == '__main__':
    main()
