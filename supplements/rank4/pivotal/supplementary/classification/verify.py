#!/usr/bin/env python3
"""Replay every necessary-condition certificate using exact arithmetic.

The verifier reconstructs each based ring, checks all its axioms, recomputes
formal codegrees and character fields, and enumerates all claimed low
restriction matrices. Catalogue labels and recorded statuses are not evidence.
"""
import argparse,json,multiprocessing,sys,time
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
import rapid
from rings import *
from literature import *
from spherical import *

MODEL_KEYS={}

def initialize(models):
    MODEL_KEYS.clear()
    MODEL_KEYS.update({m['model']:canonical(m['matrices']) for m in models})

def verify_record(pair):
    row,record=pair;R=row['tensor'];c=record['certificate'];stage=record['stage'];kind=c['kind']
    require(all(row[k]==record[k] for k in ('id','tag','parameters')),'certificate identifies a different census ring')
    require(R==(sd_tensor if row['tag']=='S' else ns_tensor)(row['parameters']),'tensor/parameter mismatch')
    validate(R)
    if stage=='rank_two':check_rank_two(R,c);return stage
    if stage=='formal_codegree_dnumber':check_dnumber(R,c);return stage
    if stage=='published_rank_four_families':check_small_families(R,c);return stage
    if stage in ('spherical_arithmetic','central_induction'):
        require(kind=='spherical','wrong spherical certificate class')
        require((c.get('pseudo') is None)==(stage=='spherical_arithmetic'),'wrong spherical stage')
        check_sphere(R,c);return stage
    require(stage=='model' and kind=='model','unknown certificate or stage')
    require(c['model'] in MODEL_KEYS and canonical(R)==MODEL_KEYS[c['model']],'model tensor mismatch')
    require(sphere_certificate(R) is None,'model violates a necessary-condition filter')
    return stage

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT.parent/'census/data/rings.jsonl')
    p.add_argument('--results',type=Path,default=ROOT/'results')
    p.add_argument('--models',type=Path,default=ROOT/'models.json')
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--report',type=Path,help='Output path for this replay report.')
    a=p.parse_args();start=time.monotonic()
    rows=[json.loads(l) for l in a.input.open()];records=[json.loads(l) for l in (a.results/'certificates.jsonl').open()]
    require(len(rows)==len(records),'missing or extra certificates')
    require(len({x['id'] for x in rows})==len(rows),'duplicate census identifiers')
    require([x['id'] for x in rows]==[x['id'] for x in records],'certificate coverage/order differs')
    require(len({canonical(r['tensor']) for r in rows})==len(rows),'isomorphic duplicates in census')
    models=json.loads(a.models.read_text());require(len({m['model'] for m in models})==len(models),'duplicate model names')
    counts=Counter()
    with multiprocessing.Pool(max(1,a.workers),initializer=initialize,initargs=(models,)) as pool:
        for stage in pool.imap_unordered(verify_record,zip(rows,records),chunksize=20):counts[stage]+=1
    summary=json.loads((a.results/'summary.json').read_text());require(summary['census_count']==len(rows),'wrong summary census size')
    require(summary.get('schema_version')==5,'unsupported classification schema')
    expected_stages=['rank_two','formal_codegree_dnumber','spherical_arithmetic',
                     'published_rank_four_families','central_induction']
    require([item['filter'] for item in summary['stages']]==expected_stages,
            'summary filters are omitted, duplicated, or out of order')
    require(set(counts)<=set(expected_stages+['model']), 'unexpected verified stage')
    left=len(rows)
    for item in summary['stages']:
        require(item['excluded']==counts[item['filter']],'wrong reported exclusion count')
        left-=item['excluded'];require(item['remaining']==left,'wrong remaining count')
    require(left==counts['model']==len(models)==summary['model_count'],'model coverage differs')
    require({r['certificate']['model'] for r in records if r['stage']=='model'}=={m['model'] for m in models},'missing model')
    expected_survivors=[{'id':r['id'],'tag':r['tag'],'parameters':r['parameters'],
                         'model':r['certificate']['model']} for r in records if r['stage']=='model']
    require(json.loads((a.results/'survivors.json').read_text())==expected_survivors,
            'survivor ledger differs from verified model certificates')
    report={'optimized_python':bool(sys.flags.optimize),'arithmetic_backend':rapid.BACKEND,'survivor_ledger_checked':True,'checked_rings':len(rows),'verified_models':counts['model'],'verified_filters':dict(counts),'seconds':round(time.monotonic()-start,6),'all_checks_passed':True}
    (a.report or a.results/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
