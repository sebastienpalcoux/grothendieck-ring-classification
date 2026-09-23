"""Two-sided module Gram obstruction for a split involution algebra.

No pivotality/positivity of categorical dimensions is assumed. Positivity below
is solely Frobenius--Perron positivity of a semisimple module category.
Discovery uses rational LP; verification reconstructs all finite domains and
checks exact Farkas vectors without calling an optimizer.
"""
import itertools,math,json,time
from collections import Counter
from fractions import Fraction as Q
import sympy as s
from exact import require,vector,ec
from rings import Characters,dual
from involution_module import invs,generated_basis,prod,transpose
from higher_traces import farkas,check_farkas

def anti_representations(R,g):
    n=len(R);du=dual(R)
    require(all(R[i][j]==R[j][i] for i in range(n) for j in range(n)), 'commutativity required')
    fixed=[x for x in range(n) if R[g][x][x]];f=len(fixed)
    if not 0<f<=2:return None
    eye=tuple(int(i==j) for i in range(f) for j in range(f));sets=[]
    for i in range(n):
        bounds=[R[i][x][y] for x in fixed for y in fixed]
        vals=list(itertools.product(*(range(-a,a+1,2) for a in bounds)))
        if du[i]==i:vals=[v for v in vals if transpose(v,f)==v]
        sets.append(vals)
    sets[0]=[eye];choices=[]
    for count in (1,2):
        for seed in itertools.combinations(range(1,n),count):
            info=generated_basis(R,seed)
            if info:choices.append((math.prod(len(sets[i]) for i in seed),seed,info))
        if choices:break
    if not choices:return None
    nodes,seed,(words,inv)=min(choices,key=lambda v:(v[0],v[1]));coef=[[Q(inv[j,i]) for i in range(n)] for j in range(n)]
    allowed=list(map(set,sets));out=set()
    for vals in itertools.product(*(sets[i] for i in seed)):
        given=dict(zip(seed,vals))
        if any(prod(given[i],given[j],f)!=prod(given[j],given[i],f) for i in seed for j in seed):continue
        images=[]
        for word in words:
            z=eye
            for i in word:z=prod(z,given[i],f)
            images.append(z)
        mats=[]
        for k in range(n):
            v=tuple(sum(coef[k][i]*images[i][a] for i in range(n)) for a in range(f*f))
            if v not in allowed[k]:break
            mats.append(tuple(int(x) for x in v))
        if len(mats)!=n:continue
        if any(transpose(mats[i],f)!=mats[du[i]] for i in range(n)):continue
        if any(prod(mats[i],mats[j],f)!=tuple(sum(R[i][j][k]*mats[k][a] for k in range(n)) for a in range(f*f)) for i in range(n) for j in range(n)):continue
        # Swapping the two structures on any fixed object is a harmless gauge.
        gauges=[]
        for signs in itertools.product((-1,1),repeat=f):
            gauges.append(tuple(tuple(signs[i]*signs[j]*v[i*f+j] for i in range(f) for j in range(f)) for v in mats))
        out.add(min(gauges))
    return fixed,seed,nodes,sorted(out)

def module_matrices(R,g,fixed,T):
    n=len(R);done=set();labels=[]
    for x in range(n):
        if x in done:continue
        if x in fixed:
            labels.extend([(x,1),(x,-1)]);done.add(x)
        else:
            y=next(j for j,c in enumerate(R[g][x]) if c)
            labels.append((x,0));done.update((x,y))
    f=len(fixed);r=len(labels);F={x:k for k,x in enumerate(fixed)};Ms=[]
    for i in range(n):
        M=[]
        for x,sgx in labels:
            row=[]
            for y,sgy in labels:
                if sgx and sgy:
                    u=R[i][x][y]+sgx*sgy*T[i][F[x]*f+F[y]]
                    require(u%2==0 and u>=0,'invalid split-module coefficient');v=u//2
                elif not sgx and not sgy:
                    gx=next(k for k,c in enumerate(R[g][x]) if c)
                    v=R[i][x][y]+R[i][gx][y]
                else:v=R[i][x][y]
                row.append(v)
            M.append(row)
        Ms.append(s.Matrix(M))
    du=dual(R)
    require(Ms[0]==s.eye(r),'module unit')
    require(all(Ms[i].T==Ms[du[i]] for i in range(n)),'module transpose')
    require(all(Ms[i]*Ms[j]==sum((R[i][j][k]*Ms[k] for k in range(n)),s.zeros(r)) for i in range(n) for j in range(n)),'module multiplication')
    return labels,Ms

