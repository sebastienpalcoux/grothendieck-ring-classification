"""Exact FP upper bounds for distinguished central fusion coefficients."""
from pathlib import Path
from dataclasses import replace
import argparse,hashlib,json,sys
from atomic_galois_balance import st,need,coordinates
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'commutative_integer'))
from features import build,check_integer
from atomic_spectrum import AtomicSpectrum,table_for
from review_cm_real_sts import fib_group


def tighten_fusion_bounds(system,C,T):
    """N_AB^C dim(C) <= dim(A) dim(B), in the exact positive FP embedding."""
    K=C.a['K'];embedding=C.a['embedding'];ds=C.a['ds']
    fp=T.characters.index(tuple(T.ds));beta={fp:K.one}
    frame=system.metadata['frame_index']
    if frame is None:
        groups=C.meta['low_character_labels'];lows=[(groups[g],v)for g,v,z in C.low]
    else:
        vs=[(1,)+(0,)*7]+[C.low[j][1]for j in C.frames[frame]]
        lows=list(zip(C.meta['frame_character_labels'][frame],vs))
    for E,v in lows:
        value=sum((K(int(n))*d for n,d in zip(v,ds)),K.zero)
        need(sum((T.K(int(n))*d for n,d in zip(v,T.ds)),T.K.zero)==T.beta[E],
             'restriction dimension differs from distinguished FP dimension')
        need(E not in beta or beta[E]==value,'multiple FP dimensions for one character')
        beta[E]=value
    need(set(beta)==set(range(len(T.characters)))and all(embedding.sign(v)>0 for v in beta.values()),
         'incomplete or nonpositive distinguished FP dimensions')
    def floor(value):
        need(embedding.sign(value)>=0,'negative FP ratio')
        lo,hi=0,1
        while embedding.sign(value-K(hi))>=0:lo,hi=hi,2*hi
        while hi-lo>1:
            mid=(lo+hi)//2
            if embedding.sign(value-K(mid))>=0:lo=mid
            else:hi=mid
        need(embedding.sign(value-K(lo))>=0 and embedding.sign(value-K(lo+1))<0,
             'incorrect exact FP floor')
        return lo
    bounds=list(system.bounds);records=[]
    for j,label in enumerate(system.column_labels):
        if label[0]!='fusion_coefficient':continue
        _,E,F,G=label;upper=floor(beta[E]*beta[F]/beta[G]);old=bounds[j]
        bounds[j]=min(old,upper)
        records.append({'column':j,'triple':[E,F,G],'old_upper':old,
                        'exact_FP_upper':upper,'new_upper':bounds[j]})
    report={'kind':'exact_distinguished_FP_fusion_upper_bounds','FP_character':fp,
            'FP_field_polynomial':list(map(str,K.mod.to_list())),
            'distinguished_dimensions':[list(map(str,coordinates(beta[E],len(K.mod.to_list())-1)))for E in range(len(beta))],
            'tightened_variables':sum(r['new_upper']<r['old_upper']for r in records),'records':records}
    meta={**system.metadata,'kind':'commutative_integer_with_exact_FP_fusion_bounds',
          'source_metadata':system.metadata,'FP_fusion_bounds':report,'bounds_sha256':st.digest(bounds)}
    return replace(system,bounds=tuple(bounds),metadata=meta)


def control():
    R=fib_group(True);C=AtomicSpectrum(R,4);T=table_for(R,C.a);S=build(C,T)
    saved=json.loads((HERE.parent/'commutative_integer/control.json').read_text())
    need(S.metadata==saved['metadata'],'actual center control base differs')
    check_integer(S,saved['integer_witness'])
    bounded=tighten_fusion_bounds(S,C,T)
    check_integer(bounded,saved['integer_witness'])
    return {'kind':'exact_FP_fusion_bound_control','model':'Fibonacci tensor Vec(C4)',
            'tensor_sha256':st.digest(R),'actual_integer_center_witness_retained':True,
            'metadata':bounded.metadata,
            'feature_source_sha256':hashlib.sha256((HERE.parent/'commutative_integer/features.py').read_bytes()).hexdigest()}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    result=control();path=HERE/'fp_fusion_bounds_results.json'
    if args.write:path.write_text(json.dumps(st.encode(result),indent=2)+'\n')
    else:need(st.encode(result)==json.loads(path.read_text()),'FP fusion bound control differs')
    print('PASS exact FP fusion upper bounds retain the actual complex-character center',flush=True)


if __name__=='__main__':main()
