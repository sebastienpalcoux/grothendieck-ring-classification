"""Exact joint-rotation certificates on the unique R439/R567 full-S frame."""
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'noncommutative'))
import central_support as c
import full_rotation as full
import certified_lp as lp
import additional_central_constraints as central

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census={r['id']:r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text())}
    full.base.install();path=HERE/'additional_joint_rotation_h6.json'
    saved=None if args.write else json.loads(path.read_text());out=[]
    for index,ident in enumerate(('R8_3_439','R8_3_567')):
        source=census[ident];R=source['tensor'];frames=central.compute(source)
        indices=[r['low_index'] for r in frames['frames'] if r['complete_symmetric_S_assignments']]
        c.require(indices==[2],'unique complete full-S frame')
        a=c.w.data(R);cols=a['lows'][2];L=c.s.Matrix.hstack(*map(c.s.Matrix,cols));cases=[]
        indicators=full.base.h.indicator_choices(R)
        if not args.write:
            record=saved[index]
            c.require(record['id']==ident and record['tensor_sha256']==source['tensor_sha256'],'source binding')
            c.require([x['indicators'] for x in record['cases']]==list(map(list,indicators)),'complete indicator domain')
        for at,ep in enumerate(indicators):
            A,b,meta=full.system(R,a,L,ep,6)
            if args.write:decision=lp.decide(A,b)
            else:
                decision=record['cases'][at]['decision']
                c.require(record['cases'][at]['metadata']==meta,'joint rotation system metadata')
            lp.verify(A,b,decision)
            cases.append({'indicators':list(ep),'metadata':meta,'decision':decision})
            print(ident,ep,decision['status'],flush=True)
        out.append({'id':ident,'tensor_sha256':source['tensor_sha256'],'height':6,'low_index':2,
                    'scope':'pseudo_unitary_necessary_condition; general existence after additional_scope_gates.py',
                    'cases':cases})
        if args.write:path.write_text(json.dumps(out,indent=2)+'\n')
    if not args.write:c.require(out==saved,'complete additional joint rotation replay')
    print('PASS: all16 joint indicator branches recorded; only exact rays or exact primal witnesses are conclusions')

if __name__=='__main__':main()
