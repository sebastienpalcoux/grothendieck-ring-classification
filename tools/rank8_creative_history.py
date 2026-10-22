"""Verify and replay the immutable pre-E21 rank-eight scientific release.

Current publication routers may evolve. Historical mathematics is replayed
from its byte-exact published archive, never with newer replacement routers.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE = 'supplements/rank8/release/rank8-certified-research-20261022.zip'
ARCHIVE_SHA256 = '7c3b35b94e683db34a2247edf9e4247e1424be71c72ad8379e4d503c2267319a'
PREFIX = 'rank8-certified-research-20261022/'
MANIFEST = 'evidence/rank8_research_20261022/publication/source_manifest.json'
MANIFEST_SHA256 = '67f00e4b4ba0ddbd3586ea308f7cc56e04589f7851338f015a009992ac1c2b09'
# These current publication routers are independently bound in the new stage.
# Their old versions remain in the immutable archive used for historical replay.
SUPERSEDED_ROUTERS = {'tools/rank8_publication.py', 'tools/verify_current_publication.py'}
SUPERSEDED_PUBLICATION_DOCS = {'site/BRAIDED_CATEGORIFICATION.md', 'site/CATEGORIFICATION_SCOPE.md'}
SUPERSEDED_SOURCES = SUPERSEDED_ROUTERS | SUPERSEDED_PUBLICATION_DOCS
NEXT_ACCEPTED = 'evidence/rank8_next_20261021/accepted.json'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def baseline(repo):
    repo = Path(repo)
    need(sha((repo/ARCHIVE).read_bytes()) == ARCHIVE_SHA256, 'Frozen scientific archive changed')
    with zipfile.ZipFile(repo/ARCHIVE) as bundle:
        names = bundle.namelist()
        need(len(names) == len(set(names)), 'Duplicate historical archive members')
        need(all(n.startswith(PREFIX) and not PurePosixPath(n[len(PREFIX):]).is_absolute()
                 and '..' not in PurePosixPath(n[len(PREFIX):]).parts for n in names), 'Unsafe historical path')
        checks = json.loads(bundle.read(PREFIX+'SHA256SUMS.json'))
        need(set(checks) == {n[len(PREFIX):]for n in names}-{'SHA256SUMS.json'}, 'Historical checksum coverage')
        for name, digest in checks.items():
            need(sha(bundle.read(PREFIX+name)) == digest, 'Historical member changed: '+name)
        raw = bundle.read(PREFIX+MANIFEST)
        need(sha(raw) == MANIFEST_SHA256 and (repo/MANIFEST).read_bytes() == raw, 'Historical source manifest changed')
        sources = json.loads(raw)
        need(len(sources) == 1785, 'Historical source coverage')
        for name, digest in sources.items():
            need(checks.get(name) == digest, 'Historical source not bound to archive: '+name)
            if name not in SUPERSEDED_SOURCES:
                need(sha((repo/name).read_bytes()) == digest, 'Immutable historical input changed: '+name)
    return {'archive':ARCHIVE,'archive_sha256':ARCHIVE_SHA256,
            'source_manifest':MANIFEST,'source_manifest_sha256':MANIFEST_SHA256,
            'source_files':len(sources),'current_routers_replaced':sorted(SUPERSEDED_ROUTERS),
            'current_publication_documents_replaced':sorted(SUPERSEDED_PUBLICATION_DOCS),
            'historical_publication_document_bytes_preserved_in_archive':True,
            'historical_router_bytes_preserved_in_archive':True}

def replay(repo, historical=False, optimized=False):
    repo = Path(repo).resolve()
    identity = baseline(repo)
    scripts = [
        ('supplements/rank8/software/verify_m3_continuation.py', []),
        ('tools/verify_rank8_frontier.py', ['--repo']),
        ('evidence/rank8_center_followup_20261021/verify.py', ['--root']),
        ('tools/verify_rank8_research_20261022.py', ['--repo']),
    ]
    receipts = []
    with tempfile.TemporaryDirectory(prefix='rank8-pre-e21-history-') as directory:
        target = Path(directory)/'repo'
        target.mkdir()
        with zipfile.ZipFile(repo/ARCHIVE) as bundle:
            for member in bundle.namelist():
                name = member[len(PREFIX):]
                path = target/name
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(bundle.read(member))
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE',None)
        env.pop('PYTHONPATH',None)
        env.update(PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        for index,(script,flags) in enumerate(scripts):
            output = Path(directory)/f'check_{index}.json'
            # Keep assertions in direct and transitive historical proof code.
            # Some frozen dispatchers propagate -O to their children, so an
            # optimized outer invocation must not pass it across this boundary.
            command = [sys.executable, str(target/script)]
            if flags:
                command += flags+[str(target)]
            command += ['--output',str(output)]
            if not historical:
                command.append('--metadata-only')
            result = subprocess.run(command,cwd=target,env=env,capture_output=True,text=True)
            need(result.returncode == 0,'Frozen historical replay failed: '+script+'\n'+result.stdout+result.stderr)
            receipt = json.loads(output.read_text())
            need(receipt['status'] == ('PASS' if historical else 'METADATA_PASS'),
                 'Unexpected historical replay status: '+script)
            receipts.append({'script':script,'status':receipt['status'],
                             'python_optimization':0,'assertions_enabled':True,
                             'receipt_sha256':sha(output.read_bytes())})
        # The R721 model stage has five accepted mathematical verifiers, but
        # no aggregate dispatcher. Merely validating its ledger would omit
        # their proofs from a claimed full historical replay.
        next_checks = json.loads((target/NEXT_ACCEPTED).read_text())['verifiers']
        need(len(next_checks) == len(set(next_checks)) == 5,
             'Complete historical R721 verifier coverage')
        frozen_sources = json.loads((target/MANIFEST).read_text())
        need(all(script in frozen_sources and script.endswith('.py') for script in next_checks),
             'Historical R721 verifier is not source-bound')
        if historical:
            for script in next_checks:
                command = [sys.executable, str(target/script)]
                result = subprocess.run(command,cwd=target,env=env,capture_output=True,text=True)
                need(result.returncode == 0,'Frozen R721 replay failed: '+script+'\n'+result.stdout+result.stderr)
                receipts.append({'script':script,'status':'PASS','python_optimization':0,
                                 'assertions_enabled':True,
                                 'stdout_stderr_sha256':sha((result.stdout+result.stderr).encode())})
        # Legacy R721 producers regenerate receipts by default. Those writes
        # occur only in this disposable copy and must reproduce the accepted
        # bytes exactly; the live checkout is never their working directory.
        for name, digest in frozen_sources.items():
            need(sha((target/name).read_bytes()) == digest,
                 'Historical replay changed a frozen accepted source: '+name)
    need(baseline(repo) == identity,'Live historical inputs changed during isolated replay')
    return {**identity,'status':'PASS','mode':'full historical rank-eight replay'if historical else 'historical source and receipt validation',
            'mathematical_replay_performed':historical,'checks':receipts,
            'optimized_python_requested':bool(optimized),
            'all_mathematical_children_assertions_enabled':True,
            'R721_accepted_mathematical_verifiers':next_checks,
            'R721_mathematical_replay_performed':historical,
            'live_checkout_modified':False}

def research_summary(repo):
    """Read the previous published result in its verified historical context."""
    baseline(repo)
    receipt_path = 'evidence/rank8_research_20261022/publication/replay_normal.json'
    with zipfile.ZipFile(Path(repo)/ARCHIVE) as bundle:
        receipt = json.loads(bundle.read(PREFIX+receipt_path))
    need(receipt['status'] == 'PASS' and receipt['mathematical_replay_performed'],
         'Historical research summary requires a completed published replay')
    keys = ('new_decisions', 'resolved_ids', 'counts', 'baseline_records_preserved',
            'inherited_models_preserved', 'new_models', 'remaining_ids', 'date',
            'ledger', 'ledger_sha256', 'models', 'models_sha256', 'accepted',
            'accepted_sha256', 'baseline_ledger', 'baseline_ledger_sha256',
            'attempts_source', 'evidence')
    return {key: receipt[key] for key in keys}
