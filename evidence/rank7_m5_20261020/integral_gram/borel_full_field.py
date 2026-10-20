"""Exact Borel spectral moment audit of the newest full-field witnesses."""
import json
import sys
import sympy as s
import explore as e
q=e.q;m=e.m;HERE=e.HERE
sys.path.insert(0,str(HERE.parent/'computation'))
from branch_lattice import negative_vector
from character_induction import evaluate


def audit(path):
    data=json.loads(path.read_text());rid=data['id']
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid);table=m.ExactQuadraticCharacterTable(N,d,5);K=table.K
    normalized=[tuple(x/f for x in row) for row,f in zip(table.rows,table.codegrees)]
    galois=table.automorphisms();orbits=[];seen=set()
    for i,row in enumerate(normalized):
        if i in seen:continue
        orb={normalized.index(tuple(evaluate(x.to_list(),r,K) for x in row)) for r in galois}
        seen|=orb;orbits.append(sorted(orb))
    basis=s.Matrix([[int(i in orb) for orb in orbits] for i in range(7)])
    M0=basis.T*basis;results=[]
    for result in data['results']:
        if not result.get('exact_feasible'):continue
        dom=next(x for x in e.domains(rid) if x['low_index']==result['index']);label=dom['cases'][result['case']]['label']
        lows=[(1,0,0,0,0,0,0)]+[tuple(v) for v in data['low']];assigned=dict(zip(label,lows))
        def values(row):
            vals=[sum((K(c)*x for c,x in zip(row,nrow)),K.zero) for nrow in normalized]
            out=[s.simplify(K.to_sympy(sum((vals[i] for i in orb),K.zero))) for orb in orbits]
            q.require(all(x.is_Rational for x in out),'Borel invariant character values rational')
            return s.Matrix(out)
        lowS=s.Matrix([[s.simplify(K.to_sympy(sum((K(c)*x for c,x in zip(assigned[j],normalized[i])),K.zero))) for j in range(7)] for i in range(7)])
        M1=s.simplify(basis.T*lowS*basis);fixed=[(row,1) for row in lows]
        for item in result['support']:
            if data['phase_records'][item['phase']]['orders']!=[1]:continue
            count=item['count']*item['multiplicity_unit']
            fixed.extend(((0,)+tuple(v),count) for v,g,z in data['orbits'][item['orbit']])
        M2=sum((count*values(row)*values(row).T for row,count in fixed),s.zeros(len(orbits)))
        forms={'upper_endpoint':(M0+M1)/2-M2,
               'gap_minus_half_minus_fifth':M2+s.Rational(7,10)*M1+s.Rational(1,10)*M0,
               'gap_minus_fifth_zero':M2+M1/5,'gap_zero_tenth':M2-M1/10,
               'gap_tenth_one':M2-s.Rational(11,10)*M1+M0/10}
        violations=[]
        for name,form in forms.items():
            vector=negative_vector(form.tolist())
            if vector is not None:violations.append({'test':name,'vector':vector,'value':str((s.Matrix(vector).T*form*s.Matrix(vector))[0])})
        record={'id':rid,'case':result['case'],'character_orbits':orbits,'M0':[[str(x) for x in row] for row in M0.tolist()],
                'M1':[[str(x) for x in row] for row in M1.tolist()],'M2':[[str(x) for x in row] for row in M2.tolist()],
                'violations':violations,'source_file':path.name,'optimized_python':not __debug__}
        print(json.dumps(record),flush=True);results.append(record)
    (HERE/(path.stem+'_borel_audit.json')).write_text(json.dumps(results,indent=2)+'\n')


if __name__=='__main__':
    for name in ['R7_5_3895_full_field_verlinde_branch165.json','R7_5_5039_full_field_verlinde_chi8_0.json','R7_5_5039_full_field_verlinde_chi8_2.json']:
        audit(HERE/name)
