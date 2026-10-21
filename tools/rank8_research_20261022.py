"""Accepted 22 October research overlay on the immutable R721 publication.

Only R8_3_65 and R8_3_1795 change classification status. The inherited model catalogue is
reused without alteration. Other findings retain their explicit scope.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import rank8_next as previous

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'evidence/rank8_research_20261022'
ACCEPTED = EVIDENCE + '/accepted.json'
AUDIT = EVIDENCE + '/per_ring_research_audit.json'
LEDGER = 'supplements/rank8/output/research_20261022/ledger.json'
MODELS = previous.MODELS
ARCHIVE = 'supplements/rank8/release/rank8-certified-research-20261022.zip'
PUBLICATION = EVIDENCE + '/publication'
PUBLICATION_DATE = '2026-10-22'
PUBLICATION_DATE_LONG = '22 October 2026'
STATUS_REPORT = 'prepublication-review-2026-10-22.pdf'
BASELINE_LEDGER = previous.LEDGER
BASELINE_LEDGER_SHA256 = 'fccfbdb7e454511cd0d0908f321f3e22b971164f58a853d26880ecb03b28e33b'
BASELINE_MODELS = previous.MODELS
BASELINE_MODELS_SHA256 = 'f26206578e9be9a151eed7694aae05e010b6e7254b188b367a13e270a737b141'
BASELINE_AUDIT = previous.AUDIT
BASELINE_AUDIT_SHA256 = 'fb22a43bd87e0df3faad56c5772a078aaaec6deb691bf6b340cc1034c4ec1454'
RESIDUAL_IDS = {f'R8_3_{n}' for n in (65, 928, 941, 982, 1154, 1768, 1795, 3472)}
R65_SHA256 = 'fb2d70fa36311b2092190eb1ecd5e3e82fd4ab7ff646b11aa7c7e518d261a1c4'
R1795_SHA256 = 'feddd2934d44be4872c82ed6c5650bf9d8aac2bc87b72778d88b375726f4cd1f'
EXCLUDED_IDS = {'R8_3_65', 'R8_3_1795'}
REALIZED_STATUSES = previous.REALIZED_STATUSES
need, safe_path = previous.need, previous.safe_path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bound(repo, name, digest):
    need(safe_path(name), 'Unsafe research source: ' + name)
    raw = (Path(repo) / name).read_bytes()
    need(sha(raw) == digest, 'Accepted research source changed: ' + name)
    return raw


def active(repo):
    return (Path(repo) / LEDGER).is_file()


def accepted(repo):
    repo = Path(repo)
    value = json.loads((repo / ACCEPTED).read_text())
    need(value['schema'] == 'rank8-research-20261022-accepted/v1', 'Research acceptance schema')
    for key, path, digest in [('ledger', BASELINE_LEDGER, BASELINE_LEDGER_SHA256),
                              ('models', BASELINE_MODELS, BASELINE_MODELS_SHA256),
                              ('audit', BASELINE_AUDIT, BASELINE_AUDIT_SHA256)]:
        need(value['baseline_' + key] == path and value['baseline_' + key + '_sha256'] == digest,
             'Research baseline identity: ' + key)
        need(value['source_sha256'].get(path) == digest, 'Unbound research baseline: ' + key)
    for path, digest in value['source_sha256'].items():
        read_bound(repo, path, digest)
    decisions = value['decisions']
    need(len(decisions) == 2 and {d['id'] for d in decisions} == EXCLUDED_IDS,
         'Exactly the reviewed R65 and R1795 classification decisions are accepted')
    expected_hashes = {'R8_3_65': R65_SHA256, 'R8_3_1795': R1795_SHA256}
    for decision in decisions:
        ring_id = decision['id']
        need(decision['tensor_sha256'] == expected_hashes[ring_id] and
             decision['status'] == 'excluded', 'Accepted excluded tensor: ' + ring_id)
        cert = decision['certificate']
        need(cert['scope'] == 'general_complex_fusion_category', 'General exclusion scope')
        for path in [cert['proof'], cert['evidence'], *cert['verifiers']]:
            need(path in value['source_sha256'], 'Unbound exclusion proof: ' + path)
        receipt = json.loads((repo / cert['evidence']).read_text())
        need(receipt['tensor_sha256'] == expected_hashes[ring_id], 'Exclusion receipt tensor')
        if ring_id == 'R8_3_65':
            need(cert['kind'] == 'pointed_induction_fourier_phase_all_classes' and
                 receipt['status'] == 'six_branches_covering_all_four_pointed_classes_verified_exactly' and
                 receipt['previous_k0_subgroup_dual_proof_required'] is False,
                 'R65 receipt does not cover the direct unified exclusion')
        else:
            need(cert['kind'] == 'pointed_induction_fourier_fibre_packing_all_indicators' and
                 receipt['status'] == 'all_parities_exact_infeasible',
                 'R1795 receipt must exclude both pointed associator classes')
            branches = receipt['parities']
            need(len(branches) == 2 and
                 {p['pointed_second_indicator'] for p in branches} == {-1, 1} and
                 all(p['status'] == 'all_indicator_branches_exact_infeasible' and
                     p['verified_indicator_branches'] == p['admissible_indicator_branches'] == 8
                     for p in branches), 'R1795 requires all sixteen indicator branches')
            gate_path = cert['general_reduction_evidence']
            need(gate_path in value['source_sha256'], 'Unbound R1795 general reduction')
            gates = json.loads((repo / gate_path).read_text())
            gate = next(g for g in gates if g['id'] == ring_id)
            need(gate['tensor_sha256'] == expected_hashes[ring_id] and
                 gate['conclusion'] == 'every categorification is spherical and has a pseudo-unitary Galois conjugate; no existence or general unbraided exclusion asserted',
                 'R1795 general-to-Galois-pseudo-unitary gate')
        for path, digest in receipt['sources'].items():
            need(value['source_sha256'].get(path) == digest,
                 'Unbound imported exclusion source: ' + path)
    need(set(value['research_updates']) == RESIDUAL_IDS, 'All eight prior residuals need scoped research records')
    for ring_id, updates in value['research_updates'].items():
        need(updates, 'Empty research record: ' + ring_id)
        for update in updates:
            need(all(update.get(k) for k in ('domain', 'outcome', 'scope', 'limitation')),
                 'Unscoped research update: ' + ring_id)
            for path in update.get('evidence', []) + update.get('verifiers', []):
                need(path in value['source_sha256'], 'Unbound research update: ' + path)
    for path in value['verifiers']:
        need(path in value['source_sha256'] and path.endswith('.py'), 'Unbound executable verifier: ' + path)
    return value


def reconcile(repo):
    repo = Path(repo)
    manifest = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_LEDGER, BASELINE_LEDGER_SHA256))
    models = json.loads(read_bound(repo, BASELINE_MODELS, BASELINE_MODELS_SHA256))
    need(len(baseline) == 4500 and len(models) == 92, 'Historical research input coverage')
    need({r['id'] for r in baseline if r['status'] == 'unresolved'} == RESIDUAL_IDS,
         'Prior unresolved inventory changed')
    rows = deepcopy(baseline)
    by_id = {r['id']: r for r in rows}
    for decision in manifest['decisions']:
        row = by_id[decision['id']]
        need(row['multiplicity'] == 3 and row['status'] == 'unresolved' and
             row['tensor_sha256'] == decision['tensor_sha256'], 'Must exclude exact unresolved baseline tensor')
        row.update(status='excluded', criterion=decision['certificate']['kind'],
                   certificate=deepcopy(decision['certificate']), research_baseline_status='unresolved')
    need(all(a == b for a, b in zip(baseline, rows) if a['id'] not in EXCLUDED_IDS),
         'An unaccepted historical record changed')
    counts = Counter(r['status'] for r in rows if r['multiplicity'] == 3)
    need(counts == Counter(excluded=3506, unitarily_realized=15, unresolved=6), 'Research classification counts')
    positives = {r['id']: r['status'] for r in rows
                 if r['multiplicity'] == 3 and r['status'] in REALIZED_STATUSES}
    need({r['id']: r['status'] for r in models if r['multiplicity'] == 3} == positives,
         'Inherited models and research ledger differ')
    report = {'new_decisions': 2, 'resolved_ids': ['R8_3_65', 'R8_3_1795'], 'counts': dict(counts),
              'baseline_records_preserved': 4498, 'inherited_models_preserved': len(models),
              'new_models': 0, 'remaining_ids': sorted(RESIDUAL_IDS - EXCLUDED_IDS, key=lambda x: int(x.split('_')[-1]))}
    return rows, report


def reconcile_audit(repo):
    repo = Path(repo)
    manifest = accepted(repo)
    baseline = json.loads(read_bound(repo, BASELINE_AUDIT, BASELINE_AUDIT_SHA256))
    result = deepcopy(baseline)
    result.update(schema='rank8-research-20261022-per-ring-audit/v1',
                  baseline_audit=BASELINE_AUDIT, baseline_audit_sha256=BASELINE_AUDIT_SHA256,
                  remaining_unresolved=6, accepted_new_exclusions=2,
                  accepted_general_exclusions=baseline['accepted_general_exclusions'] + 2,
                  current_stage_new_models=0)
    need(len(result['rows']) == len({r['id'] for r in result['rows']}) == 34,
         'Historical research audit coverage changed')
    for row in result['rows']:
        row['prior_stage_completed'] = deepcopy(row.get('latest_completed', []))
        row['latest_completed'] = deepcopy(manifest['research_updates'].get(row['id'], []))
        if row['id'] in EXCLUDED_IDS:
            row.update(general_status='excluded', noncategorification_proved=True,
                       screening_stage='generally_excluded', accepted_exclusion=deepcopy(next(d['certificate'] for d in manifest['decisions'] if d['id'] == row['id'])))
    for path, digest in manifest['source_sha256'].items():
        need(path not in result['artifact_sha256'] or result['artifact_sha256'][path] == digest,
             'Inherited research source hash conflict: ' + path)
        result['artifact_sha256'][path] = digest
    return result


def validate_ledger(repo):
    repo = Path(repo)
    rows, report = reconcile(repo)
    for name, value in ((LEDGER, rows), (AUDIT, reconcile_audit(repo))):
        need((repo / name).is_file() and json.loads((repo / name).read_text()) == value,
             'Published research overlay differs from accepted evidence: ' + name)
    report.update(date=PUBLICATION_DATE, ledger=LEDGER, ledger_sha256=sha((repo / LEDGER).read_bytes()),
                  models=MODELS, models_sha256=BASELINE_MODELS_SHA256,
                  accepted=ACCEPTED, accepted_sha256=sha((repo / ACCEPTED).read_bytes()),
                  baseline_ledger=BASELINE_LEDGER, baseline_ledger_sha256=BASELINE_LEDGER_SHA256,
                  attempts_source=AUDIT, evidence=EVIDENCE)
    return report


def validate(repo):
    return validate_ledger(repo)


def commands(repo):
    return list(accepted(repo)['verifiers'])


def source_inventory(repo):
    repo = Path(repo)
    inherited = previous.source_inventory(repo)
    manifest = accepted(repo)
    paths = {ACCEPTED, LEDGER, AUDIT, 'tools/rank8_research_20261022.py', 'tools/rank8_publication.py',
             'tools/current_publication.py', 'tools/verify_current_publication.py',
             'tools/package_rank8_m3_data.py'}
    paths.update(manifest['source_sha256'])
    # Package the explicit accepted dependency closure, not exploratory folder
    # contents. Only source-bound pointed follow-up files enter this inventory.
    for name in (EVIDENCE + '/README.md',
                 'tools/verify_rank8_research_20261022.py',
                 'tools/build_rank8_research_20261022_release.py'):
        if (repo / name).is_file():
            paths.add(name)
    current = {path: sha((repo / path).read_bytes()) for path in sorted(paths)}
    need(all(path not in current or current[path] == digest for path, digest in inherited.items()),
         'Research and historical source inventories disagree')
    return dict(sorted({**inherited, **current}.items()))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.parse_args()
    print(json.dumps(validate_ledger(ROOT), indent=2))
