"""Exact exploratory degree-two Borel compression moments of q=5 ghosts."""
import json,sys
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'criteria'))
import q5_modular_low as modular
from branch_lattice import negative_vector
q=modular.q


def main():
    rid='R7_5_3895';N=next(r['tensor'] for r in json.loads((HERE/'source_frontier.json').read_text()) if r['id']==rid)
    d,D,gram,zs,transport,signs=q.source_data(N,rid)
    table=modular.ExactQuadraticCharacterTable(N,d,5);K=table.K
    records=json.loads((HERE/(rid+'_low_verlinde_snapshot.json')).read_text())['results']
    domains=json.loads((HERE.parent/'integral_gram'/f'{rid}_domains.json').read_text())
    basis=s.Matrix.hstack(*[s.eye(7)[:,i] for i in range(3)],s.eye(7)[:,3]+s.eye(7)[:,4],s.eye(7)[:,5]+s.eye(7)[:,6])
    M0=basis.T*basis;result=[]
    for record in records:
        dom=next(a for a in domains if a['low_index']==record['index']);label=dom['cases'][record['case']]['label']
        lows=[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']];assigned=dict(zip(label,lows))
        def values(v):
            numbers=[sum((K(v[i])*row[i] for i in range(7)),K.zero)/f for row,f in zip(table.rows,table.codegrees)]
            compressed=numbers[:3]+[numbers[3]+numbers[4],numbers[5]+numbers[6]]
            out=[s.simplify(K.to_sympy(x)) for x in compressed]
            q.require(all(x.is_Rational for x in out),'torus-trivial coordinates are rational')
            return s.Matrix(out)
        lowS=s.Matrix([[s.simplify(K.to_sympy(sum((K(assigned[j][k])*table.rows[i][k] for k in range(7)),K.zero)/table.codegrees[i])) for j in range(7)] for i in range(7)])
        M1=s.simplify(basis.T*lowS*basis)
        fixed=[(v,1) for v in lows]
        for index,count in record['actual_support']:
            if index%10==0:fixed.extend(((0,)+tuple(v),count) for v,_,z in dom['orbits'][index//10])
        M2=sum((count*values(v)*values(v).T for v,count in fixed),s.zeros(5))
        tests={'upper_endpoint':s.Rational(1,2)*M0+s.Rational(1,2)*M1-M2,
               'gap_minus_half_minus_fifth':M2+s.Rational(7,10)*M1+s.Rational(1,10)*M0,
               'gap_minus_fifth_zero':M2+s.Rational(1,5)*M1,
               'gap_zero_tenth':M2-s.Rational(1,10)*M1,
               'gap_tenth_one':M2-s.Rational(11,10)*M1+s.Rational(1,10)*M0}
        certificates=[]
        for name,form in tests.items():
            vector=negative_vector(form.tolist())
            if vector is not None:
                value=(s.Matrix(vector).T*form*s.Matrix(vector))[0]
                certificates.append({'test':name,'vector':vector,'value':str(value)})
        out={'active_branch':record.get('active_branch'),'center_fixed_rank':sum(c for v,c in fixed),
             'M0':[[str(x) for x in row] for row in M0.tolist()],
             'M1':[[str(x) for x in row] for row in M1.tolist()],
             'M2':[[str(x) for x in row] for row in M2.tolist()],
             'violations':certificates}
        result.append(out);print(json.dumps(out),flush=True)
    (HERE/'R7_5_3895_borel_ghost_results.json').write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
