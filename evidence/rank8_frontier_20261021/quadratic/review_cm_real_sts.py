"""Exact CM-real-STS control, independent coefficients and packed oracle checks."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,sys
import sympy as s
HERE=Path(__file__).resolve().parent;GI=HERE.parent/'global_induction';sys.path.insert(0,str(GI))
from atomic_cm_real_sts import AtomicCMRealSTS
from quartic_complex_character_table import QuarticComplexTable
from sextic_character_table import rational_vector
from review_atomic_spectrum import oracle_checks
from rank_two_and_models import need
import column_generation as cg
import complete_phase_one as packed
st=cg.st


def fib_group(cyclic):
    R=[[[0]*8 for _ in range(8)]for _ in range(8)]
    for i in range(8):
        for j in range(8):
            f,g=divmod(i,4);h,k=divmod(j,4)
            for z in([0,1]if f==h==1 else[f+h]):R[i][j][4*z+((g+k)%4 if cyclic else g^k)]+=1
    return R


def direct_coefficients(C,T):
    K=T.K;q=C.a['q'];r=1 if q==5 else 3;u=K([1,0]);rad=(u*u+K(q+r))/(K(2)*u)
    basis=[K.one,rad];V=s.Matrix.hstack(*(rational_vector(x,4)for x in basis));W=(V.T*V).inv()*V.T
    def coords(v):
        co=list(W*rational_vector(v,4));need(sum((K(x)*b for x,b in zip(co,basis)),K.zero)==v,'independent projection outside FP field')
        return [Q(str(x))for x in co]
    def real(v):return(v+T.conjugate(v))/K(2)
    def char(v,E):return sum((K(n)*x for n,x in zip(v,T.characters[E])),K.zero)
    labels=C.meta['low_character_labels'];fp=C.meta['FP_character']
    rows=[(ri,lab)for ri,lab in enumerate(C.rows)if lab[0]=='CM_STS_real'];digests=[]
    for index in range(C.nvars):
        actual=C.column(index);expected={}
        if index<C.offset:
            group,v,z=C.low[index];G=labels[group];cv=[char(v,E)for E in range(8)]
            for ri,(_,E,F,k)in rows:
                value=real(cv[E]*cv[F]-(T.codegrees[F]*cv[E]if G==F else K.zero))
                co=coords(value)[k]*C.scales[ri]
                need(co.denominator==1,'independent low coefficient not integral')
                if co:expected[ri]=int(co)
        elif index<C.high_end:
            orbit,ti=divmod(index-C.offset,C.nt);phase=sum((K(s.Rational(x.numerator,x.denominator))*b for x,b in zip(C.types[ti][0],basis)),K.zero)
            for ri,(_,E,F,k)in rows:
                value=sum((char((0,)+tuple(C.a['high'][j][0]),E)*char((0,)+tuple(C.a['high'][j][0]),F)
                           for j in C.orbits[orbit]),K.zero)
                need(T.conjugate(value)==value,'independent complete high orbit not real')
                co=coords(value*phase)[k]*C.scales[ri]
                need(co.denominator==1,'independent high coefficient not integral')
                if co:expected[ri]=int(co)
        actual={ri:actual[ri]for ri,lab in rows if actual.get(ri,0)}
        need(actual==expected,'independent STS column differs');digests.append(expected)
        need(packed.fast_column(C,index)==C.column(index),'packed CM discovery column differs')
    for ri,(_,E,F,k)in rows:
        expected=coords(real((T.codegrees[F]if F==fp else K.zero)-K.one))[k]*C.scales[ri]
        need(expected.denominator==1 and int(expected)==C.rhs[ri],'independent STS fixed-unit rhs differs')
    return {'all_columns_checked':C.nvars,'CM_STS_rows_checked':len(rows),
            'independent_coefficients_sha256':st.digest(digests),'packed_all_columns_equal_original':True,
            'fixed_unit_rhs_checked':True}


def legacy_packed_control():
    from atomic_real_sts import AtomicRealSTS
    from sts_frame import STSFrameCone
    R=fib_group(False);a=st.old.setup(R);result=[]
    for cls in[AtomicRealSTS,STSFrameCone]:
        C=cls(R,4,data=a)
        for j in range(C.nvars):need(packed.fast_column(C,j)==C.column(j),'legacy packed column mismatch')
        result.append({'class':cls.__name__,'complete_columns_checked':C.nvars,'low':C.offset,
                       'high':C.high_end-C.offset,'rotations':C.nvars-C.high_end})
    return {'model':'Fibonacci tensor Vec(C2 times C2)','controls':result}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--rediscover',action='store_true');args=parser.parse_args()
    need(not args.rediscover or args.write,'control rediscovery requires write')
    path=HERE/'review_cm_real_sts_results.json';saved=json.loads(path.read_text())if path.exists()else None
    R=fib_group(True);a=st.old.setup(R);C=AtomicCMRealSTS(R,4,data=a);T=QuarticComplexTable(R,a)
    need(any(T.conjugate(v)!=v for row in T.characters for v in row),'control has no nonreal character')
    for g in range(4):
        for x,y in[(1,0),(0,1),(1,1)]:
            v=[0]*8;v[g]=x;v[g+4]=y;need(T.failure(v)is None,'known center restriction rejected')
    indicators=[0,1,0,1,0,1,0]
    if args.rediscover:
        ray,feasible,active,iterations=cg.solve_case(C,indicators,cg.initial_columns(C),1024,300,
            lambda it:print('CM control',it[-1]['iteration'],it[-1]['outcome'],flush=True))
        need(ray is None and feasible is not None,'known complex CM-STS control not exactly feasible')
    else:feasible=saved['exact_feasible']
    C.check_feasible(feasible['indices'],feasible['weights'],indicators)
    sources=[HERE/'atomic_cm_real_sts.py',HERE/'quartic_complex_character_table.py',GI/'atomic_spectrum.py',
             GI/'partial_s.py',GI/'streaming.py',GI/'complete_phase_one.py']
    result={'kind':'independent_CM_real_STS_exact_known_model_review','result':'PASS',
            'model':'Fibonacci tensor Vec(C4)','tensor_sha256':st.digest(R),'metadata':C.meta,
            'source_sha256':{str(p.relative_to(HERE.parent)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sources},
            'independent_coefficients':direct_coefficients(C,T),'oracle_controls':oracle_checks(C),
            'exact_feasible':feasible,'indicators':indicators,'legacy_packed_control':legacy_packed_control(),
            'scope':'necessary pseudo-unitary full-field S and real-projected STS; general exclusion requires signed lift'}
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(saved==result,'CM real STS control receipt differs')
    print('PASS: exact complex known-model CM-STS primal, independent coefficients, complete oracle and packed controls',flush=True)
if __name__=='__main__':main()
