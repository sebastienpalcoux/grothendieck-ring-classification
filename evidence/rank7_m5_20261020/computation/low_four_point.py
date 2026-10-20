"""Exact four-point low fusion constraints on feasible necessary-data ghosts.

For low objects E,F,G,H, computes multiplicity of the unit in E F G H.
Also computes the Gram matrix of low-to-high fusion coefficients for each E.
A violation rejects only the supplied ghost, not every potential category.
"""
import argparse,hashlib,itertools,json,sys,time
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
from branch_lattice import negative_vector
q=modular.q


def audit(rid,rows,identity):
    N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    ds,D,B,zs,transport,signs=q.source_data(N,rid)
    table=modular.ExactQuadraticCharacterTable(N,ds,5);K=table.K;n=len(N)
    dual=[next(j for j in range(n) if N[i][j][0]) for i in range(n)]
    dual_chars=[next(j for j,row in enumerate(table.rows) if tuple(row)==tuple(character[dual[i]] for i in range(n))) for character in table.rows]
    dimensions=[sum((K(v[i])*table.ds[i] for i in range(n)),K.zero) for v,c in rows]
    values=[[sum((K(v[i])*character[i] for i in range(n)),K.zero) for character in table.rows] for v,c in rows]
    q.require([[sum(c*v[i]*v[j] for v,c in rows) for j in range(n)] for i in range(n)]==B,'full restriction Gram identity')
    coeffs={};violations=[]
    for length in (3,4):
        for indices in itertools.combinations_with_replacement(range(n),length):
            total=K.zero
            for (_,count),val,z in zip(rows,values,dimensions):
                prod=K(count)/z**(length-2)
                for E in indices:prod*=val[E]/table.codegrees[E]
                total+=prod
            total*=table.D**(length-2)
            rational=K.to_sympy(total)
            coeffs[indices]=rational
            if not rational.is_Integer or rational<0:
                violations.append({'indices':indices,'value':str(rational)})
    grams=[]
    for E in range(n):
        A=s.Matrix([[coeffs[tuple(sorted((E,F,dual_chars[G])))] for G in range(n)] for F in range(n)])
        # B B*: sum of unknown low-to-high coefficients times conjugates.
        moment=s.Matrix([[coeffs[tuple(sorted((dual_chars[E],E,F,dual_chars[G])))] for G in range(n)] for F in range(n)])
        residual=moment-A*A.T
        bad_entries=[(i,j,str(residual[i,j])) for i in range(n) for j in range(i+1) if residual[i,j].is_Integer is not True or residual[i,j]<0]
        vec=negative_vector(residual.tolist()) if all(x.is_Rational for x in residual) else None
        grams.append({'character':E,'bad_entries':bad_entries,'negative_vector':vec,'residual':[[str(x) for x in row] for row in residual.tolist()]})
    return {'id':rid,**identity,'center_rank':sum(c for v,c in rows),'triple_tests':84,'quartic_tests':210,
            'nonunit_quartic_tests':126,'violations':violations,'coefficients':{','.join(map(str,key)):str(value) for key,value in coeffs.items()},'residual_grams':grams,'scope':'Only rejects supplied necessary-data witness if a necessary condition fails.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full-field',action='store_true');ap.add_argument('--ring',default='R7_5_3895');args=ap.parse_args()
    results=[];files=[]
    if args.full_field:
        names=['R7_5_3895_full_field_verlinde_branch165.json','R7_5_5039_full_field_verlinde_chi8_0.json','R7_5_5039_full_field_verlinde_chi8_2.json']
        for name in names:
            path=HERE.parent/'integral_gram'/name;data=json.loads(path.read_text());files.append(path)
            for rec in data['results']:
                if not rec.get('exact_feasible'):continue
                rows=[((1,0,0,0,0,0,0),1)]+[(tuple(v),1) for v in data['low']]
                for item in rec['support']:
                    rows.extend(((0,)+tuple(v),item['count']*item['multiplicity_unit']) for v,g,z in data['orbits'][item['orbit']])
                results.append(audit(data['id'],rows,{'file':name,'case':rec['case']}))
    else:
        rid=args.ring;path=HERE/(rid+'_low_verlinde_snapshot.json');files.append(path)
        records=json.loads(path.read_text())['results'];domains=json.loads((HERE.parent/'integral_gram'/f'{rid}_domains.json').read_text())
        for rec in records:
            if not rec.get('exact_feasible'):continue
            dom=next(a for a in domains if a['low_index']==rec['index'])
            rows=[((1,0,0,0,0,0,0),1)]+[(tuple(v),1) for v in dom['low']]
            for idx,count in rec['actual_support']:
                rows.extend(((0,)+tuple(v),count) for v,g,z in dom['orbits'][idx//10])
            results.append(audit(rid,rows,{'active_branch':rec.get('active_branch'),'case':rec['case']}))
    out={'status':'COMPLETED','optimized_python':not __debug__,'source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files+[Path(__file__)]},'results':results}
    suffix='full_field' if args.full_field else args.ring
    (HERE/('low_four_point_'+suffix+'.json')).write_text(json.dumps(out,indent=2)+'\n')
    for r in results:print(json.dumps({k:v for k,v in r.items() if k not in ('residual_grams','coefficients')}),flush=True)
    print(json.dumps({'bad_grams':sum(bool(g['bad_entries'] or g['negative_vector']) for r in results for g in r['residual_grams'])}))

if __name__=='__main__':main()
