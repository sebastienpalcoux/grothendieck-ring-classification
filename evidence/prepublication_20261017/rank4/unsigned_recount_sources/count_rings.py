#!/usr/bin/env python3
"""Count independent rank-four isomorphism classes; prepare OEIS A354472 data.

No imported census is used by the enumerator. Counts are by exact multiplicity.
There is no default timeout: a complete bound-128 search may require substantial
CPU time. --timeout optionally limits the executable; incomplete runs produce
no count artifacts. Full-tensor validation is performed by audit_census.py.
"""
from pathlib import Path
import argparse,hashlib,json,os,platform,subprocess,tempfile,time
ROOT=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bound',type=int,default=128)
    p.add_argument('--timeout',type=float,default=None)
    p.add_argument('--threads',type=int,default=2,help='OpenMP threads; use 1 for the original single-thread enumerator')
    args=p.parse_args()
    if not 1<=args.threads<=256:p.error('threads must be in [1,256]')
    src=ROOT/'software'/('enumerate_census_parallel.cpp' if args.threads>1 else 'enumerate_census.cpp')
    start=time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        exe=Path(tmp)/'census'
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0]
        subprocess.run(['g++','-O3','-std=c++17']+(['-fopenmp'] if args.threads>1 else [])+[str(src),'-o',str(exe)],check=True)
        compiled=time.monotonic()
        result=subprocess.run([str(exe),str(args.bound),'--counts'],check=True,
            text=True,stdout=subprocess.PIPE,timeout=args.timeout,env={**os.environ,'OMP_NUM_THREADS':str(args.threads)})
    finished=time.monotonic();rows=[list(map(int,line.split())) for line in result.stdout.splitlines()]
    assert [r[0] for r in rows]==list(range(1,args.bound+1))
    assert all(len(r)==4 and r[1]==r[2]+r[3] for r in rows)
    report={'bound':args.bound,'total':sum(r[1] for r in rows),
      'counts':{r[0]:r[1] for r in rows},'selfdual_counts':{r[0]:r[2] for r in rows},
      'one_dual_pair_counts':{r[0]:r[3] for r in rows},
      'enumeration_seconds':round(finished-compiled,3),'total_seconds':round(finished-start,3),
      'threads':args.threads,'compiler':compiler,'platform':platform.platform(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
      'complete':True,'scope':'Independent fusion-ring census only; categorification is addressed separately by certificate verification.'}
    out=ROOT/'oeis';out.mkdir(exist_ok=True)
    (out/f'counts_{args.bound}.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/f'b354472_through_{args.bound}.txt').write_text(''.join(f'{r[0]} {r[1]}\n' for r in rows))
    (out/f'counts_{args.bound}.csv').write_text('multiplicity,total,selfdual,one_dual_pair\n'+''.join(','.join(map(str,r))+'\n' for r in rows))
    print(json.dumps({k:v for k,v in report.items() if not k.endswith('counts')},indent=2))
if __name__=='__main__':main()
