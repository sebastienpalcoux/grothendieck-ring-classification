"""Exact necessary-data control with integral center columns restored."""
from pathlib import Path
import argparse
import itertools
import json
import verify as gram

HERE=Path(__file__).resolve().parent
base=gram.source
need=base.need


def run():
    R=base.source();a=base.h.quadratic_data(R);K=a['K'];D=a['D']
    fc,chars=base.spectral(R,a);cols=a['lows'][12]
    Q,high,bad,center=base.high_filter(a,fc,chars,cols)
    need([r['index']for r in bad]==[37],'complete spectral filter')
    q=tuple(int(Q[i,j])for i,j in gram.PAIRS);vectors=[tuple(v)for v,z in high]
    patterns=gram.independent(q,vectors,[i for i in range(38)if i!=37])
    need(len(patterns)==402,'complete enlarged integer-Gram control domain')
    triples=list(itertools.combinations_with_replacement(range(1,5),3))
    value=lambda ch,col:base.value(ch,col,K)
    dim=lambda col:sum((K(v)*d for v,d in zip(col,a['ds'])),K.zero)
    lowvalues=[[value(ch,col)for ch in chars]for col in cols]
    highvalues=[[value(ch,(0,)+v)for ch in chars]for v,z in high]
    lowdims=[dim(col)for col in cols];highdims=[dim((0,)+v)for v,z in high]
    equations=[]
    for E,F,G in triples:
        scale=D/(fc[E]*fc[F]*fc[G])
        constant=scale*sum((v[E]*v[F]*v[G]/d for v,d in zip(lowvalues,lowdims)),K.zero)
        coefficients=[scale*v[E]*v[F]*v[G]/d for v,d in zip(highvalues,highdims)]
        equations.append((constant,coefficients))
    for index,m in enumerate(patterns):
        values=[]
        for constant,coefficients in equations:
            v=constant+sum((K(z)*x for z,x in zip(m,coefficients)if z),K.zero)
            coefficients=v.to_list()
            if len(coefficients)>1 or(coefficients and(coefficients[0].denominator!=1 or coefficients[0]<0)):break
            values.append(base.h.ec(v))
        else:
            return {'kind':'rank5_integral_columns_restored_necessary_cubic_control',
                'source_tensor_sha256':base.TENSOR_SHA,'complete_integer_control_domain_count':len(patterns),
                'selected_pattern_index':index,'multiplicities':list(m),'triples':[list(t)for t in triples],
                'cubic_values':values,'nonunit_integral_high_indices':[i for i in [9,17,19,27]if m[i]],
                'scope':'exact Gram and all twenty distinguished low cubic coefficients; not asserted to be an actual categorical center'}
    raise ValueError('no exact control passed')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=run();path=HERE/'positive_control.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'positive cubic control changed')
    print('PASS: restored integral-column control satisfies the exact Gram identity and all20 distinguished cubic nonnegative-integer conditions.')
