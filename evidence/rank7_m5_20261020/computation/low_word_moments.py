"""Exact low-object word moments of fixed necessary-data witnesses."""
import argparse,itertools,json,sys,time
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
q=modular.q


def analyze(rid,rows,identity,max_degree=6):
    N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    ds,D,B,zs,transport,signs=q.source_data(N,rid);table=modular.ExactQuadraticCharacterTable(N,ds,5);K=table.K;n=len(N)
    spectral={};active=[i for i in range(n) if i!=table.fp]
    for v,c in rows:
        z=sum((K(v[i])*table.ds[i] for i in range(n)),K.zero)
        lam=tuple(table.D*sum((K(v[i])*table.rows[E][i] for i in range(n)),K.zero)/(table.codegrees[E]*z) for E in active)
        spectral[lam]=spectral.get(lam,K.zero)+K(c)*z*z/table.D**2
    records=[]
    for degree in range(4,max_degree+1):
        violations=[];count=0
        for indices in itertools.combinations_with_replacement(range(n-1),degree):
            total=K.zero
            for lam,weight in spectral.items():
                prod=weight
                for E in indices:prod*=lam[E]
                total+=prod
            rational=K.to_sympy(total);count+=1
            if rational.is_Integer is not True or rational<0:
                violations.append({'indices':[active[i] for i in indices],'value':str(rational)})
        rec={'degree':degree,'tested':count,'violations':violations};records.append(rec)
        print(json.dumps({'id':rid,**identity,'degree':degree,'tested':count,'violations':len(violations),'examples':violations[:3]}),flush=True)
    return {'id':rid,**identity,'rank':sum(c for v,c in rows),'distinct_joint_eigenvalues':len(spectral),'moments':records}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--max-degree',type=int,default=6);args=ap.parse_args();result=[]
    rid='R7_5_3895';records=json.loads((HERE/(rid+'_low_verlinde_snapshot.json')).read_text())['results'];domains=json.loads((HERE.parent/'integral_gram'/f'{rid}_domains.json').read_text())
    for rec in records:
        if rec.get('active_branch')!=0:continue
        dom=next(a for a in domains if a['low_index']==rec['index']);rows=[((1,0,0,0,0,0,0),1)]+[(tuple(v),1) for v in dom['low']]
        for idx,count in rec['actual_support']:rows.extend(((0,)+tuple(v),count) for v,g,z in dom['orbits'][idx//10])
        result.append(analyze(rid,rows,{'active_branch':0},args.max_degree))
    for name in ['R7_5_5039_full_field_verlinde_chi8_0.json','R7_5_5039_full_field_verlinde_chi8_2.json']:
        data=json.loads((HERE.parent/'integral_gram'/name).read_text())
        for rec in data['results']:
            if not rec.get('exact_feasible'):continue
            rows=[((1,0,0,0,0,0,0),1)]+[(tuple(v),1) for v in data['low']]
            for item in rec['support']:rows.extend(((0,)+tuple(v),item['count']*item['multiplicity_unit']) for v,g,z in data['orbits'][item['orbit']])
            result.append(analyze(data['id'],rows,{'source':name,'case':rec['case']},args.max_degree))
    (HERE/'low_word_moment_results.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
