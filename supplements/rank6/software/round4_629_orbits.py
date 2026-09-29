"""Odd principal-unit Galois orbit bounds for center restriction columns.

Research: this module only constructs and exactly tests necessary linear rows.
No categorification claim follows from solver success or failure alone.
"""
import math,itertools,json,time
import sympy as s
from exact import require
import round3_m4 as ambient
from spectral_induction import Spectrum
from character_induction import Ineligible

def orbit_domain(data,bound):
    F=data['F'];ps=data['primes'];C=data['C'];h=data['height']
    if F%2==0 or 2 in ps or any(F%p for p in ps):raise Ineligible('odd principal-unit cyclotomic domain required')
    if set(map(int,s.factorint(F)))!=set(ps):raise Ineligible('conductor and dimension prime supports must coincide')
    c={p:int(s.factorint(F)[p]) for p in ps};upper={}
    for p in ps:
        a=0
        while p**(a+1)<=bound:a+=1
        upper[p]=c[p]+a
    found={}
    for es in itertools.product(*(range(upper[p]+1) for p in ps)):
        order=math.prod(p**a for p,a in zip(ps,es));degree=math.prod(p**max(0,a-c[p]) for p,a in zip(ps,es))
        if degree>bound:continue
        for a in range(order):
            if math.gcd(a,order)>1:continue
            typ=tuple(ambient.relative_root(C,F,order,a*j) for j in range(1,h+1))
            require(typ in data['phases'],'orbit trace outside complete ambient domain')
            ti=data['phases'].index(typ)
            found.setdefault(ti,set()).add(degree)
    # A multiple orbit size contributes no new count to the additive semigroup.
    return {ti:sorted(e for e in sizes if not any(e%d==0 for d in sizes if d<e)) for ti,sizes in sorted(found.items())}

def refine(R,data,cols,lab,ep,with_verlinde=False):
    A,b,meta=ambient.system(R,data,cols,ep,lab)
    if A is None:return A,b,meta
    tab=data['tab'];G,vs=ambient.high_vectors(data,cols);sp=Spectrum(tab,cols,[(v,None) for v in vs]);bad=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in bad]
    labels=[(v,ti) for v in vs for ti in range(len(data['phases']))]
    if with_verlinde:
        from pathlib import Path
        import sys
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'research/round3/quartic'))
        from verlinde_probe import verlinde
        A,b,labels,base=verlinde(R,data,tab,cols,lab,A,b,labels)
    bounds={v:min(int(G[i,i])//(v[i]*v[i]) for i in range(len(v)) if v[i]) for v in vs}
    domains={B:orbit_domain(data,B) for B in sorted(set(bounds.values()))}
    columns=[];nold=len(A[0]);integrality=[];hist={}
    for j in range(nold):
        if j>=len(labels):columns.append((j,1));integrality.append(int(with_verlinde))
        else:
            v,ti=labels[j]
            for e in domains[bounds[v]].get(ti,[]):columns.append((j,e));integrality.append(1);hist[e]=hist.get(e,0)+1
    AA=[[row[j]*e for j,e in columns] for row in A]
    return AA,b,dict(parent=meta,old_variables=nold,variables=len(columns),high_variables=len(labels),orbit_sizes=hist,removed_high_variables=sum(not domains[bounds[v]].get(ti) for v,ti in labels),integrality=integrality,columns=columns)

def verify_witness(R,record):
    """Replay an exact surviving necessary-system witness, never a model."""
    from fractions import Fraction
    data=ambient.data_for(R,record['height'],15)
    br=record['branches'][-1]
    require(br.get('exact_primal') is True,'no exact primal witness')
    require(type(br['low']) is int and 0<=br['low']<len(data['lows']),'invalid low frame')
    cols=data['lows'][br['low']]
    require(tuple(br['lab']) in data['tab'].assignments(cols),'invalid low character labelling')
    require(tuple(br['ep']) in ambient.indicator_choices(R),'invalid indicator choice')
    A,b,meta=refine(R,data,cols,br['lab'],br['ep'],record['with_verlinde'])
    require(A is not None and json.loads(json.dumps(meta))==br['meta'],'incorrect finite system metadata')
    x=list(map(Fraction,br['primal']))
    require(len(x)==len(A[0]) and all(z>=0 for z in x),'invalid nonnegative primal vector')
    require(all(not ii or z.denominator==1 for z,ii in zip(x,meta['integrality'])),'nonintegral orbit count')
    den=math.lcm(*(z.denominator for z in x));support=[(j,int(z*den)) for j,z in enumerate(x) if z]
    require(all(sum(row[j]*z for j,z in support)==rhs*den for row,rhs in zip(A,b)),'exact primal equation failed')
    rank=len(cols)+sum(z*e for z,(j,e) in zip(x,meta['columns']) if j<meta['high_variables'])
    return {'passed':True,'claim':'feasibility of specified necessary system only; no categorification or modular data constructed','rows':len(A),'variables':len(x),'induction_rank':str(rank),'optimizer_used':False}
