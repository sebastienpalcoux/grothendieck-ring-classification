#!/usr/bin/env python3
"""Verify full tensor identities, exact bounds, and based-ring distinction.
Uses Python rather than the C++ elimination, with shared tensor utilities.
Run: python3 verify_census.py
--regenerate also rebuilds the complete search and compares exact parameter sets.
"""
import argparse
import collections
import csv
import hashlib
import gzip
import json
from pathlib import Path
import tempfile
import time
from rank4 import (require,tensor,validate,canonical,fingerprint,casimir,
                   leading_minors,characteristic_polynomial)
ROOT=Path(__file__).resolve().parent

def verify(data,regenerate=False):
    start=time.monotonic();manifest=json.loads((data/'manifest.json').read_text())
    M=manifest['maximum_multiplicity'];D=manifest['dimension_exclusive_bound']
    for name,digest in manifest['sha256'].items():
        require(hashlib.sha256((data/name).read_bytes()).hexdigest()==digest,'file digest: '+name)
    for name, digest in manifest['source_sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, 'source digest: '+name)
    raw = (data/'rings.jsonl').read_bytes()
    compressed = (data/'rings.jsonl.gz').read_bytes()
    require(gzip.decompress(compressed)==raw, 'gzip/uncompressed content differs')
    require(compressed[4:8]==b'\0'*4 and compressed[9]==255 and compressed[3]==0,
            'non-normalized gzip header')
    seen=set();parameters=[];counts=collections.Counter();types=collections.Counter()
    by_type=collections.Counter()
    with (data/'rings.jsonl').open() as f:
        for index,line in enumerate(f):
            row=json.loads(line);tag=row['tag'];p=row['parameters'];R=row['tensor']
            require(row['id']==index,'index mismatch')
            require(tensor(tag,p)==R,'parameter expansion')
            validate(R)
            key=canonical(R);require(key not in seen,'isomorphic repeated ring');seen.add(key)
            require(fingerprint(R)==row['canonical_sha256'],'canonical digest')
            m=max(v for A in R for r in A for v in r)
            require(m==row['multiplicity'] and 1<=m<=M,'multiplicity bound')
            C=casimir(R);minors=leading_minors(C,D)
            require(len(minors)==4 and min(minors)>0 and minors==row['pd_minors'],'FPdim certificate')
            require(characteristic_polynomial(C)==row['casimir_charpoly'],'Casimir characteristic polynomial')
            counts[m]+=1;types[tag]+=1;by_type[(m,tag)]+=1;parameters.append((tag,tuple(p)))
    require(len(seen)==manifest['number_of_rings'],'total')
    require(parameters==sorted(set(parameters)),'parameter ordering')
    expected=''.join(tag+' '+' '.join(map(str,p))+'\n' for tag,p in parameters)
    require(expected==(data/'parameters.txt').read_text(),'plain parameter list')
    require(dict(counts)=={int(k):v for k,v in manifest['counts_by_multiplicity'].items()},'counts')
    require(dict(types)==manifest['type_counts'],'duality counts')
    with (data/'counts.csv').open() as f:
        rows=list(csv.DictReader(f))
        require(len(rows)==M,'count table length')
        for m,row in enumerate(rows,1):
            require(int(row['multiplicity'])==m and int(row['rings'])==counts[m],'count table')
            require(int(row['self_dual'])==by_type[(m,'S')], 'self-dual count table')
            require(int(row['one_dual_pair'])==by_type[(m,'N')], 'dual-pair count table')
    if regenerate:
        from generate import generate
        with tempfile.TemporaryDirectory(prefix='rank4-regeneration-') as tmp:
            target=Path(tmp);generate(target,M,D)
            require((target/'parameters.txt').read_bytes()==(data/'parameters.txt').read_bytes(),'complete regeneration mismatch')
            require((target/'rings.jsonl').read_bytes()==(data/'rings.jsonl').read_bytes(),'regenerated certificates mismatch')
    report={'all_checks_passed':True,'type_counts':dict(types),
            'counts_by_multiplicity':dict(sorted(counts.items())),
            'duality_split_csv_checked':True,'gzip_content_and_header_checked':True,
            'source_hashes_checked':True,'rings_verified':len(seen),'all_tensor_axioms':True,'all_six_basis_permutations':True,
            'exact_dimension_bound':True,'complete_regeneration':regenerate,
            'elapsed_seconds':round(time.monotonic()-start,3)}
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=ROOT/'data')
    parser.add_argument('--regenerate',action='store_true')
    parser.add_argument('--report',type=Path,default=ROOT/'audit.json')
    args=parser.parse_args();report=verify(args.data,args.regenerate)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
