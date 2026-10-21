#!/usr/bin/env python3
"""R1660: direct modular coefficients and every column of all separators.

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
import column_generation as cg
from sts_frame import STSFrameCone
from frame_cone import FrameCone
from partial_s import Table
from exact import evaluate

def need(ok,message):
    if not ok:raise ValueError(message)

def compute():
    source=st.load_ring('R8_3_1660');R=source['tensor']
    receipt=json.loads((STAGE/'global_induction/complete_results/R8_3_1660_sts_frame_h4.json').read_text())
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
    print('R1660 all direct S coefficients PASS',lowchecks,highchecks,flush=True)
    # Reconstruct the high STS coefficients by integer arithmetic in the
    # independently checked basis (1,sqrt(2),sqrt(3),sqrt(6)). This still
    # builds every actual column; it does not contract or call the oracle.
    need(C.width==4 and C.sts_scales==[4]*4,'reviewed radical basis and scales')
    import math
    high_integer=[]
    for features in C.sts_high:
        converted=[]
        for co in features:
            vv=[x*4 for x in co]
            need(all(x.denominator==1 for x in vv),'integral scaled STS features')
            converted.append(tuple(int(x) for x in vv))
        high_integer.append(converted)
    trace_integer=[]
    for trace in C.sts_trace1:
        denominator=math.lcm(*(x.denominator for x in trace))
        trace_integer.append((denominator,tuple(int(x*denominator) for x in trace)))
    products=[(i,j,i^j,(2 if i&j&1 else 1)*(3 if i&j&2 else 1))
              for i in range(4) for j in range(4)]
    def explicit_column(index):
        column=dict(FrameCone.column(C,index))
        if index<C.offset:
            column.update(C.sts_low[index]);return column
        if index>=C.high_end:return column
        orbit,ti=divmod(index-C.offset,C.nt);denominator,trace=trace_integer[ti]
        for rows,co in zip(C.sts_rows,high_integer[orbit]):
            values=[0]*4
            for i,j,k,factor in products:values[k]+=co[i]*trace[j]*factor
            for row,value in zip(rows,values):
                need(value%denominator==0,'integral reconstructed STS column')
                if value:column[row]=value//denominator
        return column
    for index in [0,C.offset-1,C.offset,C.offset+1,C.high_end-1,C.nvars-1]:
        need(explicit_column(index)==C.column(index),'direct integer-column positive control')
    cases=receipt['pseudo_certificate']['cases'];need([r['indicators'] for r in cases]==list(map(list,st.old.ht.indicator_choices(R))),'complete indicators')
    minima=[0]*len(cases);negative=[0]*len(cases);score_hash=[hashlib.sha256() for _ in cases]
    for j in range(C.nvars):
        column=explicit_column(j)
        for i,case in enumerate(cases):
            value=sum(case['y'][row]*co for row,co in column.items())
            minima[i]=min(minima[i],value);negative[i]+=value<0
            score_hash[i].update((str(value)+'\n').encode())
    checked=[]
    for i,case in enumerate(cases):
        bty=sum(x*y for x,y in zip(C.rhs_for(case['indicators']),case['y']))
        need(not negative[i] and bty==case['bTy'] and bty<0,'direct full-column Farkas check')
        checked.append({'indicators':case['indicators'],'minimum':minima[i],'negative_columns':negative[i],'bTy':bty,'all_direct_scores_sha256':score_hash[i].hexdigest()})
    cg._cones[(st.digest(R),4,'sts_frame')]=C
    cg.verify(R,receipt['certificate'])
    general=receipt['certificate']['general']
    need(general['kind']=='oriented_signed' and len(general['branches'])==8,'complete general signed lift')
    need(all(b['obstruction']['kind']=='gauge_original' for b in general['branches']),'signed scope alternatives')
    print('R1660 complete general signed replay PASS',flush=True)
    return {'result':'PASS','scope':'general_complex_fusion_category',
            'signed_branches':len(general['branches']),'all_signed_branches_gauge_original':True,
            'spherical_characters':general['sphere']['characters'],'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'complete_frames_before_S_symmetry':C.meta['frames_before_S_symmetry'],
            'complete_labeled_frames':len(C.frames),'full_columns':C.nvars,
            'direct_low_S_equations':lowchecks,'direct_high_orbit_S_equations':highchecks,
            'factored_Farkas_oracle_used':False,'domain_constructor_shared':True,'general_scope_replay_performed':True,
            'certificate_sha256':hashlib.sha256((STAGE/'global_induction/complete_results/R8_3_1660_sts_frame_h4.json').read_bytes()).hexdigest(),
            'cases':checked}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute();path=HERE/'r1660_direct.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'R1660 direct review receipt')
    print('PASS R1660 direct full-column separators',result['full_columns'],'columns',flush=True)

if __name__=='__main__':main()
