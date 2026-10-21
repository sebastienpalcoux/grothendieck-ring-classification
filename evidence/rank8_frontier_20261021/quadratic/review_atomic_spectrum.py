"""Independent exact checks of full-field labeled atomic S constraints.

The default is a read-only replay. --write refreshes this additive review
receipt only. This review does not extend pseudo-unitary arithmetic to the
general scope; that requires the separately replayed signed lift.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse, hashlib, json, sys
HERE=Path(__file__).resolve().parent
GI=HERE.parent/'global_induction'
sys.path.insert(0,str(GI))
import streaming as st
from atomic_spectrum import AtomicSpectrum,table_for
from atomic_real_sts import AtomicRealSTS
from rank_two_and_models import need


def fib_v4():
    R=[[[0]*8 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in ([0,1] if f==h==1 else [f+h]):R[i][j][4*z+(g^k)]+=1
    return R


def direct_symmetry(C,T):
    K=T.K;labels=C.meta['low_character_labels'];fp=C.meta['FP_character']
    need(T.characters[fp]==tuple(T.ds),'FP label mismatch')
    rows=[(r,l) for r,l in enumerate(C.rows) if l[0]=='atomic_S_full_field']
    values=[]
    for index,(group,v,z) in enumerate(C.low):
        G=labels[group];dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero)
        need(dim==T.beta[G],'labeled column has wrong dimension')
        chis=[sum((K(n)*x for n,x in zip(v,ch)),K.zero) for ch in T.characters]
        actual=C.column(index);out=[]
        for r,(_,E,F,k) in rows:
            expected=K.zero
            if G==F:expected+=T.beta[E]*chis[E]
            if G==E:expected-=T.beta[F]*chis[F]
            coeff=T.coordinates(expected)[k]*C.scales[r]
            need(coeff.denominator==1 and actual.get(r,0)==int(coeff),'full-field S coefficient differs')
            need(C.rhs[r]==0,'unexpected S symmetry rhs')
            out.append(int(coeff))
        # All omitted equations with the unit character hold identically.
        need(T.beta[G]*T.characters[G][0]==dim,'omitted FP S equation failed')
        values.append(out)
    for index in range(C.offset,C.nvars):
        actual=C.column(index)
        need(not any(actual.get(r,0) for r,l in rows),'high/rotation column has unexpected S term')
    return {'low_columns_checked':len(C.low),'full_field_symmetry_rows':len(rows),
            'coefficient_sha256':st.digest(values),'omitted_FP_equations_checked':True}


def oracle_checks(C):
    result=[]
    for seed in [3,11,29]:
        y=[((seed*(j+1)*(j+7))%31)-15 for j in range(C.nrows)]
        direct=[sum(y[r]*v for r,v in C.column(j).items()) for j in range(C.nvars)]
        scores=dict(C.low_scores(y));scores.update(C.high_scores(y))
        scores.update((C.high_end+j,sum(y[r]*v for r,v in col.items())) for j,col in enumerate(C.rotation_columns))
        need(len(scores)==C.nvars and all(scores[j]==v for j,v in enumerate(direct)),'factored oracle differs from direct column score')
        report=C.oracle(y,64)
        need(report['minimum']==min([0]+direct),'oracle minimum differs')
        need(report['negative_columns']==sum(v<0 for v in direct),'oracle negative count differs')
        need(all(direct[j]<0 for j in report['violating_columns']),'oracle returned nonnegative column')
        result.append({'seed':seed,'minimum':report['minimum'],'negative_columns':report['negative_columns'],
                       'complete_column_scores_sha256':st.digest(direct)})
    return result


def semantic_key(C,index):
    if index<C.offset:
        group,v,z=C.low[index]
        return ('low',C.meta['low_character_labels'][group],v)
    if index<C.high_end:
        orbit,ti=divmod(index-C.offset,C.nt)
        return ('high',tuple(tuple(C.a['high'][j][0]) for j in C.orbits[orbit]),tuple(C.types[ti]))
    return ('rotation',st.digest(C.rotation[index-C.high_end]))


def control():
    R=fib_v4();a=st.old.setup(R);C=AtomicSpectrum(R,4,data=a);T=table_for(R,a)
    positive=[]
    for g in range(4):
        for u,v in [(1,0),(0,1),(1,1)]:
            c=[0]*8;c[g]=u;c[g+4]=v
            need(T.failure(c) is None,'known central restriction rejected');positive.append(c)
    old=AtomicRealSTS(R,4,data=a)
    saved=json.loads((GI/'atomic_validation.json').read_text())['feasible']
    old.check_feasible(saved['indices'],saved['weights'],saved['indicators'])
    lookup={semantic_key(C,j):j for j in range(C.nvars)}
    need(len(lookup)==C.nvars,'nonunique semantic variable key')
    indices=[lookup[semantic_key(old,j)] for j in saved['indices']]
    C.check_feasible(indices,saved['weights'],saved['indicators'])
    return {'known_model':'Fibonacci tensor Vec(C2 times C2)','tensor_sha256':st.digest(R),
            'metadata':C.meta,'known_center_columns_retained':positive,
            'symmetry_check':direct_symmetry(C,T),'oracle_checks':oracle_checks(C),
            'exact_feasible':{'indices':indices,'weights':saved['weights'],'indicators':saved['indicators']}}


def ring_review(index):
    row=st.load_ring(f'R8_3_{index}');R=row['tensor'];a=st.old.setup(R)
    C=AtomicSpectrum(R,4,data=a);T=table_for(R,a)
    result={'id':row['id'],'tensor_sha256':row['tensor_sha256'],'metadata':C.meta,
            'symmetry_check':direct_symmetry(C,T),'oracle_checks':oracle_checks(C)}
    if index==3413:
        import atomic_spectrum_generation as driver
        path=GI/'atomic_spectrum_results'/f'{row['id']}_h4.json'
        record=json.loads(path.read_text())
        need(record['tensor_sha256']==row['tensor_sha256'] and record['status']=='excluded',
             'wrong source or incomplete general exclusion')
        pseudo=record['pseudo_certificate']
        need(pseudo['metadata']==C.meta,'certificate domain metadata differs')
        choices=list(map(list,st.old.ht.indicator_choices(R)))
        need([branch['indicators'] for branch in pseudo['cases']]==choices,'indicator coverage incomplete')
        cases=[]
        for branch in pseudo['cases']:
            y=branch['y'];need(len(y)==C.nrows and all(type(x)is int for x in y),'invalid integral separator')
            scores=[sum(y[r]*v for r,v in C.column(j).items()) for j in range(C.nvars)]
            bTy=sum(x*v for x,v in zip(C.rhs_for(branch['indicators']),y))
            need(min(scores)>=0 and bTy==branch['bTy'] and bTy<0,'direct complete-domain separator failure')
            cases.append({'indicators':branch['indicators'],'complete_columns':len(scores),
                          'minimum_column_pairing':min(scores),'bTy':bTy,'column_pairings_sha256':st.digest(scores)})
        driver.cg._cones[(st.digest(R),4,driver.VARIANT)]=C
        driver.cg.verify(R,record['certificate'])
        general=record['certificate']['general']
        need(general['kind']=='oriented_signed' and general['sphere']['pseudo']==pseudo,'wrong general lift')
        result['general_certificate_review']={'certificate_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'direct_complete_domain_cases':cases,'signed_branches':len(general['branches']),
             'spherical_character_alternatives':general['sphere']['characters'],
             'signed_obstructions':[branch.get('obstruction') for branch in general['branches']],
             'complete_general_replay':'PASS','scope':'general_complex_fusion_category'}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--ring',type=int,action='append');args=p.parse_args();args.ring=args.ring or [3413]
    dependencies=[GI/'atomic_spectrum.py',GI/'atomic_spectrum_generation.py',GI/'streaming.py',GI/'partial_s.py',
                  HERE/'sextic_character_table.py',HERE/'quartic_complex_character_table.py']
    result={'kind':'independent_full_field_atomic_S_review','result':'PASS',
            'categorical_scope':'pseudo-unitary center S symmetry and eigenvalue integrality; general exclusion requires signed lift',
            'source_sha256':{str(f.relative_to(HERE.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in dependencies},
            'positive_control':control(),'records':[ring_review(i) for i in args.ring]}
    suffix='_'+'_'.join(map(str,args.ring)) if args.ring else ''
    dest=HERE/f'review_atomic_spectrum{suffix}_results.json'
    if args.write:dest.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(dest.read_text())==result,'atomic S review receipt changed')
    print('PASS: independent full-field S coefficients, complete factored oracle, and exact known-model primal',args.ring,flush=True)
if __name__=='__main__':main()
