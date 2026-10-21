"""Explicit Q(sqrt3,sqrt5) complete-cone discovery and exact replay."""
import argparse,json
import column_generation as cg
from exact import require

def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--ring');g.add_argument('--verify');ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=2048);ap.add_argument('--lp-seconds',type=int,default=300);ap.add_argument('--variant',choices=('frame','sts_frame'),default='sts_frame');args=ap.parse_args()
    if args.verify:
        row=json.loads(cg.st.Path(args.verify).read_text());source=cg.st.load_ring(row['id']);require(source['tensor_sha256']==row['tensor_sha256'],'source binding mismatch');cg.verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=cg.st.load_ring(args.ring);variant='q35_'+args.variant;out=cg.run(source,args.height,args.batch,args.lp_seconds,cg.st.HERE/'generic_results'/f'{args.ring}_{args.variant}_h{args.height}.json',variant=variant);print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
