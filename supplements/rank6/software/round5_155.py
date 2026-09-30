"""Unified pointed-subcategory twist support; R155 discovery and exact replay."""
import itertools
from exact import require
import round4_155 as V

def pointed_projection_system(R,data,cols,ep,lab):
    A,b,meta=V.system(R,data,cols,ep,lab)
    if A is None:return A,b,meta
    C=data['C'];F=data['F'];height=data['height'];phases=data['phases'];labels=meta['labels'];n=len(R)
    involutions=[g for g in range(1,n) if R[g][g]==[int(k==0) for k in range(n)]]
    allowed={}
    for g in involutions:
        require(ep[g-1] in (-1,1),'wrong invertible second indicator')
        if ep[g-1]==1:roots=[C.one,-C.one]
        else:
            require(F%4==0,'missing fourth roots');roots=[C.unit**(F//4),-C.unit**(F//4)]
        allowed[g]={tuple(z**k for k in range(1,height+1)) for z in roots}
    keep=[j for j in range(len(A[0])) if j>=len(labels) or all(not labels[j][0][g-1] or phases[labels[j][1]] in allowed[g] for g in involutions)]
    A=[[row[j] for j in keep] for row in A]
    meta.update(projection_involutions=involutions,keep=keep,projection_labels=[labels[j] for j in keep if j<len(labels)],variables=len(keep),rows=len(A))
    return A,b,meta

def nonselfdual_stabilizer_system(R,data,cols,ep,lab,exact_cubic_value=None):
    """Pair-insertion bound for every forced anticommuting fixed simple.

    No self-duality condition is needed by the pivotal rotation proof.
    This implementation keeps the real relative-average bound nu3<=m/4.
    """
    from fractions import Fraction
    from module_dual_gram import anti_representations
    from involution_module import invs
    from modular_character_induction import rational_rows
    A,b,meta=pointed_projection_system(R,data,cols,ep,lab)
    if A is None:return A,b,meta
    C=data['C'];D=data['DD'];dims=data['dims'];F=data['F'];labels=meta['labels'];keep=meta['keep'];nv=len(A[0]);nh=len(labels);objects=[];module=[]
    require(F%3!=0,'this implementation requires the third-root average to be real')
    for g in invs(R):
        info=anti_representations(R,g)
        if info is None:continue
        fixed,seed,nodes,reps=info;f=len(fixed)
        for j,obj in enumerate(fixed):
            if reps and all(T[g][j*f+j]==-1 for T in reps):
                objects.append(obj)
                module.append(dict(g=g,fixed=fixed,generators=list(seed),nodes=nodes,representations=[list(map(list,T)) for T in reps],object=obj))
    objects=sorted(set(objects))
    for obj in objects:
        m=sum(R[obj][obj][j]*R[j][obj][0] for j in range(len(R)))
        require(m%2==0,'odd Clifford module dimension')
        low=sum((C(v[obj])*sum((C(v[i])*dims[i] for i in range(len(R))),C.zero) for v in cols),C.zero)
        coeff=[C(labels[j][0][obj-1])*sum((C(labels[j][0][i-1])*dims[i] for i in range(1,len(R))),C.zero)*data['phases'][labels[j][1]][2] if j<nh else C.zero for j in keep]+[C.zero]*(nv-len(keep))
        if exact_cubic_value is None:
            # Normalized averaging gives -m/2 <= nu3 <= m/4.
            for row in A:row.append(0)
            coeff.append(D);nv+=1;rhs=C(Fraction(m,4))*D-low
        else:rhs=C(exact_cubic_value)*D-low
        for row,val in rational_rows(coeff,rhs,C):A.append(row);b.append(val)
    meta.update(cubic_stabilizer_objects=objects,forced_module_data=module,rows=len(A),variables=nv)
    return A,b,meta

def profile_lattice(R,data,cols,lab,degree=4):
    """Exact bounded lattice for Gram, Galois and low-word constraints."""
    import math
    import sympy as s
    from fractions import Fraction
    from spectral_induction import Spectrum
    from round4_quartic_profiles import word_forms
    from round3_m4 import high_vectors
    from exact import evaluate
    G,V0=high_vectors(data,cols);sp=Spectrum(data['tab'],cols,[(v,None) for v in V0]);V=[v for v in V0 if list(v) not in sp.forbidden]
    require(not sp.missing_low,'missing low spectral type')
    n=len(V);r=len(R);A=[];b=[]
    for i in range(r-1):
        for j in range(i,r-1):A.append([v[i]*v[j] for v in V]);b.append(int(G[i,j]))
    aa,bb=sp.balance([(v,None) for v in V],n);A+=aa;b+=bb
    bounds=[min(int(G[i,i])//(v[i]*v[i]) for i in range(r-1) if v[i]) for v in V]
    C=data['C'];star=[lab.index(data['tab'].rows.index(tuple(evaluate(x.to_list(),C.unit**(data['F']-1),C) for x in data['tab'].rows[lab[a]]))) for a in range(r)]
    constraints=[]
    for height in range(3,degree+1):
        for word,forms in word_forms(data,cols,V,sp,lab,height):
            for denominator,row in forms[1:]:
                if any(row):A.append(list(row[1:]));b.append(-row[0])
            denominator,row=forms[0];upper=sum(abs(a)*x for a,x in zip(row[1:],bounds))+abs(row[0])
            if height==3:
                for a,bb,c in set(itertools.permutations(word)):
                    product=[sum(cols[a][i]*cols[bb][j]*R[i][j][k] for i in range(r) for j in range(r)) for k in range(r)]
                    upper=min(upper,denominator*min(product[k]//cols[star[c]][k] for k in range(r) if cols[star[c]][k]))
            constraints.append((denominator,row,upper))
    rr,piv=s.Matrix(A).row_join(s.Matrix(b)).rref()
    if n in piv:return dict(inconsistent=True,high_columns=[list(v) for v in V])
    free=[j for j in range(n) if j not in piv];coeff=[[Fraction(i==j) for j in free] for i in range(n)];constant=[Fraction(0)]*n
    for h,i in enumerate(piv):constant[i]=Fraction(rr[h,-1]);coeff[i]=[-Fraction(rr[h,j]) for j in free]
    records=[(constant[i],coeff[i],bounds[i],1) for i in range(n)]
    for denominator,row,upper in constraints:
        records.append((row[0]+sum(a*x for a,x in zip(row[1:],constant)),[sum(a*c[j] for a,c in zip(row[1:],coeff)) for j in range(len(free))],upper,denominator))
    order=sorted(range(len(free)),key=lambda j:(bounds[free[j]],-sum(abs(c[j]) for _,c,_,_ in records)))
    normalized=[]
    for constant,row,upper,modulus in records:
        row=[row[j] for j in order];den=math.lcm(*(x.denominator for x in [constant]+row));normalized.append([int(constant*den),[int(x*den) for x in row],int(upper*den),int(modulus*den)])
    return dict(inconsistent=False,free=[free[j] for j in order],bounds=[bounds[free[j]] for j in order],records=normalized,variables=n,high_columns=[list(v) for v in V])


def enumerate_lattice(domain,node_limit=10000000):
    """Optimizer-free exhaustive interval/congruence recursion."""
    import math
    if domain['inconsistent']:return [],0
    bounds=domain['bounds'];records=domain['records'];n=len(bounds);m=len(records);nv=domain['variables'];mn=[[0]*m for _ in range(n+1)];mx=[[0]*m for _ in range(n+1)];gcd=[[0]*m for _ in range(n+1)]
    for i,(_,_,_,modulus) in enumerate(records):gcd[n][i]=modulus
    for k in range(n-1,-1,-1):
        for i,(_,row,_,_) in enumerate(records):
            value=row[k]*bounds[k];mn[k][i]=mn[k+1][i]+min(0,value);mx[k][i]=mx[k+1][i]+max(0,value);gcd[k][i]=math.gcd(gcd[k+1][i],row[k])
    out=[];nodes=0
    def visit(k,partial):
        nonlocal nodes
        nodes+=1
        if nodes>node_limit:raise TimeoutError('exact affine lattice node budget; no completeness claim')
        if any(value+mx[k][i]<0 or value+mn[k][i]>records[i][2] or value%gcd[k][i] for i,value in enumerate(partial)):return
        if k==n:out.append([partial[i]//records[i][3] for i in range(nv)]);return
        for x in range(bounds[k]+1):visit(k+1,[value+records[i][1][k]*x for i,value in enumerate(partial)])
    visit(0,[row[0] for row in records]);return sorted(out),nodes

def verify_pointed_reduction(R,record):
    import round3_m4 as M
    from induction import low_failure
    from higher_traces import check_farkas
    require(record.get('complete') is True,'pointed reduction is incomplete')
    data=M.data_for(R,record['height'],record['F']);expected=[];nrays=0;survivors=[]
    for ix,cols in enumerate(data['lows']):
        why=low_failure(cols,data['ch'].C,data['ds'],data['D'],data['K'],data['embedding'],data['ch'].du);labs=data['tab'].assignments(cols)
        if why:expected.append((ix,None,None));rec=record['branches'][len(expected)-1];require(rec=={'low':ix,'ordinary':why},'ordinary branch mismatch');continue
        if not labs:expected.append((ix,None,None));rec=record['branches'][len(expected)-1];require(rec=={'low':ix,'no_labellings':True},'character domain mismatch');continue
        for lab in labs:
            for ep in M.indicator_choices(R):
                expected.append((ix,list(lab),list(ep)));rec=record['branches'][len(expected)-1];require((rec['low'],rec.get('lab'),rec.get('ep'))==expected[-1],'incomplete labelling/indicator domain');A,b,meta=pointed_projection_system(R,data,cols,ep,lab)
                if A is None:require(rec['outcome']=='spectral' and rec['meta']==meta,'spectral mismatch');continue
                require((len(A),len(A[0]))==(rec['rows'],rec['columns']),'system shape mismatch')
                if rec['outcome']=='exact_farkas':check_farkas(A,b,rec['ray']);nrays+=1
                else:survivors.append(dict(low=ix,labelling=list(lab),indicators=list(ep)))
    require(len(expected)==len(record['branches']),'extra branch in record')
    return dict(passed=True,optimizer_used=False,exact_rays=nrays,survivors=survivors)

def check_sparse_ray(rows,rhs,nv,y):
    require(len(y)==len(rhs) and all(type(x) is int for x in y),'bad sparse ray')
    z=[0]*nv
    for row,weight in zip(rows,y):
        if weight:
            for j,a in row.items():z[int(j)]+=a*weight
    require(all(x>=0 for x in z) and sum(a*b for a,b in zip(rhs,y))<0,'sparse Farkas inequality failed')
    return True


def sparse_ray(rows,rhs,nv,time_limit=20):
    import numpy as np
    import sympy as s
    import math
    from fractions import Fraction
    from scipy.sparse import coo_matrix,hstack,vstack,csr_matrix
    from scipy.optimize import linprog
    ii=[];jj=[];vv=[]
    for i,row in enumerate(rows):
        for j,a in row.items():ii.append(i);jj.append(int(j));vv.append(a)
    A=coo_matrix((np.array(vv,dtype=float),(ii,jj)),shape=(len(rows),nv)).tocsr();b=np.asarray(rhs,dtype=float);m=len(rhs);scale=np.maximum(1,np.maximum(abs(A).max(axis=1).toarray().ravel(),abs(b)));AA=A.multiply(1/scale[:,None]).tocsr();bb=b/scale
    sol=linprog(np.ones(2*m),A_ub=vstack([hstack([-AA.T,AA.T]),csr_matrix(np.r_[bb,-bb][None,:])]),b_ub=np.r_[np.zeros(nv),-1.],bounds=(0,None),options={'time_limit':time_limit})
    if not sol.success:return None
    y=(sol.x[:m]-sol.x[m:])/scale;y/=max(abs(y));support=np.flatnonzero(abs(y)>1e-9).tolist()
    for denominator in [100,10000,1000000]:
        yy=[Fraction(float(y[i])).limit_denominator(denominator) if i in support else Fraction(0) for i in range(m)];den=math.lcm(*(z.denominator for z in yy));out=[int(z*den) for z in yy]
        try:check_sparse_ray(rows,rhs,nv,out);return out
        except Exception:pass
    for threshold in [1e-8,1e-7,1e-6]:
        active=np.flatnonzero(abs(A.T@y)<threshold).tolist();Q=s.Matrix([[rows[i].get(j,0) for i in support] for j in active]+[[rhs[i] for i in support]]);target=s.zeros(Q.rows,1);target[-1]=-1;rr,piv=Q.row_join(target).rref()
        if len(piv)!=len(support) or (piv and piv[-1]>=len(support)):continue
        zz=[rr[i,-1] for i in range(len(support))];den=math.lcm(*(int(z.q) for z in zz));out=[0]*m
        for i,z in zip(support,zz):out[i]=int(z*den)
        gcd=math.gcd(*out);out=[x//gcd for x in out]
        try:check_sparse_ray(rows,rhs,nv,out);return out
        except Exception:pass
    return None

def pointed_pair_action(R,data,cols,lab,A,b,labels,kept,g,h,sign=1):
    """Necessary simultaneous lifts: q(g)=i,q(h)=-1,q(gh)=sign*i.

    Both lifts have order two, and the forgetful kernel must be trivial.
    The low unit forces each lift to be unique with the prescribed twist.
    """
    from collections import Counter
    from modular_character_induction import rational_rows
    C=data['C'];tab=data['tab'];F=data['F'];phases=data['phases'];height=len(phases[0]);require(F%4==0 and sign in (-1,1),'bad pointed quadratic form');ii=C.unit**(F//4);one=phases.index(tuple(C.one for _ in range(height)));nv=len(A[0]);variables={};constant=Counter();pairing=-sign
    mul=lambda v,k:tuple(sum(v[i]*R[k][i][j] for i in range(len(R))) for j in range(len(R)))
    for a,v in enumerate(cols):
        values=[]
        for k in (g,h):
            z=tab.rows[lab[a]][k];require(z in (C.one,-C.one),'non-sign low monodromy');values.append(1 if z==C.one else -1)
        constant[(tuple(v),one,*values)]+=1
    for j,orig in enumerate(kept):
        if orig<len(labels):
            v,t=labels[orig]
            for eg,eh in itertools.product((-1,1),repeat=2):variables[((0,)+tuple(v),t,eg,eh)]=nv;nv+=1
    for row in A:row.extend([0]*(nv-len(row)))
    for j,orig in enumerate(kept):
        if orig<len(labels):
            v,t=labels[orig];row=[0]*nv;row[j]=-1
            for eg,eh in itertools.product((-1,1),repeat=2):row[variables[((0,)+tuple(v),t,eg,eh)]]=1
            A.append(row);b.append(0)
    domain=set(variables)|set(constant)
    for generator in (g,h):
        seen=set()
        for key in sorted(domain):
            v,t,eg,eh=key
            if generator==g:factor=ii*C(eg);eg1=-eg;eh1=pairing*eh
            else:factor=C(-eh);eg1=pairing*eg;eh1=eh
            phase=tuple(factor**k*z for k,z in enumerate(phases[t],1));require(phase in phases,'pointed action leaves phase domain');other=(mul(v,generator),phases.index(phase),eg1,eh1);pair=tuple(sorted((key,other)))
            if pair in seen:continue
            seen.add(pair);row=[0]*nv
            if key in variables:row[variables[key]]+=1
            if other in variables:row[variables[other]]-=1
            if any(row) or constant[other]!=constant[key]:A.append(row);b.append(constant[other]-constant[key])
    for which in (0,1,2):
        for i in range(len(R)):
            row=[C.zero]*nv
            for (v,t,eg,eh),j in variables.items():
                ep=eg if which==0 else eh if which==1 else eg*eh;dv=sum((C(v[k])*data['dims'][k] for k in range(len(R))),C.zero);row[j]=C(ep*v[i])*dv
            rhs=-sum((C((eg if which==0 else eh if which==1 else eg*eh)*v[i]*ct)*sum((C(v[k])*data['dims'][k] for k in range(len(R))),C.zero) for (v,t,eg,eh),ct in constant.items()),C.zero)
            for rr,bb in rational_rows(row,rhs,C):A.append(rr);b.append(bb)
    return A,b,dict(new_variables=nv-len(kept),quadratic_sign=sign,variables=nv,rows=len(A))

def pointed_profile_reason(R,cols,high,profile):
    """Forgetful-kernel injectivity, subgroup image, and tensor permutation."""
    from collections import Counter
    counts=Counter(map(tuple,cols));counts.update({(0,)+tuple(v):m for v,m in zip(high,profile) if m})
    inv=[g for g in range(len(R)) if sum(R[g][g])==1 and R[g][g][0]]
    image=[g for g in inv if counts[tuple(int(i==g) for i in range(len(R)))]]
    require(counts[tuple([1]+[0]*(len(R)-1))]==1,'nontrivial forgetful kernel')
    if any(counts[tuple(int(i==g) for i in range(len(R)))]>1 for g in inv):return 'noninjective_image',image
    if any(next(k for k,z in enumerate(R[g][h]) if z) not in image for g in image for h in image):return 'image_not_subgroup',image
    for g in image:
        for v,m in list(counts.items()):
            w=tuple(sum(v[i]*R[g][i][k] for i in range(len(R))) for k in range(len(R)))
            if counts[w]!=m:return 'action_count',image
    return None,image

def pointed_stabilizer_divisibility(R,cols,high,profile,group,radical):
    """Every simple stabilizer lies in the radical of pointed monodromy."""
    from collections import Counter
    counts=Counter(map(tuple,cols));counts.update({(0,)+tuple(v):m for v,m in zip(high,profile) if m})
    failures=[]
    for v,m in sorted(counts.items()):
        stabilizer=[g for g in group if tuple(sum(v[i]*R[g][i][k] for i in range(len(R))) for k in range(len(R)))==v]
        divisor=len(stabilizer)//len(set(stabilizer)&set(radical))
        if m%divisor:failures.append(dict(column=list(v),multiplicity=m,divisor=divisor))
    return failures

def verify_labelling_quotient(cols,labs):
    witnesses=[]
    for lab in labs:
        perms=[p for p in itertools.permutations(range(len(cols))) if all(cols[p[a]]==cols[a] and lab[a]==labs[0][p[a]] for a in range(len(cols)))]
        require(bool(perms),'unproved character labelling quotient');witnesses.append(list(perms[0]))
    return witnesses

def semion_packet_frontier(R,data,cols,lab,high,profile,g):
    """Complete centralizer packet orientations and restricted adjunction.

    Requires a pure central lift of g with twist +i or -i. Only the center
    is decomposed as Semion times its centralizer, never the original C.
    """
    import numpy as np
    from collections import Counter
    n=len(R);counts=Counter(map(tuple,cols));counts.update({(0,)+tuple(v):m for v,m in zip(high,profile)if m})
    mul=lambda v:tuple(sum(v[i]*R[g][i][k]for i in range(n))for k in range(n))
    C=data['C'];selected=[a for a in range(len(cols))if data['tab'].rows[lab[a]][g]==C.one]
    require(all(data['tab'].rows[lab[a]][g]in(C.one,-C.one)for a in range(len(cols))),'nonsign semion monodromy')
    wanted=Counter(tuple(cols[a])for a in selected);require(0 in selected and wanted[tuple(cols[0])]==1,'centralizer adjoint unit')
    ccol=tuple(sum(cols[a][k]for a in selected if a)for k in range(n));RFc=sum((ccol[k]*np.array(R[k],dtype=np.int64).T for k in range(n)),np.zeros((n,n),dtype=np.int64))
    seen=set();packets=[]
    for v in sorted(counts):
        if v in seen:continue
        packet=Counter([v,mul(v)]);seen.update(packet);m=counts[v]//packet[v]
        if any(counts[w]!=m*z for w,z in packet.items()):return dict(complete=True,packet_failure=True,survivors=[])
        vectors=sorted(packet);compositions=[(m,)]if len(vectors)==1 else[(a,m-a)for a in range(m+1)]
        choices=[p for p in compositions if all(ct==wanted[w]for w,ct in zip(vectors,p)if w[0])]
        packets.append((vectors,choices))
    dual=[next(j for j in range(n)if R[i][j][0])for i in range(n)];survivors=[];reject=Counter();tested=0
    for choices in itertools.product(*(p[1]for p in packets)):
        tested+=1;W=[v for(vs,cs),p in zip(packets,choices)for v,m in zip(vs,p)for _ in range(m)];cc=Counter(W)
        if any(cc[tuple(v[dual[i]]for i in range(n))]!=m for v,m in cc.items()):reject['duality']+=1;continue
        # These small input bounds explicitly protect exact int64 arithmetic.
        bound=max([1]+[abs(x)for v in W for x in v]+[abs(int(x))for row in RFc for x in row]);require(max(1,len(W),n)**3*bound**3<2**62,'int64 exactness bound')
        mat=np.array(W,dtype=np.int64).T;Nsum=mat.T@mat-np.eye(len(W),dtype=np.int64)
        if np.any(Nsum<0):reject['negative_fusion_entry']+=1;continue
        if not np.array_equal(mat@Nsum,RFc@mat):reject['restriction_product']+=1;continue
        survivors.append(dict(W=[list(v)for v in W],Nsum=Nsum.tolist()))
    return dict(complete=True,selected_low=selected,packet_choices=[len(cs)for vs,cs in packets],tested=tested,rejections=dict(reject),survivors=survivors)

def charge_coupled_pointed_action(R,data,cols,lab,ss,words,g,h,sign=-1,qg_sign=1):
    """One assignment for word coefficients, twists, and monodromy charges."""
    from collections import Counter
    from modular_character_induction import rational_rows
    C=data['C'];phases=data['phases'];height=len(phases[0]);ii=C(qg_sign)*C.unit**(data['F']//4);require(sign in(-1,1)and qg_sign in(-1,1),'bad quadratic form')
    lowcharge=[tuple(1 if data['tab'].rows[lab[a]][k]==C.one else-1 for k in(g,h))for a in range(len(cols))]
    charges=[tuple(__import__('math').prod(lowcharge[a][k]for a in w)for k in(0,1))for w in words];old2new={};labels=[];integ=[];totals={}
    for j,(q,t)in enumerate(ss['labels']):
        old2new[j]=[]
        if q=='aux':old2new[j].append(len(labels));labels.append(('aux',t));integ.append(ss['integrality'][j]);continue
        v,x=ss['coefficient_labels'][q];support={ch for z,ch in zip(x,charges)if z};allowed=list(support)if len(support)==1 else list(itertools.product((-1,1),repeat=2))if not support else[]
        for eg,eh in allowed:
            k=len(labels);old2new[j].append(k);labels.append((q,t,eg,eh));integ.append(1);totals.setdefault((tuple(v),t,eg,eh),[]).append(k)
    rows=[{k:int(a)for j,a in row.items()for k in old2new[int(j)]}for row in ss['rows']];rhs=list(ss['rhs']);one=phases.index(tuple(C.one for _ in range(height)));constant=Counter((tuple(v),one,*lowcharge[a])for a,v in enumerate(cols));domain=set(totals)|set(constant);pairing=-sign
    mul=lambda v,k:tuple(sum(v[i]*R[k][i][j]for i in range(len(R)))for j in range(len(R)))
    for generator in(g,h):
        seen=set()
        for key in sorted(domain):
            v,t,eg,eh=key
            if generator==g:factor=ii*C(eg);eg1=-eg;eh1=pairing*eh
            else:factor=C(-eh);eg1=pairing*eg;eh1=eh
            phase=tuple(factor**k*z for k,z in enumerate(phases[t],1));require(phase in phases,'nonclosed trace phases');other=(mul(v,generator),phases.index(phase),eg1,eh1);pair=tuple(sorted((key,other)))
            if pair in seen:continue
            seen.add(pair);row=Counter({k:1 for k in totals.get(key,[])})
            for k in totals.get(other,[]):row[k]-=1
            row={k:z for k,z in row.items()if z};val=constant[other]-constant[key]
            if row or val:rows.append(row);rhs.append(val)
    for which in(0,1,2):
        for i in range(len(R)):
            row=[C.zero]*len(labels)
            for(v,t,eg,eh),js in totals.items():
                ep=eg if which==0 else eh if which==1 else eg*eh;dv=sum((C(v[k])*data['dims'][k]for k in range(len(R))),C.zero)
                for j in js:row[j]=C(ep*v[i])*dv
            val=-sum((C((eg if which==0 else eh if which==1 else eg*eh)*v[i]*ct)*sum((C(v[k])*data['dims'][k]for k in range(len(R))),C.zero)for(v,t,eg,eh),ct in constant.items()),C.zero)
            for rr,bb in rational_rows(row,val,C):rows.append({j:int(z)for j,z in enumerate(rr)if z});rhs.append(int(bb))
    return dict(rows=rows,rhs=rhs,labels=labels,integrality=integ,coefficient_labels=ss['coefficient_labels'])

def sparse_congruence(rows,rhs,nv,primes=(2,3)):
    """Exact sparse finite-field discovery; every variable must be integral."""
    for prime in primes:
        basis={}
        for i,row in enumerate(rows):
            v={int(j):int(a)%prime for j,a in row.items()if a%prime};value=rhs[i]%prime;w={i:1}
            while v:
                pivot=min(v)
                if pivot not in basis:
                    factor=pow(v[pivot],-1,prime);basis[pivot]=({j:a*factor%prime for j,a in v.items()},value*factor%prime,{j:a*factor%prime for j,a in w.items()});break
                u,ub,uw=basis[pivot];factor=v[pivot];value=(value-factor*ub)%prime
                for j,a in u.items():
                    z=(v.get(j,0)-factor*a)%prime
                    if z:v[j]=z
                    elif j in v:del v[j]
                for j,a in uw.items():
                    z=(w.get(j,0)-factor*a)%prime
                    if z:w[j]=z
                    elif j in w:del w[j]
            else:
                if value:return dict(prime=prime,rows=sorted(map(list,w.items())),value=value)
    return None

def check_sparse_congruence(rows,rhs,nv,witness):
    import sympy as s
    p=witness['prime'];require(s.isprime(p),'nonprime congruence');y={int(i):int(x)for i,x in witness['rows']};require(len(y)==len(witness['rows'])and all(0<=i<len(rows)and 0<x<p for i,x in y.items()),'bad congruence coefficients');result=[0]*nv
    for i,x in y.items():
        for j,a in rows[i].items():result[int(j)]+=x*a
    require(all(z%p==0 for z in result),'nonzero congruence coefficients');value=sum(x*rhs[i]for i,x in y.items())%p;require(value!=0 and value==witness['value'],'zero congruence rhs');return True

def split_centralizer_adjoint(R,data,cols,lab,packet,g,h,sign):
    """Recover the two low matrices from the pointed monodromy grading.

    For A1 of charge + and A2 of charge -, N_A1 is the same-charge block
    of V^t V-I, while N_A2 is its complementary block. Copy permutations
    justify enumeration of charge counts inside each restriction type.
    """
    import numpy as np
    from collections import Counter
    require(sign in(-1,1),'bad pointed quadratic sign');n=len(R);C=data['C'];W=packet['W'];counts=Counter(map(tuple,W));gh=next(i for i,x in enumerate(R[g][h])if x);centralizer_invertible=h if sign==-1 else gh;pure=tuple(int(i==centralizer_invertible)for i in range(n))
    if counts[pure]!=1:return dict(complete=True,wrong_pointed_component=True,survivors=[])
    charge=lambda a,k:1 if data['tab'].rows[lab[a]][k]==C.one else-1
    require(charge(1,g)==charge(2,g)==1 and charge(1,h)==1 and charge(2,h)==-1,'wrong low gradings')
    mul=lambda v:tuple(sum(v[i]*R[g][i][k]for i in range(n))for k in range(n))
    forced=Counter()
    for a,v in enumerate(cols):
        eg=charge(a,g);eh=charge(a,h);forced[(tuple(v)if eg==1 else mul(v),eh if eg==1 else-sign*eh)]+=1
    forced[pure,-sign]=max(forced[pure,-sign],1)
    types=sorted(counts);ranges=[range(forced[v,1],counts[v]-forced[v,-1]+1)for v in types];positions={v:[i for i,w in enumerate(W)if tuple(w)==v]for v in types};mat=np.array(W,dtype=np.int64).T;Ns=np.array(packet['Nsum'],dtype=np.int64);Fa=sum((cols[1][k]*np.array(R[k],dtype=np.int64).T for k in range(n)),np.zeros((n,n),dtype=np.int64));rank=len(W);bound=max([1]+[abs(int(x))for row in Ns for x in row]+[abs(int(x))for row in Fa for x in row]);require(max(rank,n)**2*bound**3<2**62,'int64 exactness bound');sur=[];reject=Counter();tested=0
    for cc in itertools.product(*ranges):
        tested+=1;eps=np.full(rank,-1,dtype=np.int64)
        for v,number in zip(types,cc):eps[positions[v][:number]]=1
        dual=[next(j for j in range(n)if R[i][j][0])for i in range(n)];charged=Counter((tuple(v),int(e))for v,e in zip(W,eps))
        if any(charged[(tuple(v[dual[i]]for i in range(n)),e)]!=m for(v,e),m in charged.items()):reject['charged_duality']+=1;continue
        action=lambda v:tuple(sum(v[i]*R[centralizer_invertible][i][k]for i in range(n))for k in range(n))
        if any(charged[(action(v),e if sign==-1 else-e)]!=m or (sign==-1 and e==1 and action(v)==v and m%2)for(v,e),m in charged.items()):reject['pointed_charge_action']+=1;continue
        A=Ns*((eps[:,None]*eps[None,:]+1)//2)
        if not np.array_equal(mat@A,Fa@mat):reject['restriction_product']+=1;continue
        if not np.array_equal(A@Ns,Ns@A):reject['commutation']+=1;continue
        sur.append(dict(plus_counts=list(cc),charges=eps.tolist(),Na=A.tolist(),Nb=(Ns-A).tolist()))
    return dict(complete=True,types=[list(v)for v in types],ranges=[list(z)for z in ranges],tested=tested,rejections=dict(reject),survivors=sur)

def sparse_prime_power_congruence(rows,rhs,nv,prime=2,power=6):
    """Local Smith elimination over Z/p^k, with an exact integer witness."""
    modulus=prime**power;rr=[{int(j):a%modulus for j,a in row.items()if a%modulus}for row in rows];bb=[x%modulus for x in rhs];ww=[{i:1}for i in range(len(rows))];active=set(range(len(rows)));bycol=[set()for _ in range(nv)]
    for i,row in enumerate(rr):
        for j in row:bycol[j].add(i)
    def valuation(a):
        v=0
        while a%prime==0:v+=1;a//=prime
        return v
    def witness(i,m):
        w=dict(modulus=m,rows=sorted([j,x%m]for j,x in ww[i].items()if x%m),value=bb[i]%m);check_sparse_modular(rows,rhs,nv,w);return w
    while active:
        empty=[i for i in active if not rr[i]]
        for i in empty:
            if bb[i]:return witness(i,modulus)
            active.remove(i)
        if not active:break
        choice=None
        for i in sorted(active):
            for j,a in rr[i].items():
                v=valuation(a)
                if choice is None or v<choice[0]:choice=(v,i,j)
                if v==0:break
            if choice[0]==0:break
        v,i,j=choice;divisor=prime**v;factor=pow(rr[i][j]//divisor,-1,modulus);rr[i]={k:a*factor%modulus for k,a in rr[i].items()};bb[i]=bb[i]*factor%modulus;ww[i]={k:a*factor%modulus for k,a in ww[i].items()};require(rr[i][j]==divisor,'local Smith pivot failed')
        if bb[i]%divisor:return witness(i,divisor)
        active.remove(i)
        for k in rr[i]:bycol[k].discard(i)
        for target in list(bycol[j]):
            require(target in active and rr[target][j]%divisor==0,'local Smith divisibility');q=rr[target][j]//divisor;bb[target]=(bb[target]-q*bb[i])%modulus
            for k,a in rr[i].items():
                z=(rr[target].get(k,0)-q*a)%modulus
                if z:rr[target][k]=z;bycol[k].add(target)
                elif k in rr[target]:del rr[target][k];bycol[k].discard(target)
            for k,a in ww[i].items():
                z=(ww[target].get(k,0)-q*a)%modulus
                if z:ww[target][k]=z
                elif k in ww[target]:del ww[target][k]
    return None

def check_sparse_modular(rows,rhs,nv,witness):
    m=witness['modulus'];require(type(m)is int and m>1,'invalid modulus');y=dict(witness['rows']);require(len(y)==len(witness['rows'])and all(0<=i<len(rows)and 0<x<m for i,x in y.items()),'bad modular witness');co=[0]*nv
    for i,x in y.items():
        for j,a in rows[i].items():co[int(j)]+=x*a
    value=sum(x*rhs[i]for i,x in y.items())%m;require(all(a%m==0 for a in co)and value!=0 and value==witness['value'],'modular witness failed');return True
