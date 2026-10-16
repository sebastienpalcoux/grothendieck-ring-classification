#!/usr/bin/env python3
"""Enumerate every rank-four fusion ring in the strict FP-dimension window.
Run: python3 generate.py
Dependencies: Python >=3.9 and a C++17 compiler (default: g++).
No precomputed ring list is read. Output defaults to data/ beside this script.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import time
from rank4 import tensor,casimir,leading_minors,characteristic_polynomial,fingerprint

ROOT=Path(__file__).resolve().parent

def encode(obj):return json.dumps(obj,separators=(',',':'),sort_keys=True)

def generate(output,M=31,D=1000,compiler='g++'):
    start=time.monotonic();output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rank4-enumerate-') as tmp:
        exe=Path(tmp)/'enumerate'
        subprocess.run([compiler,'-O3','-std=c++17',str(ROOT/'enumerate.cpp'),'-o',str(exe)],check=True)
        result=subprocess.run([str(exe),str(M),str(D)],check=True,text=True,stdout=subprocess.PIPE)
    parameters=[]
    for line in result.stdout.splitlines():
        tag,*p=line.split();parameters.append((tag,tuple(map(int,p))))
    parameters.sort()
    if len(set(parameters))!=len(parameters):raise RuntimeError('repeated parameter record')
    lines=[];counts=collections.Counter();by_type=collections.Counter()
    for index,(tag,p) in enumerate(parameters):
        R=tensor(tag,p);C=casimir(R);minors=leading_minors(C,D)
        if len(minors)!=4 or min(minors)<=0:raise RuntimeError('dimension certificate failure')
        m=max((1,)+p);counts[m]+=1;by_type[(m,tag)]+=1
        record={'id':index,'tag':tag,'parameters':p,'multiplicity':m,'tensor':R,
                'canonical_sha256':fingerprint(R),'pd_minors':minors,
                'casimir_charpoly':characteristic_polynomial(C)}
        lines.append(encode(record))
    parameter_bytes=''.join(tag+' '+' '.join(map(str,p))+'\n'for tag,p in parameters).encode()
    tensor_bytes=('\n'.join(lines)+'\n').encode()
    (output/'parameters.txt').write_bytes(parameter_bytes)
    (output/'rings.jsonl').write_bytes(tensor_bytes)
    # Normalize mtime, filename (absent), and OS byte. The uncompressed hash
    # remains the portable invariant across different DEFLATE implementations.
    compressed = bytearray(gzip.compress(tensor_bytes, compresslevel=9, mtime=0))
    compressed[9] = 255  # RFC 1952: unknown OS, independent of this host.
    (output/'rings.jsonl.gz').write_bytes(compressed)
    with (output/'counts.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['multiplicity','rings','self_dual','one_dual_pair'])
        for m in range(1,M+1):writer.writerow([m,counts[m],by_type[(m,'S')],by_type[(m,'N')]])
    manifest={'rank':4,'maximum_multiplicity':M,'dimension_exclusive_bound':D,
              'number_of_rings':len(parameters),'type_counts':{tag:sum(v for (m,t),v in by_type.items()if t==tag)for tag in ['S','N']},
              'counts_by_multiplicity':dict(sorted(counts.items())),
              'compression':'gzip level 9; mtime=0; no filename; OS=255; raw JSON hash is the cross-environment content invariant',
              'fpdim_certificate':'positive leading principal minors of D*I-sum_i N_i*N_i^T',
              'characteristic_polynomial':'descending coefficients; FPdim is largest real root',
              'sha256':{name:hashlib.sha256((output/name).read_bytes()).hexdigest()
                        for name in ['parameters.txt','rings.jsonl','rings.jsonl.gz','counts.csv']},
              'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                               for name in ['enumerate.cpp','generate.py','rank4.py']}}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{len(parameters)} rings; output {output}; {time.monotonic()-start:.3f} seconds including compilation.')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'data')
    parser.add_argument('--max-multiplicity',type=int,default=31)
    parser.add_argument('--dimension-bound',type=int,default=1000)
    parser.add_argument('--compiler',default='g++')
    args=parser.parse_args();generate(args.output,args.max_multiplicity,args.dimension_bound,args.compiler)
