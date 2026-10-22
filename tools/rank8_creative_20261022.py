"""Accepted E21 realization and scoped research overlay on the frozen research release.

Only R8_3_982 changes classification status. Its full source graph determines
the neutral component fusion tensor exactly. The other five residual rings
retain unresolved status with separately scoped research updates.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import rank8_research_20261022 as previous
import rank8_creative_history as history

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'evidence/rank8_creative_20261022'
ACCEPTED = EVIDENCE + '/accepted.json'
MODEL_MANIFEST = EVIDENCE + '/r982/model_catalog_entry.json'
AUDIT = EVIDENCE + '/per_ring_research_audit.json'
LEDGER = 'supplements/rank8/output/creative_20261022/ledger.json'
MODELS = 'supplements/rank8/output/creative_20261022/model_catalog.json'
ARCHIVE = 'supplements/rank8/release/rank8-certified-creative-20261022.zip'
PUBLICATION = EVIDENCE + '/publication'
PUBLICATION_DATE = '2026-10-22'
PUBLICATION_DATE_LONG = '22 October 2026'
STATUS_REPORT = 'prepublication-review-2026-10-22.pdf'
BASELINE_LEDGER = previous.LEDGER
BASELINE_LEDGER_SHA256 = '521b9b9fb16a86c7c4ba491b8c2c0ebad05de1e41aafb5bc225d6342c9477e4e'
BASELINE_MODELS = previous.MODELS
BASELINE_MODELS_SHA256 = 'f26206578e9be9a151eed7694aae05e010b6e7254b188b367a13e270a737b141'
BASELINE_AUDIT = previous.AUDIT
BASELINE_AUDIT_SHA256 = '751c315c5434ede9d9001f32b712ad889e5a1c4da6eadb0400475853766105aa'
RESIDUAL_IDS = {f'R8_3_{n}' for n in (928, 941, 982, 1154, 1768, 3472)}
REALIZED_ID = 'R8_3_982'
REALIZED_TENSOR_SHA256 = 'f4a9fb77b3a78e9dcd8370ca9fa822ea331f1b71e3fad7990efdd386445fcd1c'
REALIZED_STATUSES = previous.REALIZED_STATUSES
need, safe_path = previous.need, previous.safe_path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bound(repo, name, digest):
    need(safe_path(name), 'Unsafe creative source: ' + name)
    raw = (Path(repo) / name).read_bytes()
    need(sha(raw) == digest, 'Accepted creative source changed: ' + name)
    return raw


def active(repo):
    return (Path(repo) / LEDGER).is_file()


def accepted(repo):
    repo = Path(repo)
    value = json.loads((repo / ACCEPTED).read_text())
    need(value['schema'] == 'rank8-creative-20261022-accepted/v1', 'Creative acceptance schema')
    for key, path, digest in [('ledger', BASELINE_LEDGER, BASELINE_LEDGER_SHA256),
                              ('models', BASELINE_MODELS, BASELINE_MODELS_SHA256),
                              ('audit', BASELINE_AUDIT, BASELINE_AUDIT_SHA256)]:
        need(value['baseline_' + key] == path and value['baseline_' + key + '_sha256'] == digest,
             'Creative baseline identity: ' + key)
        need(value['source_sha256'].get(path) == digest, 'Unbound creative baseline: ' + key)
    for path, digest in value['source_sha256'].items():
        read_bound(repo, path, digest)
    need(value['model_manifest'] == MODEL_MANIFEST and MODEL_MANIFEST in value['source_sha256'],
         'Unbound accepted E21 model manifest')
    records = json.loads((repo / MODEL_MANIFEST).read_text())
    need(len(records) == 1 and records[0]['id'] == REALIZED_ID,
         'Only the reviewed E21 neutral-component model is accepted')
    model = records[0]
    need(model['multiplicity'] == 3 and model['status'] == 'unitarily_realized' and
         model['model_scope'] == 'unitary' and model['unitary'] == model['pseudo_unitary'] == 'yes',
         'Accepted R982 unitary model scope')
    tensor = model['tensor']
    need(sha(json.dumps(tensor, separators=(',', ':')).encode()) ==
         model['tensor_sha256'] == REALIZED_TENSOR_SHA256, 'Accepted canonical E21 tensor digest')
    need(model['source_certificate'] == EVIDENCE+'/r982/e21_model.py' and
         model['source_certificate'] in value['source_sha256'] and model['constructors'],
         'Missing exact E21 model verifier or constructor')
    for path, digest in model['evidence_sha256'].items():
        need(value['source_sha256'].get(path) == digest, 'E21 model evidence not accepted: ' + path)
    for constructor in model['constructors']:
        p, t = constructor['basis_map_source_to_model'], constructor['tensor']
        need(p == [0,2,3,4,5,1,7,6] and sorted(p) == list(range(8)), 'Exact E21 basis map')
        need(all(t[p[i]][p[j]][p[k]] == tensor[i][j][k]
                 for i in range(8) for j in range(8) for k in range(8)),
             'All 512 E21 model tensor entries match the canonical tensor')
    receipt_path = EVIDENCE+'/r982/e21_model.json'
    need(receipt_path in value['source_sha256'], 'Unbound exact E21 model receipt')
    receipt = json.loads((repo/receipt_path).read_text())
    need(receipt['status'] == 'PASS' and receipt['canonical_tensor_sha256'] == REALIZED_TENSOR_SHA256
         and receipt['canonical_structure_constants_checked'] == 512
         and receipt['neutral_rank'] == 8 and receipt['neutral_maximum_coefficient'] == 3
         and receipt['unit_evaluation_rank_by_total_degree'] == [1,3,6,10,15,21,24],
         'E21 receipt lacks the complete graph-derived identification')
    need(value['decisions'] == [{'id': model['id'], 'tensor_sha256': model['tensor_sha256'],
                                'status': model['status'], 'model': model['model']}],
         'Accepted classification decision differs from exact E21 model')
    need(set(value['research_updates']) == RESIDUAL_IDS,
         'All six prior residuals require explicitly scoped creative records')
    for ring_id, updates in value['research_updates'].items():
        need(updates, 'Empty creative research record: ' + ring_id)
        for update in updates:
            need(all(update.get(k) for k in ('domain', 'outcome', 'scope', 'limitation')),
                 'Unscoped creative update: ' + ring_id)
            paths = update.get('evidence', []) + update.get('verifiers', [])
            if update.get('proof'):
                paths.append(update['proof'])
            for path in paths:
                need(path in value['source_sha256'], 'Unbound creative research update: ' + path)
    for path in value['verifiers']:
        need(path in value['source_sha256'] and path.endswith('.py'),
             'Unbound executable creative verifier: ' + path)
    return value, records


def reconcile(repo):
    repo = Path(repo)
    manifest, new_models = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_LEDGER, BASELINE_LEDGER_SHA256))
    inherited = json.loads(read_bound(repo, BASELINE_MODELS, BASELINE_MODELS_SHA256))
    need(len(baseline) == 4500 and len(inherited) == 92, 'Historical creative input coverage')
    need({r['id'] for r in baseline if r['status'] == 'unresolved'} == RESIDUAL_IDS,
         'Prior unresolved inventory changed')
    rows = deepcopy(baseline)
    row = next(r for r in rows if r['id'] == REALIZED_ID)
    model = new_models[0]
    need(row['multiplicity'] == 3 and row['status'] == 'unresolved' and
         row['tensor_sha256'] == model['tensor_sha256'], 'Must realize exact unresolved baseline tensor')
    row.update(status=model['status'], models=[model['model']], model_source=MODEL_MANIFEST,
               creative_baseline_status='unresolved')
    need(all(a == b for a, b in zip(baseline, rows) if a['id'] != REALIZED_ID),
         'An unaccepted historical record changed')
    models = deepcopy(inherited) + deepcopy(new_models)
    need(len({m['id'] for m in models}) == len(models) == 93, 'Unique current model inventory')
    need(models[:-1] == inherited, 'Inherited model records changed')
    counts = Counter(r['status'] for r in rows if r['multiplicity'] == 3)
    need(counts == Counter(excluded=3506, unitarily_realized=16, unresolved=5),
         'Exact-multiplicity-three creative classification counts')
    cumulative = Counter(r['status'] for r in rows)
    need(cumulative == Counter(excluded=4402, unitarily_realized=93, unresolved=5),
         'Cumulative through-multiplicity-three creative counts')
    positives = {r['id']: r['status'] for r in rows
                 if r['multiplicity'] == 3 and r['status'] in REALIZED_STATUSES}
    need({m['id']: m['status'] for m in models if m['multiplicity'] == 3} == positives,
         'Creative models and ledger differ')
    need({m['id'] for m in models} ==
         {r['id'] for r in rows if r['status'] in REALIZED_STATUSES},
         'Cumulative realized IDs and inherited model IDs differ')
    report = {'new_decisions': 1, 'resolved_ids': [REALIZED_ID], 'counts': dict(counts),
              'cumulative_counts': dict(cumulative), 'baseline_records_preserved': 4499,
              'inherited_models_preserved': 92, 'new_models': 1,
              'remaining_ids': sorted(RESIDUAL_IDS-{REALIZED_ID}, key=lambda x: int(x.split('_')[-1]))}
    return rows, models, report


def reconcile_audit(repo):
    repo = Path(repo)
    manifest, new_models = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_AUDIT, BASELINE_AUDIT_SHA256))
    result = deepcopy(baseline)
    result.update(schema='rank8-creative-20261022-per-ring-audit/v1',
                  baseline_audit=BASELINE_AUDIT, baseline_audit_sha256=BASELINE_AUDIT_SHA256,
                  remaining_unresolved=5, accepted_new_exclusions=0,
                  accepted_new_models=baseline.get('accepted_new_models', 0)+1,
                  current_stage_new_models=1)
    need(len(result['rows']) == len({r['id'] for r in result['rows']}) == 34,
         'Historical creative audit coverage changed')
    for row in result['rows']:
        row['prior_stage_completed'] = deepcopy(row.get('latest_completed', []))
        row['latest_completed'] = deepcopy(manifest['research_updates'].get(row['id'], []))
        if row['id'] == REALIZED_ID:
            model = new_models[0]
            row.update(general_status='unitarily_realized', categorification_or_novelty_proved=True,
                       categorification_proved=True, novelty_proved=False, noncategorification_proved=False,
                       screening_stage='unitarily_realized', accepted_model=model['model'],
                       model_source=MODEL_MANIFEST,
                       screening_case_specific_focus='The exact triality-zero fusion tensor of the known unitary E21 chiral category agrees with all 512 canonical R982 coefficients. Both nonregular based module types and the algebra 1+X5 are realized.',
                       screening_definition='Known unitary construction identified by an exact source-graph fusion-tensor crosswalk; preceding screening records are historical research attempts.')
    for path, digest in manifest['source_sha256'].items():
        if path in result['artifact_sha256'] and result['artifact_sha256'][path] != digest:
            need(path in history.SUPERSEDED_PUBLICATION_DOCS,
                 'Inherited creative source hash conflict: ' + path)
            result.setdefault('historical_publication_artifact_sha256', {})[path] = result['artifact_sha256'][path]
        result['artifact_sha256'][path] = digest
    return result


def validate_ledger(repo):
    repo = Path(repo)
    rows, models, report = reconcile(repo)
    for name, value in ((LEDGER, rows), (MODELS, models), (AUDIT, reconcile_audit(repo))):
        need((repo/name).is_file() and json.loads((repo/name).read_text()) == value,
             'Published creative overlay differs from accepted evidence: ' + name)
    report.update(date=PUBLICATION_DATE, ledger=LEDGER, ledger_sha256=sha((repo/LEDGER).read_bytes()),
                  models=MODELS, models_sha256=sha((repo/MODELS).read_bytes()),
                  accepted=ACCEPTED, accepted_sha256=sha((repo/ACCEPTED).read_bytes()),
                  baseline_ledger=BASELINE_LEDGER, baseline_ledger_sha256=BASELINE_LEDGER_SHA256,
                  attempts_source=AUDIT, evidence=EVIDENCE)
    return report


def validate(repo):
    return validate_ledger(repo)


def commands(repo):
    manifest, _ = accepted(repo)
    return list(manifest['verifiers'])


def source_inventory(repo):
    repo = Path(repo)
    history.baseline(repo)
    inherited = json.loads(read_bound(repo, history.MANIFEST, history.MANIFEST_SHA256))
    manifest, _ = accepted(repo)
    paths = {ACCEPTED, MODEL_MANIFEST, LEDGER, MODELS, AUDIT,
             'tools/rank8_creative_20261022.py', 'tools/rank8_creative_history.py',
             history.MANIFEST, history.ARCHIVE, 'tools/rank8_publication.py',
             'tools/current_publication.py', 'tools/verify_current_publication.py',
             'tools/package_rank8_m3_data.py', 'tools/replay_current_publication_ci.py'}
    paths.update(history.SUPERSEDED_PUBLICATION_DOCS)
    paths.update(manifest['source_sha256'])
    # Include exactly the accepted evidence closure, not arbitrary discovery
    # output, mutable exploratory logs, or unfinished cone computations.
    for name in (EVIDENCE+'/README.md', 'tools/verify_rank8_creative_20261022.py',
                 'tools/build_rank8_creative_20261022_release.py'):
        if (repo/name).is_file():
            paths.add(name)
    current = {path: sha((repo/path).read_bytes()) for path in sorted(paths)}
    need(all(path in history.SUPERSEDED_SOURCES or path not in current or current[path] == digest
             for path, digest in inherited.items()),
         'Creative and historical source inventories disagree')
    return dict(sorted({**inherited, **current}.items()))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.parse_args()
    print(json.dumps(validate_ledger(ROOT), indent=2))
