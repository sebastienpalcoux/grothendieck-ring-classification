"""Build a checksum-indexed, self-contained rank-seven research bundle.

Run after the recorded earlier verification and the ordinary and optimized
residual-update verifiers have passed.
No executable binaries, temporary search logs, or proposed models are shipped.
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'release'
DIST.mkdir(exist_ok=True)
OUT=DIST/'rank7-certified-through-m4.zip'
exact=[
    'README.md','analyze.py','verify.py','build_release.py','zero_spectrum7.cpp',
    'data/rank7_tables.txt.gz','data/lower_rank_positive_models.json',
    'data/integral_rank7_noncomm_published.txt',
    'data/anyonwiki_models.json','data/residual_20261002_exclusions.json',
    'data/residual_20261002_models.json','data/residual_20261002_preservation.json',
    'data/model_catalog.json',
    'output/residual_20261002_verification.json','software/verify_residual_20261002.py',
    'output/pre_residual_20261002_verification_report.json',
    'data/oriented_verified_certificates.json',
    'output/rank7_ledger.json','output/rank7_model_catalog.json',
    'output/rank7_summary.json','output/rank7_verification_report.json',
    'papers/manuscript.tex','papers/manuscript.pdf',
    'papers/generated_tables.tex','papers/generate_tables.py',
    'papers/ty_equivariant_models.md',
    'output/ty_equivariant_models_verification.json',
    'output/quaternion_equivariant_model_verification.json',
    'papers/r7_4_2019_chern_proof.md','papers/r7_2_75_proof.md',
    'data/r7_4_2019_chern_certificate.json','data/r7_2_75_certificate.json',
    'output/r7_4_2019_chern_verification.json','output/r7_2_75_verification.json',
    'papers/R2019_CHERN_CLASS_AUDIT.md','data/r7_4_2019_independent_audit.json',
    'papers/R75_GENERAL_EXCLUSION_AUDIT.md','papers/order16_orbit_lemma.md',
    'output/order16_orbit_verification.json',
    'papers/D96_GENERAL_EXCLUSION_PROOF.md','data/d96_premise_certificates.json',
    'output/d96_premise_verification.json',
    'papers/R75_CRITERIA_INDEPENDENT_AUDIT.md','papers/D96_INDEPENDENT_AUDIT.md',
]
code=sorted(x.relative_to(ROOT).as_posix() for x in (ROOT/'software').iterdir()
            if x.suffix in {'.py','.cpp'})
files=sorted(set(exact+code))
sources={p:ROOT/p for p in files}
evidence=ROOT.parents[1]/'evidence/anyonwiki'
for path in evidence.rglob('*'):
    if path.is_file() and '__pycache__'not in path.parts:
        sources['evidence/anyonwiki/'+path.relative_to(evidence).as_posix()]=path
files=sorted(sources)
summary=json.loads((ROOT/'output/rank7_summary.json').read_text())
report=json.loads((ROOT/'output/rank7_verification_report.json').read_text())
assert report['normal_passed'] and (report['optimized_passed'] or
       (report.get('previous_negative_records_unchanged') and report.get('positive_import_verified')))
assert report.get('residual_update_verified') and report.get('residual_update_normal_and_optimized_passed')
assert report['verified']==sum(summary['ring_counts'].values())==4201
assert summary['model_count']==len(json.loads((ROOT/'output/rank7_model_catalog.json').read_text())) and summary['max_multiplicity']==4
hashes={p:hashlib.sha256(sources[p].read_bytes()).hexdigest() for p in files}
manifest={'title':'Rank-seven Grothendieck rings: certified exclusions and models through multiplicity four',
          'source_repository_commit':summary['source_commit'],
          'source_sha256':summary['source_sha256'],'files_sha256':hashes}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for name in files:
        info=zipfile.ZipInfo('rank7-certified-through-m4/'+name,
                             date_time=(2026,9,23,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,sources[name].read_bytes(),compress_type=zipfile.ZIP_DEFLATED,
                   compresslevel=8)
    info=zipfile.ZipInfo('rank7-certified-through-m4/MANIFEST.json',
                         date_time=(2026,9,23,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o644<<16
    z.writestr(info,json.dumps(manifest,indent=2,sort_keys=True)+'\n',
               compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
print(OUT)
print('SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest())
