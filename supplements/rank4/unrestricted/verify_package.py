#!/usr/bin/env python3
"""Check source/data integrity and the current rank-four manuscript tables.

This checker is independent of Python assertions. Full mathematical-certificate
replay is performed by supplementary/check.py, not by this hash manifest.
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT/'PACKAGE_MANIFEST.json'
TABLES = {
    'source/models.tex': 'models.tex',
    'source/generated_filters.tex': 'generated_filters.tex',
    'source/generated_census.tex': 'generated_census.tex',
    'supplementary/classification/generated_scope.tex': 'generated_scope.tex',
    'audit/quartic_trace13_table.tex': 'quartic_trace13_table.tex',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_paths():
    explicit = {
        'supplementary/model_table.json', 'supplementary/provenance.json',
        'supplementary/classification/scope.json',
        'supplementary/classification/results/certificates.jsonl',
        'supplementary/classification/results/summary.json',
        'supplementary/classification/results/survivors.json',
        'supplementary/classification/verification/exact_model_dimensions_audit.json',
        'audit/quartic_trace13_exact_resolvent_chart.json',
    }
    prefixes = ('supplementary/census/data/', 'supplementary/classification/data/',
                'supplementary/models/', 'verification_receipts/')
    result = []
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        name = path.relative_to(ROOT).as_posix()
        if path.suffix in ('.py', '.cpp', '.md', '.tex') or name in explicit or name.startswith(prefixes) or path.name in ('requirements.txt', 'CENSUS_LICENSE'):
            result.append(path)
    return result


def check_scopes():
    census = json.loads((ROOT/'supplementary/census/data/manifest.json').read_text())
    summary = json.loads((ROOT/'supplementary/classification/results/summary.json').read_text())
    report = json.loads((ROOT/'supplementary/verification_report.json').read_text())
    require(census['number_of_rings'] == summary['census_count'] == report['census_rings'] == 1692,
            'ordinary census count mismatch')
    require(census['type_counts'] == {'S':1642, 'N':50}, 'ordinary duality counts')
    require(summary['excluded'] == report['excluded'] == 1677 and summary['model_count'] == report['models'] == 15,
            'classification totals')
    require(report['passed'] and report['fresh_ordinary_census'] and report['fresh_signed_cover'],
            'fresh complete replay report required')
    require(report['unresolved'] == 0 and report['dimension_exclusive_bound'] == 1000 and report['multiplicity_bound'] == 31,
            'replay scope mismatch')
    require(report['census_sha256'] == digest(ROOT/'supplementary/census/data/rings.jsonl'), 'stale census receipt')
    require(report['ledger_sha256'] == digest(ROOT/'supplementary/classification/results/certificates.jsonl'), 'stale ledger receipt')
    for name in ('normal_deep.json','optimized_deep.json'):
        delivered=json.loads((ROOT/'verification_receipts'/name).read_text())
        require(delivered['passed'] and delivered['deep_checks'] and delivered['fresh_signed_cover'],
                'incomplete delivered deep replay: '+name)
        require(delivered['census_sha256']==report['census_sha256'] and
                delivered['ledger_sha256']==report['ledger_sha256'],
                'delivered replay does not bind the shipped census and ledger: '+name)
    return {'ordinary_census':1692, 'self_dual':1642, 'one_dual_pair':50,
            'exclusions':1677, 'models':15, 'dimension_exclusive_bound':1000,
            'multiplicity_bound':31}


def run(write=False, manuscript_root=None):
    scopes = check_scopes()
    files = {p.relative_to(ROOT).as_posix():digest(p) for p in stable_paths()}
    if write:
        MANIFEST.write_text(json.dumps({'schema':1, 'algorithm':'sha256', 'scope':scopes,
            'files':files, 'interpretation':'Source, deterministic data, generated tables, and delivered replay receipts. Fresh timing logs and mutable replay reports are checked by scope and data identity, not frozen hashes.'}, indent=2)+'\n')
    manifest = json.loads(MANIFEST.read_text())
    require(manifest['schema'] == 1 and manifest['scope'] == scopes, 'integrity manifest scope')
    require(manifest['files'] == files, 'source, data, or delivered receipt differs from manifest')
    if manuscript_root is not None:
        target = Path(manuscript_root).resolve()/'generated/unrestricted'
        for source, name in TABLES.items():
            require((ROOT/source).read_bytes() == (target/name).read_bytes(),
                    'manuscript generated table differs: '+name)
    print('PASS: rank-four package integrity; 1692 inputs, 1677 exclusions, 15 models; '+str(len(files))+' frozen files.')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true', help='maintainer: record a fully replayed package')
    parser.add_argument('--manuscript-root', type=Path, help='rank4/papers directory containing generated/unrestricted')
    args = parser.parse_args()
    run(args.write_manifest, args.manuscript_root)
