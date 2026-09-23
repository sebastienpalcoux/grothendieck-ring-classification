#!/usr/bin/env python3
"""Match the pinned census and verify all categorification certificates.

No exclusion is dispatched by a census index. Python -O is supported: proof
conditions use explicit exceptions, never assert statements. Numerical linear
programming is not imported or invoked by this verification command.
"""
import os
for _v in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[_v]='1'
import argparse,collections,concurrent.futures,hashlib,itertools,json,sys,time,traceback
from pathlib import Path
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'software'))
from exact import require
from rings import fingerprint,permute
from census_common import canonical,check_axioms,pinned_prefix,TABLES_SHA256

def check_one(item):
    import unified
    key,R,c=item;st=time.monotonic()
    try:
        require(fingerprint(R)==key,'certificate tensor fingerprint mismatch')
        unified.verify(R,c)
        return {'key':key,'kind':c['kind'],'seconds':round(time.monotonic()-st,6),'okay':True}
    except Exception:
        return {'key':key,'kind':c.get('kind'),'okay':False,'error':traceback.format_exc()}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--skip-regressions',action='store_true',help='check all census and decision certificates, but omit secondary controls')
    a=ap.parse_args();require(1<=a.jobs<=16,'jobs must lie in 1..16')
    start=time.monotonic()
    mode='optimized' if sys.flags.optimize else 'normal'
    out=a.output or P/f'verification/{mode}_verification.json'
    rows=json.load(open(P/'data/classification_tensors.json'))
    pinned,expected_counts=pinned_prefix(18)
    cache=json.load(open(P/'certificates/exclusions.json'))
    front=json.load(open(P/'data/frontier.json'))
    registry=json.load(open(P/'data/positive_models.json'))
    import unified
    require(unified.build_model_registry()==registry,'positive constructions or registered order changed')
    seen=set();order=collections.Counter();counts=collections.Counter()
    tensors={};ledger=[];allocation=collections.Counter();models_seen=set();frontkeys={r['fingerprint']:r for r in front}
    modelmap={canonical(r['tensor']):i for i,r in enumerate(registry)}
    work=[]
    for r in rows:
        R=r['N'];check_axioms(R);key=fingerprint(R);can=canonical(R)
        require(can in pinned and can not in seen,'missing or repeated pinned census ring')
        seen.add(can);tensors[key]=R;m=r['m'];require(m==max(x for M in R for row in M for x in row),'wrong exact multiplicity')
        counts[m]+=1;order[m]+=1
        require(r['local_index']==order[m],'local canonical numbering gap')
        dual=unified.dual(R)
        dtype='S' if dual==list(range(5)) else 'N2' if dual.count(0)==1 and sum(dual[i]!=i for i in range(5))==2 else 'N4'
        require(r['duality_type']==dtype,'tensor duality metadata mismatch')
        model=modelmap.get(can);categories=int(key in cache)+int(model is not None)+int(key in frontkeys)
        require(categories==1,'decision classes overlap or leave a gap')
        rec={'m':m,'j':r['j'],'local_index':r['local_index'],'fingerprint':key}
        if key in cache:
            c=cache[key];work.append((key,R,c));allocation[c['kind']]+=1
            rec.update(general='excluded',pivotal='excluded',spherical='excluded',pseudo_unitary='excluded',unitary='excluded',criterion=c['kind'])
        elif model is not None:
            models_seen.add(model);match=unified.match_model(R,registry);require(match is not None,'positive tensor isomorphism')
            rec.update(general='realized',pivotal='realized',spherical='realized',pseudo_unitary='realized',unitary='realized',criterion='unitary_model',model=match)
        else:
            f=frontkeys[key];require(f['N']==R and f['m']==m,'frontier tensor mismatch')
            require(unified.dual(R)==list(range(5)),'pivotal-to-spherical inference requires self-duality')
            unified.check_sphere(R,f['spherical_certificate'],unified.check_extended_pseudo)
            # Recompute the published dimension and formal-codegree metadata.
            d=unified.higher_traces.quadratic_data(R,gram_prune=True)
            require(d is not None and d['q']==f['dimension_field'],'frontier field')
            require([[str(x) for x in pair] for pair in d['dimensions']]==f['dimensions'],'frontier dimension vector')
            require([str(x) for x in d['global_dimension']]==f['global_dimension'],'frontier global dimension')
            require([{'polynomial':unified.pc(g),'multiplicity':m} for g,m in d['ch'].cf]==f['formal_codegrees'],'frontier formal codegrees')
            rec.update(general='unresolved',pivotal='excluded',spherical='excluded',pseudo_unitary='excluded',unitary='excluded',criterion='spherical_only')
        ledger.append(rec)
    require(seen==pinned,'pinned repository census not fully matched up to isomorphism')
    require(set(cache)=={k for k,R,c in work},'extraneous exclusion certificate')
    require(models_seen==set(range(len(registry))),'positive model not represented')
    require(dict(counts)==expected_counts,'pinned census count mismatch')
    require(len(rows)==len(pinned)==28493,'census total')
    require(sum(counts[m] for m in counts if m<=17)==23413,'classification census endpoint')
    require(len(models_seen)==17 and len(frontkeys)==2 and all(f['m']==18 for f in front),'scope assertion')
    print(f'PASS pinned repository crosswalk, {len(rows)} exact tensors, 17 constructed models, two spherical frontier certificates.',flush=True)
    print(f'Checking {len(work)} tensor-indexed general exclusion certificates on {a.jobs} workers.',flush=True)
    results=[];failed=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for i,r in enumerate(pool.map(check_one,work,chunksize=20),1):
            results.append(r)
            if not r['okay']:
                failed.append(r);print('FAILED',r['key'],r['error'],flush=True)
            if i%2000==0:print(f'{i}/{len(work)} certificates checked; failures={len(failed)}',flush=True)
    detail=P/f'verification/{mode}_certificate_checks.json'
    detail.write_text(json.dumps(results,separators=(',',':'))+'\n')
    require(not failed,f'{len(failed)} certificate failures; see {detail}')
    controls={}
    if not a.skip_regressions:
        from regression_tests import run
        controls=run(rows,cache,registry)
    summary={'status':'PASS','mode':mode,'python':sys.version,'jobs':a.jobs,'pinned_repository_commit':'b86eb6dc6eeeafe5fc5f6906d7b074e0322e9726','pinned_tables_sha256':TABLES_SHA256,'census_total':len(rows),'complete_general_bound':17,'first_general_frontier_multiplicity':18,'frontier_local_indices':[r['local_index'] for r in front],'positive_models':len(models_seen),'general_exclusions':len(work),'criterion_allocation':dict(sorted(allocation.items())),'counts':dict(sorted(counts.items())),'regressions':controls,'seconds':round(time.monotonic()-start,6)}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(summary,indent=2)+'\n')
    (P/'data/decisions.json').write_text(json.dumps(ledger,separators=(',',':'))+'\n')
    print(json.dumps(summary,indent=2),flush=True)
    print('PASS: every accepted decision reconstructed using exact arithmetic.',flush=True)

if __name__=='__main__':main()
