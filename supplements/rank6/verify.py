#!/usr/bin/env python3
"""Check the pinned repository import, model constructions, and exclusion certificates.

Census exhaustiveness and based-isomorphism uniqueness are inherited from the
trusted fusion-ring-census release; this script does not enumerate a census or
repeat its all-tensor verification.
"""
import os,sys
# The runtime may load SymPy during site startup, before this file executes.
# Restart once with the polynomial backend used to generate row-indexed rays.
if os.environ.get('SYMPY_GROUND_TYPES') != 'python':
    os.environ['SYMPY_GROUND_TYPES'] = 'python'
    os.execvpe(sys.executable, sys.orig_argv, os.environ)
for v in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[v]='1'
import json,time,argparse,hashlib,traceback,collections
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P/'software'))
from exact import require
from prepare import key
from import_repository import verify_source
from existence import verify_ledger,positive_registry,POSITIVE_STATUSES,structure_only_records

def worker(o):
    r,c=o;st=time.monotonic()
    try:
        import scipy.optimize
        def forbidden(*a,**k):raise RuntimeError('floating-point linear programming is forbidden during checking')
        scipy.optimize.linprog=forbidden
        scipy.optimize.milp=forbidden
        from check import verify
        verify(r['N'],c)
        return {'id':r['id'],'kind':c['kind'],'passed':True,'seconds':time.monotonic()-st}
    except Exception as e:return {'id':r['id'],'kind':c['kind'],'passed':False,'error':str(e),'traceback':traceback.format_exc(),'seconds':time.monotonic()-st}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--jobs',type=int,default=2);ap.add_argument('--out',default='verification/check.jsonl');ap.add_argument('--proofs-only',action='store_true');a=ap.parse_args()
    st=time.monotonic();rows=json.load(open(P/'data/census.json'));ledger=json.load(open(P/'data/decisions.json'));idx={r['id']:r for r in rows};require(len(idx)==len(rows),'duplicate census ID');source=verify_source(rows);require([r['id'] for r in rows]==[d['id'] for d in ledger],'ledger does not exactly cover census')
    verify_ledger(ledger)
    if not a.proofs_only:
        from positive_models import examples
        from oriented_signed import validate_general
        constructors={name:(R,ref) for name,R,ref in examples()}
        for m in json.load(open(P/'data/constructed_positive_models.json')):
            R,ref=constructors[m['name']];validate_general(R);require(R==m['N'] and key(R)==key(idx[m['id']]['N']),'positive model tensor mismatch')
        from group_theoretical import examples as gt
        constructions={name:(R,aux) for name,R,aux in gt()}
        for m in json.load(open(P/'data/group_theoretical_models.json')):
            R,aux=constructions[m['name']];validate_general(R);require(R==m['N'] and key(R)==key(idx[m['id']]['N']),'group-theoretical model mismatch')
        from additional_models import examples as extra
        constructors_extra={name:(R,ref) for name,R,ref in extra()}
        records=json.load(open(P/'data/additional_positive_models.json'))
        require(set(constructors_extra)=={m['name'] for m in records},'additional constructor registry mismatch')
        for m in records:
            R,ref=constructors_extra[m['name']];validate_general(R);require(R==m['N'] and key(R)==key(idx[m['id']]['N']),'additional positive model mismatch')
        from complete_models import examples as completed
        complete={name:(R,ref) for name,R,ref in completed()}
        entries=json.load(open(P/'data/complete_positive_models.json'))
        require(set(complete)=={m['name'] for m in entries},'complete registry mismatch')
        for m in entries:
            R,ref=complete[m['name']];validate_general(R)
            require(R==m['N'] and key(R)==key(idx[m['id']]['N']),'complete constructor mismatch')
        from twisted_group_models import twisted_s4
        _,aux=twisted_s4()
        require(json.loads(json.dumps(aux))==json.load(open(P/'data/twisted_s4_certificate.json')),'twisted S4 certificate mismatch')
        from literature_models import examples as literature
        lm={name:(R,ref,e) for name,R,ref,e in literature()}
        lr=json.load(open(P/'data/literature_positive_models.json'))
        require(set(lm)=={r['name'] for r in lr},'literature constructor registry mismatch')
        for rec in lr:
            R,ref,e=lm[rec['name']];validate_general(R)
            require(R==rec['N'] and key(R)==key(idx[rec['id']]['N']),'literature full-tensor mismatch')
            require(e==rec['existence'] and ref==rec['reference'],'literature structure or source mismatch')
        from fermionic_products import examples as products, verify_local_certificate
        fm={name:(R,ref,e) for name,R,ref,e in products()}
        fr=json.load(open(P/'data/fermionic_product_models.json'))
        require(set(fm)=={r['name'] for r in fr},'fermionic product constructor registry mismatch')
        for rec in fr:
            R,ref,e=fm[rec['name']];validate_general(R)
            require(R==rec['N'] and key(R)==key(idx[rec['id']]['N']),'fermionic product full-tensor mismatch')
            require(e==rec['existence'] and ref==rec['reference'],'fermionic product source/structure mismatch')
            verify_local_certificate(*rec['parameters'],rec['local_certificate'])
        from exceptional_g2 import examples as g2examples,construct as g2construct
        gm={name:(R,ref,e) for name,R,ref,e in g2examples()}
        gr=json.load(open(P/'data/exceptional_g2_models.json'))
        require(set(gm)=={r['name'] for r in gr},'exceptional G2 registry mismatch')
        for rec in gr:
            R,ref,e=gm[rec['name']];validate_general(R)
            require(R==rec['N'] and key(R)==key(idx[rec['id']]['N']),'exceptional G2 full-tensor mismatch')
            require(ref==rec['reference'] and e==rec['existence'],'exceptional G2 source/structure mismatch')
        require(json.loads(json.dumps(g2construct()[1]))==json.load(open(P/'data/exceptional_g2_certificate.json')),'exceptional G2 source certificate mismatch')
        from near_group_inversion import verify as verify_inversion
        verify_inversion()
        from through7_models import verify as verify_through7_models
        verify_through7_models()
        from residual_models import verify as verify_residual_models
        verify_residual_models()
        from model_catalog import verify_catalog
        verify_catalog()
        print('TRUSTED SOURCE IMPORT AND CONSTRUCTED MODELS VERIFIED',flush=True)
    from oriented_extension import pseudo_check
    for rec in structure_only_records():
        pseudo_check(idx[rec['id']]['N'],rec['certificate'])
    from modular_frontier import verify as verify_modular_frontier
    frontier=verify_modular_frontier()
    work=[(idx[d['id']],d['certificate']) for d in ledger if d['status']=='excluded'];out=P/a.out;out.parent.mkdir(parents=True,exist_ok=True);fail=[]
    with ProcessPoolExecutor(max_workers=a.jobs) as ex,out.open('w') as f:
        for i,z in enumerate(ex.map(worker,work,chunksize=1)):
            f.write(json.dumps(z,separators=(',',':'))+'\n');f.flush()
            if not z['passed']:fail.append(z);print('FAIL',z,flush=True)
            elif i%200==0:print('CHECKED',i+1,'/',len(work),z['id'],flush=True)
    require(not fail,f'{len(fail)} negative certificates failed')
    m1=[d for d in ledger if d['m']==1];require(len(m1)==39 and sum(d['status']=='excluded' for d in m1)==18 and sum(d['status']=='unitarily_realized' for d in m1)==21,'explicit multiplicity-one classification count mismatch')
    positive=set(positive_registry())
    require(positive=={d['id'] for d in ledger if d['status'] in POSITIVE_STATUSES},'positive registry not exhaustive for claimed positives')
    stats={'passed':True,'optimized_python':not __debug__,'census_tensors':len(rows),'unit_fixing_permutations':0,'census_validation':'trusted repository SHA256, coverage and tensor-ID checks','source':source,'negative_certificates':len(work),'structure_only_exclusions':len(structure_only_records()),'frontier':frontier,'counts':dict(collections.Counter(d['status'] for d in ledger)),'seconds':time.monotonic()-st,'ledger_sha256':hashlib.sha256((P/'data/decisions.json').read_bytes()).hexdigest()}
    out.with_suffix('.summary.json').write_text(json.dumps(stats,indent=2)+'\n');print(json.dumps(stats,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
