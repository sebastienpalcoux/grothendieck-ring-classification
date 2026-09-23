"""Build a checksum-indexed, self-contained rank-seven research bundle.

Run after both the ordinary and optimized full-ledger verifiers have passed.
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
    'data/oriented_verified_certificates.json',
    'output/rank7_ledger.json','output/rank7_model_catalog.json',
    'output/rank7_summary.json','output/rank7_verification_report.json',
    'papers/manuscript.tex','papers/manuscript.pdf',
    'papers/generated_tables.tex','papers/generate_tables.py',
]
code=sorted(x.relative_to(ROOT).as_posix() for x in (ROOT/'software').iterdir()
            if x.suffix in {'.py','.cpp'})
files=sorted(set(exact+code))
summary=json.loads((ROOT/'output/rank7_summary.json').read_text())
report=json.loads((ROOT/'output/rank7_verification_report.json').read_text())
assert report['normal_passed'] and report['optimized_passed']
assert report['verified']==sum(summary['ring_counts'].values())==4201
assert summary['model_count']==16 and summary['max_multiplicity']==4
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}
manifest={'title':'Rank-seven Grothendieck rings: certified exclusions and models through multiplicity four',
          'source_repository_commit':summary['source_commit'],
          'source_sha256':summary['source_sha256'],'files_sha256':hashes}
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for name in files:
        info=zipfile.ZipInfo('rank7-certified-through-m4/'+name,
                             date_time=(2026,9,23,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,(ROOT/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,
                   compresslevel=8)
    info=zipfile.ZipInfo('rank7-certified-through-m4/MANIFEST.json',
                         date_time=(2026,9,23,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o644<<16
    z.writestr(info,json.dumps(manifest,indent=2,sort_keys=True)+'\n',
               compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
print(OUT)
print('SHA256',hashlib.sha256(OUT.read_bytes()).hexdigest())
