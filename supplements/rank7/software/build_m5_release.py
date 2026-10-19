"""Package the M5 continuation and its exact replay sources, without binaries."""
import hashlib,json,zipfile
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'release/rank7-certified-through-m5.zip'
def require(v,m):
    if not v:raise ValueError(m)
def main():
    report=json.loads((P/'output/m5/replay_normal.json').read_text())
    ledger=P/'output/rank7_ledger.json';digest=hashlib.sha256(ledger.read_bytes()).hexdigest()
    require(report['status']=='PASS' and report['mode']=='full_exact_replay' and report['ledger_sha256']==digest,'current exact replay required')
    files={}
    for relative in ['supplements/rank7/software','supplements/rank7/data','supplements/rank7/output','supplements/rank7/provenance','evidence/rank7_m5_20261019','manuscripts/rank7/papers']:
        for p in (ROOT/relative).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix in {'.py','.cpp','.json','.jsonl','.gz','.txt','.md','.tex','.pdf','.csv'}:
                files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
    for relative in ['supplements/rank7/analyze.py','supplements/rank7/MANIFEST_through_m4.json','supplements/rank7/README.md','supplements/rank7/zero_spectrum7.cpp','supplements/rank7/release/rank7-certified-through-m4.zip']:
        files[relative]=(ROOT/relative).read_bytes()
    files['README.md']=('''# Rank-seven continuation through multiplicity five

AI-generated research; independent human verification and Lean formalization pending.

This archive preserves the earlier 4201 records and supplies all 5805 new records,
exact negative certificates, the Rep(AGL(1,7)) character model, and the open frontier.
The supplied census completeness claim is producer-reported; this continuation
checks source coverage and certificates, not a fresh full census enumeration.

From this directory, with Python3, SymPy, NumPy and a C++17 compiler:

```sh
python supplements/rank7/software/verify_m5.py --jobs 4
python -O supplements/rank7/software/verify_m5.py --jobs 4
```

Metadata-only checks use `--metadata-only` and do not replay proofs.
SciPy is optional for discovery routines and is not required for exact replay.
The immutable earlier full replay package is retained at
`supplements/rank7/release/rank7-certified-through-m4.zip`.
The current manuscript is `manuscripts/rank7/papers/manuscript.pdf`.
''').encode()
    manifest={name:hashlib.sha256(raw).hexdigest() for name,raw in sorted(files.items())}
    current={'title':'Rank-seven Grothendieck rings: certified exclusions, model, and open frontier through multiplicity five','date':'2026-10-19','new_status_counts':report['new_status_counts'],'ledger_sha256':digest,'normal_replay_sha256':hashlib.sha256((P/'output/m5/replay_normal.json').read_bytes()).hexdigest(),'files_sha256':manifest}
    manifest_bytes=(json.dumps(current,indent=2)+'\n').encode();(P/'MANIFEST.json').write_bytes(manifest_bytes);files['supplements/rank7/MANIFEST.json']=manifest_bytes
    manifest['supplements/rank7/MANIFEST.json']=hashlib.sha256(manifest_bytes).hexdigest();files['SHA256SUMS.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    OUT.parent.mkdir(exist_ok=True);prefix='rank7-certified-through-m5/'
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(prefix+name,date_time=(2026,10,19,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'path':str(OUT),'files':len(files),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
