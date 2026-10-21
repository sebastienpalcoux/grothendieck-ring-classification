"""Exact direct-S normalization and complete oracle validation; no solver."""
import argparse,json
from fractions import Fraction as Q
import streaming as st
from exact import require,evaluate,key
from partial_s import Table
from sts_frame import STSFrameCone

def validate():
    records=[]
    for rid in ('R8_3_334','R8_3_1739'):
        source=st.load_ring(rid);R=source['tensor'];a=st.old.setup(R);du=[next(j for j in range(8) if R[i][j][0]) for i in range(8)]
        chosen={tuple(v) for v,z in a['high'][:24]};chosen|={tuple(v[du[k]-1] for k in range(1,8)) for v in list(chosen)};a=dict(a,high=[h for h in a['high'] if tuple(h[0]) in chosen]);C=STSFrameCone(R,4,a);T=Table(R,C.a);K=T.K
        real=lambda x:(x+evaluate(x.to_list(),T.zeta**(-1),K))/K(2)
        chi=lambda E,v:sum((K(n)*z for n,z in zip(v,T.characters[E])),K.zero)
        decoded=lambda col,rr:sum((K(st.old.s.Rational(col.get(row,0),C.sts_scales[k]))*b for k,(row,b) in enumerate(zip(rr,T.basis))),K.zero)
        lowchecks=0
        for j,(frame,labels) in enumerate(zip(C.frames,C.meta['frame_character_labels'])):
            vs=[(1,)+(0,)*7]+[C.low[k][1] for k in frame];inverse={E:i for i,E in enumerate(labels)};col=C.column(j)
            for (E,F),rr in zip(C.pairs,C.sts_rows):
                SEF=T.beta[E]*chi(E,vs[inverse[F]])
                lhs=sum((T.beta[E]*chi(E,v)*T.beta[F]*chi(F,v) for v in vs),K.zero)-T.D*SEF
                require(decoded(col,rr)+K.one==real(lhs/(T.beta[E]*T.beta[F])),'direct distinguished-S normalization differs')
                lowchecks+=1
        high_sample=sorted(set(range(C.offset,min(C.offset+2*C.nt,C.high_end)))|set(range(C.offset,C.high_end,max(1,(C.high_end-C.offset)//37))))
        for j in high_sample:
            orbit,ti=divmod(j-C.offset,C.nt);col=C.column(j);trace=sum((K(st.old.s.Rational(x.numerator,x.denominator))*basis for x,basis in zip(C.types[ti][0],T.basis)),K.zero)
            vs=[(0,)+tuple(C.a['high'][k][0]) for k in C.orbits[orbit]]
            for (E,F),rr in zip(C.pairs,C.sts_rows):
                coefficient=sum((chi(E,v)*chi(F,v) for v in vs),K.zero)
                require(coefficient==real(coefficient),'unpaired imaginary high coefficient')
                require(decoded(col,rr)==coefficient*trace,'direct high-S trace coefficient differs')
        for seed in range(3):
            y=[((i*31+seed*17)%47)-23 for i in range(C.nrows)];scores=[sum(y[r]*v for r,v in C.column(j).items()) for j in range(C.nvars)];report=C.oracle(y,limit=C.nvars)
            require(report['minimum']==min(0,min(scores)) and set(report['violating_columns'])=={j for j,v in enumerate(scores) if v<0},'complete STS oracle differs from direct columns')
        records.append({'id':rid,'tensor_sha256':source['tensor_sha256'],'frames':len(C.frames),'variables':C.nvars,'rows':C.nrows,'direct_distinguished_S_checks':lowchecks,'direct_high_S_checks':len(high_sample)*len(C.pairs),'complete_oracle_controls':3,'STS_feature_sha256':C.meta['STS_feature_sha256']})
        print('PASS',rid,len(C.frames),C.nvars,flush=True)
    return {'result':'PASS','records':records}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args();result=validate();p=st.HERE/'sts_validation.json'
    if args.write:p.write_text(json.dumps(result,separators=(',',':'))+'\n')
    else:require(json.loads(p.read_text())==result,'STS validation receipt differs')
if __name__=='__main__':main()
