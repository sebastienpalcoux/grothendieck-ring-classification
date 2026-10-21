"""Independent full-field atomic-S review of R1055 with a complex model control.

Default: exact read-only replay. --write refreshes the receipt. The optional
--rediscover-control proposes a positive-control primal numerically; exact
verification is mandatory and discovery requires --write.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent;GI=HERE.parent/'global_induction'
sys.path.insert(0,str(GI))
import atomic_spectrum_generation as driver
from atomic_spectrum import AtomicSpectrum,table_for
from review_atomic_spectrum import oracle_checks
from rank_two_and_models import need
st=driver.cg.st


def direct_symmetry(C,T):
    K=T.K;labels=C.meta['low_character_labels'];fp=C.meta['FP_character']
    rows={(E,F,k):r for r,lab in enumerate(C.rows)if lab[0]=='atomic_S_full_field'for _,E,F,k in[lab]}
    pairs=list(itertools.combinations(labels,2));values=[]
    for index,(group,v,z)in enumerate(C.low):
        G=labels[group];dim=sum((K(n)*d for n,d in zip(v,T.ds)),K.zero)
        need(dim==T.beta[G],'labeled restriction has wrong dimension')
        chis=[sum((K(n)*x for n,x in zip(v,ch)),K.zero)for ch in T.characters]
        expected={}
        for E,F in pairs:
            if G==F:val=T.beta[E]*chis[E]
            elif G==E:val=-T.beta[F]*chis[F]
            else:continue
            for k,x in enumerate(T.coordinates(val)):
                r=rows[E,F,k];x*=C.scales[r];need(x.denominator==1,'nonintegral scaled coefficient')
                if x:expected[r]=int(x)
        actual={r:x for r,x in C.column(index).items()if r in rows.values() and x}
        need(actual==expected,'direct full-field S coefficients differ')
        need(T.beta[G]*T.characters[G][0]==dim,'omitted FP equation fails')
        values.append(expected)
    for index in range(C.offset,C.nvars):
        need(not any(r in rows.values()and x for r,x in C.column(index).items()),'unexpected high S coefficient')
    need(all(C.rhs[r]==0 for r in rows.values()),'nonzero S rhs')
    return {'low_columns_checked':len(C.low),'coordinate_rows':len(rows),
            'direct_coefficient_sha256':st.digest(values),'omitted_FP_equations_checked':True}


def complex_control(saved,rediscover):
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):R[i][j][4*z+(g+k)%4]+=1
    a=st.old.setup(R);C=AtomicSpectrum(R,4,data=a);T=table_for(R,a)
    need(T.degree==4 and any(T.conjugate(v)!=v for row in T.characters for v in row),'control lacks nonreal characters')
    positive=[]
    for g in range(4):
        for u,v in[(1,0),(0,1),(1,1)]:
            c=[0]*8;c[g]=u;c[g+4]=v;need(T.failure(c)is None,'known central restriction rejected');positive.append(c)
    indicators=next(ep for ep in st.old.ht.indicator_choices(R)if list(ep)==[0,1,0,1,0,1,0])
    if rediscover:
        ray,feasible,active,iterations=driver.cg.solve_case(C,indicators,driver.cg.initial_columns(C),1024,300,
            lambda it:print('complex control',it[-1]['iteration'],it[-1]['outcome'],flush=True))
        need(ray is None and feasible is not None,'known complex-character model failed exact feasibility')
    else:feasible=saved['positive_control']['exact_feasible']
    C.check_feasible(feasible['indices'],feasible['weights'],indicators)
    return {'model':'Fibonacci tensor Vec(C4)','tensor_sha256':st.digest(R),'metadata':C.meta,
            'all_twelve_actual_center_restrictions_retained':positive,
            'nonreal_characters_present':True,'direct_symmetry':direct_symmetry(C,T),'oracle_checks':oracle_checks(C),
            'exact_feasible':feasible,'indicators':list(indicators)}


def review():
    source=st.load_ring('R8_3_1055');R=source['tensor'];a=st.old.setup(R);C=AtomicSpectrum(R,4,data=a);T=table_for(R,a)
    path=GI/'atomic_spectrum_results/R8_3_1055_h4.json';record=json.loads(path.read_text())
    need(record['id']==source['id']and record['tensor_sha256']==source['tensor_sha256']and record['status']=='excluded',
         'wrong source or incomplete general certificate')
    pseudo=record['pseudo_certificate'];need(pseudo['metadata']==C.meta,'certificate metadata mismatch')
    need([b['indicators']for b in pseudo['cases']]==list(map(list,st.old.ht.indicator_choices(R))),'incomplete indicators')
    cases=[]
    for branch in pseudo['cases']:
        y=branch['y'];need(len(y)==C.nrows and all(type(x)is int for x in y),'invalid integral separator')
        scores=[sum(y[r]*v for r,v in C.column(j).items())for j in range(C.nvars)]
        bTy=sum(x*v for x,v in zip(C.rhs_for(branch['indicators']),y))
        need(min(scores)>=0 and bTy<0 and bTy==branch['bTy'],'complete direct separator failure')
        cases.append({'indicators':branch['indicators'],'complete_columns_checked':len(scores),'minimum_pairing':min(scores),
                      'bTy':bTy,'complete_pairings_sha256':st.digest(scores)})
    driver.cg._cones[(st.digest(R),4,driver.VARIANT)]=C;driver.cg.verify(R,record['certificate'])
    general=record['certificate']['general'];need(general['kind']=='oriented_signed'and general['sphere']['pseudo']==pseudo,'wrong signed lift')
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],'metadata':C.meta,
            'direct_symmetry':direct_symmetry(C,T),'oracle_checks':oracle_checks(C),'direct_separator_cases':cases,
            'certificate_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'general_replay':'PASS','signed_branch_count':len(general['branches']),
            'signed_obstructions':[b.get('obstruction')for b in general['branches']],
            'spherical_character_alternatives':general['sphere']['characters'],'scope':'general_complex_fusion_category'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--rediscover-control',action='store_true');args=p.parse_args()
    need(not args.rediscover_control or args.write,'control rediscovery requires write')
    dest=HERE/'review_atomic_complex_1055_results.json';saved=json.loads(dest.read_text())if dest.exists()else None
    dependencies=[GI/'atomic_spectrum.py',GI/'atomic_spectrum_generation.py',GI/'streaming.py',GI/'partial_s.py',
                  HERE/'quartic_complex_character_table.py',HERE/'review_atomic_spectrum.py']
    result={'kind':'independent_complex_character_atomic_S_exclusion_review','result':'PASS',
            'sources':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()for p in dependencies},
            'positive_control':complex_control(saved,args.rediscover_control),'record':review()}
    if args.write:dest.write_text(json.dumps(result,indent=2)+'\n')
    else:need(saved==result,'complex atomic review receipt changed')
    print('PASS:1055 complete direct cone inequalities and signed lift, with exact complex-character positive control',flush=True)
if __name__=='__main__':main()
