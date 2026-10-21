"""Complete unrestricted scope-gate applicability for R439,R455,R567.

All three gates succeed. R439/R567 additionally need the spherical
dimension-field obstruction, proved in ADDITIONAL_SCOPE_GATES.md.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'review'))
import verify_nc_gate_unrestricted as gate
s=gate.old.s;need=gate.need

def rational_audit(R):
    a=gate.old.ScalarCharacters(R);n=len(R)
    need(all(N.T==a.N[a.du[i]] for i,N in enumerate(a.N)),'star-closed regular algebra')
    commutators=s.Matrix.vstack(*(N*M-M*N for N in a.N for M in a.N))
    W=s.Matrix.hstack(*commutators.nullspace())
    need(W.cols==4,'complete four-dimensional scalar regular summand')
    P=W*(W.T*W).inv()*W.T;Q=s.eye(n)-P
    need(P*P==P and Q*Q==Q and P*Q==s.zeros(n),'orthogonal rational projectors')
    need(all(P*N==N*P and Q*N==N*Q for N in a.N),'regular invariant summands')
    need(P.rank()==Q.rank()==4,'regular ranks four plus four')
    scalar=[P*N for N in a.N];matrix=[Q*N for N in a.N]
    scalar_span=s.Matrix.hstack(*(s.Matrix(list(N)) for N in scalar))
    matrix_span=s.Matrix.hstack(*(s.Matrix(list(N)) for N in matrix))
    need(scalar_span.rank()==matrix_span.rank()==4,'complete block algebra dimensions')
    need(all(N*M==M*N for N in scalar for M in scalar),'scalar block commutative')
    need(a.p.degree()==4 and s.gcd(a.p,a.p.diff()).degree()==0,'separable complete scalar polynomial')
    B=[matrix[j] for j in matrix_span.rref()[1]]
    equations=s.Matrix.vstack(*(s.Matrix.hstack(*(s.Matrix(list(N*M-M*N)) for N in B)) for M in B))
    need(len(B)-equations.rank()==1,'matrix block central simple over C')
    eigenvalue=s.trace(Q*a.C)/4
    need(Q*a.C==eigenvalue*Q and eigenvalue/2==a.matrix_codegree,'matrix formal codegree including multiplicity two')
    components=[]
    for f,m in a.components:
        need(m==1 and f.is_irreducible,'complete irreducible scalar component')
        K,ds,D,pD=a.component(f)
        need(all(ds[i]*ds[j]==sum((K(R[i][j][k])*ds[k] for k in range(n)),K.zero) for i in range(n) for j in range(n)),'all scalar maps satisfy multiplication')
        components.append({'scalar_polynomial':gate.old.pc(f),'dimension_polynomial':gate.old.pc(pD)})
    need(sum(len(r['scalar_polynomial'])-1 for r in components)==4,'all scalar characters accounted')
    return {'complex_algebra':'C^4 + M2(C)','regular_block_ranks':[4,4],
            'scalar_components':components,'matrix_casimir_eigenvalue':str(eigenvalue),
            'matrix_formal_codegree':str(a.matrix_codegree),
            'scalar_projector':[[str(x) for x in row] for row in P.tolist()],
            'matrix_projector':[[str(x) for x in row] for row in Q.tolist()]}

def compute(source):
    R=source['tensor'];need(hashlib.sha256(json.dumps(R,separators=(',',':')).encode()).hexdigest()==source['tensor_sha256'],'source hash')
    vals,p,statistics=gate.unrestricted(R);a=gate.old.ScalarCharacters(R);du=a.du
    ordinary=gate.old.character_obstructions(R,a.cf);fp=gate.old.pc(a.fp()[0])
    ordinary_gate=[r['factor'] for r in ordinary if r['obstruction'] is None]==[fp]
    signs=[(1,)+tail for tail in itertools.product((-1,1),repeat=7) if all(((1,)+tail)[i]==((1,)+tail)[du[i]] for i in range(8))]
    masks=[tuple(g[x]*g[y]*g[z] for orb in p['active'] for x,y,z in [orb[0]]) for g in signs]
    groups={}
    for v in vals:
        T=gate.old.from_values(R,p,v);gate.old.validate_general(T)
        representative=min(tuple(x*y for x,y in zip(v,mask)) for mask in masks)
        groups.setdefault(representative,[]).append(v)
    reports=[]
    for representative,members in sorted(groups.items()):
        T=gate.old.from_values(R,p,representative);gauge=gate.old.proofs.gauge_original(T,R)
        audit=rational_audit(T)
        if gauge is not None:
            need(all(T[i][j][k]==gauge[i]*gauge[j]*gauge[k]*R[i][j][k] for i in range(8) for j in range(8) for k in range(8)),'full gauge equality')
            report={'kind':'spherical_section','gauge_signs':gauge}
        else:
            signed=gate.old.ScalarCharacters(T);characters=gate.old.character_obstructions(T,a.cf+signed.cf)
            for character in characters:
                obstruction=character['obstruction']
                if obstruction and obstruction['kind']=='field_degree':
                    component=next(f for f,m in signed.components if gate.old.pc(f)==character['factor'])
                    required=next(f for f,m in a.cf if gate.old.pc(f)==obstruction['polynomial'])
                    K,dimensions,delta,dimension_poly=signed.component(component)
                    need(component.is_irreducible and required.is_irreducible,'dimension field and codegree irreducibility')
                    need(component.degree()==1 and required.degree()==2,'specific rational/quadratic field obstruction')
                    need(delta==K(24) and all(len(d.to_list())<=1 for d in dimensions),'rational signed simple dimensions and nonzero dimension24')
                    need(component.degree()%required.degree()!=0,'required codegree cannot lie in signed dimension field')
                    character['field_obstruction_validation']={'signed_dimension_field_degree':1,
                        'signed_dimension':'24','ordinary_formal_codegree_degree':2,
                        'ordinary_formal_codegree_polynomial':gate.old.pc(required),
                        'simple_dimensions':[gate.old.ec(d) for d in dimensions],
                        'theorem':'Ostrik1309.4822 Theorem2.13: delta/f is a central simple dimension in the signed character field'}
            supported=all(c['obstruction'] and c['obstruction']['kind'] in ('zero','duality','norm','field_degree') for c in characters)
            report={'kind':'nongauge_excluded' if supported else 'nongauge_character_survives',
                    'characters':characters}
        reports.append({'representative':list(representative),'members':len(members),'rational_block_audit':audit,**report})
    success=ordinary_gate and all(r['kind']!='nongauge_character_survives' for r in reports)
    return {'id':source['id'],'tensor_sha256':source['tensor_sha256'],
            'outcome':'Galois_pseudo_unitary_reduction' if success else 'scope_gate_not_proved',
            'scope':'general_complex_fusion_category; no existence or nonexistence conclusion',
            'signed_variables':len(p['domains']),'normalized_indicator_domains_used':False,
            'commutativity_assumed':False,'complete_signed_count':len(vals),
            'native_statistics':statistics,
            'signed_values_sha256':hashlib.sha256(json.dumps(vals,separators=(',',':')).encode()).hexdigest(),
            'ordinary_rational_block_audit':rational_audit(R),'ordinary_characters':ordinary,
            'ordinary_FP_orbit_only':ordinary_gate,'gauge_classes':reports}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    census=json.loads((gate.OLD/'pipeline/census_m3.json').read_text())
    result=[compute(next(row for row in census if row['id']==f'R8_3_{i}')) for i in (439,455,567)]
    path=HERE/'additional_scope_gates.json'
    if args.write:path.write_text(json.dumps(result,indent=2)+'\n')
    else:need(result==json.loads(path.read_text()),'additional complete scope-gate replay')
    for row in result:
        print('PASS',row['id'],row['complete_signed_count'],row['outcome'],
              [(r['kind'],r['members']) for r in row['gauge_classes']])

if __name__=='__main__':main()
