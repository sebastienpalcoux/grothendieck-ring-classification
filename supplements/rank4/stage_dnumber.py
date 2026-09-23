#!/usr/bin/env python3
"""Stream every pinned census parameter through exact formal-codegree factoring."""
import argparse,gzip,json,sys,time,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'software'))
from rings import sd_tensor,ns_tensor
from rapid import dnumber

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=ROOT/'data/parameters_128.txt.gz')
    p.add_argument('--out',type=Path,default=ROOT/'certificates/stage_dnumber')
    p.add_argument('--limit',type=int)
    args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    started=time.monotonic();counts=Counter();by_m={};checked=0
    with gzip.open(args.input,'rt') as source,gzip.open(args.out/'excluded.jsonl.gz','wt',compresslevel=6) as excluded,(args.out/'residual.jsonl').open('w') as residual:
        for source_index,line in enumerate(source):
            if args.limit is not None and source_index>=args.limit:break
            w=line.split();tag=w[0];p=tuple(map(int,w[1:]));R=(sd_tensor if tag=='S' else ns_tensor)(p)
            c=dnumber(R);m=max(1,*p);counts['dnumber' if c else 'residual']+=1
            by_m.setdefault(m,Counter())['dnumber' if c else 'residual']+=1
            row={'source_index':source_index,'tag':tag,'parameters':p,'certificate':c}
            (excluded if c else residual).write(json.dumps(row,separators=(',',':'))+'\n')
            checked+=1
            if checked%100000==0:print(checked,dict(counts),round(time.monotonic()-started,2),flush=True)
    summary={'checked':checked,'counts':dict(counts),'by_multiplicity':by_m,'elapsed_seconds':round(time.monotonic()-started,3),'input_sha256':hashlib.sha256(args.input.read_bytes()).hexdigest()}
    (args.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
