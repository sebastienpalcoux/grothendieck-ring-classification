#!/usr/bin/env python3
"""Package the complete R3472 proof, preserving historical archive identity.

The new mathematical replay is self-contained. The large unchanged creative
archive is a separately pinned companion for publication/history verification.
"""
from pathlib import Path
import argparse
import json
import zipfile
import rank8_exclusion_20261022 as stage
from verify_rank8_exclusion_20261022 import check_reports

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'rank8-certified-exclusion-20261022/'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    args = parser.parse_args(); repo = args.repo.resolve()
    summary = stage.validate_ledger(repo); inventory = stage.source_inventory(repo)
    manifest_sha,receipts = check_reports(repo,summary,inventory)
    companion = {'path':stage.HISTORICAL_ARCHIVE,'sha256':stage.HISTORICAL_ARCHIVE_SHA256,
                 'bytes':(repo/stage.HISTORICAL_ARCHIVE).stat().st_size}
    paths = set(inventory)-{stage.HISTORICAL_ARCHIVE}
    paths.update(p.relative_to(repo).as_posix() for p in (repo/stage.PUBLICATION).rglob('*') if p.is_file())
    # Publication modules imported by the new router are included even when
    # the standalone mathematical proof does not need them.
    paths.update(p.relative_to(repo).as_posix() for p in (repo/'tools').glob('rank8_*.py'))
    for directory in ('manuscripts/rank8/paper','supplements/rank8/paper'):
        paths.update(p.relative_to(repo).as_posix() for p in (repo/directory).glob('*')
                     if p.is_file() and p.suffix in ('.tex','.pdf','.bib','.sty','.cls'))
    files = {p:(repo/p).read_bytes() for p in sorted(paths)}
    files['EXTERNAL_COMPANIONS.json'] = stage.json_bytes([companion])
    files['README.md'] = (
        '# General complex exclusion of R8_3_3472\n\n'
        'Exact multiplicity three: 3507 general exclusions, 16 unitary models, 4 unresolved.\n'
        'Through multiplicity three: 4403 general exclusions, 93 unitary models, 4 unresolved.\n\n'
        'The complete mathematical proof and its repository-relative dependencies are included. '
        'Install the dependencies documented in evidence/r3472_exclusion_20261022/README.md and run:\n\n'
        '```sh\npython3 evidence/r3472_exclusion_20261022/replay.py\n```\n\n'
        'The terminal arithmetic alone uses only the Python standard library:\n\n'
        '```sh\npython3 evidence/r3472_exclusion_20261022/terminal/check.py\n```\n\n'
        'Run these assertion-based proof commands without -O. The publication coordinator '
        'tools/verify_rank8_exclusion_20261022.py safely supports normal and -O outer invocations '
        'by keeping every mathematical child unoptimized. Its canonical receipts are included.\n\n'
        'Publication metadata and --historical replay additionally require the unchanged creative ZIP '
        'at the path and SHA-256 listed in EXTERNAL_COMPANIONS.json. It is distributed separately '
        'and included by the common publication bundle; it is not duplicated in this compact archive. '
        'The optional historical replay explicitly records a missing-helper repair in an isolated copy. '
        'The frozen historical ZIP is never rewritten.\n\n'
        'The new proof is a general noncategorification theorem. Earlier feasible relaxations and '
        'conditional construction restrictions are retained only as historical research checkpoints. '
        'Independent human mathematical review remains pending.\n'
    ).encode()
    checks = {name:stage.sha(raw) for name,raw in sorted(files.items())}
    files['SHA256SUMS.json'] = stage.json_bytes(checks)
    target = repo/stage.ARCHIVE; target.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as bundle:
        for name,raw in sorted(files.items()):
            info = zipfile.ZipInfo(PREFIX+name,date_time=(2026,10,22,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED; info.external_attr = 0o644 << 16
            bundle.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(target) as bundle:
        stage.need(len(bundle.namelist()) == len(files),'Exact exclusion archive member count')
        for name,digest in checks.items():
            stage.need(stage.sha(bundle.read(PREFIX+name)) == digest,'Archive round-trip: '+name)
    stage.need(stage.source_inventory(repo) == inventory,'Sources changed while packaging')
    report = {'schema':'rank8-exclusion-20261022-package/v1','status':'PASS',
              'archive':stage.ARCHIVE,'archive_sha256':stage.sha(target.read_bytes()),
              'archive_bytes':target.stat().st_size,'members':len(files),
              'source_manifest_sha256':manifest_sha,'targeted_replay_receipt_sha256':receipts,
              'historical_archive_sha256':stage.HISTORICAL_ARCHIVE_SHA256,
              'external_companions':[companion],'classification':summary,
              'scope':'Source-bound complete proof package and exact member round-trip; historical archive is a separately pinned companion.'}
    (repo/stage.EVIDENCE/'package.json').write_bytes(stage.json_bytes(report))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
