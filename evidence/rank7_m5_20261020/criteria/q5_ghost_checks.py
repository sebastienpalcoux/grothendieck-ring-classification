"""Independent necessary checks on exported integer induction data; not models."""
import itertools
import json
from pathlib import Path
import sympy as s

import q5_modular_low as m
q=m.q
HERE=Path(__file__).resolve().parent


def run(rid,source_path=None):
    directory=HERE.parent/'integral_gram'
    domains=json.loads((directory/(rid+'_domains.json')).read_text())
    source_file=Path(source_path) if source_path else directory/(rid+'_verlinde_discovery.json')
    source=json.loads(source_file.read_text())
    tensor=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(tensor,rid)
    table=m.ExactQuadraticCharacterTable(tensor,d,5);K=table.K
    star=[]
    for row in table.rows:
        dual=[K.from_sympy(s.conjugate(K.to_sympy(x))) for x in row]
        matches=[h for h,r in enumerate(table.rows) if list(r)==dual]
        q.require(len(matches)==1,'unique conjugate character')
        star.append(matches[0])
    results=[]
    seen=set()
    for record in source['results']:
        if not record.get('exact_feasible'):continue
        dom=next(d for d in domains if d['low_index']==record['index'])
        case=dom['cases'][record['case']]
        fingerprint=(tuple(map(tuple,record['actual_support'])),tuple(case['label']))
        if fingerprint in seen:continue
        seen.add(fingerprint)
        low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']]
        assigned=dict(zip(case['label'],low))
        objects=[(v,1) for v in low]
        for index,mult in record['actual_support']:
            objects.extend(((0,)+tuple(row[0]),mult) for row in dom['orbits'][index//10])
        for v,_ in objects:table.prepare(v)
        def triple(E,F,G):
            if table.fp in (E,F,G):
                other=list((E,F,G));other.remove(table.fp)
                return int(other[0]==star[other[1]])
            result=table.D/(table.codegrees[E]*table.codegrees[F]*table.codegrees[G])*sum((count*table.values[E,v]*table.values[F,v]*table.values[G,v]/table.dims[v] for v,count in objects),K.zero)
            expr=s.simplify(K.to_sympy(result))
            q.require(expr.is_Integer and expr>=0,'integer nonnegative low Verlinde')
            return int(expr)
        residuals=[]
        for E,F in itertools.combinations_with_replacement(range(7),2):
            v,w=assigned[E],assigned[F]
            product=[sum(v[i]*w[j]*tensor[i][j][k] for i in range(7) for j in range(7)) for k in range(7)]
            remainder=[product[k]-sum(triple(E,F,star[G])*assigned[G][k] for G in range(7)) for k in range(7)]
            residuals.append({'characters':[E,F],'remainder':remainder})
        traces=[]
        for E in range(7):
            eigenvalues=[(table.D/table.codegrees[E]*table.values[E,v]/table.dims[v],count) for v,count in objects]
            powers=[s.simplify(K.to_sympy(sum((count*value**power for value,count in eigenvalues),K.zero))) for power in range(1,5)]
            traces.append({'character':E,'trace_powers':[str(x) for x in powers], 'nonnegative_integer':all(x.is_Integer and x>=0 for x in powers)})
        result={'low_index':record['index'],'case':record['case'],'forgetful_residual_violations':[r for r in residuals if r['remainder'][0]!=0 or min(r['remainder'])<0], 'fusion_trace_violations':[r for r in traces if not r['nonnegative_integer']], 'all_fusion_traces':traces}
        results.append(result)
        print(json.dumps(result),flush=True)
    output=(source_file.stem+'_ghost_checks.json') if source_path else rid+'_ghost_checks.json'
    (HERE/output).write_text(json.dumps({'id':rid,'scope':'necessary_data_only','results':results},indent=2)+'\n')


if __name__=='__main__':
    import sys
    run(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else None)
