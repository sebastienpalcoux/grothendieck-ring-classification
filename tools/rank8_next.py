"""Accepted R721 model overlay on the immutable rank-eight frontier release.

The old ledgers, model catalogue, and research audit remain source snapshots.
Only the accepted R721 record changes a classification decision. Research
updates record stronger necessary conditions without changing their status.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import rank8_frontier as frontier

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'evidence/rank8_next_20261021'
ACCEPTED = EVIDENCE + '/accepted.json'
MODEL_MANIFEST = EVIDENCE + '/models/consolidated_models.json'
AUDIT = EVIDENCE + '/per_ring_research_audit.json'
BASELINE_LEDGER = frontier.LEDGER
BASELINE_LEDGER_SHA256 = 'bc63a1083e72b8ebf2a1a33b53b6046c0a2920a79b9f11c783b230c7cf5d7d83'
BASELINE_MODELS = 'supplements/rank8/output/m3/model_catalog.json'
BASELINE_MODELS_SHA256 = '9af4323bc5648f12081e1cae01271bc934301c921856daa1419e817a448d9a88'
BASELINE_AUDIT = frontier.EVIDENCE + '/structural_models/per_ring_research_audit.json'
LEDGER = 'supplements/rank8/output/next_20261021/ledger.json'
MODELS = 'supplements/rank8/output/next_20261021/model_catalog.json'
ARCHIVE = 'supplements/rank8/release/rank8-certified-next-20261021.zip'
PUBLICATION = EVIDENCE + '/publication'
REALIZED_STATUSES = {'unitarily_realized', 'pseudo_unitarily_realized'}
need, safe_path = frontier.need, frontier.safe_path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bound(repo, name, digest):
    need(safe_path(name), 'Unsafe overlay source: ' + name)
    raw = (Path(repo) / name).read_bytes()
    need(sha(raw) == digest, 'Overlay source changed: ' + name)
    return raw


def active(repo):
    return (Path(repo) / LEDGER).is_file()


def accepted(repo):
    repo = Path(repo)
    value = json.loads((repo / ACCEPTED).read_text())
    need(value['schema'] == 'rank8-next-accepted/v1', 'Overlay acceptance schema')
    need(value['baseline_ledger'] == BASELINE_LEDGER and
         value['baseline_ledger_sha256'] == BASELINE_LEDGER_SHA256,
         'Overlay frontier identity')
    need(value['baseline_models'] == BASELINE_MODELS and
         value['baseline_models_sha256'] == BASELINE_MODELS_SHA256,
         'Overlay inherited model identity')
    need(value['baseline_audit'] == BASELINE_AUDIT, 'Overlay inherited audit identity')
    for path, digest in value['source_sha256'].items():
        read_bound(repo, path, digest)
    need(value['model_manifest'] == MODEL_MANIFEST and MODEL_MANIFEST in value['source_sha256'],
         'Unbound accepted model manifest')
    records = json.loads((repo / MODEL_MANIFEST).read_text())
    need(len(records) == 1 and records[0]['id'] == 'R8_3_721', 'Only the reviewed R721 model is accepted')
    row = records[0]
    need(row['multiplicity'] == 3 and row['status'] == 'unitarily_realized' and
         row['model_scope'] == 'unitary' and row['unitary'] == row['pseudo_unitary'] == 'yes',
         'Accepted R721 model scope')
    tensor = row['tensor']
    need(sha(json.dumps(tensor, separators=(',', ':')).encode()) == row['tensor_sha256'],
         'Accepted model tensor digest')
    need(row['source_certificate'] in value['source_sha256'] and row['constructors'],
         'Unbound model verifier or missing constructor')
    for path, digest in row['evidence_sha256'].items():
        need(value['source_sha256'].get(path) == digest, 'Model evidence not accepted: ' + path)
    for constructor in row['constructors']:
        p, t = constructor['basis_map_source_to_model'], constructor['tensor']
        need(sorted(p) == list(range(8)), 'Invalid model basis map')
        need(all(t[p[i]][p[j]][p[k]] == tensor[i][j][k]
                 for i in range(8) for j in range(8) for k in range(8)),
             'Model full-tensor crosswalk differs')
    need(value['decisions'] == [{'id': row['id'], 'tensor_sha256': row['tensor_sha256'],
                                'status': row['status'], 'model': row['model']}],
         'Accepted decision differs from model certificate')
    need(value['baseline_audit_sha256'] == value['source_sha256'].get(BASELINE_AUDIT),
         'Unbound historical research audit')
    for updates in value['research_updates'].values():
        for update in updates:
            need(update['outcome'] and update['scope'] and update['limitation'], 'Unscoped research update')
            for field in ('evidence', 'verifiers'):
                for path in update.get(field, []):
                    need(path in value['source_sha256'], 'Unbound research update: ' + path)
    return value, records


def reconcile(repo):
    repo = Path(repo)
    manifest, new_models = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_LEDGER, BASELINE_LEDGER_SHA256))
    inherited = json.loads(read_bound(repo, BASELINE_MODELS, BASELINE_MODELS_SHA256))
    need(len(baseline) == 4500 and len(inherited) == 91, 'Historical overlay input coverage')
    rows = deepcopy(baseline)
    by_id = {r['id']: r for r in rows}
    for model in new_models:
        row = by_id[model['id']]
        need(row['multiplicity'] == 3 and row['status'] == 'unresolved' and
             row['tensor_sha256'] == model['tensor_sha256'], 'Overlay must realize the exact unresolved tensor')
        row.update(status=model['status'], models=[model['model']], model_source=MODEL_MANIFEST,
                   next_baseline_status='unresolved')
    changed = {r['id'] for r in new_models}
    need(all(a == b for a, b in zip(baseline, rows) if a['id'] not in changed),
         'Unaccepted historical record changed')
    models = deepcopy(inherited) + deepcopy(new_models)
    need(len({r['id'] for r in models}) == len(models), 'Duplicate overlay model')
    need([r for r in models if r['id'] not in changed] == inherited, 'Inherited models changed')
    counts = Counter(r['status'] for r in rows if r['multiplicity'] == 3)
    need(counts == Counter(excluded=3504, unitarily_realized=15, unresolved=8), 'Unexpected overlay counts')
    positives = {r['id']: r['status'] for r in rows
                 if r['multiplicity'] == 3 and r['status'] in REALIZED_STATUSES}
    need({r['id']: r['status'] for r in models if r['multiplicity'] == 3} == positives,
         'Overlay models and ledger differ')
    report = dict(new_decisions=len(changed), resolved_ids=sorted(changed), counts=dict(counts),
                  baseline_records_preserved=len(rows)-len(changed), inherited_models_preserved=len(inherited))
    return rows, models, report


def reconcile_audit(repo):
    repo = Path(repo)
    manifest, new_models = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_AUDIT, manifest['baseline_audit_sha256']))
    result = deepcopy(baseline)
    result['schema'] = 'rank8-next-per-ring-research-audit/v1'
    result['baseline_audit'] = BASELINE_AUDIT
    result['baseline_audit_sha256'] = manifest['baseline_audit_sha256']
    result['accepted_new_models'] = 1
    result['remaining_unresolved'] = 8
    by_id = {m['id']: m for m in new_models}
    need(len(result['rows']) == len({r['id'] for r in result['rows']}) == 34,
         'Original research audit coverage changed')
    need(set(manifest['research_updates']) <= {r['id'] for r in result['rows']},
         'Research update refers to an unknown historical row')
    for row in result['rows']:
        row['latest_completed'] = deepcopy(manifest['research_updates'].get(row['id'], []))
        if row['id'] in by_id:
            model = by_id[row['id']]
            row.update(general_status=model['status'], categorification_or_novelty_proved=True,
                       categorification_proved=True, novelty_proved=False,
                       screening_stage='unitarily_realized', accepted_model=model['model'],
                       model_source=MODEL_MANIFEST)
    for path, digest in manifest['source_sha256'].items():
        need(path not in result['artifact_sha256'] or result['artifact_sha256'][path] == digest,
             'Inherited research source hash conflict: ' + path)
        result['artifact_sha256'][path] = digest
    return result


def validate_ledger(repo):
    repo = Path(repo)
    rows, models, report = reconcile(repo)
    for name, value in ((LEDGER, rows), (MODELS, models), (AUDIT, reconcile_audit(repo))):
        path = repo / name
        need(path.is_file() and json.loads(path.read_text()) == value,
             'Published overlay differs from accepted evidence: ' + name)
    report.update(ledger=LEDGER, ledger_sha256=sha((repo/LEDGER).read_bytes()),
                  models=MODELS, models_sha256=sha((repo/MODELS).read_bytes()),
                  accepted=ACCEPTED, accepted_sha256=sha((repo/ACCEPTED).read_bytes()),
                  baseline_ledger=BASELINE_LEDGER, baseline_ledger_sha256=BASELINE_LEDGER_SHA256,
                  attempts_source=AUDIT, evidence=EVIDENCE)
    return report


def validate(repo):
    """Publication-facing alias; validates the ledger, models, and audit."""
    return validate_ledger(repo)


def commands(repo):
    value, _ = accepted(repo)
    return list(value['verifiers'])


def source_inventory(repo):
    repo = Path(repo)
    inherited = frontier.source_inventory(repo)
    manifest, _ = accepted(repo)
    paths = {ACCEPTED, LEDGER, MODELS, AUDIT, 'tools/rank8_next.py'}
    paths.update(manifest['source_sha256'])
    for p in (repo/EVIDENCE).rglob('*'):
        if (p.is_file() and p.suffix in {'.py', '.json', '.md', '.tex', '.txt', '.gz', '.log'}
                and '__pycache__' not in p.parts and 'publication' not in p.relative_to(repo/EVIDENCE).parts):
            paths.add(p.relative_to(repo).as_posix())
    current = {name: sha((repo/name).read_bytes()) for name in sorted(paths)}
    need(all(name not in current or current[name] == digest for name, digest in inherited.items()),
         'Overlay and historical source inventories disagree')
    return dict(sorted({**inherited, **current}.items()))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate the accepted publication overlay (default).')
    parser.parse_args()
    print(json.dumps(validate_ledger(ROOT), indent=2))
