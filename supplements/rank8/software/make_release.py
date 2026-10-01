"""Freeze a checked rank-eight manuscript, decision ledger, and verifier bundle.

Usage: python3 software/make_release.py /path/to/verified/rank7_ledger.json
The imported rank-seven negatives must actually occur in that verified ledger.
This script records its digest, not its 4201 full multiplication tables, in
the rank-eight release; all four exact proofs and tensors are already bundled.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]


def digest(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(rank7_source:Path)->None:
    rank7_source=rank7_source.resolve()
    report=json.loads((ROOT/'verification/report.json').read_text())
    assert report['fully_checked'] and report['census_size']==973
    counts=json.loads((ROOT/'data/classification_counts.json').read_text())
    assert counts==report['counts']
    decisions=json.loads((ROOT/'data/decisions.json').read_text())
    for band in counts:
        rows=[x for x in decisions if x['multiplicity']==band['multiplicity']]
        assert band==dict(multiplicity=band['multiplicity'],fusion_rings=len(rows),
            excluded=sum(x['status']=='excluded'for x in rows),
            realized=sum(x['status']=='unitarily_realized'for x in rows),
            unresolved=sum(x['status']=='unresolved'for x in rows))

    original=json.loads((ROOT/'data/rank7_certified_negative_subrings.json').read_text())
    imported={z['id']:z for z in original}
    assert len(imported)==4 and set(imported)=={'R7_2_64','R7_2_207','R7_2_221','R7_2_289'}
    rank7=json.loads(rank7_source.read_text())
    assert len(rank7)==4201
    parent={z['id']:z for z in rank7 if z['id'] in imported}
    assert len(parent)==4
    for rid,z in imported.items():
        parent_row=parent[rid]
        assert parent_row['status']=='excluded',rid
        assert parent_row['tensor']==z['tensor'],rid
        assert parent_row['certificate']==z['certificate'],rid

    signed=json.loads((ROOT/'experimental_signed/signed_certified_campaign.json').read_text())
    assert len(signed['entries'])==75
    for z in signed['entries']:
        path=ROOT/'experimental_signed/certificates'/(z['id']+'.json')
        assert digest(path)==z['certificate_sha256'],z['id']

    stages=list(csv.DictReader((ROOT/'data/exclusion_stages.csv').open()))
    assert len(stages)==30
    by={}
    for row in stages:
        by.setdefault(row['stage'],{})[str(row['multiplicity'])]=int(row['new_exclusions'])
    first=[{'criterion':k,
            'first_excluding_multiplicity_within_complete_source':
            next((int(m) for m in ('1','2') if v[m]>0),None),
            'new_exclusions_by_exact_multiplicity':v} for k,v in by.items()]
    (ROOT/'data/criterion_first_occurrence.json').write_text(json.dumps({
        'source_complete_through_multiplicity':2,
        'does_not_establish_criterion_stabilization':True,
        'criteria_in_order':first},indent=2)+'\n')

    files=[]
    for directory,patterns in (
        ('data',('*.json','*.csv','*.gz')),
        ('software',('*.py','*.cpp')),
        ('experimental_signed',('*.py','*.cpp','*.json','README.md')),
        ('experimental_signed/certificates',('*.json',)),
        ('paper',('*.tex','*.pdf')),
        ('verification',('report.json',))):
        folder=ROOT/directory
        for pattern in patterns:
            files.extend(p for p in folder.glob(pattern) if p.is_file())
    files.append(ROOT/'README.md')
    evidence=ROOT.parents[1]/'evidence/anyonwiki'
    external=[p for p in evidence.rglob('*')if p.is_file()and '__pycache__'not in p.parts]
    def relative(p):
        return p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT)else 'evidence/anyonwiki/'+p.relative_to(evidence).as_posix()
    files=sorted(set(files+external),key=relative)
    assert len(files)>=130
    provenance={
        'status':'checked rank-eight categorification frontier through complete multiplicity two',
        'source_fusion_census_commit':'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726',
        'source_uncompressed_sha256':'97b86d2de8ca0352c5c6e14686cd1d43dbd52180dc53b2ff1ccf7a61788c9600',
        'rank7_parent_source_ledger_sha256':digest(rank7_source),
        'rank7_inherited_negative_ids':sorted(imported),
        'positive_model_count':sum(x['status']=='unitarily_realized'for x in decisions),
        'source_record_count':973,
        'excluded_count':824,
        'unresolved_count':sum(x['status']=='unresolved'for x in decisions),
        'signed_exact_witnesses':75,
        'counts':counts,
        'files':{relative(p):{'sha256':digest(p),'bytes':p.stat().st_size}
                 for p in files}}
    manifest=ROOT/'manifest.json'
    manifest.write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
    files.append(manifest)
    archive=ROOT/'rank8-verified-supplement.zip'
    with ZipFile(archive,'w',compression=ZIP_DEFLATED,compresslevel=9) as zf:
        for p in files:
            name=relative(p)
            info=ZipInfo('rank8/'+name,date_time=(2026,9,23,0,0,0))
            info.compress_type=ZIP_DEFLATED
            zf.writestr(info,p.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)
    print('FROZEN',archive,'files',len(files),'zip_sha256',digest(archive),
          'manifest_sha256',digest(manifest),flush=True)


if __name__=='__main__':
    assert len(sys.argv)==2,'pass the final rank-seven ledger path after its whole-ledger verifier passes'
    main(Path(sys.argv[1]))
