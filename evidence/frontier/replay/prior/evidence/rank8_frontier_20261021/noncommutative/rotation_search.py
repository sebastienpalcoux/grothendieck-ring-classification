"""Central-support refined finite rotation search; exact rays only accepted."""
from pathlib import Path
import argparse,json,sys,time
import central_support as c
import biquadratic_traces as bq
import higher_traces as h
sys.path.insert(0,str(c.OLD.parent/'performance'))
import gram_vectors_rank8 as grams

def install():
    c.w.core.restriction=c.restriction
    h.high_columns=grams.high_columns

def search(R,height):
    install(); quartic=c.w.spectral(R)['factor'].degree()==4
    a=bq.data(R) if quartic else c.w.data(R);out=[]
    for index,cols in enumerate(a['lows']):
        why=c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        rec={'low_index':index,'columns':list(map(list,cols)),'ordinary':why};out.append(rec)
        if why:continue
        rec['systems']=[];L=c.s.Matrix.hstack(*map(c.s.Matrix,cols))
        for ep in h.indicator_choices(R):
            A,rhs,meta=bq.system(R,a,cols,ep,height) if quartic else h.build_system(R,a,L,ep,height)
            ray=h.farkas(A,rhs)
            if ray:h.check_farkas(A,rhs,ray)
            meta.pop('labels',None)
            rec['systems'].append({'indicators':list(ep),'metadata':meta,'ray':ray})
            print(index,ep,meta,'exact_ray',ray is not None,flush=True)
    return {'scope':'pseudo_unitary_only','height':height,'column_counts':list(map(len,a['columns'])),
            'low_count':len(a['lows']),'branches':out,'excludes':all(x['ordinary'] or all(y['ray'] is not None for y in x['systems']) for x in out)}

def verify(R,saved):
    install();quartic=c.w.spectral(R)['factor'].degree()==4
    a=bq.data(R) if quartic else c.w.data(R)
    c.require(saved['scope']=='pseudo_unitary_only','scope')
    c.require(saved['column_counts']==list(map(len,a['columns'])) and saved['low_count']==len(a['lows'])==len(saved['branches']),'complete low branches')
    for index,(cols,rec) in enumerate(zip(a['lows'],saved['branches'])):
        c.require(rec['low_index']==index and rec['columns']==list(map(list,cols)),'low column identity')
        why=c.w.core.low_failure(cols,a['Gram'],a['ds'],a['D'],a['K'],a['embedding'],a['du'])
        c.require(why==rec['ordinary'],'ordinary criterion replay')
        if why:continue
        eps=h.indicator_choices(R);c.require([x['indicators'] for x in rec['systems']]==list(map(list,eps)),'all indicator branches')
        L=c.s.Matrix.hstack(*map(c.s.Matrix,cols))
        for ep,case in zip(eps,rec['systems']):
            A,rhs,meta=bq.system(R,a,cols,ep,saved['height']) if quartic else h.build_system(R,a,L,ep,saved['height'])
            meta.pop('labels',None);c.require(meta==case['metadata'],'system identity')
            if case['ray'] is not None:h.check_farkas(A,rhs,case['ray'])
    c.require(saved['excludes']==all(x['ordinary'] or all(y['ray'] is not None for y in x['systems']) for x in saved['branches']),'exclusion status')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--ring',type=int,required=True);ap.add_argument('--height',type=int,default=6);ap.add_argument('--verify',action='store_true');args=ap.parse_args()
    r=next(r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text()) if r['id']==f'R8_3_{args.ring}')
    path=c.HERE/f'rotation_{args.ring}_h{args.height}.json'
    if args.verify:verify(r['tensor'],json.loads(path.read_text())['result']);print('PASS');return
    start=time.monotonic();result=search(r['tensor'],args.height)
    out={'id':r['id'],'tensor_sha256':r['tensor_sha256'],'seconds':time.monotonic()-start,'result':result}
    path.write_text(json.dumps(out,indent=2,default=int)+'\n');print(r['id'],'excludes',result['excludes'],flush=True)

if __name__=='__main__':main()
