"""Exact low-Verlinde/restriction-product/congruence central sieve.

The underlying system is tensor-parametric and all enumeration is replayed.
Numerical optimization is used only in discovery of exact integer dual rays.
"""
import json,time,itertools
from pathlib import Path
import modular_moments as M
from exact import require
from rings import dual
from spectral_induction import reciprocity_data,low_failure,indicator_choices,Ineligible
from higher_traces import farkas,check_farkas
ROOT=Path(__file__).resolve().parents[1]


def data_for(R):
    if dual(R)!=list(range(len(R))):raise Ineligible('self-dual ring required for real low Verlinde rows')
    data,tab=reciprocity_data(R)
    if tab.K.mod.degree()>(1 if data['q']==1 else 2):raise Ineligible('whole character field outside quadratic trace field')
    return data,tab


def system(R,data,tab,cols,ep,height,lab):
    return M.system(R,data,tab,cols,ep,height,lab,cubic=True,restriction_products=True,rational_rotations=True)


def certificate(R,height=6,progress=None):
    data,tab=data_for(R);out={'kind':'low_verlinde_restriction','version':1,'scope':'pseudo_unitary','height':height,'q':data['q'],'table':tab.metadata(),'column_counts':list(map(len,data['columns'])),'branches':[]}
    for ix,cols in enumerate(data['lows']):
        br={'columns':list(map(list,cols))};out['branches'].append(br)
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:br['ordinary']=why;continue
        labs=tab.assignments(cols);br['labellings']=list(map(list,labs));br['cases']=[]
        for lab in labs:
            for ep in indicator_choices(R):
                A,b,meta=system(R,data,tab,cols,ep,height,lab);ray=farkas(A,b);cong=None
                if ray is not None:check_farkas(A,b,ray)
                else:
                    cong=M.congruence_witness(A,b,meta['integrality'])
                    if cong is not None:M.check_congruence(A,b,meta['integrality'],cong)
                if progress:progress(ix,lab,ep,ray is not None or cong is not None)
                if ray is None and cong is None:return None
                br['cases'].append({'labelling':list(lab),'indicators':list(ep),'rows':len(A),'variables':len(A[0]),'ray':ray,'congruence':cong})
    return out


def verify(R,c):
    require(c['kind']=='low_verlinde_restriction' and c['version']==1 and c['scope']=='pseudo_unitary','wrong low Verlinde certificate')
    require(type(c['height']) is int and 3<=c['height']<=12,'invalid trace height')
    data,tab=data_for(R)
    require(c['q']==data['q'] and c['table']==tab.metadata() and c['column_counts']==list(map(len,data['columns'])),'incorrect finite field or column domain')
    require(len(c['branches'])==len(data['lows']),'omitted low frame')
    nrays=ncong=0
    for cols,br in zip(data['lows'],c['branches']):
        require(br['columns']==list(map(list,cols)),'wrong low frame')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(br['ordinary']==why,'incorrect ordinary obstruction');continue
        labs=tab.assignments(cols);require(br['labellings']==list(map(list,labs)),'omitted character labelling')
        expected=[(list(lab),list(ep)) for lab in labs for ep in indicator_choices(R)]
        require([(r['labelling'],r['indicators']) for r in br['cases']]==expected,'omitted indicator/character branch')
        for rec in br['cases']:
            A,b,meta=system(R,data,tab,cols,rec['indicators'],c['height'],rec['labelling'])
            require(rec['rows']==len(A) and rec['variables']==len(A[0]),'wrong system shape')
            require((rec['ray'] is None)!=(rec['congruence'] is None),'exactly one exact obstruction required')
            if rec['ray'] is not None:check_farkas(A,b,rec['ray']);nrays+=1
            else:M.check_congruence(A,b,meta['integrality'],rec['congruence']);ncong+=1
    return {'passed':True,'low_frames':len(data['lows']),'rays':nrays,'congruences':ncong,'optimizer_used':False}


def verify_general(R,c):
    import galois_pseudo_reduction as G
    require(c['kind']=='general_low_verlinde_restriction' and c['version']==1 and c['scope']=='general','wrong general low Verlinde certificate')
    red=G.verify(R,c['reduction']);rec=verify(R,c['pseudo']);return dict(rec,reduction=red)


if __name__=='__main__':
    import argparse,signal
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('id');ap.add_argument('--height',type=int,default=6);ap.add_argument('--seconds',type=int,default=840);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    R=next(x['N'] for x in json.load(open(ROOT/'data/census.json')) if x['id']==a.id)
    if a.verify:
        record=json.loads(a.output.read_text());c=record.get('certificate',record)
        print(json.dumps((verify_general if c['kind']=='general_low_verlinde_restriction' else verify)(R,c),indent=2));raise SystemExit(0)
    def stop(*_):raise TimeoutError('explicit discovery budget')
    def progress(*v):print(json.dumps({'progress':v}),flush=True)
    signal.signal(signal.SIGALRM,stop);signal.alarm(a.seconds);st=time.monotonic()
    try:
        c=certificate(R,a.height,progress);rec={'id':a.id,'outcome':'pseudo_unitary_excluded' if c else 'no_exact_obstruction','certificate':c}
    except Ineligible as e:rec={'id':a.id,'outcome':'ineligible','reason':str(e)}
    except TimeoutError as e:rec={'id':a.id,'outcome':'budget_incomplete','reason':str(e)}
    finally:signal.alarm(0)
    rec['seconds']=time.monotonic()-st;a.output.write_text(json.dumps(rec,separators=(',',':'))+'\n');print({k:v for k,v in rec.items() if k!='certificate'},flush=True)
