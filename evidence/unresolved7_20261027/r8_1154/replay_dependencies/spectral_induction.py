"""Exact joint-spectrum integrality and Galois multiplicity constraints.

This module strengthens the character-induction relaxation. It uses no ring
identifiers. Discovery is numerical only to propose exact Farkas witnesses.
"""
from character_induction import *
from tensor_rotation import system_rotation
from fractions import Fraction as Q
from collections import Counter
from functools import lru_cache

class Spectrum:
    def __init__(self,table,cols,high):
        self.table=table;K=table.K
        self.low=list(map(tuple,cols));self.high=[(0,)+tuple(v) for v,z in high]
        self.vectors=self.low+self.high
        self.types=[]
        for v in self.vectors:
            table.prepare(v)
            self.types.append(tuple((table.D/f)*table.values[h,v]/table.dims[v] for h,f in enumerate(table.codegrees)))
        self._integer={}
        bad=set()
        for typ in set(self.types):
            if not all(self.integral(x) for x in typ):bad.add(typ)
        self.roots=table.automorphisms();alltypes=set(self.types)
        self.conjugates={t:tuple(tuple(evaluate(x.to_list(),r,K) for x in t) for r in self.roots) for t in alltypes}
        for typ in alltypes:
            if any(y not in alltypes for y in self.conjugates[typ]):bad.add(typ)
        # Remove whole Galois orbits when a member violates a necessary condition.
        while True:
            new={t for t in alltypes-bad if any(x in bad for x in self.conjugates[t])}
            if not new:break
            bad|=new
        self.forbidden=[list(v[1:]) for v,t in zip(self.high,self.types[len(cols):]) if t in bad]
        self.missing_low=[j for j,t in enumerate(self.types[:len(cols)]) if t in bad]
        self.bad=bad
    def integral(self,x):
        if x in self._integer:return self._integer[x]
        K=self.table.K;n=K.mod.degree();z=K([1,0]);powers=[K.one]
        for i in range(1,n):powers.append(powers[-1]*z)
        columns=[]
        for u in powers:
            co=(x*u).to_list();co=[K.dom.zero]*(n-len(co))+co
            columns.append(list(reversed(co)))
        M=s.Matrix.hstack(*[s.Matrix(c) for c in columns]);p=M.charpoly().as_poly()
        value=all(s.denom(a)==1 for a in p.all_coeffs());self._integer[x]=value;return value
    def metadata(self):
        return {'high_columns':len(self.high),'forbidden':self.forbidden,'missing_low':self.missing_low,
                'joint_types':len(set(self.types)),'forbidden_types':len(self.bad)}
    def balance(self,labs,nvars,trace_one=None):
        """Galois multiplicities, optionally separately for each trace type.

        For the canonical modular data of a center theta_{sigma(Z)}=sigma^2(theta_Z).
        Every square fixes a quadratic trace field, so the normalized relative
        twist-trace type is preserved. Low objects all have twist one.
        """
        idx={v:t for v,t in zip(self.vectors,self.types)};lows=Counter(self.types[:len(self.low)])
        alltypes=sorted(set(self.types),key=str);seen=set();rows=[];rhs=[]
        tis=[None] if trace_one is None else sorted(set(ti for v,ti in labs)|{trace_one})
        for t in alltypes:
            if t in seen or t in self.bad:continue
            orbit=set(self.conjugates[t]);seen|=orbit
            for w in sorted(orbit-{t},key=str):
                for ti in tis:
                    row=[(int(idx[(0,)+tuple(v)]==t)-int(idx[(0,)+tuple(v)]==w))*int(ti is None or ti==tj) for v,tj in labs]
                    row += [0]*(nvars-len(row));value=(lows[w]-lows[t])*int(ti is None or ti==trace_one)
                    if any(row) or value:rows.append(row);rhs.append(value)
        return rows,rhs

def build_system(R,data,table,cols,ep,height,spec):
    L=s.Matrix.hstack(*map(s.Matrix,cols));A,b,meta=system_rotation(R,data,L,ep,height)
    from higher_traces import trace_types
    types,_=trace_types(data['q'],data['primes'],height)
    one=types.index(tuple((Q(1),Q(0)) for _ in range(height)))
    rows,rhs=spec.balance(meta['labels'],len(A[0]),one);A+=rows;b+=rhs
    forbidden=set(map(tuple,spec.forbidden));labs=meta['labels']
    keep=[j for j in range(len(A[0])) if j>=len(labs) or tuple(labs[j][0]) not in forbidden]
    return [[row[j] for j in keep] for row in A],b,{'balance_rows':len(rows),'columns_kept':len(keep)}

def certificate(R,height=6,progress=None):
    try:data,tab=reciprocity_data(R)
    except Ineligible:return None
    branches=[]
    for ix,cols in enumerate(data['lows']):
        branch={'columns':list(map(list,cols))}
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:branch['ordinary']=why
        else:
            aa=tab.assignments(cols);branch['labellings']=list(map(list,aa))
            if aa:
                L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=Spectrum(tab,cols,high);branch['spectrum']=sp.metadata()
                if not sp.missing_low:
                    cases=[]
                    for ep in indicator_choices(R):
                        if progress:progress(ix,list(ep),sp.metadata())
                        A,b,meta=build_system(R,data,tab,cols,ep,height,sp);y=farkas(A,b)
                        if y is None:return None
                        cases.append({'indicators':list(ep),'y':y,'bTy':sum(x*z for x,z in zip(b,y))})
                    branch['rotation']=cases
        branches.append(branch)
    return {'kind':'galois_twist_induction','height':height,'q':data['q'],'table':tab.metadata(),
            'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify(R,c):
    data,tab=reciprocity_data(R);require(c['kind']=='galois_twist_induction','wrong spectrum certificate')
    require(c['q']==data['q'] and c['table']==tab.metadata(),'wrong spectral character data')
    require(c['column_counts']==list(map(len,data['columns'])),'wrong low-column counts')
    require(len(c['branches'])==len(data['lows']),'missing low branches')
    for cols,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==list(map(list,cols)),'wrong low branch')
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'wrong ordinary obstruction');continue
        aa=tab.assignments(cols);require(branch['labellings']==list(map(list,aa)),'wrong or omitted character assignments')
        if not aa:continue
        L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);sp=Spectrum(tab,cols,high)
        require(branch['spectrum']==sp.metadata(),'wrong spectral exclusion data')
        if sp.missing_low:continue
        cases=branch['rotation'];eps=indicator_choices(R)
        require([x['indicators'] for x in cases]==list(map(list,eps)),'missing indicators')
        for ep,case in zip(eps,cases):
            A,b,meta=build_system(R,data,tab,cols,ep,c['height'],sp);check_farkas(A,b,case['y'])
            require(case['bTy']==sum(x*z for x,z in zip(b,case['y'])),'wrong exact Farkas value')
