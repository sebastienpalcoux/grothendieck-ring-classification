#!/usr/bin/env python3
"""Construct the shared universal signed-ring catalog from a complete enumeration."""
from pathlib import Path
import argparse,gzip,json,sys
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'software'))
from global_signed import build_catalog,build_from_enumerator,SOURCE

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path)
    p.add_argument('--bound',type=int,default=128);p.add_argument('--workers',type=int,default=4);p.add_argument('--threads',type=int,default=4)
    p.add_argument('--prefix',type=Path,default=ROOT/'data/signed_universal_128');p.add_argument('--source',type=Path,default=SOURCE)
    args=p.parse_args();opener=gzip.open if args.input and args.input.suffix=='.gz' else open
    if args.input:
        with opener(args.input,'rt') as lines:
            kept,report=build_catalog(lines,args.bound,args.workers,Path(str(args.prefix)+'.jsonl.gz'),Path(str(args.prefix)+'_manifest.json'),args.source)
    else:
        if args.bound!=128:raise ValueError('automatic released-catalog generation requires bound128')
        kept,report=build_from_enumerator(args.bound,args.workers,args.threads)
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
