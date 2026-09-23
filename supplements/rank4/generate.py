#!/usr/bin/env python3
"""Regenerate the bounded classification with exact arithmetic and resumable stages.

Completed per-ring records are checkpoints, not trusted proof: verify.py replays
all mathematical witnesses and exhaustive searches from the pinned fusion data.
"""
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,io,json,subprocess,sys,time
from contextlib import contextmanager
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from census_data import iter_parameters,record_metadata,read_manifest


@contextmanager
def deterministic_gzip(path):
    with path.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',compresslevel=6,fileobj=raw,mtime=0) as compressed:
            with io.TextIOWrapper(compressed,encoding='utf-8',newline='\n') as text:
                yield text


def rows(path):
    with (gzip.open(path,'rt') if path.suffix=='.gz' else path.open()) as f:
        for line in f:yield json.loads(line)


def merge(output):
    """Join by input identity, never by status or mathematical classification."""
    from exact import require
    base=ROOT/'certificates';survivors={}
    for path in (base/'stage_easy.jsonl',base/'stage_signed.jsonl'):
        if path.exists():
            for r in rows(path):
                sid=r['source_index']
                if r.get('certificate') is not None:survivors[sid]=r
                elif sid not in survivors:survivors[sid]=r
    exclusions=iter(rows(base/'stage_dnumber/excluded.jsonl.gz'));pending=next(exclusions,None)
    counts=Counter();kinds=Counter();unresolved=[];manifest=read_manifest()
    output.parent.mkdir(parents=True,exist_ok=True);temporary=output.with_suffix(output.suffix+'.tmp')
    with deterministic_gzip(temporary) as f:
        header={'schema':2,'scope':'rank4_multiplicity_at_most_128','bound':128,'records':manifest['rings'],
            'census_commit':manifest['commit'],'parameters_sha256':manifest['parameters_gz_sha256'],
            'layout':'One header followed by one record per parameter source line in source order.'}
        f.write(json.dumps(header,separators=(',',':'))+'\n')
        for sid,tag,p in iter_parameters():
            if pending is not None and pending['source_index']==sid:
                r=pending;pending=next(exclusions,None)
            else:r=survivors.pop(sid,None)
            require(r is not None,'missing stage record for source index '+str(sid))
            require(r['tag']==tag and tuple(r['parameters'])==p,'stage input mismatch')
            c=r.get('certificate');status='unresolved' if c is None else ('realized' if c['kind']=='model' else 'excluded')
            if c is None:unresolved.append(sid)
            else:kinds[c['kind']]+=1
            counts[status]+=1
            row={**record_metadata(sid,tag,p),'status':status,'certificate':c}
            if c is None:row['unresolved_reason']=r.get('unresolved_reason') or r.get('error') or 'No criterion supplied a witness.'
            f.write(json.dumps(row,separators=(',',':'))+'\n')
        require(pending is None and not survivors,'extra stage records beyond census')
    temporary.replace(output)
    summary={'scope':header['scope'],'records':sum(counts.values()),'counts':dict(counts),'top_level_criteria':dict(kinds),
        'unresolved_source_indices':unresolved,'certificate_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'verified':False,'note':'Generation report only; see verification/summary.json for independently replayed evidence.'}
    (base/'generation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    return 0 if not unresolved else 2


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--workers',type=int,default=4)
    p.add_argument('--engine',choices=['cpp','python'],default='cpp');p.add_argument('--merge-only',action='store_true')
    p.add_argument('--output',type=Path,default=ROOT/'certificates/classification.jsonl.gz');args=p.parse_args()
    if not args.merge_only:
        from audit import audit_census_inputs
        audit_census_inputs(ROOT)
        stage=ROOT/'certificates/stage_dnumber';summary=stage/'summary.json'
        if summary.exists():
            report=json.loads(summary.read_text());manifest=read_manifest()
            if report['checked']!=manifest['rings'] or report['input_sha256']!=manifest['parameters_gz_sha256']:
                raise ValueError('incompatible d-number checkpoint; move it aside and rerun')
        else:subprocess.run([sys.executable,str(ROOT/'stage_dnumber.py'),'--input',str(ROOT/'data/parameters_128.txt.gz')],check=True)
        subprocess.run([sys.executable,str(ROOT/'stage_classify.py'),'--phase','easy','--workers',str(args.workers)],check=True)
        if not (ROOT/'data/signed_universal_128_manifest.json').exists():
            subprocess.run([sys.executable,str(ROOT/'build_signed_catalog.py'),'--workers',str(args.workers),'--threads',str(args.workers)],check=True)
        signed_input=ROOT/'certificates/stage_signed_input.jsonl'
        with signed_input.open('w') as f:
            for r in rows(ROOT/'certificates/stage_easy.jsonl'):
                if r.get('certificate') is None:f.write(json.dumps(r,separators=(',',':'))+'\n')
        subprocess.run([sys.executable,str(ROOT/'stage_classify.py'),'--phase','signed','--workers',str(args.workers),'--engine',args.engine,'--input',str(signed_input),'--output',str(ROOT/'certificates/stage_signed.jsonl')],check=True)
    return merge(args.output)
if __name__=='__main__':sys.exit(main())
