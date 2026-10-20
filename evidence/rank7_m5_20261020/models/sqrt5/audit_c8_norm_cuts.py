#!/usr/bin/env python3
"""Independent direct spectral replay of every exported C8 integer-norm cut.

Does not import integer_norm_cuts, word_coefficients, or low-Verlinde caches.
Old integer chord centers are arbitrary valid centers at every labeling.
"""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import sys
import sympy as s

HERE=Path(__file__).resolve().parent;EVIDENCE=HERE.parents[1]
sys.path.insert(0,str(EVIDENCE/'criteria'))
import q5_center_trace as q
from exact_quadratic_characters import ExactQuadraticCharacterTable


def require(ok,message):
    if not ok:raise ValueError(message)


def rational_part(value,K):
    # Independent linear algebra in the coefficient representation of K.
    deg=K.mod.degree()
    def vec(v):
        c=[s.Rational(str(x)) for x in v.to_list()]
        return s.Matrix([0]*(deg-len(c))+c)
    B=s.Matrix.hstack(vec(K.one),vec(K.from_sympy(s.sqrt(5))))
    ans=B.gauss_jordan_solve(vec(value))[0]
    require(B*ans==vec(value) and all(z.is_Rational for z in ans),'whole group lies in Qsqrt5')
    return F(str(ans[0]))


def independent_conjugate(t):
    # Explicit candidates come from the nearest two integers to t/2.
    k=t.numerator//(2*t.denominator)
    choices={0,max(k,0),max(k+1,0)}
    return max(t*j-j*j for j in choices)


def audit(path):
    system=json.loads(path.read_text());rid=system['id'];record=system['norm_cut_record'];cut=system['norm_cut_coefficients']
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    require(q.tensor_hash(N)==system['source_sha256']==record['source_sha256'],'pinned canonical tensor')
    ds,D,B,zs,T,signs=q.source_data(N,rid);table=ExactQuadraticCharacterTable(N,ds,5);K=table.K
    labels=system['label'];low=[(1,0,0,0,0,0,0)]+[tuple(v) for v in system['low']]
    require(len(labels)==7 and set(labels)==set(range(7)) and labels[0]==table.fp,'complete low labeling')
    assigned={E:row for E,row in zip(labels,low)}
    if 'characters' in record:E,G=record['characters'];centers=record['low_coefficients_at_witness']
    else:
        require(len(record['combinations'])==1 and record['combinations'][0]['coefficient']==1,'single positive product')
        E,G=(record['low_labels'][i] for i in record['combinations'][0]['objects']);centers=record['low_tangent']
    require(all(type(a)is int for a in centers),'arbitrary integral chord centers')
    x=list(map(F,record['x']))
    dual={i:next(j for j,row2 in enumerate(table.rows) if row2==tuple(row[table.du[k]] for k in range(7))) for i,row in enumerate(table.rows)}
    source=[sum(assigned[E][i]*assigned[G][j]*N[i][j][k] for i in range(7) for j in range(7)) for k in range(7)]
    alpha=[2*a+1-sum(c*v for c,v in zip(x,row)) for a,row in zip(centers,low)]
    constant=sum(c*v for c,v in zip(x,source))-sum(a*(a+1) for a in centers)
    groups=[low]+[[(0,)+tuple(row[0]) for row in orb] for orb in system['orbits']]
    @lru_cache(None)
    def restriction(row):
        z=sum((K(row[i])*table.ds[i] for i in range(7)),K.zero)
        vals=tuple(sum((K(row[i])*ch[i] for i in range(7)),K.zero) for ch in table.rows)
        return z,vals
    @lru_cache(None)
    def moment(group_index,word):
        total=K.zero
        for row in groups[group_index]:
            z,chars=restriction(row);value=table.D**(len(word)-2)/z**(len(word)-2)
            for char in word:value*=chars[char]/table.codegrees[char]
            total+=value
        return rational_part(total,K)
    quartic=(E,G,dual[E],dual[G])
    known_n=[];orbit_n=[]
    for H in labels:
        if H==table.fp:
            known_n.append(F(int(E==dual[G])));orbit_n.append([F(0)]*len(system['orbits']))
        else:
            word=(E,G,dual[H]);known_n.append(moment(0,word))
            orbit_n.append([moment(j+1,word) for j in range(len(system['orbits']))])
    rhs=constant+sum(a*n for a,n in zip(alpha,known_n))-moment(0,quartic)
    costs=[]
    for j,group in enumerate(groups[1:]):
        correction=sum(independent_conjugate(sum(c*v for c,v in zip(x,row))) for row in group)
        costs.append(moment(j+1,quartic)+correction-sum(a*n[j] for a,n in zip(alpha,orbit_n)))
    require(source==cut['source_product'],'source forgetful product recomputed for current labels')
    require([str(a) for a in alpha]==cut['low_linear_weights'],'current low chord coefficients')
    require(str(constant)==cut['constant'] and list(centers)==cut['low_chord_centers'],'current chord constant and centers')
    require([str(c) for c in costs]==cut['coefficients'] and str(rhs)==cut['rhs'],'every direct spectral cut coefficient')
    require(list(quartic)==cut['quartic_word'],'correct dualized quartic word')
    # Locate and verify the actual row of the exported integer system, allowing
    # only a positive row scaling and its single nonnegative slack variable.
    phase_labels=system['phase_labels'];cols=system['columns'];target=system['rhs']
    expected=[F(l['multiplicity_unit'])*costs[l['orbit']] for l in phase_labels]
    candidates=[]
    for row,b in enumerate(target):
        if not b or not rhs:continue
        scale=F(b)/rhs
        if scale<=0:continue
        if not all(F(c[row])==scale*v for c,v in zip(cols,expected)):continue
        tail=[(j,F(cols[j][row])) for j in range(len(phase_labels),len(cols)) if cols[j][row]]
        if len(tail)==1 and tail[0][1]==-scale:candidates.append((row,str(scale),tail[0][0]))
    require(len(candidates)==1,'unique exact integer-system row for the audited norm cut')
    return {'file':path.name,'case':system['case'],'chi8_branch':system['chi8_branch'],'id':rid,
            'status':'PASS','source_sha256':q.tensor_hash(N),'system_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'low_labels':labels,'characters':[E,G],'source_product':source,'low_chord_centers':centers,
            'cut_rhs':str(rhs),'orbit_coefficient_count':len(costs),'system_row':candidates[0][0],
            'positive_row_scale':candidates[0][1],'slack_column':candidates[0][2],
            'scope':'Every center-row coefficient and appended system row independently recomputed; arbitrary old integer chord centers remain valid at the current labeling.'}


if __name__=='__main__':
    paths=sorted((EVIDENCE/'criteria').glob('*_c8_case*_system.json'))
    require(len(paths)==6,'six complete current C8 representative systems')
    records=[audit(path) for path in paths]
    report={'status':'PASS','optimized_python':not __debug__,'systems':records,
            'numerical_optimizers_used':False,'shared_cut_or_word_coefficient_builders_used':False}
    out=HERE/f'c8_norm_cut_audit_{"optimized" if not __debug__ else "normal"}.json'
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
