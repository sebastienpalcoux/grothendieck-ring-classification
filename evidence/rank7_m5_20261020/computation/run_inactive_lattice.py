"""Prepare exact inactive-lattice tests for the exported R3895 systems."""
import argparse,hashlib,json,time
from pathlib import Path
from inactive_lattice import prepare,hermite_basis
HERE=Path(__file__).resolve().parent;INPUT=HERE.parent/'integral_gram'


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--frame',type=int,choices=(6,8),required=True)
    args=ap.parse_args();cache={}
    for case in (0,2,4,6):
        start=time.monotonic();source=INPUT/f'R7_5_3895_system_{args.frame}_{case}.json'
        raw=source.read_bytes();system=json.loads(raw);active=system['active_variables'];active_set=set(active)
        inactive=[col for j,col in enumerate(system['columns']) if j not in active_set]
        columns=[system['columns'][j] for j in active]
        key=hashlib.sha256(json.dumps(inactive,separators=(',',':')).encode()).hexdigest()
        print(json.dumps({'event':'lattice_start','frame':args.frame,'case':case,'inactive':len(inactive),'width':len(system['rhs'])}),flush=True)
        if key not in cache:
            cache[key]=hermite_basis(inactive)
            print(json.dumps({'event':'hnf_complete','rank':len(cache[key]),'seconds':time.monotonic()-start}),flush=True)
        record=prepare(inactive,system['rhs'],columns,basis=cache[key])
        out={'id':system['id'],'low_index':args.frame,'case':case,'source_sha256':hashlib.sha256(raw).hexdigest(),
             'active_variables':active,'active_weights':system['active_weights'],'active_budget':system['active_budget'],
             'prepared':record,'seconds':time.monotonic()-start}
        path=HERE/f'R7_5_3895_inactive_lattice_{args.frame}_{case}.json'
        path.write_text(json.dumps(out,separators=(',',':'))+'\n')
        print(json.dumps({'event':'lattice_ready','frame':args.frame,'case':case,'tests':len(record['tests']),
                         'moduli':sorted({t['modulus'] for t in record['tests']}),'seconds':time.monotonic()-start}),flush=True)


if __name__=='__main__':main()
