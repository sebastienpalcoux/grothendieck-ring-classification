"""Complex low-Verlinde and restriction-product necessary equations.

This extension admits non-self-dual input rings and determines the duality
of low central objects from conjugation of their complete characters.
"""
import itertools, json, math, time
import round3_m4 as M
from exact import evaluate, require
from modular_character_induction import rational_rows
from spectral_induction import Spectrum


def system(R,data,cols,ep,lab,quartic=False,quartic_cutoff=None):
    A,b,meta=M.system(R,data,cols,ep,lab)
    if A is None:return A,b,meta
    C=data['C'];n=len(R);tab=data['tab'];G,vs,sp=data['_branch_cache'][tuple(map(tuple,cols))]
    forbidden=set(map(tuple,sp.forbidden));vs=[v for v in vs if v not in forbidden]
    labels=[(v,ti) for v in vs for ti in range(len(data['phases']))]
    nv=len(A[0]);nh=len(labels);tuples=dict(zip(sp.vectors,sp.types));triple={};base=nv
    lowstar=[]
    for a in range(n):
        row=tab.rows[lab[a]];crow=tuple(evaluate(x.to_list(),C.unit**(data['F']-1),C) for x in row)
        lowstar.append(lab.index(tab.rows.index(crow)))
    require(lowstar[0]==0 and all(lowstar[lowstar[i]]==i for i in range(n)), 'invalid central low duality')
    for a in range(n):
        require(tuple(cols[lowstar[a]])==tuple(cols[a][data['ch'].du[i]] for i in range(n)), 'low dual restriction mismatch')
    for a,bb,c in itertools.combinations_with_replacement(range(1,n),3):
        ha,hb,hc=[lab[x] for x in (a,bb,c)]
        weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)}
        rhs=-sum((weights[v] for v in sp.low),C.zero)
        co=[weights[(0,)+tuple(v)] for v,ti in labels]+[C.zero]*(nv-nh)+[-C.one]
        for row in A:row.append(0)
        triple[(a,bb,c)]=nv;nv+=1
        for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
    allowed=[v for v in sp.high if list(v[1:]) not in sp.forbidden]
    product_variables={}
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ca,cb=cols[a],cols[bb];fp=[sum(ca[i]*cb[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
        qvars={}
        for v in allowed:
            bound=min(fp[k]//v[k] for k in range(n) if v[k])
            if bound:qvars[v]=(nv,bound);nv+=1
        product_variables[a,bb]=qvars
        for row in A:row.extend([0]*(nv-len(row)))
        for k in range(n):
            row=[0]*nv
            for c in range(1,n):row[triple[tuple(sorted((a,bb,lowstar[c])))]]+=cols[c][k]
            for v,(j,B) in qvars.items():row[j]=v[k]
            A.append(row);b.append(fp[k]-int(a==lowstar[bb] and k==0))
        for v,(j,B) in qvars.items():
            row=[0]*(nv+1);row[j]=1;row[nv]=1
            for k,(w,ti) in enumerate(labels):
                if tuple(w)==v[1:]:row[k]-=B
            for rr in A:rr.append(0)
            A.append(row);b.append(0);nv+=1
    if quartic:
        for a,bb in itertools.combinations_with_replacement(range(1,n),2):
            ha,hb,hsa,hsb=[lab[x] for x in (a,bb,lowstar[a],lowstar[bb])]
            weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hsa]*tuples[v][hsb]*tab.dims[v]**2/tab.D**2 for v in set(sp.vectors)}
            rhs=-sum((weights[v] for v in sp.low),C.zero)+C(int(a==lowstar[bb]))
            qvars=product_variables[a,bb]; terms=[]
            fp=[sum(cols[a][i]*cols[bb][j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
            for c in range(1,n):
                B=min(fp[k]//cols[c][k] for k in range(n) if cols[c][k])
                terms.append((triple[tuple(sorted((a,bb,lowstar[c])))],B,None))
            terms.extend((j,B,v) for v,(j,B) in qvars.items())
            zvars=[]
            for j,B,v in terms:
                z=nv;nv+=1;zvars.append(z)
                for row in A:row.append(0)
                # For integer n, n^2 >= (2k+1)n-k(k+1); sum over
                # central simples of each restriction type v.
                for k in range(B if quartic_cutoff is None else min(B,quartic_cutoff)):
                    row=[0]*(nv+1);row[z]=1;row[j]-=2*k+1;row[nv]=-1
                    if v is None: rr=-k*(k+1)
                    else:
                        rr=0
                        for jj,(w,ti) in enumerate(labels):
                            if tuple(w)==v[1:]:row[jj]+=k*(k+1)
                    for rr0 in A:rr0.append(0)
                    A.append(row);b.append(rr);nv+=1
                row=[0]*(nv+1);row[z]=-1;row[j]+=B;row[nv]=-1
                for rr0 in A:rr0.append(0)
                A.append(row);b.append(0);nv+=1
            co=[weights[(0,)+tuple(v)] for v,ti in labels]+[C.zero]*(nv-nh)
            for z in zvars:co[z]=-C.one
            for row,val in rational_rows(co,rhs,C):A.append(row);b.append(val)
    meta.update({'lowstar' :lowstar,'integrality':[1]*nv,'labels':labels,'base':base,'rows':len(A),'variables':nv})
    return A,b,meta

def central_invertible_system(R,data,cols,ep,lab,Kpoint,quartic=False,quartic_cutoff=None):
    """Necessary action of lifts of based-ring involutions, trivial kernel.

    The low frame must have exactly one restriction column equal to the unit.
    Central invertibles then map injectively to based-ring invertibles. A lift
    with indicator -1 has twist +/-i and acts freely on central simples; its
    twist ratio is +/-i. Matching counts encode the resulting involution.
    """
    A,b,meta=system(R,data,cols,ep,lab,quartic=quartic,quartic_cutoff=quartic_cutoff)
    if A is None:return A,b,meta
    n=len(R);unit=tuple([1]+[0]*(n-1));require(sum(tuple(c)==unit for c in cols)==1,'nontrivial kernel of central invertibles')
    invs=[i for i in range(n) if sum(R[i][data['ch'].du[i]])==1]
    require(0 in Kpoint and set(Kpoint)<=set(invs),'bad pointed subgroup')
    require(all(next(k for k,z in enumerate(R[i][j]) if z) in Kpoint for i in Kpoint for j in Kpoint),'pointed subset not closed')
    labels=meta['labels'];C=data['C'];F=data['F'];phases=data['phases'];nv=len(A[0]);one=phases.index(tuple(C.one for _ in range(data['height'])));low={}
    for c in cols:low[(tuple(c),one)]=low.get((tuple(c),one),0)+1
    allpairs=set(low)|{((0,)+tuple(v),ti) for v,ti in labels};pos={((0,)+tuple(v),ti):j for j,(v,ti) in enumerate(labels)}
    for g in invs[1:]:
        row=[0]*nv
        for j,(v,ti) in enumerate(labels):
            if tuple((0,)+tuple(v))==tuple(int(i==g) for i in range(n)):row[j]=1
        A.append(row);b.append(int(g in Kpoint))
    for g in Kpoint:
        if g==0:continue
        require(data['ch'].du[g]==g,'only involutive central lifts supported')
        def action(v):return tuple(sum(v[i]*R[g][i][k] for i in range(n)) for k in range(n))
        if ep[g-1]==-1:
            require(F%4==0,'semion transport requires i in ambient field')
            ii=C.unit**(F//4);perms=[]
            for z in (ii,-ii):perms.append({t:phases.index(tuple(z**k*x for k,x in enumerate(tt,1))) for t,tt in enumerate(phases)})
            edges=set()
            for v,t in allpairs:
                for pm in perms:
                    w=(action(v),pm[t]);u=(v,t)
                    if w in allpairs:edges.add(tuple(sorted((u,w),key=str)))
            edges=sorted(edges,key=str);starts=nv;nv+=len(edges)
            for row in A:row.extend([0]*(nv-len(row)))
            for u in sorted(allpairs,key=str):
                row=[0]*nv
                if u in pos:row[pos[u]]=-1
                for j,e in enumerate(edges):row[starts+j]=int(e[0]==u)+int(e[1]==u)
                A.append(row);b.append(low.get(u,0))
        else:
            vs={v for v,t in allpairs}
            for v in sorted(vs):
                w=action(v);row=[0]*nv
                for j,(vv,ti) in enumerate(labels):row[j]=int((0,)+tuple(vv)==v)-int((0,)+tuple(vv)==w)
                value=sum(k for (vv,t),k in low.items() if vv==w)-sum(k for (vv,t),k in low.items() if vv==v)
                if any(row) or value:A.append(row);b.append(value)
    meta.update({'pointed_subgroup':list(Kpoint),'integrality':[1]*nv,'rows':len(A),'variables':nv})
    return A,b,meta

def primal_system(R,c):
    """Reconstruct one necessary system; this certifies survival only."""
    require(c.get('kind')=='complex_center_primal' and c.get('version')==1,'wrong primal certificate kind')
    data=M.data_for(R,c['height'],c['F'])
    require(0<=c['low']<len(data['lows']),'invalid low frame index')
    cols=data['lows'][c['low']]
    require(list(map(list,cols))==c['low_columns'],'wrong low frame')
    lab=tuple(c['labelling']);ep=tuple(c['indicators'])
    require(lab in data['tab'].assignments(cols),'invalid low labelling')
    require(ep in M.indicator_choices(R),'invalid second indicators')
    if 'pointed_subgroup' in c:A,b,meta=central_invertible_system(R,data,cols,ep,lab,c['pointed_subgroup'],quartic=c.get('quartic',False),quartic_cutoff=c.get('quartic_cutoff'))
    else:A,b,meta=system(R,data,cols,ep,lab,quartic=c.get('quartic',False),quartic_cutoff=c.get('quartic_cutoff'))
    require(A is not None,'primal branch already spectrally excluded')
    return A,b,meta


def verify_primal_coordinates(R,c,A,b,meta):
    """Check a proposed integer point after exact system reconstruction."""
    from fractions import Fraction
    require(c['rows']==len(A) and c['variables']==len(A[0]),'wrong system dimensions')
    x=list(map(Fraction,c['values']))
    require(len(x)==len(A[0]) and all(t>=0 for t in x),'wrong length or negative primal coordinate')
    require(all(t.denominator==1 for t in x),'nonintegral primal coordinate')
    x=list(map(int,x))
    require(all(sum(a*t for a,t in zip(row,x) if a and t)==rhs for row,rhs in zip(A,b)),'primal equality failed')
    rank=len(R)+sum(x[:len(meta['labels'])])
    require(str(rank)==c['center_rank'],'wrong conditional center rank')
    return {'passed':True,'equations':len(A),'variables':len(x),'all_coordinates_integral':True,'center_rank':int(rank),'optimizer_used':False,'scope':'necessary_system_survival_only'}


def verify_primal(R,c):
    A,b,meta=primal_system(R,c)
    return verify_primal_coordinates(R,c,A,b,meta)


def frozen_control_tasks(root):
    """Stable 10+54 control domain, independent of later ledger allocations."""
    from pathlib import Path
    root=Path(root)
    tensors={r['id']:r['N'] for r in json.loads((root/'data/census.json').read_text())}
    positives=json.loads((root/'data/model_catalog.json').read_text())
    frontier=json.loads((root/'verification/round4/campaign_manifest.json').read_text())['ids']
    status={r['id']:r['status'] for r in positives}
    require(len(status)==54 and len(frontier)==10 and not set(status)&set(frontier),'wrong frozen control domain')
    status.update({rid:'unresolved' for rid in frontier})
    return [(rid,tensors[rid],status[rid]) for rid in sorted(status,key=lambda r:tuple(map(int,r.split('_')[1:]))) ]
