"""Build the final checked rank-seven bundle with a complete replay repository.

Both latest-stage normal/optimized receipts and the final PDF are prerequisites.
Use --check-inputs to validate all final inputs without writing an archive.
"""
import argparse
import collections
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT/'release'
OUT = DIST/'rank7-certified-through-m4.zip'
STAGE = 'evidence/upper_residual_20261002b'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_bytes(source):
    return source if isinstance(source, bytes) else source.read_bytes()


def digest(source):
    return hashlib.sha256(source_bytes(source)).hexdigest()


def repository_root():
    candidates = [ROOT/'verification-repository']
    candidates.extend(p/'verification-repository' for p in ROOT.parents)
    candidates.extend(ROOT.parents)
    for p in candidates:
        if (p/'tools/verify_upper_residual_20261002b.py').is_file():
            return p
    raise FileNotFoundError('The complete checked verification repository is required')


def portable_file(path):
    excluded_parts = {'__pycache__','.git','node_modules','release','.pytest_cache'}
    excluded_names = {'restore_selection.json','restore_pending.json'}
    return (path.is_file() and not excluded_parts.intersection(path.parts)
            and path.name not in excluded_names and not path.name.startswith('restore_')
            and path.suffix not in {'.pdf','.zip','.pyc','.pyo','.bin','.o','.so','.log','.aux','.out','.toc'})


def verification_sources(repo):
    """Collect current replay dependencies and exact historical override bytes."""
    repo = Path(repo)
    directories = [
        'supplements/rank7/software','supplements/rank7/data','supplements/rank7/output',
        'supplements/rank7/evidence','supplements/rank7/papers',
        'supplements/rank8/software','supplements/rank8/data','supplements/rank8/verification',
        'supplements/rank8/experimental_signed','supplements/rank8/paper',
        'evidence/anyonwiki','evidence/residual_20261002',STAGE,
        'evidence/upper_residual_20261002b_recovery',
    ]
    sources = {}
    for directory in directories:
        require((repo/directory).is_dir(), 'Missing replay directory '+directory)
        for p in (repo/directory).rglob('*'):
            if portable_file(p):
                sources[p.relative_to(repo).as_posix()] = p
    for name in ['supplements/rank7/analyze.py','supplements/rank7/verify.py',
                 'supplements/rank7/README.md','supplements/rank7/build_release.py',
                 'supplements/rank7/zero_spectrum7.cpp','supplements/rank8/README.md',
                 'tools/verify_upper_residual_20261002b.py',
                 'tools/verify_residual_20261002.py','tools/verify_anyonwiki_import.py']:
        require((repo/name).is_file(), 'Missing replay entrypoint '+name)
        sources[name] = repo/name
    old = json.loads((repo/'evidence/residual_20261002/previous_records.json').read_text())
    for name, expected in old['source_files_sha256'].items():
        require((repo/name).is_file(), 'Missing historical dependency '+name)
        baseline = repo/STAGE/'baseline_files'/name
        require(digest(repo/name) == expected or
                (baseline.is_file() and digest(baseline) == expected),
                'Missing exact historical source bytes '+name)
        sources[name] = repo/name
        if baseline.is_file():
            sources[baseline.relative_to(repo).as_posix()] = baseline
    for name, expected in json.loads((repo/STAGE/'source_files.json').read_text()).items():
        p = (repo/name).resolve()
        require(repo.resolve() in p.parents and p.is_file(), 'Missing pinned current source '+name)
        require(digest(p) == expected, 'Pinned current source changed '+name)
        require(portable_file(p), 'Nonportable pinned source '+name)
        sources[name] = p
    sources['README.md'] = (
        '# Exact upper-rank verification repository\n\n'
        'This directory contains both census sources, current ledgers, new models, '
        'theoretical premise checkers, and exact historical overrides. With Python3 '
        'and SymPy installed, run from this directory:\n\n'
        '```sh\npython3 tools/verify_upper_residual_20261002b.py\n'
        'python3 -O tools/verify_upper_residual_20261002b.py\n```\n\n'
        'The outer rank-seven and rank-eight verify.py entrypoints dispatch here. '
        'Historical verification uses a temporary copy; current ledgers are never '
        'rewritten to obtain a historical pass. General exclusions and scoped '
        'obstructions remain distinct.\n').encode()
    return {'verification-repository/'+name:p for name,p in sorted(sources.items())}


