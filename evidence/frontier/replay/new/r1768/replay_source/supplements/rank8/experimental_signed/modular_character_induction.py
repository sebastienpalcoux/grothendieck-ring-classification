"""Exact modular low-twist equations refining character-aware central induction.

The mathematical input is a pseudo-unitary category with commutative ring and
rational/quadratic character field. All finite hypotheses and all character
assignments are reconstructed. Discovery may use LP; verification is exact.
"""
from spectral_induction import (reciprocity_data,Ineligible,Spectrum,high_columns,
    low_failure,indicator_choices,system_rotation,farkas,check_farkas,
    require,s,Q,math,itertools)
from higher_traces import trace_types


def rational_rows(coeff,rhs,K):
    degree=K.mod.degree()
    def coordinates(x):
        z=list(reversed(x.to_list()))
        return z+[K.dom.zero]*(degree-len(z))
    cc=[coordinates(x) for x in coeff];bb=coordinates(rhs)
    for k in range(degree):
        row=[Q(str(x[k])) for x in cc];v=Q(str(bb[k]))
        den=math.lcm(v.denominator,*(x.denominator for x in row))
        row=[int(x*den) for x in row];v=int(v*den)
        gcd=math.gcd(v,*row) or 1
        row=[x//gcd for x in row];v//=gcd
        # Redundant zero equations are omitted by a deterministic rule.
        if any(row) or v:yield row,v


def equation_system(R,data,tab,cols,ep,height,lab,spec=None):
    K=tab.K;n=len(R)
    require(K.mod.degree()<=(1 if data['q']==1 else 2),
            'the whole character field must lie in the relative trace field')
    sq=K.from_sympy(s.sqrt(data['q']))
    types,_=trace_types(data['q'],data['primes'],height)
    one=types.index(tuple((Q(1),Q(0)) for _ in range(height)))
    phases=[K(t[0][0])+K(t[0][1])*sq for t in types]
    L=s.Matrix.hstack(*map(s.Matrix,cols))
    if spec is None:
        _,high=high_columns(data,L);spec=Spectrum(tab,cols,high)
    A,b,meta=system_rotation(R,data,L,ep,height)
    labels=meta['labels']
    rows,rhs=spec.balance(labels,len(A[0]),one);A+=rows;b+=rhs
    n_balance=len(rows);forbidden=set(map(tuple,spec.forbidden))
    keep=[j for j in range(len(A[0])) if j>=len(labels) or tuple(labels[j][0]) not in forbidden]
    A=[[row[j] for j in keep] for row in A]
    tuples=dict(zip(spec.vectors,spec.types));n_pair=0
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=tab.D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),K.zero)
        coeff=[weights[(0,)+tuple(labels[j][0])]*phases[labels[j][1]] if j<len(labels) else K.zero for j in keep]
        for row,value in rational_rows(coeff,rhs,K):A.append(row);b.append(value);n_pair+=1
    return A,b,{'balance_equations':n_balance,'modular_equations':n_pair,'variables':len(keep),'equations':len(A)}


def certificate(R,height=6,progress=None):
    try:data,tab=reciprocity_data(R)
    except Ineligible:return None
    if tab.K.mod.degree()>(1 if data['q']==1 else 2):return None
    branches=[]
    for ix,cols in enumerate(data['lows']):
        branch={'columns':list(map(list,cols))}
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:branch['ordinary']=why
        else:
            assignments=tab.assignments(cols);branch['labellings']=list(map(list,assignments))
            if assignments:
                L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=Spectrum(tab,cols,high)
                branch['spectrum']=sp.metadata()
                if not sp.missing_low:
                    cases=[]
                    for lab in assignments:
                        indicators=[]
                        for ep in indicator_choices(R):
                            if progress:progress(ix,list(lab),list(ep))
                            A,b,meta=equation_system(R,data,tab,cols,ep,height,lab,sp);y=farkas(A,b)
                            if y is None:return None
                            check_farkas(A,b,y)
                            indicators.append({'indicators':list(ep),'system':meta,'y':y,
                                'bTy':sum(x*z for x,z in zip(b,y))})
                        cases.append({'labelling':list(lab),'indicators':indicators})
                    branch['cases']=cases
        branches.append(branch)
    return {'kind':'modular_character_induction','version':1,'height':height,
            'q':data['q'],'table':tab.metadata(),'column_counts':list(map(len,data['columns'])),
            'branches':branches}


def verify(R,c):
    data,tab=reciprocity_data(R)
    require(c['kind']=='modular_character_induction' and c.get('version')==1,'wrong modular certificate kind/version')
    require(tab.K.mod.degree()<=(1 if data['q']==1 else 2),'character field outside trace field')
    require(isinstance(c['height'],int) and 2<=c['height']<=12,'invalid trace height')
    require(c['q']==data['q'] and c['table']==tab.metadata(),'incorrect character data')
    require(c['column_counts']==list(map(len,data['columns'])),'incomplete low columns')
    require(len(c['branches'])==len(data['lows']),'omitted low branch')
    for cols,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==list(map(list,cols)),'wrong low branch')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'wrong ordinary obstruction');continue
        aa=tab.assignments(cols);require(branch['labellings']==list(map(list,aa)),'omitted or altered character assignment')
        if not aa:continue
        L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=Spectrum(tab,cols,high)
        require(branch['spectrum']==sp.metadata(),'wrong spectrum pruning')
        if sp.missing_low:continue
        require([x['labelling'] for x in branch['cases']]==list(map(list,aa)),'omitted modular labelling')
        for lab,case in zip(aa,branch['cases']):
            eps=indicator_choices(R)
            require([x['indicators'] for x in case['indicators']]==list(map(list,eps)),'omitted indicator choice')
            for ep,rec in zip(eps,case['indicators']):
                A,b,meta=equation_system(R,data,tab,cols,ep,c['height'],lab,sp)
                require(rec['system']==meta,'incorrect modular equation counts')
                check_farkas(A,b,rec['y'])
                require(rec['bTy']==sum(x*z for x,z in zip(b,rec['y'])),'incorrect exact separating value')
