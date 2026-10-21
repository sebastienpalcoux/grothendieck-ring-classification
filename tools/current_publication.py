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
    need(revision['schema'] == 'current-document-revision/v1' and revision['date'] in ('2026-10-17', '2026-10-19', '2026-10-20', '2026-10-21'),
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
