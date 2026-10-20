"""Package the M5 continuation and its exact replay sources, without binaries."""
import hashlib,json,zipfile
from pathlib import Path
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];OUT=P/'release/rank7-certified-through-m5.zip'
def require(v,m):
    if not v:raise ValueError(m)
def main():
    report=json.loads((P/'output/m5/replay_normal.json').read_text())
    ledger=P/'output/rank7_ledger.json';digest=hashlib.sha256(ledger.read_bytes()).hexdigest()
    receipts={}
    for mode in ('normal','optimized'):
        receipt=json.loads((P/f'output/m5/replay_{mode}.json').read_text())
        require(receipt['status']=='PASS' and receipt['mode']=='full_exact_replay'
                and receipt['ledger_sha256']==digest
                and receipt['optimized_python']==(mode=='optimized')
                and receipt['new_status_counts']==report['new_status_counts']
                and receipt['new_exclusions_replayed']==report['new_status_counts']['excluded'],
                f'current complete {mode} replay required')
        receipts[mode]=hashlib.sha256((P/f'output/m5/replay_{mode}.json').read_bytes()).hexdigest()
    files={}
    for relative in ['supplements/rank6/software','supplements/rank7/software','supplements/rank7/data','supplements/rank7/output','supplements/rank7/provenance','evidence/rank7_m5_20261019','evidence/rank7_m5_20261020','manuscripts/rank7/papers']:
        for p in (ROOT/relative).rglob('*'):
            if (p.is_file() and not any(part.startswith('.') for part in p.relative_to(ROOT).parts)
                    and '__pycache__' not in p.parts
                    and not (relative == 'evidence/rank7_m5_20261020'
                             and p.name.endswith(('.progress.json', '_checkpoint.json', '.checkpoint.json')))
                    and p.suffix in {'.py','.cpp','.json','.jsonl','.gz','.txt','.md','.tex','.pdf','.csv'}):
                files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
    for relative in ['supplements/rank7/analyze.py','supplements/rank7/MANIFEST_through_m4.json','supplements/rank7/README.md','supplements/rank7/requirements-m5.txt','supplements/rank7/zero_spectrum7.cpp','supplements/rank7/release/rank7-certified-through-m4.zip',
                     'evidence/unified_20261016/rank7/verify_quadratic_center_trace.py',
                     'tools/replay_m5_ci.py']:
        files[relative]=(ROOT/relative).read_bytes()
    files['README.md']=('''# Rank-seven continuation through multiplicity five

AI-generated research; independent human verification and Lean formalization pending.

This archive preserves the earlier 4201 records and supplies all 5805 new records,
exact negative certificates, the Rep(AGL(1,7)) character model, and the open frontier.
The supplied census completeness claim is producer-reported; this continuation
checks source coverage and certificates, not a fresh full census enumeration.

From this directory, with Python 3.12 and a C++17 compiler:

```sh
python -m pip install -r supplements/rank7/requirements-m5.txt
python supplements/rank7/software/verify_m5.py --jobs 4
python -O supplements/rank7/software/verify_m5.py --jobs 4
```

On a slower or shared machine, use `python tools/replay_m5_ci.py --jobs 2`
(and the same command with `python -O`). This runs the complete checker with
the native low-frame enumeration deadline extended from 60 to 1200 seconds;
all domains, arithmetic, output checks and timeout failures remain intact.

Metadata-only checks use `--metadata-only` and do not replay proofs.
SciPy is optional for discovery routines and is not required for exact replay.
NetworkX is required by the full Morita-dual enumeration for R7_5_4982.
That assertion-based subcertificate runs in an isolated unoptimized child
even when the aggregate dispatcher is invoked with `-O`; its checks remain active.
The immutable earlier full replay package is retained at
`supplements/rank7/release/rank7-certified-through-m4.zip`.
The current manuscript is `manuscripts/rank7/papers/manuscript.pdf`.
''').encode()
    manifest={name:hashlib.sha256(raw).hexdigest() for name,raw in sorted(files.items())}
    current={'title':'Rank-seven Grothendieck rings: certified exclusions, model, and open frontier through multiplicity five','date':'2026-10-20','new_status_counts':report['new_status_counts'],'ledger_sha256':digest,'normal_replay_sha256':receipts['normal'],'optimized_replay_sha256':receipts['optimized'],'files_sha256':manifest}
    manifest_bytes=(json.dumps(current,indent=2)+'\n').encode();(P/'MANIFEST.json').write_bytes(manifest_bytes);files['supplements/rank7/MANIFEST.json']=manifest_bytes
    manifest['supplements/rank7/MANIFEST.json']=hashlib.sha256(manifest_bytes).hexdigest();files['SHA256SUMS.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    OUT.parent.mkdir(exist_ok=True);prefix='rank7-certified-through-m5/'
    with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            info=zipfile.ZipInfo(prefix+name,date_time=(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    print(json.dumps({'path':str(OUT),'files':len(files),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
