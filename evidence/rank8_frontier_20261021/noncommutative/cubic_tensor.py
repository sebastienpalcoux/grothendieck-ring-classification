"""Complete small-rank rational tensor cones after integral cubic Verlinde."""
import argparse,itertools,json
import central_integral_filters as f
c=f.c

def prepare(R,a,cols):
    _,high=f.v.modular.full.base.grams.high_columns(a,c.s.Matrix.hstack(*map(c.s.Matrix,cols)))
    vectors=[(0,)+tuple(v) for v,z in high]
    matrix=c.s.Matrix.hstack(*map(c.s.Matrix,vectors));coordinates=list(matrix.T.rref()[1])
    triples=list(itertools.combinations_with_replacement(range(1,5),3))
    pairs=list(itertools.combinations_with_replacement(range(1,5),2))
    products=[]
    for i,j in pairs:
        products.append([sum(cols[i][u]*cols[j][v]*R[u][v][k] for u in range(8) for v in range(8))-int(i==j and k==0) for k in range(8)])
    bases={};cache={}
    def decide(counts,coefficients):
        support=tuple(i for i,n in enumerate(counts) if n)
        if support not in bases:
            c.require(matrix[:,support].rank()==len(coordinates),'full-rank active Gram support')
            candidates=[]
            for indices in itertools.combinations(support,len(coordinates)):
                minor=matrix[coordinates,indices];det=int(minor.det())
                if not det:continue
                adj=minor.adjugate()*(1 if det>0 else -1)
                candidates.append((indices,abs(det),[list(map(int,row)) for row in adj.tolist()]))
            bases[support]=candidates
        results=[]
        for pair,product in zip(pairs,products):
            i,j=pair
            target=tuple(product[k]-sum(cols[ell][k]*coefficients[triples.index(tuple(sorted((i,j,ell))))] for ell in range(1,5)) for k in range(8))
            key=(support,target)
            if key not in cache:
                witness=None
                for indices,den,adj in bases[support]:
                    numerators=[sum(q*target[k] for q,k in zip(row,coordinates)) for row in adj]
                    if min(numerators)<0:continue
                    if any(sum(n*vectors[ix][k] for n,ix in zip(numerators,indices))!=den*target[k] for k in range(8)):continue
                    witness={'basis':list(indices),'numerators':numerators,'denominator':den};break
                cache[key]=witness
            results.append(cache[key])
        return results
    return decide

def compute_1154():
    f.v.modular.full.base.install()
    domain=json.loads((c.HERE.parent/'central_integrality/integer_gram_1154.json').read_text())
    filtered=json.loads((c.HERE/'central_integral_filters_1154.json').read_text())
    row=next(r for r in json.loads((c.OLD.parent/'pipeline/census_m3.json').read_text()) if r['id']==domain['id'])
    c.require(row['tensor_sha256']==domain['tensor_sha256']==filtered['tensor_sha256'],'tensor binding')
    R=row['tensor'];a=c.w.data(R);cols=a['lows'][31];decide=prepare(R,a,cols)
    rows=f.cubic_rows(R,a,cols,(0,1,2,3,4));cases=[]
    for i in filtered['combined_survivor_indices']:
        counts=domain['completions'][i];coefficients=f.cubic_values(rows,counts)
        c.require(coefficients is not None,'integral cubic coefficients')
        witnesses=decide(counts,coefficients)
        cases.append({'gram_index':i,'cone_feasible':all(x is not None for x in witnesses),'witnesses':witnesses})
    return {'id':row['id'],'tensor_sha256':row['tensor_sha256'],'scope':'pseudo_unitary_only',
            'low_index':31,'input_gram_patterns':len(cases),'cases':cases,
            'conclusion':'Complete rational cones for all distinguished pairs; integrality and full center associativity are not imposed.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    result=compute_1154();path=c.HERE/'cubic_tensor_1154.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:c.require(result==json.loads(path.read_text()),'complete tensor-cone replay')
    print('PASS R1154: complete exact tensor-cone test;',sum(x['cone_feasible'] for x in result['cases']),'/',result['input_gram_patterns'],'Gram patterns survive')

if __name__=='__main__':main()