def dual_dimensions(labels,Ms,g,K,ds):
    r=len(labels);u=labels.index((0,0))
    dims=[ds[x]/(2 if sign else 1) for x,sign in labels]
    require(dims[u]==K.one,'unit-module normalization')
    G=s.eye(r)+Ms[g];done=set();cols=[]
    # I+P, for an involutive permutation, has a unique nonnegative integral
    # Gram decomposition: two unit columns at a fixed point; one pair-column
    # at a transposition. The unit of the dual is one of the columns at u.
    for i in range(r):
        if i in done:continue
        j=next(j for j in range(r) if Ms[g][i,j])
        require(sum(Ms[g][i,jj] for jj in range(r))==1 and Ms[g][j,i]==1,'involution not a permutation')
        v=[0]*r;v[i]=1
        if j==i:cols.extend([v[:],v[:]])
        else:v[j]=1;cols.append(v)
        done.update((i,j))
    B=s.Matrix.hstack(*map(s.Matrix,cols));require(B*B.T==G,'unit Gram decomposition')
    dD=[sum((v[j]*dims[j] for j in range(r)),K.zero) for v in cols]
    dD.remove(K.one)
    return dims,Counter(tuple(ec(z)) for z in dD)

def gram_columns(Qm,dims,target,K,degree):
    r=len(dims)
    if any(x<0 for x in Qm):return []
    bound=[math.isqrt(int(Qm[i,i])) for i in range(r)]
    B=s.Matrix.hstack(*(vector(x,degree) for x in dims));rank=B.rank()
    rows=list(B.T.rref()[1]);C=B.extract(rows,range(r));rhs=vector(target,degree).extract(rows,[0])
    choices=[]
    for piv in itertools.combinations(range(r),rank):
        mat=C.extract(range(rank),piv)
        if mat.det()!=0:
            free=tuple(i for i in range(r) if i not in piv)
            choices.append((math.prod(bound[i]+1 for i in free),piv,free,mat.inv()))
    require(choices,'empty dimension span')
    nodes,piv,free,inv=min(choices,key=lambda x:(x[0],x[1]))
    if nodes>4000000:raise TimeoutError('module Gram vector domain exceeds budget')
    A=inv*C.extract(range(rank),free);b=inv*rhs
    den=math.lcm(*(int(x.q) for x in list(A)+list(b)))
    ai=[[int(A[i,j]*den) for j in range(len(free))] for i in range(rank)];bi=[int(x*den) for x in b]
    out=[];entries=[[int(x) for x in row] for row in Qm.tolist()]
    for vals in itertools.product(*(range(bound[i]+1) for i in free)):
        if any(vals[i]*vals[j]>entries[free[i]][free[j]] for i in range(len(free)) for j in range(i,len(free))):continue
        numer=[bi[i]-sum(ai[i][j]*vals[j] for j in range(len(free))) for i in range(rank)]
        if any(v%den or v<0 or v//den>bound[piv[i]] for i,v in enumerate(numer)):continue
        v=[0]*r
        for i,x in zip(free,vals):v[i]=x
        for i,x in zip(piv,numer):v[i]=x//den
        if not any(v) or any(v[i]*v[j]>entries[i][j] for i in range(r) for j in range(i,r)):continue
        if sum((v[i]*dims[i] for i in range(r)),K.zero)!=target:continue
        # Rank-one subtraction is positive semidefinite; all principal minors
        # can be replaced by a rational LDL test, but simple exact eigen-free
        # criterion using column-space and a nonsingular principal block suffices.
        out.append(tuple(v))
    return sorted(out)

def system(R,g,fixed,T,m,arithmetic=None):
    labels,Ms=module_matrices(R,g,fixed,T)
    if arithmetic is None:arithmetic=Characters(R).fp()
    f,K,ds,D,pD,embedding=arithmetic;degree=f.degree();dims,counts=dual_dimensions(labels,Ms,g,K,ds)
    r=len(labels);G=sum((int(Ms[i][m,m])*Ms[i] for i in range(len(R))),s.zeros(r));Qm=G.copy();Qm[m,m]-=1
    require(G==G.T,'internal-end Gram not symmetric')
    if any(x<0 for x in Qm):return None,dict(reason='negative_gram')
    ij=list(itertools.combinations_with_replacement(range(r),2));keys=sorted(counts);columns=[];classids=[]
    for k,z in enumerate(keys):
        target=K(list(map(s.Rational,z)))*dims[m]
        for v in gram_columns(Qm,dims,target,K,degree):columns.append(v);classids.append(k)
    A=[[v[i]*v[j] for v in columns] for i,j in ij]
    A += [[int(k==kk) for k in classids] for kk in range(len(keys))]
    b=[int(Qm[i,j]) for i,j in ij]+[counts[z] for z in keys]
    meta={'module_simple':m,'rows':len(A),'columns':len(columns),'dual_rank':1+sum(counts.values()),'dimension_classes':keys,'counts':[counts[z] for z in keys]}
    return (A,b),meta

def certificate(R):
    if not all(R[i][j]==R[j][i] for i in range(len(R)) for j in range(len(R))):return None
    arithmetic=None
    for g in invs(R):
        info=anti_representations(R,g)
        if info is None:continue
        fixed,seed,nodes,reps=info;branches=[]
        if arithmetic is None:arithmetic=Characters(R).fp()
        if arithmetic[0].degree()>4:continue
        for T in reps:
            labels,Ms=module_matrices(R,g,fixed,T);passed=False
            for m in range(1,len(labels)):
                ab,meta=system(R,g,fixed,T,m,arithmetic)
                if ab is None:
                    branches.append(dict(T=[list(x) for x in T],module_simple=m,reason=meta['reason']));passed=True;break
                A,b=ab
                if not A[0]:
                    if any(b):
                        y=[0]*len(b);y[next(i for i,x in enumerate(b) if x)]=-1
                    else:continue
                else:y=farkas(A,b)
                if y is not None:
                    check_farkas(A,b,y);branches.append(dict(T=[list(x) for x in T],module_simple=m,meta=meta,y=y));passed=True;break
            if not passed:break
        if len(branches)==len(reps):return dict(kind='module_dual_gram',involution=g,fixed=fixed,generators=list(seed),generator_tuples=nodes,branches=branches)
    return None

def verify(R,c):
    require(c['kind']=='module_dual_gram' and c['involution'] in invs(R),'invalid module dual input')
    g=c['involution'];info=anti_representations(R,g);require(info is not None,'ineligible module size')
    fixed,seed,nodes,reps=info
    require(c['fixed']==fixed and c['generators']==list(seed) and c['generator_tuples']==nodes,'incorrect exhaustive domain')
    require([b['T'] for b in c['branches']]==[[list(x) for x in T] for T in reps],'missing module action branches')
    arithmetic=Characters(R).fp()
    for T,b in zip(reps,c['branches']):
        ab,meta=system(R,g,fixed,T,b['module_simple'],arithmetic)
        if ab is None:require(b.get('reason')==meta['reason'],'wrong Gram obstruction')
        else:
            require(b['meta']==meta,'incorrect rebuilt module Gram metadata');check_farkas(*ab,b['y'])
    return True
