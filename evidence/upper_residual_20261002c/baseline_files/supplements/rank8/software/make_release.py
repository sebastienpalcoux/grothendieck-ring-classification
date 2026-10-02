"""Freeze the final checked rank-eight paper, ledger and full replay repository.

Usage: python3 software/make_release.py /path/to/verified/rank7_ledger.json
Use --check-inputs to validate final inputs without writing an archive.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publication_helpers():
    candidates = [ROOT/'verification-repository']
    candidates.extend(p/'verification-repository' for p in ROOT.parents)
    candidates.extend(ROOT.parents)
    for repo in candidates:
        helper = repo/'supplements/rank7/build_release.py'
        if helper.is_file() and (repo/'tools/verify_upper_residual_20261002b.py').is_file():
            spec = importlib.util.spec_from_file_location('upper_release_shared_helpers',helper)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return repo,module
    raise FileNotFoundError('The complete current verification repository is required')


def main(rank7_source: Path, check_only=False):
    repo, helper = publication_helpers()
    latest = helper.checked_upper_stage(repo)
    rank7_source = rank7_source.resolve()
    report = json.loads((ROOT/'verification/report.json').read_text())
    require(report.get('fully_checked') is True and report['census_size'] == 973,
            'Previous rank-eight full verification')
    require(report.get('previous_negative_records_unchanged') is True and report.get('positive_import_verified') is True,
            'Previous rank-eight preservation flags')
    require(report.get('upper_residual_update_verified') is True, 'Latest rank-eight stage not verified')
    counts = json.loads((ROOT/'data/classification_counts.json').read_text())
    require(counts == report['counts'], 'Rank-eight report counts')
    decisions = json.loads((ROOT/'data/decisions.json').read_text())
    require(len(decisions) == 973 and len({x['id'] for x in decisions}) == 973, 'Rank-eight census coverage')
    tally = dict(collections.Counter(x['status'] for x in decisions))
    require(tally == latest['status_totals']['8'], 'Latest rank-eight receipt totals')
    for band in counts:
        rows = [x for x in decisions if x['multiplicity'] == band['multiplicity']]
        require(band == dict(multiplicity=band['multiplicity'],fusion_rings=len(rows),
                    excluded=sum(x['status']=='excluded' for x in rows),
                    realized=sum(x['status']=='unitarily_realized' for x in rows),
                    unresolved=sum(x['status']=='unresolved' for x in rows)),
                'Rank-eight multiplicity partition')

    original = json.loads((ROOT/'data/rank7_certified_negative_subrings.json').read_text())
    imported = {x['id']:x for x in original}
    require(len(imported) == 4 and set(imported) == {'R7_2_64','R7_2_207','R7_2_221','R7_2_289'},
            'Imported rank-seven negative inventory')
    rank7 = json.loads(rank7_source.read_text())
    require(len(rank7) == 4201 and len({x['id'] for x in rank7}) == 4201, 'Rank-seven census coverage')
    require(dict(collections.Counter(x['status'] for x in rank7)) == latest['status_totals']['7'],
            'Rank-seven parent ledger is stale')
    parent = {x['id']:x for x in rank7 if x['id'] in imported}
    require(len(parent) == 4, 'Missing imported rank-seven negative')
    for rid,x in imported.items():
        y = parent[rid]
        require(y['status'] == 'excluded' and y['tensor'] == x['tensor']
                and y['certificate'] == x['certificate'], 'Imported parent changed '+rid)

    signed = json.loads((ROOT/'experimental_signed/signed_certified_campaign.json').read_text())
    require(len(signed['entries']) == 75, 'Historical signed witness inventory')
    for x in signed['entries']:
        p = ROOT/'experimental_signed/certificates'/(x['id']+'.json')
        require(digest(p) == x['certificate_sha256'], 'Signed certificate changed '+x['id'])

    stages = list(csv.DictReader((ROOT/'data/exclusion_stages.csv').open()))
    require(stages and len(stages) % 2 == 0, 'Two multiplicity bands per exclusion stage')
    require(len({(x['stage'],x['multiplicity']) for x in stages}) == len(stages), 'Duplicate stage row')
    by = {}
    cumulative = {1:0,2:0}
    bands = {x['multiplicity']:x for x in counts}
    for x in stages:
        m = int(x['multiplicity']); n = int(x['new_exclusions'])
        require(m in (1,2) and n >= 0, 'Invalid exclusion stage count')
        by.setdefault(x['stage'],{})[str(m)] = n
        cumulative[m] += n
        require(int(x['remaining_after']) == bands[m]['fusion_rings']-cumulative[m],
                'Stage remaining means nonexcluded, including models: '+x['stage'])
    require(all(set(x) == {'1','2'} for x in by.values()), 'Incomplete stage multiplicities')
    require(all(cumulative[m] == bands[m]['excluded'] for m in (1,2)), 'Stage exclusions differ from ledger')
    first = [{'criterion':k,
              'first_excluding_multiplicity_within_complete_source':next((int(m) for m in ('1','2') if v[m]>0),None),
              'new_exclusions_by_exact_multiplicity':v} for k,v in by.items()]
    first_payload = json.dumps({'source_complete_through_multiplicity':2,
        'does_not_establish_criterion_stabilization':True,'criteria_in_order':first},indent=2)+'\n'

    sources = {}
    for directory,patterns in (
        ('data',('*.json','*.csv','*.gz','*.jl')),
        ('software',('*.py','*.cpp')),
        ('experimental_signed',('*.py','*.cpp','*.json','README.md')),
        ('experimental_signed/certificates',('*.json',)),
        ('paper',('*.tex','*.pdf','*.md')),
        ('verification',('*.json',))):
        for pattern in patterns:
            for p in (ROOT/directory).glob(pattern):
                if p.is_file():
                    sources[p.relative_to(ROOT).as_posix()] = p
    sources['README.md'] = ROOT/'README.md'
    sources['data/criterion_first_occurrence.json'] = first_payload.encode()
    evidence = repo/'evidence/anyonwiki'
    for p in evidence.rglob('*'):
        if helper.portable_file(p):
            sources['evidence/anyonwiki/'+p.relative_to(evidence).as_posix()] = p
    sources.update(helper.verification_sources(repo))
    # The derived criterion table must have identical bytes in the outer bundle
    # and its replay repository. Otherwise its post-collection write would make
    # the miniature copy disagree with the already-computed archive manifest.
    sources['verification-repository/supplements/rank8/data/criterion_first_occurrence.json'] = first_payload.encode()
    require((ROOT/'paper/rank8.pdf').is_file(), 'Final rank-eight PDF is missing')
    require(len(sources) >= 130, 'Incomplete archive source inventory')
    provenance = {
        'status':'checked rank-eight categorification frontier through complete multiplicity two',
        'source_fusion_census_commit':'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
        'source_uncompressed_sha256':'97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600',
        'rank7_parent_source_ledger_sha256':digest(rank7_source),
        'rank7_inherited_negative_ids':sorted(imported),
        'positive_model_count':tally['unitarily_realized'], 'source_record_count':973,
        'excluded_count':tally['excluded'], 'unresolved_count':tally['unresolved'],
        'signed_exact_witnesses':75, 'counts':counts,
        'upper_stage_changed_records':latest['changed_records'],
        'normal_and_optimized_upper_stage_checked':True,
        'self_contained_verification_root':'verification-repository',
        'files':{name:{'sha256':helper.digest(p),'bytes':len(helper.source_bytes(p))}
                 for name,p in sorted(sources.items())},
    }
    if check_only:
        print(json.dumps({'status':'PASS','archive_inputs':len(sources),'changed_records':latest['changed_records']}))
        return
    (ROOT/'data/criterion_first_occurrence.json').write_text(first_payload)
    manifest = ROOT/'manifest.json'
    manifest.write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
    sources['manifest.json'] = manifest
    archive = ROOT/'rank8-verified-supplement.zip'
    with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as zf:
        for name,p in sorted(sources.items()):
            info = ZipInfo('rank8/'+name,date_time=(2026,10,2,0,0,0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info,helper.source_bytes(p),compress_type=ZIP_DEFLATED,compresslevel=9)
    print('FROZEN',archive,'files',len(sources),'zip_sha256',digest(archive),
          'manifest_sha256',digest(manifest),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rank7_source',type=Path,help='Final fully verified rank-seven ledger')
    parser.add_argument('--check-inputs',action='store_true',help='Validate inputs without writing a ZIP')
    args = parser.parse_args()
    main(args.rank7_source,args.check_inputs)
