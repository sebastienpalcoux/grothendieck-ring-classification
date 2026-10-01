"""Replay all eleven completion proofs, sharing finite proofs only in-process."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import traceback
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[name]='1'
sys.dont_write_bytecode=True
import m9_completion as proof

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    output=args.output or proof.ROOT/('verification/m9/completion/replay_'+('normal' if __debug__ else 'optimized')+'.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    import scipy.optimize as opt
    def denied(*a,**kw):raise RuntimeError('numerical optimizer forbidden in exact replay')
    opt.linprog=opt.milp=denied
    from check import verify
    manifest=proof.validate_manifest()
    rows={r['id']:r for r in json.loads((proof.ROOT/'data/census.json').read_text())}
    certificate_path=proof.ROOT/'certificates/m9_completion.jsonl'
    records=[json.loads(line) for line in certificate_path.read_text().splitlines()]
    proof.require(len(records)==len(proof.CASES) and {r['id'] for r in records}==set(proof.CASES),'completion records missing or repeated')
    results=[];start=time.monotonic()
    for record in records:
        rid=record['id'];tick=time.monotonic()
        result={'id':rid,'m':9,'tensor_sha256':proof.object_sha(rows[rid]['N']),
                'certificate_sha256':proof.object_sha(record['certificate']),
                'optimized_python':not __debug__,'optimizer_used':False,'bundles':proof.CASES[rid][1]}
        try:
            verify(rows[rid]['N'],record['certificate'])
            result['passed']=True
        except Exception as error:
            result.update(passed=False,diagnostic=str(error),traceback=traceback.format_exc())
        result['seconds']=time.monotonic()-tick;results.append(result)
        report={'complete':len(results)==len(records),'passed':len(results)==len(records) and all(r['passed'] for r in results),
                'count':len(records),'optimized_python':not __debug__,'optimizer_disabled':True,
                'census_sha256':proof.file_sha(proof.ROOT/'data/census.json'),'certificates_sha256':proof.file_sha(certificate_path),
                'proof_manifest_sha256':proof.file_sha(proof.ROOT/proof.MANIFEST),'checker_sha256':manifest['checker_sha256'],
                'results':results,'bundles':proof.cached_receipts(),'seconds':time.monotonic()-start}
        output.write_text(json.dumps(report,indent=2)+'\n')
        print(rid,result['passed'],round(result['seconds'],3),flush=True)
        if not result['passed']:print(result['diagnostic'],flush=True)
    proof.validate_receipt(list(rows.values()),records,report,optimized=not __debug__)
    return 0

if __name__=='__main__':
    raise SystemExit(main())
