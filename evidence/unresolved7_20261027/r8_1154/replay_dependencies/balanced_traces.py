"""Finite twist traces with exact duality and quadratic Galois count balance."""
from higher_traces import *
from collections import Counter

def positive_pair(z,q):
    a,b=z
    if not b:return a>0
    if a>=0 and b>=0:return True
    if a<=0 and b<=0:return False
    return a*a>q*b*b if a>0 else q*b*b>a*a

def system(R,data,L,ep,height):
    A,b,meta=build_system(R,data,L,ep,height);labs=meta['labels'];nvars=len(A[0]);du=dual(R);q=data['q'];D=data['global_dimension'];d=data['dimensions'];new=[];rhs=[]
    # Duality acts on restrictions and preserves the ribbon twist.
    present=set((tuple(v),ti) for v,ti in labs);seen=set()
    for v,ti in sorted(present):
        w=tuple(v[du[i]-1] for i in range(1,len(R)))
        pair=tuple(sorted((v,w)))
        if v==w or (pair,ti) in seen:continue
        seen.add((pair,ti));row=[0]*nvars
        for j,(u,tj) in enumerate(labs):
            if tj==ti:row[j]=int(tuple(u)==v)-int(tuple(u)==w)
        new.append(row);rhs.append(0)
    n_dual=len(new)
    # Galois symmetry of the normalized S matrix of the center.
    if q>1:
        norm=D[0]**2-q*D[1]**2
        ratio=((D[0]**2+q*D[1]**2)/norm,2*D[0]*D[1]/norm)
        def hat(z):
            y=mul(ratio,(z[0],-z[1]),q)
            return y if positive_pair(y,q) else (-y[0],-y[1])
        def dim(v):return tuple(sum((Q(v[i])*d[i][k] for i in range(len(R))),Q(0)) for k in range(2))
        low=Counter(dim(list(L[:,j])) for j in range(L.cols));hd=[dim([0]+v) for v,ti in labs]
        allvals=set(low)|set(hd);allvals|={hat(z) for z in allvals};seen=set()
        for z in sorted(allvals):
            w=hat(z);require(hat(w)==z,'Galois dimension involution failed')
            pair=tuple(sorted((z,w)))
            if z==w or pair in seen:continue
            seen.add(pair);row=[int(v==z)-int(v==w) for v in hd]+[0]*(nvars-len(hd));new.append(row);rhs.append(low[w]-low[z])
    A+=new;b+=rhs
    meta.update(balance_rows=len(new),duality_rows=n_dual,galois_rows=len(new)-n_dual)
    return A,b,meta

def certificate(R,height=6):
    data=quadratic_data(R,gram_prune=True)
    if data is None:return None
    branches=[]
    for cols in data['lows']:
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du);branch={'columns':[list(c) for c in cols]}
        if why:branch['ordinary']=why
        else:
            L=s.Matrix.hstack(*map(s.Matrix,cols));cases=[]
            for ep in indicator_choices(R):
                A,b,meta=system(R,data,L,ep,height);y=farkas(A,b)
                if y is None:return None
                cases.append({'indicators':list(ep),'y':y,'balance_rows':meta['balance_rows'],'bTy':sum(x*z for x,z in zip(b,y))})
            branch['higher']=cases
        branches.append(branch)
    return {'kind':'balanced_indicator_traces','height':height,'q':data['q'],'column_counts':list(map(len,data['columns'])),'branches':branches}

def verify(R,c):
    data=quadratic_data(R,gram_prune=True);require(data is not None,'ineligible balanced trace ring');require(c['kind']=='balanced_indicator_traces' and c['q']==data['q'],'bad balanced certificate')
    require(c['column_counts']==list(map(len,data['columns'])),'incomplete balanced low columns');require(len(c['branches'])==len(data['lows']),'missing balanced low branches')
    for cols,branch in zip(data['lows'],c['branches']):
        require(branch['columns']==[list(v) for v in cols],'wrong balanced low branch');why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du)
        if why:require(branch.get('ordinary')==why,'bad balanced ordinary obstruction');continue
        eps=indicator_choices(R);require([case['indicators'] for case in branch['higher']]==list(map(list,eps)),'missing balanced indicators');L=s.Matrix.hstack(*map(s.Matrix,cols))
        for ep,case in zip(eps,branch['higher']):
            A,b,meta=system(R,data,L,ep,c['height']);check_farkas(A,b,case['y']);require(case['balance_rows']==meta['balance_rows'],'wrong balance rows');require(case['bTy']==sum(x*z for x,z in zip(b,case['y'])),'wrong balanced separating value')
