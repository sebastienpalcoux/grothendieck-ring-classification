"""Additive commutative rank-eight adapter for exact biquadratic induction."""
from pathlib import Path
from collections import OrderedDict
import argparse,json,sys,time,traceback
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT/'supplements/rank8/experimental_signed'),str(ROOT/'supplements/rank8/software'),str(HERE.parent/'noncommutative')]

def install():
    import accelerated
    accelerated.install()
    import biquadratic_traces as bq,biquadratic_lift as lift,induction
    import low_failure_exact
    low_failure_exact.install(bq.w.core)
    if getattr(bq,'_commutative_rank8_installed',False):return bq,lift
    from rings import Characters,codegree_poly
    from exact import require,discover_roots,check_roots
    from proofs import multiplication_matrix
    original=bq.w.spectral
    def spectral(R):
        if len(R)!=8 or any(R[i][j]!=R[j][i] for i in range(8) for j in range(8)):return original(R)
        ch=Characters(R);f,K,ds,D,pD,e=ch.fp();roots=discover_roots(codegree_poly(R),K)
        require(roots is not None,'formal codegrees do not split in FP field');check_roots(codegree_poly(R),K,roots)
        require(len(roots)==8 and D in roots,'incomplete commutative codegrees');roots.remove(D)
        return dict(n=8,N=ch.N,du=ch.du,generator=ch.k,factor=f,K=K,ds=ds,D=D,embedding=e,Casimir=ch.C,Gram=ch.C,codegrees=[D]+roots,multiplicities=[1]*8)
    old_low=bq.low_frames
    def low_frames(columns,weights,B):
        return induction.low_matrices(columns,B,gram_prune=True) if list(weights)==[1]*7 else old_low(columns,weights,B)
    old_data=bq.data;data_cache={};high_cache=OrderedDict();field_cache={}
    def data(R):
        key=tuple(x for matrix in R for row in matrix for x in row)
        if key in data_cache:return data_cache[key]
        a=old_data(R);a['_ring_key']=key
        # The global relaxation deliberately suppresses low-frame enumeration.
        # Such an incomplete setup must not replace a complete fixed-frame run.
        if a['lows']:data_cache[key]=a
        return a
    def high_columns(a,cols):
        key=(a['_ring_key'],tuple(map(tuple,cols)))
        if key in high_cache:high_cache.move_to_end(key);return high_cache[key]
        L=bq.s.Matrix.hstack(*map(bq.s.Matrix,cols));Q=a['Gram']-L*L.T;high=[]
        for v in bq.native(Q.extract(range(1,8),range(1,8))):
            fk=(a['_ring_key'],tuple(v))
            if fk not in field_cache:
                z=sum((a['K'](v[i])*a['ds'][i+1] for i in range(7)),a['K'].zero)
                cp=multiplication_matrix(a['D']/z,a['K'],a['factor']).charpoly().as_poly()
                okay=all(x.q==1 for x in cp.all_coeffs())
                if okay:
                    cp=multiplication_matrix(z,a['K'],a['factor']).charpoly().as_poly().sqf_part();co=cp.all_coeffs();degree=cp.degree();norm=abs(int(co[-1]))
                    require(norm>0 and all(x.q==1 for x in co),'nonintegral central dimension')
                    okay=not any(int(c)**degree%norm**j for j,c in enumerate(co[1:],1))
                field_cache[fk]=a['coords'](z) if okay else None
            if field_cache[fk] is not None:high.append((tuple(v),field_cache[fk]))
        result=(L,Q,high);high_cache[key]=result
        while len(high_cache)>8:high_cache.popitem(last=False)
        return result
    bq.w.spectral=spectral;bq.low_frames=low_frames;bq.data=data;bq.high_columns=high_columns;bq._commutative_rank8_installed=True
    return bq,lift

def verify(R,c):
    bq,lift=install();lift.verify(R,c)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',required=True);ap.add_argument('--height',type=int,default=6);args=ap.parse_args()
    row=next(r for r in json.loads((HERE.parent/'pipeline/census_m3.json').read_text()) if r['id']==args.ring)
    dest=HERE/'advanced'/'biquadratic'/f'{args.ring}.json';dest.parent.mkdir(parents=True,exist_ok=True);start=time.monotonic()
    out={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'mode':'biquadratic','status':'no_conclusion'}
    try:
        bq,lift=install();pseudo,report=bq.discover(row['tensor'],args.height);out['report']=report
        if pseudo:
            bq.verify(row['tensor'],pseudo);out['pseudo_certificate']=pseudo;c,lr=lift.discover(row['tensor'],pseudo);out['lift_report']=lr
            if c:lift.verify(row['tensor'],c);out.update(status='excluded',scope='general',certificate=c)
            else:out['status']='pseudo_unitary_only'
    except Exception as exc:out.update(status='error',error=repr(exc),traceback=traceback.format_exc())
    out['seconds']=round(time.monotonic()-start,3);dest.write_text(json.dumps(out,separators=(',',':'))+'\n');print(args.ring,out['status'],out['seconds'],flush=True)
if __name__=='__main__':main()
