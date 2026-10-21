#!/usr/bin/env python3
"""R985: direct modular coefficients and every column of both separators.

Shares the already-reviewed complete domain constructor, but does not use
its factored Farkas oracle to establish the inequalities. All low and high
STS features are first checked against the exact S-matrix formulas.
"""
from pathlib import Path
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent
STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'global_induction'))
import streaming as st
from sts_frame import STSFrameCone
from partial_s import Table
from exact import evaluate

def need(ok,message):
    if not ok:raise ValueError(message)

def compute():
    source=st.load_ring('R8_3_985');R=source['tensor']
    receipt=json.loads((STAGE/'global_induction/sts_results/R8_3_985_h4.json').read_text())
    need(st.digest(R)==source['tensor_sha256']==receipt['tensor_sha256'],'source binding')
    C=STSFrameCone(R,4);need(C.meta==receipt['metadata'],'complete source domain')
    T=Table(R,C.a);K=T.K
    real=lambda x:(x+evaluate(x.to_list(),T.zeta**(-1),K))/K(2)
    def decode(co):
        return sum((K(st.old.s.Rational(x.numerator,x.denominator))*basis for x,basis in zip(co,T.basis)),K.zero)
    cache={}
    def chars(v):
        v=tuple(v)
        if v not in cache:cache[v]=[sum((K(n)*z for n,z in zip(v,ch)),K.zero) for ch in T.characters]
        return cache[v]
    lowchecks=0
    for index,(frame,labels) in enumerate(zip(C.frames,C.meta['frame_character_labels'])):
        columns=[(1,)+(0,)*7]+[C.low[j][1] for j in frame]
        values=[chars(v) for v in columns];inverse={E:j for j,E in enumerate(labels)}
        need(len(inverse)==8,'complete bijective low labeling')
        for E in range(8):
            for F in range(8):
                need(T.beta[E]*values[inverse[F]][E]==T.beta[F]*values[inverse[E]][F],'distinguished S symmetry')
        for (E,F),rows in zip(C.pairs,C.sts_rows):
            direct=sum((T.beta[E]*v[E]*T.beta[F]*v[F] for v in values),K.zero)-T.D*T.beta[E]*values[inverse[F]][E]
            encoded=decode([st.Q(C.sts_low[index].get(row,0),C.sts_scales[k]) for k,row in enumerate(rows)])
            need(encoded+K.one==real(direct/(T.beta[E]*T.beta[F])),'independent low S normalization')
            lowchecks+=1
    highchecks=0
    for oi,orbit in enumerate(C.orbits):
        values=[chars((0,)+tuple(C.a['high'][j][0])) for j in orbit]
        for pair,co in zip(C.pairs,C.sts_high[oi]):
            E,F=pair;direct=sum((v[E]*v[F] for v in values),K.zero)
            need(direct==real(direct),'high orbit product not real before trace')
            need(decode(co)==direct,'independent high S product')
            highchecks+=1
    print('R985 all direct S coefficients PASS',lowchecks,highchecks,flush=True)
    cases=receipt['pseudo_certificate']['cases'];need([r['indicators'] for r in cases]==list(map(list,st.old.ht.indicator_choices(R))),'complete indicators')
    minima=[0]*len(cases);negative=[0]*len(cases);score_hash=[hashlib.sha256() for _ in cases]
    for j in range(C.nvars):
        column=C.column(j)
        for i,case in enumerate(cases):
            value=sum(case['y'][row]*co for row,co in column.items())
            minima[i]=min(minima[i],value);negative[i]+=value<0
            score_hash[i].update((str(value)+'\n').encode())
    checked=[]
    for i,case in enumerate(cases):
        bty=sum(x*y for x,y in zip(C.rhs_for(case['indicators']),case['y']))
        need(not negative[i] and bty==case['bTy'] and bty<0,'direct full-column Farkas check')
        checked.append({'indicators':case['indicators'],'minimum':minima[i],'negative_columns':negative[i],'bTy':bty,'all_direct_scores_sha256':score_hash[i].hexdigest()})
    return {'result':'PASS','id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'complete_frames_before_S_symmetry':C.meta['frames_before_S_symmetry'],
            'complete_labeled_frames':len(C.frames),'full_columns':C.nvars,
            'direct_low_S_equations':lowchecks,'direct_high_orbit_S_equations':highchecks,
            'factored_Farkas_oracle_used':False,'domain_constructor_shared':True,
            'cases':checked}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'r985_direct.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'R985 direct review receipt')
    print('PASS R985 direct full-column separators',result['full_columns'],'columns',flush=True)

if __name__=='__main__':main()
