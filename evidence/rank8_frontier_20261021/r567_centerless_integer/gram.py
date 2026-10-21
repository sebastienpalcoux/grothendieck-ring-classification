"""Complete integer Gram domain for the original noncommutative R567 ring."""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import itertools
import json
import source

HERE=Path(__file__).resolve().parent
need=source.need
PAIRS=list(itertools.combinations_with_replacement(range(4),2))


def outer(v):return tuple(v[i]*v[j]for i,j in PAIRS)


def primary(q,vectors,allowed):
    forms=[outer(v)for v in vectors]
    U1=[i for i in allowed if vectors[i][0]==1]
    U2=[i for i in allowed if vectors[i][0]==2]
    W1=[i for i in allowed if vectors[i][1]==1]
    W2=[i for i in allowed if vectors[i][1]==2]
    F=[i for i in allowed if vectors[i][:2]==(0,0)and all(vectors[i][2:])]
    P=[i for i in allowed if vectors[i][:2]==(0,0)and vectors[i][2]and not vectors[i][3]]
    Z=[i for i in allowed if vectors[i][:3]==(0,0,0)]
    need(set(U1+U2+W1+W2+F+P+Z)==set(allowed),'complete disjoint first-coordinate partition')
    need(all(not(v[0]and v[1])for v in vectors),'orthogonal u and w supports')
    need([vectors[i][2]for i in P]==[1,2,4]and[vectors[i][3]for i in Z]==[1,2,4],'pure-axis domains')
    need(q[:4]==(4,0,4,4)and q[4:7]==(4,6,6),'small-row targets')
    def sub(q,ids):
        r=tuple(q[j]-sum(forms[i][j]for i in ids)for j in range(10))
        return r if min(r)>=0 else None
    cache={}
    def tail(a,b,c):
        key=a,b,c
        if key in cache:return cache[key]
        result=[]
        def axis(n):
            return [(n-16*y-4*x,x,y)for y in range(n//16+1)for x in range((n-16*y)//4+1)]
        def visit(at,aa,bb,cc,terms):
            if at==len(F):
                if bb:return
                for ps in axis(aa):
                    for qs in axis(cc):result.append(terms+list(zip(P,ps))+list(zip(Z,qs)))
                return
            i=F[at];p,r=vectors[i][2:]
            bound=min(aa//(p*p),bb//(p*r),cc//(r*r))
            for m in range(bound+1):visit(at+1,aa-m*p*p,bb-m*p*r,cc-m*r*r,terms+[(i,m)])
        visit(0,a,b,c,[]);cache[key]=result;return result
    answers=[];ustage=0;wstage=0
    us=list(itertools.chain(itertools.combinations_with_replacement(U1,4),((i,)for i in U2)))
    ws=list(itertools.chain(itertools.combinations_with_replacement(W1,4),((i,)for i in W2)))
    for u in us:
        r=sub(q,u)
        if r is None or any(r[:4]):continue
        ustage+=1
        for w in ws:
            t=sub(r,w)
            if t is None or any(t[:7]):continue
            wstage+=1
            for terms in tail(*t[7:]):
                ans=[0]*len(vectors)
                for i in u+w:ans[i]+=1
                for i,m in terms:ans[i]+=m
                answers.append(tuple(ans))
    need(len(set(answers))==len(answers),'primary enumeration contains duplicates')
    return sorted(answers),{'u_multiset_domain':len(us),'u_row_survivors':ustage,
        'w_multiset_domain_per_u':len(ws),'u_w_row_survivors':wstage,'distinct_tail_Gram_targets':len(cache)}


def independent(q,vectors,allowed):
    forms=[outer(v)for v in vectors]
    groups=[[i for i in allowed if next(j for j,x in enumerate(vectors[i])if x)==k]for k in range(4)]
    answers=[];counts=[0]*len(vectors)
    def level(k,residual):
        if k==4:
            need(not any(residual),'terminal residual');answers.append(tuple(counts));return
        row=[at for at,(i,j)in enumerate(PAIRS)if i==k];indices=groups[k]
        def choose(at,r):
            if at==len(indices):
                if not any(r[j]for j in row):level(k+1,r)
                return
            i=indices[at];f=forms[i];bound=min(r[j]//x for j,x in enumerate(f)if x)
            for m in range(bound+1):
                counts[i]=m;choose(at+1,tuple(v-m*w for v,w in zip(r,f)))
            counts[i]=0
        choose(0,residual)
    level(0,q)
    need(len(set(answers))==len(answers),'independent enumeration contains duplicates')
    return sorted(answers)


def run():
    R,a,b,chars,cols,Q,H,meta=source.data()
    need(json.loads(json.dumps(meta,default=int))==json.loads((HERE/'source.json').read_text()),'source/domain replay')
    full=[tuple(v)for v,z in H]
    reduced=[(v[0],v[4],v[2],v[3])for v in full]
    lift=[0,0,2,3,1,1,1]
    need(all(v==tuple(w[k]for k in lift)for v,w in zip(full,reduced)),'exact high-vector rank-four reduction')
    indices=[0,4,2,3];small=[[int(Q[i,j])for j in indices]for i in indices]
    need(small==[[4,0,4,4],[0,4,6,6],[4,6,42,31],[4,6,31,42]],'reduced Gram')
    need(all(Q[i,j]==small[lift[i]][lift[j]]for i in range(7)for j in range(7)),'full Gram reduction')
    q=tuple(small[i][j]for i,j in PAIRS);allowed=meta['allowed_indices'];dual=meta['dual_high_indices']
    need(all(dual[i]in allowed for i in allowed),'filtered domain dual-closed')
    all_solutions,stats=primary(q,reduced,allowed)
    independent_solutions=independent(q,reduced,allowed)
    need(all_solutions==independent_solutions,'two complete integer enumerations differ')
    solutions=[m for m in all_solutions if all(m[i]==m[dual[i]]for i in range(len(H)))]
    for m in all_solutions:
        need(all(sum(m[k]*full[k][i]*full[k][j]for k in range(len(H)))==Q[i,j]
            for i in range(7)for j in range(7)),'full 49-entry Gram verification')
        need(all(not m[i]for i in range(len(H))if i not in allowed),'forbidden vector')
    dependencies=[]
    for p in [HERE/'source.py',HERE/'source.json',HERE.parent/'review/INTEGRAL_CENTER_SUBCATEGORY.md',
              HERE.parent/'review/integral_center_subcategory.py',HERE.parent/'review/integral_center_subcategory.json']:
        dependencies.append({'path':str(p.relative_to(HERE.parents[2])),
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'kind':'complete_integer_Gram_and_duality_for_centerless_R567',
        'id':meta['id'],'tensor_sha256':meta['tensor_sha256'],'low_index':2,
        'high_vectors':[list(v)for v in full],'reduced_coordinates':['u','w','p','q'],
        'full_coordinate_lift':lift,'reduced_Gram':small,'allowed_indices':allowed,
        'dual_high_indices':dual,'enumeration':stats,'integer_Gram_count':len(all_solutions),
        'duality_compatible_count':len(solutions),'solutions':[list(m)for m in solutions],
        'all_integer_Gram_solutions_sha256':hashlib.sha256(json.dumps(all_solutions,separators=(',',':')).encode()).hexdigest(),
        'central_high_simple_count_distribution':dict(sorted(Counter(map(sum,solutions)).items())),
        'independent_check':'two complete integer enumerations agree before the exact duality filter',
        'dependencies':dependencies,'outcome':'exact_integer_Gram_survivors'if solutions else'exact_integer_Gram_empty',
        'scope':'necessary central integer multiplicities only; not fusion rules or associators'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');args=p.parse_args()
    actual=json.loads(json.dumps(run(),default=int));path=HERE/'gram.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'complete R567 integer-Gram receipt differs')
    print('PASS R567:',actual['integer_Gram_count'],'integer Grams;',actual['duality_compatible_count'],'dual-compatible; two independent enumerations agree.')
