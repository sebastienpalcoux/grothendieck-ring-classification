"""Exact discovery/replay for real distinguished-center STS frame cones."""
import argparse,json
import column_generation as cg
from exact import require
verify=cg.verify

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--ring');g.add_argument('--verify');ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=1024);ap.add_argument('--lp-seconds',type=int,default=300);args=ap.parse_args()
    if args.verify:
        row=json.loads(cg.st.Path(args.verify).read_text());source=cg.st.load_ring(row['id']);require(source['tensor_sha256']==row['tensor_sha256'],'source binding mismatch');verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=cg.st.load_ring(args.ring);out=cg.run(source,args.height,args.batch,args.lp_seconds,cg.st.HERE/'sts_results'/f'{args.ring}_h{args.height}.json',variant='sts_frame');print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
