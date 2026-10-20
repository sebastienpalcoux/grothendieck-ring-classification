"""Independent exact checks of exported necessary low-Verlinde data.

No LP, MILP, cached coefficient columns, or floating-point arithmetic is used.
Passing is feasibility of these necessary equations, not a fusion-category model.
"""
import argparse,copy,hashlib,itertools,json,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
INPUT=HERE.parent/'integral_gram'
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
q=modular.q


def verify(N,dom,record,table,B):
    K=table.K;n=len(N);du=[next(j for j in range(n) if N[i][j][0]) for i in range(n)]
    low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']]
    rows=[(v,1) for v in low]
    if record.get('zero_phase_required'):
        q.require(any(q.phase_vertices()[column%10]==(0,0,0,0) for column,count in record['actual_support']),'missing required zero phase')
    for column,count in record['actual_support']:
        q.require(type(count) is int and count>0,'nonpositive integral multiplicity')
        orbit,phase=divmod(column,10)
        q.require(0<=phase<10 and 0<=orbit<len(dom['orbits']),'column index')
        rows.extend(((0,)+tuple(v),count) for v,_,z in dom['orbits'][orbit])
    gram=[[sum(c*v[i]*v[j] for v,c in rows) for j in range(n)] for i in range(n)]
    q.require(gram==B,'full restriction Gram identity')
    dimensions=[sum((K(v[i])*table.ds[i] for i in range(n)),K.zero) for v,c in rows]
    values=[[sum((K(v[i])*character[i] for i in range(n)),K.zero) for character in table.rows] for v,c in rows]
    dual_chars=[next(j for j,row in enumerate(table.rows) if tuple(row)==tuple(character[du[i]] for i in range(n))) for character in table.rows]
    q.require(sum((K(c)*z*z for (_,c),z in zip(rows,dimensions)),K.zero)==table.D**2,'center dimension squared')
    for E,F in itertools.product(range(n),repeat=2):
        total=sum((K(c)*val[E]*val[dual_chars[F]] for (_,c),val in zip(rows,values)),K.zero)
        q.require(total==table.codegrees[E]*table.codegrees[F]*K(int(E==F)),'normalized S low-row orthogonality')
    triples=list(itertools.combinations_with_replacement(range(n),3));coeffs={}
    for E,F,G in triples:
        value=table.D/(table.codegrees[E]*table.codegrees[F]*table.codegrees[G])
        value*=sum((K(c)*val[E]*val[F]*val[G]/z for (_,c),val,z in zip(rows,values,dimensions)),K.zero)
        rational=K.to_sympy(value)
        q.require(rational.is_Integer and rational>=0,'low Verlinde value is not a nonnegative integer')
        coeffs[E,F,G]=int(rational)
        if table.fp in (E,F,G):
            pair=list((E,F,G));pair.remove(table.fp)
            q.require(int(rational)==int(pair[0]==dual_chars[pair[1]]),'unit low fusion coefficient')
    active=list(itertools.combinations_with_replacement([i for i in range(n) if i!=table.fp],3))
    q.require([coeffs[t] for t in active]==record['verlinde_coefficients'],'recorded low fusion coefficients')
    return {'low_index':dom['low_index'],'case':record['case'],'center_rank':sum(c for v,c in rows),
            'active_branch':record.get('active_branch'),
            'restriction_gram_entries':n*n,'normalized_S_orthogonality_entries':n*n,
            'symmetric_triples':len(triples),'nontrivial_symmetric_triples':len(active),
            'coefficient_range':[min(coeffs.values()),max(coeffs.values())]}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--ring',default='R7_5_5039',choices=('R7_5_3895','R7_5_5039'));args=ap.parse_args()
    start=time.monotonic();rid=args.ring
    tensor_file=HERE/'source_frontier.json'
    N=next(r['tensor'] for r in json.loads(tensor_file.read_text()) if r['id']==rid)
    dimensions,D,B,zs,transport,signs=q.source_data(N,rid)
    table=modular.ExactQuadraticCharacterTable(N,dimensions,5);K=table.K;n=len(N)
    for row in table.rows:
        q.require(row[0]==K.one,'unital character')
        for i,j in itertools.product(range(n),repeat=2):
            q.require(row[i]*row[j]==sum((K(N[i][j][k])*row[k] for k in range(n)),K.zero),'character product')
    domain_file=INPUT/(rid+'_domains.json');result_file=HERE/(rid+'_low_verlinde_snapshot.json')
    domains=json.loads(domain_file.read_text());records=json.loads(result_file.read_text())['results']
    summaries=[];bad_controls=0
    for record in records:
        if not record.get('exact_feasible'):continue
        dom=next(d for d in domains if d['low_index']==record['index'])
        summaries.append(verify(N,dom,record,table,B))
        altered=copy.deepcopy(record);altered['actual_support'][0][1]+=1
        try:verify(N,dom,altered,table,B)
        except (ValueError,RuntimeError):bad_controls+=1
        else:raise ValueError('corrupted witness accepted')
    q.require(summaries,'no complete exact witness found')
    files=[Path(__file__),tensor_file,domain_file,result_file]
    output={'status':'PASS','id':rid,'scope':'Feasible necessary low-center data only; no existence conclusion.',
            'optimized_python':not __debug__,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
            'witnesses':summaries,'corrupted_multiplicity_controls_rejected':bad_controls,
            'numerical_optimizers_used':False,'cached_Verlinde_coefficients_used':False,'seconds':time.monotonic()-start}
    prefix='' if rid=='R7_5_5039' else rid+'_'
    target=HERE/(prefix+('low_verlinde_witness_optimized.json' if not __debug__ else 'low_verlinde_witness_normal.json'))
    target.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))


if __name__=='__main__':main()
