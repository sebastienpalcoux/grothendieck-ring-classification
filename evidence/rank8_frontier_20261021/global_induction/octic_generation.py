"""Isolated Q(sqrt3,sqrt5,i) character-field atomic spectral adapter."""
import argparse,json,sys
import column_generation as cg
from exact import require
VARIANT='q35_octic_atomic_spectrum'
def install():
    if VARIANT in cg.VARIANTS:return
    cg.VARIANTS=(*cg.VARIANTS,VARIANT);original=cg.cone
    def cone(R,height,variant='streaming'):
        if variant!=VARIANT:return original(R,height,variant)
        key=(cg.st.digest(R),height,variant)
        if key not in cg._cones:
            import generic_data,atomic_spectrum
            sys.path.insert(0,str(cg.st.HERE.parent/'quadratic'))
            from octic_complex_character_table import OcticTable
            a=generic_data.setup(R,3,5);saved=atomic_spectrum.table_for
            atomic_spectrum.table_for=lambda RR,aa:OcticTable(RR,aa)
            try:cg._cones[key]=atomic_spectrum.AtomicSpectrum(R,height,data=a)
            finally:atomic_spectrum.table_for=saved
        return cg._cones[key]
    cg.cone=cone
install()
def main():
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--ring');g.add_argument('--verify');ap.add_argument('--height',type=int,default=4);ap.add_argument('--batch',type=int,default=2048);ap.add_argument('--lp-seconds',type=int,default=300);args=ap.parse_args()
    if args.verify:
        row=json.loads(cg.st.Path(args.verify).read_text());source=cg.st.load_ring(row['id']);require(row['tensor_sha256']==source['tensor_sha256'],'source binding mismatch');cg.verify(source['tensor'],row['certificate']);print('PASS',row['id']);return
    source=cg.st.load_ring(args.ring);out=cg.run(source,args.height,args.batch,args.lp_seconds,cg.st.HERE/'octic_results'/f'{args.ring}_h{args.height}.json',variant=VARIANT);print(source['id'],out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
