"""Isolated registration, discovery and exact replay of labeled atomic STS."""
import argparse,json
import column_generation as cg
from exact import require
VARIANT='atomic_real_sts'
def install():
    if VARIANT in cg.VARIANTS:return
    cg.VARIANTS=(*cg.VARIANTS,VARIANT);original=cg.cone
    def cone(R,height,variant='streaming'):
        if variant!=VARIANT:return original(R,height,variant)
        key=(cg.st.digest(R),height,variant)
        if key not in cg._cones:
            from atomic_real_sts import AtomicRealSTS
            cg._cones[key]=AtomicRealSTS(R,height)
        return cg._cones[key]
    cg.cone=cone
install()
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--ring');g.add_argument('--verify');ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=2048);ap.add_argument('--lp-seconds',type=int,default=300);args=ap.parse_args()
    if args.verify:
        row=json.loads(cg.st.Path(args.verify).read_text());source=cg.st.load_ring(row['id']);require(source['tensor_sha256']==row['tensor_sha256'],'source binding mismatch');cg.verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=cg.st.load_ring(args.ring);out=cg.run(source,args.height,args.batch,args.lp_seconds,cg.st.HERE/'atomic_results'/f'{args.ring}_h{args.height}.json',variant=VARIANT);print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
