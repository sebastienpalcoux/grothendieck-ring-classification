"""Exact integer forgetful decompositions for every surviving low pair."""
from pathlib import Path
from functools import lru_cache
import argparse,hashlib,itertools,json
import verify as base
HERE=Path(__file__).resolve().parent;need=base.need


def solve(target,columns):
    tail=[tuple(c[1:])for c in columns];goal=tuple(target[1:]);need(target[0]==0,'high tensor residual has zero unit coefficient')
    @lru_cache(None)
    def visit(at,r):
        if at==len(tail):return ()if not any(r)else None
        if any(r[j]and not any(v[j]for v in tail[at:])for j in range(7)):return None
        v=tail[at];bound=min(r[j]//x for j,x in enumerate(v)if x)
        for m in range(bound+1):
            answer=visit(at+1,tuple(x-m*y for x,y in zip(r,v)))
            if answer is not None:return(m,)+answer
        return None
    answer=visit(0,goal)
    if answer is not None:need(all(sum(m*c[j]for m,c in zip(answer,columns))==target[j]for j in range(8)),'exact integer decomposition')
    return answer


def run():
    R,a,chars,cols,Q,H,meta=base.source();K=a['K'];prior=json.loads((HERE/'results.json').read_text())
    need(prior['source']==json.loads(json.dumps(meta,default=int)),'exact source domain')
    data=base.cubic_data(a,chars,cols,H);records=[];all_pass=True
    for index in prior['all_tests_survivors']:
        m=prior['patterns'][index]['multiplicities'];active=[i for i,n in enumerate(m)if n]
        coefficients={}
        for triple,low,high in data:
            value=low+sum((K(n)*v for n,v in zip(m,high)),K.zero);cs=value.to_list()
            need(len(cs)<=1 and(not cs or(cs[0].denominator==1 and cs[0]>=0)),'complete low cubic values')
            coefficients[triple]=int(cs[0])if cs else 0
        cases=[]
        for i,j in itertools.combinations_with_replacement(range(1,5),2):
            target=[sum(cols[i][u]*cols[j][v]*R[u][v][k]for u in range(8)for v in range(8))-int(i==j and k==0)
                    -sum(coefficients[tuple(sorted((i,j,l)))]*cols[l][k]for l in range(1,5))for k in range(8)]
            if min(target)<0:answer=None
            else:answer=solve(target,[(0,)+H[z][0]for z in active])
            if answer is None:all_pass=False
            cases.append({'pair':[i,j],'target':target,'aggregate_high_fusion_coefficients':list(answer)if answer is not None else None})
        records.append({'pattern_index':index,'active_high_indices':active,'pair_tests':cases})
    return {'kind':'R455_complete_low_pair_integer_forgetful_tests','source_sha256':hashlib.sha256((HERE/'results.json').read_bytes()).hexdigest(),
        'patterns':records,'all_pairs_admit_integer_decomposition':all_pass,
        'scope':'necessary aggregate coefficients for low-low products; no full central fusion ring or associator constructed'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();actual=run();path=HERE/'pair_tensors.json'
    if args.write:path.write_text(json.dumps(actual,indent=2)+'\n')
    else:need(actual==json.loads(path.read_text()),'exact pair tensor receipt')
    print('PASS R455:',len(actual['patterns']),'patterns;',sum(len(r['pair_tests'])for r in actual['patterns']),'integer pair tests; all feasible=',actual['all_pairs_admit_integer_decomposition'])
