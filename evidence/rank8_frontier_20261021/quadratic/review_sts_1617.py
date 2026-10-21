#!/usr/bin/env python3
"""R1617: direct modular coefficients and every column of both separators.

Shares the already-reviewed complete domain constructor, but does not use
its factored Farkas oracle to establish the inequalities. The full oracle
is separately compared with every direct score, and the complete signed
lift is replayed through the accepted general-category checker. All low and high
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
import column_generation as cg

def need(ok,message):
    if not ok:raise ValueError(message)

def compute():
    source=st.load_ring('R8_3_1617');R=source['tensor']
    receipt=json.loads((STAGE/'global_induction/complete_results/R8_3_1617_sts_frame_h4.json').read_text())
    need(st.digest(R)==source['tensor_sha256']==receipt['tensor_sha256'],'source binding')
    need(receipt['status']=='excluded' and receipt['scope']=='general_complex_fusion_category','not a complete general result')
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
    for rows in C.sts_rows:
        for k,row in enumerate(rows):
            need(C.rhs[row]==(-C.sts_scales[k] if k==0 else 0),'independent STS right-hand side')
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
    print('R1617 all direct S coefficients PASS',lowchecks,highchecks,flush=True)
    cases=receipt['pseudo_certificate']['cases'];need([r['indicators'] for r in cases]==list(map(list,st.old.ht.indicator_choices(R))),'complete indicators')
    need(all(len(c['y'])==C.nrows and all(type(x)is int for x in c['y']) for c in cases),'invalid integral separator')
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
        oracle=C.oracle(case['y'],64)
        need(oracle['minimum']==minima[i] and oracle['negative_columns']==negative[i], 'full oracle differs from direct all-column scores')
        checked.append({'indicators':case['indicators'],'minimum':minima[i],'negative_columns':negative[i],'bTy':bty,'all_direct_scores_sha256':score_hash[i].hexdigest()})
    cg._cones[(st.digest(R),4,'sts_frame')]=C
    cg.verify(R,receipt['certificate'])
    general=receipt['certificate']['general']
    need(general['kind']=='oriented_signed' and general['sphere']['pseudo']==receipt['pseudo_certificate'],'wrong signed lift')
    certificate_path=STAGE/'global_induction/complete_results/R8_3_1617_sts_frame_h4.json'
    dependencies=['streaming.py','column_generation.py','frame_cone.py','spectral_frame.py','sts_frame.py','partial_s.py']
    return {'result':'PASS','scope':'general_complex_fusion_category',
            'certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
            'sources':{name:hashlib.sha256((STAGE/'global_induction'/name).read_bytes()).hexdigest()for name in dependencies},
            'complete_general_replay':'PASS','signed_branch_count':len(general['branches']),
            'signed_obstructions':[b.get('obstruction')for b in general['branches']],
            'spherical_character_alternatives':general['sphere']['characters'],'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'complete_frames_before_S_symmetry':C.meta['frames_before_S_symmetry'],
            'complete_labeled_frames':len(C.frames),'full_columns':C.nvars,
            'direct_low_S_equations':lowchecks,'direct_high_orbit_S_equations':highchecks,
            'factored_Farkas_oracle_used_for_inequalities':False,'factored_oracle_also_compared':True,'domain_constructor_shared':True,
            'cases':checked}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'review_sts_1617_results.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'R1617 direct review receipt')
    print('PASS R1617 direct full-column separators',result['full_columns'],'columns',flush=True)

if __name__=='__main__':main()
