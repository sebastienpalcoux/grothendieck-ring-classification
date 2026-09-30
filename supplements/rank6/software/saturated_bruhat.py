"""Vector Bruhat equations on a saturated dimension-block cyclic module.

For a real quadratic character of conductor f and its twist-fixed vector w,
the finite-level representation gives ST^nSw=chi(n)T^(-n^-1)Sw for every
unit n modulo f. A twist-one low coordinate therefore gives the linear
equation sum_Z S_AZ L_chi(FZ) theta_Z^n=chi(n)L_chi(FA).

Rows below use complete column-major (restriction type, phase type) slots.
They are necessary equations, never a feasibility or existence certificate.
"""
import math,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'research/round5/unification'))
from exact import require,evaluate
from dimension_block_support import saturated_characters
from equality_modrep import induced_model

def verify_bruhat_model(certificate):
    f=certificate['conductor'];chi=certificate['character'];model=induced_model(f,chi)
    S=model['S'];T=model['T'];B=model['basis'];units=[n for n in range(f) if math.gcd(n,f)==1]
    for n in units:
        require(S*(T**n)*S*B==chi[n]*(T**((-pow(n,-1,f))%f))*S*B,'finite induced Bruhat identity failed')
    return dict(conductor=f,unit_powers=units,fixed_character_dimension=B.cols,vector_checks=len(units)*B.cols)

def phase_equations(data,columns,low_columns,labelling,certificate):
    pack=saturated_characters(data);C=pack['C'];E=pack['E'];F=pack['F'];EF=pack['EF'];f=certificate['conductor']
    require(F%f==0,'retained phase field does not contain all conductor roots')
    require(tuple(labelling) in list(map(tuple,data['tab'].assignments(low_columns))),'invalid low character labelling')
    matches=[c for c in pack['characters'] if c['conductor']==f and c['fourier']==certificate['lambda_value']]
    require(len(matches)==1,'saturated character not uniquely identified');ch=matches[0]
    model=verify_bruhat_model(certificate);units=model['unit_powers'];nt=len(data['phases'])
    embed=lambda z:z if E==C else evaluate(z.to_list(),E.unit**(EF//F),E)
    dim=lambda v:sum((C(n)*z for n,z in zip(v,data['dims'])),C.zero)
    def L(v):
        q=dim(v)/data['DD']
        return sum((a*embed(evaluate(q.to_list(),C.unit**b,C)) for a,b in zip(ch['weights'],pack['reps'])),E.zero)
    def sa(a,v):
        return embed(dim(low_columns[a])/data['DD']*sum((C(n)*z for n,z in zip(v,data['tab'].rows[labelling[a]])),C.zero))
    require(all(sa(a,low_columns[b])==sa(b,low_columns[a]) for a in range(len(low_columns)) for b in range(len(low_columns))),'low S block is not symmetric')
    roots={tuple(C.unit**((F//f)*j*k) for k in range(1,len(data['phases'][0])+1)):j for j in range(f)}
    row_labels=[(n,a) for n in units for a in range(len(low_columns))]
    rows=[[E.zero]*(len(columns)*nt)for _ in row_labels];rhs=[];forbidden=set()
    for n,a in row_labels:
        rhs.append(E(certificate['character'][n])*L(low_columns[a])-sum((sa(a,v)*L(v)for v in low_columns),E.zero))
    for i,col in enumerate(columns):
        v=(0,)+tuple(col);ell=L(v)
        if not ell:continue
        weights=[sa(a,v)*ell for a in range(len(low_columns))]
        for ti,phase in enumerate(data['phases']):
            power=roots.get(tuple(phase))
            if power is None:forbidden.add(i*nt+ti);continue
            theta=E.unit**((EF//f)*power)
            for row,(n,a) in zip(rows,row_labels):row[i*nt+ti]=weights[a]*theta**n
    return rows,rhs,sorted(forbidden),dict(model,cyclotomic_rows=len(rows),calculation_conductor=EF,row_labels=list(map(list,row_labels)))
