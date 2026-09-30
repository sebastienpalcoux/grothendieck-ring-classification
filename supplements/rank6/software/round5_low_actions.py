"""Exact necessary regular actions from simultaneous low-word coefficients."""
import itertools,math
from fractions import Fraction
import sympy as s
from exact import require
from round4_quartic_profiles import enumerate_affine


def low_action_system(R,W,star,words,U,a,known_actions=(),trace=None):
    """Row convention: M[j,k]=[A_a X_j:X_k]; U[word] lists coefficients."""
    r=len(W);n=len(R);wi={tuple(w):j for j,w in enumerate(words)};fixed={};keys={};bounds=[]
    def key(j,k):
        pairs=[tuple(sorted((j,star[k])))]
        if star[a]==a:pairs.append(tuple(sorted((star[j],k))))
        return min(pairs)
    def fix(j,k,v):
        q=key(j,k)
        if q in fixed:require(fixed[q]==v,'inconsistent fixed action')
        fixed[q]=v
    for b in range(n):
        vals=[int(k==a) for k in range(r)] if b==0 else U[wi[tuple(sorted((a,b)))]]
        for k,v in enumerate(vals):fix(b,k,v)
    for j in range(n,r):
        prod=[sum(W[a][u]*W[j][v]*R[u][v][h] for u in range(n) for v in range(n)) for h in range(n)]
        for k in range(n,r):
            q=key(j,k)
            if q in fixed:continue
            bd=min(prod[h]//W[k][h] for h in range(n) if W[k][h])
            if q in keys:bounds[keys[q]]=min(bounds[keys[q]],bd)
            else:keys[q]=len(keys);bounds.append(bd)
    rows=[];rhs=[]
    def add(terms,b):
        row={}
        for q,v in terms:
            if q in fixed:b-=v*fixed[q]
            elif v:row[keys[q]]=row.get(keys[q],0)+v
        row={j:v for j,v in row.items() if v}
        if row or b:rows.append(row);rhs.append(b)
    inv=[i for i in range(n) if sum(R[i][next(j for j in range(n) if R[i][j][0])])==1]
    for j in range(r):
        if sum(W[j])==1 and W[j].index(1) in inv:add([(key(j,k),1) for k in range(r)],1)
        prod=[sum(W[a][u]*W[j][v]*R[u][v][h] for u in range(n) for v in range(n)) for h in range(n)]
        for h in range(n):add([(key(j,k),W[k][h]) for k in range(r)],prod[h])
    for word in words:
        nextword=tuple(sorted([a]+list(word)))
        if nextword not in wi:continue
        u=U[wi[tuple(word)]];v=U[wi[nextword]]
        for k in range(r):add([(key(j,k),u[j]) for j in range(r)],v[k])
    if trace is not None:add([(key(j,j),1) for j in range(r)],trace)
    for M in known_actions:
        for j in range(r):
            for k in range(r):add([(key(j,l),M[l][k]) for l in range(r) if M[l][k]]+[(key(l,k),-M[j][l]) for l in range(r) if M[j][l]],0)
    return dict(fixed=[[list(k),v] for k,v in fixed.items()],keys=[list(k) for k in keys],bounds=bounds,rows=[list(map(list,row.items())) for row in rows],rhs=rhs,star=star,a=a)


def positive_presolve(system):
    """Propagate exact intervals; add all coordinates fixed by these bounds."""
    rows=[dict(row) for row in system['rows']];rhs=system['rhs'][:];lo=[0]*len(system['bounds']);hi=system['bounds'][:];changed=True;feasible=True
    while changed and feasible:
        changed=False
        for row,b in zip(rows,rhs):
            if any(v<0 for v in row.values()):continue
            mn=sum(lo[j]*v for j,v in row.items());mx=sum(hi[j]*v for j,v in row.items())
            if not mn<=b<=mx:feasible=False;break
            for j,v in row.items():
                l=max(lo[j],-(-(b-mx+hi[j]*v)//v));h=min(hi[j],(b-mn+lo[j]*v)//v)
                if l>h:feasible=False;break
                if l!=lo[j] or h!=hi[j]:changed=True;lo[j]=l;hi[j]=h
    if feasible:
        for j,(l,h) in enumerate(zip(lo,hi)):
            if l==h:rows.append({j:1});rhs.append(l)
    else:rows.append({});rhs.append(1)
    return rows,rhs,hi


def enumerate_actions(system,node_limit=5000000,expected_charpoly=None):
    rows,rhs,bounds=positive_presolve(system);order=sorted(range(len(bounds)),key=lambda j:-bounds[j]);A=[[row.get(j,0) for j in order] for row in rows];vals,stats=enumerate_affine(A,rhs,[bounds[j] for j in order],node_limit);fixed={tuple(k):v for k,v in system['fixed']};keys={tuple(k):j for j,k in enumerate(system['keys'])};star=system['star'];r=len(star);a=system['a'];matrices=[];rejected=[]
    def key(j,k):
        pairs=[tuple(sorted((j,star[k])))]
        if star[a]==a:pairs.append(tuple(sorted((star[j],k))))
        return min(pairs)
    expected_moments=None
    if expected_charpoly is not None:
        # Fast exact quadratic and cubic power traces before characteristic polynomials.
        p=s.Poly.from_list(expected_charpoly,s.Symbol('t'));expected_moments=[]
        # Newton sums recursively, retaining all arithmetic over ZZ.
        co=list(map(int,expected_charpoly));pw=[r]
        for k in range(1,4):pw.append(-sum(co[j]*pw[k-j] for j in range(1,k))-k*co[k])
        expected_moments=pw[1:]
    for si,v in enumerate(vals):
        vv={j:x for j,x in zip(order,v)};M=[[fixed[q] if (q:=key(j,k)) in fixed else vv[keys[q]] for k in range(r)] for j in range(r)]
        if expected_moments is not None:
            tr1=sum(M[j][j] for j in range(r));tr2=sum(M[j][k]*M[k][j] for j in range(r) for k in range(r));tr3=sum(M[i][j]*M[j][k]*M[k][i] for i in range(r) for j in range(r) for k in range(r)) if tr2==expected_moments[1] else None
            if [tr1,tr2,tr3]!=expected_moments:rejected.append([si,tr1,tr2,tr3]);continue
            if list(map(int,s.Matrix(M).charpoly().all_coeffs()))!=expected_charpoly:rejected.append([si,'characteristic_polynomial']);continue
        matrices.append(M)
    return dict(enumeration=stats,affine_solutions=len(vals),spectral_rejections=rejected,matrices=matrices)


def spectral_polynomial(C,eigenvalues):
    co=[C.one]
    for x in eigenvalues:
        out=[C.zero]*(len(co)+1)
        for i,v in enumerate(co):out[i]+=v;out[i+1]-=v*x
        co=out
    out=[]
    for v in co:
        q=v.to_list();require(len(q)<=1 and (not q or q[0].denominator==1),'noninteger regular characteristic polynomial');out.append(int(q[0]) if q else 0)
    return out


def general_action_system(R,W,star,a,known):
    """One further regular action, with every already known action imposed."""
    r=len(W);n=len(R);fixed={};keys={};bounds=[]
    def key(j,k):
        pairs=[tuple(sorted((j,star[k])))]
        if star[a]==a:pairs.append(tuple(sorted((star[j],k))))
        return min(pairs)
    def fix(j,k,v):
        q=key(j,k)
        if q in fixed:require(fixed[q]==v,'inconsistent fixed action')
        fixed[q]=v
    for k in range(r):fix(0,k,int(k==a))
    for b,M in known.items():
        for k,v in enumerate(M[a]):fix(b,k,v)
    for j in range(r):
        prod=[sum(W[a][u]*W[j][v]*R[u][v][h] for u in range(n) for v in range(n)) for h in range(n)]
        for k in range(r):
            q=key(j,k)
            if q in fixed:continue
            bd=min(prod[h]//W[k][h] for h in range(n) if W[k][h])
            if q in keys:bounds[keys[q]]=min(bounds[keys[q]],bd)
            else:keys[q]=len(keys);bounds.append(bd)
    rows=[];rhs=[]
    def add(terms,b):
        row={}
        for q,v in terms:
            if q in fixed:b-=v*fixed[q]
            elif v:row[keys[q]]=row.get(keys[q],0)+v
        row={j:v for j,v in row.items() if v}
        if row or b:rows.append(row);rhs.append(b)
    inv=[i for i in range(n) if sum(R[i][next(j for j in range(n) if R[i][j][0])])==1]
    for j in range(r):
        if sum(W[j])==1 and W[j].index(1) in inv:add([(key(j,k),1) for k in range(r)],1)
        prod=[sum(W[a][u]*W[j][v]*R[u][v][h] for u in range(n) for v in range(n)) for h in range(n)]
        for h in range(n):add([(key(j,k),W[k][h]) for k in range(r)],prod[h])
    for M in known.values():
        for j in range(r):
            for k in range(r):add([(key(j,l),M[l][k]) for l in range(r) if M[l][k]]+[(key(l,k),-M[j][l]) for l in range(r) if M[j][l]],0)
    return dict(fixed=[[list(k),v] for k,v in fixed.items()],keys=[list(k) for k in keys],bounds=bounds,rows=[list(map(list,row.items())) for row in rows],rhs=rhs,star=star,a=a)
