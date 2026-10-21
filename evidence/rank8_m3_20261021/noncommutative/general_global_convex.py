"""Isolated coprime-biquadratic adapter for the global induction relaxation."""
from pathlib import Path
import argparse,json,sys,time,traceback
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import global_induction as engine
import general_biquadratic as field
from types import SimpleNamespace
from exact import require

def install(q,r):
    field.configure(q,r)
    def setup(R):
        import induction
        require(all(R[i][j]==R[j][i] for i in range(8) for j in range(8)),'commutative adapter required')
        original=induction.low_matrices;induction.low_matrices=lambda *args,**kwargs:[]
        try:a=field.data(R)
        finally:induction.low_matrices=original
        a['width']=4;a['B']=a['Gram'];a['mul']=field.mul;a['traces']=field.trace_types
        a['rotations']=lambda order,rs:field.trace_types(order,engine.s.divisors(order),rs)[0]
        a['high']=engine.biquadratic_high(a,SimpleNamespace(native=field.bq.native,mul=field.mul))
        a['field']={'degree':4,'radicands':[q,r],'primes':list(field.PRIMES)}
        require(all(a['columns']),'empty low restriction set')
        return a
    engine._setup=setup;engine._data_cache.clear();engine._system_cache.clear();engine.install()

def verify(R,c):
    require(c['kind']=='general_global_convex_induction_lift','wrong generalized convex certificate')
    install(*c['radicands'])
    engine.verify(R,{'kind':'global_convex_induction_lift','general':c['general']})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--q',type=int,default=3);ap.add_argument('--r',type=int,default=5);ap.add_argument('--height',type=int,default=4);args=ap.parse_args()
    row=next(r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring)
    dest=HERE/f'general_global_convex_{args.ring}.json';start=time.monotonic()
    out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':'general_global_convex','radicands':[args.q,args.r],'status':'running'}
    def save():
        out['seconds']=round(time.monotonic()-start,3);tmp=dest.with_suffix('.json.tmp');tmp.write_text(json.dumps(out,separators=(',',':'))+'\n');tmp.replace(dest)
    def progress(c):out.update(status='partial_indicator_certificate',partial_certificate=c);save()
    save()
    try:
        install(args.q,args.r);pseudo,report=engine.certificate(row['tensor'],args.height,progress);out['report']=report
        if pseudo:
            out.pop('partial_certificate',None);out.update(status='pseudo_certificate_pending_replay',pseudo_certificate=pseudo);save()
            import character_induction as ci
            general=ci.lift_general(row['tensor'],pseudo,120)
            if general:
                c={'kind':'general_global_convex_induction_lift','radicands':[args.q,args.r],'general':general}
                engine.verify(row['tensor'],{'kind':'global_convex_induction_lift','general':general})
                out.update(status='excluded',scope='general',certificate=c)
            else:engine.verify_pseudo(row['tensor'],pseudo);out['status']='pseudo_unitary_only'
        else:out['status']='no_conclusion'
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    save();print(args.ring,out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
