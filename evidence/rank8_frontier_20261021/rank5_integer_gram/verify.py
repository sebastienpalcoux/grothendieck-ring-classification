"""Complete nonnegative integer Gram completions for the forced R439 dual.

Default invocation reconstructs the source and finite domain and checks a
saved receipt. It never supplies an associator or a central simple object.
"""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/'r439_centerless_rank5/verify.py'
sp=importlib.util.spec_from_file_location('r439_rank5_center_source',SOURCE)
source=importlib.util.module_from_spec(sp);sp.loader.exec_module(source)
need=source.need


def outer(v):return tuple(v[i]*v[j]for i in range(4)for j in range(i,4))
PAIRS=list(itertools.combinations_with_replacement(range(4),2))


def subtract(q,indices,forms):
    v=tuple(q[k]-sum(forms[i][k]for i in indices)for k in range(10))
    return v if min(v)>=0 else None


def primary(q,vectors,allowed):
    """Exhaust fixed first-row multisets, then second-row, then a 2x2 Gram."""
    forms=[outer(v)for v in vectors]
    A=[i for i in allowed if vectors[i][0]and not vectors[i][1]]
    B=[i for i in allowed if vectors[i][0]and vectors[i][1]]
    C=[i for i in allowed if not vectors[i][0]and vectors[i][1]==1]
    E=[i for i in allowed if not vectors[i][0]and vectors[i][1]==2]
    F=[i for i in allowed if vectors[i][:2]==(0,0)and vectors[i][2]and vectors[i][3]]
    P=[i for i in allowed if vectors[i][:2]==(0,0)and vectors[i][2]and not vectors[i][3]]
    Z=[i for i in allowed if vectors[i][:3]==(0,0,0)]
    need(set(A+B+C+E+F+P+Z)==set(allowed),'complete disjoint block partition')
    need(all(vectors[i][0]==1 and vectors[i][1]in(0,1)for i in A+B),'first-row values')
    need([vectors[i][2]for i in P]==[1,2]and[vectors[i][3]for i in Z]==[1,2],'pure-axis square domains')
    need(q[:4]==(4,2,4,4),'forced first row')
    answers=[];first=0;second=0
    cache={}
    def pq(a,b,c):
        key=(a,b,c)
        if key in cache:return cache[key]
        out=[]
        def visit(at,aa,bb,cc,terms):
            if at==len(F):
                if bb:return
                for pp in range(aa//4+1):
                    for qq in range(cc//4+1):
                        out.append(terms+[(P[0],aa-4*pp),(P[1],pp),(Z[0],cc-4*qq),(Z[1],qq)])
                return
            i=F[at];p,r=vectors[i][2:]
            bound=min(aa//(p*p),bb//(p*r),cc//(r*r))
            for m in range(bound+1):visit(at+1,aa-m*p*p,bb-m*p*r,cc-m*r*r,terms+[(i,m)])
        visit(0,a,b,c,[]);cache[key]=out;return out
    for aa in itertools.combinations_with_replacement(A,2):
        for bb in itertools.combinations_with_replacement(B,2):
            block=aa+bb;r=subtract(q,block,forms)
            if r is None or any(r[:4]):continue
            first+=1
            need(r[4]==4,'second diagonal after first row')
            choices=itertools.chain(itertools.combinations_with_replacement(C,4),((i,)for i in E))
            for cc in choices:
                t=subtract(r,cc,forms)
                if t is None or any(t[:7]):continue
                second+=1
                for tail in pq(*t[7:]):
                    ans=[0]*len(vectors)
                    for i in block+cc:ans[i]+=1
                    for i,m in tail:ans[i]+=m
                    answers.append(tuple(ans))
    need(len(set(answers))==len(answers),'duplicate primary completions')
    return sorted(answers),{'first_row_complete_multiset_domain':len(A)*(len(A)+1)//2*len(B)*(len(B)+1)//2,
        'first_row_survivors':first,'second_row_survivors':second,'distinct_tail_Gram_targets':len(cache)}


def independent(q,vectors,allowed):
    """Uniform recursive multiplicity enumeration, independent of fixed 4/2 split."""
    forms=[outer(v)for v in vectors]
    groups=[[i for i in allowed if next(j for j,x in enumerate(vectors[i])if x)==k]for k in range(4)]
    answers=[];counts=[0]*len(vectors)
    def level(k,residual):
        if k==4:
            need(not any(residual),'terminal residual')
            answers.append(tuple(counts));return
        row=[at for at,(i,j)in enumerate(PAIRS)if i==k]
        indices=groups[k]
        def choose(at,r):
            if at==len(indices):
                if not any(r[j]for j in row):level(k+1,r)
                return
            i=indices[at];f=forms[i]
            bound=min(r[j]//x for j,x in enumerate(f)if x)
            for m in range(bound+1):
                counts[i]=m
                choose(at+1,tuple(v-m*w for v,w in zip(r,f)))
            counts[i]=0
        choose(0,residual)
    level(0,q)
    need(len(set(answers))==len(answers),'duplicate independent completions')
    return sorted(answers)


def run():
    R=source.source();a=source.h.quadratic_data(R);fc,chars=source.spectral(R,a)
    cols=a['lows'][12]
    Q,H,bad,old_center=source.high_filter(a,fc,chars,cols)
    need(Q.tolist()==[[4,2,4,4],[2,6,7,7],[4,7,34,31],[4,7,31,34]],'source residual Gram')
    vectors=[tuple(v)for v,z in H]
    need(len(vectors)==38,'complete high-vector count')
    rational=[i for i,(v,z)in enumerate(H)if not z[1]]
    need(rational==[i for i,v in enumerate(vectors)if v[2:]==(0,0)],'all rational dimensions identified')
    spectral=[r['index']for r in bad]
    need(rational==[9,17,19,27]and spectral==[37],'exact necessary filters')
    allowed=[i for i in range(len(H))if i not in rational+spectral]
    q=tuple(int(Q[i,j])for i,j in PAIRS)
    solutions,stats=primary(q,vectors,allowed)
    other=independent(q,vectors,allowed)
    need(solutions==other,'independent complete integer enumeration differs')
    forms=[outer(v)for v in vectors]
    for m in solutions:
        need(all(x>=0 and isinstance(x,int)for x in m),'nonnegative integer multiplicities')
        need(all(sum(m[i]*forms[i][j]for i in range(len(H)))==q[j]for j in range(10)),'full Gram identity')
        need(not any(m[i]for i in rational+spectral),'forbidden central simple')
    dependencies=[]
    for relative in ['r439_centerless_rank5/verify.py','review/INTEGRAL_CENTER_SUBCATEGORY.md',
                     'review/integral_center_subcategory.py','review/integral_center_subcategory.json']:
        p=BASE/relative
        dependencies.append({'path':str(p.relative_to(HERE.parents[2])),
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'kind':'complete_integer_Gram_completions_for_centerless_R439_rank5_dual',
        'rank5_tensor_sha256':source.TENSOR_SHA,'source_archive_sha256':source.ARCHIVE_SHA,
        'rank5_source_id':'R5_3_40','low_frame_index':12,'low_columns':[list(c)for c in cols],
        'residual_Gram':Q.tolist(),'high_vectors':[list(v)for v in vectors],
        'rational_dimension_forbidden_indices':rational,'spectral_forbidden_indices':spectral,
        'allowed_indices':allowed,'enumeration':stats,'solution_count':len(solutions),
        'solutions':[list(m)for m in solutions],
        'high_central_simple_count_distribution':dict(sorted(Counter(map(sum,solutions)).items())),
        'independent_reconstruction':'two complete integer enumerations agreed on every multiplicity vector',
        'dependencies':dependencies,
        'scope':'necessary central integer multiplicities only; no fusion rules or associators constructed',
        'outcome':'exact_integer_Gram_survivors'if solutions else'exact_integer_Gram_empty'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'results.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'integer Gram receipt changed')
    print('PASS: complete rank-five integer Gram domain;',actual['solution_count'],'solutions; two independent enumerations agree.')
