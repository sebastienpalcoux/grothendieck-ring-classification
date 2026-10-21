"""Pure invertible restrictions when the central forgetful kernel is Vec."""
from dataclasses import replace
from pathlib import Path
import argparse,json,sys
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'commutative_integer'))
from features import st,require,build,check_integer
from atomic_spectrum import AtomicSpectrum,table_for
from review_cm_real_sts import fib_group


def tighten_pure_bounds(S,R,T):
    require(all(R[i][j]==R[j][i]for i in range(8)for j in range(8)),
            'pure-pointed kernel adapter requires a commutative source ring')
    fp=T.characters.index(tuple(T.ds));others=[E for E,beta in enumerate(T.beta)if E!=fp and beta==T.K.one]
    pointed=[i for i,d in enumerate(T.ds)if d==T.K.one]
    for i in pointed:
        dual=next(j for j in range(8)if R[i][j][0])
        require(R[i][dual]==[1]+[0]*7,'dimension-one source simple not invertible')
    bounds=list(S.bounds);changes=[];seen={}
    if not others:
        for j,label in enumerate(S.column_labels):
            if label[0]!='high_orbit':continue
            restrictions=label[2];upper=bounds[j]
            for v in restrictions:
                support=[i for i,n in enumerate(v)if n]
                if len(support)!=1 or support[0]not in pointed:continue
                g=support[0];k=v[g]
                if k!=1:upper=0
                else:
                    require(g not in seen or seen[g]==j,'multiple columns for one pure invertible lift need a joint bound')
                    seen[g]=j;upper=min(upper,1)
            if upper!=bounds[j]:changes.append({'column':j,'label':st.encode(label),'old_upper':bounds[j],'new_upper':upper});bounds[j]=upper
    report={'kind':'pure_pointed_forgetful_kernel_bounds','tensor_sha256':st.digest(R),
            'pointed_source_indices':pointed,'FP_character':fp,'other_dimension_one_distinguished_labels':others,
            'kernel_Vec_hypothesis_verified':not others,'changes':changes,
            'unique_pure_lift_columns':[[g,j]for g,j in sorted(seen.items())]}
    metadata={**S.metadata,'kind':'integer_center_with_pure_pointed_bounds','pre_pure_metadata':S.metadata,
              'pure_pointed_bounds':report,'bounds_sha256':st.digest(bounds)}
    return replace(S,bounds=tuple(bounds),metadata=metadata)


def control():
    R=fib_group(True);C=AtomicSpectrum(R,4);T=table_for(R,C.a);S=build(C,T)
    saved=json.loads((STAGE/'commutative_integer/control.json').read_text());require(saved['metadata']==S.metadata,'actual control base differs')
    bounded=tighten_pure_bounds(S,R,T);check_integer(bounded,saved['integer_witness'])
    require(not bounded.metadata['pure_pointed_bounds']['kernel_Vec_hypothesis_verified'],'known Rep(C4) kernel incorrectly declared Vec')
    require(bounded.bounds==S.bounds,'inapplicable pure-kernel filter changed actual center')
    return {'model':'Fibonacci tensor Vec(C4)','nontrivial_kernel_filter_not_applied':True,
            'actual_integer_witness_retained':True,'metadata':bounded.metadata}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    out=control();path=HERE/'pure_pointed_bounds_results.json'
    if a.write:path.write_text(json.dumps(st.encode(out),indent=2)+'\n')
    else:require(st.encode(out)==json.loads(path.read_text()),'pure-pointed control differs')
    print('PASS conditional pure-pointed bounds retain the actual nontrivial-kernel center',flush=True)


if __name__=='__main__':main()
