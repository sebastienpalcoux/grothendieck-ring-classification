"""Quadratic character-level modular moment constraints (research refinement).

All new rows are exact. Eligibility requires the entire character field to be
contained in the quadratic field used by the relative twist traces.
"""
from spectral_induction import *
from higher_traces import trace_types

def coordinates(x,K):
    return list(reversed(x.to_list()))+[K.dom.zero]*(K.mod.degree()-len(x.to_list()))

def rational_rows(coeff,rhs,K):
    deg=K.mod.degree();cc=[coordinates(x,K) for x in coeff];bb=coordinates(rhs,K)
    for k in range(deg):
        row=[Q(str(x[k])) for x in cc];rv=Q(str(bb[k]));den=math.lcm(rv.denominator,*(x.denominator for x in row));rr=[int(x*den) for x in row];b=int(rv*den);g=math.gcd(b,*rr) or 1
        yield [x//g for x in rr],b//g

def system(R,data,tab,cols,ep,height,lab,cubic=False,restriction_products=False,rational_rotations=False):
    K=tab.K;n=len(R)
    require(K.mod.degree() <= (1 if data['q']==1 else 2),'complete character field outside trace field')
    # This also explicitly checks that sqrt(q) embeds in the field, as initialized.
    sq=K.from_sympy(s.sqrt(data['q']))
    types,_=trace_types(data['q'],data['primes'],height)
    one=types.index(tuple((Q(1),Q(0)) for _ in range(height)))
    phases=[K(t[0][0])+K(t[0][1])*sq for t in types]
    L=s.Matrix.hstack(*map(s.Matrix,cols));_,high=high_columns(data,L);spec=Spectrum(tab,cols,high)
    A,b,meta=system_rotation(R,data,L,ep,height);labs=meta['labels'];rows,rhs=spec.balance(labs,len(A[0]),one);A+=rows;b+=rhs
    old=len(A[0]);keep=[j for j in range(old) if j>=len(labs) or list(labs[j][0]) not in spec.forbidden]
    A=[[row[j] for j in keep] for row in A];nv=len(keep);tuples=dict(zip(spec.vectors,spec.types));nold=nv
    # high and rotation counts are integers in a genuine category, whereas the
    # slack variables for inequalities need not be integral in this normalization.
    rot=set(j for block in meta['rotation_blocks'] for j in range(block['start'],block['start']+block['count']))
    integrality=[int(j<len(labs) or j in rot) for j in keep]
    for a,bb in itertools.combinations_with_replacement(range(1,n),2):
        ha,hb=lab[a],lab[bb]
        weights={v:tuples[v][ha]*tuples[v][hb]*tab.dims[v]**2 for v in set(spec.vectors)}
        rhs=tab.D*tab.dims[tuple(cols[a])]*tab.values[ha,tuple(cols[bb])]-sum((weights[v] for v in spec.low),K.zero)
        coeff=[weights[(0,)+tuple(labs[j][0])]*phases[labs[j][1]] if j<len(labs) else K.zero for j in keep]
        for row,c in rational_rows(coeff,rhs,K):A.append(row);b.append(c)
    triple_vars={}
    if cubic:
        require(all(R[i][i][0]==1 for i in range(n)),'cubic prototype requires self-duality of all ring simples')
        for a,bb,c in itertools.combinations_with_replacement(range(1,n),3):
            ha,hb,hc=[lab[x] for x in (a,bb,c)]
            weights={v:tuples[v][ha]*tuples[v][hb]*tuples[v][hc]*tab.dims[v]**2/tab.D**2 for v in set(spec.vectors)}
            rhs=-sum((weights[v] for v in spec.low),K.zero)
            coeff=[weights[(0,)+tuple(labs[j][0])] if j<len(labs) else K.zero for j in keep]+[K.zero]*(nv-nold)+[-K.one]
            for row in A:row.append(0)
            triple_vars[tuple(sorted((a,bb,c)))]=nv
            nv+=1;integrality.append(1)
            for row,c in rational_rows(coeff,rhs,K):A.append(row);b.append(c)
    if restriction_products:
        require(cubic,'restriction products require low Verlinde coefficients')
        allowed=[v for v in spec.high if list(v[1:]) not in spec.forbidden]
        for a,bb in itertools.combinations_with_replacement(range(1,n),2):
            ca,cb=tuple(cols[a]),tuple(cols[bb]);fp=[sum(ca[i]*cb[j]*R[i][j][k] for i in range(n) for j in range(n)) for k in range(n)]
            qvars={}
            for v in allowed:
                bound=min(fp[k]//v[k] for k in range(n) if v[k])
                if bound:
                    qvars[v]=(nv,bound);nv+=1;integrality.append(1)
            for row in A:row += [0]*(nv-len(row))
            for k in range(n):
                row=[0]*nv
                for c in range(1,n):row[triple_vars[tuple(sorted((a,bb,c)))]]+=cols[c][k]
                for v,(j,M) in qvars.items():row[j]=v[k]
                rhs=fp[k]-int(a==bb and k==0);A.append(row);b.append(rhs)
            for v,(j,M) in qvars.items():
                row=[0]*(nv+1);row[j]=1;row[nv]=1
                for jj,k in enumerate(keep):
                    if k<len(labs) and tuple(labs[k][0])==v[1:]:row[jj]-=M
                for rr in A:rr.append(0)
                A.append(row);b.append(0);integrality.append(1);nv+=1
    scales={}
    if rational_rotations:
        from tensor_rotation import rotation_types
        for block in meta['rotation_blocks']:
            order=block['order'];overlap=math.prod(p**int(s.factorint(order).get(p,0)) for p in data['primes'])
            if overlap>2:continue
            rs=[int(v) for v in s.divisors(order) if v<order];rt=rotation_types(data['q'],order,rs)
            weights={}
            for dd in s.divisors(order):
                dd=int(dd);tt=tuple((Q(int(s.mobius(dd//math.gcd(dd,r))),int(s.totient(dd//math.gcd(dd,r)))),Q(0)) for r in rs)
                weights[tt]=math.gcd(weights.get(tt,0),int(s.totient(dd)))
            for offset,tt in enumerate(rt):
                require(tt in weights,'nonrational rotation type in rational intersection')
                j=keep.index(block['start']+offset);scales[j]=weights[tt]
        for row in A:
            for j,w in scales.items():row[j]*=w
    return A,b,{'keep':keep,'labels':labs,'integrality':integrality,'spec':spec.metadata(),'column_vectors':spec.high,'rotation_scales':scales}

def congruence_witness(A,b,integrality,primes=(2,3,5,7,11,13,17,19)):
    """A finite-field left-null witness supported on exact integer-count rows."""
    integer=[j for j,x in enumerate(integrality) if x];cont=[j for j,x in enumerate(integrality) if not x]
    ix=[i for i,row in enumerate(A) if not any(row[j] for j in cont)]
    for p in primes:
        # Reduce the augmented equation rows, tracking integer row operations mod p.
        basis={}
        for i in ix:
            v=[A[i][j]%p for j in integer]+[b[i]%p];w={i:1}
            for k in sorted(basis):
                if v[k]:
                    u,z=basis[k];a=v[k];v=[(x-a*y)%p for x,y in zip(v,u)]
                    for j,y in z.items():
                        w[j]=(w.get(j,0)-a*y)%p
                        if not w[j]:w.pop(j)
            pivot=next((j for j,x in enumerate(v[:-1]) if x),None)
            if pivot is None:
                if v[-1]:return {'prime':p,'rows':sorted([i,x] for i,x in w.items()),'value':v[-1]}
                continue
            q=pow(v[pivot],-1,p);v=[x*q%p for x in v];w={i:x*q%p for i,x in w.items()};basis[pivot]=(v,w)
    return None

def check_congruence(A,b,integrality,w):
    p=w['prime'];require(s.isprime(p),'congruence modulus not prime');y=[0]*len(A)
    for i,x in w['rows']:require(0<=i<len(A) and 0<x<p and y[i]==0,'bad congruence witness');y[i]=x
    cont=[j for j,x in enumerate(integrality) if not x]
    require(all(not y[i] or not any(A[i][j] for j in cont) for i in range(len(A))),'continuous variables in congruence row')
    require(all(sum(y[i]*A[i][j] for i in range(len(A)))%p==0 for j,x in enumerate(integrality) if x),'congruence functional not null')
    value=sum(x*z for x,z in zip(y,b))%p;require(value and value==w['value'],'congruence right side vanishes')