def checked_upper_stage(repo):
    stage = repo/STAGE
    decisions = json.loads((stage/'decisions.json').read_text())
    require(len({x['id'] for x in decisions}) == len(decisions), 'Duplicate current transition')
    totals = {}
    for rank, name in [(7,'supplements/rank7/output/rank7_ledger.json'),
                       (8,'supplements/rank8/data/decisions.json')]:
        ledger = json.loads((repo/name).read_text())
        totals[str(rank)] = dict(collections.Counter(x['status'] for x in ledger))
    reports = []
    for optimized, filename in [(False,'verification_normal.json'),(True,'verification_optimized.json')]:
        report = json.loads((stage/filename).read_text())
        require(report.get('status') == 'PASS' and report.get('python_optimized') is optimized,
                'Latest '+filename+' must pass')
        require(report.get('changed_records') == len(decisions), 'Stale transition receipt '+filename)
        require(report.get('status_totals') == totals, 'Stale ledger totals '+filename)
        require(report.get('previous_negative_records_unchanged') is True
                and report.get('unaffected_records_unchanged') is True,
                'Historical preservation not checked '+filename)
        require(report.get('new_general_exclusions') == sum(x['status']=='excluded' for x in decisions)
                and report.get('new_unitary_models') == sum(x['status']=='unitarily_realized' for x in decisions),
                'Stale decision scope counts '+filename)
        require(report.get('source_manifest_sha256') == hashlib.sha256((stage/'source_files.json').read_bytes()).hexdigest(), 'Stale source manifest receipt '+filename)
        require(report.get('preservation_manifest_sha256') == hashlib.sha256((stage/'previous_records.json').read_bytes()).hexdigest(), 'Stale preservation manifest receipt '+filename)
        reports.append(report)
    a,b = [dict(x) for x in reports]
    a.pop('python_optimized'); b.pop('python_optimized')
    require(a == b, 'Normal and optimized current-stage results differ')
    return reports[0]


def collect_sources(repo):
    names = [
        'README.md','analyze.py','verify.py','build_release.py','zero_spectrum7.cpp',
        'data/rank7_tables.txt.gz','data/lower_rank_positive_models.json',
        'data/integral_rank7_noncomm_published.txt','data/anyonwiki_models.json',
        'data/residual_20261002_exclusions.json','data/residual_20261002_models.json',
        'data/residual_20261002_preservation.json','data/model_catalog.json',
        'data/oriented_verified_certificates.json',
        'output/residual_20261002_verification.json',
        'output/pre_residual_20261002_verification_report.json',
        'output/rank7_ledger.json','output/rank7_model_catalog.json',
        'output/rank7_summary.json','output/rank7_verification_report.json',
        'papers/manuscript.tex','papers/manuscript.pdf','papers/generated_tables.tex',
        'papers/generate_tables.py',
    ]
    sources = {name:ROOT/name for name in names}
    for directory, suffixes in [('software',{'.py','.cpp'}),('papers',{'.tex','.md'}),
                                 ('data',{'.json'}),('output',{'.json'})]:
        for p in (ROOT/directory).glob('*'):
            if p.is_file() and p.suffix in suffixes:
                sources[p.relative_to(ROOT).as_posix()] = p
    # All new TeX inputs are included, rather than a stale fixed filename list.
    evidence = repo/'evidence/anyonwiki'
    for p in evidence.rglob('*'):
        if portable_file(p):
            sources['evidence/anyonwiki/'+p.relative_to(evidence).as_posix()] = p
    sources.update(verification_sources(repo))
    require(all(isinstance(p,bytes) or p.is_file() for p in sources.values()),
            'Missing final paper or release source')
    return sources


def main(check_only=False):
    repo = repository_root()
    latest = checked_upper_stage(repo)
    summary = json.loads((ROOT/'output/rank7_summary.json').read_text())
    report = json.loads((ROOT/'output/rank7_verification_report.json').read_text())
    require(report['normal_passed'] and (report['optimized_passed'] or
            (report.get('previous_negative_records_unchanged') and report.get('positive_import_verified'))),
            'Previous rank-seven verification flags')
    require(report.get('residual_update_verified') and report.get('residual_update_normal_and_optimized_passed'),
            'Historical residual stage not verified')
    require(report.get('upper_residual_update_verified') is True, 'Latest rank-seven stage not verified')
    require(report['verified'] == sum(summary['ring_counts'].values()) == 4201, 'Rank-seven census size')
    require(summary['max_multiplicity'] == 4, 'Rank-seven census bound')
    require(summary['model_count'] == len(json.loads((ROOT/'output/rank7_model_catalog.json').read_text())),
            'Rank-seven model count')
    expected = latest['status_totals']['7']
    require((report['excluded'],report['models'],report['unresolved']) ==
            (expected['excluded'],expected['unitarily_realized'],expected['unresolved']), 'Rank-seven report totals')
    sources = collect_sources(repo)
    manifest = {
        'title':'Rank-seven Grothendieck rings: certified exclusions and models through multiplicity four',
        'source_repository_commit':summary['source_commit'], 'source_sha256':summary['source_sha256'],
        'files_sha256':{name:digest(p) for name,p in sorted(sources.items())},
        'upper_stage_changed_records':latest['changed_records'], 'status_totals':expected,
        'self_contained_verification_root':'verification-repository',
        'normal_and_optimized_upper_stage_checked':True,
    }
    if check_only:
        print(json.dumps({'status':'PASS','archive_inputs':len(sources),'changed_records':latest['changed_records']}))
        return
    DIST.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as archive:
        for name,p in sorted(sources.items()):
            info = zipfile.ZipInfo('rank7-certified-through-m4/'+name,date_time=(2026,10,2,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info,source_bytes(p),compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
        info = zipfile.ZipInfo('rank7-certified-through-m4/MANIFEST.json',date_time=(2026,10,2,0,0,0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        archive.writestr(info,json.dumps(manifest,indent=2,sort_keys=True)+'\n',
                         compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
    print(OUT)
    print('SHA256',digest(OUT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-inputs', action='store_true', help='Validate inputs without writing a ZIP')
    main(parser.parse_args().check_inputs)
