#!/usr/bin/env python3
"""Package the accepted E21 realization and exact creative-stage evidence.

The previous scientific archive remains byte-exact inside the package, so
historical proofs are replayed in their original context. Current routers,
the new ledger, model catalogue and new receipts have separate bindings.
"""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
import rank8_creative_20261022 as stage
import rank8_creative_history as history
from verify_rank8_creative_20261022 import check_reports

ROOT=Path(__file__).resolve().parents[1]
PREFIX='rank8-certified-creative-20261022/'

def raw_json(value):
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=ROOT)
    args=parser.parse_args();repo=args.repo.resolve()
    summary=stage.validate_ledger(repo)
    inventory=stage.source_inventory(repo)
    manifest_sha,receipts=check_reports(repo,summary,inventory)
    history.baseline(repo)
    files={}
    with zipfile.ZipFile(repo/history.ARCHIVE)as old:
        for name in old.namelist():
            local=name[len(history.PREFIX):]
            if local not in ('README.md','SHA256SUMS.json'):
                files[local]=old.read(name)
    paths=set(inventory)
    paths.add(stage.PUBLICATION+'/source_manifest.json')
    paths.update(p.relative_to(repo).as_posix()for p in (repo/stage.PUBLICATION).rglob('*')if p.is_file())
    # Current rank-eight article and all of its TeX inputs are included for
    # readers; the proof receipt inventory is separately bound above.
    for directory in ('manuscripts/rank8/paper','supplements/rank8/paper'):
        paths.update(p.relative_to(repo).as_posix()for p in (repo/directory).rglob('*')
                     if p.is_file()and p.suffix in ('.tex','.pdf','.bib','.sty','.cls'))
    for name in paths:
        files[name]=(repo/name).read_bytes()
    files['README.md']=(
        '# Rank-eight E21 realization and creative research\n\n'
        'Exact multiplicity three: 3506 general exclusions, 16 unitary models, 5 unresolved.\n'
        'Through multiplicity three: 4402 general exclusions, 93 unitary models, 5 unresolved.\n\n'
        'R8_3_982 is the neutral triality component of the known unitary E21 chiral category. '
        'Read evidence/rank8_creative_20261022/README.md and r982/E21_MODEL.md for the precise construction, source graph and exact coefficient identification.\n\n'
        'Install the supplied Python requirements, then run from this directory:\n\n'
        '```sh\npython tools/verify_rank8_creative_20261022.py\n'
        'python -O tools/verify_rank8_creative_20261022.py\n```\n\n'
        'The default replays the new targeted mathematics. --metadata-only checks source identities and both published replay receipts. '
        '--historical additionally replays the prior rank-eight chain from the nested byte-exact scientific archive. '
        'Invoke historical verifiers through that option: the current publication routers intentionally describe the newer ledger. '
        'Current proofs and exact checks are subject to independent mathematical review; the five remaining candidates are not established exotic categories.\n'
    ).encode()
    checks={name:stage.sha(content)for name,content in sorted(files.items())}
    files['SHA256SUMS.json']=raw_json(checks)
    target=repo/stage.ARCHIVE;target.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as bundle:
        for name,content in sorted(files.items()):
            info=zipfile.ZipInfo(PREFIX+name,date_time=(2026,10,22,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
            bundle.writestr(info,content,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(target)as bundle:
        stage.need(len(bundle.namelist())==len(files),'Exact archive member count')
        for name,digest in checks.items():
            stage.need(stage.sha(bundle.read(PREFIX+name))==digest,'Archive round-trip: '+name)
    stage.need(stage.source_inventory(repo)==inventory,'Sources changed while packaging')
    report={'schema':'rank8-creative-20261022-package/v1','status':'PASS',
            'archive':stage.ARCHIVE,'archive_sha256':stage.sha(target.read_bytes()),
            'archive_bytes':target.stat().st_size,'members':len(files),
            'source_manifest_sha256':manifest_sha,'targeted_replay_receipt_sha256':receipts,
            'historical_archive_sha256':history.ARCHIVE_SHA256,
            'classification':summary,
            'scope':'Source-bound package and byte-exact round-trip; extraction replay is a separate check.'}
    (repo/stage.EVIDENCE/'package.json').write_bytes(raw_json(report))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
