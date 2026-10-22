"""Identity checks for current documents and byte-exact replay sources."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

DOCUMENT_REVISION = 'data/current_document_revision.json'
REPLAY_DIRECTORY = 'evidence/publication_20261017'
REPLAY_MANIFEST_SHA256 = 'c2c969efd3f29172eec3a8187331470d8669021eaec4f703f8bc0b17e06630b5'
REPLAY_ARCHIVE_SHA256 = 'b5c98ca8317bdee7c439f2198d6f32807dd302dc440f2f458443642f2f179f2d'
CITATION_REPLAY_DIRECTORY = 'evidence/citation_20261019'
CITATION_REPLAY_MANIFEST_SHA256 = 'f66e3f910da6bce16b33c8fd8eabb2ab999959895a211b0c46f71a036cc65bd1'
CITATION_REPLAY_ARCHIVE_SHA256 = 'e42c63857d52450f1e90db2a4474476148cbce70ea58edfe7acad6aad96bd06e'
EXCLUDED_DOCUMENTS = {'manuscripts/prepublication-review-2026-10-17.pdf',
                      'manuscripts/prepublication-review-2026-10-19.pdf'}
# Retain dated historical reports; the active extension selects the current one.

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def safe_relative(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and '..' not in path.parts and path.as_posix() == name

def current_rank8_overlay(repo):
    """Select the newest accepted overlay without changing historical routers."""
    from importlib import import_module
    for name in ('rank8_exclusion_20261022', 'rank8_creative_20261022'):
        stage = import_module(name)
        if stage.active(repo):
            return stage
    return None

def rank8_historical_repair(repo):
    """Bind a reconstructed missing helper without rewriting historical claims."""
    from copy import deepcopy
    import rank8_exclusion_20261022 as stage
    repo = Path(repo).resolve()
    identity = stage.historical_identity(repo)
    helper = 'evidence/rank8_creative_20261022/r3472/second_branch_count.py'
    receipt = 'evidence/rank8_creative_20261022/r3472/verification.json'
    tensor = 'site/dist/downloads/fusion-tensors/R8_3_3472.txt'
    accepted_name = 'evidence/rank8_creative_20261022/accepted.json'
    manifest_name = 'evidence/rank8_creative_20261022/publication/source_manifest.json'
    accepted = stage.accepted(repo)
    if isinstance(accepted, tuple):
        accepted = accepted[0]
    replacements = {name: (repo / name).read_bytes() for name in (helper, receipt, tensor)}
    for name, raw in replacements.items():
        need(accepted['source_sha256'].get(name) == sha(raw),
             'Historical repair is not bound by the new exclusion checkpoint: ' + name)
    with zipfile.ZipFile(repo / stage.HISTORICAL_ARCHIVE) as archive:
        prefix = stage.HISTORICAL_PREFIX
        names = set(archive.namelist())
        need(prefix + helper not in names, 'Historical missing-helper premise changed')
        need(prefix + tensor not in names, 'Historical missing-tensor premise changed')
        original_raw = archive.read(prefix + receipt)
        old_accepted = json.loads(archive.read(prefix + accepted_name))
        original_manifest_raw = archive.read(prefix + manifest_name)
        original_manifest = json.loads(original_manifest_raw)
        need(old_accepted['source_sha256'][receipt] == sha(original_raw)
             and original_manifest[receipt] == sha(original_raw),
             'Original conditional receipt is not bound by its historical manifests')
    before, after = json.loads(original_raw), json.loads(replacements[receipt])
    need(before['inputs'].get(tensor) == sha(replacements[tensor]),
         'Restored canonical tensor differs from the original verification receipt')
    old_states = [158885, 121756, 37967, 832]
    new_states = [1078029, 840138, 232981, 681]
    need([x['states'] for x in before['second_branch_arithmetic_counts']] == old_states
         and [x['states'] for x in after['second_branch_arithmetic_counts']] == new_states,
         'Unexpected reconstructed-helper diagnostic counts')
    normalized = deepcopy(after)
    for row, old in zip(normalized['second_branch_arithmetic_counts'], old_states):
        row['states'] = old
    need(normalized == before, 'Historical repair changes more than four cache-state diagnostics')
    scripts = old_accepted['verifiers']
    need(scripts and len(scripts) == len(set(scripts)), 'Historical creative verifier coverage')
    need(all(safe_relative(name) and name.endswith('.py') and name in original_manifest
             and name in old_accepted['source_sha256']
             and original_manifest.get(name) == old_accepted['source_sha256'].get(name)
             for name in scripts), 'Historical creative verifier lacks its original source binding')
    checkpoint = {**original_manifest, **{name: sha(raw) for name, raw in replacements.items()}}
    checkpoint[manifest_name] = sha(original_manifest_raw)
    provenance = {
        'schema': 'rank8-creative-reconstructed-helper-checkpoint/v1',
        'historical_archive': identity,
        'original_source_manifest': manifest_name,
        'original_source_manifest_sha256': sha(original_manifest_raw),
        'original_verification_sha256': sha(original_raw),
        'injected_sources_sha256': {name: sha(replacements[name]) for name in (helper, tensor)},
        'replaced_receipts_sha256': {receipt: sha(replacements[receipt])},
        'changed_fields': [f'second_branch_arithmetic_counts[{i}].states' for i in range(4)],
        'historical_state_counts': old_states,
        'reconstructed_state_counts': new_states,
        'mathematical_receipt_fields_unchanged': True,
        'original_manifests_rewritten': False,
        'scope': ('The missing helper is a reconstruction, not recovered original code. '
                  'The missing canonical tensor is restored with its original receipt hash. '
                  'The original verifier and every mathematical receipt field are preserved; '
                  'four cache traversal counts have an explicit new checkpoint binding.'),
    }
    return provenance, checkpoint, replacements, scripts

def replay_rank8_exclusion_history(repo, output_dir, optimized=False):
    """Replay all old checks, explicitly repairing the missing creative helper."""
    import os
    import subprocess
    import sys
    import tempfile
    import rank8_exclusion_20261022 as stage
    repo, output_dir = Path(repo).resolve(), Path(output_dir).resolve()
    provenance, checkpoint, replacements, scripts = rank8_historical_repair(repo)
    original_identity = provenance['historical_archive']
    output_dir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env.pop('PYTHONPATH', None)
    env.update(PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1',
               OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    checks = []
    def record(name, command, cwd):
        print('HISTORICAL REPLAY', name, flush=True)
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
        log = output_dir / name
        need(not log.is_relative_to(repo / 'evidence/rank8_creative_20261022'),
             'A new historical replay log cannot overwrite creative-stage evidence')
        log.write_text(result.stdout + result.stderr)
        need(result.returncode == 0, 'Historical checkpoint replay failed: ' + name + '\n'
             + result.stdout + result.stderr)
        print('HISTORICAL PASS', name, flush=True)
        return {'status': 'PASS', 'returncode': 0, 'python_optimization': 0,
                'assertions_enabled': True,
                'log': log.relative_to(repo).as_posix() if log.is_relative_to(repo) else str(log),
                'log_sha256': sha(log.read_bytes())}
    with tempfile.TemporaryDirectory(prefix='rank8-exclusion-history-') as directory:
        target = Path(directory) / 'repo'
        target.mkdir()
        with zipfile.ZipFile(repo / stage.HISTORICAL_ARCHIVE) as archive:
            seen = set()
            for member in archive.infolist():
                need(member.filename.startswith(stage.HISTORICAL_PREFIX), 'Historical member root')
                name = member.filename[len(stage.HISTORICAL_PREFIX):]
                need(safe_relative(name) and name not in seen and not member.is_dir()
                     and (member.external_attr >> 16) & 0o170000 != 0o120000,
                     'Unsafe or duplicate historical member: ' + name)
                seen.add(name)
                path = target / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(archive.read(member))
        # This uses the original pre-E21 dispatcher, which covers the original
        # M3, frontier, center follow-up, R721 and research-stage mathematics.
        earlier_receipt = output_dir / 'pre_creative_replay.json'
        code = ('import json,sys; from pathlib import Path; '
                'sys.path.insert(0,str(Path(sys.argv[1])/"tools")); '
                'from rank8_creative_history import replay; '
                'r=replay(Path(sys.argv[1]),historical=True,optimized=bool(int(sys.argv[3]))); '
                'Path(sys.argv[2]).write_text(json.dumps(r,indent=2)+"\\n"); '
                'print(json.dumps(r,indent=2))')
        old_check = record('pre_creative_replay.log',
                           [sys.executable, '-c', code, str(target), str(earlier_receipt),
                            str(int(bool(optimized)))], target)
        old_check.update(script='tools/rank8_creative_history.py',
                         receipt_sha256=sha(earlier_receipt.read_bytes()))
        checks.append(old_check)
        for name, raw in replacements.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        def verify_checkpoint():
            for name, digest in checkpoint.items():
                need((target / name).is_file() and sha((target / name).read_bytes()) == digest,
                     'Historical checkpoint source changed: ' + name)
        verify_checkpoint()
        # Do not rerun the old aggregate against altered hashes. Every one of
        # its original mathematical scripts runs under this explicitly new
        # source checkpoint, with the old aggregate/manifests retained intact.
        for index, script in enumerate(scripts, 1):
            item = record(f'creative_{index:02d}_{Path(script).parent.name}_{Path(script).stem}.log',
                          [sys.executable, str(target / script)], target)
            item['script'] = script
            checks.append(item)
        verify_checkpoint()
    need(stage.historical_identity(repo) == original_identity, 'Pinned historical archive changed during replay')
    need(rank8_historical_repair(repo)[1] == checkpoint, 'Live repair checkpoint changed during replay')
    checkpoint_path = output_dir / 'creative_repair_source_manifest.json'
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + '\n')
    report = {**provenance, 'status': 'PASS', 'mathematical_replay_performed': True,
              'mode': 'complete historical replay with explicit reconstructed-helper checkpoint',
              'optimized_python_requested': bool(optimized),
              'all_mathematical_children_assertions_enabled': True,
              'creative_mathematical_verifiers': scripts, 'checks': checks,
              'checkpoint_source_manifest_sha256': sha(checkpoint_path.read_bytes()),
              'historical_archive_bytes_preserved': True, 'live_scientific_sources_modified': False,
              'receipt_output_directory': (output_dir.relative_to(repo).as_posix()
                                           if output_dir.is_relative_to(repo) else str(output_dir))}
    (output_dir / 'historical_replay.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report

def document_paths(repo):
    from rank8_publication import active
    excluded = EXCLUDED_DOCUMENTS | ({'manuscripts/prepublication-review-2026-10-20.pdf'} if active(repo) else set())
    roots = [repo / 'manuscripts']
    roots += [repo / 'supplements' / ('rank' + str(rank)) / folder
              for rank in range(2, 9) for folder in ('papers', 'paper')]
    return {path.relative_to(repo).as_posix()
            for root in roots for path in root.rglob('*')
            if path.is_file() and path.suffix in ('.tex', '.pdf')
            and path.relative_to(repo).as_posix() not in excluded} | {'docs/New_category_candidates_and_open_cases.pdf'}

def validate_documents(repo, check_web=False):
    repo = Path(repo)
    revision = json.loads((repo / DOCUMENT_REVISION).read_text())
    need(revision['schema'] == 'current-document-revision/v1' and revision['date'] in ('2026-10-17', '2026-10-19', '2026-10-20', '2026-10-21', '2026-10-22'),
         'Current document revision identity')
    from rank7_publication import remaining_ids, extension
    need(revision['remaining_ids'] == remaining_ids(repo)
         and revision['accepted_decisions'] == 36, 'Current document mathematical scope')
    need(revision.get('rank7_m5_update') == extension(repo), 'Current rank-seven extension scope')
    from rank8_publication import extension as rank8_extension
    need(revision.get('rank8_m3_update') == rank8_extension(repo), 'Current rank-eight extension scope')
    progress = 'evidence/rigidity_20261017/rank6/research_progress.json'
    need(revision['research_progress'] == progress and
         revision['research_progress_sha256'] == sha((repo / progress).read_bytes()),
         'Current document research identity')
    documents = revision['documents']
    need(set(documents) == document_paths(repo), 'Complete current document inventory')
    for name, item in documents.items():
        need(safe_relative(name), 'Unsafe document path')
        raw = (repo / name).read_bytes()
        need(len(raw) == item['bytes'] and sha(raw) == item['sha256'], 'Current document identity: ' + name)
        if name.endswith('.pdf'):
            need(raw.startswith(b'%PDF-'), 'Invalid current PDF: ' + name)
        if name.startswith('manuscripts/rank') and ('/papers/' in name or '/paper/' in name):
            mirror = name.replace('manuscripts/', 'supplements/', 1)
            if mirror in documents:
                need(documents[mirror] == item, 'Supplement manuscript copy differs: ' + mirror)
    for web, source in revision['web_copies'].items():
        need(safe_relative(web) and web.startswith('papers/') and source in documents
             and source.endswith('.pdf'), 'Invalid current website PDF mapping')
        if check_web:
            raw = (repo / 'site/dist' / web).read_bytes()
            need(sha(raw) == documents[source]['sha256'], 'Website PDF differs from current manuscript: ' + web)
    return revision

def citation_replay_sources(repo):
    """Read pinned catalog/source bytes required by historical commitments."""
    folder = Path(repo) / CITATION_REPLAY_DIRECTORY
    raw = (folder / 'replay_files.json').read_bytes()
    need(sha(raw) == CITATION_REPLAY_MANIFEST_SHA256, 'Immutable citation replay manifest identity')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'citation-replay-sources/v1' and
         manifest['baseline_commit'] == '4487d2bfd643ebe80a1199b31f3d2bdd1bc64983',
         'Citation replay baseline identity')
    archive = folder / 'replay_files.zip'
    need(sha(archive.read_bytes()) == CITATION_REPLAY_ARCHIVE_SHA256,
         'Immutable citation replay archive identity')
    result = {}
    with zipfile.ZipFile(archive) as bundle:
        need(len(bundle.namelist()) == len(set(bundle.namelist())) and
             set(bundle.namelist()) == set(manifest['files']), 'Exact citation replay archive inventory')
        for name, item in manifest['files'].items():
            need(safe_relative(name), 'Unsafe citation replay path')
            content = bundle.read(name)
            need(len(content) == item['bytes'] and sha(content) == item['sha256'],
                 'Citation replay byte identity: ' + name)
            result[name] = content
    return result

def replay_sources(repo):
    repo = Path(repo)
    folder = repo / REPLAY_DIRECTORY
    raw = (folder / 'replay_files.json').read_bytes()
    need(sha(raw) == REPLAY_MANIFEST_SHA256, 'Immutable replay manifest identity')
    manifest = json.loads(raw)
    need(manifest['baseline_commit'] == 'c1165f6ec2b7ca890e7c5100eb3cda093a9fce70', 'Replay baseline identity')
    archive = folder / 'replay_files.zip'
    need(sha(archive.read_bytes()) == REPLAY_ARCHIVE_SHA256, 'Immutable replay archive identity')
    result = {}
    with zipfile.ZipFile(archive) as bundle:
        need(len(bundle.namelist()) == len(set(bundle.namelist())) and
             set(bundle.namelist()) == set(manifest['files']), 'Exact replay archive inventory')
        for name, item in manifest['files'].items():
            need(safe_relative(name), 'Unsafe replay path')
            content = bundle.read(name)
            need(len(content) == item['bytes'] and sha(content) == item['sha256'], 'Replay byte identity: ' + name)
            result[name] = content
    citations = citation_replay_sources(repo)
    need(not set(result).intersection(citations), 'Citation replay must be additive')
    result.update(citations)
    from rank7_publication import extension, historical_sources
    if extension(repo):
        previous = historical_sources(repo)
        need(not set(result).intersection(previous), 'Rank-seven extension replay must be additive')
        result.update(previous)
    return result

def restore_replay_sources(repo, destination, sources=None):
    repo, destination = Path(repo).resolve(), Path(destination).resolve()
    need(repo != destination and repo not in destination.parents, 'Replay requires an isolated directory')
    sources = replay_sources(repo) if sources is None else sources
    for name, raw in sources.items():
        target = (destination / name).resolve()
        need(destination in target.parents, 'Unsafe replay destination')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    return len(sources)
