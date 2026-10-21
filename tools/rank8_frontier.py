"""A separately replayed continuation of the immutable rank-eight M3 release."""
from collections import Counter
from copy import deepcopy
from pathlib import Path, PurePosixPath
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'evidence/rank8_frontier_20261021'
ACCEPTED = EVIDENCE + '/accepted.json'
RESEARCH_CHECKS = EVIDENCE + '/research_checks.json'
BASELINE_LEDGER = 'supplements/rank8/output/m3/ledger.json'
BASELINE_SHA256 = '5a68ab083eecbbd2522bf89015cf73d5efcc3ad654a40976f4c4649fe1106fe2'
BASELINE_REPLAYS = {
    'evidence/rank8_m3_20261021/pipeline/continuation_replay.json':
        '81c43d58b1ae4aa7887b128eafc1f9971dc5cae467c7600a6de9be7489bcf28e',
    'evidence/rank8_m3_20261021/pipeline/continuation_replay_optimized_invocation.json':
        'c2298d5ac971dfcb5dc0babe26dd8a838f91c42a62fa99743ca1f15bded4b6ea',
}
LEDGER = 'supplements/rank8/output/frontier_20261021/ledger.json'
ARCHIVE = 'supplements/rank8/release/rank8-certified-frontier-20261021.zip'
PUBLICATION = EVIDENCE + '/publication'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and p.as_posix() == name


def active(repo):
    return (Path(repo) / LEDGER).is_file()


def accepted(repo):
    repo = Path(repo)
    value = json.loads((repo / ACCEPTED).read_text())
    need(value['schema'] == 'rank8-frontier-accepted/v1', 'Frontier acceptance schema')
    need(value['baseline_ledger'] == BASELINE_LEDGER and
         value['baseline_ledger_sha256'] == BASELINE_SHA256, 'Frontier baseline identity')
    ids = [r['id'] for r in value['decisions']]
    need(len(ids) == len(set(ids)), 'Duplicate frontier decision')
    for row in value['decisions']:
        need(row['status'] == 'excluded', 'Unsupported new frontier outcome')
        certificate = row['certificate']
        need(certificate['scope'] == 'general_complex_fusion_category', 'General exclusion scope required')
        need(certificate['kind'] and certificate['verifiers'], 'Missing frontier proof or verifier')
        for name in [certificate['evidence'], certificate['proof'], *certificate['verifiers']]:
            need(safe_path(name) and name.startswith(EVIDENCE + '/') and (repo / name).is_file(),
                 'Missing or unsafe frontier evidence: ' + name)
    return value


def reconcile(repo):
    repo = Path(repo)
    raw = (repo / BASELINE_LEDGER).read_bytes()
    need(sha(raw) == BASELINE_SHA256, 'The published M3 baseline changed')
    baseline = json.loads(raw)
    rows = deepcopy(baseline)
    by_id = {r['id']: r for r in rows}
    manifest = accepted(repo)
    for decision in manifest['decisions']:
        row = by_id[decision['id']]
        need(row['id'].startswith('R8_3_') and row['multiplicity'] == 3 and row['status'] == 'unresolved',
             'Frontier may only decide an unresolved baseline M3 tensor')
        need(row['tensor_sha256'] == decision['tensor_sha256'], 'Frontier tensor identity')
        row['status'] = decision['status']
        row['criterion'] = decision['certificate']['kind']
        row['certificate'] = deepcopy(decision['certificate'])
        row['frontier_baseline_status'] = 'unresolved'
    changed = {d['id'] for d in manifest['decisions']}
    need(all(a == b for a, b in zip(baseline, rows) if a['id'] not in changed),
         'An unaccepted baseline record changed')
    counts = Counter(r['status'] for r in rows if r['multiplicity'] == 3)
    return rows, {'new_decisions': len(changed), 'resolved_ids': sorted(changed, key=lambda x: int(x.split('_')[-1])),
                  'counts': dict(counts), 'baseline_records_preserved': len(rows) - len(changed)}


