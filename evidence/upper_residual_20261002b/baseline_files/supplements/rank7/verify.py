"""Replay every rank-seven negative certificate and positive tensor match.

This reads the packaged census bytes, never the original checkout. Usage:
    python verify.py
    python -O verify.py
"""
import argparse
import collections
import concurrent.futures
import json
from pathlib import Path
from analyze import ROOT,KNOWN,SOURCE_SHA,read_source,model_matches,verify_own

def require(condition,message):
    if not condition:raise ValueError(message)

def _verify_one(item):
    ring,certificate=item
    verify_own(ring,certificate)
    return True

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers',type=int,default=4,
                        help='processes for exact exhaustive oriented branch replays')
    args=parser.parse_args()
    require(1<=args.workers<=8,'invalid verifier worker count')
    out=ROOT/'output'
    summary=json.loads((out/'rank7_summary.json').read_text())
    rows=read_source(summary['max_multiplicity'])
    ledger=json.loads((out/'rank7_ledger.json').read_text())
    catalog=json.loads((out/'rank7_model_catalog.json').read_text())
    require((ROOT/'data/model_catalog.json').read_bytes()==(out/'rank7_model_catalog.json').read_bytes(),
            'published model catalogue alias differs')
    require(len(ledger)==len(rows),'ledger count differs from census count')
    require(len({r['id'] for r in ledger})==len(ledger),'duplicate decision identifier')
    require(summary['source_sha256']==SOURCE_SHA,'summary source changed')
    require(summary['ring_counts']=={str(m):KNOWN[m]
            for m in range(1,summary['max_multiplicity']+1)},'source counts differ')
    positive,fresh_catalog=model_matches(rows)
    require(catalog==fresh_catalog,'positive catalogue altered or construction mismatched')
    stages=collections.defaultdict(collections.Counter)
    statuses=collections.defaultdict(collections.Counter)
    costly=[]
    for source,rec in zip(rows,ledger):
        require(source['id']==rec['id'] and source['source_line']==rec['source_line'],
                'decision order/source line changed')
        require(source['tensor']==rec['tensor'] and source['multiplicity']==rec['multiplicity'],
                'decision tensor changed')
        mm=positive.get(rec['id'],[])
        require(rec['model_names']==mm,'unverified positive model name')
        status=rec['status'];m=rec['multiplicity']
        if status=='unitarily_realized':
            require(bool(mm) and rec['certificate'] is None and rec['criterion'] is None,
                    'unsupported positive record')
        elif status=='excluded':
            require(not mm and rec['criterion'] in summary['stage_order']
                    and isinstance(rec['certificate'],dict),'unsupported exclusion')
            if rec['criterion']=='oriented_dimension_order':
                costly.append((rec['tensor'],rec['certificate']))
            else:verify_own(rec['tensor'],rec['certificate'])
            stages[rec['criterion']][m]+=1
        elif status=='unresolved':
            require(not mm and rec['certificate'] is None and rec['criterion'] is None,
                    'unsupported unresolved record')
        else:raise ValueError('unknown status '+str(status))
        statuses[str(m)][status]+=1
    require({stage:{str(m):count for m,count in stages[stage].items()}
            for stage in summary['stage_order']}==summary['stage_counts'],'stage counts altered')
    require({str(m):dict(statuses[str(m)])
            for m in range(1,summary['max_multiplicity']+1)}==summary['status_counts'],
            'status counts altered')
    if costly:
        with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as executor:
            require(sum(executor.map(_verify_one,costly))==len(costly),
                    'an exhaustive signed certificate failed replay')
    report={'verified':len(rows),'excluded':sum(r['status']=='excluded' for r in ledger),
            'models':len(positive),'unresolved':sum(r['status']=='unresolved' for r in ledger),
            'census_sha256':SOURCE_SHA,'max_multiplicity':summary['max_multiplicity']}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
