#!/usr/bin/env python3
"""Regenerate the signed cover, check positive coverage, and replay all witnesses.

Run this file without options for the complete finite proof. The optional
cached mode explicitly trusts a previously verified global-cover report.
"""
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,json,multiprocessing,platform,sys,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from scope import BOUND,SPEC,CERTIFICATES
from exact import require
from rings import sd_tensor,validate,canonical,fingerprint,canonical_sd_tuple,SD_MASKS

def positive_cover(rows):
    positive=set()
    for p,det in rows:
        images=set()
        for mask in range(8):
            q=tuple(v*(-1 if (mask&SD_MASKS[k]).bit_count()%2 else 1) for k,v in enumerate(p))
            if min(q)>=0:images.add(canonical_sd_tuple(q))
        require(len(images)<=1,'two positive orbits within one signed orbit')
        require(not positive.intersection(images),'repeated positive orbit')
        positive.update(images)
    return positive

def init_worker(engine):
    global MODELS,SEARCH
    from signed import Search
    MODELS=json.loads((ROOT/'data/models.json').read_text())
    SEARCH=Search(engine)

def verify_task(row):
    from dispatch import check
    R=sd_tensor(row['tuple']);validate(R)
    require(fingerprint(R)==row['sha256'],'input tensor digest mismatch')
    check(R,row['certificate'],MODELS,SEARCH)
    return row['certificate']['kind']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--global-workers',type=int,default=4)
    p.add_argument('--global-threads',type=int,default=4)
    p.add_argument('--engine',choices=['cpp','python'],default='cpp')
    p.add_argument('--trust-cached-global',action='store_true',help='trust the supplied verified full-cover report; this mode alone does not establish completeness')
    args=p.parse_args();started=time.monotonic();out=ROOT/'verification';out.mkdir(exist_ok=True)
    for n in (args.workers,args.global_workers,args.global_threads):require(1<=n<=64,'worker guard')
    from global_signed import load_catalog,verify_global_catalog
    rows,manifest=load_catalog()
    if args.trust_cached_global:
        global_proof=json.loads((out/'global_signed_catalog.json').read_text())
        require(global_proof.get('verified') is True,'cached report is not verified')
        for k in ('bound','total_orbits','retained_orbits','catalog_sha256','generator_source_sha256','filter_source_sha256','pipeline_source_sha256'):
            require(global_proof.get(k)==manifest.get(k),'cached catalog identity mismatch: '+k)
        for filename,k in (('enumerate_global_signed.cpp','generator_source_sha256'),('rapid.py','filter_source_sha256'),('global_signed.py','pipeline_source_sha256')):
            require(hashlib.sha256((ROOT/'software'/filename).read_bytes()).hexdigest()==manifest[k],'cached source identity mismatch')
        print('EXPLICIT TRUST: using a cached full-cover verification report.',flush=True)
    else:global_proof=verify_global_catalog(workers=args.global_workers,threads=args.global_threads)
    required=positive_cover(rows);models=json.loads((ROOT/'data/models.json').read_text())
    require(len(models)==SPEC['models'],'wrong model-table size')
    for m in models:validate(m['matrices'])
    require(len({canonical(m['matrices']) for m in models})==len(models),'isomorphic model tensors')
    seen=set();records=[];counts=Counter();model_names=[]
    with gzip.open(CERTIFICATES,'rt') as f:
        header=json.loads(next(f))
        require(header['schema']==SPEC['positive_schema'] and header['bound']==BOUND,'wrong certificate scope')
        require(header['global_catalog_sha256']==manifest['catalog_sha256'],'wrong catalog identity')
        for line in f:
            row=json.loads(line);q=tuple(row['tuple'])
            require(len(q)==10 and all(type(v) is int and 0<=v<=BOUND for v in q),'bad input tuple')
            key=canonical_sd_tuple(q)
            require(key in required and key not in seen,'unrelated or duplicate positive orbit');seen.add(key)
            k=row['certificate']['kind']
            require(row['status']==('realized' if k=='model' else 'excluded'),'unproved status')
            counts[k]+=1;records.append(row)
            if k=='model':model_names.append(row['certificate']['model'])
    require(seen==required and len(records)==header['records'],'positive coverage incomplete')
    require(len(set(model_names))==len(model_names)==SPEC['selfdual_models'],'wrong self-dual model count')
    print(f'COVERAGE: all {len(records)} positive orbits occur exactly once.',flush=True)
    checked=0
    with multiprocessing.Pool(args.workers,initializer=init_worker,initargs=(args.engine,)) as pool:
        for kind in pool.imap_unordered(verify_task,records,chunksize=4):
            checked+=1
            if checked%100==0:print('CHECKED',checked,'of',len(records),flush=True)
    import sympy
    from rapid import BACKEND
    report={'scope':f'Self-dual rank-four complex Grothendieck rings of multiplicity at most {BOUND}',
            'bound':BOUND,'checked_records':checked,'realized':len(model_names),
            'excluded':checked-len(model_names),'unresolved':0,'top_level_criteria':dict(counts),
            'models':model_names,'positive_catalog_coverage':True,'unsigned_census_required':False,
            'global_catalog_regenerated_in_this_run':not args.trust_cached_global,
            'global_catalog_report':global_proof,'certificate_sha256':hashlib.sha256(CERTIFICATES.read_bytes()).hexdigest(),
            'python':platform.python_version(),'sympy':sympy.__version__,'universal_arithmetic_backend':BACKEND,
            'local_search_engine':args.engine,
            'elapsed_seconds':round(time.monotonic()-started,3),
            'interpretation':'Exact certificate replay. Necessity of the categorical criteria and the six non-self-dual models are proved in the manuscript; this is not proof-assistant certification.'}
    (out/'compact_summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {checked} positive orbits; {checked-len(model_names)} exclusions; {len(model_names)} self-dual models; zero unresolved.',flush=True)
    print('Elapsed seconds:',report['elapsed_seconds'],flush=True)
if __name__=='__main__':main()
