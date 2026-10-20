"""Exact necessary low-block Verlinde coefficients, with LP/MILP discovery."""
import argparse
import itertools
import json
import math
import time
import hashlib
from fractions import Fraction as F

import explore as e
m=e.m;q=e.q;HERE=e.HERE


def coefficients(table,dom,use_cache=True):
    domain_sha=hashlib.sha256(json.dumps({'low':dom['low'],'orbits':dom['orbits']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
    target=HERE/(dom['id']+'_verlinde_'+str(dom['low_index'])+'_'+domain_sha[:12]+'.json')
    if use_cache and target.exists():
        return json.loads(target.read_text())
    K=table.K
    n=K.mod.degree()
    def vector(x):
        c=[F(str(t)) for t in x.to_list()];return [F(0)]*(n-len(c))+c
    one=vector(K.one);root=vector(K.from_sympy(m.s.sqrt(5)))
    a0,b0=next((i,j) for i in range(n) for j in range(i+1,n) if one[i]*root[j]!=one[j]*root[i])
    det=one[a0]*root[b0]-one[b0]*root[a0]
    def quadratic(value):
        v=vector(value)
        a=(v[a0]*root[b0]-v[b0]*root[a0])/det
        b=(one[a0]*v[b0]-one[b0]*v[a0])/det
        q.require(all(x==a*y+b*z for x,y,z in zip(v,one,root)),'whole dual orbit Verlinde value is real quadratic')
        return a,b
    triples=list(itertools.combinations_with_replacement([i for i in range(7) if i!=table.fp],3))
    groups=[[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']]]+[[((0,)+tuple(v)) for v,_,z in orbit] for orbit in dom['orbits']]
    values=[]
    for gi,group in enumerate(groups):
        for v in group:table.prepare(v)
        row=[]
        for E,F0,G in triples:
            factor=table.D/(table.codegrees[E]*table.codegrees[F0]*table.codegrees[G])
            value=factor*sum((table.values[E,v]*table.values[F0,v]*table.values[G,v]/table.dims[v] for v in group),K.zero)
            pair=quadratic(value)
            row.extend(str(x) for x in pair)
        values.append(row)
    result={'triples':triples,'known':values[0],'orbits':values[1:],'domain_sha256':domain_sha}
    if use_cache:target.write_text(json.dumps(result)+'\n')
    return result


def run(rid,export_only=False):
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    from scipy.sparse import csc_matrix
    from spectral_induction import Spectrum
    N=next(r['tensor'] for r in json.loads((q.ROOT/'supplements/rank7/output/m5/census.json').read_text()) if r['id']==rid)
    d,D,B,zs,T,signs=q.source_data(N,rid)
    table=m.ExactQuadraticCharacterTable(N,d,5)
    ds=e.domains(rid);results=[];pool=[]
    for dom in ds:
        if rid=='R7_5_5039' and dom['low_index']==1:continue
        dom['id']=rid
        V=coefficients(table,dom);known=list(map(F,V['known']));vcols=[list(map(F,c)) for c in V['orbits']]
        print(json.dumps({'event':'verlinde_ready','index':dom['low_index'],'triples':len(V['triples'])}),flush=True)
        orbits=dom['orbits']
        sp=Spectrum(table,[(1,0,0,0,0,0,0)]+[tuple(v) for v in dom['low']],[(v,z) for orbit in orbits for v,_,z in orbit])
        if sp.missing_low:continue
        forbidden=set(map(tuple,sp.forbidden))
        excluded={oi for oi,orb in enumerate(orbits) if any(tuple(v) in forbidden for v,_,z in orb)}
        muls=[]
        for oi,orb in enumerate(orbits):
            v=(0,)+tuple(orb[0][0]);tv=T(v)
            if all(x<=0 for x in tv):tv=tuple(-x for x in tv)
            dv=tuple(v[i] for i in T.dual)
            muls.extend([1]*4+[2 if tv==v or tv==dv else 1]*6)
        for ci,case in enumerate(dom['cases']):
            if -1 in case['sign']:continue
            delta=-1 if case['label'].index(5)<case['label'].index(6) else 1
            phase=4 if delta==-1 else 7
            i,j=(3,4) if rid=='R7_5_3895' else (2,3)
            selection=[k for k in range(len(dom['columns'])) if k//10 not in excluded and
                       (all(v[i]==v[j] for v,_,z in orbits[k//10]) or k%10==phase)]
            cols=[[muls[k]*F(x) for x in dom['columns'][k]]+[muls[k]*x for x in vcols[k//10]] for k in selection]
            rhs=list(map(F,case['rhs']))+[-x for x in known]
            old=len(case['rhs'])
            for ti in range(len(V['triples'])):
                c=[F(0)]*len(rhs);c[old+2*ti]=-1;cols.append(c)
            extra=0
            if rid=='R7_5_5039':
                for phase_set,limit in [({0,4,7},2),({1,5,8},2),({2,6,9},4)]:
                    for j,c in enumerate(cols):
                        weight=0
                        if j<len(selection) and selection[j]%10 in phase_set:
                            k=selection[j]
                            weight=muls[k]*sum((v[0]-v[1])**2 for v,_,z in orbits[k//10])
                        c.append(F(weight))
                    rhs.append(F(limit));c=[F(0)]*len(rhs);c[-1]=1;cols.append(c);extra+=1
            cols,rhs=m.integral_system(cols,rhs)
            if rid=='R7_5_5039':
                positive_rows=list(range(21))+list(range(len(rhs)-3,len(rhs)))
                keep=[j for j in range(len(selection)) if all(cols[j][r]<=rhs[r] for r in positive_rows)]
                removed=len(selection)-len(keep)
                cols=[cols[j] for j in keep]+cols[len(selection):]
                selection=[selection[j] for j in keep]
                print(json.dumps({'event':'integer_zero_pruning','index':dom['low_index'],'case':ci,'removed':removed,'remaining_phase_variables':len(selection)}),flush=True)
            if rid=='R7_5_3895':
                active=[j for j,k in enumerate(selection) if any(v[3]!=v[4] for v,_,z in orbits[k//10])]
                weights={j:sum((v[3]-v[4])**2 for v,_,z in orbits[selection[j]//10])*muls[selection[j]] for j in active}
                payload={'id':rid,'low_index':dom['low_index'],'case':ci,'source_sha256':q.tensor_hash(N),
                         'columns':cols,'rhs':rhs,'phase_selection':selection,'multipliers':muls,
                         'active_variables':active,'active_weights':weights,'active_budget':8}
                (HERE/(rid+'_system_'+str(dom['low_index'])+'_'+str(ci)+'.json')).write_text(json.dumps(payload)+'\n')
                if export_only:
                    print(json.dumps({'event':'system_export','index':dom['low_index'],'case':ci,'columns':len(cols),'active':len(active)}),flush=True)
                    continue
            sep=q.separate(cols,rhs,pool)
            if sep is not None:
                result={'index':dom['low_index'],'case':ci,'exact_separator':sep};results.append(result);print(json.dumps(result),flush=True);continue
            # A raw rank-deficient HNF is too expensive here; the finite active
            # orbit decomposition is checked separately with projected HNF.
            ub=[min(rhs[i]//c[i] for i in range(21) if c[i]>0) for c in cols[:len(selection)]]+[np.inf]*(len(V['triples'])+extra)
            start=time.monotonic()
            solved=milp(np.r_[np.ones(len(selection)),np.zeros(len(V['triples'])+extra)],integrality=np.ones(len(cols)),bounds=Bounds(np.zeros(len(cols)),ub),constraints=LinearConstraint(csc_matrix(np.array(cols,dtype=float).T),rhs,rhs),options={'time_limit':60})
            result={'index':dom['low_index'],'case':ci,'status':int(solved.status),'message':solved.message,'seconds':time.monotonic()-start}
            if solved.x is not None:
                x=[round(float(v)) for v in solved.x]
                result['exact_feasible']=all(sum(c[i]*v for c,v in zip(cols,x))==b for i,b in enumerate(rhs))
                result['actual_support']=[(selection[i],v*muls[selection[i]]) for i,v in enumerate(x[:len(selection)]) if v]
                result['verlinde_coefficients']=x[len(selection):len(selection)+len(V['triples'])]
                result['conductor_eight_phase_budget']=(rid=='R7_5_5039')
            results.append(result);print(json.dumps(result),flush=True)
            (HERE/(rid+'_verlinde_discovery.json')).write_text(json.dumps({'results':results,'separators':pool},indent=2)+'\n')
    (HERE/(rid+'_verlinde_discovery.json')).write_text(json.dumps({'results':results,'separators':pool},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('ring',choices=q.CONFIG);p.add_argument('--export',action='store_true');a=p.parse_args();run(a.ring,a.export)
