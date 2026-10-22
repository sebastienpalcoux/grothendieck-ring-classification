"""Accepted general R3472 exclusion over the preserved creative-stage ledger.

The published creative archive supplies the historical classification identity.
Unpublished focused research already in the checkout is retained as a separately
bound checkpoint; its stale creative replay receipts are not reinterpreted.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile
import rank8_creative_20261022 as previous

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'evidence/r3472_exclusion_20261022'
ACCEPTED = EVIDENCE + '/accepted.json'
AUDIT = EVIDENCE + '/per_ring_research_audit.json'
LEDGER = 'supplements/rank8/output/exclusion_20261022/ledger.json'
MODELS = previous.MODELS
ARCHIVE = 'supplements/rank8/release/rank8-certified-exclusion-20261022.zip'
PUBLICATION = EVIDENCE + '/publication'
PUBLICATION_DATE = '2026-10-22'
PUBLICATION_DATE_LONG = '22 October 2026'
STATUS_REPORT = 'prepublication-review-2026-10-22.pdf'
RING_ID = 'R8_3_3472'
TENSOR_SHA256 = '33984d45e69ff778e70847def8349abda79ed6c0eaea242a73b533649f9b153a'
CRITERION = 'exact_center_indicator_certificate'
PROOF_MANIFEST = EVIDENCE + '/proof_manifest.json'
PROOF_RECEIPT = EVIDENCE + '/verification.json'
PROOF = EVIDENCE + '/manuscript.tex'
VERIFIER = EVIDENCE + '/replay.py'
BASELINE_LEDGER = previous.LEDGER
BASELINE_LEDGER_SHA256 = 'edac9d5685ed86acfff16d620598d76324430559cab58d9bf24d59074927d067'
BASELINE_MODELS = previous.MODELS
BASELINE_MODELS_SHA256 = '7b84c11792c15c9cc07a723fe3d03cf8c56f049907bb9de7be35fb9cefbbf382'
BASELINE_AUDIT = previous.AUDIT
HISTORICAL_ARCHIVE = previous.ARCHIVE
HISTORICAL_ARCHIVE_SHA256 = '4fc22ea0fd4bfef492aefe778467b3b5f9567bb045b500846a349f81e38c4dfb'
HISTORICAL_PREFIX = 'rank8-certified-creative-20261022/'
REMAINING_IDS = ['R8_3_928', 'R8_3_941', 'R8_3_1154', 'R8_3_1768']
REALIZED_STATUSES = previous.REALIZED_STATUSES


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_path(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def read_bound(repo, name, digest):
    need(safe_path(name), 'Unsafe exclusion source: ' + name)
    raw = (Path(repo) / name).read_bytes()
    need(sha(raw) == digest, 'Bound exclusion source changed: ' + name)
    return raw


def active(repo):
    return (Path(repo) / LEDGER).is_file()


def historical_identity(repo):
    """Validate the frozen archive identity, without claiming a new replay."""
    repo = Path(repo)
    need(sha((repo/HISTORICAL_ARCHIVE).read_bytes()) == HISTORICAL_ARCHIVE_SHA256,
         'Published creative archive changed')
    with zipfile.ZipFile(repo/HISTORICAL_ARCHIVE) as bundle:
        names = bundle.namelist()
        need(len(names) == len(set(names)) and all(
            n.startswith(HISTORICAL_PREFIX) and safe_path(n[len(HISTORICAL_PREFIX):])
            for n in names), 'Unsafe or duplicate historical archive member')
        checks = json.loads(bundle.read(HISTORICAL_PREFIX+'SHA256SUMS.json'))
        need(set(checks) == {n[len(HISTORICAL_PREFIX):] for n in names}-{'SHA256SUMS.json'},
             'Historical archive checksum coverage')
        for name, digest in ((BASELINE_LEDGER, BASELINE_LEDGER_SHA256),
                             (BASELINE_MODELS, BASELINE_MODELS_SHA256)):
            raw = bundle.read(HISTORICAL_PREFIX+name)
            need(sha(raw) == digest == checks.get(name), 'Historical classification identity: '+name)
            need((repo/name).read_bytes() == raw, 'Historical ledger or model inventory changed: '+name)
        receipt_name = previous.PUBLICATION+'/replay_normal.json'
        raw = bundle.read(HISTORICAL_PREFIX+receipt_name)
        need(sha(raw) == checks.get(receipt_name), 'Historical receipt identity')
        report = json.loads(raw)
        need(report['status'] == 'PASS' and report['counts'] ==
             {'excluded':3506, 'unitarily_realized':16, 'unresolved':5},
             'Historical creative classification counts')
    return {'archive':HISTORICAL_ARCHIVE, 'archive_sha256':HISTORICAL_ARCHIVE_SHA256,
            'ledger':BASELINE_LEDGER, 'ledger_sha256':BASELINE_LEDGER_SHA256,
            'models':BASELINE_MODELS, 'models_sha256':BASELINE_MODELS_SHA256,
            'mathematical_replay_performed':False,
            'scope':'Frozen published creative archive and classification identity; no fresh historical mathematical replay.'}


def creative_summary(repo):
    historical_identity(repo)
    with zipfile.ZipFile(Path(repo)/HISTORICAL_ARCHIVE) as bundle:
        r = json.loads(bundle.read(HISTORICAL_PREFIX+previous.PUBLICATION+'/replay_normal.json'))
    keys = ('new_decisions','resolved_ids','counts','cumulative_counts',
            'baseline_records_preserved','inherited_models_preserved','new_models',
            'remaining_ids','date','ledger','ledger_sha256','models','models_sha256',
            'accepted','accepted_sha256','baseline_ledger','baseline_ledger_sha256',
            'attempts_source','evidence')
    result = {k:r[k] for k in keys if k in r}
    result['historical_scope'] = 'Published creative checkpoint, preserved in the frozen archive.'
    return result


def research_summary(repo):
    """Read the pre-creative result inside the same immutable archive."""
    historical_identity(repo)
    name = 'evidence/rank8_research_20261022/publication/replay_normal.json'
    with zipfile.ZipFile(Path(repo)/HISTORICAL_ARCHIVE) as bundle:
        r = json.loads(bundle.read(HISTORICAL_PREFIX+name))
    keys = ('new_decisions','resolved_ids','counts','cumulative_counts',
            'baseline_records_preserved','inherited_models_preserved','new_models',
            'remaining_ids','date','ledger','ledger_sha256','models','models_sha256',
            'accepted','accepted_sha256','baseline_ledger','baseline_ledger_sha256',
            'attempts_source','evidence')
    return {k:r[k] for k in keys if k in r}


def decision():
    return {'id':RING_ID, 'rank':8, 'multiplicity':3, 'tensor_sha256':TENSOR_SHA256,
            'status':'excluded', 'scope':'general_complex', 'criterion':CRITERION,
            'proof_source':EVIDENCE, 'proof':PROOF, 'verifier':VERIFIER}


def accepted(repo):
    repo = Path(repo)
    value = json.loads((repo/ACCEPTED).read_text())
    need(value['schema'] == 'rank8-r3472-exclusion-20261022-accepted/v1', 'Exclusion acceptance schema')
    need(value['decisions'] == [decision()], 'Exact general-complex R3472 decision required')
    for key, name, digest in [('ledger',BASELINE_LEDGER,BASELINE_LEDGER_SHA256),
                              ('models',BASELINE_MODELS,BASELINE_MODELS_SHA256)]:
        need(value['baseline_'+key] == name and value['baseline_'+key+'_sha256'] == digest,
             'Exclusion baseline '+key)
    need(value['historical_archive'] == HISTORICAL_ARCHIVE and
         value['historical_archive_sha256'] == HISTORICAL_ARCHIVE_SHA256,
         'Exclusion historical archive identity')
    need(value['baseline_audit'] == BASELINE_AUDIT and
         value['source_sha256'].get(BASELINE_AUDIT) == value['baseline_audit_sha256'],
         'Unbound preserved focused-research checkpoint')
    for name, digest in value['source_sha256'].items():
        read_bound(repo, name, digest)
    need(value['verifiers'] == [VERIFIER] and all(p in value['source_sha256'] for p in
         (PROOF_MANIFEST, PROOF_RECEIPT, PROOF, VERIFIER)), 'Incomplete accepted proof registration')
    proof_manifest = json.loads((repo/PROOF_MANIFEST).read_text())
    need(proof_manifest['schema'] == 'r3472-exclusion-proof-closure-v1', 'Proof closure schema')
    need(all(value['source_sha256'].get(p) == h for p,h in proof_manifest['files'].items()),
         'Accepted sources omit a proof dependency')
    receipt = json.loads((repo/PROOF_RECEIPT).read_text())
    need(receipt.get('complete_general_categorification_exclusion') is True and
         receipt.get('status') in ('verified','PASS'), 'Full R3472 proof has not passed')
    tensor = json.loads((repo/value['canonical_tensor']).read_text())
    need(sha(json.dumps(tensor,separators=(',',':')).encode()) == TENSOR_SHA256,
         'Canonical R3472 tensor changed')
    return value


def reconcile(repo):
    repo = Path(repo)
    manifest = accepted(repo)
    historical_identity(repo)
    baseline = json.loads(read_bound(repo,BASELINE_LEDGER,BASELINE_LEDGER_SHA256))
    need(len(baseline) == 4500, 'Complete historical rank-eight ledger required')
    rows = deepcopy(baseline)
    row = next(r for r in rows if r['id'] == RING_ID)
    need(row['status'] == 'unresolved' and row['tensor_sha256'] == TENSOR_SHA256,
         'Only the exact unresolved R3472 input can change')
    row.update(status='excluded', criterion=CRITERION, scope='general_complex',
               proof_source=EVIDENCE, proof=PROOF, verifier=VERIFIER,
               exclusion_baseline_status='unresolved')
    need(all(a == b for a,b in zip(baseline,rows) if a['id'] != RING_ID),
         'An unrelated classification record changed')
    counts = Counter(r['status'] for r in rows if r['multiplicity'] == 3)
    total = Counter(r['status'] for r in rows)
    need(counts == Counter(excluded=3507,unitarily_realized=16,unresolved=4), 'Exact M3 exclusion counts')
    need(total == Counter(excluded=4403,unitarily_realized=93,unresolved=4), 'Cumulative exclusion counts')
    need([r['id'] for r in rows if r['status']=='unresolved'] == REMAINING_IDS, 'Remaining rank-eight IDs')
    models = json.loads(read_bound(repo,BASELINE_MODELS,BASELINE_MODELS_SHA256))
    need(len(models) == 93 and {m['id'] for m in models} ==
         {r['id'] for r in rows if r['status'] in REALIZED_STATUSES}, 'Preserved model inventory')
    report = {'new_decisions':1, 'resolved_ids':[RING_ID], 'counts':dict(counts),
              'cumulative_counts':dict(total), 'baseline_records_preserved':4499,
              'inherited_models_preserved':93, 'new_models':0,
              'remaining_ids':REMAINING_IDS, 'criterion':CRITERION,
              'scope':'general_complex', 'complete_general_categorification_exclusion':True}
    return rows, report


def reconcile_audit(repo):
    repo = Path(repo)
    manifest = accepted(repo)
    audit = json.loads(read_bound(repo,BASELINE_AUDIT,manifest['baseline_audit_sha256']))
    result = deepcopy(audit)
    result.update(schema='rank8-r3472-exclusion-20261022-per-ring-audit/v1',
                  baseline_audit=BASELINE_AUDIT, baseline_audit_sha256=manifest['baseline_audit_sha256'],
                  remaining_unresolved=4, accepted_new_exclusions=1, current_stage_new_models=0,
                  current_stage_general_exclusions=1)
    need(len(result['rows']) == len({r['id'] for r in result['rows']}) == 34, 'Historical audit coverage')
    row = next(r for r in result['rows'] if r['id'] == RING_ID)
    row['prior_stage_completed'] = deepcopy(row.get('latest_completed',[]))
    row.update(general_status='excluded', noncategorification_proved=True,
               categorification_proved=False, categorification_or_novelty_proved=False,
               novelty_proved=False, screening_stage='excluded', criterion=CRITERION,
               proof_source=EVIDENCE, proof=PROOF,
               screening_case_specific_focus='Complete center restriction frames and cyclic rotation integrality give an exact general complex exclusion.',
               screening_definition='Accepted general noncategorification theorem, after a complete sphericalization and Galois reduction. Earlier feasible relaxations and construction searches are historical checkpoints.')
    row['latest_completed'] = [{'domain':CRITERION,
        'outcome':'All 372 distinguished restriction frames are excluded: 276 by exact span certificates, eleven remaining symmetry orbits by exact phase separators, and the final orbit by 1648 rational integer-bound deductions and a final positive separator.',
        'scope':'All complex fusion categorifications, without an initial pivotal, spherical, braided, unitary or pseudo-unitary hypothesis.',
        'limitation':'Computer-assisted exact proof, subject to independent human mathematical review; this is a nonexistence theorem and does not construct a category.',
        'proof':PROOF, 'evidence':[PROOF_RECEIPT,PROOF_MANIFEST], 'verifiers':[VERIFIER]}]
    result.setdefault('historical_publication_artifact_sha256',{})
    for name,digest in manifest['source_sha256'].items():
        old = result['artifact_sha256'].get(name)
        if old and old != digest:
            result['historical_publication_artifact_sha256'][name] = old
        result['artifact_sha256'][name] = digest
    result['research_status'] = 'R8_3_3472 is generally excluded; four rank-eight cases remain unresolved.'
    return result


def validate_ledger(repo):
    repo = Path(repo)
    rows, report = reconcile(repo)
    for name,value in ((LEDGER,rows),(AUDIT,reconcile_audit(repo))):
        need((repo/name).is_file() and json.loads((repo/name).read_text()) == value,
             'Published exclusion overlay differs from accepted proof: '+name)
    report.update(date=PUBLICATION_DATE, ledger=LEDGER, ledger_sha256=sha((repo/LEDGER).read_bytes()),
                  models=MODELS, models_sha256=BASELINE_MODELS_SHA256,
                  accepted=ACCEPTED, accepted_sha256=sha((repo/ACCEPTED).read_bytes()),
                  baseline_ledger=BASELINE_LEDGER, baseline_ledger_sha256=BASELINE_LEDGER_SHA256,
                  attempts_source=AUDIT, evidence=EVIDENCE)
    return report


validate = validate_ledger


def commands(repo):
    return list(accepted(repo)['verifiers'])


def source_inventory(repo):
    repo = Path(repo)
    manifest = accepted(repo)
    historical_identity(repo)
    paths = set(manifest['source_sha256']) | {ACCEPTED,AUDIT,LEDGER,MODELS,HISTORICAL_ARCHIVE,
        'tools/rank8_exclusion_20261022.py','tools/rank8_publication.py',
        'tools/verify_rank8_exclusion_20261022.py','tools/build_rank8_exclusion_20261022_release.py',
        'tools/current_publication.py','tools/verify_current_publication.py',
        'tools/replay_current_publication_ci.py','tools/package_rank8_m3_data.py',
        'site/CATEGORIFICATION_SCOPE.md','site/BRAIDED_CATEGORIFICATION.md',
        'evidence/rank8_creative_20261022/r3472/second_branch_count.py'}
    return {name:sha((repo/name).read_bytes()) for name in sorted(paths)}


def prepare(repo):
    """Explicitly bind the completed proof and preserve the earlier checkpoint."""
    repo = Path(repo)
    historical_identity(repo)
    closure = json.loads((repo/PROOF_MANIFEST).read_text())
    need(closure['schema'] == 'r3472-exclusion-proof-closure-v1', 'Proof closure must be completed first')
    sources = dict(closure['files'])
    paths = {PROOF_MANIFEST,PROOF_RECEIPT,PROOF,VERIFIER,BASELINE_LEDGER,BASELINE_MODELS,
             BASELINE_AUDIT,previous.ACCEPTED,
             'site/dist/downloads/fusion-tensors/R8_3_3472.txt',
             'evidence/rank8_creative_20261022/r3472/second_branch_count.py',
             'evidence/rank8_creative_20261022/r3472/verification.json'}
    checkpoint = json.loads((repo/previous.ACCEPTED).read_text())
    paths.update(p for p in checkpoint['source_sha256'] if p.startswith('evidence/r3472_focus_20261022/'))
    for name in paths:
        digest = sha((repo/name).read_bytes())
        need(name not in sources or sources[name] == digest, 'Proof closure changed before acceptance: '+name)
        sources[name] = digest
    manifest = {'schema':'rank8-r3472-exclusion-20261022-accepted/v1', 'date':PUBLICATION_DATE,
        'decisions':[decision()], 'baseline_ledger':BASELINE_LEDGER,
        'baseline_ledger_sha256':BASELINE_LEDGER_SHA256,'baseline_models':BASELINE_MODELS,
        'baseline_models_sha256':BASELINE_MODELS_SHA256,'baseline_audit':BASELINE_AUDIT,
        'baseline_audit_sha256':sources[BASELINE_AUDIT],
        'baseline_audit_scope':'Preserved unpublished focused-research checkpoint; historical classification is bound separately to the published creative archive.',
        'historical_archive':HISTORICAL_ARCHIVE,'historical_archive_sha256':HISTORICAL_ARCHIVE_SHA256,
        'canonical_tensor':'site/dist/downloads/fusion-tensors/R8_3_3472.txt',
        'proof_manifest':PROOF_MANIFEST,'proof_receipt':PROOF_RECEIPT,
        'verifiers':[VERIFIER],'source_sha256':dict(sorted(sources.items()))}
    (repo/ACCEPTED).write_bytes(json_bytes(manifest))
    rows,report = reconcile(repo)
    (repo/LEDGER).parent.mkdir(parents=True,exist_ok=True)
    (repo/LEDGER).write_bytes(json_bytes(rows))
    (repo/AUDIT).write_bytes(json_bytes(reconcile_audit(repo)))
    return validate_ledger(repo)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    parser.add_argument('--publish',action='store_true',help='Bind the completed proof and write the new overlay')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    print(json.dumps(prepare(args.repo) if args.publish else validate_ledger(args.repo),indent=2))
