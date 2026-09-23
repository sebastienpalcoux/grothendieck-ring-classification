#!/usr/bin/env python3
"""Resumable exact classification of the d-number survivors.

Only completed records are appended. --phase easy defers signed enumeration;
--phase full runs every remaining established criterion; --phase signed
uses the signed-lift criteria directly on the easy-stage residuals. No previous status
or catalogue label is accepted as mathematical evidence.
"""
import argparse,json,sys,time,traceback,multiprocessing,os
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))

def initialize(phase,engine):
    global PHASE,MODELS,SEARCH,KEYS
    from dispatch import canonical
    PHASE=phase;MODELS=json.loads((ROOT/'data/models.json').read_text());KEYS={canonical(m['matrices']):m['model'] for m in MODELS};SEARCH=None
    if phase in ('full','signed'):
        from signed import Search
        SEARCH=Search(engine)

def classify(row):
    from dispatch import (sd_tensor,ns_tensor,canonical,ranktwo_recognizer,nonselfdual_recognizer,diagonal_recognizer,near_recognizer,literature_near_recognizer,cyclotomic_failure,matrices,t,subring_certificate,Characters,key,pseudo_certificate,involution_propagation_recognizer,signed_certificate)
    start=time.monotonic()
    R=(sd_tensor if row['tag']=='S' else ns_tensor)(row['parameters'])
    try:
        if PHASE=='signed':
            c,reason=signed_certificate(R,SEARCH)
            return {**row,'certificate':c,'unresolved_reason':reason,'elapsed_seconds':round(time.monotonic()-start,4)}
        c=None;reason=None
        k=canonical(R)
        if k in KEYS:c={'kind':'model','model':KEYS[k]}
        if c is None:
            for test in (ranktwo_recognizer,nonselfdual_recognizer,diagonal_recognizer,near_recognizer,literature_near_recognizer):
                c=test(R)
                if c:break
        if c is None:c=cyclotomic_failure([N.charpoly(t).as_poly() for N in matrices(R)])
        if c is None:c=subring_certificate(R)
        if c is None:
            f,K,ds,D,pD,emb=Characters(R).fp()
            weak=len(key(D))==1 and key(D)[0].q==1
            two=len(set(map(key,ds)))==2
            if weak or two:
                proof=pseudo_certificate(R)
                if proof:
                    c=involution_propagation_recognizer(proof) if weak else None
                    if c is None:c={'kind':'weak_integral' if weak else 'two_dimensions','pseudo':proof}
        if c is None and PHASE=='full':c,reason=signed_certificate(R,SEARCH)
        return {**row,'certificate':c,'unresolved_reason':reason,'elapsed_seconds':round(time.monotonic()-start,4)}
    except Exception as e:
        return {**row,'certificate':None,'error':traceback.format_exc(),'elapsed_seconds':round(time.monotonic()-start,4)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'certificates/stage_dnumber/residual.jsonl')
    p.add_argument('--output',type=Path,default=ROOT/'certificates/stage_easy.jsonl')
    p.add_argument('--phase',choices=['easy','full','signed'],default='easy');p.add_argument('--engine',choices=['cpp','python'],default='cpp');p.add_argument('--workers',type=int,default=4)
    p.add_argument('--limit',type=int)
    args=p.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True);done=set();counts=Counter();start=time.monotonic()
    if args.output.exists():
        for line in args.output.open():
            r=json.loads(line);done.add(r['source_index']);counts[r['certificate']['kind'] if r['certificate'] else 'residual']+=1
    rows=[r for line in args.input.open() if (r:=json.loads(line))['source_index'] not in done]
    if args.limit:rows=rows[:args.limit]
    print('START',len(rows),'pending;',len(done),'already complete',flush=True)
    with args.output.open('a',buffering=1) as out,multiprocessing.Pool(args.workers,initializer=initialize,initargs=(args.phase,args.engine)) as pool:
        for i,r in enumerate(pool.imap_unordered(classify,rows,chunksize=1),1):
            out.write(json.dumps(r,separators=(',',':'))+'\n');kind=r['certificate']['kind'] if r['certificate'] else 'residual';counts[kind]+=1
            if kind=='residual' or r['elapsed_seconds']>=10:print('RECORD',r['source_index'],r['tag'],r['parameters'],kind,r['elapsed_seconds'],r.get('error',''),flush=True)
            if i%100==0:print('PROGRESS',i,len(rows),dict(counts),round(time.monotonic()-start,2),flush=True)
    print('COMPLETE',dict(counts),round(time.monotonic()-start,2),flush=True)
if __name__=='__main__':main()