def validate_ledger(repo):
    rows, report = reconcile(repo)
    path = Path(repo) / LEDGER
    need(path.is_file() and json.loads(path.read_text()) == rows, 'Current frontier ledger differs from accepted evidence')
    report.update(ledger=LEDGER, ledger_sha256=sha(path.read_bytes()),
                  accepted=ACCEPTED, accepted_sha256=sha((Path(repo) / ACCEPTED).read_bytes()),
                  baseline_ledger=BASELINE_LEDGER, baseline_ledger_sha256=BASELINE_SHA256,
                  evidence=EVIDENCE)
    return report


def commands(repo):
    names = []
    for row in accepted(repo)['decisions']:
        for script in row['certificate']['verifiers']:
            if script not in names:
                names.append(script)
    path = Path(repo) / RESEARCH_CHECKS
    if path.is_file():
        research = json.loads(path.read_text())
        need(research['schema'] == 'rank8-frontier-research-replays/v1', 'Research replay schema')
        for item in research['checks']:
            script = item['script']
            need(safe_path(script) and script.startswith(EVIDENCE + '/') and
                 (Path(repo) / script).is_file() and item['scope'], 'Research replay identity')
            if script not in names:
                names.append(script)
    return names


def baseline_inputs(repo):
    """Bind every inherited proof, data source and log to the frozen replays.

    The receipt identities come from the immutable M3 archive. Replaying the
    baseline with a custom output preserves these publication receipts. The
    same checks work after extraction, without requiring a nested old ZIP.
    """
    repo = Path(repo)
    bound = dict(BASELINE_REPLAYS)
    reports = []
    for (name, expected), lane in zip(BASELINE_REPLAYS.items(), ('normal', '-O')):
        raw = (repo / name).read_bytes()
        need(sha(raw) == expected, 'Frozen baseline replay receipt changed: ' + name)
        report = json.loads(raw)
        need(report['status'] == 'PASS' and report['receipt_scope'] == 'publication' and
             report['requested_optimization'] == lane and
             report['proof_interpreter_assertions_enabled'] is True,
             'Invalid baseline full replay lane: ' + name)
        for field in ('proof_source_sha256', 'source_manifests_sha256'):
            for path, digest in report[field].items():
                need(safe_path(path), 'Unsafe inherited baseline input: ' + path)
                need(path not in bound or bound[path] == digest, 'Conflicting baseline hash: ' + path)
                bound[path] = digest
        for section in report['sections']:
            path = section['log']
            need(section['status'] == 'PASS' and safe_path(path), 'Invalid baseline replay log')
            digest = section['log_sha256']
            need(path not in bound or bound[path] == digest, 'Conflicting baseline log hash: ' + path)
            bound[path] = digest
        reports.append(report)
    for field in ('ledger_digest', 'proof_source_sha256', 'source_manifests_sha256'):
        need(reports[0][field] == reports[1][field], 'Baseline replay lanes disagree: ' + field)
    need([r['section'] for r in reports[0]['sections']] ==
         [r['section'] for r in reports[1]['sections']], 'Baseline replay coverage differs')
    for path, digest in bound.items():
        target = repo / path
        need(target.is_file() and sha(target.read_bytes()) == digest,
             'Inherited baseline proof, source or log changed: ' + path)
    return bound


def source_inventory(repo):
    repo = Path(repo)
    inherited = baseline_inputs(repo)
    paths = {ACCEPTED, LEDGER, 'tools/rank8_frontier.py', 'tools/verify_rank8_frontier.py'}
    research = repo / RESEARCH_CHECKS
    if research.is_file():
        paths.add(RESEARCH_CHECKS)
        for name in json.loads(research.read_text()).get('dependencies', []):
            need(safe_path(name) and (repo / name).is_file(), 'Missing research dependency: ' + name)
            paths.add(name)
    for p in (repo / EVIDENCE).rglob('*'):
        if (p.is_file() and p.suffix in {'.py', '.cpp', '.h', '.hpp', '.json', '.md', '.tex', '.g', '.bib', '.log'}
                and '__pycache__' not in p.parts and 'publication' not in p.relative_to(repo / EVIDENCE).parts):
            paths.add(p.relative_to(repo).as_posix())
    current = {name: sha((repo / name).read_bytes()) for name in sorted(paths)}
    need(all(name not in current or current[name] == digest for name, digest in inherited.items()),
         'Frontier and inherited baseline inventories disagree')
    return dict(sorted({**inherited, **current}.items()))
