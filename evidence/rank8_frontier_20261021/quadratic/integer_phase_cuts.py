"""Exact global cuts joining integer restrictions to complete phase cones."""
from pathlib import Path
from dataclasses import replace
from fractions import Fraction as Q
import argparse,hashlib,json,math,sys
HERE=Path(__file__).resolve().parent;STAGE=HERE.parent
sys.path.insert(0,str(STAGE/'commutative_integer'))
from features import build,check_integer
from phase_mass import MassCone,st,require
from atomic_cm_real_sts import AtomicCMRealSTS
from atomic_spectrum import table_for
from review_cm_real_sts import fib_group


def match_columns(C,S):
    groups=C.meta['low_character_labels']
    lows={(groups[g],tuple(v)):j for j,(g,v,z)in enumerate(C.low)}
    require(len(lows)==len(C.low),'duplicate labeled low source column')
    highs={tuple(orbit):j for j,orbit in enumerate(C.orbits)}
    out=[]
    for label in S.column_labels:
        if label[0]=='low':out.append(('low',lows[(label[1],tuple(label[2]))]))
        elif label[0]=='high_orbit':
            j=highs[tuple(label[1])]
            require(tuple(map(tuple,label[2]))==tuple((0,)+tuple(C.a['high'][i][0])for i in C.orbits[j]),'high restriction alignment differs')
            out.append(('high',j))
        else:out.append(('auxiliary',None))
    return out


def specialize(C,S,values):
    check_integer(S,values);matched=match_columns(C,S);low=[];high=[]
    for n,(kind,j)in zip(values,matched):
        if kind=='low':
            require(n in(0,1),'low count is not one-hot')
            if n:low.append(j)
        elif kind=='high'and n:high.append((j,n))
    require(len(low)==7,'distinguished low count differs')
    return MassCone(C,low,high)


def make_cut(C,S,ep,base_covector):
    """Minimize y on every complete high phase fiber; check all auxiliaries."""
    require(len(base_covector)==C.nrows,'base phase covector length differs')
    rational=list(map(Q,base_covector));denominator=math.lcm(*(x.denominator for x in rational))
    y=[int(x*denominator)for x in rational]
    def dot(j):return sum(y[i]*a for i,a in C.column(j).items())
    low=[dot(j)for j in range(C.offset)]
    high=[];argmin=[]
    for oi in range(len(C.orbits)):
        values=[dot(C.offset+oi*C.nt+ti)for ti in range(C.nt)]
        best=min(values);high.append(best);argmin.append(values.index(best))
    auxiliary=[dot(j)for j in range(C.high_end,C.nvars)]
    require(all(x>=0 for x in auxiliary),'negative complete auxiliary phase column')
    coefficients=tuple(low[j] if kind=='low' else high[j] if kind=='high' else 0 for kind,j in match_columns(C,S))
    rhs=sum(a*b for a,b in zip(y,C.rhs_for(ep)))
    require(isinstance(rhs,int),'nonintegral phase-cut RHS')
    report={'kind':'complete_phase_fiber_global_integer_cut','indicators':list(ep),
            'base_covector':y,'low_column_count':len(low),'high_orbit_count':len(high),
            'complete_phase_types_per_orbit':C.nt,'auxiliary_column_count':len(auxiliary),
            'low_pairings_sha256':st.digest(low),'high_minima':high,'high_argmin':argmin,
            'auxiliary_pairings_sha256':st.digest(auxiliary),'auxiliary_minimum':min(auxiliary)if auxiliary else None,
            'integer_column_labels_sha256':st.digest(S.column_labels),
            'coefficients_sha256':st.digest(coefficients),'rhs':rhs,
            'source_phase_metadata_sha256':st.digest(C.meta)}
    return coefficients,rhs,report


def append_cut(S,coefficients,rhs,report):
    require(len(coefficients)==len(S.columns),'cut coefficient count differs')
    upper=rhs-sum(min(0,a*bound)for a,bound in zip(coefficients,S.bounds))
    require(upper>=0,'global cut contradicts the original finite box')
    columns=tuple(tuple(col)+(a,)for col,a in zip(S.columns,coefficients))
    columns += ((0,)*len(S.rhs)+(1,),)
    target=tuple(S.rhs)+(rhs,);bounds=tuple(S.bounds)+(upper,)
    labels=tuple(S.column_labels)+(('phase_cut_slack',st.digest(report)),)
    rows=tuple(S.row_labels)+(('global_phase_fiber_inequality',st.digest(report)),)
    h=hashlib.sha256()
    for col in columns:h.update((repr(col)+'\n').encode())
    meta={'kind':'integer_reconstruction_with_global_phase_cut','previous_metadata_sha256':st.digest(S.metadata),
          'cut_sha256':st.digest(report),'rows':len(target),'variables':len(columns),
          'columns_sha256':h.hexdigest(),'rhs_sha256':st.digest(target),'bounds_sha256':st.digest(bounds),
          'column_labels_sha256':st.digest(labels),'row_labels_sha256':st.digest(rows)}
    return replace(S,columns=columns,rhs=target,bounds=bounds,column_labels=labels,row_labels=rows,metadata=meta)


def control():
    R=fib_group(True);C=AtomicCMRealSTS(R,4);T=table_for(R,C.a);S=build(C,T)
    saved=json.loads((STAGE/'commutative_integer/control.json').read_text());require(saved['metadata']==S.metadata,'actual center base differs')
    values=saved['integer_witness'];check_integer(S,values)
    ep=list(next(iter(st.old.ht.indicator_choices(R))));tests=[]
    for sign in(1,-1):
        y=[0]*C.nrows;y[C.sts_rows[1][0]]=sign
        co,b,report=make_cut(C,S,ep,y);slack=b-sum(a*n for a,n in zip(co,values))
        require(slack>=0,'actual center violates valid phase-fiber cut')
        augmented=append_cut(S,co,b,report);check_integer(augmented,values+[slack])
        tests.append({'cut':report,'actual_slack':slack,'augmented_metadata':augmented.metadata})
    return {'kind':'global_phase_cut_actual_center_control','model':'Fibonacci tensor Vec(C4)',
            'tensor_sha256':st.digest(R),'all_actual_integer_equations_retained':True,'tests':tests}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');a=p.parse_args()
    result=control();path=HERE/'integer_phase_cuts_results.json'
    if a.write:path.write_text(json.dumps(st.encode(result),indent=2)+'\n')
    else:require(st.encode(result)==json.loads(path.read_text()),'phase-cut control differs')
    print('PASS complete-fiber global phase cuts retain the actual integer center',flush=True)


if __name__=='__main__':main()
