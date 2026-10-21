"""Exact height-six rotation with complete complex partial-S integrality."""
from pathlib import Path
import argparse,hashlib,json
import source
from certified_lp import decide,verify

HERE=Path(__file__).resolve().parent
need=source.need


def system(d,indicators):
    R,a,b,chars,cols,Q,high,meta=d
    L=source.s.Matrix.hstack(*map(source.s.Matrix,cols))
    A,rhs,old=source.full.system(R,a,L,indicators,6)
    forbidden=sorted(set(meta['integral_forbidden_indices']+[r['index']for r in meta['spectral_exclusions']]))
    for i in forbidden:
        row=[0]*len(A[0]);row[i*old['trace_types']:(i+1)*old['trace_types']]=[1]*old['trace_types'];A.append(row);rhs.append(0)
    return A,rhs,dict(old,forbidden_high_indices=forbidden,system_sha256=hashlib.sha256(json.dumps([A,rhs],separators=(',',':')).encode()).hexdigest())


def run(write):
    d=source.data();source_meta=json.loads(json.dumps(d[-1],default=int))
    need(source_meta==json.loads((HERE/'source.json').read_text()),'complete source-domain replay')
    old=json.loads((HERE.parent/'noncommutative_followup/additional_joint_rotation_h6.json').read_text())
    prior=next(r for r in old if r['id']=='R8_3_567')
    choices=list(source.full.h.indicator_choices(d[0]))
    need(list(map(list,choices))==[c['indicators']for c in prior['cases']],'complete eight indicator choices')
    path=HERE/'rotation_spectral.json';saved=None if write else json.loads(path.read_text());cases=[]
    for index,indicators in enumerate(choices):
        A,b,meta=system(d,indicators)
        if write:
            earlier=prior['cases'][index]['decision']
            decision=dict(earlier,ray=earlier['ray']+[0]*len(meta['forbidden_high_indices']))if earlier['status']=='exact_infeasible_relaxation'else decide(A,b)
        else:
            need(saved['cases'][index]['metadata']==meta,'exact augmented system');decision=saved['cases'][index]['decision']
        verify(A,b,decision)
        cases.append({'indicators':list(indicators),'metadata':meta,'decision':decision})
        print('R567',indicators,decision['status'],flush=True)
    result={'id':'R8_3_567','source_domain_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),
        'cases':cases,'excluded':all(c['decision']['status']=='exact_infeasible_relaxation'for c in cases),
        'scope':'necessary pseudo-unitary center constraints, applicable in general via the certified Galois gate and integral-center lemma'}
    if write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==saved,'exact complete spectral/rotation replay')
    print('PASS R567 complete spectral/rotation domain; excluded=',result['excluded'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();run(args.write)
